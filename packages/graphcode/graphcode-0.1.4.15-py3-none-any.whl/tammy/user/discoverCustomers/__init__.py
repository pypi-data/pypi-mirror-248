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
  
  try:
    userName_list = getUserNames(request_dict)
  except:
    userName_list = [request_dict["metadata"]["userName"]]
    
  tam_list = []
  searchCustomerResult_list = []
  for userName in userName_list:
    k2 = K2(userAccountId= request_dict["metadata"]["awsAccountId"], loginAliasId= request_dict["metadata"]["userName"])
    thisCustomerResult_list = k2.get(
      {
        "accountId": "000000000000",
        "regionCode": "us-east-1",
        "apiName":"kumoscp.searchCustomers", 
        "args": "{\"searchFilter\":\"EMAIL\",\"searchFilterValue\":\"" + userName + "\",\"requestedBy\":\""+ request_dict["metadata"]["userName"] +"@\"}",
        }
      )
    
    for customerItem_dict in thisCustomerResult_list:
      try:
        for teamMembersItem_dict in customerItem_dict["teamMembers"]:
          role = teamMembersItem_dict["role"]
          email = teamMembersItem_dict["email"].strip().replace("@amazon.com","")
          
          if role in customerItem_dict.keys() and email not in customerItem_dict[role]:
            customerItem_dict[role].append(email)
          else:
            customerItem_dict[role] = [email]
          
          if role in ["ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY", "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY", "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME"]:
            if email not in tam_list:
              tam_list.append(email)
              
          for key in teamMembersItem_dict.keys():
            if key in ["role", "email"]:
              continue
            
            elif key in customerItem_dict.keys():
              customerItem_dict[key].append(teamMembersItem_dict[key])
            
            else:
              customerItem_dict[key] = [teamMembersItem_dict[key]]
            
        
        del customerItem_dict["teamMembers"]
        
        try:
          customerItem_dict = {
            "region":customerItem_dict["supportLocations"][-1]["region"],
            "area":customerItem_dict["supportLocations"][-1]["name"],
            **customerItem_dict
            }
        except:
          logError('unexpected supportLocations or supportLocations not found')
          
        try:
          del teamMembersItem_dict["serviceName_"]
        except:
          logError('serviceName_ not found')
      
        try:
          del teamMembersItem_dict["apiName_"]
        except:
          logError('apiName_ not found')
          
        try:
          del teamMembersItem_dict["searchFilter_"]
        except:
          logError('searchFilter_ not found')
        try:
          del teamMembersItem_dict["requestedBy_"]
        except:
          logError('requestedBy_ not found')
        try:
          del teamMembersItem_dict["searchFilterValue_"]
        except:
          logError('searchFilterValue_ not found')
        
        searchCustomerResult_list.append(customerItem_dict)
        
      except:
        logException('teamMembers not found, unexpected customerItem_dict:[{}]'.format(customerItem_dict))
    
    tamStr = ""
    for tamAliasId in tam_list:
      if tamStr == "":
        tamStr += tamAliasId
      else:
        tamStr += ",{}".format(tamAliasId)
    searchCustomerResult_list.append({"contractNotes":tamStr})
    
  return {
    "customerList": searchCustomerResult_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
  
def getCustoerList(userAccountId = "749952098923", loginAliasId = "hoeseong"):
  k2 = K2(userAccountId=userAccountId, loginAliasId=loginAliasId)
  searchCustomerResult_list = k2.get(
    {
      "accountId": "000000000000",
      "regionCode": "us-east-1",
      "apiName":"kumoscp.searchCustomers", 
      "args": "{\"searchFilter\":\"EMAIL\",\"searchFilterValue\":\"" + "syellajo" + "\",\"requestedBy\":\""+ loginAliasId+"@\"}",
      }
    )
  
  for customerItem_dict in searchCustomerResult_list:
    try:
      for teamMembersItem_dict in customerItem_dict["teamMembers"]:
        role = teamMembersItem_dict["role"]
        email = teamMembersItem_dict["email"].strip().replace("@amazon.com","")
        
        if role in customerItem_dict.keys() and email not in customerItem_dict[role]:
          customerItem_dict[role].append(email)
        else:
          customerItem_dict[role] = [email]
          
        for key in teamMembersItem_dict.keys():
          if key in ["role", "email"]:
            continue
          
          elif key in customerItem_dict.keys():
            customerItem_dict[key].append(teamMembersItem_dict[key])
          
          else:
            customerItem_dict[key] = [teamMembersItem_dict[key]]
      
      del customerItem_dict["teamMembers"]
      
      try:
        del teamMembersItem_dict["serviceName_"]
      except:
        logError('serviceName_ not found')
      
      try:
        del teamMembersItem_dict["apiName_"]
      except:
        logError('apiName_ not found')
        
      try:
        del teamMembersItem_dict["searchFilter_"]
      except:
        logError('searchFilter_ not found')
      try:
        del teamMembersItem_dict["requestedBy_"]
      except:
        logError('requestedBy_ not found')
      try:
        del teamMembersItem_dict["searchFilterValue_"]
      except:
        logError('searchFilterValue_ not found')
      
    except:
      logException('teamMembers not found, unexpected customerItem_dict:[{}]'.format(customerItem_dict))
    
    logDebug("customerItem_dict:[{}]".format(customerItem_dict))
  
def localUnitTest():
  unitTestFunction_dict = {"getCustoerList":{"target":getCustoerList, "args":()},
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()