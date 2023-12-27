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
from graphcode.conf import GcConf

from graphcode.path import createDir
from graphcode.unittest import unitTest

import json

import time
from pytz import timezone
from datetime import datetime

from tammy.midway import PdxMidway

from os.path import join

class PdxEnterpriseCustomerProfiles():
  def __init__(self, userAccountId = None, loginAliasId = None, sourceMedia = "local"):
    gcConf = GcConf()
    self.HOME_DIR = createDir(join(gcConf.getHomeDirectory(), "moduAWS-temp/EnterpriseCustomerProfile"))
    
    self.userAccountId = userAccountId
    self.loginAliasId = loginAliasId
    self.userAliasId = None
    
    self.sourceMedia = sourceMedia
    self.errMsg_list = []
    
    self.allCustomerInformationHTML = None
    
    self.enterpriseCustomerProfile_dict = None
    self.enterpriseCustomerProfile_list = None
  
    self.loadAllEnterpriseCustomerProfiles()
    
  def fetchAllCustomerInformation(self, targetURL = "https://taminator.aka.amazon.com/customer/list"):
    pdxMidway = PdxMidway(userAccountId = self.userAccountId, loginAliasId = self.loginAliasId)
    self.userAliasId = pdxMidway.user
    logDebug("midway userAliasId:[{}] is set".format(self.userAliasId))
    
    fetchedHTML = None
    
    try:
      r = pdxMidway.request(targetURL)
      fetchedHTML = r.content.decode()
      #logDebug("#fetchedHTML:type:{} -> len:{:,}".format(type(fetchedHTML), len(fetchedHTML)))
      
      f = open("{}/fetchAllCustomerInformation.html".format(self.HOME_DIR), "w")
      f.write(fetchedHTML)
      f.close()
      
    except Exception as e:
      errMsg = logError("unable to connect to url:[{}]-->Error:[{}]".format(targetURL, e))
      self.errMsg_list.append({"error":errMsg})
    
    return fetchedHTML
  
  def loadCustomerListHTML(self):
    if self.sourceMedia == "local":
      htmlFilename = "{}/fetchAllCustomerInformation.html".format(self.HOME_DIR)
      try:
        f = open(htmlFilename, "r")
        self.allCustomerInformationHTML = f.read()
        #logDebug("#sourceMedia:[{}] -> allCustomerInformationHTML:type:{} -> len:{}".format(self.sourceMedia, type(self.allCustomerInformationHTML), len(self.allCustomerInformationHTML)))
        
        if len(self.allCustomerInformationHTML) == 0:
          self.allCustomerInformationHTML = self.fetchAllCustomerInformation()
      except Exception as e:
        errorMessage = "Error:[{}] -> unable to load allCustomerInformationHTML with html:[{}]".format(e, htmlFilename)
        logError(errorMessage)
        
        self.allCustomerInformationHTML = self.fetchAllCustomerInformation()
      
    else:
      self.allCustomerInformationHTML = self.fetchAllCustomerInformation()
      if len(self.errMsg_list) > 0:
        self.allCustomerInformationHTML = self.fetchAllCustomerInformation()
        
    return self.allCustomerInformationHTML
  
  def getCustomerList(self):
    if self.allCustomerInformationHTML == None:
      self.allCustomerInformationHTML = self.loadCustomerListHTML()
  
  def findword(self, text, keyword, offset = 0):
    if keyword != "":
      begin = text.find(keyword, offset)
      end = begin + len(keyword)
    else:
      begin = -1
      end = -1
      
    return begin, end
  
  def getPhrase(self, text, startWith, endWith, offset = 0):
    #logDebug("#text:[len:{}], startWith:[{}], endWith:[{}], offset:[{}]".format(len(text), startWith, endWith, offset))
    firstStartOffset, firstEndOffset = self.findword(text, startWith, offset)
    
    secondStartOffset, secondEndOffset = self.findword(text, endWith, firstEndOffset + 1)
    
    thisPhrase = text[firstStartOffset + len(startWith):secondEndOffset - len(endWith)]
    
    return thisPhrase.strip(), firstStartOffset + len(startWith), secondEndOffset - len(endWith)
    
  def loadAllEnterpriseCustomerProfiles(self):
    if self.allCustomerInformationHTML == None:
      self.allCustomerInformationHTML = self.loadCustomerListHTML()
    
    if isinstance(self.allCustomerInformationHTML, str) != True:
      return self.allCustomerInformationHTML
    
    startWith = '<table id="customer-list" class="ui small table will_toggle" width="100%">'
    endWith = '</table>'
    
    CustomerListTableHTML, startOffset, endOffset = self.getPhrase((self.allCustomerInformationHTML), startWith, endWith)
    #logDebug("#self.allCustomerInformationHTML:[len:{}] -> CustomerListTableHTML:[len:{}]".format(len(self.allCustomerInformationHTML), len(CustomerListTableHTML)))
    
    try:
      f = open("{}/customerListTableHTML.html".format(self.HOME_DIR), "w")
      f.write(CustomerListTableHTML)
      f.close()
    except Exception as e:
      errorMessage = "Error:[{}] -> unable to get customer list table".format(e)
      logError(errorMessage)    

    columnNameHTML, columnNameStartOffset, columnNameEndOffset = self.getPhrase((CustomerListTableHTML), startWith = "<tr>", endWith="</tr>")
    #logDebug("#self.allCustomerInformationHTML:[len:{}] -> CustomerListTableHTML:[len:{}]->columnNameHTML:[len:{}]".format(len(self.allCustomerInformationHTML), len(CustomerListTableHTML), len(columnNameHTML)))
    
    columnName_list = []
    lastEndOffset = 0
    thisEndOffset = 0
    while True:
      columnName, startOffset, thisEndOffset = self.getPhrase(columnNameHTML, startWith = "<th>", endWith="</th>", offset = thisEndOffset)
      
      if thisEndOffset > 0 and thisEndOffset > lastEndOffset:
        lastEndOffset = thisEndOffset
        
        #logDebug("#columnName:[{}]".format(columnName))
        if columnName != "":
          if "Customer" in columnName:
            columnName_list.append("customerName") 
            columnName_list.append("customerDomainName") 
          else:
            columnName_list.append(columnName) 
      else:
        break
    columnName_list.append("additionalContacts")
    logInfo("columName_list(len:{}):[{}]".format(len(columnName_list), columnName_list))
    
    startsWith = '<tbody id="customer-list-body" style="display: none">'
    endWith = '</tbody>'
    customerProfilesHTML, startOffset, endOffset = self.getPhrase((CustomerListTableHTML), startWith = startsWith, endWith = endWith)
    #logDebug("#self.allCustomerInformationHTML:[len:{}] -> CustomerListTableHTML:[len:{}]->customerProfilesHTML:[len:{}]".format(len(self.allCustomerInformationHTML), len(CustomerListTableHTML), len(customerProfilesHTML)))
    
    customerProfileCount = 0
    customerProfile_list = []
    lastEndOffset = 0
    thisEndOffset = 0
    while True:
      customerProfileCount += 1
      
      customerProfiles, startOffset, thisEndOffset = self.getPhrase(customerProfilesHTML, startWith = "<tr>", endWith="</tr>", offset = thisEndOffset)
      
      thisCustomerDetails = customerProfiles.replace("\n","").replace("\r", "")
      #logDebug("#(#{}) customerProfiles:[{}]".format(customerProfileCount, thisCustomerDetails))
      
      if thisEndOffset > 0 and thisEndOffset > lastEndOffset:
        lastEndOffset = thisEndOffset
        
        customerDetail_dict = {}
        
        lastCustomerDetailsEndOffset = 0
        CustomerDetailsEndOffset = 0
        colunmNameCount = 0
        while True:
          columnValue, CustomerDetailsStartOffset, CustomerDetailsEndOffset = self.getPhrase(thisCustomerDetails, startWith = "<td>", endWith="</td>", offset = CustomerDetailsEndOffset)
          columnValue = columnValue.replace("  ","")
          #logDebug("#(#{}:{}) columnValue:[{}]".format(customerProfileCount, colunmNameCount, columnValue))
          
          if CustomerDetailsEndOffset > 0 and CustomerDetailsEndOffset > lastCustomerDetailsEndOffset and colunmNameCount < len(columnName_list):
            lastCustomerDetailsEndOffset = CustomerDetailsEndOffset
            #logDebug("#(#{})[{}:{}] columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, lastCustomerDetailsEndOffset, CustomerDetailsEndOffset, columnName_list[colunmNameCount], columnValue))
            
            
            if colunmNameCount == 0 and columnName_list[colunmNameCount] == "customerName":
              customerName, customerNameStartOffset, customerNameEndOffset = self.getPhrase(columnValue, startWith = "<b>", endWith="</b>")
              if isinstance(customerName, str) and len(customerName) == 0:
                customerName, customerNameStartOffset, customerNameEndOffset = self.getPhrase(columnValue, startWith = "<a ", endWith="</a>")
                
              if customerName.startswith("href="):
                customerName, customerNameStartOffset, customerNameEndOffset = self.getPhrase(customerName, startWith = 'target="_blank">', endWith='</a>')
              #logDebug("#(#{}) customerName:[{}]".format(colunmNameCount, customerName))
              
              customerDetail_dict[columnName_list[colunmNameCount]] = customerName
              colunmNameCount += 1
              
              customerDomainName, customerDomainNameStartOffset, customerDomainNameEndOffset = self.getPhrase(columnValue, startWith = '<small class="date">', endWith='</small>', offset = customerNameEndOffset)
              #logDebug("#(#{}) customerDomainName:[{}]".format(colunmNameCount, customerDomainName))
              
              customerDetail_dict[columnName_list[colunmNameCount]] = customerDomainName
              colunmNameCount += 1
            elif colunmNameCount == 2 and columnName_list[colunmNameCount] == "ES Organization":
              #logDebug("#(#{})[{}:{}] columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, lastEndOffset, thisEndOffset, columnName_list[colunmNameCount], columnValue))
          
              customerDetail_dict["entOrganization"] = columnValue
              colunmNameCount += 1
            elif colunmNameCount == 3 and columnName_list[colunmNameCount] == "TAM":
              thirdColumnLastEndOffset = 0
              thirdColumnEndOffset = 0
              thirdColumnCount = 0
              thirdColumnValue_list = []
              while True:
                thirdColumnValue, thirdColumnStartOffset, thirdColumnEndOffset = self.getPhrase(columnValue, startWith = '" target="_blank">', endWith='</a>')
                if thisEndOffset > 0 and thirdColumnEndOffset > thirdColumnLastEndOffset:
                  #logDebug("#[{}:{}] thirdColumnValue:[{}]".format(thirdColumnLastEndOffset, thirdColumnEndOffset, thirdColumnValue))
                
                  thirdColumnLastEndOffset = thirdColumnEndOffset
                  thirdColumnValue_list.append(thirdColumnValue)
                else:
                  break
              customerDetail_dict[columnName_list[colunmNameCount]] = thirdColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict[columnName_list[colunmNameCount]]))
              
              colunmNameCount += 1
            elif colunmNameCount == 4 and columnName_list[colunmNameCount] == "TAMs email":
              forthColumnLastEndOffset = 0
              forthColumnEndOffset = 0
              forthColumnCount = 0
              forthColumnValue_list = []
              while True:
                forthColumnValue, forthColumnStartOffset, forthColumnEndOffset = self.getPhrase(columnValue, startWith = '" target="_blank">', endWith='</a>')
                if thisEndOffset > 0 and forthColumnEndOffset > forthColumnLastEndOffset:
                  #logDebug("#[{}:{}] forthColumnValue:[{}]".format(forthColumnLastEndOffset, forthColumnEndOffset, forthColumnValue))
                
                  forthColumnLastEndOffset = forthColumnEndOffset
                  forthColumnValue_list.append(forthColumnValue)
                else:
                  break
              #customerDetail_dict[columnName_list[colunmNameCount]] = forthColumnValue_list
              customerDetail_dict["tamEmail"] = forthColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict["tamEmail"]))
              
              colunmNameCount += 1
            elif colunmNameCount == 5 and columnName_list[colunmNameCount] == "SA":
              fifthColumnLastEndOffset = 0
              fifthColumnEndOffset = 0
              fifthColumnCount = 0
              fifthColumnValue_list = []
              while True:
                fifthColumnValue, fifthColumnStartOffset, fifthColumnEndOffset = self.getPhrase(columnValue, startWith = '" target="_blank">', endWith='</a>')
                if thisEndOffset > 0 and fifthColumnEndOffset > fifthColumnLastEndOffset:
                  #logDebug("#[{}:{}] fifthColumnValue:[{}]".format(fifthColumnLastEndOffset, fifthColumnEndOffset, fifthColumnValue))
                
                  fifthColumnLastEndOffset = fifthColumnEndOffset
                  fifthColumnValue_list.append(fifthColumnValue)
                else:
                  break
              customerDetail_dict[columnName_list[colunmNameCount]] = fifthColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict[columnName_list[colunmNameCount]]))
              
              colunmNameCount += 1
            elif colunmNameCount == 6 and columnName_list[colunmNameCount] == "AM":
              sixthColumnLastEndOffset = 0
              sixthColumnEndOffset = 0
              sixthColumnCount = 0
              sixthColumnValue_list = []
              while True:
                sixthColumnValue, sixthColumnStartOffset, sixthColumnEndOffset = self.getPhrase(columnValue, startWith = '" target="_blank">', endWith='</a>')
                if thisEndOffset > 0 and sixthColumnEndOffset > sixthColumnLastEndOffset:
                  #logDebug("#[{}:{}] sixthColumnValue:[{}]".format(sixthColumnLastEndOffset, sixthColumnEndOffset, sixthColumnValue))
                
                  sixthColumnLastEndOffset = sixthColumnEndOffset
                  sixthColumnValue_list.append(sixthColumnValue)
                else:
                  break
              customerDetail_dict[columnName_list[colunmNameCount]] = sixthColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict[columnName_list[colunmNameCount]]))
              
              colunmNameCount += 1
            elif colunmNameCount == 7 and columnName_list[colunmNameCount] == "Account team email":
              seventhColumnLastEndOffset = 0
              seventhColumnEndOffset = 0
              seventhColumnCount = 0
              seventhColumnValue_list = []
              while True:
                seventhColumnValue, seventhColumnStartOffset, seventhColumnEndOffset = self.getPhrase(columnValue, startWith = '" target="_blank">', endWith='</a>')
                if thisEndOffset > 0 and seventhColumnEndOffset > seventhColumnLastEndOffset:
                  #logDebug("#[{}:{}] seventhColumnValue:[{}]".format(seventhColumnLastEndOffset, seventhColumnEndOffset, seventhColumnValue))
                
                  seventhColumnLastEndOffset = seventhColumnEndOffset
                  seventhColumnValue_list.append(seventhColumnValue)
                else:
                  break
              #customerDetail_dict[columnName_list[colunmNameCount]] = seventhColumnValue_list
              customerDetail_dict["accountTeamEmail"] = seventhColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict["accountTeamEmail"]))
              
              colunmNameCount += 1
            elif colunmNameCount == 8 and columnName_list[colunmNameCount] == "All Team Members":
              eighthColumnLastEndOffset = 0
              eighthColumnEndOffset = 0
              eighthColumnCount = 0
              eighthColumnValue_list = []
              while True:
                eighthColumnValue, eighthColumnStartOffset, eighthColumnEndOffset = self.getPhrase(columnValue, startWith = '<a class="content">', endWith='</a></div>')
                if thisEndOffset > 0 and eighthColumnEndOffset > eighthColumnLastEndOffset:
                  #logDebug("#[{}:{}] eighthColumnValue:[{}]".format(eighthColumnLastEndOffset, eighthColumnEndOffset, eighthColumnValue))
                
                  eighthColumnLastEndOffset = eighthColumnEndOffset
                  eighthColumnValue_list.append(eighthColumnValue)
                else:
                  break
              #customerDetail_dict[columnName_list[colunmNameCount]] = eighthColumnValue_list
              customerDetail_dict["allMemberEmails"] = eighthColumnValue_list
              #logDebug("#(#{}) columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, columnName_list[colunmNameCount], customerDetail_dict["allMemberEmails"]))
              
              colunmNameCount += 1
            elif colunmNameCount == 9:# and columnName_list[colunmNameCount] == "additionalContacts":
              columnValue, CustomerDetailsStartOffset, CustomerDetailsEndOffset = self.getPhrase(columnValue, startWith = 'class="show-account-team-members" data-team-members="', endWith='" data-web-domain="')
              
              additionalContacts_list = None
              try:
                columnValue = columnValue.replace("&quot;",'"')
                additionalContacts_list = json.loads(columnValue)
              except Exception as e:
                errorMessage = "Error:[{}] -> failed to get additional contacts with [{}]".format(e, columnValue)
                
              
              #logDebug("#additionalContacts:[{}]".format(columnValue))
              
              if additionalContacts_list != None and isinstance(additionalContacts_list, list):
                  
                for additionalContactItems in additionalContacts_list:
                  #{"email": "balwani@amazon.com", "contactId": "3148c224-9f45-4afb-84e3-5b40ba69ca25", "role": "ENTERPRISE_ACCOUNT_ENGINEER_PRIMARY"}
                  role = additionalContactItems["role"]
                  email = additionalContactItems["email"]
                  if "@amazon" in email:
                    email = email.split("@")[0]
                   
                  #contactId = additionalContactItems["contactId"]
                  
                  if role in customerDetail_dict.keys():
                    customerDetail_dict[role].append(email)
                  else:
                    customerDetail_dict[role] = [email]
                    colunmNameCount += 1
              else:
                pass
            else:
              #logDebug("#(#{})[{}:{}] columnName:[{}] -> columnValue:[{}]".format(colunmNameCount, lastEndOffset, thisEndOffset, columnName_list[colunmNameCount], columnValue))
          
              customerDetail_dict[columnName_list[colunmNameCount]] = columnValue
              colunmNameCount += 1  
            
          else:
            break
        
        customerProfile_list.append(customerDetail_dict)
        #logDebug("#(#{}) customerProfiles:[{}]".format(thisEndOffset, customerProfile_list[-1]))
        
      else:
        break
      
      #if customerProfileCount > 3:
      #  break
    logInfo("customerProfile_list:[len:{}]".format(len(customerProfile_list)))
    
    self.enterpriseCustomerProfile_list = customerProfile_list
      
    return customerProfile_list
  
  def discoverCustomers(self, query = ""):
    if self.enterpriseCustomerProfile_list == None:
      self.loadAllEnterpriseCustomerProfiles()
    
    result_list = []
    if isinstance(query, str):
      if query == "" or query == "hoeseong":
        result_list = self.enterpriseCustomerProfile_list
      elif len(query.replace(" ",""))>3:
        for customerProfileItems in self.enterpriseCustomerProfile_list:
          for profileItemName in customerProfileItems.keys():
            if isinstance(customerProfileItems[profileItemName], list):
              isFound = False
              for thisProfileItem in customerProfileItems[profileItemName]:
                if query.lower() in thisProfileItem.lower():
                  result_list.append(customerProfileItems)
                  isFound = True
                  break
              if isFound:
                break
            elif query.lower() in "{}".format(customerProfileItems[profileItemName]).lower():
              result_list.append(customerProfileItems)
              break
      else:
        errMsg = logError("Error:['unexpected value'] -> query:type:{}:[{}] is expected with larger than 3 characters instead of {}".format(type(query), query, len(query)))
    else:
      errMsg = logError("Error:['unexpected value'] -> query:type:{}:[{}] is should be string".format(type(query), query))
    
    if len(self.errMsg_list) > 0:
      return self.errMsg_list
    else:
      return result_list
  
  def getCustomerDetails(self, input_dict, wbResult_dict):
    accountDetails_dict = {}
    parentAccountIdMapping_dict = {}
    
    entCustomerProfile_dict = {}
    customerId_dict = {}
    
    for resultApiName in wbResult_dict.keys():
      if "profile.list" in resultApiName:
        result_list = wbResult_dict[resultApiName]
        if isinstance(result_list, list) and len(result_list) > 0 and isinstance(result_list[0], dict):
          pass
        else:
          logDebug("resultApiName:[{}] -> type:{}:result_list:[{}]".format(resultApiName, type(result_list), result_list))
          continue
        
        for resultItems in result_list:
          logDebug("resultApiName:[{}] -> resultItems:[{}]".format(resultApiName, resultItems))
          
          if "customerDomainName" in resultItems.keys():
            customerDomainName = resultItems["customerDomainName"]
          else:
            continue
          
          if customerDomainName in entCustomerProfile_dict.keys():
            for profileItemName in resultItems.keys():
              entCustomerProfile_dict[customerDomainName][profileItemName] = resultItems[profileItemName]
            
          else:
            entCustomerProfile_dict[customerDomainName] = resultItems
            
    logInfo("total {} customer profiles are updated".format(len(entCustomerProfile_dict.keys())))
    #end if "ent.discoverCustomers" in resultApiName:
      
    for resultApiName in wbResult_dict.keys():
      if "kumoscp.searchCustomers" in resultApiName:
        result_list = wbResult_dict[resultApiName]
        if isinstance(result_list, list) and len(result_list) > 0 and isinstance(result_list[0], dict):
          pass
        else:
          logDebug("resultApiName:[{}] -> type:{}:result_list:[{}]".format(resultApiName, type(result_list), result_list))
          continue
        
        for resultItems in result_list:
          logDebug("resultApiName:[{}] -> resultItems:[{}]".format(resultApiName, resultItems))
          
          if "primaryWebDomain" in resultItems.keys():
            primaryWebDomain = resultItems["primaryWebDomain"]
          else:
            continue
          
          if "id" in resultItems.keys():
            customerId = resultItems["id"]
            customerId_dict[customerId] = primaryWebDomain
          else:
            continue
          
          if primaryWebDomain in entCustomerProfile_dict.keys():
            for profileItemName in resultItems.keys():
              entCustomerProfile_dict[primaryWebDomain][profileItemName] = resultItems[profileItemName]
          else:
            entCustomerProfile_dict[primaryWebDomain] = resultItems
            
      #end elif "kumoscp.searchCustomers" in resultApiName:
    logInfo("total {} customer profiles are updated".format(len(entCustomerProfile_dict.keys())))
    logInfo("total {} customerIds are found".format(len(customerId_dict.keys())))
    
    for resultApiName in wbResult_dict.keys():
      if "kumoscp.getCustomerAccountFullList" in resultApiName:
        result_list = wbResult_dict[resultApiName]
        if isinstance(result_list, list) and len(result_list) > 0 and isinstance(result_list[0], dict):
          pass
        else:
          logDebug("resultApiName:[{}] -> type:{}:result_list:[{}]".format(resultApiName, type(result_list), result_list))
          continue
        
        for resultItems in result_list:
          #logDebug("#resultItems:[{}]".format(resultItems))
          
          if "accountId" in resultItems.keys():
            accountId = resultItems["accountId"]
          else:
            continue
          
          if accountId in accountDetails_dict.keys():
            for accountDetailItemName in resultItems.keys():
              accountDetails_dict[accountId][accountDetailItemName] = resultItems[accountDetailItemName]
          else:
            accountDetails_dict[accountId] = resultItems
          
          if "id" in accountDetails_dict[accountId].keys() and accountDetails_dict[accountId]["id"] in customerId_dict.keys():
            primaryWebDomain = customerId_dict[accountDetails_dict[accountId]["id"]]
            if primaryWebDomain in entCustomerProfile_dict.keys():
              customerProfile_dict = entCustomerProfile_dict[primaryWebDomain]
              for profileItemName in customerProfile_dict.keys():
                accountDetails_dict[accountId][profileItemName] = customerProfile_dict[profileItemName]
          
              #logDebug("#accountId:[{}] -> accountDetails:[{}]".format(accountId, accountDetails_dict[accountId]))
          #endif "id" in accountDetails_dict[accountId].keys() and accountDetails_dict[accountId]["id"] in customerId_dict.keys():
        #endfor resultItems in result_list:
        logInfo("total {} accountId's details are updated".format(len(accountDetails_dict.keys())))
      #end:elif "kumoscp.getCustomerAccountFullList" in resultApiName:
      
    #end:for resultApiName in wbResult_dict.keys():
    '''
    for resultApiName in wbResult_dict.keys():
      if "awsadms.getChildAccountsForParentAccount" in resultApiName:
        result_list = wbResult_dict[resultApiName]
        if isinstance(result_list, list) and len(result_list) > 0 and isinstance(result_list[0], dict):
          pass
        else:
          logDebug("resultApiName:[{}] -> type:{}:result_list:[{}]".format(resultApiName, type(result_list), result_list))
          continue
        
        for resultItems in result_list:
          #logDebug("#resultItems:[{}]".format(resultItems))
          
          if "childAccountList" in resultItems.keys():
            childAccountId = resultItems["childAccountList"]
          else:
            continue
          
          if "parentAccountId" in resultItems.keys():
            parentAccountId = resultItems["parentAccountId"]
          else:
            continue
          
          if childAccountId in parentAccountIdMapping_dict.keys():
            pass
          else:
            parentAccountIdMapping_dict[childAccountId] = parentAccountId
          
        logInfo("total {} child accountId are mapped with parentAccountIds".format(len(accountDetails_dict.keys())))
      #end:elif "kumoscp.getCustomerAccountFullList" in resultApiName:
    '''
    #end:for resultApiName in wbResult_dict.keys():
    
    for resultApiName in wbResult_dict.keys():
      if "as.getAddressById" in resultApiName:
        result_list = wbResult_dict[resultApiName]
        if isinstance(result_list, list) and len(result_list) > 0 and isinstance(result_list[0], dict):
          pass
        else:
          logDebug("resultApiName:[{}] -> type:{}:result_list:[{}]".format(resultApiName, type(result_list), result_list))
          continue
        
        for resultItems in result_list:
          if "accountId" in resultItems.keys():
            accountId = resultItems["accountId"]
          else:
            continue
          
          if "Label_" in resultItems.keys():
            customerLabel = resultItems["Label_"]
          else:
            customerLabel = ""
            
          if "FullName_" in resultItems.keys():
            customerFullName = resultItems["FullName_"]
          else:
            customerFullName = ""
            
          if "CompanyName_" in resultItems.keys():
            customerCompanyName = resultItems["CompanyName_"]
          else:
            customerCompanyName = ""
            
          if "EmailAddress_" in resultItems.keys():
            customerEmailAddress = resultItems["EmailAddress_"]
          else:
            customerEmailAddress = ""
            
          if accountId in accountDetails_dict.keys():
            logWarn("accountId:[{}] is duplicated with [{}]".format(accountId, accountDetails_dict[accountId]))
            accountDetails_dict[accountId]["accountId"] = accountId
            accountDetails_dict[accountId]["customerLabel"] = customerLabel
            accountDetails_dict[accountId]["customerFullName"] = customerFullName
            accountDetails_dict[accountId]["customerCompanyName"] = customerCompanyName
            accountDetails_dict[accountId]["customerEmailAddress"] = customerEmailAddress
          else:
            accountDetails_dict[accountId] = {}
            if accountId in parentAccountIdMapping_dict.keys():
              parentAccountId = parentAccountIdMapping_dict[accountId]
              if parentAccountId in accountDetails_dict.keys():
                for accountDetailItemName in accountDetails_dict[parentAccountId].keys():
                  accountDetails_dict[accountId][accountDetailItemName] = accountDetails_dict[parentAccountId][accountDetailItemName]
            
            accountDetails_dict[accountId]["accountId"] = accountId
            accountDetails_dict[accountId]["customerLabel"] = customerLabel
            accountDetails_dict[accountId]["customerFullName"] = customerFullName
            accountDetails_dict[accountId]["customerCompanyName"] = customerCompanyName
            accountDetails_dict[accountId]["customerEmailAddress"] = customerEmailAddress
    
    for accountId in accountDetails_dict.keys():
      if "customerEmailAddress" in accountDetails_dict[accountId].keys() and accountDetails_dict[accountId]["customerEmailAddress"] == "":
        if accountId in parentAccountIdMapping_dict.keys():
          parentAccountId = parentAccountIdMapping_dict[accountId]
          if parentAccountId in accountDetails_dict.keys():
            accountDetails_dict[accountId]["customerEmailAddress"] = accountDetails_dict[parentAccountId]["customerEmailAddress"]
      
    accountDetails_list = []
    for accountId in accountDetails_dict.keys():
      ##logDebug("#accountId:[{}] -> accountDetails:[{}]".format(accountId, accountDetails_dict[accountId]))
      accountDetails_list.append(accountDetails_dict[accountId])
    
    return accountDetails_list

  def getEnterpriseCustomerDetails(self, wbResult_dict):
    customerDetails_list = []
    for resultApiName in wbResult_dict.keys():
      if "getCustomerDetails" in resultApiName and isinstance(wbResult_dict[resultApiName], list) and len(wbResult_dict[resultApiName]) > 0 and isinstance(wbResult_dict[resultApiName][0], dict):
        customerDetails_list = wbResult_dict[resultApiName]
        logDebug("resultApiName:[{}] -> type:{}:result_list:[len:{}]".format(resultApiName, type(customerDetails_list), len(customerDetails_list)))
      else:
        continue
    
      for customerDetailItems in customerDetails_list:
        logDebug("customerDetailItems.keys:[{}]".format(customerDetailItems.keys()))
        
        if "accountId" in customerDetailItems.keys():
          accountId = customerDetailItems["accountId"]
          
          thisCustomerDetails_dict = {}
          thisCustomerDetails_dict["customerProfileName"] = customerDetailItems["name"]
          thisCustomerDetails_dict["accountId"] = accountId
          thisCustomerDetails_dict["payerAccountId"] = customerDetailItems["payerId"]
          thisCustomerDetails_dict["accountType"] = customerDetailItems["role"]
          thisCustomerDetails_dict["accountStatusCode"] = customerDetailItems["status"]
          thisCustomerDetails_dict["supportLevel"] = customerDetailItems["supportLevel"]
          
          if "customerCompanyName" in customerDetailItems.keys():
            thisCustomerDetails_dict["customerCompanyName"] = customerDetailItems["customerCompanyName"]
          else:
            thisCustomerDetails_dict["customerCompanyName"] = ""
            
          if "customerEmailAddress" in customerDetailItems.keys():
            thisCustomerDetails_dict["customerEmailAddress"] = customerDetailItems["customerEmailAddress"]
          else:
            thisCustomerDetails_dict["customerEmailAddress"] = ""
            
          if "customerFullName" in customerDetailItems.keys():
            thisCustomerDetails_dict["customerFullName"] = customerDetailItems["customerFullName"]
          else:
            thisCustomerDetails_dict["customerFullName"] = ""
            
          if "customerLabel" in customerDetailItems.keys():
            thisCustomerDetails_dict["customerLabel"] = customerDetailItems["customerLabel"]
          else:
            thisCustomerDetails_dict["customerLabel"] = ""
            
          if "email" in customerDetailItems.keys():
            thisCustomerDetails_dict["customerEmailDomain"] = customerDetailItems["email"]
          else:
            thisCustomerDetails_dict["customerEmailDomain"] = ""
            
          if "primaryWebDomain" in customerDetailItems.keys():
            thisCustomerDetails_dict["webDomain"] = customerDetailItems["primaryWebDomain"]
          else:
            thisCustomerDetails_dict["webDomain"] = ""
            
          if "entOrganization" in customerDetailItems.keys():
            thisCustomerDetails_dict["entOrganization"] = customerDetailItems["entOrganization"]
          else:
            thisCustomerDetails_dict["entOrganization"] = ""
            
          thisCustomerDetails_dict["primaryContacts"] = []
          thisCustomerDetails_dict["primaryContactSource"] = ""
          if "TAM" in customerDetailItems.keys():
            thisCustomerDetails_dict["primaryTAM"] = customerDetailItems["TAM"]
          else:
            thisCustomerDetails_dict["primaryTAM"] = ""
          if "ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY" in customerDetailItems.keys():
            thisCustomerDetails_dict["secondaryTAM"] = customerDetailItems["ENTERPRISE_ACCOUNT_ENGINEER_SECONDARY"]
          else:
            thisCustomerDetails_dict["secondaryTAM"] = ""
          if "ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME" in customerDetailItems.keys():
            thisCustomerDetails_dict["nightTAM"] = customerDetailItems["ENTERPRISE_ACCOUNT_ENGINEER_NIGHT_TIME"]
          else:
            thisCustomerDetails_dict["nightTAM"] = ""
          if "ENTERPRISE_SUPPORT_MANAGER" in customerDetailItems.keys():
            thisCustomerDetails_dict["enterpriseSupportManager"] = customerDetailItems["ENTERPRISE_SUPPORT_MANAGER"]
          else:
            thisCustomerDetails_dict["enterpriseSupportManager"] = ""
            
          if len(thisCustomerDetails_dict["primaryTAM"]) == 0:
            if len(thisCustomerDetails_dict["primaryTAM"]) == 0:
              if len(thisCustomerDetails_dict["secondaryTAM"]) == 0:
                if len(thisCustomerDetails_dict["nightTAM"]) == 0:
                  if len(thisCustomerDetails_dict["enterpriseSupportManager"]) == 0:
                    logWarn("unable able to set the primaryContact with TAM's contacts")
                  else:
                    for contactAliasId in thisCustomerDetails_dict["enterpriseSupportManager"]:
                      if "-" in contactAliasId:
                        pass
                      else:
                        thisCustomerDetails_dict["primaryContacts"].append(contactAliasId)
                    
                    thisCustomerDetails_dict["primaryContactSource"] = "enterpriseSupportManager"
                else: # night
                  for contactAliasId in thisCustomerDetails_dict["nightTAM"]:
                    if "-" in contactAliasId:
                      pass
                    else:
                      thisCustomerDetails_dict["primaryContacts"].append(contactAliasId)
                      
                  thisCustomerDetails_dict["primaryContactSource"] = "nightTAM"
              else: # Secondary
                for contactAliasId in thisCustomerDetails_dict["secondaryTAM"]:
                  if "-" in contactAliasId:
                    pass
                  else:
                    thisCustomerDetails_dict["primaryContacts"].append(contactAliasId)
                  
                thisCustomerDetails_dict["primaryContactSource"] = "secondaryTAM"
            else: #Primary
              for contactAliasId in thisCustomerDetails_dict["primaryTAM"]:
                if "-" in contactAliasId:
                  pass
                else:
                  thisCustomerDetails_dict["primaryContacts"].append(contactAliasId)
                
              thisCustomerDetails_dict["primaryContactSource"] = "primaryTAM"
            
        else:
          continue
      
      customerDetails_list.append(thisCustomerDetails_dict)
    #end for resultApiName in wbResult_dict.keys():
    
    return customerDetails_list
  
def unitTest_getAllCustomers():
  
  pdxEnterpriseCustomerProfiles = PdxEnterpriseCustomerProfiles()
  
  #moduEnterpriseSupport.fetchAllCustomerInformation()
  customerProfileCount = 0
  for customerProfileItems in pdxEnterpriseCustomerProfiles.discoverCustomers("hoeseong"):
    customerProfileCount += 1
    logInfo("(#{}) customerProfileItems:[{}]".format(customerProfileCount, customerProfileItems))

def localUnitTest():
  unitTestFunction_dict = {#"unitTest_getK2ResponseProdWith_support_describeCase":{"target":unitTest_getK2ResponseProdWith_support_describeCase, "args":()},
                           "unitTest_getAllCustomers":{"target":unitTest_getAllCustomers, "args":()},
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  
  localUnitTest()
  
  #{"accountId":"454539282959","region":"us-east-1","args":{"accountId":"454539282959"},"apiName":"awsadms.getAccountIdentifiersByAccountId","sessionMetadata":{"segment":"rds_workbench","instance_id":"b866b658-d4c1-4ff9-8202-8a43efaff1c6-1","name":"Account Details"}}
