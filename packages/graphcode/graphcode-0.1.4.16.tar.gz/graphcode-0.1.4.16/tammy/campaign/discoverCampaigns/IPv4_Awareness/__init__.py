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
from graphcode.lib import getDateString

from pathway import requests

from wooju.lib import loadCache, saveCache
from tammy.email import GcEmail

from os.path import basename, dirname

import time

def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "state": "SUCCEEDED",
      "__file__": __file__
      }
  except:
    response_dict = {
      "apiName": request_dict["apiName"],
      "state":"FAILED",
      "errorReasons":[logException("apiName:[{}] failed".format(request_dict["apiName"]))],
      "__file__": __file__
      }

  return response_dict

def action(request_dict):
  logMessage_list = []
  errorReason_list = []
  
  #campaignName = basename(dirname(__file__))

  campaignName = request_dict["attributes"]["campaign"]["name"]
  campaignNameMessage_list = getCampainMessages(request_dict)
  campaignNameMessage_list = sendCampaignMessages(campaignNameMessage_list)

  return {
    campaignName:campaignNameMessage_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def getCampainMessages(request_dict):
  try:
    beforeVsAfter_summary_list = loadCache(request_dict, name="beforeVsAfter_summary_list")
  except:
    request_dict["attributes"]["dbType"] = "aws"
    
    response_dict = requests(
      request_dict = {
        **request_dict,
        "apiName":"tammy.dw.aws.templates.esCustomer_IPv4"
      }
    )
    for resKey in response_dict["response"].keys():
      logDebug("resKey:[{}]".format(resKey))
    
    beforeVsAfter_summary_list = response_dict["response"]["beforeVsAfter_summary"]
    saveCache(request_dict, name="beforeVsAfter_summary_list", value=beforeVsAfter_summary_list, ttl_s=86400*7)
  
  #campaignName = request_dict["attributes"]["campaign"]["name"]
  campaignSubject = request_dict["attributes"]["head"]["subject"]
  campaignBody = request_dict["attributes"]["body"]
  
  campaignTo = request_dict["attributes"]["head"]["to"]
  logDebug(f"campaignTo:[{campaignTo}]")
  campaignCc = request_dict["attributes"]["head"]["cc"]
  logDebug(f"campaignCc:[{campaignCc}]")
  campaignBcc = "campaignhub-noreply@amazon.com" #request_dict["attributes"]["head"]["bcc"]
  logDebug(f"campaignBcc:[{campaignBcc}]")

  if "dryRun" in request_dict["attributes"].keys() and "Yes" in request_dict["attributes"]["dryRun"]:
    dryrunPrefix = "campaignhub+"
  else:
    dryrunPrefix = ""
  logDebug(f"dryrunPrefix:[{dryrunPrefix}]")
  
  campaignNameMessage_list = []
  itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=beforeVsAfter_summary_list, divider=3)
  for ipv4Item_dict in beforeVsAfter_summary_list:
    itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, ipv4Item_dict, itemName="ipv4Item_dict")

    ipv4Item_dict["hourlyIpv4UsageValue"] = f"{int(ipv4Item_dict['ipv4UsageValue']/5/7/24):,}"

    thisCampaignSubject = campaignSubject
    thisCampaignBody = campaignBody
    thisCampaignFrom = "campaignhub-noreply@amazon.com"
    thisCampaignTo = ""
    thisCampaignCc = ""
    thisCampaignBcc = "campaignhub@amazon.com;"
    for itemKey in ipv4Item_dict.keys():
      targetKeyword = "${"+f"{itemKey}"+"}"
      #logDebug(f"(#{itemCount:,})\t[{targetKeyword}]:[{ipv4Item_dict[itemKey]}]")

      if thisCampaignSubject.find(targetKeyword) != -1:
        thisCampaignSubject = thisCampaignSubject.replace(targetKeyword, f"{ipv4Item_dict[itemKey]}")

      if thisCampaignBody.find(targetKeyword) != -1:
        thisCampaignBody = thisCampaignBody.replace(targetKeyword, f"{ipv4Item_dict[itemKey]}")

      if campaignTo.find(targetKeyword) != -1 and isinstance(ipv4Item_dict[itemKey], str):
        for emailAddress in ipv4Item_dict[itemKey].split(";"): 
          if emailAddress.find("@") == -1:
            thisCampaignTo +=  f"{dryrunPrefix}{emailAddress}@amazon.com;"
          else:
            thisCampaignTo += f"{dryrunPrefix}{emailAddress};"
            
      if campaignCc.find(targetKeyword) != -1 and isinstance(ipv4Item_dict[itemKey], str):
        for emailAddress in ipv4Item_dict[itemKey].split(";"): 
          if emailAddress.find("@") == -1:
            thisCampaignCc +=  f"{dryrunPrefix}{emailAddress}@amazon.com;"
          else:
            thisCampaignCc += f"{dryrunPrefix}{emailAddress};"
            
      if campaignBcc.find(targetKeyword) != -1 and isinstance(ipv4Item_dict[itemKey], str):
        for emailAddress in ipv4Item_dict[itemKey].split(";"): 
          if emailAddress.find("@") == -1:
            thisCampaignBcc +=  f"{dryrunPrefix}{emailAddress}@amazon.com;"
          else:
            thisCampaignBcc += f"{dryrunPrefix}{emailAddress};"
        
    #logDebug(f"(#{itemCount:,})\t[{targetKeyword}]:[{ipv4Item_dict[itemKey]}]->subject:[{thisCampaignSubject}]")
    
    campaignNameMessage_list.append(
      {
        "subject":thisCampaignSubject,
        "from": thisCampaignFrom,
        "to": thisCampaignTo,
        "cc": thisCampaignCc,
        "bcc": thisCampaignBcc,
        "body": thisCampaignBody
      }
    )
  
  return campaignNameMessage_list
            
def sendCampaignMessages(campaignNameMessage_list):
  errorReason_list = []
  logMessage_list = []
  
  thisCampaignNameMessage_list = []
  itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=campaignNameMessage_list, divider=3)
  for campaignMessageItem_dict in campaignNameMessage_list:
    itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, campaignMessageItem_dict, itemName="campaignMessageItem_dict")
    
    #if "nike" not in campaignMessageItem_dict["subject"].lower(): #["sugarcrm","nike"]
    #  continue
    
    if campaignMessageItem_dict["subject"].lower() in ["sugarcrm","nike","sap.com"]:
      continue
    
    try:
      gcEmail = GcEmail()
      gcEmail.setDefaultEmailDomain("amazon.com")
      gcEmail.setEmailType("html")

      gcEmail.setFromAlias(campaignMessageItem_dict["from"])

      if len(campaignMessageItem_dict["to"].split(";")) > 0 and len(campaignMessageItem_dict["to"].split(";")[0]) > 0:
        for emailAddress in campaignMessageItem_dict["to"].split(";"):
          if len(emailAddress) > 0:
            gcEmail.addToAlias(emailAddress)
      else:
        logWarn(f"No receiver for [{campaignMessageItem_dict['subject']}]")
        continue
        
      if len(campaignMessageItem_dict["cc"].split(";")) > 0 and len(campaignMessageItem_dict["cc"].split(";")[0]) > 0:
        for emailAddress in campaignMessageItem_dict["cc"].split(";"):
          if len(emailAddress) > 0:
            gcEmail.addToAlias(emailAddress)
    
      if len(campaignMessageItem_dict["bcc"].split(";")) > 0 and len(campaignMessageItem_dict["bcc"].split(";")[0]) > 0:
        for emailAddress in campaignMessageItem_dict["bcc"].split(";"):
          if len(emailAddress) > 0:
            gcEmail.addToAlias(emailAddress)
    
      gcEmail.setSubject(campaignMessageItem_dict["subject"])
      
      gcEmail.setConext(campaignMessageItem_dict["body"])
      
      gcEmail.sendEmail()
      thisCampaignNameMessage_list.append(
        {
          "sent":getDateString("now"),
          **campaignMessageItem_dict,
          "errorReason":""
        }
      )
    
    except Exception as e:
      thisCampaignNameMessage_list.append(
        {
          "sent":"failed",
          **campaignMessageItem_dict,
          "errorReason":logException(f"unable to send an email with campaignMessageItem_dict:[{campaignMessageItem_dict}]")
        }
      )
      errorReason_list.append(f"unable to send an email with campaignMessageItem_dict:[{campaignMessageItem_dict}]")

    #comment out the following: break before it's send
    #break
  
  return thisCampaignNameMessage_list