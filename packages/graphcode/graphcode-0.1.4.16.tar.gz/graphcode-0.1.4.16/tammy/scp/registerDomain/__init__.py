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
  
  profileName = input_dict["profileName"].strip()
  if isinstance(profileName, str):
    if len(profileName) >= 3:
      logDebug("profileName(len:{:,}->{:,}):[{}]".format(len(input_dict["profileName"]), len(profileName), profileName))
    elif len(profileName) == 0:
      profileName = None
      logDebug("profileName will be set with customer name")
    else:
      updateMsg(errorReason_list, logError("profileName(len:{:,}->{:,}):[{}] must be string and 3 characters at least".format(len(input_dict["profileName"]), len(profileName), profileName)))
  else:
    updateMsg(errorReason_list, logError("profileName(len:{:,}->{:,}):[{}] must be string and 3 characters at least".format(len(input_dict["profileName"]), len(profileName), profileName)))
  logDebug("profileName:[{}]".format(profileName))
  
  customerDomainName = input_dict["customerDomainName"].strip().lower()
  if isinstance(customerDomainName, str) and len(customerDomainName.split(".")) >= 1 and len(customerDomainName.split(".")[0]) >= 2:
    logDebug("customerDomainName(len:{:,}->{:,}):[{}]".format(len(input_dict["customerDomainName"]), len(customerDomainName), customerDomainName))
  else:
    updateMsg(errorReason_list, logError("customerDomainName(len:{:,}->{:,}):[{}] must be string and 3 characters at least".format(len(input_dict["customerDomainName"]), len(customerDomainName), customerDomainName)))
  logDebug("customerDomainName:[{}]".format(customerDomainName))
  
  if len(errorReason_list) > 0:
    return {
      "error": errorReason_list
      }
    
  profileName_dict = loadProfiles(request_dict)
  if profileName != None:
    if profileName.lower() in profileName_dict["__profileNames__"].keys():
      logDebug("profileName:[{}] is found".format(profileName))
    else:
      updateMsg(errorReason_list, logError("profileName:[{}] is not found".format(profileName)))
  
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
  registeredAccountId_list = []
  for searchCustomerResultDetails_dict in searchCustomerResult_list:
    if profileName == None:
      profileName = searchCustomerResultDetails_dict["name"]
    
    if profileName.lower() not in profileName_dict["__profileNames__"].keys():
      #logDebug("#profileName:[{}] is not found".format(profileName))
    
      profileName_dict["__profileNames__"][profileName.lower()] = {
        "fqpn":"{}/{}".format("/CUSTOMERS", profileName),
        "parentFQPN":"/CUSTOMERS",
        "profileName":profileName,
        "domains": [],
        "accountId_list": [],
        "lastUpdateTime": snapshotTime,
        "lastUpdateDate": snapshotDate,
        }
      profileItem_dict = profileName_dict["__profileNames__"][profileName.lower()]
      
    else:  
      profileItem_dict = profileName_dict["__profileNames__"][profileName.lower()]
    logDebug("profileItem_dict:[{}]".format(profileItem_dict))
    
    parentFullyQualifiedProfileName = profileName_dict["__profileNames__"][profileName.lower()]["parentFQPN"]
    logDebug("parentFullyQualifiedProfileName:[{}]".format(parentFullyQualifiedProfileName))
    if len(parentFullyQualifiedProfileName) >= 3:
      thisProfileName_dict = profileName_dict
      logDebug("parentFullyQualifiedProfileName:[{}]".format(parentFullyQualifiedProfileName))
      
      thisParentFullyQualifiedProfileName = ""
      if parentFullyQualifiedProfileName.startswith("/"):
        parentFullyQualifiedProfileName_list = parentFullyQualifiedProfileName[1:].split("/")
      else:
        parentFullyQualifiedProfileName_list = parentFullyQualifiedProfileName.split("/")
        
      for thisProfileName in parentFullyQualifiedProfileName_list:
        if len(thisProfileName.strip()) >= 3 and thisProfileName in thisProfileName_dict.keys():
          thisParentFullyQualifiedProfileName += "/{}".format(thisProfileName)
          thisProfileName_dict = thisProfileName_dict[thisProfileName]
          logDebug("thisProfileName:[{}] is found in FQPN:[{}]:[{}]".format(thisProfileName, thisParentFullyQualifiedProfileName, thisProfileName_dict.keys()))
        else:
          updateMsg(errorReason_list, "thisProfileName:[{}] is not found in FQPN:[{}]".format(thisProfileName, thisParentFullyQualifiedProfileName))
      
          return {
            "error": errorReason_list
            }
      
      thisProfileName_dict[profileName] = {}
      
    if profileItem_dict["domains"] != None:
      if customerDomainName in profileItem_dict["domains"]:
        logWarn("customerDomainName:[{}] is found at profileName:[{}]".format(customerDomainName, profileName))
      else:
        profileItem_dict["domains"].append(customerDomainName)
    else:
      profileItem_dict["domains"] = [customerDomainName]
    logDebug("profileItem_dict:[{}]".format(profileItem_dict))
    
    if customerDomainName in profileName_dict["DOMAINS"].keys():
      if "profileNames" in profileName_dict["DOMAINS"][customerDomainName].keys() and isinstance(profileName_dict["DOMAINS"][customerDomainName]["profileNames"], list):
        if profileName in profileName_dict["DOMAINS"][customerDomainName]["profileNames"]:
          logDebug("customerDomainName:[{}] is already registered to profileName:[{}]".format(customerDomainName, profileName))
        else:
          profileName_dict["DOMAINS"][customerDomainName]["profileNames"].append(customerDomainName)
          logDebug("customerDomainName:[{}] is being registered to profileName:[{}]".format(customerDomainName, profileName))
      else:
        profileName_dict["DOMAINS"][customerDomainName]["profileNames"] = [profileName]
    else:
      profileName_dict["DOMAINS"][customerDomainName] = {
        "profileNames":[profileName]
        }
      
    customerDomain_dict = profileName_dict["DOMAINS"][customerDomainName]
    customerDomain_dict["lastUpdateTime"] = snapshotTime
    customerDomain_dict["lastUpdateDate"] = snapshotDate
      
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
    
    if len(accountId_list) > 0 and profileItem_dict["accountId_list"] == None:
      profileItem_dict["accountId_list"] = []
      logDebug("profileItem_dict['accountId_list']:[{}] is set ".format(profileItem_dict["accountId_list"]))
    
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
        registeredAccountId_list.append(accountIdItem_dict["accountId"])
      
      if accountIdItem_dict["accountId"] not in profileItem_dict["accountId_list"]:
        profileItem_dict["accountId_list"].append(accountIdItem_dict["accountId"])
        #logDebug("profileItem_dict['accountId_list']:[len:{:,}] is updated ".format(len(profileItem_dict["accountId_list"])))
  
  if len(registeredAccountId_list) > 0:
    saveProfiles(request_dict, profileName_dict)
  
  if len(registeredAccountId_list) > 0 \
      and ("dryRun" not in request_dict["attributes"].keys() or request_dict["attributes"]["dryRun"].lower() not in ["true", "yes"]):
    saveProfiles(request_dict, profileName_dict)
    saveAccountDetails(request_dict, accountDetails_dict=profileName_dict["__accountIds__"])
  
    tammyRequest_dict = {
        **request_dict,
        "apiName": "profile.discoverAccounts"
        }
    tammyRequest_dict["attributes"]["accountIds"] = "{}".format(registeredAccountId_list)
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