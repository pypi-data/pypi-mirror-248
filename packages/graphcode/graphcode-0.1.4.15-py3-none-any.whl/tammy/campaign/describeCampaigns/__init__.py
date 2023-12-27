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
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.lib import loadRevision_list
from wooju.lib import loadResourceDetailsWithIndex_dict, loadResourceDetailsIndex_list

def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "state": "SUCCEEDED",
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
  
  index_list = []
  campaignDetails_dict ={}
  try:
    index_list = loadResourceDetailsIndex_list(request_dict)
    
    serviceName_list = []
    for indexItem_dict in index_list:
      try:
        serviceName_list.append(indexItem_dict["serviceName"])
        updateMsg(logMessage_list, {"thisServiceName":indexItem_dict["serviceName"], **indexItem_dict})
        
      except:
        updateMsg(errorReason_list, logException("unexpected indexItem_dict:[{}]".format(indexItem_dict)))
    
    campaignDetails_dict = loadResourceDetailsWithIndex_dict(request_dict, serviceName_list=serviceName_list)
  except:
    index_list = [
      {
        "error": updateMsg(errorReason_list, logException("failed to load 'index_list' of esCustomer details"))
        }
      ]
    
  try:
    revision_list = loadRevision_list(request_dict)
  except:
    revision_list = [
      {
        "error": updateMsg(errorReason_list, logException("unable to load revision_list"))
        }
      ]
    
  return {
    ".index":index_list,
    ".revision":revision_list,
    **campaignDetails_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
