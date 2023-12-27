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

from graphcode.unittest import unitTest

import subprocess

import time
import json

class PdxLdap():
  def __init__(self):
    self.ldapGroup_dict = {}
    self.ldapDictionaryWithAliasId = {}
    self.ldapReportingLine_dict = {}

  def getLDAPUsersWithLdapGroupName(self, ldapGroupName):
    if ldapGroupName == "" or ldapGroupName == None:
      return []
    
    # TIMEOUT: 3 seconds
    # HOST: ldap.amazon.com 
    cmd = '/usr/bin/ldapsearch -x -H ldap://ldap.amazon.com:389 -b "ou=Groups,o=amazon.com" -s sub -a always -z 1000 "(&(cn={}))" "memberuid"'.format(ldapGroupName)
    
    ## run it ##
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    ldapOutpuLines_list = p.stdout.readlines()
    
    user_list = []
    for ldapItem_line in ldapOutpuLines_list:
      decodedLdapItem_line = ldapItem_line.decode('utf-8').replace("\n","").replace("\r","")
      if decodedLdapItem_line.startswith("memberuid:"):
        user_list.append(decodedLdapItem_line.split(" ")[1])
    
    try:
      logDebug("ldapGroup:[{}]->users:[len:{:,}]".format(ldapGroupName, len(user_list)))
    except:
      logException("unexpected ldapGroupName:[{}], user_list:[{}]".format(ldapGroupName, user_list))
    
    self.ldapGroup_dict[ldapGroupName] = {"members": user_list, "latestUpdateTime": time.time()}
    
    return user_list
  
  def isMemberOfLdapGroup(self, ldapGroupName, loginAliasId):
    if ldapGroupName in self.ldapGroup_dict.keys() and loginAliasId in self.ldapGroup_dict[ldapGroupName]["members"] and (time.time()-self.ldapGroup_dict[ldapGroupName]["latestUpdateTime"]) < 900:
      logDebug("{}@ is a member of ldapGroupName:[{}] (cacheTimeout:{:.2f}s)".format(loginAliasId, ldapGroupName, 900 - (time.time()-self.ldapGroup_dict[ldapGroupName]["latestUpdateTime"])))
      return True
    
    elif loginAliasId in self.getLDAPUsersWithLdapGroupName(ldapGroupName):
      return True
    
    else:
      return False
  
  def queryLDAPWithLoginID(self, loginAliasId):
    if loginAliasId == "" or loginAliasId == None:
      return {}  
    
    elif loginAliasId in self.ldapDictionaryWithAliasId.keys() and len(self.ldapDictionaryWithAliasId[loginAliasId].keys()) > 1:
      return self.ldapDictionaryWithAliasId[loginAliasId]
    
    # TIMEOUT: 3 seconds
    # HOST: ldap.amazon.com 
    cmd = '/usr/bin/ldapsearch -l 3 -t -H ldap://ldap.amazon.com -x -b "o=amazon.com" -s sub "uid=' + loginAliasId + '" 2> /dev/null'
    
    ## run it ##
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    ldapOutpuLines_list = p.stdout.readlines()
    
    if len(ldapOutpuLines_list) < 2:
      # check error for the LDAP output
      retryCount = 0
      
      while retryCount < 3:
        retryCount += 1
        logError("retrying #{} loginAliasId:[{}] to get the output from LDAP->cmd:[{}].".format(retryCount, loginAliasId, cmd))
        
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        try:
          ldapOutpuLines_list = p.stdout.readlines()
        except Exception as e:
          errorMessage = "Error:[{}] -> unable to read ldapsearch".format(e)
          logError( errorMessage)
        
        if len(ldapOutpuLines_list) >= 2:
          break
    
      if retryCount >= 3:
        logError("failed loginAliasId:[{}] of getting the output from LDAP->cmd:[{}]".format(loginAliasId, cmd))
    
    logDebug("ldapOutpuLines_list:[{}]".format(ldapOutpuLines_list))
    
    ldapAliasInfo_dict = {}
    
    attributeName = ""
    attributeValue = ""
    sshpublickeyCount = 0
    for ldapOutpuLine in ldapOutpuLines_list:
      ldapTextLine = ldapOutpuLine.decode('utf-8').replace("\n","").replace("\r","")
      
      if len(ldapOutpuLine) == 0:
        logDebug("ldapTextLine:[{}]".format(ldapTextLine))
        continue
      else:
        commentPosition = ldapTextLine.find("#")
        spacePosition = ldapTextLine.find(" ")
        delimerPosition = ldapTextLine.find(":")
        #logDebug("[{}:{}:{}] ldapTextLine:[{}]".format(commentPosition, spacePosition, delimerPosition, ldapTextLine))
      
      if commentPosition == 0:
        #logDebug("line:[{}] will be ignored as it's commented.".format(ldapTextLine))
        continue
      elif spacePosition == 0:
        if attributeName != "" and ldapAliasInfo_dict[attributeName] != "":
          if "sshpublickey" in attributeName :
            attributeValue = "{}{}".format(ldapAliasInfo_dict[attributeName], ldapTextLine[1:])
            ldapAliasInfo_dict[attributeName] = attributeValue
          if attributeName == "dn":
            for subAttributeItems in ldapAliasInfo_dict[attributeName]:
              for subAttributeItemKey in subAttributeItems.keys():
                if subAttributeItemKey == "o":
                  subAttributeItems[subAttributeItemKey] = "{}{}".format(subAttributeItems[subAttributeItemKey],ldapTextLine[1:])
          
      elif delimerPosition > 1:
        attributeName = ldapTextLine[:delimerPosition]
  
        if attributeName == "sshpublickey":
          attributeName = "{}_{}".format(ldapTextLine[:delimerPosition], sshpublickeyCount)
          sshpublickeyCount += 1
        
        if ldapTextLine[delimerPosition+1] != " ":
          attributeValue = ldapTextLine[delimerPosition+1:]
        else:
          attributeValue = ldapTextLine[delimerPosition+2:]
   
        if "=" in attributeValue:
          subAttribute_list = []
          for subAttributeItem in attributeValue.split(","):
            subAttributeName = subAttributeItem[:subAttributeItem.find("=")]
            subAttributeValue = subAttributeItem[subAttributeItem.find("=")+1:]
  
            subAttribute_list.append({subAttributeName: subAttributeValue})
          
          if attributeName != "":
            logDebug("attributeName:[{}] -> [{}]".format(attributeName, subAttribute_list))
          
          if attributeName == "amznmanageremployees":
            if attributeName in ldapAliasInfo_dict.keys():
              ldapAliasInfo_dict[attributeName].append(subAttribute_list)
            else:
              ldapAliasInfo_dict[attributeName] = [subAttribute_list]
          else:
            ldapAliasInfo_dict[attributeName] = subAttribute_list
            
        else:
          
          ldapAliasInfo_dict[attributeName] = attributeValue
        
          
    #logMessage("TRACE","(#{:>9,}) loginAliasId:[{}] -> ldapAttributes:[{}]".format(len(self.ldapDictionaryWithAliasId.keys()), loginAliasId, ldapAliasInfo_dict))
    
    self.ldapDictionaryWithAliasId[loginAliasId] = ldapAliasInfo_dict
    logInfo("(#{}) loginAliasId:[{}] is looked up".format(len(self.ldapDictionaryWithAliasId), loginAliasId))
    
    #for key in ldapAliasInfo_dict.keys():
    #  logMessage("INFO", "  +>[{}]:[{}]".format(key, ldapAliasInfo_dict[key]))
    
    return ldapAliasInfo_dict
  
  def isActiveUser(self, loginAliasId):
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "dn" not in ldapAliasInfo_dict.keys():
      ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId)
      
    aliasIdStatus = "Unknown"
    if "dn" in ldapAliasInfo_dict.keys():
      if isinstance(ldapAliasInfo_dict["dn"], list):
        for subAttributeItems in ldapAliasInfo_dict["dn"]:
          if "ou" in subAttributeItems.keys():
            ouValue = subAttributeItems['ou']
            
            if ouValue == "people":
              aliasIdStatus = True
              break
            elif ouValue == "inactive users":
              aliasIdStatus = False
              break
      elif isinstance(ldapAliasInfo_dict["dn"], str) and "=" in ldapAliasInfo_dict["dn"]:
        subAttribute_list = []
        for subAttributeItem in ldapAliasInfo_dict["dn"].split(","):
          subAttributeName = subAttributeItem[:subAttributeItem.find("=")]
          subAttributeValue = subAttributeItem[subAttributeItem.find("=")+1:]
  
          subAttribute_list.append({subAttributeName: subAttributeValue})
        ldapAliasInfo_dict["dn"] = subAttribute_list
        
        for subAttributeItems in ldapAliasInfo_dict["dn"]:
          if "ou" in subAttributeItems.keys():
            ouValue = subAttributeItems['ou']
            
            if ouValue == "people":
              aliasIdStatus = True
              break
            elif ouValue == "inactive users":
              aliasIdStatus = False
              break
  
      else:    
        logError("loginAliasId:[{}] -> type:{} -> ldapAliasInfo_dict[\"dn\"]:[{}]".format(loginAliasId, type(ldapAliasInfo_dict["dn"]), ldapAliasInfo_dict["dn"]))
    
    return aliasIdStatus
  
  def getFullName(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "gecos" in ldapAliasInfo_dict.keys():
      fullName = ldapAliasInfo_dict["gecos"]
    else:
      fullName = "not_found"
    
    return fullName
  
  
  def getFirstName(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "gecos" in ldapAliasInfo_dict.keys():
      firstName = ldapAliasInfo_dict["gecos"].split(" ")[0]
    else:
      firstName = "not_found"
    
    return firstName
  
  
  def getLastName(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "gecos" in ldapAliasInfo_dict.keys():
      lastNameOffset = ldapAliasInfo_dict["gecos"].find(" ")
      if lastNameOffset > 0:
        lastName = ldapAliasInfo_dict["gecos"][lastNameOffset+1:]
      else:
        lastName = ldapAliasInfo_dict["gecos"]
    else:
      lastName = "not_found"
    
    return lastName
  
  
  def getJobLevel(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
      #return "Unknown"
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "amznjobcode" in ldapAliasInfo_dict.keys():
      jobLevel = ldapAliasInfo_dict["amznjobcode"]
    else:
      ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
      if "amznjobcode" in ldapAliasInfo_dict.keys():
        jobLevel = ldapAliasInfo_dict["amznjobcode"]
      else:
        jobLevel = "X"
    
    return jobLevel
    
  def getManagerAliasId(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    managerAliasId = "not_found"
    
    if "manager" in ldapAliasInfo_dict.keys():
      
      if isinstance(ldapAliasInfo_dict["manager"], str):
        logInfo("---> before: [{}]".format(ldapAliasInfo_dict["manager"]))
        jsonText = ldapAliasInfo_dict["manager"].replace("'",'"')
        logInfo("---> after: [{}]".format(ldapAliasInfo_dict["manager"]))
        
        if jsonText[0] == "[":
          endPosition = len(jsonText)
          while True:
            if jsonText[endPosition-1] == "]":
              break
            else:
              endPosition -= 1
              
              if endPosition == 1:
                break
          if endPosition > 1:
            ldapAliasInfo_dict["manager"] = json.loads(jsonText[0:endPosition])
          else:
            return "not_found({})".format(ldapAliasInfo_dict["manager"])
      
      if isinstance(ldapAliasInfo_dict["manager"], list):
        for subAttributeItems in ldapAliasInfo_dict["manager"]:
          try:
            if "cn" in subAttributeItems.keys():
              managerCN = subAttributeItems['cn']
              if len(managerCN.split("(")) == 2:
                managerAliasId = managerCN[managerCN.find("(")+1:managerCN.find(")")]
              else:
                managerCN = managerCN.split("(")[-1]
                managerAliasId = managerCN[:managerCN.find(")")]
          except Exception as e:
            logError("subAttributeItems:[{}] -> Error:[{}]".format(subAttributeItems, e))
            managerAliasId = "not_found+({})".format(ldapAliasInfo_dict["manager"])
      else:
        thisManagerString = "{}".format(ldapAliasInfo_dict["manager"])
        beginOffset = thisManagerString.find("(")
        endOffset = thisManagerString.find(")", beginOffset)
        if endOffset > beginOffset:
          managerAliasId = thisManagerString[beginOffset:endOffset]
        else:
          managerAliasId = "not_found++({})".format(ldapAliasInfo_dict["manager"])
        
    return managerAliasId

  def getDirectReportAliases(self, loginAliasId):
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    directReportAlias_list = []
    if "amznmanageremployees" in ldapAliasInfo_dict:
      logInfo("amznmanageremployees:[{}]".format(ldapAliasInfo_dict["amznmanageremployees"]))
      for directReportDict in ldapAliasInfo_dict["amznmanageremployees"]:
        directName = directReportDict[0]['cn']
        
        aliasBeingOffset = directName.rfind("(") + 1
        aliasEndOffset = directName.rfind(")")
        
        #logUnitTest("directReportDict:[{}]".format(directName[aliasBeingOffset:aliasEndOffset]))
        directReportAlias_list.append(directName[aliasBeingOffset:aliasEndOffset])
    else:
      logError( "loginAliasId:[{}] doesn't have any direct reporter".format(loginAliasId))

    return directReportAlias_list
  
  
  def getSteamAliasId(self, loginAliasId):
    if loginAliasId == "":
      raise ValueError("loginAliasId shouldn't be Null.")
    
    ldapAliasInfo_dict = self.queryLDAPWithLoginID(loginAliasId) 
    
    if "amzndepartmentalsteam" in ldapAliasInfo_dict.keys():
      steamAliasId = ldapAliasInfo_dict["amzndepartmentalsteam"]
    else:
      steamAliasId = "not_found"
    
    return steamAliasId
  
  
  def getReportingLineAlias(self, loginAliasId):
    if loginAliasId == "":
      return {}
    
    if loginAliasId in self.ldapReportingLine_dict.keys():
      return self.ldapReportingLine_dict[loginAliasId]
    
    reportingLine_dict = {}
    
    jobLevel = self.getJobLevel(loginAliasId)
    reportingLine_dict[jobLevel] = [loginAliasId]
    
    steamAliasId = self.getSteamAliasId(loginAliasId)
    reportingLine_dict["S"] = [steamAliasId]
    
    thisLoginAliasId = loginAliasId
    while True:
      thisManagerAliasId = self.getManagerAliasId(thisLoginAliasId)
      if thisManagerAliasId == "jeff":
        break
      
      if thisManagerAliasId != steamAliasId and thisManagerAliasId != "not_found":
        thisJobLevel = self.getJobLevel(thisManagerAliasId)
        #logTrace("thisManagerAliasId:[{}] -> thisJobLevel:[{}]".format(thisManagerAliasId, thisJobLevel))
        
        if thisJobLevel == "X":
          #logError("thisManagerAliasId:[{}] -> thisJobLevel:[{}]".format(thisManagerAliasId, thisJobLevel))
          break
        
        if thisJobLevel in reportingLine_dict.keys():
          reportingLine_dict[thisJobLevel].append(thisManagerAliasId)
        else:
          reportingLine_dict[thisJobLevel] = [thisManagerAliasId]
      else:
        thisJobLevel = self.getJobLevel(thisManagerAliasId)
        
        if thisJobLevel in reportingLine_dict.keys():
          reportingLine_dict[thisJobLevel].append(thisManagerAliasId)
        else:
          reportingLine_dict[thisJobLevel] = [thisManagerAliasId]     
          
        break
      
      thisLoginAliasId = thisManagerAliasId
        
    self.ldapReportingLine_dict[loginAliasId] = reportingLine_dict
    
    return reportingLine_dict
  
  
  def getSVP(self, loginAliasId):
    reportingLine_dict = self.getReportingLineAlias(loginAliasId)
    
    if '12' in reportingLine_dict.keys() and loginAliasId in reportingLine_dict["12"]:
      return loginAliasId
    if '11' in reportingLine_dict.keys():
      if loginAliasId in reportingLine_dict["11"]:
        return loginAliasId
      else:
        return reportingLine_dict["11"][0]
    elif '10' in reportingLine_dict.keys():
      return "+{}".format(reportingLine_dict["10"][-1])
    elif '8' in reportingLine_dict.keys():
      return "++{}".format(reportingLine_dict["8"][-1])
    else:
      return ""
  
  
  def getVVP(self, loginAliasId):
    reportingLine_dict = self.getReportingLineAlias(loginAliasId)
    
    if '10' in reportingLine_dict.keys():
      return reportingLine_dict["10"][-1]
    else:
      return ""
  
  
  def getFirstVP(self, loginAliasId):
    reportingLine_dict = self.getReportingLineAlias(loginAliasId)
    
    if '10' in reportingLine_dict.keys():
      return reportingLine_dict["10"][0]
    else:
      return ""
    
  
  def getFirstDirector(self, loginAliasId):
    reportingLine_dict = self.getReportingLineAlias(loginAliasId)
    
    if '8' in reportingLine_dict.keys():
      return reportingLine_dict["8"][0]
    else:
      return ""
  
  
  def getFirstSrManager(self, loginAliasId):
    reportingLine_dict = self.getReportingLineAlias(loginAliasId)
    
    if '7' in reportingLine_dict.keys():
      return reportingLine_dict["7"][0]
    elif '6' in reportingLine_dict.keys():
      return "+{}".format(reportingLine_dict["6"][0])
    elif '5' in reportingLine_dict.keys():
      return "++{}".format(reportingLine_dict["5"][0])
    else:
      return ""


  def getOwnerInfo(self, loginAliasId):
    if loginAliasId == "":
      ownerInfoDict = {}
      ownerInfoDict['aliasId'] = ""
      ownerInfoDict['firstName'] = ""
      ownerInfoDict['fullName'] = ""
      ownerInfoDict['aliasIdStatus'] = ""
      ownerInfoDict['jobLevel'] = ""
      ownerInfoDict['reportingChains'] = ""
      ownerInfoDict['SVP'] = ""
      ownerInfoDict['VVP'] = ""
      ownerInfoDict['fisrtVP'] = ""
      ownerInfoDict['firstDirector'] = ""
      ownerInfoDict['firstSrManager'] = ""  
    else:
      ownerInfoDict = {}
      ownerInfoDict['aliasId'] = loginAliasId
      ownerInfoDict['firstName'] = self.getFirstName(loginAliasId)
      ownerInfoDict['fullName'] = self.getFullName(loginAliasId)
      ownerInfoDict['aliasIdStatus'] = self.getAliasIdStatus(loginAliasId)
      ownerInfoDict['jobLevel'] = self.getJobLevel(loginAliasId)
      ownerInfoDict['reportingChains'] = self.getReportingLineAlias(loginAliasId)
      ownerInfoDict['SVP'] = self.getSVP(loginAliasId)
      ownerInfoDict['VVP'] = self.getVVP(loginAliasId)
      ownerInfoDict['fisrtVP'] = self.getFirstVP(loginAliasId)
      ownerInfoDict['firstDirector'] = self.getFirstDirector(loginAliasId)
      ownerInfoDict['firstSrManager'] = self.getFirstSrManager(loginAliasId)
    
    return ownerInfoDict

def ldapTest(loginAliasId):
  #loginAliasId = "hoeseong"
  
  pdxLdap = PdxLdap()
  ldapAliasInfo_dict = pdxLdap.queryLDAPWithLoginID(loginAliasId)
  logDebug("ldapAliasInfo_dict:[{}]".format(ldapAliasInfo_dict))
  
  managerAliasId = pdxLdap.getManagerAliasId(loginAliasId=loginAliasId)
  logDebug("isMemberOfLdapGroup({}):[{}]".format(loginAliasId, managerAliasId))
  
  ldapGroupName = "aws-tam-global"
  user_list = pdxLdap.getLDAPUsersWithLdapGroupName(ldapGroupName)
  logDebug("user_list:[{}]".format(user_list))
  
  isMemberOfLdapGroup = pdxLdap.isMemberOfLdapGroup(ldapGroupName=ldapGroupName, loginAliasId=loginAliasId)
  logDebug("isMemberOfLdapGroup({},{}):[{}]".format(ldapGroupName, loginAliasId, isMemberOfLdapGroup))
  
  ldapGroupName = "moduaws-access"
  isMemberOfLdapGroup = pdxLdap.isMemberOfLdapGroup(ldapGroupName=ldapGroupName, loginAliasId=loginAliasId)
  logDebug("isMemberOfLdapGroup({},{}):[{}]".format(ldapGroupName, loginAliasId, isMemberOfLdapGroup))
  
def lookupDirects(loginAliasId):
  
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
    
    
  
def localUnitTest():
  unitTestFunction_dict = {#"ldapTest":{"target":ldapTest, "args":("hoeseong",)},
                           "lookupDirects":{"target":lookupDirects, "args":("jfariss",)},
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()