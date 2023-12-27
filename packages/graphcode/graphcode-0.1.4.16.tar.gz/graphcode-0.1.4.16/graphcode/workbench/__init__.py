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
from graphcode.workbench.unpack import GcWbUnpack
from graphcode.workerV3 import GcWorker

from tammy.k2 import K2

from multiprocessing import Pool, cpu_count

from uuid import uuid4

import copy

def generateWbRequests(user_dict, request_list, apiList):
  if isinstance(apiList, list) == False:
    logError("unexpected format:type:[{}] must be 'list'".format(type(apiList)))
    return None
  
  if len(apiList) == 0:
    logError("apiList:type:{}:[{}] must have a single item".format(type(apiList), apiList))
    return None
  
  errMsg_list = []
  thisApiList = []
  for apiItem_dict in thisApiList:
    if "apiName" in apiItem_dict.keys() and apiItem_dict["apiName"].startswith("#") != False:
      thisApiList.append(apiItem_dict)
    else:
      errMsg_list.append("'apiName' is not found at apiItem_dict:[{}]".format(apiItem_dict))
  thisApiList = thisApiList
  
  if len(errMsg_list) > 0:
    logError("unexpected apiList:[{}]".format(errMsg_list))
    return None
  
  for request_dict in request_list:
    try:
      request_dict["apiList"] = apiList
        
    except:
      logException("unable to add 'apiList' to request_dict:type:{}:[{}]".format(type(request_dict), request_dict))
  
  logDebug("request_list:[len:{:,}]".format(len(request_list)))
  
  return request_list
    
def workbenchV3(user_dict, request_list, apiList = None):
  hasK2RespondedAsExpected = {"apiCount":-1, "status":False, "errMsg":None}
  
  if apiList != None:
    request_list = generateWbRequests(user_dict, request_list, apiList)
  logDebug("total {:,} requests are requested".format(len(request_list)))
  
  thisRequests_dict= {}
  apiRequestList_dict = {}
  for request_dict in request_list:
    if isinstance(request_dict, dict) and "apiList" in request_dict.keys() and isinstance(request_dict["apiList"],list):
      apiCount = 0
      for apiRequest_dict in request_dict["apiList"]:
        #
        #commeted out to check the midway cookie status
        #
        #if apiRequest_dict["platform"] in ["k2","K2"] and hasK2RespondedAsExpected["status"] == False:
        #  if hasK2RespondedAsExpected["apiCount"] >= 0:
        #    return {"error":
        #            [
        #              {
        #                "error": hasK2RespondedAsExpected["errMsg"]
        #                }
        #              ]
        #            }
        #  else:
        #    k2 = K2(userAccountId= user_dict["cookies"]["awsAccountId"], loginAliasId= user_dict["cookies"]["loginAliasId"])
        #    k2Result_list = k2.get(
        #      { 
        #        "accountId":user_dict["cookies"]["awsAccountId"], 
        #        "regionCode": "us-east-1", 
        #        "apiName":"ec2.describeRegions", 
        #        "args": {}
        #        }
        #      )
        #    try:
        #      if len(k2Result_list) == 1 and k2Result_list[0]["statusCode"] != 200:
        #        logInfo("=====>k2Result_list:[{}]".format(k2Result_list[0]["error"]))
        #        hasK2RespondedAsExpected["apiCount"] =  apiCount
        #        hasK2RespondedAsExpected["status"] =  False
        #        hasK2RespondedAsExpected["errMsg"] =  "{} in {}(StatusCode:{})".format(k2Result_list[0]["error"], k2Result_list[0]["regionCode_"], k2Result_list[0]["statusCode"])
        #        return {
        #          "error": [
        #            {
        #              "error": hasK2RespondedAsExpected["errMsg"]
        #              }
        #            ]
        #          }
        #      else:
        #        logInfo("=====>k2Result_list:[{}]".format(k2Result_list[0]))
        #        hasK2RespondedAsExpected["apiCount"] =  apiCount
        #        hasK2RespondedAsExpected["status"] =  True
        #    except:
        #      logException("unexpected k2Result:[{}]".format(k2Result_list))
              
        if apiRequest_dict["apiName"].startswith("#"):
          continue
        
        if apiCount == 0:
          if apiCount in thisRequests_dict.keys():
            thisRequests_dict[apiCount].append({**apiRequest_dict, **request_dict})
          else:
            thisRequests_dict[apiCount] = [{**apiRequest_dict, **request_dict}]
        else:
          if apiCount in thisRequests_dict.keys():
            if "{}".format(apiRequest_dict) in apiRequestList_dict.keys():
              pass
            else:
              thisRequests_dict[apiCount].append(apiRequest_dict)
          else:
            thisRequests_dict[apiCount] = [apiRequest_dict]
            apiRequestList_dict["{}".format(apiRequest_dict)] = None
          
        pass#logDebug("thisRequests_dict[{}][-1]:{}".format(apiCount, thisRequests_dict[apiCount][-1]))
        
        apiCount += 1
      
      del request_dict["apiList"]
    else:
      logWarn("'apiList' is not found:[{}]".format(request_dict))
      
  for apiCount in thisRequests_dict.keys():
    logDebug("apiCount:[{}]->total {:,} requests are requested".format(apiCount, len(thisRequests_dict[apiCount])))
    
  processNumer = cpu_count()
  
  wbResult_dict = {}
  for apiCount in thisRequests_dict.keys():
    #for indexKey in wbResult_dict.keys():
    #  logDebug("====xxxxxxxxx=======>{}:indexKey:[{}](len:{})".format(apiCount, indexKey, len(wbResult_dict)))
    
    if apiCount == 0:
      thisRequest_list = thisRequests_dict[apiCount]
    else:
      thisRequest_list = []
      thisApiRequestIndex_dict = {}
      for apiRequest_dict in thisRequests_dict[apiCount]:
        try:
          gcWbUnpack = GcWbUnpack(meta_dict= {}, apiRequest_dict=apiRequest_dict, wbResult_dict= wbResult_dict)
        except:
          logException("unable to set 'gcWbUnpack'")
          continue
        
        targetKey_dict= {}
        if isinstance(apiRequest_dict, dict) and "inputs" in apiRequest_dict.keys():
          if isinstance(apiRequest_dict["inputs"], dict) and "targetValues" in apiRequest_dict["inputs"].keys():
            for tartgetMappingString in apiRequest_dict["inputs"]["targetValues"].split(","):
              if len(tartgetMappingString.split(":")) > 0:
                targetKey_dict[tartgetMappingString.split(":")[0]]= None
          elif isinstance(apiRequest_dict["inputs"], str):
            for inputSring in apiRequest_dict["inputs"].split(";"):
              if "targetValues=" in inputSring.strip():
                for tartgetMappingString in inputSring.split("=")[-1].split(","):
                  if len(tartgetMappingString.split(":")) > 0:
                    targetKey_dict[tartgetMappingString.split(":")[0]]= None
        
        indexKey = ""
        for thisRequest_dict in gcWbUnpack.get():
          for targetKey in targetKey_dict.keys():
            if targetKey in thisRequest_dict.keys():
              indexKey += "{}".format(thisRequest_dict[targetKey])
            
          try:  
            if indexKey in thisApiRequestIndex_dict.keys():
              pass
            elif "accountId" in thisRequest_dict.keys() and isinstance(thisRequest_dict["accountId"], str) and thisRequest_dict["accountId"].startswith("accountId"):
              logWarn("removed thisRequest_dict:[{}]".format(thisRequest_dict))
            else:
              thisRequest_list.append(thisRequest_dict)
              pass#logDebug("#{}:thisRequest_list[-1]:{}".format(apiCount, thisRequest_list[-1]))
              
              thisApiRequestIndex_dict[indexKey] = None
          except:
            logException("unexpected thisRequest_dict:[{}]".format(thisRequest_dict))
    
    # requests are populated!
    if len(thisRequest_list) > 0:
      apiName = None
      pt = "2x2"
      totalRequestNumber = len(thisRequest_list)
      requestCount = 0
      if len(thisRequest_list) >0:
        for thisReqeust_dict in thisRequest_list:
          requestCount += 1
          
          #for key in thisReqeust_dict.keys():
          #  logDebug("(#{}/{}) key:[{}]->[{}]".format(requestCount, totalRequestNumber, key, thisReqeust_dict[key]))
            
          if isinstance(thisReqeust_dict, dict) and "apiName" in thisReqeust_dict.keys():
            apiName = thisReqeust_dict["apiName"]
            pt = thisReqeust_dict["pt"]
            #break
      processNumer, threadNumber = getPxT(apiName, pt)
      
      targetRequestNumber = len(thisRequest_list)
      try:
        targetListChunkSize = int(targetRequestNumber / processNumer)
        
        if targetListChunkSize < 1:
          targetListChunkSize = 1
      except:
        logException("unable to determine the target chunk size with targetRequestNumber:[{}] and processNumer:[{}]".format(targetRequestNumber, processNumer))
        targetListChunkSize = cpu_count()
        targetRequestNumber = -1
        processNumer = 1
      
      
      if processNumer > 1:
        targetRequest_list = []
        targetRequest_list.append([])
        
        targetRequestCount = 0
        
        for targetRequest_dict in thisRequest_list:
          targetRequestCount += 1
          #logDebug("#{} {}".format(targetRequestCount, targetRequest_dict))
          try:
            targetRequest_dict["requestId"] = "{}_{}-{}".format(uuid4(), targetRequestNumber, targetRequestCount)
          except:
            logError("unable to add 'requestId' at targetRequest_dict:[{}]".format(targetRequest_dict))
            
          if targetRequestCount % targetListChunkSize == 0:
            #logInfo("targetRequest_list(len:{})->targetRequestCount:[{}]:[{}]".format(len(targetRequest_list), targetRequestCount, targetRequest_dict))
            targetRequest_list[-1].append(targetRequest_dict)
            targetRequest_list.append([])
          else:
            #logDebug("targetRequestCount:[{}]:[{}]".format(targetRequestCount, targetRequest_dict))
            targetRequest_list[-1].append(targetRequest_dict)
        
        try:
          # the targetRequest_dict must be copied through deepcopy. If not, 
          lastTargetRequest_dict = copy.deepcopy(targetRequest_dict)
          logDebug("===>type:{}:targetRequest_list[-1][-1]:[{}]".format(type(targetRequest_list), targetRequest_dict))
        except:
          lastTargetRequest_dict = None
          logDebug("===>type:{}:targetRequest_list:[{}]".format(type(targetRequest_list), targetRequest_list))
        
        poolResult_list = []
        try:
          gcWorker = GcWorker(user_dict, wbResult_dict)
          logDebug("'gcWorker' is created")
          p = Pool(processNumer)
          poolResult_list = p.map(gcWorker.get, targetRequest_list)
        except:
          errMsg = logException("unable to run gcWorker.get()")
          try:
            for targetRequestItems in targetRequest_list:
              logDebug("type:{}:targetRequestItems:[{}]".format(type(targetRequestItems), targetRequestItems))
              poolResult_list = gcWorker.get(targetRequestItems)
          except:  
            errMsg += logException("unable to run gcWorker.get()")
            poolResult_list = [[{"error":errMsg}]]
          
        thisWorkerResult_list = []
        if isinstance(poolResult_list, list) and len(poolResult_list) > 0 and isinstance(poolResult_list[0], list):
          for poolResultItem_list in poolResult_list:
            for thisResultItem_dict in poolResultItem_list:
              thisWorkerResult_list.append(thisResultItem_dict)
        else:
          thisWorkerResult_list = poolResult_list
        #logDebug("#thisWorkerResult_list(len:{})".format(len(thisWorkerResult_list)))
        
      #if processNumer > 1:
      else:
        try:
          gcWorker = GcWorker(user_dict, wbResult_dict)
          
          if threadNumber > 1:
            thisWorkerResult_list = gcWorker.get(thisRequest_list)
          else:
            thisWorkerResult_list = []
            for request_dict in thisRequest_list:
              thisResult_list = gcWorker.run(request_dict)
              if isinstance(thisResult_list, list):
                for thisResultItem_dict in thisResult_list:
                  thisWorkerResult_list.append(thisResultItem_dict)
              else:
                thisWorkerResult_list.append(thisResult_list)
          
          if len(thisRequest_list) > 0:
            lastTargetRequest_dict = thisRequest_list[-1]
            
        except Exception as e:
          errMsg = logException("unable to run gcWorker.run()->Error:[{}]".format(e))
          thisWorkerResult_list.append({"error":errMsg})
          lastTargetRequest_dict = None
          
      #end if processNumer > 1:
    else:
      try:
        thisWorkerResult_list = [
            {
              "apiName_": thisRequests_dict[apiCount][-1]["apiName"],
              "error":"no request",
              "requestCount": 0,
              "resultCount": -1,
              "lastRequest": "{}".format(thisRequests_dict[apiCount])
              }
            ]
      except:
        thisWorkerResult_list = [
            {
              "error":"no request",
              "requestCount": 0,
              "resultCount": -1,
              "lastRequest": "{}".format(thisRequests_dict[apiCount])
              }
            ]
        
    #if len(thisRequest_list) > 0:
     
    try:
      if isinstance(thisWorkerResult_list, list) and len(thisWorkerResult_list) == 0:
        try:
          thisWorkerResult_list = [
            {
              "apiName_": lastTargetRequest_dict["apiName"],
              "accountId_": lastTargetRequest_dict["accountId"],
              "regionCode_": lastTargetRequest_dict["regionCode"],
              "error":"no data",
              "requestCount": targetRequestNumber,
              "resultCount": len(thisWorkerResult_list),
              "lastRequest": "{}".format(lastTargetRequest_dict)
              }
            ]
        except:
          thisWorkerResult_list = [
            {
              "error":"no data",
              "requestCount": targetRequestNumber,
              "resultCount": len(thisWorkerResult_list),
              "lastRequest": "{}".format(lastTargetRequest_dict)
              }
            ]
      #else:
      # for thisWorkerResultItem_dict in thisWorkerResult_list:
      #    logDebug("=====>#thisWorkerResult_list(len:{:,}):[-1]:[{}]".format(len(thisWorkerResult_list), thisWorkerResultItem_dict))
        
    except Exception as e:
      logException("unable to determine the type of the result:[{}]-->Error:[{}]".format(thisWorkerResult_list, "{}".format(e)))                                                                                      
    
    totalRequestNumber = len(thisWorkerResult_list)
    if totalRequestNumber > 10:
      percentageDelimiter = int(totalRequestNumber/3) -1
    else:
      percentageDelimiter = 1
    if totalRequestNumber > 0:
      requestCount = 0
      for thisResultItem_dict in thisWorkerResult_list:
        indexKey = None
        if isinstance(thisResultItem_dict, dict) and "apiName_" in thisResultItem_dict.keys():
          try:
            if "serviceName_" in thisResultItem_dict.keys():
              indexKey = "{}:{}.{}".format(apiCount, thisResultItem_dict["serviceName_"], thisResultItem_dict["apiName_"])
            else:
              indexKey = "{}:{}".format(apiCount, thisResultItem_dict["apiName_"])
          except:
            indexKey = "{}:{}".format(apiCount, apiName)
            logException("unable to set indexKey with thisResultItem_dict:[{}]->indexKey:[{}]".format(thisResultItem_dict, indexKey))
        elif isinstance(thisResultItem_dict, dict) and "apiName" in thisResultItem_dict.keys():
          try:
            if "serviceName_" in thisResultItem_dict.keys():
              indexKey = "{}:{}.{}".format(apiCount, thisResultItem_dict["serviceName_"], thisResultItem_dict["apiName"])
            else:
              indexKey = "{}:{}".format(apiCount, thisResultItem_dict["apiName"])
          except:
            indexKey = "{}:{}".format(apiCount, apiName)
            logException("unable to set indexKey with thisResultItem_dict:[{}]->indexKey:[{}]".format(thisResultItem_dict, indexKey)) 
        elif apiName != None:
          indexKey = "{}:{}".format(apiCount, apiName)
        else:
          logWarn("'apiName' is not found at thisResultItem_dict:{}:[{}]".format(apiCount, thisResultItem_dict))
          continue
        
        requestCount += 1
        if (totalRequestNumber % percentageDelimiter) == 0:
          logDebug("(#{:,}/{:,})\tindexKey:[{}]->thisResultItem_dict:[{}]".format(requestCount, totalRequestNumber, indexKey, thisResultItem_dict))
        
        if indexKey in wbResult_dict.keys():
          wbResult_dict[indexKey].append(thisResultItem_dict)
        elif indexKey != None:
          wbResult_dict[indexKey] = [thisResultItem_dict]
    else:
      if apiName in [None, "None"]:
        pass
      else:
        indexKey = "{}:{}".format(apiCount, apiName)
        wbResult_dict[indexKey] = [{"error":"<-- no data -->"}]
  
  toBeDeletedIndexKey_list = []
  for indexKey in wbResult_dict.keys():
    if "nosave" in indexKey:
      toBeDeletedIndexKey_list.append(indexKey)
      
  for indexKey in toBeDeletedIndexKey_list:
    del wbResult_dict[indexKey]
  
  apiNameMapping_dict = {}
  for indexKey in wbResult_dict.keys():
    try:
      apiName = indexKey.split(":")[-1]
    except:
      logException("unable to get apiName from the indexKey:[{}]".format(indexKey))
      continue
    
    if apiName in apiNameMapping_dict.keys():
      for result_dict in wbResult_dict[indexKey]:
        apiNameMapping_dict[apiName].append(result_dict)
    else:
      apiNameMapping_dict[apiName] = wbResult_dict[indexKey]
      
  #logDebug("#indexKeys:[{}]".format(apiNameMapping_dict.keys()))
  return apiNameMapping_dict

def getPxT(apiName, pt):
  processNumer = 2
  threadNumber = 2
  
  if apiName not in ["profile", "analyze", "discoverResources", "discoverRegions"]:
    try:
      if pt.strip() != "":
        pt_list = pt.strip().split("x")
        if len(pt_list) >= 2:
          processNumer = int(pt_list[0])
          threadNumber = int(pt_list[1])
        elif len(pt_list) == 1:
          processNumer = int(pt_list[0])
          threadNumber = 2
        else:
          processNumer = 2
          threadNumber = 12
        logDebug("===>{}:processNumer:{}:threadNumber:[{}]".format(pt_list, processNumer, threadNumber))
      else:
        processNumer = 2
        threadNumber = 12
        
    except:
      logException("unable to set 'pt' with apiName[{}]->pt:[{}]".format(apiName, pt))
    
      processNumer = 2
      threadNumber = 12
    
    if processNumer > cpu_count()*2:
      processNumer = cpu_count()*2
  else:
    processNumer = 1
    threadNumber = cpu_count()
    
  try:
    if "describeResource" in apiName and processNumer > 2:
      processNumer =  2
  except Exception as e:
    logException("unable to determine the processNumber with apiName:[{}".format(apiName))
    
  return processNumer, threadNumber
