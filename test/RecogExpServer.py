# -*- coding: utf-8 -*-
import sys, boto3
 
#args = sys.argv
#filename = args[1]
filename = 'picture/ex1.jpg' 

#boto3のclient作成、rekognitionとリージョンを指定
client = boto3.client('rekognition','us-east-1')
 
# 画像ファイルを読み込んでバイト列を取得
with open(filename, 'rb') as source_image:
    source_bytes = source_image.read()
 
# rekognitionのdetect_labelsにバイト列を渡してラベル検出実行
response = client.detect_faces(
               Image={
                   'Bytes': source_bytes
               },
               Attributes=['ALL']
)
 
print(response['FaceDetails'][0]['Emotions']) 
# 返ってきたresponseからラベル名(Name)と確度(Confidence)を整形して出力
#for label in response['FaceDetails']:
#    print("{Smile:30},{Confidence:.2f}%".format(**label))