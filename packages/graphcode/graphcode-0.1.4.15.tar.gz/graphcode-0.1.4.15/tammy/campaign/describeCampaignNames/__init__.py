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

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

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
  
  cwd = __file__.replace("describeCampaignNames","discoverCampaigns")
  logDebug("cwd:[{}]".format(cwd))
  
  campaignName_list = []
  for campaignName in listDir(dirname(cwd), type = "dir"):
    if campaignName.startswith("_"):
      continue
    
    campaignName_list.append(
      {
        "campaignName": campaignName.replace("_"," ")
        }
      )
    
  return {
    "campaignNames": campaignName_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
