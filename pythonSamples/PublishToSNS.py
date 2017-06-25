import json
import boto3
#from urlparse import urlsplit

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    origKey = event['Records'][0]['s3']['object']['key'] 
    newKey = origKey.replace('inputs/','outputs/',1)
    srcBucket = event['Records'][0]['s3']['bucket']['name']
    #origKeyArr = urlsplit(origKey)
    message = {'newKey':newKey}
    print("value1 = " + origKey)
    s3Client = boto3.client('s3')
    myObj = s3Client.get_object(Bucket=srcBucket,Key=origKey)
    body = myObj['Body'].read()
    s3Client.put_object(Body=body, Bucket=srcBucket, Key=newKey)
    
    client = boto3.client('sns')
    response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:814129119746:demoTester',
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    return newKey # Echo back the first key value
    #raise Exception('Something went wrong')