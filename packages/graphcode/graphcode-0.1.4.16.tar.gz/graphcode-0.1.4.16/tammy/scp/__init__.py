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

from pathway import requests

from wooju.lib import saveCache, loadCache

from tammy.ldap import PdxLdap

def getESAccountInfoDetails_dict(request_dict):
  try:
    request_dict["apiName"] = "tammy.scp.describeESCustomers"
    esAccountInfo_dict = loadCache(request_dict, name="esAccountInfoDetailsV2_dict")
    esCustomerInfo_dict = loadCache(request_dict, name="esCustomerInfo_dict")
  except:
    pdxLdap = PdxLdap()
    
    request_dict["attributes"]["cache"] = ["esAccountIds", "esCustomers"]
    response_dict = requests(
      request_dict = {
          **request_dict,
          "apiName":"tammy.scp.discoverESCustomers"
        }
      ) 
    
    esAccountId_list = response_dict["response"]["esAccountIds"]
    esCustomer_list = response_dict["response"]["esCustomers"]
        
    esAccountInfo_dict = {}
    for esAccountIdItem_dict in esAccountId_list:
      esAccountInfo_dict[esAccountIdItem_dict["accountId"]] = {
        "name":esAccountIdItem_dict["name"],
        "email":esAccountIdItem_dict["email"],
        "status":esAccountIdItem_dict["status"],
        "domainIds": esAccountIdItem_dict["domainIds"]
        }
      
    esCustomerInfo_dict = {}
    for esCustomerItem_dict in esCustomer_list:
      try:
        region = esCustomerItem_dict["region"]
      except:
        region = None
      
      try:
        area = esCustomerItem_dict["area"]
      except:
        area = None
        
      try:
        domainId = esCustomerItem_dict["primaryWebDomain"].lower()
      except:
        domainId = None
      try:
        name = esCustomerItem_dict["name"]
      except:
        name = None
        
      try:
        secondaryWebDomains = esCustomerItem_dict["secondaryWebDomains"]
      except:
        secondaryWebDomains = None
        
      try:
        primaryTAM = esCustomerItem_dict["ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY"]
      except:
        try:
          primaryTAM = esCustomerItem_dict["ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY"]
        except:
          primaryTAM = None
        
      try:
        if isinstance(esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"], list):
          if len(esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"]) == 1:
            ESM = esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"][0]
            esLeaders = []
            reportLine_dict = pdxLdap.getReportingLineAlias(loginAliasId=ESM)
            for level in ["5", "6", "7", "8", "10"]:
              if level in reportLine_dict.keys():
                for aliasId in reportLine_dict[level]:
                  if aliasId in esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"]:
                    continue
                  esLeaders.append(aliasId)
                  if aliasId in ["jfariss", "kooncej"]:
                    break
                
                if aliasId in ["jfariss", "kooncej"]:
                  break
          else:
            ESM = esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"]
            esLeaders = []
            reportLine_dict = pdxLdap.getDirectReportAliases(loginAliasId=ESM[0])
            for level in ["5", "6", "7", "8", "10"]:
              if level in reportLine_dict.keys():
                for aliasId in reportLine_dict[level]:
                  if aliasId in esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"]:
                      continue
                  esLeaders.append(aliasId)
                  
                  if aliasId in ["jfariss", "kooncej"]:
                    break
                
                if aliasId in ["jfariss", "kooncej"]:
                  break
        else:
          try:
            ESM = pdxLdap.getManagerAliasId(loginAliasId=primaryTAM[0])
            esLeaders = []
            reportLine_dict = pdxLdap.getDirectReportAliases(loginAliasId=ESM[0])
            for level in ["5", "6", "7", "8", "10"]:
              if level in reportLine_dict.keys():
                for aliasId in reportLine_dict[level]:
                  if aliasId in [ESM]:
                      continue
                  esLeaders.append(aliasId)
                  
                  if aliasId in ["jfariss", "kooncej"]:
                    break
                
                if aliasId in ["jfariss", "kooncej"]:
                  break
          except:
            ESM = esCustomerItem_dict["ENTERPRISE_SUPPORT_MANAGER"]
            try:
              esLeaders = esCustomerItem_dict["ENTERPRISE_SUPPORT_LEADERSHIP"]
            except:
              esLeaders = None
      except:
        ESM = None
        esLeaders = None
        
      try:
        AM = esCustomerItem_dict["ACCOUNT_MANAGER"]
        try:
          for aliasId in esCustomerItem_dict["ACCOUNT_MANAGER_PRIMARY"]:
            AM.append(aliasId)
        except:
          pass
      except:
        try:
          AM = esCustomerItem_dict["ACCOUNT_MANAGER_PRIMARY"]
        except:
          AM = None

      try:
        SA = esCustomerItem_dict["SOLUTIONS_ARCHITECT"]
        try:
          for aliasId in esCustomerItem_dict["SOLUTIONS_ARCHITECT_PRIMARY"]:
            SA.append(aliasId)
        except:
          pass
      except:
        try:
          SA = esCustomerItem_dict["SOLUTIONS_ARCHITECT_PRIMARY"]
        except:
          SA = None

        
      try:
        tamAlias = esCustomerItem_dict["accountTAMsMail"]
      except:
        tamAlias = None
        
          
      try:
        esCustomerInfo_dict[domainId] = {
          "region":region,
          "area":area,
          "domainId":domainId,
          "name":name,
          "primaryTAM":primaryTAM,
          "ESM":ESM,
          "esLeaders":esLeaders,
          "AM":AM,
          "SA":SA,
          "tamAlias":tamAlias
          }
        
        for key in esCustomerInfo_dict[domainId].keys():
          if isinstance(esCustomerInfo_dict[domainId][key], list):
            thisValue = ""
            for value in esCustomerInfo_dict[domainId][key]:
              if len(value.strip()) > 0:
                if thisValue == "":
                  thisValue += value
                else:
                  thisValue += ";{}".format(value)
            
            esCustomerInfo_dict[domainId][key] = thisValue
                
        if isinstance(secondaryWebDomains, list):
          for secondDomainId in secondaryWebDomains:
            esCustomerInfo_dict[secondDomainId.lower()] = esCustomerInfo_dict[domainId]
      except:
        logException("unexpected esCustomerItem_dict[{}]:[{}]".format(esCustomerItem_dict["primaryWebDomain"], esCustomerItem_dict))
     
    try:
      for accountId in esAccountInfo_dict.keys():
        for thisDomainId in esAccountInfo_dict[accountId]["domainIds"]:
          if "amazon" in thisDomainId.lower().split("."):
            continue
          
          try:
            esAccountInfo_dict[accountId] = {
              "domainId":thisDomainId.lower(),
              "name":esAccountInfo_dict[accountId]["name"],
              "email":esAccountInfo_dict[accountId]["email"],
              "status":esAccountInfo_dict[accountId]["status"],
              **esCustomerInfo_dict[thisDomainId.lower()]
              }
            break
          except:
            logException("unexpected esAccountInfo_dict[{}]:[{}]".format(accountId, esAccountInfo_dict[accountId]))
    except:
      logException("failed to load ESCustomerInfo")
    
    saveCache(request_dict, name="esAccountInfoDetailsV2_dict", value=esAccountInfo_dict, ttl_s=86400*30)
    saveCache(request_dict, name="esCustomerInfo_dict", value=esCustomerInfo_dict, ttl_s=86400*30)
    
  return esAccountInfo_dict, esCustomerInfo_dict
  
def getESAccountIdDetails(request_dict):
  try:
    request_dict["apiName"] = "tammy.scp.describeESCustomers"
    esAccountIdDetails_dict = loadCache(request_dict, name="esAccountIdDetails_dict")
  except:
    esAccountIdDetails_dict = {}
    
    request_dict["attributes"]["serviceNames"]=["esDomainIds", "esAccountIds"]
    response_dict = requests(
      request_dict = {
          **request_dict,
          "apiName":"tammy.scp.describeESCustomers"
        }
      )
    
    try:
      esDomainId_list = response_dict["response"]["esDomainIds"]
      esAccountId_list = response_dict["response"]["esAccountIds"]
      esNAccountId_list = []
      
      duplicatedAccountCount = 0
      itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=esDomainId_list, divider=3)
      for esDomainIdItem_dict in esDomainId_list:
        itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, esDomainIdItem_dict, itemName="esDomainIdItem_dict")
        
        if isinstance(esDomainIdItem_dict["accountIds"], list):
          for accountId in esDomainIdItem_dict["accountIds"]:
            if accountId in esAccountIdDetails_dict.keys():
              duplicatedAccountCount += 1
            else:
              esAccountIdDetails_dict[accountId] = esDomainIdItem_dict
        
        del esDomainIdItem_dict["accountIds"]
      logWarn("total {:,} accountIds are duplicated".format(duplicatedAccountCount))
      
      itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=esAccountId_list, divider=3)
      for esAccountIdItem_dict in esAccountId_list:
        itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, esAccountIdItem_dict, itemName="esAccountIdItem_dict")
        
        try:
          esAccountIdDetails_dict[esAccountIdItem_dict["accountId"]] = {
            **esAccountIdDetails_dict[esAccountIdItem_dict["accountId"]],
            **esAccountIdItem_dict
            }
        except:
          esNAccountId_list.append(esAccountIdItem_dict)
        
      logWarn("total {:,} accountIds are duplicated".format(duplicatedAccountCount))
      
    except:
      if "response" in response_dict.keys():
        logException("unexpected response_dict['response'].keys():[{}]".format(response_dict["response"].keys()))
      else:
        logException("unexpected response_dict.keys():[{}]".format(response_dict.keys())) 
      
    saveCache(request_dict, name="esAccountIdDetails_dict", value=esAccountIdDetails_dict, ttl_s=86400*30)
  
  return esAccountIdDetails_dict
    