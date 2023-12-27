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

from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from pathway import updateMsg
from moduApi.profile import loadAccountDetails
from moduApi.metric import loadMetrics, loadUsageMetrics, loadServiceMetrics
from moduApi.inputFilters import getInputs, getAccountId, getRegionCode, getApiName, getArguments, getPrimaryKeys, getDanteScriptId

from codex.midwayCookieHandler import loadLocalMidwayCookie

from uuid import uuid4

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
    "script":{
      "id":"K2-ec2_contributionmodelasset_Dante-curated-ec2",
      "tenantId":"aws"
      }, 
    "scriptInput":{
      "region":["eu-north-1","me-south-1","ap-south-1","eu-west-3","ap-southeast-3","us-east-2","af-south-1","eu-west-1","me-central-1","eu-central-1","sa-east-1","ap-east-1","ap-south-2","us-east-1","ap-northeast-2","ap-northeast-3","eu-west-2","ap-southeast-4","eu-south-1","ap-northeast-1","us-west-2","us-west-1","ap-southeast-1","ap-southeast-2","ca-central-1","eu-south-2","eu-central-2"],
      "accountsOrDomains":"000000000000"
    }
  }
  
  dante = Dante(
    userAccountId = request_dict["metadata"]["awsAccountId"], 
    loginAliasId = request_dict["metadata"]["userName"]
    )
  try:
    danteResult_dict = dante.get(payload_dict=dantePayload_dict)
  except:
    updateMsg(errorReason_list, logException("failed to request k2 with input_dict:[{}]".format(input_dict)))
    danteResult_dict = {}
  
  if "response" in danteResult_dict.keys():
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
    
