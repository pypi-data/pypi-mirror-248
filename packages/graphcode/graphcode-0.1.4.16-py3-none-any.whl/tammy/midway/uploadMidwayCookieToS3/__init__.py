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

from tammy.midway.midwayCookieHandler import PdxMidwayCookieHandler

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
  
  midwayCookie_list = updateMidwayCookieCache(request_dict, errorReason_list, logMessage_list)
  uploadMidwayCookieToS3Result_list = uploadMidwayCookieToS3(request_dict, errorReason_list, logMessage_list)
  logDebug("uploadMidwayCookieToS3Result_list:[{}]".format(uploadMidwayCookieToS3Result_list))
  
  return {
    "midwayCookie": midwayCookie_list,
    "uploadMidwayCookieToS3Result": uploadMidwayCookieToS3Result_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def updateMidwayCookieCache(request_dict, errorReason_list, logMessage_list):
  midwayCookie_list = []
  
  try:
    midwayCookieSource = request_dict["attributes"]["midwayCookieSource"]
  except:
    midwayCookieSource = "unknown"
    
  try:
    pdxMidwayCookieHandler = PdxMidwayCookieHandler(
      userAccountId= request_dict["metadata"]["awsAccountId"], 
      loginAliasId= request_dict["metadata"]["userName"]
      )
    
    midwayCookie_dict = pdxMidwayCookieHandler.getMidwayCookie(request_dict["attributes"]["midwayCookie"])
    for partition in midwayCookie_dict.keys():
      for key in midwayCookie_dict[partition].keys():
        if isinstance(midwayCookie_dict[partition][key], str) and len(midwayCookie_dict[partition][key]) > 256:
          midwayCookie_list.append(
            {
              "key":"{}.{}".format(partition, key),
              "value":"{}...(redacted)...{} (len:{:,})".format(midwayCookie_dict[partition][key][:10], 
                                                             midwayCookie_dict[partition][key][-10:], 
                                                             len(midwayCookie_dict[partition][key])
                                                             ),
              "midwayCookieSource": midwayCookieSource
              }
            )
        else:
          if isinstance(midwayCookie_dict[partition][key], dict):
            for key2 in midwayCookie_dict[partition][key].keys():
              if isinstance(midwayCookie_dict[partition][key][key2], str) and len(midwayCookie_dict[partition][key][key2]) > 256:
                midwayCookie_list.append(
                  {
                    "key":"{}.{}.{}".format(partition, key, key2),
                    "value":"{}...(redacted)...{} (len:{:,})".format(midwayCookie_dict[partition][key][key2][:10], 
                                                                   midwayCookie_dict[partition][key][key2][-10:], 
                                                                   len(midwayCookie_dict[partition][key][key2])
                                                                   ),
                    "midwayCookieSource": midwayCookieSource
                    }
                  )
              else:
                midwayCookie_list.append(
                  {
                    "key":"{}.{}.{}".format(partition, key, key2),
                    "value":"{}".format(midwayCookie_dict[partition][key][key2]),
                    "midwayCookieSource": midwayCookieSource
                    }
                  )
          else:
            midwayCookie_list.append(
              {
                "key":"{}.{}".format(partition, key),
                "value":"{}".format(midwayCookie_dict[partition][key]),
                "midwayCookieSource": midwayCookieSource
                }
              )
              
  except:
    updateMsg(errorReason_list, logException("unexpected request_dict:[{}]".format(request_dict)))
    
  return midwayCookie_list

def uploadMidwayCookieToS3(request_dict, errorReason_list, logMessage_list):
  input_dict = getInputs(request_dict)
  
  userName = request_dict["metadata"]["userName"]
  
  try:
    midwayCookieSource = request_dict["attributes"]["midwayCookieSource"]
  except:
    midwayCookieSource = "unknown"
    
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
          bucketName = '{}-{}-midway'.format(accountId, userName)
          objectKey = "cookie"
          try:
            midwayCookie = request_dict["attributes"]["midwayCookie"]
            
            # Upload the data
            try:
              logDebug("uploading midway cookie(len:{:,}) at s3://{}/{}".format(len(midwayCookie), bucketName, objectKey))
              s3Resource.Bucket(bucketName).put_object(Key=objectKey, Body=midwayCookie)
              state = "UPLOADED"
                
            except Exception as e:
              updateMsg(errorReason_list, logException("failed to upload s3://{}/{}->Error:[{}]".format(bucketName, objectKey, e)))
              state = "FAILED"
          except:
            updateMsg(errorReason_list, logException("midwayCookie not found attributes:[{}]".format(request_dict["attributes"])))
            state = "FAILED"
          
          thisResult_list.append(
            { 
              "bucketName": bucketName,
              "objectKey": objectKey,
              "size": len(midwayCookie),
              "state":state,
              "midwayCookieSource":midwayCookieSource
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