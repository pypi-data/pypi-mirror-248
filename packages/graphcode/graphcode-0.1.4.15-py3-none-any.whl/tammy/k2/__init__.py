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
from graphcode.conf import getMaxApiRetries, getWaitTimeForRateExceeded, getMaxPaginatingCount

from graphcode.parse import GcParse, nextTokenKeyword_list

from graphcode.conditions import GcConditions
from graphcode.lib import getDateString

from pathway import updateMsg

from tammy.midway import Midway
from tammy.k2.payload import K2Payload

import json
import time
import random
from uuid import uuid4

import requests

import logging

#Disable warnings from urlib3, telling us SSL cert is not in chain/CA
requests.packages.urllib3.disable_warnings()

class K2(Midway):
  def __init__(self, request_dict, logMessage_list, errorReason_list):
    Midway.__init__(self, request_dict, logMessage_list, errorReason_list)
    
    self.maxK2ApiRetry = getMaxApiRetries()
    self.maxWaitTimeForRateExceeded = getWaitTimeForRateExceeded()
    self.maxPaginatingCount = getMaxPaginatingCount()

    self.accessOverrideSession_list = []
    self.accessOverrideSession_dict = {"accessOverrideSession":None, "expirationTime":-1}
  
    self.deadRequest_list = []
    
  def get(self, input_dict, retry = 0):
    #for key in input_dict.keys():
    #  logDebug("{}:[{}]".format(key, input_dict[key]))
    #input_dict["platform"] = "k2"
    
    if "maxPaginatingCount" in input_dict.keys():
      if isinstance(input_dict["maxPaginatingCount"], int):
        self.maxPaginatingCount = input_dict["maxPaginatingCount"]
        
      elif isinstance(input_dict["maxPaginatingCount"], str):
        try:
          self.maxPaginatingCount = int(input_dict["maxPaginatingCount"])
        except:
          logException("unexpected type:{}:maxPaginatingCount:[{}]".format(type(input_dict["maxPaginatingCount"]), input_dict["maxPaginatingCount"]))
          self.maxPaginatingCount = -1
      else:
        logWarn("unexpected type:{}:maxPaginatingCount:[{}]".format(type(input_dict["maxPaginatingCount"]), input_dict["maxPaginatingCount"]))
    elif "inputs" in input_dict.keys() and isinstance(input_dict["inputs"], dict) and "maxPaginatingCount" in input_dict["inputs"].keys():
      if isinstance(input_dict["inputs"]["maxPaginatingCount"], int):
        self.maxPaginatingCount = input_dict["inputs"]["maxPaginatingCount"]
        
      elif isinstance(input_dict["inputs"]["maxPaginatingCount"], str):
        try:
          self.maxPaginatingCount = int(input_dict["inputs"]["maxPaginatingCount"])
        except:
          logException("unexpected type:{}:maxPaginatingCount:[{}]".format(type(input_dict["inputs"]["maxPaginatingCount"]), input_dict["inputs"]["maxPaginatingCount"]))
          self.maxPaginatingCount = -1
      else:
        logWarn("unexpected type:{}:maxPaginatingCount:[{}]".format(type(input_dict["inputs"]["maxPaginatingCount"]), input_dict["inputs"]["maxPaginatingCount"]))
    
    thisReulst_list = self.getWithNextToken(input_dict, retry)
    #try:
    #  logDebug("thisReulst_list:[len:{:,}]".format(len(thisReulst_list)))
    #except:
    #  logWarn("unexpected format type:{}:thisReulst_list".format(type(thisReulst_list)))
    
    if len(self.deadRequest_list) > 0:
      logError("total {:,} requests were failed".format(len(self.deadRequest_list)))
    #deadRequestCount = 0
    #for thisDeadRequest_dict in self.deadRequest_list:
    #  deadRequestCount += 1
    #  logWarn("(#{:,}\tdead thisDeadRequest_dict:[{}]".format(deadRequestCount, thisDeadRequest_dict))
    
    return thisReulst_list
  
  def getWithNextToken(self, input_dict, retry = 0):
    #for key in input_dict.keys():
    #  logDebug("{}:[{}]".format(key, input_dict[key]))
      
    if "parsed" in input_dict.keys() and isinstance(input_dict["parsed"], bool):
      parsed = input_dict["parsed"]
    else:
      parsed = True
    
    if "requestId" in input_dict.keys():
      requestId = input_dict["requestId"]
    else:
      requestId = None
    #logDebug("===============>requestId:[{}]".format(requestId))
    
    if "startTime" in input_dict.keys():
      providedStartTime = input_dict["startTime"]
    else:
      providedStartTime = "23 hours ago"
      
    if "endTime" in input_dict.keys():
      providedEndTime = input_dict["endTime"]
    else:
      providedEndTime = "now"
    
    cwPaginating_list = []
    apiName_list = input_dict["apiName"].split(".")
    if len(apiName_list) == 2 and "getMetricStatistics" in apiName_list[1]:
      if "endpointParameters" in input_dict.keys():
        #logDebug("#endpointParameters:[{}]".format(input_dict["endpointParameters"]))
        
        for endpointParameterItemMap in  input_dict["endpointParameters"].strip().split(";"):
          endpointParameterItemMap_list = endpointParameterItemMap.split("=")
          logDebug("endpointParameterItemMap_list:[{}]".format(endpointParameterItemMap_list))
          if len(endpointParameterItemMap_list) == 2:
            if endpointParameterItemMap_list[0] in input_dict.keys():
              logWarn("{}:[{}] is overwritten to with input_dict:[{}]".format(endpointParameterItemMap_list[0], endpointParameterItemMap_list[1], input_dict))
            
            input_dict[endpointParameterItemMap_list[0]] = endpointParameterItemMap_list[1]
            
      elif "inputs" in input_dict.keys():
        #logDebug("#inputs:[{}]".format(input_dict["inputs"]))
        
        for inputKey in input_dict["inputs"].keys():
          #if inputKey in input_dict.keys():
          #  logWarn("inputKeyname:[{}] is duplicated".format(inputKey))
            
          input_dict[inputKey] = input_dict["inputs"][inputKey]
        del input_dict["inputs"]
        
      if "period" in input_dict.keys():
        try:
          period = int(input_dict["period"])
        except:
          logException("unable to set 'period' with period:[{}]".format(input_dict["period"]))
          period = 300
      else:
        period = 300
        logError("'period' is not found at input_dict.keys():[{}]".format(input_dict.keys()))
      input_dict["period"] = period
      
      try:
        startTime = getDateString(input_dict["startTime"], "cloudwatch")
      except:
        logException("unable to set startTime")
        startTime = getDateString("23.9 hours ago", "cloudwatch")
      
      try:
        endTime = getDateString(input_dict["endTime"], "cloudwatch")
      except:
        logException("unable to set startTime")
        endTime = getDateString("now", "cloudwatch")
      
      while endTime > startTime + period * 1440 * 1000:
        cwPaginating_list.append([startTime, startTime + period * 1440 * 1000])
        startTime = startTime + period * 1440 * 1000
      
      if endTime > startTime:
        cwPaginating_list.append([startTime, endTime])
        
    #logDebug("#cwPaginating_list(len:{}):{}".format(len(cwPaginating_list), cwPaginating_list))
    
    paginating = True
    paginatingToken_list = []
    #nextTokenKeyword_list = ["nextToken", "NextToken", "marker", "Marker", "paginationToken", "PaginationToken", "lastEvaluatedTableName", "LastEvaluatedTableName"]
    paginatingK2Result_list = []
    cwPaginatingCount = 0
    while paginating:
      paginating = False  
      #logDebug("paginating:[{}]".format(paginating))
      if len(cwPaginating_list) > 0:
        input_dict["startTime"] = cwPaginating_list[0][0]
        input_dict["endTime"] = cwPaginating_list[0][1]
        del cwPaginating_list[0]
        #logDebug("#cwPaginating_list[{}]:[{}->{}]->{:.2f}Hours".format(cwPaginatingCount, getDateString(input_dict["startTime"]/1000), getDateString(input_dict["endTime"]/1000), (input_dict["endTime"]- input_dict["startTime"])/ 1000 / 3600))
        
        if len(cwPaginating_list) > 0:
          paginating = True
        
        cwPaginatingCount += 1
        
      try:
        #logDebug("{}:type:{}:paginatingK2Result_list(len:{:,}):[{}]".format(paginating, type(paginatingK2Result_list), len(paginatingK2Result_list), paginatingK2Result_list))
        input_dict["paginatingNumber"] = len(paginatingK2Result_list)
        k2Result_dict, payload_dict = self.run(input_dict, retry)
          
        try:
          #logDebug("#{}:type:{}:paginatingK2Result_list(len:{:,}):[{}]".format(paginating, type(paginatingK2Result_list), len(paginatingK2Result_list), paginatingK2Result_list))
          #logDebug("#k2Result_dict:[{}]".format(k2Result_dict))
          # finding a paginating token
          for nextTokenKeyword in nextTokenKeyword_list:
            if isinstance(k2Result_dict, dict):
              if nextTokenKeyword in k2Result_dict.keys() and isinstance(k2Result_dict[nextTokenKeyword], str) and k2Result_dict[nextTokenKeyword].strip() != "":
                if k2Result_dict[nextTokenKeyword] in paginatingToken_list:
                  paginating = False  
                  #del k2Result_dict[nextTokenKeyword]
                  break
                
                else:
                  paginating = True
                  paginatingToken_list.append(k2Result_dict[nextTokenKeyword])
                  
                  if nextTokenKeyword in ["lastEvaluatedTableName"]:
                    input_dict["paginatingToken"] = {"key":"exclusiveStartTableName", "value": k2Result_dict[nextTokenKeyword]}
                    
                  elif nextTokenKeyword in ["LastEvaluatedTableName"]:
                    input_dict["paginatingToken"] = {"key":"ExclusiveStartTableName", "value": k2Result_dict[nextTokenKeyword]}
                  
                  elif nextTokenKeyword in ["lastEvaluatedStreamArn"]:
                    input_dict["paginatingToken"] = {"key":"exclusiveStartStreamArn", "value": k2Result_dict[nextTokenKeyword]}
                  
                  elif nextTokenKeyword in ["LastEvaluatedStreamArn"]:
                    input_dict["paginatingToken"] = {"key":"ExclusiveStartStreamArn", "value": k2Result_dict[nextTokenKeyword]}
                  
                  else:
                    input_dict["paginatingToken"] = {"key":nextTokenKeyword, "value": k2Result_dict[nextTokenKeyword]}
                  
                  del k2Result_dict[nextTokenKeyword]
                  break
                
              else:
                for key in k2Result_dict.keys():
                  if isinstance(k2Result_dict[key], dict) and nextTokenKeyword in k2Result_dict[key].keys() and isinstance(k2Result_dict[key][nextTokenKeyword], str) and k2Result_dict[key][nextTokenKeyword].strip() != "":
                    if k2Result_dict[key][nextTokenKeyword] in paginatingToken_list:
                      del k2Result_dict[key][nextTokenKeyword]
                      break
                    else:
                      paginating = True
                      paginatingToken_list.append(k2Result_dict[key][nextTokenKeyword])
                      input_dict["paginatingToken"] = {"key":nextTokenKeyword, "value": k2Result_dict[key][nextTokenKeyword]}
                      del k2Result_dict[key][nextTokenKeyword]
                      break
          
          #logDebug("#{}:type:{}:paginatingK2Result_list(len:{:,}):[{}]".format(paginating, type(paginatingK2Result_list), len(paginatingK2Result_list), paginatingK2Result_list))
          if parsed and isinstance(k2Result_dict, dict):
            if "platform" in input_dict.keys() and input_dict["platform"] in ["dante"]:
              try:
                #logDebug("deleting sdkResponseMetadata:[{}]".format(k2Result_dict["sdkResponseMetadata"]))
                del k2Result_dict["sdkResponseMetadata"]
              except:
                pass
              
              try:
                #logDebug("deleting sdkHttpMetadata:[{}]".format(k2Result_dict["sdkHttpMetadata"]))
                del k2Result_dict["sdkHttpMetadata"]
              except:
                pass
              
              try:
                #logDebug("deleting sdkHttpMetadata:[{}]".format(k2Result_dict["sdkHttpMetadata"]))
                del k2Result_dict["danteCallStatus"]
              except:
                pass
              
              try:
                #logDebug("deleting sdkHttpMetadata:[{}]".format(k2Result_dict["sdkHttpMetadata"]))
                del k2Result_dict["_K2"]
              except:
                pass
            
            else:
                
              try:
                #logDebug("deleting sdkResponseMetadata:[{}]".format(k2Result_dict["sdkResponseMetadata"]))
                del k2Result_dict["sdkResponseMetadata"]
              except:
                pass
              
              try:
                #logDebug("deleting sdkHttpMetadata:[{}]".format(k2Result_dict["sdkHttpMetadata"]))
                del k2Result_dict["sdkHttpMetadata"]
              except:
                pass
            
            if "result" in k2Result_dict.keys() and isinstance(k2Result_dict["result"], list) and len(k2Result_dict["result"]) == 1 and isinstance(k2Result_dict["result"][-1], dict) and "error" in k2Result_dict["result"][-1].keys() and "statusCode" in k2Result_dict["result"][-1].keys():
              pass
            else:
              gcParse = GcParse(result=k2Result_dict, inputs=input_dict, payload=payload_dict)
              
              if "getMetricStatistics" not in input_dict["apiName"]:
                try:
                  argValues = ""
                  for argKey in payload_dict["args"].keys():
                    if argKey in nextTokenKeyword_list:
                      argValues += "_x{}".format(int(time.time()))
                    else:
                      argValues += "_{}".format(payload_dict["args"][argKey])
                    
                    #logDebug("(#{:,})\t{}:[{}]".format(len(paginatingToken_list), argKey, payload_dict["args"][argKey]))
                    
                  if "accountId" in payload_dict.keys() and "region" in payload_dict.keys():
                    s3KeyName = "{}/{}_{}{}.json".format(payload_dict["apiName"], payload_dict["accountId"], payload_dict["region"], argValues.replace("/",":"))
                  if "accountId" in payload_dict.keys():
                    s3KeyName = "{}/{}_{}.json".format(payload_dict["apiName"], payload_dict["accountId"], argValues.replace("/",":"))
                  elif "region" in payload_dict.keys():
                    s3KeyName = "{}/_{}{}.json".format(payload_dict["apiName"], payload_dict["region"], argValues.replace("/",":"))
                  else:
                    s3KeyName = "{}/_{}.json".format(payload_dict["apiName"], argValues.replace("/",":"))
                    
                  thisLogLevel = logging.getLogger().level
                  logging.getLogger().setLevel(logging.INFO)
                  #self.k2S3Manager.putObject(bucketName=self.k2S3bucketName, key="k2/{}".format(s3KeyName), data=json.dumps(k2Result_dict))
                  logging.getLogger().setLevel(thisLogLevel)
                except:
                  logException("unable to get k2S3KeyName with payload_dict:[{}]".format(payload_dict))
                
              k2Result_dict = gcParse.get()
              #logDebug("#{}:type:{}:k2Result_dict(len:{:,}):[{}]".format(paginating, type(k2Result_dict), len(k2Result_dict), k2Result_dict))
              #logDebug("#{}:type:{}:paginatingK2Result_list(len:{:,}):[{}]".format(paginating, type(paginatingK2Result_list), len(paginatingK2Result_list), paginatingK2Result_list))
          
          elif isinstance(k2Result_dict, list):
            try:
              apiName_list = payload_dict["apiName"].split(".")
              serviceName = apiName_list[0]
              apiName = apiName_list[1]
            except:
              serviceName =  None
              try:
                apiName = payload_dict["apiName"]
              except:
                apiName = None
              
            try:
              accountId = payload_dict["accountId"]
            except:
              accountId = None
              
            try:
              regionCode = payload_dict["region"]
            except:
              regionCode = None
              
              
            thisK2Result_list = []
            for k2ResultItem_dict in k2Result_dict:
              #logDebug("#k2ResultItem_dict:[{}]".format(k2ResultItem_dict))
              thisK2Result_list.append(
                {
                  "serviceName": serviceName,
                  "accountId_": accountId,
                  "regionCode_": regionCode,
                  **k2ResultItem_dict
                  }
                )
            
            k2Result_dict = thisK2Result_list
            
          paginatingK2Result_list.append(k2Result_dict)
          
          #if len(paginatingK2Result_list) > 0:
          #  if isinstance(paginatingK2Result_list[-1], list) and len(paginatingK2Result_list[-1]) > 0:
          #    logDebug("(#{:,})\tpaginating:[{}]:type:{}:paginatingK2Result_list[len:{:,}][-1]:[{}]".format(len(paginatingK2Result_list), paginating, type(paginatingK2Result_list), len(paginatingK2Result_list[-1]), paginatingK2Result_list[-1][-1]))
          #  else:
          #    logDebug("(#{:,})\tpaginating:[{}]:type:{}:paginatingK2Result_list[-1]:[{}]".format(len(paginatingK2Result_list), paginating, type(paginatingK2Result_list), paginatingK2Result_list[-1]))
          #else:
          #  logDebug("(#{:,})\tpaginating:[{}]:type:{}:paginatingK2Result_list:[{}]".format(len(paginatingK2Result_list), paginating, type(paginatingK2Result_list), paginatingK2Result_list))
          
          if self.maxPaginatingCount > 0 and len(paginatingK2Result_list) > self.maxPaginatingCount:
            logError("paginating is over {:,} times. If it's designed, please cut a ticket: CTI:AWS/Enterprise Support/moduAWS".format(len(paginatingK2Result_list)))
            paginating = False
          #else:
          #  logDebug("(#{}/{}) continue to paginate)".format(len(paginatingK2Result_list), self.maxPaginatingCount))
           
        except Exception as e:
          paginatingK2Result_list = [
            {
              "result":k2Result_dict, 
              "error":logError("{}->inputs:[{}]".format(e, input_dict))
              }
            ]
          logExceptionWithValueError("unexpected result->Error:[{}]".format(e))
        
        #logDebug("#payload_dict:[{}]->k2Result_dict:[{}]".format(payload_dict, k2Result_dict))
        
      except Exception as e:
        paginatingK2Result_list = [
          {
            "error":logError("{}->inputs:[{}]".format(e, input_dict))
            }
          ]
        logExceptionWithValueError("unexpected result->Error:[{}]".format(e))
    
    if len(paginatingK2Result_list) > 0 and isinstance(paginatingK2Result_list[0], list):
      thisPaginatingK2Reulst = []
      for paginatingK2ResultItems_list in paginatingK2Result_list:
        for paginatingK2ResultItems in paginatingK2ResultItems_list:
          thisPaginatingK2Reulst.append(paginatingK2ResultItems)
      paginatingK2Result_list = thisPaginatingK2Reulst
    #logDebug("#payload_dict:[{}]->type:{}:paginatingK2Result_list".format(payload_dict, type(paginatingK2Result_list)))
    
    if "getMetricStatistics" in input_dict["apiName"] and isinstance(payload_dict, dict) and "args" in payload_dict.keys():
      gcParse = GcParse(result=k2Result_dict, inputs=input_dict, payload=payload_dict)
      paginatingK2Result_list = gcParse.getCwGetMetricStatistics(paginatingK2Result_list)
      
      try:
        
        argValues = ""
        for argKey in payload_dict["args"].keys():
          if argKey in nextTokenKeyword_list:
            argValues += "_x{}".format(int(time.time()))
          else:
            argValues += "_{}".format(payload_dict["args"][argKey])
          
          #logDebug("#{}:[{}]".format(argKey, payload_dict["args"][argKey]))
          
        s3KeyName = "{}/{}_{}{}.json".format(payload_dict["apiName"], payload_dict["accountId"], payload_dict["region"], argValues.replace("/",":"))
        
        thisLogLevel = logging.getLogger().level
        logging.getLogger().setLevel(logging.INFO)
        #self.k2S3Manager.putObject(bucketName=self.k2S3bucketName, key="k2/{}".format(s3KeyName), data=json.dumps(k2Result_dict))
        logging.getLogger().setLevel(thisLogLevel)
      except:
        logException("unable to get k2S3KeyName with payload_dict:[{}]".format(payload_dict))
        
      # filter results with conditions
      '''
      try:
        if "conditions" in input_dict.keys() and input_dict["conditions"].strip() != "":
          gcConditions = GcConditions(input_dict["conditions"], paginatingK2Result_list)
          paginatingK2Result_list = gcConditions.get()
          if len(paginatingK2Result_list) > 0:
            logInfo("conditions:[{}]->results(len:{}):[{}]".format(input_dict["conditions"], len(paginatingK2Result_list), paginatingK2Result_list[-1]))
          else:
            logInfo("conditions:[{}]->results(len:{}):[{}]".format(input_dict["conditions"], len(paginatingK2Result_list), paginatingK2Result_list))
      except Exception as e:
        logException("unable to filter the result with conditions:[{}]")
      '''
    #logDebug("#payload_dict:[{}]->type:{}:paginatingK2Result_list".format(payload_dict, type(paginatingK2Result_list)))
    
    input_dict["startTime"] = providedStartTime
    input_dict["endTime"] = providedEndTime
    
    #logDebug("#type:{}:paginatingK2Result_list(len:{:,}):[{}]".format(type(paginatingK2Result_list), len(paginatingK2Result_list), paginatingK2Result_list))
    #logDebug("#payload_dict:[{}]->type:{}:paginatingK2Result_list".format(payload_dict, type(paginatingK2Result_list)))
    
    return paginatingK2Result_list
    
  def run(self, input_dict, retry = 0):
    #for key in input_dict.keys():
    #  logDebug("{}:[{}]".format(key, input_dict[key]))
      
    if self.user == None:
      self.activeMidwayCookie_dict = self.getMidwayCookie()
    input_dict["user"] = self.user
    
    try:
      if "platform" in input_dict.keys() and input_dict["platform"] in ["dante"]:
        self.headers["Content-Type"] = "application/json; charset=utf-8"
        
        url = "http://localhost:5001/k2relay"
        
      elif input_dict["regionCode"].startswith("cn-"):
        if "cn" not in self.activeMidwayCookie_dict.keys() or "active" not in self.activeMidwayCookie_dict["cn"].keys() or self.activeMidwayCookie_dict["cn"]["active"] != True:
          return [
              {
                "error": "invalid cn midway"
                }
            ], input_dict
        else:
          url = "https://k2.bjs.aws-border.com/workbench/aws/resources/"
        
      else:
        if "global" not in self.activeMidwayCookie_dict.keys() or "active" not in self.activeMidwayCookie_dict["global"].keys() or self.activeMidwayCookie_dict["global"]["active"] != True:
          return [
              {
                "error": "invalid global midway"
                }
            ], input_dict
        else:
          url = "https://k2.amazon.com/workbench/aws/resources/"
    except:
      logException("unexpected input_dict:[{}]".format(input_dict))
      url = "https://k2.amazon.com/workbench/aws/resources/"
    
    try:
      if self.accessOverrideSession_dict["accessOverrideSession"] != None and self.accessOverrideSession_dict["expirationTime"] - 60> time.time():
        input_dict["accessOverrideSession"] = self.accessOverrideSession_dict["accessOverrideSession"]
      #logDebug("#accessOverrideSession_list:[{}]".format(self.accessOverrideSession_list))
      
      #logDebug("#======>input_dict:[{}]".format(input_dict))
      k2payload = K2Payload(input_dict)
      
      if "getMetricStatistics" in input_dict["apiName"]:
        payload_dict = k2payload.getCwPayload()
      else:
        payload_dict = k2payload.get()
      
      if isinstance(payload_dict, dict) and "apiName" in payload_dict.keys():
        if "platform" in input_dict.keys() and input_dict["platform"] in ["dante"]:
          try:
            del payload_dict["sessionMetadata"]
          except:
            logException("unexpected payload_dict:[{}]".format(payload_dict))
          
        try:
          payload = json.dumps(payload_dict)
        except:
          logExceptionWithValueError(logException("unable to load payload_dict:[{}]".format(payload_dict)))
          payload = payload_dict
      else:
        payload = payload_dict
      #logDebug("#======>payload:[{}]".format(payload))
      
      if isinstance(payload, str):
        try:
          k2Result = self.request(url = url, payload= payload)
          retry2 = 0
          while k2Result == None:
            logWarn("#{}:k2Result:[{}] with url:[{}],payload:[{}]".format(retry2, k2Result, url, payload))
            k2Result = self.request(url = url, payload= payload)
            
            retry2 += 1
            if retry2 > self.maxK2ApiRetry:
              break
            
          k2Result_dict = self.k2ErrorHandler(k2Result, url, payload, retry)
          
        except Exception as e:
          try:
            if "NewConnectionError" in "{e}".format(e):
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "input_dict":input_dict, 
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(k2Result.content, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            elif k2Result != None:
              logException("unable to load json result with [{}]".format(k2Result.content))
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "input_dict":input_dict, 
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(k2Result.content, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            else:
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":None, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "input_dict":input_dict, 
                    "payload":payload, 
                    "error":logError("k2Result:{}->Error:[{}]".format(k2Result, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
          except Exception as e:
            errMsg = logException("unable to print the detils of the error")
            k2Result_dict = {
                "result":[
                  {
                    "statusCode":None, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "input_dict":input_dict, 
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(errMsg, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
      else:
        errMsg = logError("unable to get payload with input_dict:[{}]".format(input_dict))
        k2Result_dict = {
                "result":[
                  {
                    "statusCode":None, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "input_dict":input_dict, 
                    "payload":payload, 
                    "error":logError( errMsg),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
    except Exception as e:
      
      if "getMetricStatistics" in input_dict["apiName"]:
        payload_dict = k2payload.getCwPayload()
      else:
        payload_dict = k2payload.get()
      
      try:
        errMsg = logException("unable to get k2 request->Error:[{}]".format(e))
        k2Result_dict = {
                  "result":[
                    {
                      "statusCode":None, 
                      "requestCount":self.requestCount, 
                      "retryCount":retry, 
                      "input_dict":input_dict, 
                      "payload":None, 
                      "error":logError(errMsg),
                      #"midway":self.midwayCookieCache_dict,
                      "midwayRegion":self.midwayRegion
                      }
                    ]
                  }
      except:
        logException("unexpected error")
      
      #logInfo("#k2Result_dict:[{}]".format(k2Result_dict))
      
    #logInfo("#k2Result_dict:[{}]".format(k2Result_dict))
    
    return k2Result_dict, payload_dict
  
  def k2ErrorHandler(self, k2Result, url, payload, retry = 0):
    
    try:
      decodedK2Result_text = k2Result.content.decode()
      '''
      if k2Result.status_code == 200:
        try:
          k2Result_dict = json.loads(decodedK2Result_text)
        except Exception as e:
          logException("unable to get the result of payload:[{}]->Error:[{}]".format(payload, e))
          k2Result_dict = {"result":[{"payload":payload, "error":"#201:#{}:{}:{}:{}".format(retry, k2Result.status_code, e, k2Result.content)}]}
      
      el
      '''
      if k2Result.status_code == 401:
        if self.requestCount == 0:
          return {
            "result":[
              {
                "statusCode":k2Result.status_code, 
                "requestCount":self.requestCount, 
                "retryCount":retry, 
                "payload":payload, 
                "error":logError(decodedK2Result_text),
                #"midway":self.midwayCookieCache_dict,
                "midwayRegion":self.midwayRegion
                }
              ]
            }
        
        retry2 = 0
        while True:
          try:
            self.SESSION.close()
            #self.SESSION = requests.Session()
            ##self.SESSION_COOKIES = {}
            k2Result_401 = self.request(url = url, payload= payload)
            if k2Result_401.status_code!= 401:
              break
          except Exception as e:
            errMsg = logError("unable to get the response of k2Result_401->error:[{}]".format(e))
            try:
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "payload":payload, 
                    "error":logError(errMsg),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            except Exception as e:
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(errMsg, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            
          if retry2 < 10:
            retry2 += 1
          #time.sleep(retry2*random.random())
        k2Result_dict = self.k2ErrorHandler(k2Result_401, url, payload, retry2)
        
      elif retry == 0 and k2Result.status_code == 403:
        try:
          reason = json.loads(decodedK2Result_text)["reason"]
        except Exception as e:
          logError("type:{}:{}:reason:[{}]-->Error".format(k2Result.status_code, type(decodedK2Result_text).__name__, decodedK2Result_text))
          reason = None
        
        if "User is not authorized" in decodedK2Result_text:
          try:
            k2Result_dict = {
                "result":[
                  {
                    **json.loads(payload), 
                    **{
                      "statusCode":k2Result.status_code, 
                      "requestCount":self.requestCount, 
                      "retryCount":retry, 
                      "error":logError(decodedK2Result_text),
                      #"midway":self.midwayCookieCache_dict,
                      "midwayRegion":self.midwayRegion
                      }
                    }
                  ]
                }
          except:
            k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":retry, 
                    "payload":payload, 
                    "error":logError(decodedK2Result_text),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            
        elif reason  == "InvalidBusinessUseCase":
          # add BCA
          logDebug("{}({}):[{}]".format(k2Result.status_code, retry, decodedK2Result_text))
          payload = self.bcaRequest(url, payload)
          
          # get k2 result with bca
          retry2 = 0
          k2ResultWithBCA = k2Result
          while k2ResultWithBCA.status_code == 403:
            k2ResultWithBCA = self.request(url = url, payload= payload)
            retry2 += 1
            time.sleep (0.5)
            
            if retry2 > 2:
              logWarn("#{}:BcaReques seems to be wrong or delayed".format(retry2))
            
              if retry2 > 20:
                logError("#{}:BcaReques seems to be timeout".format(retry2))
                break
            
          if k2ResultWithBCA.status_code == 403:
            try:
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2ResultWithBCA.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}_{}".format(retry, retry2),
                    "payload":payload, 
                    "error":logError("BcaReques seems to be timeout after {} retries in {:.2f} seconds".format(retry2, retry2 * 0.5)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
              
            except Exception as e:
              logException("unable to get the result of payload:[{}]->Error:[{}]".format(payload, e))
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2ResultWithBCA.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}_{}".format(retry, retry2),
                    "payload":payload, 
                    "error":logError("after {} retries in 2.5 seconds, {}->Error:[{}]".format(retry2, k2ResultWithBCA.content, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
          else:
            decodedK2Result_text = k2ResultWithBCA.content.decode()
            if decodedK2Result_text.startswith("[WORKBENCH]"):
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2ResultWithBCA.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}_{}".format(retry, retry2),
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(retry2, decodedK2Result_text)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
            else:
              try:
                k2Result_dict = json.loads(decodedK2Result_text)
              except Exception as e:
                logException("unable to load json result with [{}]".format(k2ResultWithBCA.content))
                k2Result_dict = {
                  "result":[
                    {
                      "statusCode":k2ResultWithBCA.status_code, 
                      "requestCount":self.requestCount, 
                      "retryCount":"{}_{}".format(retry, retry2),
                      "payload":payload, 
                      "error":logError("{}->Error:[{}]".format(retry2, k2ResultWithBCA.content, e)),
                      #"midway":self.midwayCookieCache_dict,
                      "midwayRegion":self.midwayRegion
                      }
                    ]
                  }
              
        else:
          # get k2 result with bca
          k2Result403Retry = self.request(url = url, payload= payload)
          if k2Result403Retry.status_code == 403:
            try:
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result403Retry.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}".format(retry),
                    "payload":payload, 
                    "error":logError(k2Result403Retry.content.decode()),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
              
            except Exception as e:
              logException("unable to get the result of payload:[{}]->Error:[{}]".format(payload, e))
              k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result403Retry.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}".format(retry),
                    "payload":payload, 
                    "error":logError("{}-Error:[{}]".format(k2Result403Retry.content, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
              
          else:
            try:
              k2Result_dict = json.loads(k2Result403Retry.content.decode())
            except Exception as e:
              logException("unable to load json result with [{}]".format(k2Result403Retry.content))
              k2Result_dict =  {
                "result":[
                  {
                    "statusCode":k2Result403Retry.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}".format(retry),
                    "payload":payload, 
                    "error":logError("{}-Error:[{}]".format(k2Result403Retry.content, e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
      
      elif k2Result.status_code == 404:
        if ("TooManyRequestsException" in decodedK2Result_text \
                 or "RequestLimitExceeded" in decodedK2Result_text \
                 or "ThrottlingException" in decodedK2Result_text):
        
          retry2 = 0
          while True:
            self.SESSION.close()
            self.SESSION = requests.Session()
            ##self.SESSION_COOKIES = {}
            
            sleepTime = retry2 + (retry2+1) * random.random()
            if sleepTime > 60:
              sleepTime = self.maxWaitTimeForRateExceeded + self.maxWaitTimeForRateExceeded * random.random()
            logWarn("#{}_{}\tsleeping in {:.2f}s, due to too many requests with payload:[{}]->Error:[{}]".format(retry, retry2, sleepTime, payload, decodedK2Result_text))
            time.sleep(sleepTime)
            
            ###self.SESSION_COOKIES = {}
            #self.SESSION = requests.Session()
            #self.activeMidwayCookie_dict = self.getMidwayCookie()
            
            #logDebug("[k2:404]updatePayloadWith404TooManyRequest(before):{}".format(payload))
            #payload = self.updatePayloadWith404TooManyRequest(payload)
            #logDebug("[k2:404]updatePayloadWith404TooManyRequest(after):{}".format(payload))
            
            k2Result404TooManyRequestRetry = self.request(url = url, payload= payload)
            decodedK2Result_text = k2Result.content.decode()
            
            if "TooManyRequestsException" not in decodedK2Result_text \
                and "RequestLimitExceeded"  not in decodedK2Result_text \
                and "ThrottlingException" not in decodedK2Result_text:
              break
            
            retry2 += 1
            
            if retry2 > self.maxK2ApiRetry:
              self.deadRequest_list.append({"url":url, "payload":payload})
              
              logError("#{:,}->{}_{}\tfailed to get k2 Result with payload:[{}]->Error:[{}]".format(len(self.deadRequest_list), retry, retry2, payload, decodedK2Result_text))
              break
            
          k2Result_dict = self.k2ErrorHandler(k2Result404TooManyRequestRetry, url, payload, retry + 1)
          
        else:      
          k2Result_dict = {
                  "result":[
                    {
                      "statusCode":k2Result.status_code, 
                      "requestCount":self.requestCount, 
                      "retryCount":"{}".format(retry),
                      "payload":payload, 
                      "error":logError(decodedK2Result_text),
                      #"midway":self.midwayCookieCache_dict,
                      "midwayRegion":self.midwayRegion
                      }
                    ]
                  }
        
      elif decodedK2Result_text.startswith("[WORKBENCH]"):
        k2Result_dict = {
          "result":[
            {
              "statusCode":k2Result.status_code, 
              "requestCount":self.requestCount, 
              "retryCount":"{}".format(retry),
              "payload":payload, 
              "error":logError(decodedK2Result_text),
              #"midway":self.midwayCookieCache_dict,
              "midwayRegion":self.midwayRegion
              }
            ]
          }
        
      elif k2Result.status_code == 504 \
            and ("Connection reset by peer" in decodedK2Result_text):
        
        retry2 = 0
        k2Result504ConnectionResetRetry = ""
        while True:
          self.SESSION.close()
          #self.SESSION = requests.Session()
          ##self.SESSION_COOKIES = {}
          
          sleepTime = retry2 + (retry2+1) * random.random()
          if sleepTime > 60:
            sleepTime = self.maxWaitTimeForRateExceeded + self.maxWaitTimeForRateExceeded * random.random()
          logWarn("#{}_{}\tseeping in {:.2f}s, due 'Connection reset by peer' with payload:[{}]->Error:[{}]".format(retry, retry2, sleepTime, payload, decodedK2Result_text))
          time.sleep(sleepTime)
          
          ###self.SESSION_COOKIES = {}
          ##self.SESSION = requests.Session()
          #self.activeMidwayCookie_dict = self.getMidwayCookie()
          
          #logDebug("[k2:404]updatePayloadWith404TooManyRequest(before):{}".format(payload))
          #payload = self.updatePayloadWith404TooManyRequest(payload)
          #logDebug("[k2:404]updatePayloadWith404TooManyRequest(after):{}".format(payload))
          
          k2Result504ConnectionResetRetry = self.request(url = url, payload= payload)
          decodedK2Result_text = k2Result.content.decode()
          
          if "Connection reset by peer" not in decodedK2Result_text:
            break
          
          retry2 += 1
          
          if retry2 > self.maxK2ApiRetry:
            self.deadRequest_list.append({"url":url, "payload":payload})
            
            logError("#{:,}->{}_{}\tfailed to get k2 Result with payload:[{}]->Error:[{}]".format(len(self.deadRequest_list), retry, retry2, payload, decodedK2Result_text))
            break
          
        k2Result_dict = self.k2ErrorHandler(k2Result504ConnectionResetRetry, url, payload, retry + 1)
        
      else:
        try:
          k2Result_dict = json.loads(decodedK2Result_text)
        except:
          if "Read timed out" in decodedK2Result_text:
            
            retry2 = 0
            while True:
              #self.SESSION = requests.Session()
              ##self.SESSION_COOKIES = {}
              
              sleepTime = retry2 + (retry2+1) * random.random()
              if sleepTime > 60:
                sleepTime = self.maxWaitTimeForRateExceeded + self.maxWaitTimeForRateExceeded * random.random()
              logWarn("#{}_{}\tseeping in {:.2f}s, due 'Read timed out' with payload:[{}]->Error:[{}]".format(retry, retry2, sleepTime, payload, decodedK2Result_text))
              time.sleep(sleepTime)
              
              ###self.SESSION_COOKIES = {}
              ##self.SESSION = requests.Session()
              
              k2Result504ConnectionResetRetry = self.request(url = url, payload= payload, timeout=60+30*(retry2+1))
              decodedK2Result_text = k2Result504ConnectionResetRetry.content.decode()
              
              if "Read timed out" not in decodedK2Result_text:
                break
              
              retry2 += 1
              
              if retry2 > self.maxK2ApiRetry:
                self.deadRequest_list.append({"url":url, "payload":payload})
                
                logError("#{:,}->{}_{}\tfailed to get k2 Result with payload:[{}]->Error:[{}]".format(len(self.deadRequest_list), retry, retry2, payload, decodedK2Result_text))
                break
              
            k2Result_dict = self.k2ErrorHandler(k2Result504ConnectionResetRetry, url, payload, retry + 1)
          
          else:
            k2Result_dict = {
              "result":[
                {
                  "statusCode":k2Result.status_code, 
                  "requestCount":self.requestCount, 
                  "retryCount":"{}".format(retry),
                  "payload":payload, 
                  "error":logException("{}->Error:[{}]".format(decodedK2Result_text,"'json' format is expected")),
                  #"midway":self.midwayCookieCache_dict,
                  "midwayRegion":self.midwayRegion
                  }
                ]
              }
          
    except Exception as e:
      logException("unable to decode the content:[{}]->Error:[{}]".format(k2Result, payload, e))
      k2Result_dict = {
                "result":[
                  {
                    "statusCode":k2Result.status_code, 
                    "requestCount":self.requestCount, 
                    "retryCount":"{}".format(retry),
                    "payload":payload, 
                    "error":logError("{}->Error:[{}]".format(k2Result.content,e)),
                    #"midway":self.midwayCookieCache_dict,
                    "midwayRegion":self.midwayRegion
                    }
                  ]
                }
    
    if k2Result.status_code != 200 and "getMetricStatistics" in "{}".format(payload):
      if retry < 100:
        k2Result_dict = self.k2ErrorHandler(self.request(url = url, payload= payload), url, payload, retry + 100)
      
    return k2Result_dict
  
  def bcaRequest(self, url, payload):
    url = url[:url.find("/workbench")] + "/access_override"
    logDebug("url:[{}]".format(url))
    
    
    if self.accessOverrideSession_dict["expirationTime"] - 60 > time.time():
      logDebug("key:[expirationTime]->[{}](valid for {:.2f}s)".format(self.accessOverrideSession_dict["expirationTime"], self.accessOverrideSession_dict["expirationTime"] - time.time()))
    
      payload_dict = json.loads(payload)
      payload_dict["accessOverrideSession"] = self.accessOverrideSession_dict["accessOverrideSession"]   
      payload = json.dumps(payload_dict) 
    
    else:
      logDebug("key:[expirationTime]->[{}](valid for {:.2f}s)".format(self.accessOverrideSession_dict["expirationTime"], self.accessOverrideSession_dict["expirationTime"] - time.time()))
      
      accessOverridePayload = json.dumps({
                              "justificationType": "notListed",
                              "justificationMetadata": {
                                "justification": "{}".format(payload)
                                },
                              "ttlInSeconds":3600
                              })
      
          
      try:
        try:
          self.addHeaders('Content-Type', 'application/json')
          r = self.request(url = url, payload= accessOverridePayload)
        except Exception as e:
          errorMessage = "Error:[{}] -> url:[{}] -> payload:[{}]".format(e, url, payload)
          logError(errorMessage)
          
          return {}
        
        jsonResult = json.loads(r.content)
        if isinstance(jsonResult, dict):
          #for key in jsonResult.keys():
          #  logDebug("key:{} -> value:[{}]".format(key, jsonResult[key]))
        
          if "accessOverrideSession" in jsonResult.keys():
            #logDebug("key:[accessOverrideSession]->[{}]".format(jsonResult["accessOverrideSession"]))
            self.accessOverrideSession_dict["accessOverrideSession"] = jsonResult["accessOverrideSession"]
          
          if "expirationTime" in jsonResult.keys():
            #logDebug("key:[expirationTime]->[{}](valid for {:.2f}s)".format(jsonResult["expirationTime"], jsonResult["expirationTime"] - time.time()))
            self.accessOverrideSession_dict["expirationTime"] = jsonResult["expirationTime"]
          
        payload_dict = json.loads(payload)
        payload_dict["accessOverrideSession"] = jsonResult["accessOverrideSession"]
        payload = json.dumps(payload_dict) 
        
        if "accountId" in payload_dict.keys():
          self.accessOverrideSession_list.append(payload_dict["accountId"])
          logDebug("accountId:[{}] is set with accessOverrideSession:{}]".format(payload_dict["accountId"], payload_dict["accessOverrideSession"]))
        elif "accountIds" in payload_dict.keys():
          for accountId in payload_dict["accountIds"]:
            self.accessOverrideSession_list.append(accountId)
          logDebug("accountIds:[{}] is set with accessOverrideSession:{}]".format(payload_dict["accountIds"], payload_dict["accessOverrideSession"]))
        else:
          logWarn("unexpected payload:{}]".format(payload_dict))
        
      except Exception as e:
        errorMessage = "unable to get a bca override session->Error:[{}] -> url:[{}] -> payload:[{}]".format(e, url, payload)
        logError(errorMessage)
        
    return payload
  
  def updatePayloadWith404TooManyRequest(self, payload):
    try:
      payload_dict = json.loads(payload)
      if "sessionMetadata" in payload_dict.keys() and "instance_id" in payload_dict["sessionMetadata"].keys():
        payload_dict["sessionMetadata"]["instance_id"] = "{}-{}_{}".format(self.user, uuid4(), payload_dict["sessionMetadata"]["instance_id"].split("_")[-1])
      payload = json.dumps(payload_dict)
    except:
      logException("unable to load json with payload:[{}]".format(payload))
      
    return payload
