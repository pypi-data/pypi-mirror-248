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
Created on June 21, 1998

@author: Ryeojin Moon
'''
#from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from graphcode.io import getItemWithS3, putItemWithS3, deleteItemWithS3

from graphcode.csv import GcCsv

from graphcode.workbench import workbenchV3

from os import listdir
from os.path import exists, expanduser, join

import json
import copy

def getWbResultsToList(request_dict, request_list):
  if "serviceName" in request_dict["attributes"].keys():
    serviceName = request_dict["attributes"]["serviceName"]
  else:
    try:
      serviceName = request_list[-1]["serviceName"]
    except:
      serviceName = "-"
  logDebug("serviceName:[{}]".format(serviceName))
  
  try:
    wbResult_dict = workbenchV3(user_dict=request_dict["metadata"], request_list=request_list)
        
  except Exception as e:
    errMsg = logException("unable to load 'wbResult_dict'->Error:[{}]".format(e))
    wbResult_dict = {"error":[{"error":errMsg}]}
  
  thisResult_list = []
  for wbResultIndex in wbResult_dict.keys():
    if "nosave" in wbResultIndex:
      continue
    
    try:
      if isinstance(wbResult_dict[wbResultIndex], list) and isinstance(wbResult_dict[wbResultIndex][-1], dict):
        if "error" in wbResult_dict[wbResultIndex][-1].keys():
          wbResult_dict[wbResultIndex][-1]["serviceName_"] = serviceName
          thisResult_list.append(
            {
              "snapshotDate": None,
              "dataSources":None,
              "serviceName_": None,
              "accountId_": request_list[-1]["accountId"],
              "regionCode_": request_list[-1]["regionCode"],
              "apiName_": wbResultIndex,
              "resultCount": None,
              "requestCount": None,
              "error": None,
              "results": None,
              "lastRequest":None,
              "snapshotDate":None,
              **wbResult_dict[wbResultIndex][-1]
              }
            )
        else:
          for wbResultItem_dict in wbResult_dict[wbResultIndex]:
            #if "resourceName_" in wbResultItem_dict.keys():
            #    logDebug("resourceName_:[{}]".format(wbResultItem_dict["resourceName_"]))
            wbResultItem_dict["serviceName_"] = serviceName
            
            thisResult_list.append(
              {
                "snapshotDate":None,
                "dataSources":None,
                **wbResultItem_dict
                }
              )
      else:
        logError("unexpected type:{}:wbResult_dict[{}]:{}".format(type(wbResult_dict[wbResultIndex]), wbResultIndex, wbResult_dict[wbResultIndex]))
    except:
      try:
        thisResult_list.append(
            {
              "snapshotDate":None,
              "dataSources":None,
              "apiName_": wbResultIndex,
              **request_list[-1],
              "resultCount":-999,
              "results": wbResult_dict[wbResultIndex],
              "error": logException("unable to count wbResult_dict[{}]".format(wbResultIndex)),
              }
            )
      except:
        thisResult_list.append(
            {
              "snapshotDate":None,
              "dataSources":None,
              "apiName_": wbResultIndex,
              "request_list": request_list,
              "resultCount":-999,
              "results": wbResult_dict[wbResultIndex],
              "error": logException("unable to count wbResult_dict[{}]".format(wbResultIndex)),
              }
            )
  
  namedResource_list = []
  unNamedResource_list = []
  namedResource_dict = {}
  count = 0
  for thisResultItem_dict in thisResult_list:
    if "resourceName_" in thisResultItem_dict.keys() and thisResultItem_dict["resourceName_"] != None:
      if thisResultItem_dict["resourceName_"] in namedResource_dict.keys():
        #logInfo("#(#{})\tapiName_:[{}]->resourceName_:[{}]->thisResultItem_dict.keys():[{}]".format(count, 
        #                                                                                            thisResultItem_dict["apiName_"], 
        #                                                                                            thisResultItem_dict["resourceName_"], 
        #                                                                                            thisResultItem_dict.keys()
        #                                                                                            )
        #)
        
        try:
          #if "{}".format(thisResultItem_dict["apiName_"]) in namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]:
          #  logError("duplicated thisResultItem_dict:[{}]".format(thisResultItem_dict))
          #else:
          #  #logInfo("#dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
          #  namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"].append("{}".format(thisResultItem_dict["apiName_"]))
          namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"].append("{}".format(thisResultItem_dict["apiName_"]))
        
        except:
          logException("'apiName_' is not found at thisResultItem_dict:[{}]".format(thisResultItem_dict))
          
        if "getMetricStatistics" in thisResultItem_dict["apiName_"]:
          for key in thisResultItem_dict.keys():
            if key == "dataSources":
              continue
            
            if key in ["snapshotDate", 
                       "apiName_",
                       "resourceName_", 
                       "serviceName_", 
                       "accountId_", 
                       "regionCode_", 
                       "namespace",
                       "metricName"
                       ] or key.startswith("dimension/"):
                
              if key in namedResource_dict[thisResultItem_dict["resourceName_"]].keys():
                if isinstance(namedResource_dict[thisResultItem_dict["resourceName_"]][key], list):
                  if thisResultItem_dict[key] in namedResource_dict[thisResultItem_dict["resourceName_"]][key]:
                    pass#logWarn("#duplicated value:[{}]".format(thisResultItem_dict["resourceName_"]))
                  else:
                    namedResource_dict[thisResultItem_dict["resourceName_"]][key].append(thisResultItem_dict[key])
                else:
                  if thisResultItem_dict[key] == namedResource_dict[thisResultItem_dict["resourceName_"]][key]:
                    pass#logWarn("#duplicated value:[{}]".format(thisResultItem_dict["resourceName_"]))
                  else:
                    namedResource_dict[thisResultItem_dict["resourceName_"]][key] = [namedResource_dict[thisResultItem_dict["resourceName_"]][key], thisResultItem_dict[key]]
              else:
                namedResource_dict[thisResultItem_dict["resourceName_"]][key] = thisResultItem_dict[key]
              
            else:
              #logInfo("#2\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
              if key in namedResource_dict[thisResultItem_dict["resourceName_"]].keys():
                if isinstance(namedResource_dict[thisResultItem_dict["resourceName_"]][key], dict):
                  namedResource_dict[thisResultItem_dict["resourceName_"]][key][thisResultItem_dict["metricName"]] = thisResultItem_dict[key]
                elif thisResultItem_dict[key] not in namedResource_dict[thisResultItem_dict["resourceName_"]][key]:
                  #logDebug("#key:[{}]->type:{}:[{}]".format(key, type(namedResource_dict[thisResultItem_dict["resourceName_"]][key]), namedResource_dict[thisResultItem_dict["resourceName_"]][key]))
                  namedResource_dict[thisResultItem_dict["resourceName_"]][key] = "{},{}".format(namedResource_dict[thisResultItem_dict["resourceName_"]][key], thisResultItem_dict[key])
                #else:
                #  pass
              else:
                namedResource_dict[thisResultItem_dict["resourceName_"]][key] = {}
                namedResource_dict[thisResultItem_dict["resourceName_"]][key][thisResultItem_dict["metricName"]] = thisResultItem_dict[key]
              #logInfo("#3\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
            
          #logInfo("#4dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
          
        else:
          count += 1
          for key in thisResultItem_dict.keys():
            if key == "dataSources":
              continue
            
            if key in namedResource_dict[thisResultItem_dict["resourceName_"]].keys():
              if isinstance(namedResource_dict[thisResultItem_dict["resourceName_"]][key], list):
                if thisResultItem_dict[key] in namedResource_dict[thisResultItem_dict["resourceName_"]][key]:
                  pass#logWarn("#duplicated value:[{}]".format(thisResultItem_dict["resourceName_"]))
                else:
                  namedResource_dict[thisResultItem_dict["resourceName_"]][key].append(thisResultItem_dict[key])
              else:
                if thisResultItem_dict[key] == namedResource_dict[thisResultItem_dict["resourceName_"]][key]:
                  pass#logWarn("#duplicated value:[{}]".format(thisResultItem_dict["resourceName_"]))
                else:
                  namedResource_dict[thisResultItem_dict["resourceName_"]][key] = [
                    "{}".format(namedResource_dict[thisResultItem_dict["resourceName_"]][key]), 
                    thisResultItem_dict[key]
                    ]
            else:
              namedResource_dict[thisResultItem_dict["resourceName_"]][key] = thisResultItem_dict[key]
        
      
      # if thisResultItem_dict["resourceName_"] in namedResource_dict.keys():
      else:
        #logInfo("#(#{})\tapiName_:[{}]->resourceName_:[{}]->thisResultItem_dict.keys():[{}]".format(count, 
        #                                                                                            thisResultItem_dict["apiName_"], 
        #                                                                                            thisResultItem_dict["resourceName_"], 
        #                                                                                            thisResultItem_dict.keys()
        #                                                                                            )
        #)
        count += 1
        
        try:
          namedResource_dict[thisResultItem_dict["resourceName_"]] = {}
          namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"] = [thisResultItem_dict["apiName_"]]
          #logInfo("#1dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
          if "getMetricStatistics" in thisResultItem_dict["apiName_"]:
            for key in thisResultItem_dict.keys():
              if key == "dataSources":
                continue
              
              if key in ["snapshotDate", 
                         "apiName_",
                         "resourceName_", 
                         "serviceName_", 
                         "accountId_", 
                         "regionCode_", 
                         "namespace",
                         "metricName",
                       ] or key.startswith("dimension/"):
                namedResource_dict[thisResultItem_dict["resourceName_"]][key] = thisResultItem_dict[key]
              
              else:
                #logInfo("#2\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
                namedResource_dict[thisResultItem_dict["resourceName_"]][key] = {}
                namedResource_dict[thisResultItem_dict["resourceName_"]][key][thisResultItem_dict["metricName"]] = thisResultItem_dict[key]
                #logInfo("#3\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
              
            #logInfo("#4dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
            
          else:
            for key in thisResultItem_dict.keys():
              if key == "dataSources":
                continue
              
              #logInfo("#2\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
              namedResource_dict[thisResultItem_dict["resourceName_"]][key] = thisResultItem_dict[key]
              #logInfo("#3\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
              
            #logInfo("#4dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
            
        except:
          logException("unexpected thisResultItem_dict:[{}]".format(thisResultItem_dict))
          namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"] = ["x"]
          #logInfo("#1dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
          
          for key in thisResultItem_dict.keys():
            if key == "dataSources":
              continue
            
            #logInfo("#2\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
            namedResource_dict[thisResultItem_dict["resourceName_"]][key] = thisResultItem_dict[key]
            #logInfo("#3\tkey:[{}]->dataSources:[{}]".format(key, namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
            
          #logInfo("#4dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
          
        #logInfo("#5dataSources:[{}]".format(namedResource_dict[thisResultItem_dict["resourceName_"]]["dataSources"]))
        
    else:
      #logInfo("#'resourceName_' is not found at thisResultItem_dict:[{}]".format(thisResultItem_dict))
      try:
        unNamedResource_list.append(thisResultItem_dict)
      except:
        logException("unexpected thisResultItem_dict:[{}]".format(thisResultItem_dict))
      
  
  for key in namedResource_dict.keys():
    try:
      del namedResource_dict[key]["apiName_"]
    except:
      logException("unexpected namedResource_dict[{}]".format(key, namedResource_dict[key]))
      
    namedResource_list.append(namedResource_dict[key])
  
  if len(namedResource_list) > 0:
    return namedResource_list
  
  else:
    return unNamedResource_list   

def getWbResults(serviceName, request_dict, apiList):
  try:
    thisRequest_list = [
        {
          "accountId":request_dict["accountId"],
          "regionCode":request_dict["regionCode"],
          "serviceName": serviceName,
          "apiList": apiList
          }
      ]
  except:
    return [
        {
          "error": logException("unexpected request_dict:[{}]".format(request_dict))
          }
      ]
  logDebug("thisRequest_list:[{}]".format(thisRequest_list))
  
  #thisResult_list = []
  thisResult_list = getWbResultsToList(request_dict=request_dict, request_list=thisRequest_list)
  
  if len(thisResult_list) > 0:
    resultText = "{}".format(thisResult_list[-1])
    if len(resultText) > 2049:
      logDebug("thisResult_list(len:{:,})[-1]:[{}...{}]".format(len(thisResult_list), resultText[:1024], resultText[-1024:]))
    else:
      logDebug("thisResult_list(len:{:,})[-1]:[{}]".format(len(thisResult_list), resultText))
    
    isGetMetricStatisticsFound = False
    for apiRequest_dict in apiList:
      if "getMetricStatistics" in apiRequest_dict["apiName"]:
        isGetMetricStatisticsFound = True
        
        newThisResult_list = []
        
        resultCount = 0
        totalResultNumber = len(thisResult_list)
        if len(thisResult_list) > 10:
          percentageDelimiter = int(totalResultNumber/3) -1
        else:
          percentageDelimiter = 1
        for thisResultItem_dict in thisResult_list:
          resultCount += 1
          if (resultCount % percentageDelimiter) == 0:
            logDebug("(#{:,}/{:,})\tthisResultItem_dict:[{}]".format(resultCount, totalResultNumber, thisResultItem_dict))
            
          if "maxAverage" in thisResultItem_dict.keys():
            if isinstance(thisResultItem_dict["maxAverage"], dict):
              accessStatus = "inActive"
              
              for thisKey in thisResultItem_dict["maxAverage"].keys():
                try:
                  if thisResultItem_dict["maxAverage"][thisKey] != thisResultItem_dict["minAverage"][thisKey]:
                    accessStatus = "active"
                    break
                except:
                  logException("unexpected thisResultItem_dict[minAverage]:[{}]".format(thisResultItem_dict["minAverage"]))
                  
              newThisResult_list.append(
                {
                  **thisResultItem_dict,
                  "accessStatus": accessStatus,
                  **thisResultItem_dict["maxAverage"]
                  }
                )
            elif thisResultItem_dict["maxAverage"] == None:
              thisResultItem_dict["accessStatus"] = "inActive"
            else:
              thisResultItem_dict["accessStatus"] = "active"
          else:
            newThisResult_list.append(thisResultItem_dict)
            
        thisResult_list = newThisResult_list
    
    if isGetMetricStatisticsFound:
      logDebug("apiList has 'getMetricStatistics'")
    else:
      logDebug("apiList doesn't have 'getMetricStatistics'")
  
  if isinstance(thisResult_list, list):
    logDebug("thisResult_list(len:{:,})[-1]:[{}]".format(len(thisResult_list), thisResult_list[-1]))
  else:
    
    logDebug("thisResult_list:[{}]".format(thisResult_list))
    
  return thisResult_list

def loadWbRsults(request_dict, wbResult_dict, tableName, apiNames):
  if isinstance(apiNames, list):
    pass
  else:
    raiseValueError("'list' type is expected instead of type:{}:[{}]".format(type(apiNames), apiNames))
    
  # Read Data 
  for apiName in apiNames:
    try:
      if apiName in wbResult_dict.keys():
        pass
      else:
        wbResult_dict["{}".format(apiName)] = getItemWithS3(request_dict=request_dict, tableName=tableName, key=apiName, format="json")
      
    except Exception as e:
      wbResult_dict["{}_noData".format(apiName)] = [{"error":"no_data"}]
      #logError("unable to get '{}->Error:[{}]'".format(apiName, e))
 
  return wbResult_dict

def saveWbResultsToCsv(request_dict, wbResult_dict):
  for apiName in wbResult_dict.keys():
    if len(wbResult_dict[apiName]) > 0:
      try:
        csvFilename = join(expanduser("~/moduAWS-temp/Downloads"),"{}_{}.csv".format(apiName, request_dict["cookies"]["loginAliasId"]))   
        if request_dict["actionStatus"] == True:
          gcCsv = GcCsv(wbResult_dict[apiName], request_dict)
        else:
          gcCsv = GcCsv(wbResult_dict[apiName])
        request_dict["outputs"]["wbResults"][apiName] = gcCsv.get()
        if len(request_dict["outputs"]["wbResults"][apiName]["data"]) > 1000:
          request_dict["outputs"]["wbResults"][apiName]["data"] = copy.deepcopy(request_dict["outputs"]["wbResults"][apiName]["data"][:1000])
        
        if len(wbResult_dict[apiName]) == 0:
          pass
        elif len(wbResult_dict[apiName]) == 1 and "error" in wbResult_dict[apiName][-1].keys():
          pass
        elif request_dict["outputFormat"] == False and request_dict["actionStatus"] == False:
          pass
        else:
          request_dict["outputs"]["wbResults"][apiName]["file"] = gcCsv.save(csvFilename).split("/")[-1]
        
      except Exception as e:
        logException("unable to store api results")