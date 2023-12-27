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

import json

class Boto3Args():
  def __init__(self, inputs):
    self.input_dict = inputs
    
    if "boto3ArgParse" in self.input_dict.keys():
      if self.input_dict["boto3ArgParse"] not in ["True", "true", True]:
        self.boto3ArgParse = False
      else:
        self.boto3ArgParse = True
    else:
      self.boto3ArgParse = True
    
  def get(self):
    args_text = self.input_dict["args"].strip()
    logDebug("args_text:[{}]".format(args_text))
    if args_text != "":
      for inputName in self.input_dict.keys():
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
         
        else:
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
           
      
      logDebug("args_text:[args_text]")
      try:
        args_dict = json.loads(args_text)
        logDebug("args_dict:[{}]".format(args_dict))
        if self.boto3ArgParse and isinstance(args_dict, dict):
          newArg_dict = {}
          for key in args_dict.keys():
            newArg_dict["{}{}".format(key[0].upper(), key[1:])] = args_dict[key]
          args_dict = newArg_dict
          logDebug("args_dict:[{}]".format(args_dict))
        else:
          logWarn("unexpected format(type:{}):[{}]".format(type(json.loads(self.input_dict["args"].strip())), json.loads(self.input_dict["args"].strip()) ))
      except:
        logException("boto3ArgParse:[{}] or unable to load k2args:[{}]".format(self.boto3ArgParse, self.input_dict["args"].strip()))
        args_dict = {}
    else:
      args_dict = {}
    
    if "paginatingToken" in self.input_dict.keys():
      if self.input_dict["paginatingToken"]["key"] == "lastEvaluatedTableName":
        args_dict["exclusiveStartTableName"] = self.input_dict["paginatingToken"]["value"]
      else:
        args_dict[self.input_dict["paginatingToken"]["key"]] = self.input_dict["paginatingToken"]["value"]
      
      del self.input_dict["paginatingToken"]
    
    
    logDebug("input_dict.keys():[{}]".format(self.input_dict.keys())) 
    logDebug("args_dict:type:{}:[{}]".format(type(args_dict),args_dict))
    
    return args_dict
  
  
  
  def getCwPayload(self):
    logDebug("self.input_dict:[{}]".format(self.input_dict))
    
    dimension_list = []
    try:
      if "dimensions" in self.input_dict.keys():
        dimensionString = "dimensions"
      else:
        dimensionString = "Dimensions"
        
      if isinstance(self.input_dict[dimensionString], str):
        for dimensionItemMap in self.input_dict[dimensionString].strip().split(","):
          dimensionItemMap_list = dimensionItemMap.strip().split(":")
          if len(dimensionItemMap_list) == 2:
            if dimensionItemMap_list[1] in self.input_dict.keys():
              
              logDebug("dimensionKey:[{}]->dimensionValue:[{}]".format(dimensionItemMap_list[1], self.input_dict[dimensionItemMap_list[1]]))
              if dimensionItemMap_list[1] == self.input_dict[dimensionItemMap_list[1]]:
                self.input_dict[dimensionItemMap_list[1]] = None
              else:
                dimension_list.append({"Name":dimensionItemMap_list[0], "Value":self.input_dict[dimensionItemMap_list[1]]})
            elif "{}{}".format(dimensionItemMap_list[1][0].upper(), dimensionItemMap_list[1][1:]) in self.input_dict.keys():
              upperKey = "{}{}".format(dimensionItemMap_list[1][0].upper(), dimensionItemMap_list[1][1:])
              logDebug("dimensionKey:[{}]->dimensionValue:[{}]".format(upperKey, self.input_dict[upperKey]))
              if upperKey == self.input_dict[upperKey]:
                self.input_dict[upperKey] = None
              else:
                dimension_list.append({"Name":dimensionItemMap_list[0], "Value":self.input_dict[upperKey]})
            else:
              logWarn("dimensionKey:[{}]->[{}] is not found at input_dict:[{}]".format(dimensionItemMap_list[0], dimensionItemMap_list[1], self.input_dict))
              
          else:
            logWarn("dimensionMap:[{}] is not mapped".format(dimensionItemMap))
      else:
        dimension_list = self.input_dict[dimensionString]
        
      logDebug("dimension_list:[{}]".format(dimension_list))
    except Exception as e:
      logException("unable to map dimensions with input_dict:[{}]".format(self.input_dict))

    
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
    
    if "period" in self.input_dict.keys():
      periodString = "period"
    else:
      periodString = "Period"
    
    if "namespace" in self.input_dict.keys():
      namespaceString = "namespace"
    else:
      namespaceString = "Namespace"
    
    if "metricName" in self.input_dict.keys():
      metricNameString = "metricName"
    else:
      metricNameString = "MetricName"
    
    
    cwPayload_dict = {"Namespace": self.input_dict[namespaceString], 
                      "MetricName": self.input_dict[metricNameString], 
                      "Dimensions": dimension_list, 
                      "Period": self.input_dict[periodString], 
                      "Statistics": statistic_list, 
                      "StartTime": self.input_dict["startTime"], 
                      "EndTime": self.input_dict["endTime"]
                      }    
      
    logDebug("cwPayload_dict:[{}]".format(cwPayload_dict))
    
    return cwPayload_dict
