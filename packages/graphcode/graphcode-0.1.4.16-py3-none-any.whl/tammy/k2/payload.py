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

from uuid import uuid4

import json

import random
from graphcode.lib import getDateString

from datetime import datetime

class K2Payload():
  def __init__(self, inputs):
    self.input_dict = inputs
    
    if "paginatingNumber" in self.input_dict.keys():
      paginatingNumber = self.input_dict["paginatingNumber"]
    else:
      paginatingNumber = 0
      
    if "requestId" in self.input_dict.keys():
      self.requestId = "{}#{}".format(self.input_dict["requestId"], paginatingNumber)
    else:
      self.requestId = "{}#5000".format(uuid4()) 
      self.input_dict["requestId"] = self.requestId
      
    try:
      self.user = self.input_dict["user"]
    except:
      logWarn("'user' is missing at inputs:[{}]".format(self.input_dict))
      self.user = "unknown"
  
  
  def getApiName(self, apiName):
    if apiName in ["service-quotas"]:
      apiName = "servicequotas"
    
    return apiName
  
  def get(self):
    if "accountId" in self.input_dict.keys():
      accountId = "{}".format(self.input_dict["accountId"]).strip().zfill(12)
    else:
      accountId = ""
    
    if "regionCode" in self.input_dict.keys():
      regionCode = self.input_dict["regionCode"].strip()
    else:
      regionCode = "us-east-1"
    
    #serviceName = getValueFromRequest(keyword="serviceName", self.input_dict)
    apiName = self.getApiName(self.input_dict["apiName"]).strip()
    regionCode = self.getRandomRegionCode(apiName, regionCode)
    
    args = {}
    if 'trustedadvisor' in apiName:
      payload_dict = { "region": regionCode, "accountId": accountId, "args": args, "apiName": apiName}
      
    elif 'listMetrics' in apiName:
      payload_dict = { "apiName": "cloudwatch.listMetrics", "args": args, "accountId": accountId, "region": regionCode}
      
    elif 'getMetricStatistics' in apiName:
      payload_dict = { "apiName": "cloudwatch.getMetricStatistics", "args": args, "accountId": accountId, "region": regionCode}
      
    elif 'searchMetricsForAccount' in apiName:
      payload_dict = { "apiName": "cloudwatchinternal.searchMetricsForAccount", "args": args, "accountId": accountId, "region": regionCode}
      
    elif 'support.searchCases' in apiName or 'support.describeCase' in apiName:
      if "ForResolved" in apiName:
        payload_dict = {"args":args,"apiName":apiName.replace("ForResolved","")}
      else:
        payload_dict = {"args":args,"apiName":apiName}
      #{"args":{"filterBy":{"createdBy":[{"accountId":"393495018094"}],"language":"en"}},"apiName":"support.searchCases","sessionMetadata":{"segment":"asgard_workbench","instance_id":"cdee563b-14b8-4153-89aa-587e30892064-3","name":"cases"},"accessOverrideSession":"3090370c-1644-4280-8870-a012196150d4"}
    elif "avs.getAccountStatus" in apiName:
      payload_dict = {"region": regionCode, "args":args, "apiName":apiName}
    
    elif 'avs' in apiName:
      payload_dict = {"region":regionCode, "accountId": accountId,"args":args,"apiName":apiName}
      #payload = { "apiName": apiName, "args": args, "accessOverrideSession": thisAccessOverrideSession}
    
    elif 'kumoscp.getTags' in apiName:
      payload_dict = {"accountId": accountId, "apiName":apiName, "args":args}
      #payload = { "apiName": apiName, "args": args, "accessOverrideSession": thisAccessOverrideSession}
    
    elif 'kumoscp' in apiName:
      payload_dict = {"args":args, "apiName":apiName}
      #payload = { "apiName": apiName, "args": args, "accessOverrideSession": thisAccessOverrideSession}
    
    elif 'awsadms' in apiName:
      payload_dict = {"accountId": accountId, "apiName":apiName, "args":args, "region": regionCode}
      #payload = { "apiName": apiName, "args": args, "accessOverrideSession": thisAccessOverrideSession}
    
    elif 'lookupEvents' in apiName:
      if isinstance(self.input_dict["startTime"], str) and "T" not in self.input_dict["startTime"]:
        self.input_dict["startTime"] = getDateString(self.input_dict["startTime"], "cloudwatch")
      
      if isinstance(self.input_dict["endTime"], str) and "T" not in self.input_dict["endTime"]:
        self.input_dict["endTime"] = getDateString(self.input_dict["endTime"], "cloudwatch")
      
      logDebug("self.input_dict:[{}]".format(self.input_dict))
      if "inputs" in self.input_dict.keys() and "lookupAttributes" in self.input_dict["inputs"].keys():
        logDebug("self.input_dict['inputs']['lookupAttributes']:[{}]".format(self.input_dict["inputs"]["lookupAttributes"]))
        
        #lookupAttributes_list = [
        #  {
        #    "attributeKey": "EventSource",
        #    "attributeValue": "s3.amazonaws.com"
        #    }
        #  ]
        lookupAttributes_list = []
        for lookupAttributeItem in self.input_dict["inputs"]["lookupAttributes"].split(","):
          lookupAttributeItem_list = lookupAttributeItem.strip().split(":")
          
          if len(lookupAttributeItem_list) > 1:
            if lookupAttributeItem_list[0] in  ["EventId","EventName","ReadOnly","Username","ResourceType","ResourceName","EventSource","AccessKeyId"]:
              lookupAttributes_list.append(
                {
                  "attributeKey":lookupAttributeItem_list[0],
                  "attributeValue":lookupAttributeItem_list[1],
                  }
                )
            else:
              logWarn("unexpected attributeKey:[{}]".format(lookupAttributeItem_list[0]))
              
        payload_dict = {
          "apiName": "cloudtrail.lookupEvents", 
          "args": {
              "startTime": self.input_dict["startTime"], 
              "endTime": self.input_dict["endTime"],
              "lookupAttributes":lookupAttributes_list
              }, 
          "accountId": self.input_dict["accountId"], 
          "region": self.input_dict["regionCode"],
          "sessionMetadata": {
            "segment": "moduAWSv11",
            "name": "CTI:AWS/Enterprise Support/moduAWS",
            "instance_id": "{}-{}".format(self.user, self.requestId)
            }
          }
      else:
        payload_dict = {
          "apiName": "cloudtrail.lookupEvents", 
          "args": {
              "startTime": self.input_dict["startTime"], 
              "endTime": self.input_dict["endTime"]
              }, 
          "accountId": self.input_dict["accountId"], 
          "region": self.input_dict["regionCode"],
          "sessionMetadata": {
            "segment": "moduAWSv11",
            "name": "CTI:AWS/Enterprise Support/moduAWS",
            "instance_id": "{}-{}".format(self.user, self.requestId)
            }
          }
      #payload = { "apiName": apiName, "args": args, "accessOverrideSession": thisAccessOverrideSession}
      
    else:
      payload_dict = {"apiName": apiName, "args": args, "accountId": accountId, "region": regionCode}
      #payload = { "apiName": apiName, "args": k2_arguments, "accountId": accountId, "region": regionCode, "accessOverrideSession": thisAccessOverrideSession} 

    if isinstance(self.input_dict["args"], dict) or isinstance(self.input_dict["args"], list):
      args_text = json.dumps(self.input_dict["args"])
      
    elif isinstance(self.input_dict["args"], str):
      args_text = self.input_dict["args"].strip()
      
    else:
      args_text = ""
      
      logError("unexpected type:{}:[{}]".format(type(self.input_dict["args"]), self.input_dict["args"]))
      
    #logDebug("#args_text:[{}]".format(args_text))
    if args_text != "":
      for inputName in self.input_dict.keys():
        lowerInputName = "{}{}".format(inputName[0].lower(), inputName[1:])
        keyword = "${__" + lowerInputName + "__}"
        if args_text.find(keyword) > 0:
          try:
            if isinstance(self.input_dict[inputName], dict) or isinstance(self.input_dict[inputName], list):
              args_text = args_text.replace(keyword, json.dumps(self.input_dict[inputName]))
            else:
              args_text = args_text.replace(keyword, "{}".format(self.input_dict[inputName]))
          except:
            logException("unable to get payload with inputName:[{}] in type:{}:input_dict:[{}]".format(inputName, type(self.input_dict[inputName]), self.input_dict[inputName]))
        else:
          upperInputName = "{}{}".format(inputName[0].upper(), inputName[1:]) 
          keyword = "${__" + upperInputName + "__}"
          if args_text.find(keyword) > 0:
            try:
              if isinstance(self.input_dict[inputName], dict) or isinstance(self.input_dict[inputName], list):
                args_text = args_text.replace(keyword, json.dumps(self.input_dict[inputName]))
              else:
                args_text = args_text.replace(keyword, "{}".format(self.input_dict[inputName]))
            except:
              logException("unable to get payload with inputName:[{}] in type:{}:input_dict:[{}]".format(inputName, type(self.input_dict[inputName]), self.input_dict[inputName]))
           
      #logDebug("#args_text:'{}'".format(args_text))
      try:
        args_dict = json.loads(args_text)
        if isinstance(args_dict, dict):
          if "args" in payload_dict.keys() and isinstance(payload_dict["args"],dict):
            payload_dict["args"] = {
              **payload_dict["args"],
              **args_dict
              }
          else:
            logWarn("unexpected payload_dict:[{}]".format(payload_dict))
            payload_dict["args"] = {}
        else:
          logError("unexpected format(type:{}):[{}]".format(type(json.loads(self.input_dict["args"].strip())), json.loads(self.input_dict["args"].strip()) ))
          payload_dict["args"] = {}
      except Exception as e:
        errMsg= logException("something wrong at args_text:[{}] at args:'{}'->Error:[{}]".format(args_text, self.input_dict["args"], e))
        payload_dict["error"] = errMsg
    else:
      if "args" in payload_dict.keys() and isinstance(payload_dict["args"],dict):
        pass
      else:
        logWarn("unexpected payload_dict:[{}]".format(payload_dict))
        payload_dict["args"] = {}
      
    if "paginatingToken" in self.input_dict.keys():
      if self.input_dict["paginatingToken"]["key"] == "lastEvaluatedTableName":
        payload_dict["args"]["exclusiveStartTableName"] = self.input_dict["paginatingToken"]["value"]
      elif self.input_dict["paginatingToken"]["key"] in ["nextMarker"]:
        payload_dict["args"]["marker"] = self.input_dict["paginatingToken"]["value"]
      else:
        payload_dict["args"][self.input_dict["paginatingToken"]["key"]] = self.input_dict["paginatingToken"]["value"]
      
      del self.input_dict["paginatingToken"]
      
    if "accessOverrideSession" in self.input_dict.keys() and self.input_dict["accessOverrideSession"] != None:
      payload_dict["accessOverrideSession"] = self.input_dict["accessOverrideSession"]
    
    payload_dict["sessionMetadata"] = {
      "segment": "moduAWSv11",
      "name": "CTI:AWS/Enterprise Support/moduAWS".format(),
      "instance_id": "{}-{}".format(self.user, self.requestId)
      }
    
    #logDebug("#input_dict.keys():[{}]".format(self.input_dict.keys())) 
    #logDebug("#payload_dict:[{}]".format(payload_dict)) 
    
    return payload_dict

  def getRandomRegionCode(self, apiName, regionCode = "us-east-1"):
    if "describeRegions" in apiName:
      if "cn-" in regionCode:
        return regionCode
      else:
        regionCode_list = ["eu-north-1",
                           "ap-south-1",
                            "eu-west-3",
                            "eu-west-2",
                            "eu-west-1",
                            "ap-northeast-3",
                            "ap-northeast-2",
                            "ap-northeast-1",
                            "sa-east-1",
                            "ca-central-1",
                            "ap-southeast-1",
                            "ap-southeast-2",
                            "eu-central-1",
                            "us-east-1",
                            "us-east-2",
                            "us-west-1",
                            "us-west-2"]
        
        return regionCode_list[int(17 * random.random())]
    else:
      return regionCode
    
  def getCwPayload(self):
    #logDebug("#self.input_dict:[{}]".format(self.input_dict))
    
    dimension_list = []
    if "dimensions" in self.input_dict.keys():
      if isinstance(self.input_dict["dimensions"], str):
        try:
          for dimensionItemMap in self.input_dict["dimensions"].strip().split(","):
            dimensionItemMap_list = dimensionItemMap.strip().split(":")
            if len(dimensionItemMap_list) == 2:
              if dimensionItemMap_list[1] in self.input_dict.keys():
                #logDebug("dimensionKey:[{}]->dimensionValue:[{}]".format(dimensionItemMap_list[1], self.input_dict[dimensionItemMap_list[1]]))
                if dimensionItemMap_list[1] == self.input_dict[dimensionItemMap_list[1]]:
                  self.input_dict[dimensionItemMap_list[1]] = None
                else:
                  dimension_list.append({"name":dimensionItemMap_list[0], "value":self.input_dict[dimensionItemMap_list[1]]})
              else:
                logError("dimension:[{}]->[{}] is not found at input_dict:[{}]".format(dimensionItemMap_list[0], dimensionItemMap_list[1], self.input_dict))
            else:
              logError("dimensionMap:[{}] is not mapped at input_dict:[{}]".format(dimensionItemMap, self.input_dict))
          #logDebug("#dimension_list:[{}]".format(dimension_list))
        except Exception as e:
          logError("unable to map dimensions with input_dict:[{}]".format(self.input_dict))
      
      elif isinstance(self.input_dict["dimensions"], list):
        dimension_list = self.input_dict["dimensions"]
      else:
        logError("unexpected type:{}:dimensions:[{}]".format(type(self.input_dict["dimensions"]), self.input_dict["dimensions"]))
    
    try:
      statistic_list = []
      for thisStatistic in self.input_dict["thisStatistics"].split(","):
        if thisStatistic.lower() == "average" and "Average" not in statistic_list:
          statistic_list.append("Average")
        elif thisStatistic.lower() == "sum" and "Sum" not in statistic_list:
          statistic_list.append("Sum")
        elif thisStatistic.lower() == "minimum" and "Minimum" not in statistic_list:
          statistic_list.append("Minimum")
        elif thisStatistic.lower() == "maximum" and "Maximum" not in statistic_list:
          statistic_list.append("Maximum")
        elif thisStatistic.lower() == "sampleCount" and "SampleCount" not in statistic_list:
          statistic_list.append("SampleCount")
        else:
          logWarn("Somethign wrong:[{}]".format(thisStatistic))
          
    except:
      statistic_list = ["Average","Sum","Minimum","Maximum","SampleCount"]
    
    if isinstance(self.input_dict["startTime"], int):
      startTime = self.input_dict["startTime"]
      
    elif isinstance(self.input_dict["startTime"], float):
      startTime = int(self.input_dict["startTime"]) * 1000
      self.input_dict["startTime"] = startTime
     
    elif isinstance(self.input_dict["startTime"], str):
      try:
        startTime = int(self.input_dict["startTime"])
        self.input_dict["startTime"] = startTime
      except:
        try:
          startTime = int((datetime.strptime(self.input_dict["startTime"], "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()*1000)
          self.input_dict["startTime"] = startTime
        except:
          try:
            startTime = int((datetime.strptime(self.input_dict["startTime"], "%Y-%m-%dT%H:%M:%SZ") - datetime(1970, 1, 1)).total_seconds()*1000)
            self.input_dict["startTime"] = startTime
          except:
            try:
              startTime = int((datetime.strptime(self.input_dict["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime(1970, 1, 1)).total_seconds()*1000)
              self.input_dict["startTime"] = startTime
            except:
              try:
                startTime = int((datetime.strptime(self.input_dict["startTime"], "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()*1000)
                self.input_dict["startTime"] = startTime
              except:
                try:
                  startTime = int((datetime.strptime(self.input_dict["startTime"], "%Y-%m-%d %H:%M:%S.%f") - datetime(1970, 1, 1)).total_seconds()*1000)
                  self.input_dict["startTime"] = startTime
                except:
                  try:
                    startTime = getDateString(self.input_dict["startTime"], "cloudwatch")
                  except:
                    startTime = self.input_dict["startTime"]
    
    try:
      if startTime < 10000000000:
        startTime = startTime * 1000
    except:
      logExceptionWithValueError("startTime:[{}]".format(startTime))
        
    if isinstance(self.input_dict["endTime"], int):
      
      endTime = self.input_dict["endTime"]
    elif isinstance(self.input_dict["endTime"], float):
      endTime = int(self.input_dict["endTime"]) * 1000
      self.input_dict["endTime"] = endTime
    elif isinstance(self.input_dict["endTime"], str):
      try:
        endTime = int(self.input_dict["endTime"])
        self.input_dict["endTime"] = endTime
      except:
        try:
          endTime = int((datetime.strptime(self.input_dict["endTime"], "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()*1000)
          self.input_dict["endTime"] = endTime
        except:
          try:
            endTime = int((datetime.strptime(self.input_dict["endTime"], "%Y-%m-%dT%H:%M:%SZ") - datetime(1970, 1, 1)).total_seconds()*1000)
            self.input_dict["endTime"] = endTime
          except:
            try:
              endTime = int((datetime.strptime(self.input_dict["endTime"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime(1970, 1, 1)).total_seconds()*1000)
              self.input_dict["endTime"] = endTime
            except:
              try:
                endTime = int((datetime.strptime(self.input_dict["endTime"], "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()*1000)
                self.input_dict["endTime"] = endTime
              except:
                try:
                  endTime = int((datetime.strptime(self.input_dict["endTime"], "%Y-%m-%d %H:%M:%S.%f") - datetime(1970, 1, 1)).total_seconds()*1000)
                  self.input_dict["endTime"] = endTime
                except:
                  try:
                    endTime = getDateString(self.input_dict["endTime"], "cloudwatch")
                  except:
                    endTime = self.input_dict["endTime"]
        
    
    try:
      if endTime < 10000000000:
        endTime = endTime * 1000
    except:
      logExceptionWithValueError("endTime:[{}]".format(endTime))
    
    if isinstance(startTime, int) and isinstance(endTime, int):
      if startTime > endTime:
        raiseValueError("The parameter StartTime:[{}] must be less than the parameter EndTime:[{}].".format(self.input_dict["startTime"], self.input_dict["endTime"]))
    
      else:
        try:
          if len(dimension_list) > 0 and isinstance(dimension_list[0], dict):
            cwPayload_dict = {
              "apiName": "cloudwatch.getMetricStatistics", 
              "args": {"namespace": self.input_dict["namespace"], 
                        "metricName": self.input_dict["metricName"], 
                        "dimensions": dimension_list, 
                        "period": self.input_dict["period"], 
                        "statistics": statistic_list, 
                        "startTime": startTime, 
                        "endTime": endTime
                        }, 
              "accountId": self.input_dict["accountId"], 
              "region": self.input_dict["regionCode"],
              "sessionMetadata": {
                                  "segment": "moduAWSv11",
                                  "name": "CTI:AWS/Enterprise Support/moduAWS".format(),
                                  "instance_id": "{}-{}".format(self.user, self.requestId)
                                  }
              }
          else:
            cwPayload_dict = {
              "apiName": "cloudwatch.getMetricStatistics", 
              "args": {"namespace": self.input_dict["namespace"], 
                        "metricName": self.input_dict["metricName"], 
                        "period": self.input_dict["period"], 
                        "statistics": statistic_list, 
                        "startTime": startTime, 
                        "endTime": endTime
                        }, 
              "accountId": self.input_dict["accountId"], 
              "region": self.input_dict["regionCode"],
              "sessionMetadata": {
                                  "segment": "moduAWSv11",
                                  "name": "CTI:AWS/Enterprise Support/moduAWS".format(),
                                  "instance_id": "{}-{}".format(self.user, self.requestId)
                                  }
              }
          
          if "accessOverrideSession" in self.input_dict.keys():
            cwPayload_dict["accessOverrideSession"] = self.input_dict["accessOverrideSession"]
          
        except Exception as e:
          logException("unable to get cw payload with input_dict:[{}]->Error:[{}]".format(self.input_dict, e))
          cwPayload_dict = {}
    else:
      logError("unexpected startTime:[{}] or endTime:[{}]".format(self.input_dict["startTime"], self.input_dict["endTime"]))
      cwPayload_dict = {}
      
    #logDebug("#cwPayload_dict:[{}]".format(cwPayload_dict))
    
    return cwPayload_dict  