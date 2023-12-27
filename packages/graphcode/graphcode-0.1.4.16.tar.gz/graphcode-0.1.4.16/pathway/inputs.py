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

def getAsValueMap_dict(request_dict):
  if "inputs" in request_dict.keys():
    # k2 format
    if "asValues" in request_dict["inputs"].keys():
      asValues = request_dict["inputs"]["asValues"]
    # boto3 format
    elif "asValues" in request_dict["inputs"].keys():
      asValues = request_dict["inputs"]["asValues"]
    else:
      #self.__putErrorMessage__("'serviceName' or 'ServiceName' is not found at inputs:[{}]".format(request_dict["inputs"]))
      asValues = None
  elif "asValues" in request_dict.keys():
    asValues = request_dict["asValues"]
  elif "AsValues" in request_dict.keys():
    asValues = request_dict["AsValues"]
  else:
    asValues = None
  #logDebug("#asValues:[{}]".format(asValues)) 
  
  asValueMap_dict = {}
  if asValues != None:
    for asValueItemMap in asValues.split(","):
      asValueItemMap_list = asValueItemMap.split(":")
      if len(asValueItemMap_list) >= 2:
        asValueMap_dict[asValueItemMap_list[0].strip()] = asValueItemMap_list[-1].strip()
  #logDebug("#asValueMap_dict:[{}]".format(asValueMap_dict)) 
  
  return asValueMap_dict

def getTagetValueMap_dict(request_dict):
  if "inputs" in request_dict.keys():
    # k2 format
    if "targetValues" in request_dict["inputs"].keys():
      targetValues = request_dict["inputs"]["targetValues"]
    # boto3 format
    elif "TargetValues" in request_dict["inputs"].keys():
      targetValues = request_dict["inputs"]["TargetValues"]
    else:
      #self.__putErrorMessage__("'serviceName' or 'ServiceName' is not found at inputs:[{}]".format(request_dict["inputs"]))
      targetValues = None
  elif "targetValues" in request_dict.keys():
    targetValues = request_dict["targetValues"]
  elif "TargetValues" in request_dict.keys():
    targetValues = request_dict["TargetValues"]
  else:
    targetValues = None
  logDebug("targetValues:[{}]".format(targetValues)) 
  
  targetValueMap_dict = {}
  if targetValues != None:
    for targetValueItemMap in targetValues.split(","):
      targetValueItemMap_list = targetValueItemMap.split(":")
      if len(targetValueItemMap_list) >= 2:
        targetValueMap_dict[targetValueItemMap_list[0].strip()] = targetValueItemMap_list[-1].strip()
  logDebug("targetValueMap_dict:[{}]".format(targetValueMap_dict)) 
  
  return targetValueMap_dict

def getTagetColumnMap_dict(request_dict):
  if "inputs" in request_dict.keys():
    # k2 format
    if "targetColumns" in request_dict["inputs"].keys():
      targetColumns = request_dict["inputs"]["targetColumns"]
    # boto3 format
    elif "TargetColumns" in request_dict["inputs"].keys():
      targetColumns = request_dict["inputs"]["TargetColumns"]
    else:
      #self.__putErrorMessage__("'serviceName' or 'ServiceName' is not found at inputs:[{}]".format(request_dict["inputs"]))
      targetColumns = None
  elif "targetColumns" in request_dict.keys():
    targetColumns = request_dict["targetColumns"]
  elif "TargetColumns" in request_dict.keys():
    targetColumns = request_dict["TargetColumns"]
  else:
    targetColumns = None
  #logDebug("#targetColumns:[{}]".format(targetColumns)) 
  
  targetColumnMap_dict = {}
  if targetColumns != None:
    for targetColumnItemMap in targetColumns.split(","):
      targetColumnItemMap_list = targetColumnItemMap.split(":")
      if len(targetColumnItemMap_list) >= 2:
        targetColumnMap_dict[targetColumnItemMap_list[0].strip()] = targetColumnItemMap_list[-1].strip()
  #logDebug("#targetColumnMap_dict:[{}]".format(targetColumnMap_dict)) 
  
  return targetColumnMap_dict

def getJoinValueMap_dict(request_dict):
  if "inputs" in request_dict.keys():
    # k2 format
    if "joinValues" in request_dict["inputs"].keys():
      joinValues = request_dict["inputs"]["joinValues"]
    # boto3 format
    elif "JoinValues" in request_dict["inputs"].keys():
      joinValues = request_dict["inputs"]["JoinValues"]
    else:
      #self.__putErrorMessage__("'serviceName' or 'ServiceName' is not found at inputs:[{}]".format(request_dict["inputs"]))
      joinValues = None
  elif "joinValues" in request_dict.keys():
    joinValues = request_dict["joinValues"]
  elif "JoinValues" in request_dict.keys():
    joinValues = request_dict["JoinValues"]
  else:
    joinValues = None
  #logDebug("#joinValues:[{}]".format(joinValues)) 
  
  joinValueMap_dict = {}
  if joinValues != None:
    for joinValueItemMap in joinValues.split(","):
      joinValueItemMap_list = joinValueItemMap.split(":")
      if len(joinValueItemMap_list) >= 2:
        joinValueMap_dict[joinValueItemMap_list[0].strip()] = joinValueItemMap_list[-1].strip()
  #logDebug("#joinValueMap_dict:[{}]".format(joinValueMap_dict)) 
  
  return joinValueMap_dict

def getIndexKeyMap_dict(request_dict):
  if "inputs" in request_dict.keys():
    # k2 format
    if "indexKeys" in request_dict["inputs"].keys():
      indexKeys = request_dict["inputs"]["indexKeys"]
    # boto3 format
    elif "indexKeys" in request_dict["inputs"].keys():
      indexKeys = request_dict["inputs"]["indexKeys"]
    else:
      #self.__putErrorMessage__("'serviceName' or 'ServiceName' is not found at inputs:[{}]".format(request_dict["inputs"]))
      indexKeys = None
  elif "indexKeys" in request_dict.keys():
    indexKeys = request_dict["indexKeys"]
  elif "IndexKeys" in request_dict.keys():
    indexKeys = request_dict["IndexKeys"]
  else:
    indexKeys = None
  #logDebug("#indexKeys:[{}]".format(indexKeys)) 
  
  indexMap_dict = {}
  if indexKeys != None:
    for indexMap in indexKeys.split(","):
      indexMap_list = indexMap.split(":")
      if len(indexMap_list) >= 2:
        indexMap_dict[indexMap_list[0].strip()] = indexMap_list[-1].strip()
  #logDebug("#indexMap_dict:[{}]".format(indexMap_dict)) 
  
  return indexMap_dict

def getApiNameToBeCombined(request_dict):
  
  return getValueFromRequest(keyword="combineWith", request_dict = request_dict) 

def getSourceApiName(request_dict):
  
  return getValueFromRequest(keyword="sourceApiName", request_dict = request_dict) 

def getApiNameToBeJoined(request_dict):
  
  return getValueFromRequest(keyword="joinWith", request_dict = request_dict) 

def getAccountId(request_dict):
  
  return getValueFromRequest(keyword="accountId", request_dict = request_dict) 


def getAccountIds(request_dict):
  accountId_list = []
  
  accountId = getAccountId(request_dict)
  
  if isinstance(accountId, str):
    for thisAccountId in accountId.strip().split(","):
      if thisAccountId not in accountId_list:
        accountId_list.append(thisAccountId)
  else:
    logWarn("unexpected tyep:{}:accountId:[{}]".format(type(accountId), accountId))
  logDebug("accountId_list:[{}]".format(accountId_list))
    
  accountIds = getValueFromRequest(keyword="accountIds", request_dict = request_dict) 
  logDebug("accountIds:[{}]".format(accountIds)) 
  
  if isinstance(accountIds, str):
    for thisAccountId in accountIds.strip().split(","):
      if thisAccountId not in accountId_list:
        accountId_list.append("{}".format(thisAccountId).zfill(12))
  elif isinstance(accountIds, list):
    for thisAccountId in accountIds:
      if thisAccountId not in accountId_list:
        accountId_list.append("{}".format(thisAccountId).zfill(12))
  elif isinstance(accountIds, dict):
    for thisAccountId in accountIds.keys():
      if thisAccountId not in accountId_list:
        accountId_list.append("{}".format(thisAccountId).zfill(12))
  else:
    logWarn("unexpected tyep:{}:accontIds:[{}]".format(type(accountIds), accountIds))
  
  return accountId_list

def getRegionCode(request_dict):
  
  return getValueFromRequest(keyword="regionCode", request_dict = request_dict)  

def getRegionCodes(request_dict):
  regionCode_list = []
  
  regionCode = getRegionCode(request_dict)
  if regionCode != None:
    for thisServiceName in regionCode.strip().split(","):
      if thisServiceName not in regionCode_list and len(thisServiceName) >= 3:
        regionCode_list.append(thisServiceName)
  logDebug("regionCode_list:[{}]".format(regionCode_list))
  
  regionCodes = getValueFromRequest(keyword="regionCodes", request_dict = request_dict)  
  logDebug("regionCodes:[{}]".format(regionCodes)) 
  
  if isinstance(regionCodes, str):
    for thisRegionCode in regionCodes.strip().split(","):
      if thisRegionCode not in regionCode_list:
        regionCode_list.append(thisRegionCode)
  elif isinstance(regionCodes, list):
    for thisRegionCode in regionCodes:
      if thisRegionCode not in regionCode_list:
        regionCode_list.append(thisRegionCode)
      
  return regionCode_list


def getServiceName(request_dict):
  
  return getValueFromRequest(keyword="serviceName", request_dict = request_dict)  

def getServiceNameV2(action, request_dict):
  serviceName = getValueFromRequest(keyword="serviceName", request_dict=request_dict)
  if serviceName == None and "inputs" in request_dict.keys():
    serviceName = getValueFromRequest(keyword="serviceName", request_dict=request_dict["inputs"])
    
  if serviceName == None and action != None:
    serviceName = action
  
  if serviceName == None:
    raiseValueError("unexpected action:[{}] or request_dict:[{}]".format(action, request_dict))
  else:
    logDebug("serviceName:[{}]".format(serviceName))
    
  return serviceName
  
def getServiceNames(request_dict):
  serviceName_list = []
  
  serviceName = getServiceName(request_dict)
  if serviceName != None:
    for thisServiceName in serviceName.strip().split(","):
      if thisServiceName not in serviceName_list and len(thisServiceName) >= 3:
        serviceName_list.append(thisServiceName)
  logDebug("serviceName_list:[{}]".format(serviceName_list))
  
  serviceNames = getValueFromRequest(keyword="serviceNames", request_dict = request_dict)  
  logDebug("serviceNames:[{}]".format(serviceNames)) 
  
  if serviceNames != None and len(serviceNames.strip()) >= 3:
    for serviceName in serviceNames.strip().split(","):
      if serviceName not in serviceName_list:
        serviceName_list.append(serviceName)
      
  return serviceName_list

def getProfileName(request_dict):
  
  return getValueFromRequest(keyword="profileName", request_dict = request_dict)   

def getProfileNames(request_dict):
  profileName_list = []
  
  profileName = getProfileName(request_dict)
  if profileName != None:
    for thisprofileName in profileName.strip().split(","):
      if thisprofileName not in profileName_list and len(thisprofileName) >= 3:
        profileName_list.append(thisprofileName)
  logDebug("profileName_list:[{}]".format(profileName_list))
  
  profileNames = getValueFromRequest(keyword="profileNames", request_dict = request_dict)  
  logDebug("profileNames:[{}]".format(profileNames)) 
  
  if profileNames != None and len(profileNames.strip()) >= 3:
    for profileName in profileNames.strip().split(","):
      if profileName not in profileName_list:
        profileName_list.append(profileName)
      
  return profileName_list

def getSourceMedia(request_dict):
  
  return getValueFromRequest(keyword="sourceMedia", request_dict = request_dict) 

def getQuery(request_dict):
  
  return getValueFromRequest(keyword="query", request_dict = request_dict) 


def getUrl(request_dict):
  
  return getValueFromRequest(keyword="url", request_dict = request_dict)  
