# Author: Kushal Chokshi
# Date: 06/01/2019
# Function Name: MediaEvaluater
# Description: Function will generate the MediaInfo.
# Credit: MediaInfo

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import json
import xmltodict
import subprocess
import os
import uuid

# Generate a presigned URL for S3 Object
def get_presigned_url(expiration, objBucket, objKey):
    s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'virtual'}))
    Params={
        'Bucket': objBucket,
        'Key': objKey
    }
    print ('CORE:: Media Evaluator:: Bucket Name: ' + objBucket)
    print ('CORE:: Media Evaluator:: Object Key: ' + objKey)
    try:
        response = s3.generate_presigned_url('get_object', Params, ExpiresIn=expiration)
    except ClientError as e:
        print (e)
        raise
        return None
    return response

# Get MD5 from S3 Object Tag
def get_md5_from_objectTag(objBucket, objKey):
    s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'virtual'}))
    response = s3.get_object_tagging(
        Bucket=objBucket,
        Key=objKey
    )
    for tag in response['TagSet']:
        if tag['Key'] == 'MD5':
            md5 = tag['Value']
    return md5

# Evaluate the media using MediaInfo
def get_mediainfo(presignedURL):
    try:
        output = subprocess.check_output(["./mediainfo", "--full", "--output=JSON", presignedURL])
        json_output = json.loads(output)

        # Prepare the short media analysis JSON
        json_track = json_output['media']
        for f in json_track['track']:
            if f['@type'] == 'General':
                wrapper = f['Format']
                wrapperType = f['Format_Profile']
            if f['@type'] == 'Video':
                codec = f['Format']
                bitRate = f['BitRate']
                frameRate = f['FrameRate']
                #som = f['TimeCode_FirstFrame']
                width = f['Width']
                height = f['Height']
                framecount = f['FrameCount']
            if f['@type'] == 'Other' and f['Type'] == 'Time code':
                som = f['TimeCode_FirstFrame']
        mediaResult = {
            "Wrapper": wrapper + wrapperType,
            "Codec": codec,
            "BitRate": bitRate,
            "FrameRate": frameRate,
            "SOM": som,
            "Resolution": width + 'X' + height,
            "FrameCount": framecount
        }
    except Exception as e:
        print (e)
        raise
        return None
    return mediaResult

def lambda_handler(event, context):
    bucketName = event['bucketName']
    objectName = event['objectKey']
    signed_url = get_presigned_url(3600, bucketName, objectName)
    print ('CORE:: Media Evaluator:: Presigned URL: ' + signed_url)
    mediaAnalysis = get_mediainfo(signed_url)
    print('CORE:: Media Evaluator:: Parsed Media Analysis: ' + json.dumps(mediaAnalysis, indent=4))
    md5 = get_md5_from_objectTag(bucketName, objectName)
    print('CORE:: Media Evaluator:: MD5 Value from Object Tag: ' + md5)
    ingestData = {
        "MediaEvaluation": mediaAnalysis,
        "MD5": md5,
        "AssetID": objectName.partition(".")[0],
        "AssetUID": uuid.uuid4().hex,
        "Bucket": bucketName,
        "ObjectKey": objectName
    }
    return ingestData