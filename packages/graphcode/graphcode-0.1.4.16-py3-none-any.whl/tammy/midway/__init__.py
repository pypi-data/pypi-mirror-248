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
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError, getLogLevel, setLogLevel
from graphcode.conf import getHomeURL
from graphcode.conf import getUserAgent
from graphcode.conf import loadLocalCookie, getMaxWaitTimeForExpiredLocalCookie
from graphcode.conf import getMaxApiRetries, getWaitTimeForRateExceeded, getConnectionTimeout, getSessionTimeout

from graphcode.itemDB import GcItemDB
from graphcode.lib import getDateString

from graphcode.email import GcEmail
from graphcode.email import expiredCookieEmail

from pathway import updateMsg

from tammy.midway.midwayCookieHandler import MidwayCookieHandler

from os.path import expanduser

import inspect
import time
import random

import requests
#Disable warnings from urlib3, telling us SSL cert is not in chain/CA
requests.packages.urllib3.disable_warnings()

import json

import logging

from uuid import uuid4

from requests_kerberos import HTTPKerberosAuth, OPTIONAL

class Midway(MidwayCookieHandler):
  def __init__(self, request_dict, logMessage_list, errorReason_list):
    MidwayCookieHandler.__init__(self, request_dict, logMessage_list, errorReason_list)
    
    self.wasMidwayInitalized = False
    
    self.requestOnline = True
    self.requestCount = -1
    self.midwayRegion = None
    self.midway401ErroCount = 0
    self.notifiedTime = time.time()
    self.aeaOptedOutTime = 0
    self.activeMidwayCookie_dict = {"global":{},"cn":{}}
    self.activeMidwayCookie_dict = self.getMidwayCookie()
    
    self.maxRetry = 1
    self.maxRetrialNumberWithNone = getMaxApiRetries()
    self.sleepingTimeForMidwayCookieExpiration = 60
    self.maxWaitingCountForMidwayCookieExpiration = 1440
    self.maxWaitTimeForExpiredMidway = getMaxWaitTimeForExpiredLocalCookie()
    self.maxWaitTimeForRateExceeded = getWaitTimeForRateExceeded()
    self.connectionTimeout = getConnectionTimeout()
    self.sessionTimeout = getSessionTimeout()
    
    self.headers = self.initHeader()
    
    self.SESSION = requests.Session()
    self.SESSION_COOKIES = {}
    
    self.activeMidwayCookie_dict = self.getMidwayCookie()

    self.deadRequest_list = []

  def initHeader(self):
    return {
      'User-agent': getUserAgent()
      }
    
  def addHeaders(self, key, data):
    self.headers[key] = data
  
  def deleteHeaders(self, key):
    try:
      del self.headers[key]
    except:
      logException("unable to delete header:[{}]".format(key))

  def iterateHeaders(self):
    logDebug("Headers(len:{:,}):[{}]".format(len(self.headers.keys()), self.headers.keys()))
    
    for headerName in self.headers.keys():
      logDebug("header.{}:[{}]".format(headerName, self.headers[headerName]))
    
    return self.headers
  
  def getMidwayUser(self):
    if self.user == None:
      self.getMidwayCookie()
    
    return self.user

  def sessionRequest(self, url, payload = None, headers = None, cookies = None, timeout = None, verify = False, retry = 0):  
    self.requestCount += 1
    self.requestOnline = True
    
    if "cgi-bin/mis/query.rb" in url:
      timeout = (15, 600)
      #logDebug("timeout is set with (15, 600)")
    elif timeout == None:
      timeout = (self.connectionTimeout, self.sessionTimeout)
      #logDebug("default timeout is set with [{}]".format(timeout))
    else:
      timeout = timeout
      logDebug("timeout is set with [{}]".format(timeout))
      
    httpProtocol = None
    
    if isinstance(headers, dict):
      header_dict = self.headers
      for key in headers.keys():
        header_dict[key] = headers[key]
        
    else:
      header_dict = self.headers
    
    #for headerKey in header_dict.keys():
    #  logDebug("header:{}:[{}]".format(headerKey, header_dict[headerKey]))
      
    if payload != None and isinstance(payload, str) == False:
      payload = json.dumps(payload)
    
    #logDebug("#URL:[{}]".format(url))
    for partition in self.activeMidwayCookie_dict.keys():
      #for key in self.activeMidwayCookie_dict[partition].keys():
      #  logDebug("self.activeMidwayCookie_dict:{}.{}:[{}]".format(partition, key, self.activeMidwayCookie_dict[partition][key]))
      
      try:
        if self.activeMidwayCookie_dict[partition]["active"]:
          break
        else:
          class thisMidwayErrorResponse:
            status_code = 401
            try:
              content = "{}".format({"error":"'{}' Midway was expired {:.2f} hours ago".format(partition, (time.time()-self.activeMidwayCookie_dict[partition]["expirationTime"])/3600)}).encode()
            except:
              content = "{}".format({"error":"'{}' Midway isn't provided.".format(partition, self.activeMidwayCookie_dict)}).encode()
              
          return thisMidwayErrorResponse
      except:
        logException("midway:[{}] is not found".format(partition))
        
    if "bjs.aws-border.com" in url or "aws-border.cn" in url:
      #logDebug("#url:[{}]".format(url))
      if self.midwayRegion in ["global", None]: 
        
        #logDebug("#self.midwayRegion:[{}]".format(self.midwayRegion))
        if "cn" in self.activeMidwayCookie_dict.keys() and "active" in self.activeMidwayCookie_dict["cn"].keys() and self.activeMidwayCookie_dict["cn"]["active"]: 
          sessionCookie_dict = self.SESSION.cookies.get_dict()
          sessionCookie_dict['session'] = self.activeMidwayCookie_dict["cn"]["sessionId"] 
          
          if "aea" in self.activeMidwayCookie_dict["cn"].keys():
            sessionCookie_dict["amazon_enterprise_access"] = self.activeMidwayCookie_dict["cn"]["aea"]
            
          self.SESSION.cookies = requests.utils.cookiejar_from_dict(sessionCookie_dict)
          self.midwayRegion = "cn"
          
          thisSessionCookie_dict = self.SESSION.cookies.get_dict()
          thisCookieCount = 0
          for thisCookieName in thisSessionCookie_dict.keys():
            thisCookieCount += 1
            self.SESSION_COOKIES[thisCookieName] = thisSessionCookie_dict[thisCookieName]
            #logDebug("#requestCookies[{}]:{}:{}".format(thisCookieCount, thisCookieName, self.SESSION_COOKIES[thisCookieName]))
        
        else:
          self.activeMidwayCookie_dict = self.getMidwayCookie()
          if "cn" in self.activeMidwayCookie_dict.keys() and "active" in self.activeMidwayCookie_dict["cn"].keys() and self.activeMidwayCookie_dict["cn"]["active"]: 
            sessionCookie_dict = self.SESSION.cookies.get_dict()
            sessionCookie_dict['session'] = self.activeMidwayCookie_dict["cn"]["sessionId"] 
            
            if "aea" in self.activeMidwayCookie_dict["cn"].keys():
              sessionCookie_dict["amazon_enterprise_access"] = self.activeMidwayCookie_dict["cn"]["aea"]
              
            self.SESSION.cookies = requests.utils.cookiejar_from_dict(sessionCookie_dict)
            self.midwayRegion = "cn"
            
            thisSessionCookie_dict = self.SESSION.cookies.get_dict()
            thisCookieCount = 0
            for thisCookieName in thisSessionCookie_dict.keys():
              thisCookieCount += 1
              self.SESSION_COOKIES[thisCookieName] = thisSessionCookie_dict[thisCookieName]
              #logDebug("#requestCookies[{}]:{}:{}".format(thisCookieCount, thisCookieName, self.SESSION_COOKIES[thisCookieName]))
          else: 
            class thisMidwayErrorResponse:
              status_code = 401
              try:
                content = "{}".format({"error":"'cn' Midway was expired {:.2f} hours ago".format((time.time()-self.activeMidwayCookie_dict["cn"]["expirationTime"])/3600)}).encode()
              except:
                content = "{}".format({"error":"'cn' Midway isn't active".format(self.activeMidwayCookie_dict)}).encode()
                
            return thisMidwayErrorResponse
      else:
        #logDebug("#midwayCookie is already loaded->self.SESSION_COOKIES:[{}]".format(self.SESSION_COOKIES))
        pass
          
    else:
      #logDebug("#url:[{}]".format(url))
      if self.midwayRegion in ["cn", None]:
        #logDebug("#self.midwayRegion:[{}]".format(self.midwayRegion))
        
        if "global" in self.activeMidwayCookie_dict.keys() and "active" in self.activeMidwayCookie_dict["global"].keys() and self.activeMidwayCookie_dict["global"]["active"]: 
          sessionCookie_dict = self.SESSION.cookies.get_dict()
          sessionCookie_dict['session'] = self.activeMidwayCookie_dict["global"]["sessionId"]
          
          if "aea" in self.activeMidwayCookie_dict["global"].keys():
            sessionCookie_dict["amazon_enterprise_access"] = self.activeMidwayCookie_dict["global"]["aea"]
            
          self.SESSION.cookies = requests.utils.cookiejar_from_dict(sessionCookie_dict)
          self.midwayRegion = "global"
    
          thisSessionCookie_dict = self.SESSION.cookies.get_dict()
          thisCookieCount = 0
          for thisCookieName in thisSessionCookie_dict.keys():
            thisCookieCount += 1
            self.SESSION_COOKIES[thisCookieName] = thisSessionCookie_dict[thisCookieName]
            #logDebug("#requestCookies[{}]:{}:{}".format(thisCookieCount, thisCookieName, self.SESSION_COOKIES[thisCookieName]))
        
        else:
          self.activeMidwayCookie_dict = self.getMidwayCookie()
          if "global" in self.activeMidwayCookie_dict.keys() and "active" in self.activeMidwayCookie_dict["global"].keys() and self.activeMidwayCookie_dict["global"]["active"]: 
            sessionCookie_dict = self.SESSION.cookies.get_dict()
            sessionCookie_dict['session'] = self.activeMidwayCookie_dict["global"]["sessionId"] 
            
            if "aea" in self.activeMidwayCookie_dict["global"].keys():
              sessionCookie_dict["amazon_enterprise_access"] = self.activeMidwayCookie_dict["global"]["aea"]
              
            self.SESSION.cookies = requests.utils.cookiejar_from_dict(sessionCookie_dict)
            self.midwayRegion = "global"
            
            thisSessionCookie_dict = self.SESSION.cookies.get_dict()
            thisCookieCount = 0
            for thisCookieName in thisSessionCookie_dict.keys():
              thisCookieCount += 1
              self.SESSION_COOKIES[thisCookieName] = thisSessionCookie_dict[thisCookieName]
              #logDebug("#requestCookies[{}]:{}:{}".format(thisCookieCount, thisCookieName, self.SESSION_COOKIES[thisCookieName]))
          else: 
            class thisMidwayErrorResponse:
              status_code = 401
              try:
                content = "{}".format({"error":"'global' Midway was expired {:.2f} hours ago".format((time.time()-self.activeMidwayCookie_dict["global"]["expirationTime"])/3600)}).encode()
              except:
                content = "{}".format({"error":"'global' Midway isn't active"}).encode()
            return thisMidwayErrorResponse
      else:
        #logDebug("#midwayCookie is already loaded->self.SESSION_COOKIES:[{}]".format(self.SESSION_COOKIES))
        pass
    
    '''
    for key in sorted(self.activeMidwayCookie_dict.keys()):
      #logDebug("#activeMidwayCookie_dict[{}]:[{}]".format(key, self.activeMidwayCookie_dict[key].keys()))
      for key_2 in self.activeMidwayCookie_dict[key].keys():
        if key_2 == "sessionId":
          if len(self.activeMidwayCookie_dict[key][key_2]) > 35:
            #logDebug("#activeMidwayCookie_dict[{}][{}]:[{}...{}](len:{:,})".format(key, key_2, self.activeMidwayCookie_dict[key][key_2][:15], self.activeMidwayCookie_dict[key][key_2][-15:], len(self.activeMidwayCookie_dict[key][key_2])))
            pass
          else:
            #logDebug("#activeMidwayCookie_dict[{}][{}]:[{}](len:{:,})".format(key, key_2, self.activeMidwayCookie_dict[key][key_2][:15], self.activeMidwayCookie_dict[key][key_2][-15:], len(self.activeMidwayCookie_dict[key][key_2])))
            pass
        else:
          #logDebug("#activeMidwayCookie_dict[{}][{}]:[{}]".format(key, key_2, self.activeMidwayCookie_dict[key][key_2]))
          pass
    '''
    
    #logDebug("#Headers:[{}]".format(headers))
    #logDebug("#payload:[{}]".format(payload))
    #logDebug("#Timeout:[{}]".format(timeout))
    
    #r = self.SESSION.post(url, cookies = cookies, headers = header_dict, timeout = timeout, verify=verify, data=payload)
        
    try:
      if payload != None or "isengard" in url:
        if payload == "OPTIONS":
          httpProtocol = "OPTIONS"
          #logDebug("Protocol:[{}]".format(httpProtocol))
          if "https://api.gaderian.command-center.support.aws.a2z.com/cases" in url:
            header_dict["Access-Control-Request-Headers"] = "accessoverridesession,anti-csrf-token,content-type"
            header_dict["Access-Control-Request-Method"] = "POST"
            logDebug("Headers:[{}]".format(headers))
            r = self.SESSION.options(url, headers = header_dict)
          else:
            r = self.SESSION.options(url, headers = header_dict)
        
        else:
          httpProtocol = "POST"
          #logDebug("#Protocol:[{}]".format(httpProtocol))
          r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)

          # if None is returned, anything might be wrong from the server or the request. So, it'll retry to get no 'None' with the requested until it reach to the max retry.
          if r == None:
            retry2 = 0
            while retry2 < self.maxRetrialNumberWithNone:
              logWarn("#{}:retrying to url:[{}] with payload:[{}] due to r:[{}]".format(retry2, url, payload, r))
              r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)
              if r != None:
                break
              else:
                retry2 += 1
                
      #elif payload != None:
      #  httpProtocol = "POST"
      #  logDebug("Protocol:[{}]".format(httpProtocol))
      #  r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)
      else:
        httpProtocol = "GET"
        #logDebug("Protocol:[{}]".format(httpProtocol))

        self.SESSION.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
        
        r = self.SESSION.get(url, headers = header_dict, timeout = timeout, verify=False)
        
        # if None is returned, anything might be wrong from the server or the request. So, it'll retry to get no 'None' with the requested until it reach to the max retry.
        if r == None:
          retry2 = 0
          while retry2 < self.maxRetrialNumberWithNone:
            logWarn("#{}:retrying to url:[{}] with payload:[{}] due to r:[{}]".format(retry2, url, payload, r))
            r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)
            if r != None:
              break
            else:
              retry2 += 1
      
      #for thisKey in thisCookie_dict.keys():
      #  logInfo("===>{}:[{}]".format(thisKey, thisCookie_dict[thisKey]))
        
    except Exception as e: 
      errMsg = logError("Error:[{}:{}] -> failed to connect to url:[{}],payload:[{}],cookies:[{}]".format(e, inspect.currentframe().f_back.f_lineno, url, payload, cookies))
      
      if "redirect" in "{}".format(e):
        
        class midwayRedirectError:
          status_code = 403
          content = "{}".format(e).encode()
          
        r = midwayRedirectError
        return r
      
      retryCount = 0
      while True:
        
        self.SESSION.close()
        self.SESSION = requests.Session()
        
        retryCount += 1
        try:
          if payload != None or "isengard" in url:
            if payload == "OPTIONS":
              httpProtocol = "OPTIONS"
              #logDebug("Protocol:[{}]".format(httpProtocol))
              if "https://api.gaderian.command-center.support.aws.a2z.com/cases" in url:
                header_dict["Access-Control-Request-Headers"] = "accessoverridesession,anti-csrf-token,content-type"
                header_dict["Access-Control-Request-Method"] = "POST"
                logDebug("Headers:[{}]".format(headers))
                r = self.SESSION.options(url, headers = header_dict)
              else:
                r = self.SESSION.options(url, headers = header_dict)
            
            else:
              httpProtocol = "POST"
              #logDebug("#Protocol:[{}]".format(httpProtocol))
              r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)
              
          #elif payload != None:
          #  httpProtocol = "POST"
          #  logDebug("Protocol:[{}]".format(httpProtocol))
          #  r = self.SESSION.post(url, headers = header_dict, timeout = timeout, verify=verify, data=payload)
          else:
            httpProtocol = "GET"
            #logDebug("Protocol:[{}]".format(httpProtocol))
              
            r = self.SESSION.get(url, headers = header_dict, timeout = timeout, verify=False)
          
          return r
        
        except:
          errMsg = logError("Error:[{}:{}] -> retrying(#{:,})\tfailed to connect to url:[{}],payload:[{}],cookies:[{}]".format(e, inspect.currentframe().f_back.f_lineno, retryCount, url, payload, cookies))
          
          if retryCount > 5:
            break
          
      self.addDeadRequest(url, payload, headers, cookies, timeout, verify, retry, errMsg)
      
      class midwayConnectionResetError:
        status_code = 503
        content = "{}".format(e).encode()
        
      r = midwayConnectionResetError
      
      return r
      
      '''
      Traceback (most recent call last):
          File "/Users/hoeseong/eclipse-workspace/moduAWSv11/tammy/midway.py", line 888, in request
            r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry = 0)
          File "/Users/hoeseong/eclipse-workspace/moduAWSv11/tammy/midway.py", line 726, in sessionRequest
            raise ValueError(errorMessage)
        ValueError: Error:[('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer')):888] -> f
      '''
    
    if r == None:
      raiseValueError("r:[{}] should not be 'None'".format(r))
    
    #logDebug("#{}:r.content:[{}]".format(r.status_code, r.content.decode()))
    #logDebug("#response.headers:{}:(len:{:,}):[{}]".format(type(r.headers).__name__, len(r.headers.keys()), r.headers.keys()))
    #for headerName in r.headers.keys():
    #  logDebug("response.header.{}:[{}]".format(headerName, r.headers[headerName]))
    
    r_size = len(r.content)
    if r.status_code == 200:
      #logInfo("#{}:perf:[{}]->[{},{},{},{},payload:{}]".format(self.requestCount, r.content, r.elapsed.total_seconds(), r.status_code, r_size, url, payload))
      logInfo("#{}:{}:[{},{},{},{},payload:{}".format(self.requestCount, httpProtocol, r.elapsed.total_seconds(), r.status_code, r_size, url, payload))
    #elif r_size > 2048:
    #  logInfo("#{}:perf:[{},{},{},{},payload:{},[{}...{}]]".format(self.requestCount, r.elapsed.total_seconds(), r.status_code, r_size, url, payload, r.content[:1024], r.content[-1024:]))

    else:
      logInfo("#{}:{}:[{},{},{},{},payload:{}],{}".format(self.requestCount, httpProtocol, r.elapsed.total_seconds(), r.status_code, r_size, url, payload, r.content))
      
    thisSessionCookie_dict = r.cookies.get_dict()
    thisCookieCount = 0
    for thisCookieName in thisSessionCookie_dict.keys():
      thisCookieCount += 1
      self.SESSION_COOKIES[thisCookieName] = thisSessionCookie_dict[thisCookieName]
      #logDebug("#retrunCookies[{}]:{}:{}".format(thisCookieCount, thisCookieName, self.SESSION_COOKIES[thisCookieName]))
    
    r = self.errorHandler(r, url, payload, headers, cookies, timeout, verify, retry)
    
    
    self.requestOnline = False
    
    return r
  
  def errorHandler(self, r, url, payload, headers, cookies, timeout, verify, retry):
    #logDebug("#{}:{}:{}:{}".format(r.status_code,url,payload,retry))
        
    try:
      decodedText = r.content.decode()
      if r.status_code == 401 and "Midway" in decodedText and "midway" in decodedText:
        if "session" in self.SESSION_COOKIES.keys() and len(self.SESSION_COOKIES["session"]) > 0:
          logDebug("#session found")
          for partition in self.activeMidwayCookie_dict.keys():
            logDebug("#partition:[{}] found".format(partition))
            if "active" in self.activeMidwayCookie_dict[partition]:
              if self.activeMidwayCookie_dict[partition]["active"]:
                logDebug("partition:[{}]:[{}] found, but it doesn't work!".format(partition, self.activeMidwayCookie_dict[partition]["active"]))
                class thisMidwayErrorResponse:
                    status_code = 401
                    content = json.dumps(
                      {
                        "errorReason": f"Your current '{partition}' midway was issued before current VPN status: either connected or disconnected",
                        "nextAction": "Please use 'mwinit' for new midway cookie under the current VPN connection status: either connected or disconnected. Now, AEA is supported at tammyAPIs with or without VPN Connection.",
                        "errorMessage": decodedText
                        }
                    ).encode()
                  
                return thisMidwayErrorResponse
              else:
                __expiredMidwayCookieTime__ =  time.time()
                self.notifyMidwayCookieExpiration()
                
                while r.status_code >= 400 and (time.time() -__expiredMidwayCookieTime__) < self.maxWaitTimeForExpiredMidway:
                  time.sleep(60)
                  self.activeMidwayCookie_dict = self.getMidwayCookie(midwayCookie=loadLocalCookie())

                  r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry + 1)
                  if r.status_code < 400:
                    return r
                
                return r
        
        sleepCount = 0
        while self.wasMidwayInitalized:
          
          self.midwayRegion = None
          self.activeMidwayCookie_dict = self.getMidwayCookie(midwayCookie=loadLocalCookie())
          
          thisMsg = ""
          isActiveMidwayCookie = False
          for partition in self.activeMidwayCookie_dict.keys():
            for key in  self.activeMidwayCookie_dict[partition].keys():
              if key == "expirationTime":
                if thisMsg == "":
                  thisMsg += "{}:{}h".format(partition, (self.activeMidwayCookie_dict[partition][key]-time.time())/3600)
                else:
                  thisMsg += "and {}:{}h".format(partition, (self.activeMidwayCookie_dict[partition][key]-time.time())/3600)
              elif key == "active" and self.activeMidwayCookie_dict[partition][key]:
                isActiveMidwayCookie = self.activeMidwayCookie_dict[partition][key]
              
          if isActiveMidwayCookie:
            self.midwayRegion = None
            #self.SESSION = requests.Session()
            
            r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry = sleepCount)
            
            if r.status_code != 401:
              break
          else:
            if sleepCount in [0, 1, 2, 3, 5, 60, 180, 1000, 1200, 1400]:
              self.notifyMidwayCookieExpiration()
              
          sleepCount += 1
          if sleepCount > self.maxWaitingCountForMidwayCookieExpiration:
            logError("(#{}/{}) exceeded maxWaitingCountForMidwayCookieExpiration".format(sleepCount, self.maxWaitingCountForMidwayCookieExpiration))
            break
          
          else:
            logError("(#{}/{}) waking up in {:.1f} seconds due to expired midway cookies:[{}]".format(sleepCount, self.maxWaitingCountForMidwayCookieExpiration, self.sleepingTimeForMidwayCookieExpiration, thisMsg))
            time.sleep(self.sleepingTimeForMidwayCookieExpiration)
          
        return r
      
      elif r.status_code == 403:
        
        if "InvalidBusinessUseCase" in decodedText and (url.startswith("https://k2.amazon.com") or url.startswith("https://k2.bjs.aws-border.com")):
          return r
        
        elif "User is not authorized" in decodedText and (url.startswith("https://k2.amazon.com") or url.startswith("https://k2.bjs.aws-border.com")):
          return r
        
        elif retry == 0 and "posture_error" in decodedText:
          logDebug("{}:{}:content:[{}]".format(r.status_code, url, decodedText))
          
          aeaUrl = "https://aga.aka.amazon.com/api/get-aea-auth-user?user_name={}".format(self.userName)
          if url in [aeaUrl]:
                  
            class thisMidwayErrorResponse:
              status_code = 401
              content = "{}".format(
                {
                  "error":"Your midway is not valid. Please use 'mwinit' under VPN connection, or connect VPN!",
                  "url": url,
                  "description": decodedText
                  }
                ).encode()
            
            r = thisMidwayErrorResponse
            return r 
          
          r = self.sessionRequest(aeaUrl)
          if r.status_code < 400:
            try:
              decodedText = decodedText.replace("\r"," ").replace("|n", " ").strip().replace("  "," ")
              
              aeaResponse_dict = json.loads(decodedText)
              if aeaResponse_dict["user_data"]["opted_out"]:
                return r
              else:
                if retry < 2:
                  self.doAeaOptedOut()
              
                time.sleep(300)
                r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry + 1)
                return r
              
            except:
              logException("unable to get aeaResponse:[{}]".format(decodedText))
              return r
          else:
            return r
          
        else:
          return r
            
      elif r.status_code == 429:
        sleepTime = 2
        while self.wasMidwayInitalized:
          #self.SESSION.close()
          #self.SESSION_COOKIES = {}
          #self.SESSION = requests.Session()
          
          #self.midwayRegion = None
          #self.activeMidwayCookie_dict = self.getMidwayCookie()
          
          logInfo("=======> New session is created")
          r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry + 1)
          
          if r.status_code == 200 or r.status_code != 429:
            logInfo("=======> r.status_code:[{}]".format(r.status_code))
            self.wasMidwayInitalized = True
            break
          
          else:
            logInfo("=======> r.status_code:[{}]".format(r.status_code))
            sleepTime += sleepTime + sleepTime * random.random()
            
            #if sleepTime > self.maxWaitTimeForRateExceeded:
            #  sleepTime = self.maxWaitTimeForRateExceeded * 0.5 + self.maxWaitTimeForRateExceeded * random.random()
            sleepTime = self.maxWaitTimeForRateExceeded * random.random()
              
            logInfo("sleeping in {:.3f} seconds because '{}' is returned".format(sleepTime, r.content))
            time.sleep(sleepTime)

      else:
          
        self.wasMidwayInitalized = True
    except Exception as e:
      logException("unable to decode r.status_code:[{}]->Error:[{}]".format(r.status_code, e))
        
    return r  

  def request(self, url, payload = None, headers = None, cookies = None, timeout = None, verify = False):
    try:
      r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry = 0)
    except Exception as e:
      logException("unable to request to {} with payload:[{}]".format(url, payload))
      try:
        #self.activeMidwayCookie_dict = self.getMidwayCookie()
        self.SESSION_COOKIES = {}
        self.SESSION = requests.Session()
        #
        r = self.sessionRequest(url, payload, headers, cookies, timeout, verify, retry = 0)
      except Exception as e:
        #errMsg = logException("unable to request to {} with payload:[{}]".format(url, payload))
        self.addDeadRequest(url, payload, headers, cookies, timeout, verify, retry = 0, errMsg = "{}".format(e))
        
        class thisMidwayErrorResponse:
          status_code = 500
          content = "{}".format(e).encode()
          
        r = thisMidwayErrorResponse
    
    return r
      
  def addDeadRequest(self, url, payload = None, headers = None, cookies = None, timeout = None, verify = False, retry = None, errMsg = None):
    deadRequest_dict = {"time":getDateString(time.time()), "url":url, "payload":payload, "headers":headers, "cookies":cookies, "timeout":timeout, "verify":verify, "errMsg":errMsg}
    try:
      self.deadRequest_list.append(deadRequest_dict)
    except:
      logException("unable to add a dead request:{}".format(deadRequest_dict))
    
    return deadRequest_dict
  
  def getDeadRequests(self):
    logDebug("deadRequests:{}".format(len(self.deadRequest_list)))
    
    return self.deadRequest_list
  
  def notifyMidwayCookieExpiration(self):
    logDebug("initiated")
    
    elapsedTime = time.time() - self.notifiedTime
    if elapsedTime < 60:
      logWarn(f"Too short time to send a notification email because another notification might be sent {elapsedTime:.2f}s ago!")
      return elapsedTime
    
    itemDB = GcItemDB()
    try:
      elapsedTime = time.time() - itemDB.get(table="midway",key=self.user)
      if elapsedTime < 300:
        logWarn(f"Too short time to send a notification email because another notification might be sent {elapsedTime:.2f}s ago!")
        return elapsedTime
      else:
        itemDB.put(table="midway",key=self.user, value=time.time())
        expiredCookieEmail.send()
    except:
      itemDB.put(table="midway",key=self.user, value=time.time())
      expiredCookieEmail.send()
      
  def doAeaOptedOut(self):
    logDebug("initiated")
    
    elapsedTime = time.time() - self.aeaOptedOutTime
    if elapsedTime < 60:
      logWarn(f"Too short time to send a notification email because another notification might be sent {elapsedTime:.2f}s ago!")
      return elapsedTime
    
    itemDB = GcItemDB()
    try:
      elapsedTime = time.time() - itemDB.get(table="midway",key=f"aea.{self.user}")
      if elapsedTime < 300:
        logWarn(f"Too short time to send a notification email because another notification might be sent {elapsedTime:.2f}s ago!")
        return elapsedTime
      else:
        itemDB.put(table="midway",key=f"aea.{self.user}", value=time.time())
        self.runAeaOptedOut()
    except:
      itemDB.put(table="midway",key=f"aea.{self.user}", value=time.time())
      self.runAeaOptedOut()
      
  def runAeaOptedOut(self):
    logDebug("the aea opted out process is started........")
    try:
      url = "https://aga.aka.amazon.com/api/get-aea-auth-user-risk-score?user_name={}".format(self.userName)
      #url = "https://aea.aka.amazon.com/users/{}".format(username)
      payload = None
      
      r = self.sessionRequest(url, payload)
      logDebug("=====> [1] rContent:[{}]".format(r.content.decode()))  
      if r.status_code >= 400:
        aeaOptedOutInProgress = False
      else:
        #url = "https://gateway-api.us-west-2.aea.amazon.com/api/update-aea-auth-user"
        url = "https://aga.aka.amazon.com/api/update-aea-auth-user"
        payload = "OPTIONS"
        logInfo("payload:{}".format(payload))
      
        r = self.sessionRequest(url, payload)
        logInfo("=====> [2] r.content:[{}]".format(r.content.decode()))
        
        url = "https://aga.aka.amazon.com/api/get-csrf-token"
        payload = None
        r = self.sessionRequest(url, payload)
        logInfo("=====> [3]r.content:[{}]".format(r.content.decode()))
        try:
          csrf_token = json.loads(r.content.decode())["token"]
          
          url = "https://aga.aka.amazon.com/api/update-aea-auth-user"
          header_dict = {"anti-csrf-token": csrf_token}
          payload = json.dumps({"user_name":self.userName,"opted_out":True,"optout_reason":"Command line scripts are failing from cloud developer desktop"})
          logInfo("payload:{}".format(payload))
        
          r = self.sessionRequest(url= url, payload= payload, headers= header_dict)
          logInfo("=====> [3]r.content:[{}]".format(r.content.decode()))
          
          self.aeaOptedOutEmail()
          
        except:
          logExceptionWithValueError("unexpected response:[{}] from url:[{}],payload:[{}]".format(r.content.decode(), url, payload))
        
    except:
      logException("unable to get '{}.aea-opted-out' key".format(self.userName))
      aeaOptedOutInProgress = False
      
    return aeaOptedOutInProgress
  
  def aeaOptedOutEmail(self):
    gcEmail = GcEmail()
    gcEmail.setDefaultEmailDomain("amazon.com")
    gcEmail.setEmailType("html")
    gcEmail.setFromAlias("moduaws-no-reply")
    gcEmail.addToAlias("{}".format(self.userName))
    gcEmail.addBCCAlias("moduaws-no-reply")
    
    gcEmail.setSubject("[moduAWS] {}@, your AEA opted out ({})".format(self.userName, getHomeURL()))
    
    html = "Hi,"
    html += "<br>"
    html += "<br>"
    html += "Your AEA has been opted out."
    html += "<br>"
    html += "Please review the status at <a href='https://aea.aka.amazon.com/users/{}'>here</a>".format(self.userName)
    html += "<br>"
    html += "<br>"
    html += "Thanks,"
    html += "<br>"
    html += "<b>moduAWS</b>"
    html += "<br>"
    html += "<a href='{}'>{}</a>".format(getHomeURL(), getHomeURL())
    html += "<br>"
    html += "<br>"
    html += "date:{}".format(getDateString("now"))
    gcEmail.setConext(html)
    
    gcEmail.sendEmail()

  def mRequest(self, url, payload=None, headers=None, cookies=None, timeout=None, verify=False, verbose=False):
    if headers != None and isinstance(headers, str):
      for headerItem in headers.split("\n"):
        for headerItem in headerItem.split("\r"):
          header_list = headerItem.strip().split(":")
          if len(header_list) == 2:
            if header_list[0].strip() in ["Cookie", "Host"]:
              logDebug("ignored {}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
            else:
              self.addHeaders(key=header_list[0].strip(), data=header_list[1].strip())
              if verbose:
                logDebug("{}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
          elif len(header_list) > 2:
            header_list = ["{}".format(headerItem[:headerItem.strip().find(":")]).strip()]
            header_list.append("{}".format(headerItem[headerItem.strip().find(":")+1:].strip()))
            
            if verbose:
              logDebug("{}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
                           
          else:
            logWarn("unexpected header(len:{:,}):[{}]".format(len(header_list), headerItem))
    
    try:
      r = self.request(url, payload, headers, cookies, timeout, verify)
      return r.json()
    except:
      try:
        return r.content.decode()
      except:
        try:
          return r.content
        except:
          raiseValueError("unexpected {}:r:[{}]".format(type(r).__name__, r))
          
    return 
  
def mRequest(pdxMidway, url, payload=None, headers="", verbose=False):
  if payload == None:
    r = pdxMidway.request(url, payload)
    if verbose:
      logDebug("r.content(len:{:,}):[{}]".format(len(r.content), r.content))
  
  if headers != None and isinstance(headers, str):
    for headerItem in headers.split("\n"):
      for headerItem in headerItem.split("\r"):
        header_list = headerItem.strip().split(":")
        if len(header_list) == 2:
          if header_list[0].strip() in ["Cookie", "Host"]:
            logDebug("ignored {}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
          else:
            pdxMidway.addHeaders(key=header_list[0].strip(), data=header_list[1].strip())
            if verbose:
              logDebug("{}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
        elif len(header_list) > 2:
          header_list = ["{}".format(headerItem[:headerItem.strip().find(":")]).strip()]
          header_list.append("{}".format(headerItem[headerItem.strip().find(":")+1:].strip()))
          
          if verbose:
            logDebug("{}:[{}]".format(header_list[0].strip(), header_list[1].strip()))
                         
        else:
          logWarn("unexpected header(len:{:,}):[{}]".format(len(header_list), headerItem))
  
  r = pdxMidway.request(url, payload)
  
  return r
  