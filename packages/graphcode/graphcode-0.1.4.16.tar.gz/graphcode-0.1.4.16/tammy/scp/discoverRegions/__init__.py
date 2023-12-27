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
from graphcode.delimiter import getDelimiter, displayItemDetails

from graphcode.unittest import unitTest

from graphcode.lib import getDateString

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.lib import updateRevision_list
from wooju.lib import saveResourceDetailsWithIndex_dict, loadResourceDetailsIndex_list

from wooju.lib import cacheWbRun
from wooju.lib import saveCache, loadCache, deleteCache
from wooju.profile import loadProfiles, listProfiles, saveProfiles, saveAccountDetails
from wooju.args import getCustomerDomainName

from tammy.ldap import PdxLdap
from tammy.k2 import K2

from wooju.resource import saveGetRegions_dict
from wooju.account import saveRegionHeatMap

import time

def response(request_dict):
  response_dict = {
    "apiName": request_dict["apiName"],
    "response": action(request_dict),
    "__file__": __file__
    }

  return response_dict

def action(request_dict):
  request_dict["apiName"] = request_dict["apiName"].replace("tammy","profile")
  
  logMessage_list = []
  errorReason_list = []
  
  try:
    customerDomainName = getCustomerDomainName(request_dict)
    if len(customerDomainName.strip()) > 0:
      request_dict["attributes"]["domainIds"] = [customerDomainName]
    else:
      raiseValueError("customerDomainName:[{}](len:{:,}) is not valid".format(customerDomainName, len(customerDomainName)))
  except:
    raiseValueError("customerDomainName is not found")
  
  for key in request_dict["attributes"].keys():
    logDebug("attributes.{}({}):[{}]".format(key, type(request_dict["attributes"][key]).__name__, request_dict["attributes"][key]))
  
  getRegionByDomainId_dict = updateGetRegionByDomainId(request_dict, errorReason_list, logMessage_list)
  
  index_list = saveResourceDetailsWithIndex_dict(request_dict, resourceDetails_dict=getRegionByDomainId_dict)
  
  
  revision_dict={
    "date": getDateString("now", "date"),
    "state":request_dict["apiName"].split(".")[-1],
    }
  
  for domainId in getRegionByDomainId_dict.keys():
    revision_dict[domainId] = len(getRegionByDomainId_dict[domainId])
  
  revision_list = updateRevision_list(
    request_dict,
    revision_dict
    )
  
  return {
    ".index": index_list,
    ".revision": revision_list,
    **getRegionByDomainId_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
  
def updateGetRegionByDomainId(request_dict, errorReason_list, logMessage_list):
  try:
    raiseValueError("error")
    getRegionByDomainId_dict = loadCache(request_dict, name="getRegionByDomainId_dict")
  except:
    getRegionByDomainId_dict = getGetRegionByDomainId(request_dict, 3600*24, errorReason_list, logMessage_list)
    saveCache(request_dict, name="getRegionByDomainId_dict", value=getRegionByDomainId_dict, ttl_s=3600*24)

  saveGetRegions_dict(request_dict, getRegionByDomainId_dict, source="domainId")
  saveRegionHeatMap(request_dict)
  
  return getRegionByDomainId_dict
  
def getGetRegionByDomainId(request_dict, ttl_s, errorReason_list, logMessage_list):
  
  request_dict["attributes"]["dbType"] = "aws"
  request_dict["attributes"]["dryRun"] = False
  response_dict = requests(
    request_dict = {
        **request_dict,
        "apiName":"tammy.dw.aws.templates.esCustomer_Provisioning"
      }
    )
      
  return response_dict["response"]
  