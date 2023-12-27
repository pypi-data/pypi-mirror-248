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

from tammy.ldap import PdxLdap
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
  
  logDebug("attributes:[{}]".format(request_dict["attributes"]))
  
  try:
    if "refresh" in request_dict["attributes"].keys() and request_dict["attributes"]["refresh"]:
      raiseValueError("refreshing")
    
    esCustomer_dict = {}
    if "cache" in request_dict["attributes"].keys():
      for key in request_dict["attributes"]["cache"]:
        esCustomer_dict[key] = loadCache(request_dict, name="esCustomer_{}_list".format(key))
      
      return esCustomer_dict
    
    else:
      for key in ["esUsers", "esDomainIds", "esCustomers", "esAccounts", "esAccountIds"]:
        esCustomer_dict[key] = loadCache(request_dict, name="esCustomer_{}_list".format(key))
      
  except:
    esCustomer_dict = updateESCustomer(request_dict, errorReason_list, logMessage_list)
    for key in esCustomer_dict.keys():
      logDebug("writing {}....".format("esCustomer_{}_list".format(key)))
      saveCache(request_dict, name="esCustomer_{}_list".format(key), value=esCustomer_dict[key], ttl_s=3600*24*30)

  index_list = saveResourceDetailsWithIndex_dict(request_dict, resourceDetails_dict=esCustomer_dict)
  
  revision_dict={
    "date": getDateString("now", "date"),
    "state":request_dict["apiName"].split(".")[-1],
    }
    
  revision_list = updateRevision_list(
    request_dict,
    revision_dict
    )
    
  return {
    ".index": index_list,
    ".revision": revision_list,
    **esCustomer_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
  

def updateESCustomer(request_dict, errorReason_list, logMessage_list):
  try:
    esCustomerDetails_dict = loadCache(request_dict, name="esCustomerDetails_dict")
  except:
    esCustomerDetails_dict = getESCustomers(request_dict, 3600*24*30, errorReason_list, logMessage_list)
    saveCache(request_dict, name="esCustomerDetails_dict", value=esCustomerDetails_dict, ttl_s=3600*24*30)

  idMap_dict = esCustomerDetails_dict["idMap_dict"]
  #idDomainMap_dict = esCustomerDetails_dict["idDomainMap_dict"]
  esUser_dict = esCustomerDetails_dict["esUser_dict"]
  esCustomer_dict = esCustomerDetails_dict["esCustomer_dict"]
  esAccountId_dict = esCustomerDetails_dict["esAccountId_dict"]
  
  
  esDomainIds_dict = {}
  esUser_list = []
  for userAliasId in esUser_dict.keys():
    if isinstance(esUser_dict[userAliasId], dict):
      for key in esUser_dict[userAliasId].keys():
        if isinstance(esUser_dict[userAliasId][key], list) and len(esUser_dict[userAliasId][key]) == 0:
          esUser_dict[userAliasId][key] =  None
          
    esUser_list.append(
      {
        "tamAlias": userAliasId,
        **esUser_dict[userAliasId]
        }
      )
    
    for role in esUser_dict[userAliasId].keys():
      if role in ["ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY","ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY", "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME", "ENTERPRISE_SUPPORT_MANAGER"] and isinstance(esUser_dict[userAliasId][role], list):
        for domainId in esUser_dict[userAliasId][role]:
          if domainId in esDomainIds_dict.keys():
            if role in esDomainIds_dict[domainId].keys():
              esDomainIds_dict[domainId][role].append(userAliasId)
            else:
              esDomainIds_dict[domainId][role] = [userAliasId]
          else:
            esDomainIds_dict[domainId] = {}
            esDomainIds_dict[domainId][role] = [userAliasId]
          
    
  esCustomer_list = []
  for domainId in esCustomer_dict.keys():
    #logDebug("#domainId:[{}]".format(domainId))
    if "region" not in esCustomer_dict[domainId].keys() and isinstance(esCustomer_dict[domainId]["parentHierarchy"], str):
      try:
        for thisId in esCustomer_dict[domainId]["parentHierarchy"].split(":"):
          try:
            esCustomer_dict[domainId] = {
              **idMap_dict[thisId],
              **esCustomer_dict[domainId]
              }
            break
          except:
            logException("unexpected thisId:[{}]".format(thisId))
      except:
        logException("unexpected customerItem_dict:[{}]".format(esCustomer_dict[domainId]))
    
    try:
      esCustomer_dict[domainId]["accountIdCount"] = len(esAccountId_dict[domainId])
    except:
      logWarn("domainId:[{}] not found at esAccountId_dict".format(domainId))
      
    esCustomer_list.append(esCustomer_dict[domainId])
  
  esAccountIds_dict = {}
  esAccountId_list = []
  inActiveAccountId_list = []
  duplicatedAccountIdCount = 0
  
  itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=esAccountId_dict.keys(), divider=3)
  for domainId in esAccountId_dict.keys():
    try:
      itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, esAccountId_dict[domainId][-1], itemName="domainId")
    except:
      itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, esAccountId_dict[domainId], itemName="domainId")
    
    for esAccountIdItem_dict in esAccountId_dict[domainId]:
      esAccountId_list.append(esAccountIdItem_dict)
      
      if esAccountIdItem_dict["status"] in ["Active"]:
        if esAccountIdItem_dict["accountId"] in esAccountIds_dict.keys():
          duplicatedAccountIdCount += 1
          
          if domainId not in esAccountIds_dict[esAccountIdItem_dict["accountId"]]["domainIds"]:
            esAccountIds_dict[esAccountIdItem_dict["accountId"]]["domainIds"].append(domainId)
            esAccountIds_dict[esAccountIdItem_dict["accountId"]]["domainIdCount"] += 1
            
        else:
          
          esAccountIds_dict[esAccountIdItem_dict["accountId"]] = {
            "accountId":esAccountIdItem_dict["accountId"],
            "name":esAccountIdItem_dict["name"],
            "email":esAccountIdItem_dict["email"],
            "role":esAccountIdItem_dict["role"],
            "status":esAccountIdItem_dict["status"],
            "supportLevel":esAccountIdItem_dict["supportLevel"],
            "payerId":esAccountIdItem_dict["payerId"],
            "domainIdCount": 1,
            "domainIds":[domainId]
            }
             
      else:
        inActiveAccountId_list.append(esAccountIdItem_dict)
  
  esUserACL_list = []
  esAccountIds_list = []
  for accountId in esAccountIds_dict.keys():
    esAccountIds_list.append(esAccountIds_dict[accountId])
  
  esDomainIds_list = []
  for domainId in esDomainIds_dict.keys():
    try:
      primaryTAM = esDomainIds_dict[domainId]["ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY"]
      
      if "cdo-plus-tams-oncall" in primaryTAM:
        continue
    except:
      primaryTAM = None
    
    try:
      secondaryTAM = esDomainIds_dict[domainId]["ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY"]
      
      if "cdo-plus-tams-oncall" in secondaryTAM:
        continue
    except:
      secondaryTAM = None

    try:
      nightTimeTAM = esDomainIds_dict[domainId]["ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME"]
      
      if "cdo-plus-tams-oncall" in nightTimeTAM:
        continue
    except:
      nightTimeTAM = None

    try:
      sa_list = esDomainIds_dict[domainId]["SOLUTIONS_ARCHITECT_PRIMARY"]
      try:
        for saAlias in esDomainIds_dict[domainId]["SOLUTIONS_ARCHITECT"]:
          sa_list.append(saAlias)
      except:
        logWarn("")
    except:
      try:
        sa_list = esDomainIds_dict[domainId]["SOLUTIONS_ARCHITECT"]
      except:
        sa_list = None

    try:
      am_list = esDomainIds_dict[domainId]["ACCOUNT_MANAGER_PRIMARY"]
      try:
        for amAlias in esDomainIds_dict[domainId]["ACCOUNT_MANAGER"]:
          am_list.append(saAlias)
      except:
        logWarn("")
    except:
      try:
        am_list = esDomainIds_dict[domainId]["ACCOUNT_MANAGER"]
      except:
        am_list = None

    try:
      esm = esDomainIds_dict[domainId]["ENTERPRISE_SUPPORT_MANAGER"]
    except:
      esm = None
      
    try:
      region = esCustomer_dict[domainId]["region"]
    except:
      region = None
      
    try:
      area = esCustomer_dict[domainId]["area"]
    except:
      area = None
      
    try:
      accountCount = len(esAccountId_dict[domainId])
      try:
        accountId_list = []
        for esAccountIdItem_dict in esAccountId_dict[domainId]:
          accountId_list.append(esAccountIdItem_dict["accountId"])
      except:
        accountId_list = None
    except:
      accountCount = None
      accountId_list = None
    
    
    esDomainIds_list.append(
      {
        "region": region,
        "area": area,
        "domainId": domainId,
        "primaryTAM": primaryTAM,
        "secondaryTAM": secondaryTAM,
        "nightTimeTAM": nightTimeTAM,
        "ESM": esm,
        "AM": am_list,
        "SA": sa_list,
        "accountCount": accountCount,
        "accountIds": accountId_list
        }
      )
    
    for roleName in ["primaryTAM", "secondaryTAM", "nightTimeTAM", "ESM", "AM", "SA"]:
      if isinstance(esDomainIds_list[-1][roleName], list):
        for alisId in esDomainIds_list[-1][roleName]:
          if alisId not in esUser_list:
            esUserACL_list.append(
              {
                "username": alisId,
                "primarywebdomain": esDomainIds_list[-1]["domainId"]
                }
              )
  
  return {
    "esUsers": esUser_list,
    "usUserACL": esUserACL_list,
    "esDomainIds":esDomainIds_list,
    "esCustomers": esCustomer_list,
    "esAccounts": esAccountId_list,
    "esAccountIds": esAccountIds_list
    }
  
def getESCustomers(request_dict, ttl_s, errorReason_list, logMessage_list):
  
  try:
    userName_list = loadCache(request_dict, name="userName_list")
  except:
    try:
      managerAliasId = request_dict["attributes"]["managerAliasId"]
    except:
      managerAliasId = "jfariss"
      logException("managerAliasId not found ")
      
    userName_list = lookupSecondDirects(loginAliasId = managerAliasId)
    saveCache(request_dict=request_dict, name="userName_list", value=userName_list, ttl_s=ttl_s)
  
  thisRequest_list = []
  for userName in userName_list:
                
    thisRequest_list.append(
      {
        "accountId": "000000000000",
        "regionCode": "us-east-1",
        "apiList":[
          {
            "platform":"k2",
            "apiName":"kumoscp.searchCustomers", 
            "args": "{\"searchFilter\":\"EMAIL\",\"searchFilterValue\":\"" + userName + "\",\"requestedBy\":\""+ request_dict["metadata"]["userName"]+"@\"}",
            "inputs":"",
            "conditions":"",
             "limit":"",
             "pt":"4x6"
            },
          {
            "platform":"k2",
            "apiName":"kumoscp.getCustomerAccountFullList",
            "args":"{\"id\":\"${__id__}\"}",
            "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=accountId:000000000000,regionCode:us-east-1,id:id",
            "conditions":"",
            "limit":"",
            "pt":"8x8"
            },
          ]
        }
      )
  
  wbResult_dict = cacheWbRun(request_dict, request_list=thisRequest_list, apiList=None, ttl_s=ttl_s)
  
  idMap_dict = {}
  idDomainMap_dict = {}
  deprecatedDomainId_dict = {}
  esUser_dict = {}
  esCustomer_dict = {}
  esAccountId_dict = {}
  unexpectCustomers_list = []
  for wbIndexKey in wbResult_dict.keys():
    if isinstance(wbResult_dict[wbIndexKey], list) == False:
      logDebug("{}:wbResult_dict[{}] is ignored......".format(type(wbResult_dict[wbIndexKey]).__name__, wbIndexKey))
      continue
    
    try:
      itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=wbResult_dict[wbIndexKey], divider=3)
    except:
      logException("unable to get the delimiter at wbIndexKey:[{}]".format(wbIndexKey))
      itemCount = 0
      totalNumber = len(wbResult_dict[wbIndexKey])
      percentageDelimiter = 1
      
    if "searchCustomers" in wbIndexKey:
      for customerItem_dict in wbResult_dict[wbIndexKey]:
        itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, customerItem_dict, itemName=wbIndexKey)
        
        try:
          loweredDomainId = customerItem_dict["primaryWebDomain"].lower()
        except:
          logException("unexpected customerItem_dict:[{}]".format(customerItem_dict))
          continue
        
        try:
          if loweredDomainId in customerItem_dict.keys():
            logWarn("primaryDomain:[{}] is already updated".format(customerItem_dict["primaryWebDomain"]))
          idDomainMap_dict[customerItem_dict["id"]] = customerItem_dict["primaryWebDomain"]
          
          isIgnoredDomainId = False
          if loweredDomainId in ["www.non-customer-facing-allocation.com", "www.90daytams.com", "openmbr.tambuilders"]:
            logWarn("ignored domainId:[{}]".format(loweredDomainId))
            isIgnoredDomainId = True
          
          elif "kumoesa" in loweredDomainId.split("."):
            logWarn("ignored domainId:[{}]".format(loweredDomainId))
            isIgnoredDomainId = True
            
          elif "amazon" in loweredDomainId.split("."):
            logWarn("ignored domainId:[{}]".format(loweredDomainId))
            isIgnoredDomainId = True
          
        except:
          logException("unexpected customerItem_dict:[{}]".format(customerItem_dict))
          continue
           
        try:
          try:
            if isinstance(customerItem_dict["supportLocations"], list) and len(customerItem_dict["supportLocations"]) > 0:
              for supportLocationItem_dict in customerItem_dict["supportLocations"]:
                if supportLocationItem_dict["region"] in ["DEPRECATED"]:
                  continue
                else:
                  customerItem_dict = {
                    "region":supportLocationItem_dict["region"],
                    "area":supportLocationItem_dict["name"],
                    **customerItem_dict
                    }
                  if len(customerItem_dict["region"].strip()) > 0:
                    idMap_dict[customerItem_dict["id"]] = {
                      "region":customerItem_dict["region"],
                      "area":customerItem_dict["name"]
                      }
                    
                    if isinstance(customerItem_dict["parentHierarchy"], str):
                      for thisId in customerItem_dict["parentHierarchy"].split(":"):
                        try:
                          if thisId not in idMap_dict.keys():
                            idMap_dict[thisId] = {
                              "region":customerItem_dict["region"],
                              "area":customerItem_dict["name"]
                              }
                        except:
                          logException('unexpected supportLocations or supportLocations not found')
                  
                  break
              
              if supportLocationItem_dict["region"] in ["DEPRECATED"]:
                deprecatedDomainId_dict[loweredDomainId] = "DEPRECATED"
                       
          except:
            try:
              logException('unexpected supportLocations:[{}]'.format(customerItem_dict["supportLocations"]))
            except:
              logException("supportLocations not found")
          
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
            
            if role in ["ENTERPRISE_SUPPORT_MANAGER", "ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY", "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY", "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME"]:
                
              if isIgnoredDomainId:
                if email in esUser_dict.keys():
                  if role in esUser_dict[email].keys():
                    if loweredDomainId not in esUser_dict[email]["OTHERS"]:
                      esUser_dict[email]["OTHERS"].append(loweredDomainId)
                  else:
                    esUser_dict[email]["OTHERS"].append(loweredDomainId)
                else:
                  esUser_dict[email] = {
                    "region":customerItem_dict["region"],
                    "area":customerItem_dict["area"],
                    "ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY":[], 
                    "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY":[], 
                    "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME":[], 
                    "OTHERS":[], 
                    "ENTERPRISE_SUPPORT_MANAGER":[]
                    }
                  esUser_dict[email]["OTHERS"].append(loweredDomainId)
              else:
                if email in esUser_dict.keys():
                  if role in esUser_dict[email].keys():
                    if loweredDomainId not in esUser_dict[email][role]:
                      esUser_dict[email][role].append(loweredDomainId)
                  else:
                    esUser_dict[email][role].append(loweredDomainId)
                else:
                  try:
                    esUser_dict[email] = {
                      "region":customerItem_dict["region"],
                      "area":customerItem_dict["area"],
                      "ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY":[], 
                      "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY":[], 
                      "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME":[], 
                      "OTHERS":[], 
                      "ENTERPRISE_SUPPORT_MANAGER":[]
                      }
                  except:
                    esUser_dict[email] = {
                      "region":None,
                      "area":None,
                      "ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY":[], 
                      "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY":[], 
                      "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME":[], 
                      "OTHERS":[], 
                      "ENTERPRISE_SUPPORT_MANAGER":[]
                      }
                    unexpectCustomers_list.append(customerItem_dict)
                    
                  esUser_dict[email][role].append(loweredDomainId)
                           
          
          del customerItem_dict["teamMembers"]
            
        except:
          logException('teamMembers not found, unexpected customerItem_dict:[{}]'.format(customerItem_dict))
          continue
        
        try:
          del customerItem_dict["serviceName_"]
        except:
          logError('serviceName_ not found')
      
        try:
          del customerItem_dict["apiName_"]
        except:
          logError('apiName_ not found')
          
        try:
          del customerItem_dict["searchFilter_"]
        except:
          logError('searchFilter_ not found')
        try:
          del customerItem_dict["requestedBy_"]
        except:
          logError('requestedBy_ not found')
        try:
          del customerItem_dict["searchFilterValue_"]
        except:
          logError('requestedBy_ not found')
          
        esCustomer_dict[loweredDomainId] = customerItem_dict
        #logDebug("#customerItem_dict:[{}]".format(customerItem_dict))
    elif "getCustomerAccountFullList" in wbIndexKey:
      
      for customerItem_dict in wbResult_dict[wbIndexKey]:
        try:
          customerItem_dict["primaryWebDomain"] = idDomainMap_dict[customerItem_dict["id_"]]
          loweredDomainId = customerItem_dict["primaryWebDomain"].lower()
          
          if loweredDomainId in deprecatedDomainId_dict.keys():
            #logWarn("domainId:[{}] is deprecated".format(loweredDomainId))
            continue
                                                                                
        except:
          logException("unexpected customerItem_dict:[{}]".format(customerItem_dict))
          continue
        
        itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, customerItem_dict, itemName=wbIndexKey)
        
        if loweredDomainId in esAccountId_dict.keys():
          esAccountId_dict[loweredDomainId].append(customerItem_dict)
        else:
          esAccountId_dict[loweredDomainId] = [customerItem_dict]
          
        try:
          del customerItem_dict["serviceName_"]
        except:
          logError('serviceName_ not found')
        try:
          del customerItem_dict["apiName_"]
        except:
          logError('apiName_ not found')
        try:
          del customerItem_dict["id_"]
        except:
          logError('id_ not found')
        try:
          del customerItem_dict["merchantId"]
        except:
          logError('merchantId not found')
          
  return {
    "idMap_dict": idMap_dict,
    #"idDomainMap_dict": idDomainMap_dict,
    "esUser_dict": esUser_dict,
    "esCustomer_dict": esCustomer_dict,
    "esAccountId_dict": esAccountId_dict,
    "unexpectESCustomers": unexpectCustomers_list
    }
  
def lookupSecondDirects(loginAliasId):
  
  pdxLdap = PdxLdap()
  ldapAliasInfo_dict = pdxLdap.queryLDAPWithLoginID(loginAliasId)
  logDebug("ldapAliasInfo_dict:[{}]".format(ldapAliasInfo_dict))
  
  secondDirectAliasId_list = []
  directAliasId_list = pdxLdap.getDirectReportAliases(loginAliasId)
  for directAliasId in directAliasId_list:
    logDebug("aliadId:[{}]".format(directAliasId))
    for secondDirectAliasId in pdxLdap.getDirectReportAliases(directAliasId):
      secondDirectAliasId_list.append(secondDirectAliasId)
  
  secondAliasIdCount = 0
  for secondAliasId in secondDirectAliasId_list:
    secondAliasIdCount += 1
    logDebug("(#{:,})\tsecondAliasId:[{}]".format(secondAliasIdCount, secondAliasId))
    
  return secondDirectAliasId_list
  
    
  
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
    
    for key in customerItem_dict.keys():
      logDebug("customerItem_dict:{}:[{}]".format(key, customerItem_dict[key]))

def localUnitTest():
  unitTestFunction_dict = {"getCustoerList":{"target":getCustoerList, "args":()},
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()