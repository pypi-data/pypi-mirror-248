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

from tammy.midway import PdxMidway
from tammy.cmApi import parseCMApi

import json

import time

import secrets
from os.path import expanduser

class CMApi(PdxMidway):
  def __init__(self, userAccountId, loginAliasId):
    PdxMidway.__init__(self, userAccountId, loginAliasId)
    
    self.cmApiState_dict = {
      "SUBMITTED":{},
      "SUCCESSFUL":{},
      "FAILED":{}
      }
    
    self.parseRequest_dict = {
      'apiName':'tammy._cmApi.parserCMApi',
      'async': False,
      'metadata': {
          'awsAccountId':userAccountId,
          'userName':loginAliasId,
        },
      "attributes": None,
      'sessionToken':"p0cx3w0lmUNLf2rW1KL-0Z_m1zYE_eFFI9BuSa-zTUv0cp1nVjhDv_EHR4QaFYt",
      "__processBeginTime__": time.time()
      }
    
    self.cmApiTimeout = 900
    self.maxRetryCount =  3
    self.maxChckInRetryCount = 0
    self.maxExcuteRetryCount = 0
    self.cmApiStatusPollingTime = 0.5
    self.nextTokenPollingTime = 0.25
    self.scriptOutputNotYetCreatedExceptionPollingTime = 1
  
  def getPollingTime(self, payload_dict):
    regionCount = 0
    accountCount = 0
    domainCount = 0
    for argumentName in payload_dict.keys():
      if argumentName.lower().startswith("region"):
        if isinstance(payload_dict[argumentName], str):
          regionCount = len(payload_dict[argumentName].strip().split(","))
        elif isinstance(payload_dict[argumentName], list):
          regionCount = len(payload_dict[argumentName])
        else:
          logWarn("unexpected {}:{}:[{}]".format(type(payload_dict[argumentName]).__name__, argumentName, payload_dict[argumentName]))
      
      elif argumentName.lower().startswith("account"):
        if isinstance(payload_dict[argumentName], str):
          for accountId_str in payload_dict[argumentName].strip().split(","):
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
                
        elif isinstance(payload_dict[argumentName], list):
          for accountId in payload_dict[argumentName]:
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
          logWarn("unexpected {}:{}:[{}]".format(type(payload_dict[argumentName]).__name__, argumentName, payload_dict[argumentName]))
          
    pollingTime = regionCount * 0.125 + accountCount + 0.125 + domainCount * 1.5
    logDebug("pollingTime:[{:,.2f}]s".format(pollingTime))
    
    return pollingTime
  
  def getCMApiEndpoint(self, payload_dict):
    if isinstance(payload_dict["scriptInput"]["region"], str):
      if payload_dict["scriptInput"]["region"].lower().startswith("cn-"):
        raiseValueError("region:[{}} is not supported yet".format(payload_dict["region"]))
      else:
        return "https://prod.global.cmApi.support.aws.dev/midway/execution"
      
    elif isinstance(payload_dict["scriptInput"]["region"], list):
    
      for thisRegionCode in payload_dict["scriptInput"]["region"]:
        if thisRegionCode.lower().startswith("cn-"):
          raiseValueError("region:[{}} is not supported yet".format(payload_dict["scriptInput"]["region"]))
        else:
          return "https://prod.global.cmApi.support.aws.dev/midway/execution"
    else:
      raiseValueError("unsupported {}:region:[{}]".format(type(payload_dict["region"]).__name__, payload_dict["region"]))
  
  def getCMApiUrl(self, payload_dict, cmApiResult_dict=None):
    if cmApiResult_dict in [None]:
      return self.getCMApiEndpoint(payload_dict)
    
    elif "executionStatus" in cmApiResult_dict.keys() and cmApiResult_dict["executionStatus"] in ["SUBMITTED"]:
      return "{}/{}/status".format(self.getCMApiEndpoint(payload_dict), cmApiResult_dict["executionId"])
    
    elif "lastToken" in cmApiResult_dict.keys():
      return "{}/{}/output?continuationToken={}".format(self.getCMApiEndpoint(payload_dict), cmApiResult_dict["executionId"], cmApiResult_dict["lastToken"])
    elif "nextToken" in cmApiResult_dict.keys():
      return "{}/{}/output?continuationToken={}".format(self.getCMApiEndpoint(payload_dict), cmApiResult_dict["executionId"], cmApiResult_dict["nextToken"])
    else:
      return "https://prod.global.cmApi.support.aws.dev/midway/execution/{}/output".format(cmApiResult_dict["executionId"])
        
  def cmApiRequest(self, url, payload_dict):
    try:
      retryCount = 0
      while retryCount < self.maxRetryCount or retryCount < self.maxChckInRetryCount:
        try:
          if "/status" not in url:
            status = False
          
            r = self.sessionRequest(url=url, payload="OPTIONS")
            #logDebug("#checkIn:[{}]".format(json.loads(r.content.decode())))

          else:
            status = True
            
          if status or (r.status_code >= 200 and r.status_code < 400) :
            
            retryCount = 0
            while retryCount < self.maxRetryCount or retryCount < self.maxExcuteRetryCount:
              try:
                r = self.sessionRequest(url=url, payload=payload_dict)
                cmApiResult_dict = json.loads(r.content.decode())
                logDebug("#cmApiResult_dict:[{}]".format(cmApiResult_dict))
            
                if r.status_code >= 200 and r.status_code < 400:
                  return cmApiResult_dict
                
                elif "errorType" in cmApiResult_dict.keys():
                  if cmApiResult_dict["errorType"] in ["ScriptOutputNotYetCreatedException"]:
                    logWarn("url:[{}] is yet created. sleeping:[{:,.2f}]s".format(url, self.scriptOutputNotYetCreatedExceptionPollingTime))
                    time.sleep(self.scriptOutputNotYetCreatedExceptionPollingTime)

                  elif cmApiResult_dict["errorType"] in ["ScriptOutputNotFoundException"]:
                    logWarn("url:[{}] is not found.".format(url))
                    
                    return cmApiResult_dict
                  
                  elif cmApiResult_dict["errorType"] in ["InvalidRequestException"]:
                    logError("url:[{}] is not found.".format(url))
                    
                    return cmApiResult_dict

                  else:
                    raiseValueError("unexpected errorType:{}:[{}]".format(r.status_code, cmApiResult_dict["errorType"]))
                    
                else:
                  raiseValueError("unexpected status_code:{}:[{}]".format(r.status_code, r.content.decode()))
            
              except:
                retryCount += 1
                logExceptionWithValueError("(#retryCount:{:,})\tunexpected response [{}]:{}".format(retryCount, payload_dict, url))
            
          else:
            raiseValueError("unexpected status_code:{}:[{}]".format(r.status_code, r.content.decode()))
      
        except:
          retryCount += 1
          logExceptionWithValueError("(#retryCount:{:,})\tunexpected response [{}]:{}".format(retryCount, payload_dict, url))
      
    except: 
      raiseValueError("failed to cmApiRequest:{}:[{}]".format(url, payload_dict))
     
  def execute(self, payload_dict):
    try:
      cmApiUrl=self.getCMApiUrl(payload_dict)
      logDebug("cmApiUrl:[{}]".format(cmApiUrl))
      
      return self.cmApiRequest(url=cmApiUrl, payload_dict=payload_dict)
    except:
      logException("failed to execute:{}:[{}]".format(payload_dict))
  
  def status(self, payload_dict, cmApiExecutionResult_dict):
    try:
      cmApiUrl=self.getCMApiUrl(payload_dict, cmApiResult_dict=cmApiExecutionResult_dict)
      logDebug("cmApiUrl:[{}]".format(cmApiUrl))
      
      while True:
        cmApiStatusResult_dict = self.cmApiRequest(url=cmApiUrl, payload_dict=None)
        
        if cmApiStatusResult_dict["currentState"] in ["SUBMITTED"]:
          time.sleep(self.cmApiStatusPollingTime)
        else:
          return {
                  "executionId": cmApiExecutionResult_dict["executionId"],
                  **cmApiStatusResult_dict
                  }
        
    except:
      logException("failed to execute:{}:[{}]".format(payload_dict))
  
  
  def getCMApiOutput(self, url, cmApiOutput_dict):
    if "outputSource" in cmApiOutput_dict.keys():
      if "url" in cmApiOutput_dict["outputSource"]:
        r = self.request(cmApiOutput_dict["url"])
        try:
          return {
            "url": url,
            "outputSource": cmApiOutput_dict["outputSource"],
            "ourputUrl": cmApiOutput_dict["url"],
            "output": json.loads(r.content.decode())
            }
        except:
          return {
            "url": url,
            "outputSource": cmApiOutput_dict["outputSource"],
            "ourputUrl": cmApiOutput_dict["url"],
            "output": r.content.decode()
            }
          
      
      elif "output" in cmApiOutput_dict["outputSource"]:
        return {
          "url": url,
          "outputSource": cmApiOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": cmApiOutput_dict["output"]
          }
      
      elif cmApiOutput_dict["outputSource"] in cmApiOutput_dict.keys():
        logWarn("outputSource:[{}] is not supported yet".format(cmApiOutput_dict["outputSource"]))
        return {
          "url": url,
          "outputSource": cmApiOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": cmApiOutput_dict[cmApiOutput_dict["outputSource"]]
          }
      else:
        logWarn("outputSource:[{}] is not supported yet".format(cmApiOutput_dict["outputSource"]))
        return {
          "url": url,
          "outputSource": cmApiOutput_dict["outputSource"],
          "ourputUrl": None,
          "output": cmApiOutput_dict
          }
    else:
      logWarn("outputSource is not found".format(cmApiOutput_dict["outputSource"]))
      return {
        "url": url,
        "outputSource": None,
        "ourputUrl": None,
        "output": cmApiOutput_dict
        }
      
  def output(self, payload_dict, cmApiStatusResult_dict):
    cmApiResult_list = []
    
    nextToken_list = []
    try:
      cmApiUrl=self.getCMApiUrl(payload_dict, cmApiResult_dict=cmApiStatusResult_dict)
      logDebug("cmApiUrl:[{}]".format(cmApiUrl))
      
      while True:
        try:
          cmApiOutput_dict = self.cmApiRequest(url=cmApiUrl, payload_dict=None)
        except Exception as e:
          logDebug("ERROR:[{}]".format(e))
          time.sleep(1)
          
        cmApiOutput_dict["executionId"] = cmApiStatusResult_dict["executionId"]
        
        cmApiResult_list.append(self.getCMApiOutput(url=cmApiUrl, cmApiOutput_dict=cmApiOutput_dict))
        logDebug("#total {:,} results are retrieved from cmApi".format(len(cmApiResult_list)))
        
        if "nextToken" in cmApiOutput_dict.keys() and len(cmApiOutput_dict["nextToken"].strip()) > 0:
          if cmApiOutput_dict["nextToken"] in nextToken_list:
            logWarn("nextToken:[{}] was requested".format(cmApiOutput_dict["nextToken"]))
            time.sleep(self.nextTokenPollingTime)
          else:
            nextToken_list.append(cmApiOutput_dict["nextToken"])
            cmApiUrl=self.getCMApiUrl(payload_dict, cmApiResult_dict=cmApiOutput_dict)
            #logDebug("cmApiUrl:[{}]".format(cmApiUrl))
          
        else:
          break
        
        #logDebug("cmApiOutput_dict:[{}]".format(cmApiOutput_dict))
        
      return cmApiResult_list
        
    except:
      logException("failed to execute:{}:[{}]".format(payload_dict))
  
  def get(self, payload_dict):
    try:
      cmApiExecutionResult_dict = self.execute(payload_dict=payload_dict)
      logDebug("cmApiExecutionResult_dict:[{}]".format(cmApiExecutionResult_dict))
      try:
        cmApiStatusResult_dict = self.status(payload_dict=payload_dict, 
                                             cmApiExecutionResult_dict=cmApiExecutionResult_dict)
        logDebug("cmApiStatusResult_dict:[{}]".format(cmApiStatusResult_dict))
      
        try:
          cmApiOutputResult_list = self.output(payload_dict=payload_dict, 
                                               cmApiStatusResult_dict=cmApiStatusResult_dict)
          if len(cmApiOutputResult_list) > 0:
            logDebug("cmApiOutputResult_list(len:{:,})][-1]:[{}]".format(len(cmApiOutputResult_list), cmApiOutputResult_list[-1]))
          else:
            logDebug("cmApiOutputResult_list(len:{:,})]:[{}]".format(len(cmApiOutputResult_list), cmApiOutputResult_list))
          
          self.parseRequest_dict["attributes"]={
            "cmApiResults": cmApiOutputResult_list
            }
          return parseCMApi(self.parseRequest_dict)
        
        except:
          logException("unexpected error status:payload_dict:[{}]".format(payload_dict))
          
      except:
        logException("unexpected error status:payload_dict:[{}]".format(payload_dict))
        
    except:
      logException("unexpected error execute:payload_dict:[{}]".format(payload_dict))
      

def executeCMApi(userAccountId = None, loginAliasId = "hoeseong"):
  
  cmApi = CMApi(userAccountId = "749952098923", loginAliasId = loginAliasId)
  
  url = "https://command-center.support.aws.a2z.com/sso/login"#"https://command-center.support.aws.a2z.com/customers#/my-customers"
  r = cmApi.request(url=url)
  try:
    r_dict = json.loads(r.content.decode())
    logDebug("1\tr_dict:[{}]".format(r_dict))
    
    url = r_dict["authn_endpoint"]
    r = cmApi.request(url=url)
    logDebug("2\tr_content:[{}]".format(r.content.decode()))
    midwaySessionToken = r.content.decode()
    
    url = "https://command-center.support.aws.a2z.com/sso/login?id_token={}".format(midwaySessionToken)
    r = cmApi.request(url=url)
    logDebug("3\tr_content:[{}]".format(r.content.decode()))
    
    url = "https://cognito-identity.us-east-1.amazonaws.com/"
    poolId_dict = {"IdentityPoolId":"us-east-1:39a7a18e-9f1d-4fa1-9c5a-e4f7d98dfc98"}
    cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
    cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
    cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
    cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
    cmApi.addHeaders("Sec-Fetch-Dest", "empty")
    cmApi.addHeaders("Sec-Fetch-Mode", "cors")
    cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
    cmApi.addHeaders("TE", "trailers")
    cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetId")
    r = cmApi.request(url=url, payload=poolId_dict)
    identityId_dict = json.loads(r.content.decode())
    logDebug("4\identityId_dict:[{}]".format(identityId_dict))
    
    url = "https://cognito-identity.us-east-1.amazonaws.com/"
    payload_dict = json.loads(r.content.decode())
    cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
    cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
    cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
    cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
    cmApi.addHeaders("Sec-Fetch-Dest", "empty")
    cmApi.addHeaders("Sec-Fetch-Mode", "cors")
    cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
    cmApi.addHeaders("TE", "trailers")
    cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetOpenIdToken")
    r = cmApi.request(url=url, payload=payload_dict)
    r_dict = json.loads(r.content.decode())
    logDebug("5\tr_dict:[{}]".format(r_dict))
    cognitoSessionToken = r_dict["Token"]
    identityId = r_dict["IdentityId"]
    logDebug("5\tcognitoSessionToken:[{}]".format(cognitoSessionToken))
    logDebug("5\t{}:identityId:[{}]".format(type(identityId).__name__, identityId))
    
    payload_dict = json.loads(r.content.decode())
    url = "https://cognito-identity.us-east-1.amazonaws.com"
    r = cmApi.request(url=url, payload="OPTIONS")
    logDebug("6\tr.content:[{}]".format(r.content))
    
    #payload = {
    #  "Logins":{
    #    "midway-auth.amazon.com":"eyJ0eXAiOiJKV1MiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEyODUwNzcyIn0.eyJpc3MiOiJodHRwczovL21pZHdheS1hdXRoLmFtYXpvbi5jb20iLCJzdWIiOiJob2VzZW9uZyIsImF1ZCI6ImNvbW1hbmQtY2VudGVyLnN1cHBvcnQuYXdzLmEyei5jb20iLCJleHAiOjE2ODM5MTUxNjUsImlhdCI6MTY4MzkxNDI2NSwiYXV0aF90aW1lIjoxNjgzOTAyMjEyLCJub25jZSI6IlRMRjlUaFF4SUxRZXpObTZQUURiaXJZOURqcGlEZ2VpZnRsbWlwZXNNT0xoY0tmYVZKcUgyVnh1OUIzVWFXd2ciLCJhbXIiOiJbXCJwaW5cIiwgXCJ1MmZcIiwgXCJwZXNcIl0iLCJ0cnVzdF9zY29yZSI6MSwicmVxX2lkIjoiZDRiNTIzZDEtOTJiOS00OWJmLThhNDEtODZhYzIyYzEzZmY4IiwibWlkd2F5X3RydXN0X3Njb3JlIjpudWxsLCJhcGVzX3Jlc3VsdHMiOnsiVFpfQ09SUF9MQVBUT1AiOnsicGFzcyI6dHJ1ZSwic3RhdHVzIjoiU1VDQ0VTUyIsImZhaWx1cmVCbG9ja3NBY2Nlc3MiOmZhbHNlLCJjbGFpbXMiOltdLCJzdGVwdXBDbGFpbXMiOltdfSwiVFpfQ09SUCI6eyJwYXNzIjp0cnVlLCJzdGF0dXMiOiJTVUNDRVNTIiwiZmFpbHVyZUJsb2Nrc0FjY2VzcyI6dHJ1ZSwiY2xhaW1zIjpbXSwic3RlcHVwQ2xhaW1zIjpbXX19LCJpYWwiOjMsImFhbCI6MywianRpIjoibWRZd2l1MnlTTFp1YlVmU2d6SFhNZz09IiwicG9zdHVyZV9jaGVjayI6MSwibXdpIjowfQ.pjlDLqgusP4iy5JCK4pFvwDvK4FCtVYQUbTc3WBO350ojrqVoz8h3iFwtcu6w7xI2arvsV4IAuoCeJCZs9IC2kDJf6mFwGMiyGXaSL23BU_BU1hNOOIBdngZcIeiXb97hv9OgCJ0wwAMx6p6ZeTsWUX6J_Jmsn-ubt8GSZrvRX6JjTuQR_l-h5O3_pVmhxqcUwLXh4QxHH5kE7T9RcTLFRTHFaoJoD9gtbbBiFHGDAH_WN1knpn9TMXspjenObPc3rOKAgAGgRe-yG21Pnr-zzn7RCfSI__zdzDiNkrWQw1iuhywTbAZWre_xthKfj6WQjn9ul5H9za7R9LHPp1rKw"
    #    },
    #  "IdentityId":"us-east-1:433c9c25-8ed6-4bce-b4e6-7eb4a43be8c8"
    #}
    payload = {
      "Logins":{
        "midway-auth.amazon.com":midwaySessionToken
        },
      **poolId_dict
      }
    cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
    cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
    cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
    cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
    cmApi.addHeaders("Sec-Fetch-Dest", "empty")
    cmApi.addHeaders("Sec-Fetch-Mode", "cors")
    cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
    cmApi.addHeaders("TE", "trailers")
    cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetId")
    r = cmApi.request(url=url, payload=payload)
    logDebug("7\tr.content:[{}]".format(r.content))
    
    payload = {
      "IdentityId": identityId,
      "Logins":{
        "midway-auth.amazon.com":midwaySessionToken
        }
      }
    cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
    cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
    cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
    cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
    cmApi.addHeaders("Sec-Fetch-Dest", "empty")
    cmApi.addHeaders("Sec-Fetch-Mode", "cors")
    cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
    cmApi.addHeaders("TE", "trailers")
    cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetCredentialsForIdentity")
    r = cmApi.request(url=url, payload=payload)
    logDebug("8\tr.content:[{}]".format(r.content))
   
    
  except:
    logException("unexpected response:{}:[{}]".format(r.status_code, r.content.decode()))
  
  exit()
  
  
  
def loginCognito():
  cmApi = CMApi(userAccountId = "749952098923", loginAliasId = "hoeseong")
  
  
  url = "https://command-center.support.aws.a2z.com/sso/login"#"https://command-center.support.aws.a2z.com/customers#/my-customers"
  cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
  cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
  r = cmApi.request(url=url)
  r_dict = json.loads(r.content.decode())
  logDebug("1\tr_dict:[{}]".format(r_dict))
  
  url = r_dict["authn_endpoint"]
  r = cmApi.request(url=url)
  logDebug("2\tr_content:[{}]".format(r.content.decode()))
  
  midwaySessionToken = r.content.decode()
  logDebug("2\tmidwaySessionToken({:,}):[{}]".format(len(midwaySessionToken), midwaySessionToken))
  
  url="https://command-center.support.aws.a2z.com/sso/login?id_token={}".format(midwaySessionToken)
  r = cmApi.request(url=url)
  logDebug("3\tr_content:[{}]".format(r.content.decode()))
  logDebug("3\twill be expired in [{:,.2f}]s".format(r.json()["expires_at"]/1000-time.time()))
  
  
  nonce = secrets.token_urlsafe()
  logDebug("nonce:[{}]".format(nonce))
  
  url = "https://cognito-identity.us-east-1.amazonaws.com/"
  poolId_dict = {"IdentityPoolId":"us-east-1:39a7a18e-9f1d-4fa1-9c5a-e4f7d98dfc98"}
  cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
  cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
  cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
  cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
  cmApi.addHeaders("Sec-Fetch-Dest", "empty")
  cmApi.addHeaders("Sec-Fetch-Mode", "cors")
  cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
  cmApi.addHeaders("TE", "trailers")
  cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetId")
  r = cmApi.request(url=url, payload=poolId_dict)
  identityId_dict = json.loads(r.content.decode())
  logDebug("4\identityId_dict:[{}]".format(identityId_dict))
  
  url = "https://cognito-identity.us-east-1.amazonaws.com/"
  payload_dict = json.loads(r.content.decode())
  cmApi.addHeaders("content-type", "application/x-amz-json-1.1")
  cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
  cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
  cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
  cmApi.addHeaders("Sec-Fetch-Dest", "empty")
  cmApi.addHeaders("Sec-Fetch-Mode", "cors")
  cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
  cmApi.addHeaders("TE", "trailers")
  cmApi.addHeaders("x-amz-target", "AWSCognitoIdentityService.GetOpenIdToken")
  r = cmApi.request(url=url, payload=payload_dict)
  r_dict = json.loads(r.content.decode())
  logDebug("5\tr_dict:[{}]".format(r_dict))
  cognitoSessionToken = r_dict["Token"]
  identityId = r_dict["IdentityId"]
  logDebug("5\tcognitoSessionToken:[{}]".format(cognitoSessionToken))
  logDebug("5\t{}:identityId:[{}]".format(type(identityId).__name__, identityId))
  
  url = "https://cognito-identity.us-east-1.amazonaws.com/"
  
  cmApi.clearHeader()
  cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
  cmApi.addHeaders("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0")
  cmApi.addHeaders("Accept", "*/*")
  cmApi.addHeaders("Accept-Language", "en-US,en;q=0.5")
  cmApi.addHeaders("Accept-Encoding", "gzip, deflate, br")
  cmApi.addHeaders("Access-Control-Request-Method", "POST")
  cmApi.addHeaders("Access-Control-Request-Headers", "content-type,x-amz-content-sha256,x-amz-target,x-amz-user-agent")
  cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
  cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
  cmApi.addHeaders("Connection", "keep-alive")
  cmApi.addHeaders("Sec-Fetch-Dest", "empty")
  cmApi.addHeaders("Sec-Fetch-Mode", "cors")
  cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
  #cmApi.listHeaders()
  r = cmApi.request(url=url, payload="OPTIONS")
  
  #HTTP/2 200 OK
  #date: Sun, 21 May 2023 17:01:03 GMT
  #content-length: 0
  #x-amzn-requestid: 8793faea-1962-48d9-9b8e-d52ed53c5783
  #access-control-allow-origin: *
  #strict-transport-security: max-age=31536000; includeSubDomains
  #access-control-allow-headers: content-type,x-amz-content-sha256,x-amz-target,x-amz-user-agent
  #access-control-allow-methods: POST
  #access-control-expose-headers: x-amzn-RequestId,x-amzn-ErrorType,x-amzn-ErrorMessage,Date
  #access-control-max-age: 172800
  #X-Firefox-Spdy: h2
  logDebug("5\tr.content:[{}]".format(r.content))
  
  #POST / HTTP/2
  #Host: cognito-identity.us-east-1.amazonaws.com
  #User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
  #Accept: */*
  #Accept-Language: en-US,en;q=0.5
  #Accept-Encoding: gzip, deflate, br
  #X-Amz-User-Agent: aws-sdk-js/2.45.0 callback
  #Content-Type: application/x-amz-json-1.1
  #X-Amz-Target: AWSCognitoIdentityService.GetCredentialsForIdentity
  #X-Amz-Content-Sha256: e47b896d3c1ce49028fdc07ccba8532617dfae122cda6605899849abe6b22e32
  #Content-Length: 1056
  #Origin: https://command-center.support.aws.a2z.com
  #Connection: keep-alive
  #Referer: https://command-center.support.aws.a2z.com/
  #Sec-Fetch-Dest: empty
  #Sec-Fetch-Mode: cors
  #Sec-Fetch-Site: cross-site
  #TE: trailers
  
  
  url = "https://cognito-identity.us-east-1.amazonaws.com/"
  
  cmApi.clearHeader()
  cmApi.addHeaders("Host", "cognito-identity.us-east-1.amazonaws.com")
  cmApi.addHeaders("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0")
  cmApi.addHeaders("Accept", "*/*")
  cmApi.addHeaders("Accept-Language", "en-US,en;q=0.5")
  cmApi.addHeaders("Accept-Encoding", "gzip, deflate, br")
  cmApi.addHeaders("X-Amz-User-Agent", "aws-sdk-js/2.45.0 callback")
  cmApi.addHeaders("Content-Type", "application/x-amz-json-1.1")
  cmApi.addHeaders("X-Amz-Target", "AWSCognitoIdentityService.GetCredentialsForIdentity")
  #cmApi.addHeaders("X-Amz-Content-Sha256", "e47b896d3c1ce49028fdc07ccba8532617dfae122cda6605899849abe6b22e32")
  cmApi.addHeaders("Referer", "https://command-center.support.aws.a2z.com/")
  cmApi.addHeaders("Origin", "https://command-center.support.aws.a2z.com")
  cmApi.addHeaders("Connection", "keep-alive")
  cmApi.addHeaders("Sec-Fetch-Dest", "empty")
  cmApi.addHeaders("Sec-Fetch-Mode", "cors")
  cmApi.addHeaders("Sec-Fetch-Site", "cross-site")
  #cmApi.listHeaders()
  payload_dict = {"IdentityId":identityId, "Logins":{"midway-auth.amazon.com":midwaySessionToken}}
  r = cmApi.request(url=url, payload=payload_dict)
  
  #HTTP/2 200 OK
  #date: Sun, 21 May 2023 17:01:03 GMT
  #content-length: 0
  #x-amzn-requestid: 8793faea-1962-48d9-9b8e-d52ed53c5783
  #access-control-allow-origin: *
  #strict-transport-security: max-age=31536000; includeSubDomains
  #access-control-allow-headers: content-type,x-amz-content-sha256,x-amz-target,x-amz-user-agent
  #access-control-allow-methods: POST
  #access-control-expose-headers: x-amzn-RequestId,x-amzn-ErrorType,x-amzn-ErrorMessage,Date
  #access-control-max-age: 172800
  #X-Firefox-Spdy: h2
  logDebug("6\tr.content:[{}]".format(r.content))
  

def updateHeader(request_headers):
  header_dict = {}
  
  rawCount = 0
  for raw in request_headers.split("\n"):
    rawCount += 1
    
    raw = raw.strip()
    if len(raw) > 0:
      raw_list = raw.split(": ")
      if len(raw_list) == 2:
        logDebug("(#{:,}:{:,})\t{}".format(rawCount, len(raw_list), raw_list))
        header_dict[raw_list[0]] = raw_list[1]
      else:
        logWarn("ignored (#{:,}:{:,})\t{}".format(rawCount, len(raw_list), raw_list))
  
  return header_dict

def scp():
  result_list = []
  options_request_headers = """
OPTIONS /search/customers/internal-alias/jfariss?paginationToken=eyJwYWdpbmF0aW9uVG9rZW4iOnsicyI6ImV5SnJNU0k2ZXlKeklqb2lNREExWTJOa1pEZ3RPVFZtTlMwMFptRTNMVGcyTW1FdFpHRTRaRGsxT0RNME5qUmhJbjBzSW1zeUlqcDdJbk1pT2lKamREcGxabU01Tm1KaE5DMDRZekF4TFRReFlqRXRPVFl5T1MxbU5XRmxNbUpqTXpVeVpXSWlmWDBcdTAwM2QifSwiY29udGFjdElkIjp7InMiOiJlZmM5NmJhNC04YzAxLTQxYjEtOTYyOS1mNWFlMmJjMzUyZWIifX0%3D HTTP/2
Host: api.prod.us-east-1.scp.esa.kumo.support.aws.a2z.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Access-Control-Request-Method: GET
Access-Control-Request-Headers: authorization,content-type,x-amz-content-sha256,x-amz-date,x-amz-requested-by-user-alias,x-amz-security-token,x-amz-user-agent
Referer: https://command-center.support.aws.a2z.com/
Origin: https://command-center.support.aws.a2z.com
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
TE: trailers
"""
  option_header_dict = updateHeader(options_request_headers)
  
  get_request_headers="""
GET /search/customers/internal-alias/jfariss HTTP/2
Host: api.prod.us-east-1.scp.esa.kumo.support.aws.a2z.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-Amz-User-Agent: aws-sdk-js/2.437.0 promise
x-amz-requested-by-user-alias: hoeseong
Content-Type: application/json
X-Amz-Content-Sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
X-Amz-Date: 20230522T171626Z
x-amz-security-token: IQoJb3JpZ2luX2VjEJr//////////wEaCXVzLWVhc3QtMSJIMEYCIQDfIYz2g5da+oCqGGg77x4OosYb5vfXKYTRCIXsTorNdgIhAMshqeQSlhiAZLW2SXdtb+k5+jRv3K3wK1mDCN8EVzVqKo4ECML//////////wEQAhoMMDU1ODU2NDIwNzA0IgzooJiNyamMAr52pdkq4gN0rcPafat0MIKIBQCH8K7MJVP87v5Uhpj6e2N12FS57EYDHpSgc2Qu1eKJFdH8oDzayy6xbwZs0yzbvfRIrqugMDqVUlCVBujZS5L8mkO0v+N7Iay9CIFRDY4gwSjkc9nadkD9VdJfLOpjM5Jm1Kbe1ufKcA8RGwX2rZKEq81xUawwL/RaqfWW3YaBrzZa1K95NTbgBdpMlcqcJT2cbgGGC+OySrR2HczGb3X/kwejMHUXLcdVdD8ceogdFSgRGXbemQzYJuQ28n3CUgGRQ98pnzeq9rsAkqlpwg+FmMAno3tFzAd5eD+JEEnSFYsboZwHfgdzoduvVO3i+mrTMqcaWphY5eNy8Yoxg12+HwOmBE+UjgJq9a2Gt0mPgmgyih6uDGAZxhJ2ERp4xnwYV74UKfeCwmzTBHfOo+TYf0I6GI725MOoFjcdjntS4PIWrkBYomI7WSXSraIsZvKcU6S7yLI3qLAGOZcCINz2kPHR8MV8VubGZfWfQWNZTg8NO41wMkotG2iriE6ikJAK5aJB6I2rpPwPFZ8smyNoxjMfLMMeObrs8SxM13UDNKnaY+r/oh66v2ykt+ge7P7lDuYSgj6a5mFDXRdArTpGfJgaLbM7LofJFYbPtR0A93ICmZNJLzCKwq6jBjqDAq48G+G/48v4Q3lkinWIIpU0f3NslNcxDxBgOEzMmPxpWmOfbW+tCw7988MJUQujiDd6sdXEWhzgdr5VcAq6LW3U4lD9vdoQhQZtX3+J7zRbQnudemPwUrDxcuZ53ORYFEz26wESBu6lei2z5Z6Bxt1zvwq6B9XEhdaX8jXCXAcuhU62EiFT6/8M+iQDiEAH6aX9bAqn+M/ksZry5cHxoeK95DyCkjB3jDDQuux82V32JvSQAYH+xQpDtDEgM/L2rVUKHBGOgnD+Y7MFu/sfunGEjI5dRCfrCBEBk4aR9vTE+uQtRONw73iVv5JsxjGh4aC3MGs25caAEhRiUtYt3C9rqhQ=
Authorization: AWS4-HMAC-SHA256 Credential=ASIAQ2AKNK5QIGUB7AEI/20230522/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date;x-amz-requested-by-user-alias;x-amz-security-token;x-amz-user-agent, Signature=6f4c2e628ef21330398b08291cf648427ed91039f80628e84aa11cfe98e0d006
Origin: https://command-center.support.aws.a2z.com
Connection: keep-alive
Referer: https://command-center.support.aws.a2z.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
TE: trailers

Host: api.prod.us-east-1.scp.esa.kumo.support.aws.a2z.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-Amz-User-Agent: aws-sdk-js/2.437.0 promise
x-amz-requested-by-user-alias: hoeseong
Content-Type: application/json
X-Amz-Content-Sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
X-Amz-Date: 20230522T171836Z
x-amz-security-token: IQoJb3JpZ2luX2VjEJr//////////wEaCXVzLWVhc3QtMSJIMEYCIQDfIYz2g5da+oCqGGg77x4OosYb5vfXKYTRCIXsTorNdgIhAMshqeQSlhiAZLW2SXdtb+k5+jRv3K3wK1mDCN8EVzVqKo4ECML//////////wEQAhoMMDU1ODU2NDIwNzA0IgzooJiNyamMAr52pdkq4gN0rcPafat0MIKIBQCH8K7MJVP87v5Uhpj6e2N12FS57EYDHpSgc2Qu1eKJFdH8oDzayy6xbwZs0yzbvfRIrqugMDqVUlCVBujZS5L8mkO0v+N7Iay9CIFRDY4gwSjkc9nadkD9VdJfLOpjM5Jm1Kbe1ufKcA8RGwX2rZKEq81xUawwL/RaqfWW3YaBrzZa1K95NTbgBdpMlcqcJT2cbgGGC+OySrR2HczGb3X/kwejMHUXLcdVdD8ceogdFSgRGXbemQzYJuQ28n3CUgGRQ98pnzeq9rsAkqlpwg+FmMAno3tFzAd5eD+JEEnSFYsboZwHfgdzoduvVO3i+mrTMqcaWphY5eNy8Yoxg12+HwOmBE+UjgJq9a2Gt0mPgmgyih6uDGAZxhJ2ERp4xnwYV74UKfeCwmzTBHfOo+TYf0I6GI725MOoFjcdjntS4PIWrkBYomI7WSXSraIsZvKcU6S7yLI3qLAGOZcCINz2kPHR8MV8VubGZfWfQWNZTg8NO41wMkotG2iriE6ikJAK5aJB6I2rpPwPFZ8smyNoxjMfLMMeObrs8SxM13UDNKnaY+r/oh66v2ykt+ge7P7lDuYSgj6a5mFDXRdArTpGfJgaLbM7LofJFYbPtR0A93ICmZNJLzCKwq6jBjqDAq48G+G/48v4Q3lkinWIIpU0f3NslNcxDxBgOEzMmPxpWmOfbW+tCw7988MJUQujiDd6sdXEWhzgdr5VcAq6LW3U4lD9vdoQhQZtX3+J7zRbQnudemPwUrDxcuZ53ORYFEz26wESBu6lei2z5Z6Bxt1zvwq6B9XEhdaX8jXCXAcuhU62EiFT6/8M+iQDiEAH6aX9bAqn+M/ksZry5cHxoeK95DyCkjB3jDDQuux82V32JvSQAYH+xQpDtDEgM/L2rVUKHBGOgnD+Y7MFu/sfunGEjI5dRCfrCBEBk4aR9vTE+uQtRONw73iVv5JsxjGh4aC3MGs25caAEhRiUtYt3C9rqhQ=
Authorization: AWS4-HMAC-SHA256 Credential=ASIAQ2AKNK5QIGUB7AEI/20230522/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date;x-amz-requested-by-user-alias;x-amz-security-token;x-amz-user-agent, Signature=e810293b8d57f969b667a8fa3b04412653a04b5a3af6a134019a200c51043695
Origin: https://command-center.support.aws.a2z.com
Connection: keep-alive
Referer: https://command-center.support.aws.a2z.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
TE: trailers

"""
  cmApi = CMApi(userAccountId = "749952098923", loginAliasId = "hoeseong")
  url = "https://api.prod.us-east-1.scp.esa.kumo.support.aws.a2z.com/search/customers/internal-alias/jfariss"
    
  #paginationToken = "eyJwYWdpbmF0aW9uVG9rZW4iOnsicyI6ImV5SnJNU0k2ZXlKeklqb2lNREExWTJOa1pEZ3RPVFZtTlMwMFptRTNMVGcyTW1FdFpHRTRaRGsxT0RNME5qUmhJbjBzSW1zeUlqcDdJbk1pT2lKamREcGxabU01Tm1KaE5DMDRZekF4TFRReFlqRXRPVFl5T1MxbU5XRmxNbUpqTXpVeVpXSWlmWDBcdTAwM2QifSwiY29udGFjdElkIjp7InMiOiJlZmM5NmJhNC04YzAxLTQxYjEtOTYyOS1mNWFlMmJjMzUyZWIifX0="
  paginationToken = ""
  if len(paginationToken) == 0:
    get_headers_dict = updateHeader(get_request_headers)
    
    cmApi.clearHeader()
    for key in option_header_dict.keys():
      cmApi.addHeaders(key, option_header_dict[key])
    cmApi.listHeaders()
    
    r = cmApi.request(url=url, payload="OPTIONS")
    logDebug("1\tr.content:[{}]".format(r.content))
    
    
    cmApi.clearHeader()
    for key in get_headers_dict.keys():
      cmApi.addHeaders(key, get_headers_dict[key])
    cmApi.listHeaders()
    
    r = cmApi.request(url=url, payload=None)
    logDebug("2\tr.content:[{}]".format(r.content))
    
    try:
      paginationToken = r.json()["paginationToken"]
      if len(paginationToken) > 20:
        logDebug("paginationToken(len:{:,}):[{}...{}]".format(len(paginationToken), paginationToken[:10], paginationToken[-10:]))
    except:
      logException("paginationToken not found r.content:[{}]".format(r.content))
      exit()
    
  paginationCount = 0
  while len(paginationToken) > 0:
    paginationCount += 1
    
    url = "{}?paginationToken={}".format(url, paginationToken)
    
    cmApi.clearHeader()
    for key in option_header_dict.keys():
      cmApi.addHeaders(key, option_header_dict[key])
    cmApi.listHeaders()
    
    r = cmApi.request(url=url, payload="OPTIONS")
    logDebug("(p#{:,})\tr.content:[{}]".format(paginationCount, r.content))
    
    cmApi.clearHeader()
    for key in get_headers_dict.keys():
      cmApi.addHeaders(key, get_headers_dict[key])
    cmApi.listHeaders()
    
    r = cmApi.request(url=url, payload=None)
    logDebug("(p#{:,})\tr.content:[{}]".format(paginationCount, r.content))
    
    try:
      r_dict = r.json()
      for customerItem_dict in r_dict["customerList"]:
        result_list.append(customerItem_dict)
      
      try:
        paginationToken = r.json()["paginationToken"]
        if len(paginationToken) > 20:
          logDebug("paginationToken(len:{:,}):[{}...{}]".format(len(paginationToken), paginationToken[:10], paginationToken[-10:]))
      except:
        logException("paginationToken not found r.content:[{}]".format(r.content))
        exit()
        
    except:
      logException("unexpected r.content:[{}]".format(r.content))
      break
    
  f = open(expanduser("~/Downloads/customerList.json"), "w")
  json.dump(result_list, f)
  f.close()

def discoverBubbleWandAccounts():
  pdxMidway = PdxMidway(userAccountId = "749952098923", loginAliasId = "hoeseong")
  r = pdxMidway.mRequest(
    url="https://command-center.support.aws.a2z.com/sso/login"
    )
  
  r = pdxMidway.mRequest(
    url="https://cognito-identity.us-east-1.amazonaws.com/",
    payload=None,
    headers="""
      POST / HTTP/2
      Host: cognito-identity.us-east-1.amazonaws.com
      User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
      Accept: */*
      Accept-Language: en-US,en;q=0.5
      Accept-Encoding: gzip, deflate, br
      X-Amz-User-Agent: aws-sdk-js/2.45.0 callback
      Content-Type: application/x-amz-json-1.1
      X-Amz-Target: AWSCognitoIdentityService.GetId
      X-Amz-Content-Sha256: d47f912d649aa225f022458756af56aceb89f1b1e6d50e1bfb58ec7830c7a14a
      Content-Length: 1060
      Origin: https://command-center.support.aws.a2z.com
      Connection: keep-alive
      Referer: https://command-center.support.aws.a2z.com/
      Sec-Fetch-Dest: empty
      Sec-Fetch-Mode: cors
      Sec-Fetch-Site: cross-site
      """
    )
  
  
  
  exit()
  
  pdxMidway.mRequest(
    url="https://api.prod.us-east-1.rps.esa.kumo.support.aws.a2z.com/customers/2300422c-834b-442c-a3ce-9aad0a901d63", 
    payload=None, 
    headers="""
    GET /customers/42ce263c-a231-4e37-9fef-6e91aa4490b1 HTTP/2
    Host: api.prod.us-east-1.rps.esa.kumo.support.aws.a2z.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate, br
    X-Amz-User-Agent: aws-sdk-js/2.437.0 promise
    Content-Type: application/json
    X-Amz-Content-Sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    X-Amz-Date: 20230607T151123Z
    x-amz-security-token: IQoJb3JpZ2luX2VjEBgaCXVzLWVhc3QtMSJHMEUCIHdI1nawWxpmG6K1R9X+qgHsJgkYMZgCfPEaqLrrqrjEAiEAljxSvTr5NVh/DHVf4E098T+GpP0K9Z/cVagBgsqBJkwqhQQIYBAEGgw2MDc1NzAxNTk4MzkiDGGx2LHJDlvMOzoD7CriA+h9RIqaeSJCjhclw0IY5fC6X/t4zjeOaqQQneHWXOEgRaYbFjFBnPEagRPjtBI3ejHF2Z2EjWzU71/scwAUFdhLcvP7jCOcxF1MshGefAZyUr3tl9Gymix7QO+EJCMaBfmtDRXmo764CWIe8/CNiOd3NgRBEYBVTYgfqXrrYleGr7/wKsS9+r7P3ne1vr7IvpFtnSBA4Q/pR6AeVcdb4ijapBe6qcDb2DYE9NSOf3Rwv8St2xJN3CSjaVlwtF/7+5Y3UjixBw4FtQDG60Sv19HxBI46LA8rVmMSwBgFOrsmqoawmtuRFGSDJOSfAWjNgr8WxKkXaIWx/rzkY5iWcfo40G2YXzFNgayHQLEuOipf5VqqWq34OK87mIixYUxId8nJ9R/MI/ZHsDNFc2IXsaSRf4dokFH4VRNPMO2wUeW626avht/O4QRuGv6yFe4XMDUepC4YJUmDOornuURa10Goz/PYjA8+C3Ls61ayDid+GIhbAK1ets/UOXlFMvp7UVXLpGNtDDpTXVY3mB7qzquzLFw9zYi2OdiKJZZGICldhiduXJNMuFjt4UHN2g3WWrcZwZbfkOdNuCAY1toHRIXMzeNVjW8bRXAmfIo8bgH4109iUwkgTB6XLSDVu+dNm5L7MJu8gqQGOoQCGU0n5yBJh4nseHLwsTuZo02I5Cb1CqmQXATzU+pbHpyamMh1TjCyldzkF53mdOIEZFCy2LSftuAXu0XR59cT5BV1gX8o9YzeJyD1NDvOpjJU//tIjfjPHNaGihtjrS6rBKsfAHjnFH+f3ES7C589wPPVTJHDrD1KM8ke6UIoo/Y3AIKWr78TyIb8ZW+yBwbPMsWNlUxijioES+2dijTQ3jZnSO5IFNQvT2Jklb0fQfW6lf95CrTihD3KwObN0sZQxMAqK8A1Os0RrPxlZzqeAcoWaid78G5juC63HBllFizy3f1Jep6mdWC8mJLRK2FJCwhOtNdRFe5zQ42hIumVyj0ppic=
    Authorization: AWS4-HMAC-SHA256 Credential=ASIAY25QA5DPTVZGIT2F/20230607/us-east-1/execute-api/aws4_request, SignedHeaders=host;x-amz-content-sha256;x-amz-date;x-amz-security-token;x-amz-user-agent, Signature=c42b700402f6d10dc6cafbd3038e1330903ee5994d5497470d9c6737df2444d2
    Origin: https://command-center.support.aws.a2z.com
    Connection: keep-alive
    Referer: https://command-center.support.aws.a2z.com/
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-site
    TE: trailers
    """, 
    verbose=True
    )
  
def localUnitTest():
  unitTestFunction_dict = {
    "discoverBubbleWandAccounts":{"target":discoverBubbleWandAccounts, "args":{}}
    #"executeCMApi":{"target":executeCMApi, "args":()},
    #"loginCognito":{"target":loginCognito, "args":()},
    #"scp":{"target":scp, "args":()},
    }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()
    