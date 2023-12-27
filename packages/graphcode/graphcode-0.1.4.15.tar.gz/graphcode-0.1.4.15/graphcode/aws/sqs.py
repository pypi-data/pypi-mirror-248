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

from rymin.credentials import getCredentials

from rymin.unittest import unitTest

import random

import boto3

class awsSQS():
  def __init__(self, credentialName = None, regionCode = None):
    self.__beginTime__ = time.time()
    
    self.msgId_list = []
    
    if regionCode == None:
      self.regionCode = "us-east-1"
    else:
      self.regionCode = regionCode
    
    logDebug("connecting to S3 in {} with [{}]".format(self.regionCode, credentialName))
    self.sqsClient = self.connectSQS(credentialName, self.regionCode)
    
    #self.describeBucketsProcessTime = ModuProcessTime("describeBuckets")
    #self.listBucketsProcessTime = ModuProcessTime("listBuckets")
    #self.listObjectsProcessTime = ModuProcessTime("listObjects")
    #self.getObjectProcessTime = ModuProcessTime("getObject")
    #self.putObjectProcessTime = ModuProcessTime("putObject")
  
  def connectSQS(self, credentialName = None, regionCode = None):
    if credentialName == None:
      errorMessage = "the credential name shouldn't be [{}]".format(credentialName)
      logError(errorMessage)
      raise ValueError(errorMessage)
    else:
      accessKey, secretKey = getCredentials(credentialName)
    
    if regionCode == None:
      self.sqsClient = boto3.client('sqs',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name="us-west-2",
                        )
    else:
      self.sqsClient = boto3.client('sqs',
                        aws_access_key_id = accessKey,
                        aws_secret_access_key = secretKey,
                        aws_session_token= "",
                        region_name=regionCode,
                        )
    
    return self.sqsClient

  def receiveMessage(self, queue_url, waitTimeSeconds = 20):
    # Receive message from SQS queue
    sqs_response = self.sqsClient.receive_message(
      QueueUrl=queue_url,
      AttributeNames=[
          'SentTimestamp'
      ],
      MaxNumberOfMessages=1,
      MessageAttributeNames=[
          'All'
      ],
      VisibilityTimeout=0,
      WaitTimeSeconds=waitTimeSeconds
    )
    
    if "Messages" in sqs_response.keys():
      # Delete received message from queue
      self.sqsClient.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=sqs_response['Messages'][0]['ReceiptHandle']
      )
      
      messageId = sqs_response["Messages"][0]["MessageId"]
      if messageId in self.msgId_list:
        logWarn("duplicated messageId:[{}]".format(messageId))
        
        message = None
        
      else:
        self.msgId_list.append(messageId)
        try:
          message = sqs_response['Messages'][0]
          
        except:
          message = None
          logException("unable to get a message from {}".format(queue_url))
      
      logInfo("sqs_response:[{}]".format(sqs_response))
    else:
      message = None
    
    logDebug("message:[{}]".format(message))
          
    return message
  
  def receiveMessageBodyWithAttributes(self, queue_url, waitTimeSeconds = 20):
    message_dict = self.receiveMessage(queue_url, waitTimeSeconds)
    if message_dict != None:
      msg_dict = {"msgId":message_dict["MessageId"], "attributes":message_dict["MessageAttributes"], "message":message_dict["Body"]}
    else:
      msg_dict = None
      
    return msg_dict

def unitTest_sqsReceiveMessage():
  sqsManager = awsSQS(credentialName = "MODUAWS-SQS", regionCode = "us-east-1")
  
  message_list = []
  pollingCount = 0
  while True:
    message_dict = sqsManager.receiveMessageBodyWithAttributes("https://sqs.us-east-1.amazonaws.com/900629971091/moduaws-input-queue")
    message_list.append(message_dict)
    
    logInfo("[{}]->message:[{}]".format(pollingCount, message_dict))
    pollingCount += 1
    
    if pollingCount > 5:
      break
  
  pollingCount = 0
  for message in message_list:
    logInfo("[{}]->message:[{}]".format(pollingCount, message))
    pollingCount += 1
    

def localUnitTest():
  currentLogLevel = getLogLevel()
  setLogLevel('UNITTEST')
  unitTestFunction_dict = [
                           {"target":unitTest_sqsReceiveMessage, "args":()},
                           ]
  
  unitTest(unitTestFunction_dict)
  
  setLogLevel(currentLogLevel)

if __name__ == "__main__":
  
  
  localUnitTest()
  
  
