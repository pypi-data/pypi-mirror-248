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

from graphcode.lib import getDateString

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.profile import loadProfiles, listProfiles, saveProfiles, saveAccountDetails
from wooju.args import getInputs

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
  
  input_dict = getInputs(request_dict)
  
  customerDomainName = input_dict["customerDomainName"].strip().lower()
  if isinstance(customerDomainName, str) and len(customerDomainName.split(".")) >= 1 and len(customerDomainName.split(".")[0]) >= 2:
    logDebug("customerDomainName(len:{:,}->{:,}):[{}]".format(len(input_dict["customerDomainName"]), len(customerDomainName), customerDomainName))
  else:
    updateMsg(errorReason_list, logError("profileName(len:{:,}->{:,}):[{}] must be string and 3 characters at least".format(len(input_dict["customerDomainName"]), len(customerDomainName), customerDomainName)))
  
  if len(errorReason_list) > 0:
    return {
      "error": errorReason_list
      }
  logDebug("customerDomainName:[{}]".format(customerDomainName))
  
  profileName_dict = loadProfiles(request_dict)
  if customerDomainName in profileName_dict["DOMAINS"].keys():
    customerDomain_dict = profileName_dict["DOMAINS"][customerDomainName]
    logDebug("customerDomainName:[{}] is registered at profileNames:[{}]".format(customerDomainName, customerDomain_dict["profileNames"]))
      
  else:
    updateMsg(errorReason_list, logError("customerDomainName:[{}] must be registered".format(customerDomainName)))

  if len(errorReason_list) > 0:
    return {
      "error": errorReason_list
      }
  
  k2 = K2(userAccountId= request_dict["metadata"]["awsAccountId"], loginAliasId= request_dict["metadata"]["userName"])
  searchCustomerResult_list = k2.get(
    {
      "accountId": "000000000000",
      "regionCode": "us-east-1",
      "apiName":"kumoscp.searchCustomers", 
      "args": "{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"" + customerDomainName + "\",\"requestedBy\":\""+ request_dict["metadata"]["userName"]+"@\"}"
      }
    )
   
  snapshotTime = time.time()
  snapshotDate = getDateString(snapshotTime)
  discoveredAccountId_list = []
  for searchCustomerResultDetails_dict in searchCustomerResult_list:
    profileName = searchCustomerResultDetails_dict["name"]
    
    if profileName.lower() not in profileName_dict["__profileNames__"].keys():
      updateMsg(errorReason_list, logError("profileName:[{}] is not found at profiles".format(profileName)))
    
      if profileName not in customerDomain_dict["profileNames"]:
        updateMsg(errorReason_list, logError("profileName:[{}] is not found at domains".format(profileName)))
      else:
        customerDomain_dict["lastUpdateTime"] = snapshotTime
        customerDomain_dict["lastUpdateDate"] = snapshotDate
      
      profileName_dict["__profileNames__"][profileName.lower()] = {
        "fqpn":"{}/{}".format("/CUSTOMERS", profileName),
        "parentFQPN":"/CUSTOMERS",
        "profileName":profileName,
        "domains": [],
        "accountId_list": [],
        "lastUpdateTime": snapshotTime,
        "lastUpdateDate": snapshotDate,
        }
      
    else:  
      profileItem_dict = profileName_dict["__profileNames__"][profileName.lower()]
      logDebug("profileItem_dict:[{}]".format(profileItem_dict))
    
    if profileItem_dict["domains"] != None:
      if customerDomainName in profileItem_dict["domains"]:
        logWarn("customerDomainName:[{}] is found at profileName:[{}]".format(customerDomainName, profileName))
      else:
        profileItem_dict["domains"].append(customerDomainName)
    else:
      profileItem_dict["domains"] = [customerDomainName]
    logDebug("profileItem_dict:[{}]".format(profileItem_dict))
      
    thisContact_list = []
    for thisKey in searchCustomerResultDetails_dict.keys():
      logDebug("searchCustomerResult_dict:{}:[{}]".format(thisKey, searchCustomerResultDetails_dict[thisKey]))
    
      if searchCustomerResultDetails_dict[thisKey] in ["REDACTED"]:
        continue
      
      elif thisKey in ["serviceName_", "apiName_", "searchFilter_"]:
        continue
      
      elif thisKey in ["teamMembers"]:
        for teamMemberItem_dict in searchCustomerResultDetails_dict[thisKey]:
          thisRole = teamMemberItem_dict["role"]
          thisEmail = teamMemberItem_dict["email"]
          if thisEmail.split("@")[0] not in thisContact_list:
            thisContact_list.append(thisEmail.split("@")[0])
          
          if thisRole in customerDomain_dict.keys():
            if thisEmail not in customerDomain_dict[thisRole]:
              customerDomain_dict[thisRole].append(thisEmail)
            else:
              logWarn("email:[{}] is duplicated for role:[{}]".format(thisEmail, thisRole))
          else:
            customerDomain_dict[thisRole] = [thisEmail]
          
      else:
        customerDomain_dict[thisKey] = searchCustomerResultDetails_dict[thisKey]
    
    customerDomain_dict["contactAliases"] = thisContact_list
    if customerDomainName in profileName_dict["DOMAINS"].keys():
      logWarn("customerDomainName:[{}] is refreshed".format(customerDomainName))
    else:
      logDebug("customerDomainName:[{}] is new".format(customerDomainName))
    
    profileName_dict["DOMAINS"][customerDomainName] = customerDomain_dict
    for thisKey in profileName_dict["DOMAINS"][customerDomainName].keys():
      logDebug("{}:{}:\t{}".format(customerDomainName, thisKey, profileName_dict["DOMAINS"][customerDomainName][thisKey]))
    
    accountId_list = k2.get(
      { 
        "accountId": "000000000000",
        "regionCode": "us-east-1",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"" + customerDomain_dict["id"] + "\"}",
        }
      )
    
    accountIdCount = 0
    accountIdNumber = len(accountId_list) - 1
    if accountIdNumber < 10:
      percentageDelimiter = 1
    else:
      percentageDelimiter = int(accountIdNumber/3) + 1
    for accountIdItem_dict in accountId_list:
      if (accountIdCount % percentageDelimiter) == 0 or accountIdCount in [0, accountIdNumber]:
        logDebug("(#{:,}/{:,})\t accountIdItem_dict:[{}]".format(accountIdCount+1, accountIdNumber+1, accountIdItem_dict))
      accountIdCount += 1
      
      if accountIdItem_dict["accountId"] in profileName_dict["__accountIds__"].keys():
        if "profileNames" in profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]].keys()\
            and isinstance(profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]]["profileNames"], list):
              if profileName not in profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]]["profileNames"]:
                profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]]["profileNames"].append(profileName)
        else:
          profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]]["profileNames"] = [profileName]
         
        profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]] = {
          **profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]],
          "domainName":customerDomainName,
          "accountId":accountIdItem_dict["accountId"],
          "name":accountIdItem_dict["name"],
          "email":accountIdItem_dict["email"],
          "role":accountIdItem_dict["role"],
          "status":accountIdItem_dict["status"],
          "supportLevel":accountIdItem_dict["supportLevel"],
          
          "payerId":accountIdItem_dict["payerId"],
          "merchantId":accountIdItem_dict["merchantId"],
          
          "createdBy":accountIdItem_dict["createdBy"],
          "createdDate":accountIdItem_dict["createdDate"],
          "modifiedBy":accountIdItem_dict["modifiedBy"],
          "modifiedDate":accountIdItem_dict["modifiedDate"],
          
          "lastUpdateTime": snapshotTime,
          "lastUpdateDate": snapshotDate
          }
        updateMsg(logMessage_list, "accountId:[{}] is updated with customerDomainName:[{}]".format(accountIdItem_dict["accountId"], customerDomainName))
        
      else:
        profileName_dict["__accountIds__"][accountIdItem_dict["accountId"]] = {
          "profileNames": [profileName], 
          "domainName":customerDomainName,
          "accountId":accountIdItem_dict["accountId"],
          "name":accountIdItem_dict["name"],
          "email":accountIdItem_dict["email"],
          "role":accountIdItem_dict["role"],
          "status":accountIdItem_dict["status"],
          "supportLevel":accountIdItem_dict["supportLevel"],
          "primaryRegion": None,
          "regionNames": None,
          "accountSize": None,
          "tier1Score":None,   
          "prodEnvironmentScore": None,
          "resilienceScore": None,
          "riskScore": None,
          "riskPredictionMethods": None, 
            # manual: the score is provided by a customer or a relevant stake holder
            # machine: the score is provided by a machine 
            # hybrid: the score is provided by a machine and a human
          "activeRegions": None,
          "activeServices": None,
          "usedServices": None,
          
          "billing_email": None,  
          "billing_title": None,  
          "billing_phoneNumber": None,  
          "operations_email": None,  
          "operations_title": None, 
          "operations_phoneNumber": None, 
          "security_email": None,  
          "security_title": None,  
          "security_phoneNumber": None,
          
          "primaryOwner":None,
          "secondaryOwner":None,
          "finanaceOwner":None,
          "businessOwner":None,
          "profileOwner":None,
          
          "payerId":accountIdItem_dict["payerId"],
          "merchantId":accountIdItem_dict["merchantId"],
          
          "createdBy":accountIdItem_dict["createdBy"],
          "createdDate":accountIdItem_dict["createdDate"],
          "modifiedBy":accountIdItem_dict["modifiedBy"],
          "modifiedDate":accountIdItem_dict["modifiedDate"],
          
          "lastUpdateTime": snapshotTime,
          "lastUpdateDate": snapshotDate
          }
        updateMsg(logMessage_list, "accountId:[{}] is added with customerDomainName:[{}]".format(accountIdItem_dict["accountId"], customerDomainName))
      
      if accountIdItem_dict["status"] != "Suspended":
        discoveredAccountId_list.append(accountIdItem_dict["accountId"])
      
      if accountIdItem_dict["accountId"] not in profileItem_dict["accountId_list"]:
        profileItem_dict["accountId_list"].append(accountIdItem_dict["accountId"])
      
  if len(searchCustomerResult_list) > 0:
    saveProfiles(request_dict, profileName_dict)
    saveAccountDetails(request_dict, accountDetails_dict=profileName_dict["__accountIds__"])
   
  if len(searchCustomerResult_list) > 0:
    saveProfiles(request_dict, profileName_dict)
  
    tammyRequest_dict = {
        **request_dict,
        "apiName": "profile.discoverAccounts"
        }
    tammyRequest_dict["attributes"]["accountIds"] = "{}".format(discoveredAccountId_list)
    result_dict = requests(tammyRequest_dict)
    
    errorReason_list = consolidateErrorReasons(errorReason_list, result_dict)
    logMessage_list = consolidateLogMessages(logMessage_list, result_dict)
  
  profileList_dict = listProfiles(request_dict)
  #updateMsg(errorReason_list, profileList_dict)
  
  return {
    **profileList_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }