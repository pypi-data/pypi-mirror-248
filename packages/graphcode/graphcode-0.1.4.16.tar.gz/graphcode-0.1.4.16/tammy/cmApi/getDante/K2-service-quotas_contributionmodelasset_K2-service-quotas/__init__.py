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

from pathway import updateMsg
from moduApi.inputFilters import getInputs, getAccountId, getRegionCode, getApiName, getArguments, getPrimaryKeys, getDanteScriptId

from tammy.dante import Dante

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
  
  dantePayload_dict = {
    "executionType":"ASYNCHRONOUS",
    "script":{"id":"K2-service-quotas_contributionmodelasset_K2-service-quotas","tenantId":"aws"},
    "scriptInput":{
      "region":"eu-west-1",
      "accountIds":"000000000000"
      }
    }
  
  dante = Dante(
    userAccountId = request_dict["metadata"]["awsAccountId"], 
    loginAliasId = request_dict["metadata"]["userName"]
    )
  try:
    danteResult_dict = dante.get(payload_dict=dantePayload_dict)
  except:
    updateMsg(errorReason_list, logException("failed to request dante payload_dict:[{}]".format(dantePayload_dict)))
    danteResult_dict = {}
  
  if "response" in danteResult_dict.keys():
    
    for key in danteResult_dict["response"].keys():
      if isinstance(danteResult_dict["response"][key], list):
        if len(danteResult_dict["response"][key]) > 0:
          logDebug("{}(len:{:,})[-1]:[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key][-1]))
        else:
          logDebug("{}(len:{:,}):[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key]))
          
      else:
        logWarn("unexpected {}:{}:[{}]".format(type(danteResult_dict["response"][key]).__name__, key, danteResult_dict["response"][key]))
      
    if len(danteResult_dict["response"].keys()) > 0:
      logDebug("danteResult_dict.keys(len:{:,})]:[{}]".format(len(danteResult_dict["response"].keys()), danteResult_dict["response"].keys()))
    else:
      logDebug("danteResult_dict.keys(len:{:,})]:[{}]".format(len(danteResult_dict["response"].keys()), danteResult_dict["response"].keys()))
     
    return {
      **danteResult_dict["response"],
      "logMessages": logMessage_list,
      "errorReasons": errorReason_list
      }
  
  else:
    return {
      **danteResult_dict,
      "logMessages": logMessage_list,
      "errorReasons": errorReason_list
      }
    
