from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from .models import UserCondition, User, Photo
from .serializer import UserConditionSerializer
from django.shortcuts import render, redirect
import subprocess
import requests
import json
import sys, boto3
from django.utils import timezone

from ml_prediction import model


import json
import numpy as np
from soracom import soracom

from .forms import PhotoForm
from .models import Photo


'''
def manual(request):
    context = {}
    return render(request, 'manual.html', context)
'''

def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html', {
            'form': PhotoForm(),
        })

    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        photo = Photo()
        photo.image = form.cleaned_data['image']
        photo.pub_date = timezone.now()
        photo.save()

        return redirect('/result/predict')


    '''
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        #user_name = form.cleaned_data['user_name']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})
    '''



class PredictedViewSet(viewsets.ModelViewSet):
    queryset = UserCondition.objects.all()
    serializer_class = UserConditionSerializer

    def get_weather(self):
        #天気取得
        API_KEY = "5b9e6b9dc9b04f08658b93966331a043"
        api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"

        city_name = 'Tokyo'
        url = api.format(city = city_name, key = API_KEY)
        response = requests.get(url)
        data = json.loads(response.text)

        #天気情報
        weather = data["weather"][0]["description"]
        #最高気温
        temp_max = data["main"]["temp_max"]
        #最低気温
        temp_min = data["main"]["temp_min"]
        #寒暖差
        diff_temp = temp_max - temp_min
        #湿度
        humidity = data["main"]["humidity"]

        return weather, temp_max, temp_min, diff_temp, humidity

    def get_expression(self, image_file):
        # -*- coding: utf-8 -*-

        #args = sys.argv
        #filename = args[1]

        #boto3のclient作成、rekognitionとリージョンを指定
        client = boto3.client('rekognition','us-east-1')

        # 画像ファイルを読み込んでバイト列を取得
        source_bytes = image_file.read()
        '''
        with open(filename, 'rb') as source_image:
            source_bytes = source_image.read()
        '''

        # rekognitionのdetect_labelsにバイト列を渡してラベル検出実行
        response = client.detect_faces(
                       Image={
                           'Bytes': source_bytes
                       },
                       Attributes=['ALL']
        )

        print(response['FaceDetails'][0]['Emotions'])

        expression_dist = {}

        max = 0.0
        max_expressiopn = None
        for elem in response['FaceDetails'][0]['Emotions']:
            expression_dist[elem["Type"]] = elem['Confidence']
            if elem['Confidence'] > max:
                max = elem['Confidence']
                max_expression = elem['Type']

        expression_dist['SMILE'] = response['FaceDetails'][0]['Smile']['Value']

        return expression_dist, max_expression

    def similarity(self, imageSource, imageTarget):

        confidence = 0

        client=boto3.client('rekognition', 'us-east-1')

        response=client.compare_faces(SimilarityThreshold=70,
                                      SourceImage={'Bytes': imageSource.read()},
                                      TargetImage={'Bytes': imageTarget.read()})

        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            confidence = faceMatch['Face']['Confidence']
            print('The face at ' +
                   str(position['Left']) + ' ' +
                   str(position['Top']) +
                   ' matches with ' + str(confidence) + '% confidence')

        return confidence

    '''
    def ml_predict(self, expression):
        condition = None

        if expression == "HAPPY":
            condition = 0
        elif expression == "CALM" or expression == "SAD":
            condition = 1
        else:
            condition = 2

        return condition
    '''

    #http://<host_name>/api/predict
    @list_route(methods=["get"])
    def predict(self, request):
        #read POST params
        user_list = User.objects.order_by('-name')

        pictured_user = None

        for user in user_list:
            image_file = Photo.objects.order_by('-pub_date')[0].image
            confidence = self.similarity(user.image, image_file)
            if confidence > 70:
                #user_name = user.name
                pictured_user = user
                print("DEBUG:name",pictured_user.name)
                break

            image_file.close()

        if pictured_user != None:

            image_file = Photo.objects.order_by('-pub_date')[0].image

            #Get Expression
            expression_dist, expression = self.get_expression(image_file)
            #Get Weather
            weather, temp_max, temp_min, diff_tmp, humidity = self.get_weather()
            #Get Sensor Data
            data = json.loads(soracom.getSoracom())

            #DEBUG (Sensor Data)
            print('Sensor_Data')
            print(data)
            print('照度', data['lightSener'])
            print('心拍数', data['heartRate'])

            #register data to database for model construction
            record = UserCondition(user_name = pictured_user.name,  # 1対多対応
                expression = expression,
                weather = weather,
                temp_max = temp_max,
                temp_min = temp_min,
                diff_tmp = diff_tmp,
                humidity = humidity,
                predicted = None)
            record.save()

            #prediction
            #predicted = model.predict(argument)
            feature = np.array([expression_dist['HAPPY'], expression_dist['SAD'], expression_dist['ANGRY'],
                expression_dist['CONFUSED'], expression_dist['DISGUSTED'], expression_dist['SURPRISED'], expression_dist['CALM'],
                expression_dist['SMILE'], data['lightSener'], data['heartRate']], dtype="float64")
            predicted = model.getMood(feature)


            record.predicted = predicted
            print("DEBUG", record.expression)

            #model update based on the result
            #mode.update()

            #create serializer
            serializer = self.get_serializer(record)

            #register condition of User
            pictured_user.predicted = predicted
            pictured_user.save()

        context = {'user_list': user_list, 'data' : data, 'expression_dist' : expression_dist}

        return render(request, 'result.html',context)
        #return Response(serializer.data, status=status.HTTP_200_OK)

'''
class CreateModel(viewsets.ModelViewSet):
    def updateModel():

'''
