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
#from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from rymin.credentials import getCredentials
from rymin.path import createDir
from rymin.unittest import unitTest
from rymin.y2y.awsS3 import purgeS3Object, downloadS3Object

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
  
class awsAthena():
  def __init__(self, credentialName = None, regionCode = None):
    self.__beginTime__ = time.time()
    
    if regionCode == None:
      self.regionCode = "us-west-2"
    else:
      self.regionCode = regionCode
    
    logDebug("connecting to Athena in {} with [{}]".format(self.regionCode, credentialName))
    self.athenaClient = self.connectAthena(credentialName, self.regionCode)
    
  
  def connectAthena(self, credentialName = None, regionCode = None):
    if credentialName == None:
      errorMessage = "the credential name shouldn't be [{}]".format(credentialName)
      logError(errorMessage)
      raise ValueError(errorMessage)
    else:
      accessKey, secretKey = getCredentials(credentialName)
    
    if regionCode == None:
      self.athenaClient = boto3.client('athena',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name="us-west-2",
                        )

    else:
      self.athenaClient = boto3.client('athena',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name=regionCode,
                        )

    return self.athenaClient
  
  def queryDatabases(self, database, query, s3BucketName, s3Prefix ):
    try:
      __beginTime__ = time.time()
      response = self.athenaClient.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': 's3://pao-bi/moduAWS/athena_output/'
        }
      )
      processingTime = time.time() - __beginTime__
      
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
      
      return response["QueryExecutionId"]
    
    except Exception as e:
      errorMessage = "Error:[{}] -> unable to list table".format(e)
      logError(errorMessage)
    
    return None

  def waitForResult(self, queryExecutionId, timeout = 300):
    state = 'RUNNING'

    try:
      while (timeout > 0 and queryExecutionId != None and state in ['RUNNING', 'QUEUED']):
          timeout = timeout - 1
          response = self.athenaClient.get_query_execution(QueryExecutionId = queryExecutionId)
  
          if 'QueryExecution' in response and \
                  'Status' in response['QueryExecution'] and \
                  'State' in response['QueryExecution']['Status']:
              state = response['QueryExecution']['Status']['State']
              if state == 'FAILED':
                  return False
              elif state == 'SUCCEEDED':
                  s3Path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
                  logInfo("state:[{}]->s3Path:[{}] for queryExecutionId:[{}]".format(state, s3Path, queryExecutionId))
                  
                  return s3Path
                
          time.sleep(1)
    except:
      logException("unable to get the result from Athena with queryExecutionId:[{}]".format(queryExecutionId))
    
    return False
  
  def writeResult(self, destinationFilePath, queryExecutionId, timeout = 300):
    s3Path = self.waitForResult(queryExecutionId, timeout)
    s3BucketName = s3Path[5:s3Path.find("/", 5)]
    s3Key = s3Path[s3Path.find("/", 5)+1:]
            
    data = downloadS3Object(s3BucketName, s3Key, destinationFilePath, credentialName = "ATHENA-MODUAWS")
    purgeS3Object(s3BucketName, s3Key, credentialName = "ATHENA-MODUAWS")
    purgeS3Object(s3BucketName, "{}.metadata".format(s3Key), credentialName = "ATHENA-MODUAWS")
      
    return data
          

def unitTest_simpleQueryToAthena():
  athenaManager = awsAthena(credentialName = "ATHENA-MODUAWS", regionCode = "us-east-1")
  
  database = "pao_bi"
  query = "SELECT * FROM cdo_case_support LIMIT 100"
  s3BucketName = "pao-bi"
  s3Prefix = "moduAWS/athena_output/"
  queryExecutionId = athenaManager.queryDatabases(database, query, s3BucketName, s3Prefix)

  logInfo("QueryExecutionId:[{}]".format(queryExecutionId))
  
  result = athenaManager.getResult(queryExecutionId)
  logInfo("result:[{}]".format(result))
  
def unitTest_writeResultOfQueryToAthena():
  athenaManager = awsAthena(credentialName = "ATHENA-MODUAWS", regionCode = "us-east-1")
  
  database = "pao_bi"
  query = "SELECT * FROM cdo_case_support LIMIT 100"
  s3BucketName = "pao-bi"
  s3Prefix = "moduAWS/athena_output/"
  queryExecutionId = athenaManager.queryDatabases(database, query, s3BucketName, s3Prefix)

  logInfo("QueryExecutionId:[{}]".format(queryExecutionId))
  
  result = athenaManager.writeResult(path.expanduser("~/Downloads/athena.csv"), queryExecutionId) #this is in the unittest
  
  logInfo("result:[{}]".format(result))

def unitTest_writeResultOfQueryToAthenaOldCases():
  athenaManager = awsAthena(credentialName = "ATHENA-MODUAWS", regionCode = "us-east-1")
  
  database = "pao_bi"
  query = "select * from AwsDataCatalog.pao_bi.cdo_case_support_v2_for_languished_cases where AccountPod = 'WWOps' and caseStatus != 'Resolved' and caseAgeDays >= 30 order by caseAgeDays DESC"
  s3BucketName = "pao-bi"
  s3Prefix = "moduAWS/athena_output/"
  queryExecutionId = athenaManager.queryDatabases(database, query, s3BucketName, s3Prefix)

  logInfo("QueryExecutionId:[{}]".format(queryExecutionId))
  
  result = athenaManager.writeResult(path.expanduser("~/Downloads/athena.csv"), queryExecutionId) #this is in the unittest
  
  logInfo("result:[{}]".format(result))
  
   
def localUnitTest():
  currentLogLevel = getLogLevel()
  setLogLevel('UNITTEST')
  unitTestFunction_dict = [#{"target":unitTest_simpleQueryToAthena, "args":()},
                           #{"target":unitTest_writeResultOfQueryToAthena, "args":()},
                           {"target":unitTest_writeResultOfQueryToAthenaOldCases, "args":()},
                           #{"target":unitTest_putObject, "args":()},
                           #{"target":unitTest_listObjectsPaoBI, "args":()},
                           #{"target":unitTest_createBucket, "args":()},
                           ]
  
  unitTest(unitTestFunction_dict)
  
  setLogLevel(currentLogLevel)

if __name__ == "__main__":
  
  
  localUnitTest()
  
  # Retrieve the list of existing buckets


  