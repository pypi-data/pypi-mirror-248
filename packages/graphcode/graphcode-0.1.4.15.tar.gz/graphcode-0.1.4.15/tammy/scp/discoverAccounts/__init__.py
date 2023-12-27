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
from wooju.profile import loadProfiles, listProfiles, saveProfiles
from wooju.args import getInputs, getAccountIdsFromString

from wooju.score import predictRiskScore

from graphcode.workbench import workbenchV3

from tammy.k2 import K2

import time

def response(request_dict):
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

  accountId_list = getAccountIdsFromString(accountIds=input_dict["accountIds"])
  if len(accountId_list) > 0:
    logDebug("accountId_list:[{}]".format(accountId_list))
    
  else:
    updateMsg(errorReason_list, logError("unexpected AccountIds:[{}] must be string and 12 digits".format(input_dict["accountIds"])))
  
  if len(errorReason_list) > 0:
    return {
      "errorReason": errorReason_list
      }
  
  primaryRegion_dict = {
    "us-east-1": None,
    "cn-north-1": None
    }
  
  accountDetails_dict = {}
  updatePrimaryRegion(request_dict, primaryRegion_dict, accountId_list, accountDetails_dict, primaryRegionCode = "us-east-1")
  
  cnAccountId_list = []
  for thisAccountId in set(accountDetails_dict.keys()):
    try:
      if accountDetails_dict[thisAccountId]["primaryRegion"] == None:
        cnAccountId_list.append(thisAccountId)
    except:
      logException("unexpected accountDetails_dict[{}]:[{}]".format(thisAccountId, accountDetails_dict[thisAccountId]))
      
  if len(cnAccountId_list) > 0:
    updatePrimaryRegion(request_dict, primaryRegion_dict, cnAccountId_list, accountDetails_dict, primaryRegionCode = "cn-north-1")

  #updateSupportLevelAndContacts(request_dict, accountDetails_dict)
  
  return accountDetails_dict

def updatePrimaryRegion(request_dict, primaryRegion_dict, accountId_list, accountDetails_dict, primaryRegionCode = "us-east-1"):
  k2 = K2(userAccountId= request_dict["metadata"]["awsAccountId"], loginAliasId= request_dict["metadata"]["userName"])
  
  if primaryRegionCode in ["cn-north-1"]:
    thisPT = "1x1"
    thisChunkSize = 10
  else:
    thisPT = "8x8"
    thisChunkSize = 10
    
  wbRequest_list = []
  for chunkedAccountIds in getChunkedLists(original_list=accountId_list, chunkSize=thisChunkSize):
    #logDebug("#chunkedAccountIds:[{}]".format(chunkedAccountIds))
    
    wbRequest_list.append(
      {
        "accountId": chunkedAccountIds[-1],
        "regionCode": primaryRegionCode,
        "apiList":  [
          { 
            "platform":"k2",
            "apiName":"avs.getAccountStatus",
            "args":{"accountIds":chunkedAccountIds},
            "inputs":"",
            "conditions":"",
            "limit":"",
            "pt":thisPT
            }
          ]
        }
      )
      
  wbResult_dict = workbenchV3(user_dict=request_dict["metadata"], request_list=wbRequest_list)
  for wbResultKey in wbResult_dict.keys():
    for wbResultItem_dict in wbResult_dict[wbResultKey]:
      #logDebug("#{}:[{}]".format(wbResultItem_dict["accountId"], wbResultItem_dict["accountStatus"]))
      
      try:
        thisAccountId = wbResultItem_dict["accountId"]
      except:
        try:
          accountDetails_dict[wbResultItem_dict["accountId_"]] = wbResultItem_dict
          thisAccountId = wbResultItem_dict["accountId_"]
          logException("---->unexpected thisAccountId:[{}]->{}:wbResultItem_dict:[{}]".format(thisAccountId, type(wbResultItem_dict).__name__, wbResultItem_dict))
        except:
          logException("---->unexpected {}:wbResultItem_dict:[{}]".format(type(wbResultItem_dict).__name__, wbResultItem_dict))
          continue
        
      try:  
        if wbResultItem_dict["accountStatus"] == "Active":
          accountDetails_dict[thisAccountId] = {
            "accountId": thisAccountId,
            "status": wbResultItem_dict["accountStatus"],
            "primaryRegion": primaryRegionCode
            }
          
          if primaryRegion_dict[primaryRegionCode] == None:
            for result_dict in k2.get({ "accountId":"{}".format(thisAccountId).zfill(12), 
                                        "regionCode": primaryRegionCode, 
                                        "apiName":"ec2.describeRegions", 
                                        "args": {}
                                        }
                                      ):
              if isinstance(result_dict, dict) and "regionName" in result_dict.keys():
                if primaryRegion_dict[primaryRegionCode] == None:
                  primaryRegion_dict[primaryRegionCode] = [result_dict["regionName"]]
                else:
                  primaryRegion_dict[primaryRegionCode].append(result_dict["regionName"])
              else:
                logWarn("'regionNames' is not found result_dict:[{}]".format(result_dict))
            
            if primaryRegion_dict[primaryRegionCode] != None and len(primaryRegion_dict[primaryRegionCode]) > 0:
              accountDetails_dict[thisAccountId]["regionNames"] = primaryRegion_dict[primaryRegionCode]
          
          elif primaryRegion_dict[primaryRegionCode] != None and len(primaryRegion_dict[primaryRegionCode]) > 0:
            accountDetails_dict[thisAccountId]["regionNames"] = primaryRegion_dict[primaryRegionCode]
        
        else:
          accountDetails_dict[thisAccountId] = {
            "accountId": thisAccountId,
            "status": None,
            "primaryRegion": None,
            "regionNames": None,
            "errorReasons": wbResultItem_dict
            }
            
      except:
        logException("---->unexpected {}:wbResultItem_dict:[{}]".format(type(wbResultItem_dict).__name__, wbResultItem_dict))
        accountDetails_dict[thisAccountId] = {
          "accountId": thisAccountId,
          "status": None,
          "primaryRegion": None,
          "regionNames": None,
          "errorReasons": wbResultItem_dict
          }
    
  return accountDetails_dict

def updateSupportLevelAndContacts(request_dict, accountDetails_dict):
  accountId_dict = {}
  for thisAccountId in accountDetails_dict.keys():
    if accountDetails_dict[thisAccountId]["primaryRegion"] in accountId_dict.keys():
      accountId_dict[accountDetails_dict[thisAccountId]["primaryRegion"]].append(thisAccountId)
    else:
      accountId_dict[accountDetails_dict[thisAccountId]["primaryRegion"]] = [thisAccountId]
      
  wbRequest_list = []
  for primaryRegion in accountId_dict.keys():
    for chunkedAccountIds in getChunkedLists(original_list=accountId_dict[primaryRegion], chunkSize=10):
      #logDebug("#chunkedAccountIds:[{}]".format(chunkedAccountIds))
      
      wbRequest_list.append(
        {
          "accountId": chunkedAccountIds[-1],
          "regionCode": primaryRegion,
          "apiList":  [
            { 
              "platform":"k2",
              "apiName":"avs.getSupportLevel",
              "args":{"accountIds":chunkedAccountIds},
              "inputs":"",
              "conditions":"",
              "limit":"",
              "pt":"16x8"
              },
            { 
              "platform":"k2",
              "apiName":"awscbresourceadminservice.getParentAccountForChildAccount",
              "args":"{\"accountId\":\"${__accountId__}\"}",
              "inputs":"sourceApiName=avs.getSupportLevel;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
              "conditions":"",
              "limit":"",
              "pt":"16x8"
              },
            {
              "platform":"k2", 
              "apiName":"awsadms.getAccountIdentifiersByAccountId", 
              "args":"{\"accountId\":\"${__accountId__}\"}", 
              "inputs":"sourceApiName=avs.getSupportLevel;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
              "limit":"",
              "pt":"12x8"
              },
            {
              "platform":"k2", 
              "apiName":"iss.searchCustomers", 
              #"args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
              "args": "{\"includeDeactivatedCustomers\": false,\"marketplaceId\": \"ATVPDKIKX0DER\",\"pageSize\": 10,\"query\": {\"terms\": [{\"field_\": \"CustomerId\",\"phonetic\": false,\"prefix\": false,\"value_\": \"${__CustomerIdType__}\"}]}}",
              "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=accountId:accountId_,regionCode:regionCode_,CustomerIdType:CustomerIdType",
              "limit":"",
              "pt":"12x8"
              },
            {
              "platform":"k2", 
              "apiName":"awsadms.getAlternateContacts",
              "args":"{\"accountId\":\"${__accountId__}\"}",
              "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
              "limit":"",
              "pt":"12x8"
              },
            {
              "platform":"k2", 
              "apiName":"#kumoscp.getTags",
              "args":"{\"resourceIds\":\"${__accountId__}\"}",
              "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
              "limit":"",
              "pt":"12x8"
              },
            ]
          }
        )
      
  wbResult_dict = workbenchV3(user_dict=request_dict["metadata"], request_list=wbRequest_list)
  for wbResultKey in wbResult_dict.keys():
    if "avs.getSupportLevel" in wbResultKey:
      for wbResultItem_dict in wbResult_dict[wbResultKey]:
        #logDebug("#{}:[{}]".format(wbResultKey, wbResultItem_dict))
        
        try:
          thisSupportLevel = wbResultItem_dict["supportLevel"].lower().replace("aws","").replace("support","")
          accountDetails_dict[wbResultItem_dict["accountId"]]["supportLevel"] = thisSupportLevel[0].upper() + thisSupportLevel[1:]
        except:
          logException("unexpected error:[{}]".format(wbResultItem_dict))
    
    elif "awscbresourceadminservice.getParentAccountForChildAccount"in wbResultKey:
      for wbResultItem_dict in wbResult_dict[wbResultKey]:
        try:
          accountDetails_dict[wbResultItem_dict["accountId_"]]["payerId"] = wbResultItem_dict["parentAccountId"]
        except:
          logException("unexpected {}:[{}]".format(wbResultKey, wbResultItem_dict))
          
    elif "getAlternateContacts" in wbResultKey:
      for wbResultItem_dict in wbResult_dict[wbResultKey]:
        try:
          if "contactType" in wbResultItem_dict.keys():
            accountDetails_dict[wbResultItem_dict["accountId_"]]["{}_email".format(wbResultItem_dict["contactType"])] = wbResultItem_dict["email"]
            accountDetails_dict[wbResultItem_dict["accountId_"]]["{}_title".format(wbResultItem_dict["contactType"])] = wbResultItem_dict["title"],
            accountDetails_dict[wbResultItem_dict["accountId_"]]["{}_phoneNumber".format(wbResultItem_dict["contactType"])] = wbResultItem_dict["phoneNumber"]
        except:
          logException("unexpected {}:[{}]".format(wbResultKey, wbResultItem_dict))
          
    elif "iss.searchCustomers" in wbResultKey:
      for wbResultItem_dict in wbResult_dict[wbResultKey]:
        try:
          if "name_" in wbResultItem_dict.keys():
            accountDetails_dict[wbResultItem_dict["accountId_"]]["accountName"] = wbResultItem_dict["name_"]
            accountDetails_dict[wbResultItem_dict["accountId_"]]["accountEmail"] = wbResultItem_dict["email_"]
            accountDetails_dict[wbResultItem_dict["accountId_"]]["createdDate"] = getDateString(wbResultItem_dict["CustomerCreationDate_"])
            accountDetails_dict[wbResultItem_dict["accountId_"]]["modifiedDate"] = getDateString(wbResultItem_dict["CustomerLastUpdateDate_"])  
        except:
          logException("unexpected {}:[{}]".format(wbResultKey, wbResultItem_dict))
          
  return accountDetails_dict
