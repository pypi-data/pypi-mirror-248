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


from pathway import requests
from pathway import updateMsg

from tammy.midway import PdxMidway

from wooju.args import getTTL_s

from graphcode.io2.putItem import putItemRequest
from graphcode.io2.getItem import getItemRequest
from graphcode.io2.deleteItem import deleteItemRequest

from getpass import getuser
import time

import json

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
  
  ttl_s = 900#getTTL_s(request_dict)
  
  if ttl_s < 0:
    midwayCookieStatus_dict = updateMidwayCookieStatus(request_dict, errorReason_list, logMessage_list)
    saveMidwayCookieStatus_dict(request_dict, midwayCookieStatus_dict, ttl_s=abs(ttl_s))
  
  elif ttl_s == 0:
    midwayCookieStatus_dict = updateMidwayCookieStatus(request_dict, errorReason_list, logMessage_list)
    deleteMidwayCookieStatus_dict(request_dict)
  
  else:
    try:
      midwayCookieStatus_dict = loadMidwayCookieStatus_dict(request_dict)
      isValidMidway = False
      midWayStatus_list = []
      for partition in midwayCookieStatus_dict.keys():
        #logDebug("#{}".format(partition))
        if "badge" in midwayCookieStatus_dict[partition].keys():
          if "{}_n/a".format(partition) not in [midwayCookieStatus_dict[partition]["badge"]] \
              and "expired {}".format(partition) not in [midwayCookieStatus_dict[partition]["badge"]]:
            isValidMidway = True
          else:
            midWayStatus_list.append(midwayCookieStatus_dict[partition]["badge"])
          
        #for key in midwayCookieStatus_dict[partition].keys():
        #  logDebug("{}.{}:[{}]".format(partition, key, midwayCookieStatus_dict[partition][key]))
      
      if isValidMidway == False:
        raiseValueError("invalid midwayStatus:[{}]".format(midWayStatus_list))
        
    except:
      midwayCookieStatus_dict = updateMidwayCookieStatus(request_dict, errorReason_list, logMessage_list)
      saveMidwayCookieStatus_dict(request_dict, midwayCookieStatus_dict, ttl_s=900)
      
  return {
    **midwayCookieStatus_dict,
    "midway":[midwayCookieStatus_dict],
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
  
def saveMidwayCookieStatus_dict(request_dict, midwayCookieStatus_dict, ttl_s=900):
  tableName = "midway"
  prefix = request_dict["metadata"]["userName"]
  
  isValidMidway = False
  midWayStatus_list = []
      
  for partition in midwayCookieStatus_dict.keys():
    
    midwayCookieStatus_dict[partition]["localUser"] = getuser()

    if "badge" in midwayCookieStatus_dict[partition].keys():
      if "{}_n/a" not in [midwayCookieStatus_dict[partition]["badge"]] \
          and "expired {}".format(partition) not in [midwayCookieStatus_dict[partition]["badge"]]:
        isValidMidway = True
      else:
        midWayStatus_list.append(midwayCookieStatus_dict[partition]["badge"])
        
    if "expirationTime" in midwayCookieStatus_dict[partition].keys():
      remainingTTLs = (midwayCookieStatus_dict[partition]["expirationTime"] - time.time())
      if remainingTTLs < ttl_s:
        logWarn("midwayCookieStatus is not stored in cache due to remainingTTL:[{:.2f}]s is short or expired".format(remainingTTLs))
        
        try:
          deleteMidwayCookieStatus_dict(request_dict)
        except:
          logException("trying to delete midwayCookieStatus in cache")
        
        return midwayCookieStatus_dict
    
  #logDebug("#local midwayCookie cache will be expired in [{:,.2f}]s".format((time.time() + ttl_s)-time.time()))
  
  if isValidMidway == False:
    logError("invalid midwayStatus:[{}]".format(midWayStatus_list))
    
    try:
      deleteMidwayCookieStatus_dict(request_dict)
    except:
      logException("trying to delete midwayCookieStatus in cache")
      
    return midwayCookieStatus_dict
  
  putItemRequest(
    request_dict={
      "attributes":{
        "table": tableName,
        "prefix": prefix,
        "key": "midwayCookieStatus_dict",
        "data": midwayCookieStatus_dict,
        "ttl_s": ttl_s
        }
      }
    )
    
  return midwayCookieStatus_dict
    
def loadMidwayCookieStatus_dict(request_dict):
  tableName = "midway"
  prefix = request_dict["metadata"]["userName"]
  
  midwayCookieStatus_dict = getItemRequest(
  request_dict={
    "attributes":{
      "table": tableName,
      "prefix": prefix,
      "key": "midwayCookieStatus_dict"
      }
    }
  )
  #logDebug("#{}:aeaStatus_dict:[{}]".format(type(aeaStatus_dict).__name__, aeaStatus_dict))
  if "status_code" in midwayCookieStatus_dict.keys() and midwayCookieStatus_dict["status_code"] != 200:
    raiseValueError("unexpected midwayCookieStatus_dict:[{}]".format(midwayCookieStatus_dict))
    
  return midwayCookieStatus_dict


def deleteMidwayCookieStatus_dict(request_dict):
  tableName = "midway"
  prefix = request_dict["metadata"]["userName"]
  
  response_dict = deleteItemRequest(
    request_dict={
      "attributes":{
        "table": tableName,
        "prefix": prefix,
        "key": "midwayCookieStatus_dict"
        }
      }
    )
    
  return response_dict
    
def updateMidwayCookieStatus(request_dict, errorReason_list, logMessage_list):
  
  try:
    pdxMidway = PdxMidway(
      userAccountId= request_dict["metadata"]["awsAccountId"], 
      loginAliasId= request_dict["metadata"]["userName"]
      )
    
    thisMidwayCookie = pdxMidway.loadLocalMidwayCookie()
    
    try:
      #logDebug("midwayCookie(len:{:,}):\n{}\n".format(len(midwayCookie), midwayCookie))
      logDebug("midwayCookie(len:{:,})".format(len(thisMidwayCookie)))
    except:
      logDebug("midwayCookie:[{}]".format(thisMidwayCookie))
      
    midwayCookie_dict = pdxMidway.getMidwayCookie(midwayCookie=thisMidwayCookie)
    for partition in midwayCookie_dict.keys():
      logDebug("partition:[{}]".format(partition))
      if len(midwayCookie_dict[partition].keys()) > 0 and "sessionId" in midwayCookie_dict[partition].keys() and len(midwayCookie_dict[partition]["sessionId"]) > 256:
        logDebug("midway loaded:[{}]".format(partition))
        for key in set(midwayCookie_dict[partition].keys()):
          if key in ["aea", "sessionId"]:
            midwayCookie_dict[partition][key] = len(midwayCookie_dict[partition][key])
          elif key in ["expirationTime"]:
            ttl_h = (midwayCookie_dict[partition][key] - time.time())/60/60
            if ttl_h > 3:
              midwayCookie_dict[partition]["badgeColor"] = "badge-success"
            
            elif ttl_h > 0.1:
              midwayCookie_dict[partition]["badgeColor"] = "badge-warning"
                
            else:
              midwayCookie_dict[partition]["badgeColor"] = "badge-danger"
              
            midwayCookie_dict[partition]["TTL_h"] = float("{:.2f}".format((ttl_h)))
            
            
        midwayCookie_dict[partition]["badge"] = "{}_{:.1f}h".format(partition[0], ttl_h)
        
        if ttl_h > 0:
          result_dict = requests(
            request_dict = {
                **request_dict,
                "apiName":"tammy.midway.describeAEA"
              }
            )
          logDebug("describeAEA:[{}]".format(result_dict))
          aeaStatus_dict = {}
          for aeaResultItem_dict in result_dict["response"]["aeaStatus"]:
            aeaStatus_dict[aeaResultItem_dict["partition"]] = aeaResultItem_dict
            
          try:
            midwayCookie_dict[partition]["aeaOptedStatus"] = aeaStatus_dict[partition]
            try:
              if midwayCookie_dict[partition]["aeaOptedStatus"]["opted_out"] == False:
                if midwayCookie_dict[partition]["badgeColor"]  in ["badge-warning", "badge-danger"]:
                  midwayCookie_dict[partition]["badgeColor"] = "badge-info"
                else:
                  midwayCookie_dict[partition]["badgeColor"] = "badge-success"
              else:
                midwayCookie_dict[partition]["badgeColor"] = "badge-primary"
                
            except Exception as e:
              midwayCookie_dict[partition]["badgeColor"] = "badge-secondary"
              midwayCookie_dict[partition]["aeaOptedStatus"] = {"opted_out":"n/a"}
            
            logDebug("aeaOptedOut:[{}]".format(midwayCookie_dict[partition]["aeaOptedStatus"]["opted_out"]))
          
          except Exception as e:
            midwayCookie_dict[partition]["badgeColor"] = "badge-dark"
            midwayCookie_dict[partition]["aeaOptedStatus"] = {"opted_out":"n/a"}
            
            logDebug("aeaOptedOut:[{}]".format(midwayCookie_dict[partition]["aeaOptedStatus"]["opted_out"]))
              
        else:
          midwayCookie_dict[partition]["badgeColor"] = "badge-secondary"
          midwayCookie_dict[partition]["aeaOptedStatus"] = {"opted_out":"n/a"}
          logDebug("aeaOptedOut:[{}]".format(midwayCookie_dict[partition]["aeaOptedStatus"]["opted_out"]))
      
      else:
        #logDebug("#no midway loaded:[{}]".format(partition))
        
        midwayCookie_dict[partition]["badgeColor"] = "badge-dark"
        midwayCookie_dict[partition]["badge"] = "{}_n/a".format(partition)
        midwayCookie_dict[partition]["user"] = "n/a"
        midwayCookie_dict[partition]["aea"] = "n/a"
        midwayCookie_dict[partition]["sessionId"] = "n/a"
        midwayCookie_dict[partition]["TTL_h"] = "n/a"
        midwayCookie_dict[partition]["aeaOptedStatus"] = {"opted_out":"n/a"}
    
  except Exception as e:
    updateMsg(errorReason_list, logException("unexpected request_dict:[{}]".format(request_dict)))
    try:
      midwayCookieError_dict = json.loads("{}".format(e))
      logWarn("{}:midwayCookie_dict:[{}]".format(type(midwayCookieError_dict).__name__, midwayCookieError_dict))
    except:
      logException("failed to load midwayCookie_dict")
      midwayCookieError_dict = {}
      
    midwayCookie_dict = {}
    for partition in ["global","cn"]:
      midwayCookie_dict[partition] = {}
      if partition in midwayCookieError_dict.keys(): 
        midwayCookie_dict[partition]["badgeColor"] = "badge-danger"
        midwayCookie_dict[partition]["badge"] = "expired {}".format(partition)
        midwayCookie_dict[partition]["sessionId"] = midwayCookieError_dict[partition]
      else:
        midwayCookie_dict[partition]["badgeColor"] = "badge-secondary"
        midwayCookie_dict[partition]["badge"] = "{}_n/a".format(partition)
        midwayCookie_dict[partition]["sessionId"] = "n/a"
    
      midwayCookie_dict[partition]["user"] = "n/a"
      midwayCookie_dict[partition]["aea"] = "n/a"
      midwayCookie_dict[partition]["TTL_h"] = "n/a"
      midwayCookie_dict[partition]["aeaOptedStatus"] = {"opted_out":"n/a"}
      
  return midwayCookie_dict
