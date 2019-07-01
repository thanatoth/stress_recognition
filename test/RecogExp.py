import sys, boto3
 
args = sys.argv
 
if __name__ == "__main__":
    fileName=args[2]
    bucket=args[1]
 
    client=boto3.client('rekognition','ap-northeast-1a')
 
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
    #response = client.detect_labels(Image={'S3Object':{'Bucket':'kdgatest','Name':'ex2.jpg'}})
 
    print('Detected labels for ' + fileName)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))