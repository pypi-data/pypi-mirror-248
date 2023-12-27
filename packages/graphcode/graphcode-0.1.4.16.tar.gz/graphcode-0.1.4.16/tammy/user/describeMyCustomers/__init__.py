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

from graphcode.unittest import unitTest

from graphcode.lib import getDateString

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.profile import loadProfiles, listProfiles, saveProfiles, saveAccountDetails
from wooju.args import getInputs
from wooju.args import getUserNames

from tammy.k2 import K2

import time

import json

def response(request_dict):
  request_dict["apiName"] = request_dict["apiName"].replace("tammy","profile")
  response_dict = {
    "apiName": request_dict["apiName"],
    "response": action(request_dict),
    "__file__": __file__
    }

  return response_dict

def action(request_dict):
  logMessage_list = []
  errorReason_list = []
  
  myCustomers_dict = {
    "primaryTAM":[],
    "secondaryTAM":[],
    "nightTimeTAM":[],
  }
  
  myCustomerAccountByDomainId_dict = {}
  response_dict = requests(
    request_dict = {
        **request_dict,
        "apiName":"tammy.user.discoverCustomers"
      }
    )
  
  for customerItem_dict in response_dict["response"]["customerList"]:
    try:
      if request_dict["metadata"]["userName"] in customerItem_dict["ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY"]:
        myCustomers_dict["primaryTAM"].append(customerItem_dict)
        continue
    except:
      updateMsg(errorReason_list, logException("unexpected error at customerItem_dict:[{}]".format(customerItem_dict)))
      
    try:
      if request_dict["metadata"]["userName"] in customerItem_dict["ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY"]:
        myCustomers_dict["secondaryTAM"].append(customerItem_dict)
        continue
    except:
      updateMsg(errorReason_list, logException("unexpected error at customerItem_dict:[{}]".format(customerItem_dict)))
      
    try:
      if request_dict["metadata"]["userName"] in customerItem_dict["ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME"]:
        myCustomers_dict["nightTimeTAM"].append(customerItem_dict)
        continue
    except:
      updateMsg(errorReason_list, logException("unexpected error at customerItem_dict:[{}]".format(customerItem_dict)))
  
  myCustomer_list = []
  for tamRole in myCustomers_dict.keys():
    for customerItem_dict in myCustomers_dict[tamRole]:
      customerItem_dict["accountIds"] = []

      myCustomerAccountByDomainId_dict[customerItem_dict["primaryWebDomain"]] = []
      k2 = K2(userAccountId= request_dict["metadata"]["awsAccountId"], loginAliasId= request_dict["metadata"]["userName"])
      for accountIdItem_dict in k2.get(
                                        { 
                                          "accountId": "000000000000",
                                          "regionCode": "us-east-1",
                                          "apiName":"kumoscp.getCustomerAccountFullList",
                                          "args":"{\"id\":\"" + customerItem_dict["id"] + "\"}",
                                          }
                                        ):
        accountIdItem_dict = {
          "tamRole": tamRole,
          **accountIdItem_dict,
        }
        myCustomerAccountByDomainId_dict[customerItem_dict["primaryWebDomain"]].append(accountIdItem_dict)
        customerItem_dict["accountIds"].append(accountIdItem_dict["accountId"])
        
      myCustomer_list.append(customerItem_dict)

      if tamRole in ["primaryTAM", "secondaryTAM"]:
        request_dict["attributes"]["parentFullyQualifiedProfileName"] = "/CUSTOMERS"
        request_dict["attributes"]["profileName"] = f"{customerItem_dict['primaryWebDomain']}"
        request_dict["attributes"]["profileNames"] = ""
        request_dict["attributes"]["customerDomainName"] = ""
        request_dict["attributes"]["accountIds"] = ""
        response_dict = requests(
          request_dict = {
              **request_dict,
              "apiName":"profile.createProfile"
            }
          )
        request_dict["attributes"]["parentFullyQualifiedProfileName"] = "/CUSTOMERS/{}".format(customerItem_dict["primaryWebDomain"])
        request_dict["attributes"]["profileName"] = f"{customerItem_dict['primaryWebDomain']} - {customerItem_dict['name']}"
        response_dict = requests(
          request_dict = {
              **request_dict,
              "apiName":"profile.createProfile"
            }
          )
        
        request_dict["attributes"]["dryRun"] = "true"
        request_dict["attributes"]["profileName"] = f"{customerItem_dict['primaryWebDomain']} - {customerItem_dict['name']}"
        request_dict["attributes"]["customerDomainName"] = f"{customerItem_dict['primaryWebDomain']}"
        response_dict = requests(
          request_dict = {
              **request_dict,
              "apiName":"tammy.scp.registerDomain"
            }
          )
      else:
        request_dict["attributes"]["parentFullyQualifiedProfileName"] = "/CUSTOMERS"
        request_dict["attributes"]["profileName"] = f"{customerItem_dict['primaryWebDomain']}"
        request_dict["attributes"]["profileNames"] = ""
        request_dict["attributes"]["customerDomainName"] = ""
        request_dict["attributes"]["accountIds"] = ""
        response_dict = requests(
          request_dict = {
              **request_dict,
              "apiName":"profile.createProfile"
            }
          )
    
  return {
    "myCustomers": myCustomer_list,
    **myCustomerAccountByDomainId_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }