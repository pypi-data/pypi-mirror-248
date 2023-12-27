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

import time

import json

from tammy.midway import loadAEACache_dict, saveAEACache_dict

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
  
  pdxMidway = PdxMidway(
    userAccountId= request_dict["metadata"]["awsAccountId"], 
    loginAliasId= request_dict["metadata"]["userName"]
    )
  
  aeaStatus_dict = {}
  midwayCookie_dict = pdxMidway.getMidwayCookie(midwayCookie=pdxMidway.loadLocalMidwayCookie())
  for partition in midwayCookie_dict.keys():
    #logDebug("#{}:midwayCookie_dict[{}]:[{}]".format(type(midwayCookie_dict[partition]).__name__, partition, midwayCookie_dict[partition]))
    aeaStatus_dict[partition] = {}
    try:
      if len(midwayCookie_dict[partition].keys()) > 0 and "sessionId" in midwayCookie_dict[partition].keys() and len(midwayCookie_dict[partition]["sessionId"]) > 256:
        try:
          if (midwayCookie_dict[partition]["expirationTime"] -  - time.time()) > 0:
            r = pdxMidway.sessionRequest("https://aga.aka.amazon.com/api/get-aea-auth-user?user_name={}".format(request_dict["metadata"]["userName"]))
            try:
              aeaStatus_dict[partition] = r.json()["user_data"]
              
              if partition in ["global"]:
                regionCode = "us-east-1"
              else:
                regionCode = "cn-north-1"
                
              result_dict = requests(
                request_dict = {
                    **request_dict,
                    "attributes":{
                      "accountId": request_dict["metadata"]["awsAccountId"],
                      "apiName": "awsadms.getAccountIdentifiersByAccountId",
                      "regionCode": regionCode,
                      "arguments": {"accountId":request_dict["metadata"]["awsAccountId"]},
                      "primaryKeys":""
                      },
                    "apiName":"tammy.k2.getK2"
                  }
                )
              
              try:
                if len(result_dict["response"]["k2Results"]) == 1 and "AccountIdType" in result_dict["response"]["k2Results"][-1].keys():
                  pass#logDebug("no further action for AEA")
                else:
                  try:
                    result_dict["response"]["k2Results"][-1]["errorReasons"] = "unexpected response"
                  except:
                    logException("unexpected k2results")
                  raiseValueError("unexpected k2Results:[{}]".format(result_dict["response"]))  
                  
              except:
                  
                for key in aeaStatus_dict[partition].keys():
                  logDebug("aeaStatus_dict[{}.{}]:[{}]".format(partition, key, aeaStatus_dict[partition][key]))
                  
                  if key in ["opted_out"] and aeaStatus_dict[partition]["opted_out"] == False:
                    if pdxMidway.runAeaOptedOut({}):
                      r = pdxMidway.sessionRequest("https://aga.aka.amazon.com/api/get-aea-auth-user?user_name={}".format(request_dict["metadata"]["userName"]))
                      aeaStatus_dict[partition] = r.json()["user_data"]
                      
                      for key2 in aeaStatus_dict[partition].keys():
                        logDebug("aeaStatus_dict[{}.{}]:[{}]".format(partition, key2, aeaStatus_dict[partition][key2]))
                        if key2 in ["updated_at", "created_at"]:
                          aeaStatus_dict[partition]["age_d"] = int(aeaStatus_dict[partition][key2])
                          
                      aeaStatus_dict[partition]["age_d"] = float("{:.2f}".format((aeaStatus_dict[partition]["updated_at"] - time.time())/3600/24))
                  
                  elif key in ["updated_at", "created_at"]:
                    aeaStatus_dict[partition]["age_d"] = int(aeaStatus_dict[partition][key])
                  
            except Exception as e:
              try:
                updateMsg(errorReason_list, logError("unexpected aeaOptedOut:[{}] in '{}' partition-->Error:[{}]".format(r.context.decode(), partition, e)))
                
              except:
                logError("aeaOptedOut:[{}]".format(r))
              
          
          else:
            updateMsg(logMessage_list, logError("failed to aeaOptedOut in '{}' partition".format(partition)))
        
        except:
          updateMsg(errorReason_list, logException("unexpected error during aeaOptedOut in '{}' partition".format(partition)))
      
      else:
        pass#updateMsg(logMessage_list, logError("invalid or no midway in '{}' partition".format(partition)))
    except:
      logException("{}:midwayCookie_dict[{}]:[{}]".format(type(midwayCookie_dict[partition]).__name__, partition, midwayCookie_dict[partition]))
      time.sleep(10)
                   
  
  #saveAEACache_dict(request_dict, aeaStatus_dict)
    
  aeaStatus_list = []
  for partition in aeaStatus_dict.keys():
    if isinstance(aeaStatus_dict[partition], dict):
      aeaStatus_list.append(
        {
          "partition":partition,
          **aeaStatus_dict[partition]
          }
        )
    else:
      aeaStatus_list.append(
        {
          "{}".format(partition): aeaStatus_dict[partition]
          }
        )
    
  return {
    "aeaStatus": aeaStatus_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
