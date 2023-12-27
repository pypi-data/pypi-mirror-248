'''
Copyright (c) 1998-2124 Ryeojin Moon
Copyright (c) 2020-2124 GraphCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

THIS SOFTWARE IS NOT PROVIDED TO ANY ENTITY OR ANY GROUP OR ANY PERSON
TO THREATEN, INCITE, PROMOTE, OR ACTIVELY ENCOURAGE VIOLENCE, TERRORISM,
OR OTHER SERIOUS HARM. IF NOT, THIS SOFTWARE WILL NOT BE PERMITTED TO USE.
IF NOT, THE BENEFITS OF ALL USES AND ALL CHANGES OF THIS SOFTWARE ARE GIVEN
TO THE ORIGINAL AUTHORS WHO OWNED THE COPYRIGHT OF THIS SOFTWARE  ORIGINALLY.
THE CONDITIONS CAN ONLY BE CHANGED BY THE ORIGINAL AUTHORS' AGREEMENT
IN AN ADDENDUM, THAT MUST BE DOCUMENTED AND CERTIFIED IN FAIRNESS MANNER.
===
Created by Jan 1, 2011
Modified by Jan 1, 2023

@contributor: hoeseong
'''
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from pathway import requests, updateMsg
from wooju.args import getInputs, getAccountId, getIAMRoleName

from tammy.midway import PdxMidway

import time

import json

import logging

import boto3
import botocore


def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "__file__": __file__
      }
  except:
    response_dict = {
      "apiName": request_dict["apiName"],
      "state":"FAILED",
      "errorReasons":[logException("apiName:[{}] failed".format(request_dict["apiName"]))],
      "__file__": __file__
      }

  return response_dict

def action(request_dict):
  logMessage_list = []
  errorReason_list = []
  
  try:
    result_list = runAPIOverAssumeRole(request_dict, errorReason_list, logMessage_list)
      
  except Exception as e:
    updateMsg(errorReason_list, logException("unexpected request_dict:[{}]".format(request_dict)))
  
  return {
    "createdS3Buckets": result_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def createBucket(s3Resource, userAccountId, userName, postfix):
  bucketName = '{}-{}-{}'.format(userAccountId, userName, postfix)
  
  # Check if the bucket already exists
  isExistBucket = True
  try:
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    s3Resource.meta.client.head_bucket(Bucket=bucketName)
    logging.getLogger().setLevel(thisLogLevel)
  except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        isExistBucket = False
  
  # If the bucket does not exist, create it
  if not isExistBucket:
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    s3Resource.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
    logDebug(f'Bucket {bucketName} created.')
    logging.getLogger().setLevel(thisLogLevel)
    
    return bucketName
  
  else:
    raiseValueError(f'Bucket {bucketName} already exists.')

def applyServerSideEncryption(s3Client, userAccountId, userName, postfix):
  bucketName = '{}-{}-{}'.format(userAccountId, userName, postfix)
    
  try:
    encryptionRule = {
        'Rules': [
          {
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
          },
        ]
      }
    # Enable server-side encryption
    
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    s3Client.put_bucket_encryption(
      Bucket=bucketName,
      ServerSideEncryptionConfiguration=encryptionRule
      )
    logging.getLogger().setLevel(thisLogLevel)

    return encryptionRule
    
  except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    raiseValueError("failed to apply server-size encryption:{}:[{}]".format(e.response['Error']['Code'], e))

def putBucketPolicy(s3Client, userAccountId, userName, postfix):
  bucketName = '{}-{}-{}'.format(userAccountId, userName, postfix)
  
  try:
    if postfix in ["midway"]:
      bucketPolicy = {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Sid": "AddCannedAcl",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::900629971091:user/moduaws-x-midway-access"
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::{}-{}-midway/cookie".format(userAccountId, userName)
          }
        ]
      }
    elif postfix in ["moduaws"]:
      bucketPolicy = {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "AddCannedAcl",
              "Effect": "Allow",
              "Principal": {
                "AWS": "arn:aws:iam::900629971091:user/moduaws-codecommit-user"
              },
              "Action": [
                "s3:PutObject"
              ],
              "Resource": "arn:aws:s3:::{}-{}-moduaws/*".format(userAccountId, userName)
            }
          ]
        }
    elif postfix in ["repository"]:
      bucketPolicy = {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Sid": "AddCannedAc-Repository",
            "Effect": "Allow",
            "Principal": {
              "AWS": "arn:aws:iam::900629971091:user/moduaws-x-midway-access"
              },
            "Action": "s3:GetObject",
            "Resource": [
              "arn:aws:s3:::{}-{}-repository/*".format(userAccountId, userName),
              ]
            },
          {
            "Sid": "AddCannedAc-moduAWS_X",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::900629971091:user/moduaws-codecommit-user"
              },
            "Action": "s3:PutObject",
            "Resource": [
              "arn:aws:s3:::{}-{}-repository/*".format(userAccountId, userName),
              ]
            }
          ]
        }
    # Convert the policy to a JSON string
    bucketPolicy_string = json.dumps(bucketPolicy)
    
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    # Set the bucket policy
    s3Client.put_bucket_policy(
        Bucket=bucketName,
        Policy=bucketPolicy_string
    )
    logging.getLogger().setLevel(thisLogLevel)
    
    return bucketPolicy
  
  except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    raiseValueError("failed to put bucket policy:{}:[{}]".format(e.response['Error']['Code'], e))
    
    
def runAPIOverAssumeRole(request_dict, errorReason_list, logMessage_list):
  input_dict = getInputs(request_dict)
  
  userName = request_dict["metadata"]["userName"]
  
  try:
    accountId = getAccountId(input_dict)
    iamRoleName = getIAMRoleName(input_dict)
  except:
    accountId = request_dict["metadata"]["awsAccountId"]
    iamRoleName = "Admin"
  
    
  result_dict = requests(
      request_dict = {
          **request_dict,
          "attributes":{
            "accountId": accountId,
            "iamRoleName": iamRoleName
            },
          "apiName":"tammy.isengard.describeAssumeRoleCredential"
        }
      )
  
  isengardCrendential_dict = json.loads(result_dict["response"]["assumeRoleResult"][0]["AssumeRoleResult"])
  
  for key in isengardCrendential_dict.keys():
    logDebug("{}:[{}]".format(key, isengardCrendential_dict[key]))
             
  thisResult_list = []
  try:
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    curAssumedStsClient=boto3.client(
        'sts',
        aws_access_key_id=isengardCrendential_dict["credentials"]['accessKeyId'],
        aws_secret_access_key=isengardCrendential_dict["credentials"]['secretAccessKey'],
        aws_session_token=isengardCrendential_dict["credentials"]['sessionToken'],
    )
    logInfo("assumedAccountId:[{}]".format(curAssumedStsClient.get_caller_identity().get('Account')))
    logging.getLogger().setLevel(thisLogLevel)
    
    try:
      thisLogLevel = logging.getLogger().level
      logging.getLogger().setLevel(logging.INFO)
      session = boto3.Session(
        aws_access_key_id=isengardCrendential_dict["credentials"]['accessKeyId'],
        aws_secret_access_key=isengardCrendential_dict["credentials"]['secretAccessKey'],
        aws_session_token=isengardCrendential_dict["credentials"]['sessionToken'],
        region_name="us-west-2",
      )
      logging.getLogger().setLevel(thisLogLevel)
      
      try:
        thisLogLevel = logging.getLogger().level
        logging.getLogger().setLevel(logging.INFO)
        s3Resource = session.resource('s3')
        s3Client = session.client('s3')
        logging.getLogger().setLevel(thisLogLevel)
        
        try:
          logWarn("credential is expired in {:,} seconds".format(int(isengardCrendential_dict["credentials"]["expiration"]/1000 - time.time())))
          # List all buckets
          for bucket in s3Resource.buckets.all():
            logDebug("s3://{}/".format(bucket.name))
          
          for postfix in ["midway", "moduaws", "repository"]:
            try:
              bucketName = createBucket(s3Resource, accountId, userName, postfix)
              state = "CREATED"
            except:
              bucketName = '{}-{}-{}'.format(accountId, userName, postfix)
              state = "UPDATED"
              
            encryptionRule = applyServerSideEncryption(s3Client, accountId, userName, postfix)
            bucketPolicy = putBucketPolicy(s3Client, accountId, userName, postfix)
            
            thisResult_list.append(
              {
                "s3bucketName": bucketName,
                "encryptionRule": encryptionRule,
                "bucketPolicy": bucketPolicy,
                "state":state
                }
              )
          
        except:
          updateMsg(errorReason_list, logException("failed to provision s3://{}-{}-[midway,moduaws]".format(accountId, userName)))
      except:
        updateMsg(errorReason_list, logException("unable to initiate 'athenaBoto3Client' with 'bubblewandCrendentials'"))
    except:
      updateMsg(errorReason_list, logException("unable to initiate 'athenaBoto3Client' with 'bubblewandCrendentials'"))
  except:
    updateMsg(errorReason_list, logException("unable to initiate 'assumeStsClient' with 'bubblewandCrendentials'"))
    
  return thisResult_list