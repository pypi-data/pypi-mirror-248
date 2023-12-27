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

from graphcode.credentials import GcCredentials
from graphcode.path import createDir
from graphcode.unittest import unitTest

from os import environ
from os.path import dirname, expanduser, abspath, exists

import time
from pytz import timezone
from datetime import datetime

from random import random

import multiprocessing
from multiprocessing import Manager
from multiprocessing import Process
from multiprocessing import Queue

import threading
from threading import Thread

import boto3
import uuid

from string import ascii_lowercase

import logging
from os.path import join

class awsS3():
  def __init__(self, credentialName = None, regionCode = None):
    self.__beginTime__ = time.time()
    
    if regionCode == None:
      self.regionCode = "us-west-2"
    else:
      self.regionCode = regionCode
    
    logDebug("connecting to S3 in {} with [{}]".format(self.regionCode, credentialName))
    self.s3Resource = None
    
    self.s3Client = self.connectS3(credentialName, self.regionCode)
    logging.info("initiated s3Client:[{}]".format(self.s3Client))
    
    #self.describeBucketsProcessTime = ModuProcessTime("describeBuckets")
    #self.listBucketsProcessTime = ModuProcessTime("listBuckets")
    #self.listObjectsProcessTime = ModuProcessTime("listObjects")
    #self.getObjectProcessTime = ModuProcessTime("getObject")
    #self.putObjectProcessTime = ModuProcessTime("putObject")
  
  def connectS3(self, credentialName = None, regionCode = None):
    if credentialName == None:
      errorMessage = "the credential name shouldn't be [{}]".format(credentialName)
      logError(errorMessage)
      raise ValueError(errorMessage)
    else:
      gcCrednital = GcCredentials()
      accessKey, secretKey = gcCrednital.get(credentialName)
    
    if regionCode == None:
      self.s3Client = boto3.client('s3',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name="us-west-2",
                        )
      self.s3Resource = boto3.resource('s3',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name="us-west-2",
                        )
    else:
      self.s3Client = boto3.client('s3',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name=regionCode,
                        )
      self.s3Resource = boto3.resource('s3',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name=regionCode,
                        )
    
    return self.s3Client
  
  def listBuckets(self):
    try:
      __beginTime__ = time.time()
      response = self.s3Client.list_buckets()
      __endTime__ = time.time()
      processingTime = __endTime__ - __beginTime__
      
      #self.describeBucketsProcessTime.updateTime(__endTime__, processingTime, response)
      
      '''
      if getLogLevel() == "UNITTEST":
        for key_1 in response.keys():
          if isinstance(response[key_1], dict):
            for key_2 in response[key_1]:
              logDebug( "[{}]:[{}]->[{}]".format(key_1, key_2, response[key_1][key_2]))
          elif isinstance(response[key_1], list):
            itemCount = 0
            for key_2 in response[key_1]:
              itemCount += 1
              logDebug( "[{}](#{}):[{}]".format(key_1, itemCount, key_2))
          else:
            logDebug( "[{}]->[{}]".format(key_1,response[key_1]))
      '''  
      return response["Buckets"]
    
    except Exception as e:
      errorMessage = "Error:[{}] -> unable to list table".format(e)
      logError(errorMessage)
      #raise ValueError(errorMessage)
    
      return None

  def deleteBucket(self, s3BucketName):
    try:
      __beginTime__ = time.time()
      logDebug("s3BucketName:[{}]".format(s3BucketName))
      
      response = self.s3Client.delete_bucket(Bucket=s3BucketName)
    
      return response
    except Exception as e:
      logException()
      raise ValueError(e)
    
    raiseValueError("An unexpected behavior happens")

  def createBucket(self, s3BucketName, regionCode = None, ACL='private'):
    response_list = []
    
    try:
      __beginTime__ = time.time()
      logDebug("s3BucketName:[{}], regionCode:[{}]".format(s3BucketName, regionCode))
      
      if regionCode == None:
        environ['AWS_DEFAULT_REGION'] = 'us-west-2'
        response = self.s3Client.create_bucket(ACL = ACL, Bucket=s3BucketName, CreateBucketConfiguration={'LocationConstraint': "us-west-2"},)
      else:
        response = self.s3Client.create_bucket(ACL = ACL, Bucket=s3BucketName, CreateBucketConfiguration={'LocationConstraint': regionCode},)
      response_list.append(response)
      
      __endTime__ = time.time()
      processingTime = __endTime__ - __beginTime__
      
      #self.describeBucketsProcessTime.updateTime(__endTime__, processingTime, response)
      
      '''
      if getLogLevel() == "UNITTEST":
        for key_1 in response.keys():
          if isinstance(response[key_1], dict):
            for key_2 in response[key_1]:
              logDebug( "[{}]:[{}]->[{}]".format(key_1, key_2, response[key_1][key_2]))
          elif isinstance(response[key_1], list):
            itemCount = 0
            for key_2 in response[key_1]:
              itemCount += 1
              logDebug( "[{}](#{}):[{}]".format(key_1, itemCount, key_2))
          else:
            logDebug( "[{}]->[{}]".format(key_1,response[key_1]))
      '''      
    except Exception as e:
      logException()
      errorMessage = "Error:[{}] -> unable to create new S3 bucket".format(e)
      logError(errorMessage)
      #raise ValueError(errorMessage)

    try:
      #Give the group log-delievery WRITE and READ_ACP permisions to the
      acl = self.s3Client.get_bucket_acl(Bucket=s3BucketName)
      logDebug("s3Bucket:[{}] -> acl:[{}]".format(s3BucketName, acl.keys()))
      
      modified_acl = {}
      for key in acl.keys():
        if key in ["Owner", "Grants", "Permission"]:
          modified_acl[key] = acl[key]
      
      new_grant = {
        'Grantee': {
          'URI': "http://acs.amazonaws.com/groups/s3/LogDelivery",
          'Type' : 'Group'
        },
        'Permission': 'FULL_CONTROL',
      }
  
      modified_acl['Grants'].append(new_grant)
  
      response = self.s3Client.put_bucket_acl(AccessControlPolicy = modified_acl, Bucket=s3BucketName)
      response_list.append(response)
      
      response = self.s3Client.put_bucket_logging(
        Bucket=s3BucketName,
        BucketLoggingStatus={
          'LoggingEnabled': {
            'TargetBucket': s3BucketName,
            'TargetPrefix': "__DO_NOT_DELETE_moduAWS_accessLog__/"
          }
        }
      )
      response_list.append(response)
      
    except:
      logException()
    
    
    try:
      response = self.s3Client.put_bucket_encryption(
        Bucket=s3BucketName,
        ServerSideEncryptionConfiguration={
          'Rules': [
            {
              'ApplyServerSideEncryptionByDefault': {
                  'SSEAlgorithm': 'AES256'
              }
            },
          ]
        }
      )
      response_list.append(response) 
    except:
      logException()
      
    try:
      response = self.s3Client.put_public_access_block(
        Bucket=s3BucketName,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
      )
      response_list.append(response) 
    except:
      logException()
    
    Rule = {'Expiration': {'Days': 1000}, 'ID': 'moduaws-default-lifecycle', 'Prefix':'', 'Status': 'Enabled', 'Transition': {'Days': 30, 'StorageClass': 'ONEZONE_IA'}, 'NoncurrentVersionTransition': {'NoncurrentDays': 30, 'StorageClass': 'ONEZONE_IA'}, 'NoncurrentVersionExpiration': {'NoncurrentDays': 60}, 'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 1}}
    try:
      response = self.s3Client.put_bucket_lifecycle(
          Bucket=s3BucketName,
          LifecycleConfiguration={
              'Rules': [Rule]
            }
          )
      response_list.append(response) 
    except:
      logException()
      
    try:
      response = self.s3Client.get_bucket_lifecycle(
            Bucket=s3BucketName
            )
      response_list.append(response)
      
      for key in response.keys():
        logDebug("{}:[{}]".format(key, response[key]))
    except:
      logException()
      
    return response_list
  
  def listObjects(self, bucketName, prefix = None, listAllObject = False):
    nextCount = 0
    contents_list = []
    nextContinuationToken = None
    while True:
      try:
        __beginTime__ = time.time()
        if prefix != None:
          if nextContinuationToken != None:
            response = self.s3Client.list_objects_v2(Bucket=bucketName, Prefix= prefix, ContinuationToken = nextContinuationToken)
          else:
            response = self.s3Client.list_objects_v2(Bucket=bucketName, Prefix= prefix)
        else:
          if nextContinuationToken != None:
            response = self.s3Client.list_objects_v2(Bucket=bucketName, ContinuationToken = nextContinuationToken)
          else:
            response = self.s3Client.list_objects_v2(Bucket=bucketName)
          
        __endTime__ = time.time()
        processingTime = __endTime__ - __beginTime__
        
        #size = len("{}".format(response["Contents"]))
        #self.listObjectsProcessTime.updateTime(__endTime__, processingTime, response, size)
        
        '''
        if getLogLevel() == "UNITTEST":
          for key_1 in response.keys():
            if isinstance(response[key_1], dict):
              for key_2 in response[key_1]:
                logDebug( "[{}]:[{}]->[{}]".format(key_1, key_2, response[key_1][key_2]))
            elif isinstance(response[key_1], list):
              itemCount = 0
              for key_2 in response[key_1]:
                itemCount += 1
                #logDebug( "[{}](#{}):[{}]".format(key_1, itemCount, key_2))
            else:
              logDebug( "[{}]->[{}]".format(key_1,response[key_1]))
        '''
        if "Contents" in response.keys():
          for item in response["Contents"]:
            #logDebug("item:[{}]".format(item))
            contents_list.append(item)
        else:
          for item in response.keys():
            logInfo("[{}]:[{}]".format(item, response[item]))
          
        isTruncated = response['IsTruncated']
        if listAllObject == True and isTruncated == True:
          nextContinuationToken = response['NextContinuationToken']
          logDebug("(#{}) isTruncated:[{}]->nextContinuationToken:[{}]".format(nextCount, isTruncated, nextContinuationToken))
          nextCount += 1
          continue
        else:
          logDebug("total {} objects are listed".format(len(contents_list)))
          break
    
      except Exception as e:
        logException("unable to list table")
        break
        #raise ValueError(errorMessage)
    
    return contents_list 

  def getObject(self, bucketName, key, decodeMode = 'utf-8', ttl= 5):
    try:
      __beginTime__ = time.time()
      
      response = self.s3Client.get_object(Bucket=bucketName, Key=key)
      try:
        logInfo("s3://{}/{}->response:[{}]".format(bucketName, key,response))
      except:
        logException("unexpected error")
      if decodeMode != None and decodeMode != "b": 
        #data = response["Body"].read(2451259158)
        data = response["Body"].read(2451259158)
      else:
        data = response["Body"].read()
      __endTime__ = time.time()
      processingTime = __endTime__ - __beginTime__
      
      #self.getObjectProcessTime.updateTime(__endTime__, processingTime, response)
      
      '''
      if getLogLevel() == "UNITTEST":
        for key_1 in response.keys():
          if isinstance(response[key_1], dict):
            for key_2 in response[key_1]:
              logDebug( "[{}]:[{}]->[{}]".format(key_1, key_2, response[key_1][key_2]))
          elif isinstance(response[key_1], list):
            itemCount = 0
            for key_2 in response[key_1]:
              itemCount += 1
              logDebug( "[{}](#{}):[{}]".format(key_1, itemCount, key_2))
          else:
            logDebug( "[{}]->[{}]".format(key_1,response[key_1]))
      '''
      
      try:
        if "midway/cookie" in key:
          logWarn("key:[{}]->LastModified:[{}]".format(key, response["LastModified"]))
          for line in data.split("\n"):
            for thisLine in line.split("\r"):
              logWarn("thisLine:[{}]".format(thisLine))
      except:
        logException("unexpected response:[{}]".format(response.keys()))
      
      return data
    
    except Exception as e:
      logException("bucketName:[{}] -> key:[{}]".format(bucketName, key))
    
      return None 
        
        
  def putObject(self, bucketName, key, data):
    try:
      __beginTime__ = time.time()
      response = self.s3Client.put_object(Bucket=bucketName,
            ACL='bucket-owner-full-control',
            Key=key, 
            Body=data,
            ServerSideEncryption='AES256')
      try:
        logInfo("s3://{}/{}->response:[{}]".format(bucketName, key,response))
      except:
        logException("unexpected error")
      
      __endTime__ = time.time()
      processingTime = __endTime__ - __beginTime__
      
      size = len(data)
      #self.putObjectProcessTime.updateTime(__endTime__, processingTime, response, size)
      
      '''
      if getLogLevel() == "UNITTEST":
        for key_1 in response.keys():
          if isinstance(response[key_1], dict):
            for key_2 in response[key_1]:
              logDebug( "[{}]:[{}]->[{}]".format(key_1, key_2, response[key_1][key_2]))
          elif isinstance(response[key_1], list):
            itemCount = 0
            for key_2 in response[key_1]:
              itemCount += 1
              logDebug( "[{}](#{}):[{}]".format(key_1, itemCount, key_2))
          else:
            logDebug( "[{}]->[{}]".format(key_1,response[key_1]))
      '''
      
      return data
    
    except Exception as e:
      errorMessage = "Error:[{}] -> unable to put data({:,}bytes) to s3://{}/{}".format(e, len(data), bucketName, key)
      logError(errorMessage)
      #raise ValueError(errorMessage)
    
      return None 
  
  def deleteObject(self, bucketName, objectKey):
    try:
      __beginTime__ = time.time()
      response = self.s3Client.delete_object(
          Bucket=bucketName,
          Key=objectKey
        )
      
      return response
    
    except Exception as e:
      errorMessage = "Error:[{}] -> unable to delete the object key:[{}] at s3Bucket:[{}]".format(e, objectKey, bucketName)
      logError(errorMessage)
      raise ValueError(errorMessage)
    
  def purgeBucket(self, s3BucketName):
    objectDetails_list = self.listObjects(bucketName = s3BucketName)
    
    while len(objectDetails_list) > 0:
      totalObjectNumber = len(objectDetails_list)
      if totalObjectNumber > 10:
        percentageDelimiter = int(totalObjectNumber/3)
      else:
        percentageDelimiter = 1
      
      objectCount = 0
      tList = []
      for objectDetails in objectDetails_list:
        try:
          objectCount += 1
          
          t = Thread(target=self.deleteObject, args=(s3BucketName, objectDetails["Key"],))
          t.start()
          tList.append(t)
          #self.deleteObject(bucketName = s3BucketName, objectKey = objectDetails["Key"])
          
          if (objectCount % percentageDelimiter) == 0:
            logDebug("(#{}/{} s3://{}/{} is deleted".format(objectCount, totalObjectNumber, s3BucketName, objectDetails["Key"]))
        except:
          logException()
      
      for t in tList:
        t.join()
      logInfo("The {} deleting tasks are completed".format(totalObjectNumber))
      
      objectDetails_list = self.listObjects(bucketName = s3BucketName)
    
    self.deleteBucket(s3BucketName)
    
    return True
  
  def uploadFileobject(self, f, bucketName, objectKey):
    response = self.s3Client.upload_fileobj(f, bucketName, objectKey)
    logInfo("res:[{}]".format(response))
    return response
  
  def downloadObject(self, bucketName, objectKey, downloadFilePath):
    response = self.s3Client.download_file(bucketName, objectKey, downloadFilePath)
    logInfo("res:[{}]".format(response))
    return response
 
def purgeS3Object(bucketName, key, credentialName = None):
  binaryData = False
  
  if credentialName == None:
    logDebug("credentialName:[{}] -> s3://{}/{} will not be download".format(credentialName, bucketName, key))
    return binaryData
  
  try:
    logDebug("connecting to S3:[{}]".format(bucketName))
    ryminS3Manager = awsS3(credentialName)
    logDebug("purging s3://{}/{}".format(bucketName, key))
    binaryData = ryminS3Manager.deleteObject(bucketName, key)
  except Exception as e:
    errorMessage = "Error:[{}] -> failed to delete s3://{}/{}".format(e, bucketName, key)
    logException(errorMessage)
    raise ValueError(errorMessage)
  
  return binaryData

 
def getS3Object(bucketName, key, credentialName = None, decodeMode = 'utf-8'):
  binaryData = None
  
  if credentialName == None:
    logDebug("credentialName:[{}] -> s3://{}/{} will not be download".format(credentialName, bucketName, key))
    return binaryData
  
  try:
    logDebug("connecting to S3:[{}]".format(bucketName))
    ryminS3Manager = awsS3(credentialName)
    logDebug("downloading s3://{}/{}".format(bucketName, key))
    binaryData = ryminS3Manager.getObject(bucketName, key)
  except Exception as e:
    errorMessage = "Error:[{}] -> failed to download s3://{}/{}".format(e, bucketName, key)
    logException(errorMessage)
    raise ValueError(errorMessage)
  
  return binaryData

def putS3Object(bucketName, key, data, credentialName = None):
  if credentialName == None:
    logDebug("credentialName:[{}] -> data:[len:({})] will not be uploaded to s3://{}/{}".format(credentialName, len("{}".format(data)), bucketName, key))
    return False
  
  try:
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    
    logInfo("connecting to S3://{}".format(bucketName))
    ryminS3Manager = awsS3(credentialName)
    
    logInfo("writing: data:[len:({:,}Bytes)]->s3://{}/{}".format(len("{}".format(data)), bucketName, key))
    ryminS3Manager.putObject(bucketName, key, data)
    
    logging.getLogger().setLevel(thisLogLevel)
  except Exception as e:
    errorMessage = "Error:[{}] -> failed to upload data:[{}] -> s3://{}/{}".format(e, data, bucketName, key)
    logError(errorMessage)
    raise ValueError(errorMessage)

  return True
          
def putS3Objects(object_list, bucketName = None, credentialName = None):
  if isinstance(credentialName, str) and isinstance(bucketName, str) :
    pass
  else:
    logDebug("bucketName:[{}] and credentialName:[{}] should be 'string'".format(bucketName, credentialName))
    return False
  
  try:
    logDebug("connecting to S3://{}".format(bucketName))
    ryminS3Manager = awsS3(credentialName)
  except:
    logException("unable to connect to S3://{}".format(bucketName))
    return False
      
  if isinstance(object_list, list) and len(object_list) > 0:
    for objectItems in object_list:
      if isinstance(objectItems, dict) and "filename" in objectItems.keys() and "key" in objectItems.keys():
        try:
          f = open(abspath(expanduser(objectItems["filename"])), "rb")
          data = f.read()
          #logDebug("filename:[{}] is loaded".format(objectItems["filename"]))
          
          #logUnitTest("writing: file:[{}]->s3://{}/{}".format(objectItems["filename"], bucketName, objectItems["key"]))
          ryminS3Manager.putObject(bucketName, objectItems["key"], data)
          #logDebug("completed to write: file:[{}]->s3://{}/{}".format(objectItems["filename"], bucketName, objectItems["key"]))
        except:
          logExceptionWithValueError("unable to copy file:[{}]->s3://{}/{}".format(objectItems["filename"], bucketName, objectItems["key"]))
          
      else:
        logDebug("objectItems:[{}] isn't valid".format(objectItems))
    else:
      logDebug("object_list:[{}] isn't valid".format(object_list))
      
def downloadS3Object(bucketName, key, destinationPath, credentialName = None):
  try:
    logDebug("connecting to S3://{}".format(bucketName))
    ryminS3Manager = awsS3(credentialName)
    
    return ryminS3Manager.downloadObject(bucketName, key, destinationPath)

  except:
    logException("unable to connect to S3://{}".format(bucketName))
    return False
      
def unitTest_listBuckets():
  ryminS3Manager = awsS3()
  ryminS3Manager.listBuckets()

def unitTest_createBucket():
  activeS3Bucket_list = []
  try:
    regionCode = "us-west-2"
    credentialName = "RYMIN-S3-FULL"
    ryminS3Manager = awsS3(credentialName, regionCode)
    '''
    for s3BucketName in ryminS3Manager.listBuckets():
      if s3BucketName["Name"].startswith("moduaws-"):
        try:
          s3Response = ryminS3Manager.purgeBucket(s3BucketName["Name"])
          logInfo("s3Response:[{}]".format(s3Response))
        except Exception as e:
          logException("unable to delete s3Bucket:[{}]".format(s3BucketName["Name"]))
      else:
        activeS3Bucket_list.append(s3BucketName["Name"])
        logDebug("s3BucketName:[{}] is added".format(s3BucketName["Name"]))
    '''
  except:
    logException()
  logInfo("total {} s3 buckets are found in regionCode:[{}]".format(len(activeS3Bucket_list), regionCode))
  
  try:
    regionCode = "us-west-2"
    
    targetS3BucketName_list = ["rymin-repository"] #["moduaws-repository", "moduaws-request-queue"]
    if len(targetS3BucketName_list) > 0:
      for s3BucketName in targetS3BucketName_list:
        try:
          ryminS3Manager.createBucket(s3BucketName)
        except:
          logError("unable to create the S3 Bucket Name:[{}]".format(s3BucketName))
          logException()
    else:
      for indexCount in ascii_lowercase:
        s3BucketName = "rymin-" + "{}".format(indexCount)
        if s3BucketName in activeS3Bucket_list:
          logInfo("s3BucketName:[{}] is existing in regionCode:[{}]".format(s3BucketName, regionCode))
        else:
          logInfo("creating s3BucketName:[{}] in regionCode:[{}]".format(s3BucketName, regionCode))
          
          try:
            ryminS3Manager.createBucket(s3BucketName)
          except:
            logException("unable to create the S3 Bucket Name:[{}]".format(s3BucketName))
  
  except Exception as e:
    logException()
    errorMessage = "Error:[{}] -> failed to create S3://{}".format(e, s3BucketName, regionCode)
    logError(errorMessage)
    raise ValueError(errorMessage)
  
  try:
    ryminS3Manager = awsS3(credentialName)
    
    s3BucketCount = 0
    for s3BucketName in ryminS3Manager.listBuckets():
      s3BucketCount += 1
      logDebug("[{}] s3BucketName:[{}]".format(s3BucketCount, s3BucketName))
  except:
    logException()


def unitTest_listObjects():
  ryminS3Manager = awsS3()
  for bucketItems in ryminS3Manager.listBuckets():
    bucketName = bucketItems["Name"]
    ryminS3Manager.listObjects(bucketName)
    break

def unitTest_getObject():
  ryminS3Manager = awsS3()
  
  bucketItems_list = ryminS3Manager.listBuckets()
  logDebug( "#ofBuckets:[{}]".format(len(bucketItems_list)))
  
  lastBucketName = bucketItems_list[-1]["Name"]
  logDebug( "lastBucketName:[{}]".format(lastBucketName))
  
  objectItems_list = ryminS3Manager.listObjects(lastBucketName)
  logDebug( "#ofObjects:[{}]".format(len(objectItems_list)))
  
  lastObjectKey = objectItems_list[-1]["Key"]
  logDebug( "lastBucketName:[{}]->lastObjectKey:[{}]".format(lastBucketName, lastObjectKey))
  
  data = ryminS3Manager.getObject(lastBucketName, lastObjectKey)
  logDebug( "data:[{}]".format(data))

def unitTest_putObject():
  ryminS3Manager = awsS3()

  bucketItems_list = ryminS3Manager.listBuckets()
  logDebug( "#ofBuckets:[{}]".format(len(bucketItems_list)))
  
  lastBucketName = bucketItems_list[-1]["Name"]
  logDebug( "lastBucketName:[{}]".format(lastBucketName))
  
  objectItems_list = ryminS3Manager.listObjects(lastBucketName)
  logDebug( "#ofObjects:[{}]".format(len(objectItems_list)))
  
  lastObjectKey = objectItems_list[-1]["Key"]
  logDebug( "lastBucketName:[{}]->lastObjectKey:[{}]".format(lastBucketName, lastObjectKey))
  
  data = ryminS3Manager.getObject(lastBucketName, lastObjectKey)
  logDebug( "data:[{}]".format(data))

  #fileName = "/Users/hoeseong/raonCSV/updateItem_2019-08-29T19-45-56-986676Z.csv"
  
  #f = open(fileName, "rb")
  #data = f.read()
  ryminS3Manager.putObject(lastBucketName, "unitTest_putObject.txt", data)
  
def unitTest_moduAWS_Put_Get():
  ryminS3Manager = awsS3(credentialName = "PLUS-MODUAWS-S3", regionCode = "us-east-1")
  
  template_dict = {
    "test": "/Users/hoeseong/Downloads/c853227a-81d2-45bf-a63a-2df11550237d.json",
    "[CDO] Redshift Analysis":"/Users/hoeseong/eclipse-workspace/moduAWSv9.5/template_cdo_redhisft_analysis.json"
    }
  
  fileName = template_dict["test"]
  #fileName = template_dict["[CDO] Redshift Analysis"]
  
  f = open(fileName, "rb")
  data = f.read()
  ryminS3Manager.putObject("moduaws-input-queue", "256455912682/{}/{}".format("hoeseong", uuid.uuid4()), data)
  
  #data = ryminS3Manager.getObject("moduaws-output-queue", "256455912682/image.png")
  #logDebug( "data:[{}]".format(data))

def unitTest_2GBDownload():
  data = downloadS3Object("pao-bi", "moduAWS/athena_output/24a2d2a9-cb2c-4ada-9116-60590c1afb1d.csv", expanduser("~/Downloads/a.csv"), "S3-MODUAWS-PAO-BI")
  
def localUnitTest():
  unitTestFunction_dict = [#{"target":unitTest_listBuckets, "args":()},
                           #{"target":unitTest_listObjects, "args":()},
                           #{"target":unitTest_getObject, "args":()},
                           #{"target":unitTest_putObject, "args":()},
                           #{"target":unitTest_listObjectsPaoBI, "args":()},
                           #{"target":unitTest_createBucket, "args":()},
                           #{"target":unitTest_2GBDownload, "args":()},,
                           {"target":unitTest_moduAWS_Put_Get, "args":()},
                           ]
  
  unitTest(unitTestFunction_dict)

if __name__ == "__main__":
  
  
  localUnitTest()
  
  
