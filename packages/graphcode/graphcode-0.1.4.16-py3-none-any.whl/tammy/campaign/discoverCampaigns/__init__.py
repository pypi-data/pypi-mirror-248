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

from graphcode.path import listDir

from graphcode.lib import getDateString

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.lib import updateRevision_list
from wooju.lib import saveResourceDetailsWithIndex_dict, loadResourceDetailsIndex_list

from wooju.args import getCampaignNames

from wooju.account import loadRegionHeatMap_dict as loadAccountRegionHeatMap_dict

from tammy.campaign import getCamapaignServiceNames
from tammy.campaign import setCampaignAttributes

from os.path import dirname

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
  
  response_dict = requests(
    request_dict = setCampaignAttributes(request_dict)
  )

  campaignDetails_dict = {}
  for resKey in response_dict["response"].keys():
    if resKey in ["logMessages"]:
      for logLine in response_dict["response"][resKey]:
        logMessage_list.append(logLine)
    elif resKey in ["errorReasons"]:
      for errorLine in response_dict["response"][resKey]:
        errorReason_list.append(errorLine)
    else:
      campaignDetails_dict[resKey] = response_dict["response"][resKey]
  
  index_list = saveResourceDetailsWithIndex_dict(request_dict, resourceDetails_dict=campaignDetails_dict)
  
  revision_dict={
    "date": getDateString("now", "date"),
    "state":request_dict["apiName"].split(".")[-1],
    }
  
  for campaignName in campaignDetails_dict.keys():
    revision_dict[campaignName] = len(campaignDetails_dict[campaignName])
  
  revision_list = updateRevision_list(
    request_dict,
    revision_dict
    )
  
  return {
    ".index": index_list,
    ".revision": revision_list,
    **campaignDetails_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }