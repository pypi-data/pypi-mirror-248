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

from graphcode.lib import getDateString, getChunkedLists

from pathway import requests
from pathway import updateMsg
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.profile import loadProfiles, listProfiles, saveProfiles
from wooju.args import getInputs, getAccountIdsFromString, getCustomerDomainNames
from wooju.args import getUserNames


from graphcode.workbench import workbenchV3

from tammy.k2 import K2

import time

def response(request_dict):
  request_dict["apiName"] = request_dict["apiName"].replace("tammy","profile")
  
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
  
  customerDomainName_list = getCustomerDomainNames(request_dict)
  
  try:
    request_dict["attributes"]["userNames"] = getUserNames(request_dict)
  except:
    request_dict["attributes"]["userNames"] = [request_dict["metadata"]["userName"]]
    
  result_dict = requests(
    request_dict = {
      **request_dict,
      "apiName": "tammy.user.discoverCustomers"
      }
    )
  errorReason_list = consolidateErrorReasons(errorReason_list, result_dict)
  logMessage_list = consolidateLogMessages(logMessage_list, result_dict)
  
  accountId_list = []
  userCustomerDomainName_list = []
  matchedCustomerDomainNameCount = 0
  logDebug("customerDomainName:[{}]".format(customerDomainName_list))
  logDebug("response:[{}]".format(result_dict["response"]["customerList"]))
  for customerItem_dict in result_dict["response"]["customerList"]:
    try:
      logDebug("primaryWebDomain:[{}]".format(customerItem_dict["primaryWebDomain"]))
      userCustomerDomainName_list.append(customerItem_dict["primaryWebDomain"])
    except:
      logException("unexpected {}:customerItem_dict:[{}]".format(type(customerItem_dict).__name__, customerItem_dict))
      continue
    
    if customerItem_dict["primaryWebDomain"].strip() in customerDomainName_list:
      matchedCustomerDomainNameCount += 1
      k2 = K2(userAccountId= request_dict["metadata"]["awsAccountId"], loginAliasId= request_dict["metadata"]["userName"])
      for accountIdItem_dict in k2.get(
                                        { 
                                          "accountId": "000000000000",
                                          "regionCode": "us-east-1",
                                          "apiName":"kumoscp.getCustomerAccountFullList",
                                          "args":"{\"id\":\"" + customerItem_dict["id"] + "\"}",
                                          }
                                        ):

        try:
          del accountIdItem_dict["serviceName_"]
        except:
          logError('serviceName_ not found')
        
        try:
          del accountIdItem_dict["apiName_"]
        except:
          logError('apiName_ not found' )
        
        try:
          del accountIdItem_dict["id_"]
        except:
          logError('id_ not found' )
        
        accountId_list.append(accountIdItem_dict)
  
  if matchedCustomerDomainNameCount == 0:
    raiseValueError("domainNames:{} is invalid or not associated to {}@ that owns domainIds:[{}]".format(customerDomainName_list, request_dict["metadata"]["userName"], userCustomerDomainName_list))
    
  return {
    "accountList": accountId_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }