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

from graphcode.lib import getDateString

from pathway import requests

from tammy.midway import Midway
from graphcode.parse import GcParse

from wooju.tammy import getInput_dict, getArgument_dict

import json

import time

from uuid import uuid4
from wooju.args import getDanteScriptId

class Dante(Midway):
  def __init__(self, request_dict, logMessage_list, errorReason_list):
    Midway.__init__(self, request_dict, logMessage_list, errorReason_list)

    self.danteState_dict = {
      "SUBMITTED":{},
      "SUCCESSFUL":{},
      "FAILED":{}
      }
    
    self.danteTimeout = 900
    self.maxRetryCount =  3
    self.maxChckInRetryCount = 0
    self.maxExcuteRetryCount = 0
    self.danteStatusPollingTime = 0.5
    self.nextTokenPollingTime = 0.25
    self.scriptOutputNotYetCreatedExceptionPollingTime = 1
  
  def getPollingTime(self, argument_dict):
    regionCount = 0
    accountCount = 0
    domainCount = 0
    for argumentName in argument_dict.keys():
      if argumentName.lower().startswith("region"):
        if isinstance(argument_dict[argumentName], str):
          regionCount = len(argument_dict[argumentName].strip().split(","))
        elif isinstance(argument_dict[argumentName], list):
          regionCount = len(argument_dict[argumentName])
        else:
          logWarn("unexpected {}:{}:[{}]".format(type(argument_dict[argumentName]).__name__, argumentName, argument_dict[argumentName]))
      
      elif argumentName.lower().startswith("account"):
        if isinstance(argument_dict[argumentName], str):
          for accountId_str in argument_dict[argumentName].strip().split(","):
            try:
              if int(accountId_str) < 1000000000000 and int(accountId_str) > 0:
                accountCount += 1
              else:
                logWarn("unexpected accountId:[{}]".foramt(accountId_str))
            except:
              if len(accountId_str.strip()) > 2 and len(accountId_str.strip().split(".")) > 0:
                domainCount += 1
              else:
                logWarn("unexpected domainId:[{}]".foramt(accountId_str))
                
        elif isinstance(argument_dict[argumentName], list):
          for accountId in argument_dict[argumentName]:
            try:
              if isinstance(accountId, str) and int(accountId_str) < 1000000000000 and int(accountId_str) > 0:
                accountCount += 1
              elif isinstance(accountId, int) and accountId_str < 1000000000000 and accountId_str > 0:
                accountCount += 1
              else:
                logWarn("unexpected accountId:[{}]".foramt(accountId_str))
            except:
              if isinstance(accountId, str) and len(accountId_str.strip()) > 2 and len(accountId_str.strip().split(".")) > 0:
                domainCount += 1
              else:
                logWarn("unexpected domainId:[{}]".foramt(accountId_str))
        else:
          logWarn("unexpected {}:{}:[{}]".format(type(argument_dict[argumentName]).__name__, argumentName, argument_dict[argumentName]))
          
    pollingTime = regionCount * 0.125 + accountCount + 0.125 + domainCount * 1.5
    logDebug("pollingTime:[{:,.2f}]s".format(pollingTime))
    
    return pollingTime
  
  def getDanteEndpoint(self, argument_dict):
    if "scriptInput" in argument_dict.keys():
      if "region" in argument_dict["scriptInput"].keys():
        
        if isinstance(argument_dict["scriptInput"]["region"], str):
          if argument_dict["scriptInput"]["region"].lower().startswith("cn-"):
            raiseValueError("regionCode:[{}} is not supported yet".format(argument_dict["region"]))
          else:
            return "https://prod.global.dante.support.aws.dev/midway/execution"
          
        elif isinstance(argument_dict["scriptInput"]["region"], list):
        
          for thisRegionCode in argument_dict["scriptInput"]["region"]:
            if thisRegionCode.lower().startswith("cn-"):
              raiseValueError("regionCode:[{}} is not supported yet".format(thisRegionCode))
            
          return "https://prod.global.dante.support.aws.dev/midway/execution"
      
      else:
        logWarn(f"'region' is not found at ''scriptInput' at argument_dict.keys():[{argument_dict.keys()}]")
        return "https://prod.global.dante.support.aws.dev/midway/execution"
      
    else:
      logWarn(f"'scriptInput' is not found at argument_dict")
      return "https://prod.global.dante.support.aws.dev/midway/execution"
    
  def getDanteUrl(self, argument_dict, danteResult_dict=None):
    if danteResult_dict in [None]:
      return self.getDanteEndpoint(argument_dict)
    
    elif "executionStatus" in danteResult_dict.keys() and danteResult_dict["executionStatus"] in ["SUBMITTED"]:
      return "{}/{}/status".format(self.getDanteEndpoint(argument_dict), danteResult_dict["executionId"])
    
    elif "lastToken" in danteResult_dict.keys():
      return "{}/{}/output?continuationToken={}".format(self.getDanteEndpoint(argument_dict), danteResult_dict["executionId"], danteResult_dict["lastToken"])
    elif "nextToken" in danteResult_dict.keys():
      return "{}/{}/output?continuationToken={}".format(self.getDanteEndpoint(argument_dict), danteResult_dict["executionId"], danteResult_dict["nextToken"])
    else:
      return "https://prod.global.dante.support.aws.dev/midway/execution/{}/output".format(danteResult_dict["executionId"])
        
  def danteRequest(self, url, argument_dict):
    try:
      retryCount = 0
      while retryCount < self.maxRetryCount or retryCount < self.maxChckInRetryCount:
        try:
          if "/status" not in url:
            status = False
          
            r = self.sessionRequest(url=url, payload="OPTIONS")
            #logDebug("#checkIn:[{}]".format(r.content))

          else:
            status = True
            
          if status or (r.status_code >= 200 and r.status_code < 400) :
            
            retryCount = 0
            while retryCount < self.maxRetryCount or retryCount < self.maxExcuteRetryCount:
              try:
                #logDebug(f"#url:[{url}]")
                #logDebug(f"#argument_dict:[{argument_dict}]")
                
                r = self.sessionRequest(url=url, payload=argument_dict)
                danteResult_dict = json.loads(r.content.decode())
                #logDebug("#===>danteResult_dict:[{}]".format(danteResult_dict))

                if r.status_code >= 200 and r.status_code < 400:
                  return danteResult_dict
                
                elif danteResult_dict["errorType"] in ["ScriptOutputNotYetCreatedException"]:
                  #logWarn("url:[{}] is yet created. sleeping:[{:,.2f}]s".format(url, self.scriptOutputNotYetCreatedExceptionPollingTime))
                  time.sleep(self.scriptOutputNotYetCreatedExceptionPollingTime)
                
                elif danteResult_dict["errorType"] in ["ScriptOutputNotFoundException"]:
                  logWarn("url:[{}] is not found.".format(url))
                  
                  return danteResult_dict
                
                elif danteResult_dict["errorType"] in ["InvalidRequestException"]:
                  logError("url:[{}] is not found.".format(url))
                  
                  return danteResult_dict
                  
                else:
                  raiseValueError("unexpected status_code:{}:[{}]".format(r.status_code, r.content.decode()))
            
              except:
                retryCount += 1
                logExceptionWithValueError("(#retryCount:{:,})\tunexpected response [{}]:{}".format(retryCount, argument_dict, url))
            
          else:
            raiseValueError("unexpected status_code:{}:[{}]".format(r.status_code, r.content.decode()))
      
        except:
          retryCount += 1
          logExceptionWithValueError("(#retryCount:{:,})\tunexpected response [{}]:{}".format(retryCount, argument_dict, url))
      
    except: 
      raiseValueError("failed to danteRequest:{}:[{}]".format(url, argument_dict))
     
  def execute(self, argument_dict):
    try:
      danteUrl=self.getDanteUrl(argument_dict)
      logDebug("danteUrl:[{}]".format(danteUrl))
      
      danteResults = self.danteRequest(url=danteUrl, argument_dict=argument_dict)
      logDebug("danteResults:[{}]".format(danteResults))

      return danteResults
    
    except:
      logException(f"failed to execute:{danteUrl}:[{argument_dict}]")
  
  def status(self, argument_dict, danteExecutionResult_dict):
    try:
      danteUrl=self.getDanteUrl(argument_dict, danteResult_dict=danteExecutionResult_dict)
      logDebug("danteUrl:[{}]".format(danteUrl))
      
      while True:
        danteStatusResult_dict = self.danteRequest(url=danteUrl, argument_dict=None)
        
        if danteStatusResult_dict["currentState"] in ["SUBMITTED"]:
          time.sleep(self.danteStatusPollingTime)
        else:
          return {
                  "executionId": danteExecutionResult_dict["executionId"],
                  **danteStatusResult_dict
                  }
        
    except:
      logException(f"failed to execute:{danteUrl}:[{argument_dict}]")
  
  
  def getDanteOutput(self, url, danteOutput_dict):
    if "outputSource" in danteOutput_dict.keys():
      if "url" in danteOutput_dict["outputSource"]:
        r = self.request(danteOutput_dict["url"])
        try:
          return {
            "url": url,
            "outputSource": danteOutput_dict["outputSource"],
            "ourputUrl": danteOutput_dict["url"],
            "output": json.loads(r.content.decode())
            }
        except:
          return {
            "url": url,
            "outputSource": danteOutput_dict["outputSource"],
            "ourputUrl": danteOutput_dict["url"],
            "output": r.content.decode()
            }
          
      
      elif "output" in danteOutput_dict["outputSource"]:
        return {
          "url": url,
          "outputSource": danteOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": danteOutput_dict["output"]
          }
      
      elif danteOutput_dict["outputSource"] in danteOutput_dict.keys():
        logWarn("outputSource:[{}] is not supported yet".format(danteOutput_dict["outputSource"]))
        return {
          "url": url,
          "outputSource": danteOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": danteOutput_dict[danteOutput_dict["outputSource"]]
          }
      else:
        logWarn("outputSource:[{}] is not supported yet".format(danteOutput_dict["outputSource"]))
        return {
          "url": url,
          "outputSource": danteOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": danteOutput_dict
          }
    else:
      logWarn("outputSource is not found".format(danteOutput_dict["outputSource"]))
      return {
        "url": url,
        "outputSource": None,
        "ourputUrl": None,
        "output": danteOutput_dict
        }
      
  def output(self, argument_dict, danteStatusResult_dict):
    danteResult_list = []
    
    nextToken_list = []
    try:
      danteUrl=self.getDanteUrl(argument_dict, danteResult_dict=danteStatusResult_dict)
      logDebug("danteUrl:[{}]".format(danteUrl))
      
      try:
        while True:
          try:
            danteOutput_dict = self.danteRequest(url=danteUrl, argument_dict=None)
          except Exception as e:
            logDebug("ERROR:[{}]".format(e))
            time.sleep(1)
            
          danteOutput_dict["executionId"] = danteStatusResult_dict["executionId"]
          
          danteResult_list.append(self.getDanteOutput(url=danteUrl, danteOutput_dict=danteOutput_dict))
          logDebug("#total {:,} results are retrieved from dante".format(len(danteResult_list)))
          
          if "nextToken" in danteOutput_dict.keys() and len(danteOutput_dict["nextToken"].strip()) > 0:
            if danteOutput_dict["nextToken"] in nextToken_list:
              logWarn("nextToken:[{}] was requested".format(danteOutput_dict["nextToken"]))
              time.sleep(self.nextTokenPollingTime)
            else:
              nextToken_list.append(danteOutput_dict["nextToken"])
              danteUrl=self.getDanteUrl(argument_dict, danteResult_dict=danteOutput_dict)
              #logDebug("danteUrl:[{}]".format(danteUrl))
            
          else:
            break
          
          #logDebug("danteOutput_dict:[{}]".format(danteOutput_dict))
          
        return danteResult_list
          
      except:
        raiseValueError(f"failed to execute:{danteUrl}:[{argument_dict}]")
    
    except:
      raiseValueError(f"failed to get danteUrl with argument_dict:[{argument_dict}]")
  
  def get(self, input_dict, argument_dict):
    try:
      danteExecutionResult_dict = self.execute(argument_dict=argument_dict)
      logDebug("danteExecutionResult_dict:[{}]".format(danteExecutionResult_dict))
      try:
        danteStatusResult_dict = self.status(argument_dict=argument_dict, 
                                             danteExecutionResult_dict=danteExecutionResult_dict)
        logDebug("danteStatusResult_dict:[{}]".format(danteStatusResult_dict))
      
        try:
          danteOutputResult_list = self.output(argument_dict=argument_dict, 
                                               danteStatusResult_dict=danteStatusResult_dict)
          if len(danteOutputResult_list) > 0:
            logDebug("danteOutputResult_list(len:{:,})][-1]:[{}]".format(len(danteOutputResult_list), danteOutputResult_list[-1]))
          else:
            logDebug("danteOutputResult_list(len:{:,})]:[{}]".format(len(danteOutputResult_list), danteOutputResult_list))
          
          danteResults_dict = self.updateDanteResults(danteOutputResult_list)

          gcParse = GcParse(result=danteResults_dict["info"], inputs=input_dict, payload=argument_dict)
          danteResults_dict["info"] = gcParse.get()
          
          gcParse = GcParse(result=danteResults_dict["results"], inputs=input_dict, payload=argument_dict)
          danteResults_dict["results"] = gcParse.get()

          return danteResults_dict
        
        except:
          logException("unexpected error status:argument_dict:[{}]".format(argument_dict))
          
      except:
        logException("unexpected error status:argument_dict:[{}]".format(argument_dict))
        
    except:
      logException("unexpected error execute:argument_dict:[{}]".format(argument_dict))
      
  def updateDanteResults(self, danteOutputResult_list):
    danteResult_dict = {
      "info": [],
      "results": [],
      "errors": []
    }
    resultCount = 0
    for danteOutputResultItem_dict in danteOutputResult_list:
      #logDebug(f"[{resultCount:,}]\t{type(danteOutputResultItem_dict).__name__}:danteOutputResultItem_dict:[{danteOutputResultItem_dict}]")
      resultCount += 1
      try:
        if "output" in danteOutputResultItem_dict.keys():
          if isinstance(danteOutputResultItem_dict["output"], str):
            try:
              danteOutputResultItem_dict["output"] = json.loads(danteOutputResultItem_dict["output"].strip())
            except:
              logWarn("failed to json.loads(danteOutputResultItem_dict[\"output\"])")
              danteResult_dict["errors"].append({"errors":danteOutputResultItem_dict["output"]})

          if isinstance(danteOutputResultItem_dict["output"], dict):
            if "info" in danteOutputResultItem_dict["output"].keys():
              danteResult_dict["info"].append(danteOutputResultItem_dict["output"])
            
            elif "results" in danteOutputResultItem_dict["output"].keys():
              if isinstance(danteOutputResultItem_dict["output"]["results"], list):
                for danteResultItem_dict in danteOutputResultItem_dict["output"]["results"]:
                  try:
                    for key in danteResultItem_dict.keys():
                      if isinstance(danteResultItem_dict[key], str) \
                            and len(danteResultItem_dict[key]) > 2 \
                            and (danteResultItem_dict[key][0] in ["{"] and danteResultItem_dict[key][-1] in ["}"]) \
                            and (danteResultItem_dict[key][0] in ["["] and danteResultItem_dict[key][-1] in ["]"]):
                        try:
                          danteResultItem_dict[key] = json.loads(danteResultItem_dict[key])
                        except:
                          pass
                  except:
                    pass

                  danteResult_dict["results"].append(danteResultItem_dict)
              
              else:
                danteResult_dict["results"].append({"results":danteOutputResultItem_dict["output"]["results"]}) 
            
            else:
              danteResult_dict["errors"].append(danteOutputResultItem_dict["output"])
          
          else:
            danteResult_dict["errors"].append({"errors":danteOutputResultItem_dict["output"]})
        
        else:
          danteResult_dict["errors"].append(danteOutputResultItem_dict)
      
      except:
        danteResult_dict["errors"].append({"errors":danteOutputResultItem_dict})

    return danteResult_dict
  
  def listScripts(self):
    url = "https://read.us-east-2.prod.contribution-model.support.aws.dev/listPromotedAssets"
    r = self.sessionRequest(url=url, payload="OPTIONS")
    logDebug("#checkIn:[{}]".format(r.content))

    r = self.sessionRequest(url=url, payload={"tenantId": "aws"})
    try:
      logDebug("#promotedAssets:[{}]".format(r.content.decode()))

      return json.loads(r.content.decode())
    except:
      return {
        "error": logException("unable to list dante scripts")
      }
    
def executeDante(userAccountId = None, loginAliasId = "hoeseong"):
  
  if False:
    dantePayload_dict = {
      "executionType": "ASYNCHRONOUS",
      "script": {
        "id": "CloudWatch-SSS_contributionmodelasset_CloudWatch-SSS"
        },
      "scriptInput": {
        "region": "us-east-1",
        "accountId": "000000000000",
        "apiName": "ec2.describeRegions",
        "inputArgsAsJson": {}
        }
      }
  elif True:
    dantePayload_dict = {
      "executionType": "ASYNCHRONOUS",
      "script": {
        "id": "CloudWatch-SSS_contributionmodelasset_CloudWatch-SSS"
        },
      "scriptInput": {
        "region": "us-east-1",
        "accountId": "000000000000",
        "apiName": "kumoscp.searchCustomers",
        "inputArgsAsJson": {"searchFilter": "EMAIL", "searchFilterValue": "hoeseong", "requestedBy": "hoeseong@"}
        }
      }
  else:  
    dantePayload_dict = {
      "executionType":"ASYNCHRONOUS",
      "script":{
        "id":"K2-ec2_contributionmodelasset_Dante-curated-ec2",
        "tenantId":"aws"
        },
      "scriptInput":{
        "region":["eu-north-1","me-south-1","ap-south-1","eu-west-3","ap-southeast-3","us-east-2","af-south-1","eu-west-1","me-central-1","eu-central-1","sa-east-1","ap-east-1","ap-south-2","us-east-1","ap-northeast-2","ap-northeast-3","eu-west-2","ap-southeast-4","eu-south-1","ap-northeast-1","us-west-2","us-west-1","ap-southeast-1","ap-southeast-2","ca-central-1","eu-south-2","eu-central-2"],
        "accountsOrDomains":"000000000000"
      }
    }
  dante = Dante(userAccountId = "749952098923", loginAliasId = loginAliasId)
  danteResult_dict = dante.get(argument_dict=dantePayload_dict)
  logDebug("danteResult_dict:[{}]".format(danteResult_dict))
  
def localUnitTest():
  unitTestFunction_dict = {
    "executeDante":{"target":executeDante, "args":()},
    }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()
    