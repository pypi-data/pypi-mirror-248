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

from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.profile import loadProfiles, listProfiles, saveProfiles
from wooju.profile import saveAccountDetails
from wooju.args import getInputs

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
    updateMsg(errorReason_list, logError("profileName(len:{:,}->{:,}):[{}] must be string and 3 characters at least".format(len(input_dict["customerDomainName"]), len(customerDomainName), customerDomainName)))
  logDebug("customerDomainName:[{}]".format(customerDomainName))
  
  if len(errorReason_list) > 0:
    return {
      "error": errorReason_list
      }
    
  profile_dict = loadProfiles(request_dict)
  if profileName != None:
    if profileName.lower() in profile_dict["__profileNames__"].keys():
      logDebug("profileName:[{}] is found".format(profileName))
    else:
      updateMsg(errorReason_list, logError("profileName:[{}] is not found".format(profileName)))
  else:
    logDebug("profileName:[{}]".format(profileName))
  
  if customerDomainName in profile_dict["DOMAINS"].keys():
    logDebug("customerDomainName:[{}] is found".format(customerDomainName))
  else:
    updateMsg(errorReason_list, logError("customerDomainName:[{}] is not found".format(customerDomainName)))
  
  if len(errorReason_list) > 0:
    return {
      "error": errorReason_list
      }
  
  
  snapshotTime = time.time()
  snapshotDate = getDateString(snapshotTime)
  
  
  for thisProfileName in profile_dict["DOMAINS"][customerDomainName]["profileNames"]:
    if thisProfileName in [profileName] or profileName in [None]:
      logDebug("thisProfileName:[{}]->profileName:[{}]".format(thisProfileName, profileName))
      
      try:
        profile_dict["__profileNames__"][thisProfileName.lower()]["domains"].remove(customerDomainName)
        updateMsg(logMessage_list, "customerDomainName:[{}] is deleted at profileName:[{}]".format(customerDomainName, thisProfileName))
      except:
        logExceptionWithValueError("type:{}:domains:[{}]".format(type(profile_dict["__profileNames__"][thisProfileName.lower()]["domains"]), profile_dict["__profileNames__"][thisProfileName.lower()]["domains"]))
      
      toBeDeletedAccountId_list = []
      for accountId in profile_dict["__profileNames__"][thisProfileName.lower()]["accountId_list"]:
        try:
          profile_dict["__accountIds__"][accountId]["profileNames"].remove(thisProfileName)
          updateMsg(logMessage_list, "profileName:[{}] is deleted at accountId:[{}]".format(thisProfileName, accountId))
        
          if len(profile_dict["__accountIds__"][accountId]["profileNames"]) == 0:
            del profile_dict["__accountIds__"][accountId]
            updateMsg(logMessage_list, "accountId:[{}] is deleted, due to no profileNames".format(accountId))
          
          toBeDeletedAccountId_list.append(accountId)
          
        except Exception as e:
          updateMsg(errorReason_list, "profileName:[{}] is not found at accountId:[{}]->Error:[{}]".format(thisProfileName, accountId, e))
      
      for accountId in toBeDeletedAccountId_list:
        profile_dict["__profileNames__"][thisProfileName.lower()]["accountId_list"].remove(accountId)
        updateMsg(logMessage_list, "accountId:[{}] is deleted from profileItem_dict".format(accountId))
      
      if len(profile_dict["__profileNames__"][thisProfileName.lower()]["accountId_list"]) == 0\
          and len(profile_dict["__profileNames__"][thisProfileName.lower()]["domains"]) == 0:
        
        fqpn = profile_dict["__profileNames__"][thisProfileName.lower()]["fqpn"]
        logDebug("fqpn:[{}]".format(fqpn))
        
        thisProfileName_dict = profile_dict
        
        thisFqpnName = ""
        if fqpn.startswith("/"):
          fqpn_list = fqpn[1:].split("/")
        else:
          fqpn_list = fqpn.split("/")
        logDebug("fqpn_list:[{}]".format(fqpn_list))
        
        for thisProfileName in fqpn_list:
          if len(thisProfileName.strip()) >= 3 and thisProfileName in thisProfileName_dict.keys():
            thisFqpnName += "/{}".format(thisProfileName)
            thisProfileName_dict = thisProfileName_dict[thisProfileName]
            logDebug("thisProfileName:[{}] is found in FQPN:[{}]:[{}]".format(thisProfileName, thisFqpnName, thisProfileName_dict.keys()))
          else:
            updateMsg(errorReason_list, "thisProfileName:[{}] is not found in FQPN:[{}]".format(thisProfileName, thisFqpnName))
        
            return {
              "error": errorReason_list
              }
        try:
          if len(thisProfileName_dict.keys()) == 0:
            updateMsg(logMessage_list, "thisFqpnName:[{}] is deleted due to thisProfileName_dict.keys():[{}]".format(thisProfileName, thisFqpnName, thisProfileName_dict.keys()))
            del thisProfileName_dict
            
            try:
              del profile_dict["__profileNames__"][thisProfileName.lower()]
              updateMsg(logMessage_list, "profileName:[{}] is not deleted at profiles".format(thisProfileName))
            
            except:
              updateMsg(errorReason_list, logException("profileName:[{}] is not deleted at profiles->Error:[{}]".format(thisProfileName, e)))
          
          else:
            logDebug("thisFqpnName:[{}]->thisProfileName_dict.keys():[{}]".format(thisFqpnName, thisProfileName_dict.keys()))
        
        except Exception as e:
          updateMsg(errorReason_list, logException("profileName:[{}] is not deleted at fqpn:[{}] ->Error:[{}]".format(thisProfileName, fqpn, e)))
      #end if len(profile_dict["__profileNames__"][thisProfileName.lower()]["domains"]) == 0:
                
    else:
      logDebug("thisProfileName:[{}] is not requested".format(thisProfileName))
    
    try:
      profile_dict["DOMAINS"][customerDomainName]["profileNames"].remove(thisProfileName)
      updateMsg(logMessage_list, "thisProfileName:[{}] is removed".format(thisProfileName))
    except:
      updateMsg(errorReason_list, logException("thisProfileName:[{}] can't be removed from profileNames:[{}]".format(thisProfileName, profile_dict["DOMAINS"][customerDomainName]["profileNames"])))
    #end if thisProfileName in [profileName] or profileName in [None]:
  #end for thisProfileName in profile_dict["DOMAINS"][customerDomainName]["profileNames"]:
  
  if len(profile_dict["DOMAINS"][customerDomainName]["profileNames"]) == 0:
    del profile_dict["DOMAINS"][customerDomainName]
    updateMsg(logMessage_list, "customerDomaiNam:[{}] is deleted at DOMAINS".format(customerDomainName))  
    
  if len(logMessage_list) > 0:
    saveProfiles(request_dict, profile_dict)
    saveAccountDetails(request_dict, accountDetails_dict=profile_dict["__accountIds__"])
  
  return {
    **listProfiles(request_dict),
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }