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
Modified on Apr 23, 2023

@contributor: hoeseong
'''
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from pathway import updateMsg

from os.path import expanduser

import time
import json

class MidwayCookieHandler():
  def __init__(self, request_dict, logMessage_list, errorReason_list):
    self.logMessage_list = logMessage_list
    self.errorReason_list = errorReason_list

    self.localCookies = request_dict["metadata"]["localCookies"]

    self.userAccountId = request_dict["metadata"]["awsAccountId"]
    self.userName = request_dict["metadata"]["userName"]
    
    self.user = None

    self.midwayCookie = None
    self.localMidwayCookiePath = "~/.midway/cookie"
    
    self.midwayKeyLocation = "s3"
    self.midwayCookieTTL = 840
    
    self.s3Manager = None
       
  def getMidwayCookie(self, midwayCookie=None):
    if midwayCookie == None:
      midwayCookie = self.localCookies
    #else:
      #logDebug("midwayCookie(len:{:,}) is provided".format(len(midwayCookie)))
      
    midwayCookie_dict = {"global":{}, "cn":{}}
    try:
      globalCookie_dict = {}
      cnMidwayCookie_dict = {}
      
      for line in midwayCookie.split("\n"):
        for subLine in line.split("\r"):
          if "tpm_metrics" in subLine:
            continue
          
          elif subLine.startswith("#HttpOnly_midway-auth.aws-border.cn"):
            self.isCnMidway = True
            
            line_list = subLine.split()
            lineCount = 0
            for value in line_list:
              ##logDebug("#{}(len:{}):[{}]".format(lineCount, len(value), value))
              if len(value) == 10:
                try:
                  cnMidwayCookie_dict["expirationTime"] = int(value)
                  if cnMidwayCookie_dict["expirationTime"] - time.time() > self.midwayCookieTTL:
                    cnMidwayCookie_dict["active"] = True
                  else:
                    cnMidwayCookie_dict["active"] = False
                  
                  ##logDebug("#cn:expirationTime:[{}]({}) is found at location:[{}]".format(cnMidwayCookie_dict["expirationTime"], cnMidwayCookie_dict["active"], lineCount))
                except:
                  logError("unable to get 'expiredTime' from midway cookie:[{}]".format(line_list))
              elif len(value) > 256:
                try:
                  cnMidwayCookie_dict["sessionId"] = value
                  ##logDebug("#cn:sessionId:[len:{:,}] is found at location:[{}]".format(len(cnMidwayCookie_dict["sessionId"]), lineCount))
                except:
                  logException("unexpected midway cookie format:[{}]".format(subLine))
              
              lineCount += 1
          
            midwayCookie_dict["cn"] = cnMidwayCookie_dict
            
          elif line.startswith("#HttpOnly_.midway-auth.aws-border.cn"):
            self.isCnMidway = True
            
            line_list = subLine.split()
            lineCount = 0
            for value in line_list:
              ##logDebug("#{}(len:{}->{}):[{}]".format(lineCount, len(value), len(value.strip()), value))
              if len(value) > 256:
                try:
                  cnMidwayCookie_dict["aea"] = value
                  ##logDebug("#cn:aea:[len:{:,}] is found at location:[{}]".format(len(cnMidwayCookie_dict["aea"]), lineCount))
                except:
                  logException("unexpected midway cookie format:[{}]".format(subLine))
              
              lineCount += 1
            
            midwayCookie_dict["cn"] = cnMidwayCookie_dict
            
          elif subLine.startswith("midway-auth.aws-border.cn"):
            line_list = subLine.split()
            lineCount = 0
            #for value in line_list:
            #  logDebug("{}:[{}]".format(lineCount, value))
            #  lineCount += 1
            
            lineCount = 0
            userName_offset = 0
            for value in line_list:
              ##logDebug("#{}:cn_user:[{}]".format(lineCount, value))
              if value in ["user_name"]:
                userName_offset = lineCount
              lineCount += 1
            
            try:
              ##logDebug("#cn:line_list[{}]:[{}]".format(userName_offset, line_list[userName_offset]))
              cnMidwayCookie_dict["user"] = line_list[userName_offset+1]
              
            except:
              logError("unable to get 'expiredTime' from midway cookie:[{}]".format(line_list))
              cnMidwayCookie_dict["user"] = None
            
            midwayCookie_dict["cn"] = cnMidwayCookie_dict
            
          elif line.startswith("#HttpOnly_midway-auth.amazon.com"):
            
            self.isGlobalMidway = True
            
            line_list = subLine.split()
            lineCount = 0
            for value in line_list:
              ##logDebug("#{}(len:{}->{}):[{}]".format(lineCount, len(value), len(value.strip()), value))
              if len(value) == 10:
                try:
                  globalCookie_dict["expirationTime"] = int(value)
                  if globalCookie_dict["expirationTime"] - time.time() > 60:
                    globalCookie_dict["active"] = True
                  else:
                    globalCookie_dict["active"] = False
                      
                  ##logDebug("#global:expirationTime:[{}]({}) is found at location:[{}]".format(globalCookie_dict["expirationTime"], globalCookie_dict["active"], lineCount))
                except:
                  logError("unable to get 'expiredTime' from midway cookie:[{}]".format(line_list))
              elif len(value) > 256:
                try:
                  globalCookie_dict["sessionId"] = value
                  ##logDebug("#global:sessionId:[len:{:,}] is found at location:[{}]".format(len(globalCookie_dict["sessionId"]), lineCount))
                except:
                  logException("unexpected midway cookie format:[{}]".format(subLine))
              
              lineCount += 1
              
            midwayCookie_dict["global"] = globalCookie_dict
          
          elif line.startswith("#HttpOnly_.midway-auth.amazon.com"):
            self.isGlobalMidway = True
            
            line_list = subLine.split()
            lineCount = 0
            for value in line_list:
              ##logDebug("#{}(len:{}->{}):[{}]".format(lineCount, len(value), len(value.strip()), value))
              if len(value) > 256:
                try:
                  globalCookie_dict["aea"] = value
                  ##logDebug("#global:aea:[len:{:,}] is found at location:[{}]".format(len(globalCookie_dict["aea"]), lineCount))
                except:
                  logException("unexpected midway cookie format:[{}]".format(subLine))
              
              lineCount += 1
            
            midwayCookie_dict["global"] = globalCookie_dict
            
          
          elif subLine.startswith("midway-auth.amazon.com"):
            
            line_list = subLine.split()
            lineCount = 0
            userName_offset = 0
            for value in line_list:
              ##logDebug("#{}:global_user:[{}]".format(lineCount, value))
              if value in ["user_name"]:
                userName_offset = lineCount
              lineCount += 1
            
            try:
              ##logDebug("#global:line_list[-1]:[{}]".format(line_list[-1]))
              globalCookie_dict["user"] = line_list[userName_offset+1]
              
            except:
              logError("unable to get 'user' from midway cookie:[{}]".format(line_list))
              globalCookie_dict["user"] = None
      
          #end if "tpm_metrics" in subLine:
        #end for subLine in line.split("\r"):
      #end for line in midwayCookie.split("\n"):
            
      if "user" in cnMidwayCookie_dict.keys() and "user" in globalCookie_dict.keys():
        if globalCookie_dict["user"] == cnMidwayCookie_dict["user"]:
          self.user = globalCookie_dict["user"]
          #logDebug("#cn==global:midwayCookie is set by username:[{}]".format(self.user))
        else:
          logWarn("global:user:[{}] is not equal to cn:user:[{}]".format(globalCookie_dict["user"], self.user))
          self.user = globalCookie_dict["user"]
          #logDebug("#cn!=global:midwayCookie is set by username:[{}]".format(self.user))
      elif "user" in globalCookie_dict.keys():
        self.user = globalCookie_dict["user"]
        #logDebug("#global:midwayCookie is set by username:[{}]".format(self.user))
      elif "user" in cnMidwayCookie_dict.keys():
        self.user = cnMidwayCookie_dict["user"]
        #logDebug("#cn:midwayCookie is set by username:[{}]".format(self.user))
      else:
        self.user = self.userName
        logWarn("user not found at both cn and global, so userName:[{}] is set".format(self.userName))
          
    except:
      logException("unable to get 'midway' cookie from {}".format(self.midwayKeyLocation))
    
    if self.userName != self.user:
      logWarn("userName:[{}] is not matched with user:[{}]".format(self.userName, self.user))
    else:
      logDebug("userName:[{}] is the same user:[{}]".format(self.userName, self.user))
      
    if "active" in midwayCookie_dict["global"].keys() and "active" in midwayCookie_dict["cn"].keys():
      if midwayCookie_dict["global"]["active"] == True and midwayCookie_dict["cn"]["active"] == True:
        pass
      else:
        raiseValueError(updateMsg(self.errorReason_list, json.dumps(
            {
              'global':'expired {:.2f} hours ago'.format((globalCookie_dict["expirationTime"] - time.time())/3600),
              'cn':'expired {:.2f} hours ago'.format((globalCookie_dict["expirationTime"] - time.time())/3600),
              'error':'(#498)unable to get the active midway keys in "global" and "cn"'
              }
            )
          ))
    elif "active" in midwayCookie_dict["global"].keys():
      if midwayCookie_dict["global"]["active"] == True:
        pass
      else:
        raiseValueError(updateMsg(self.errorReason_list, json.dumps(
            {
              "global":"expired {:.2f} hours ago".format((globalCookie_dict["expirationTime"] - time.time())/3600),
              "error":"(#510)unable to get the active midway keys in 'global'",
              }
            )
          ))
    elif "active" in midwayCookie_dict["cn"].keys():
      if midwayCookie_dict["cn"]["active"] == True:
        pass
      else:
        raiseValueError(updateMsg(self.errorReason_list, json.dumps(
            {
              "cn":"expired {:.2f} hours ago".format((globalCookie_dict["expirationTime"] - time.time())/3600),
              "error":"(#522)unable to get the active midway keys in 'cn'",
              }
            )
          ))
    else:
        raiseValueError(updateMsg(self.errorReason_list, json.dumps(
            {
              "error":"(#529)unexpected midwayCookie_dict:[{}]".format(midwayCookie_dict)
              }
            )
          ))
    #try:
    #  for key in midwayCookie_dict.keys():
    #    logDebug("{}:[{}]".format(key, midwayCookie_dict[key]))
    #  time.sleep(1)
    #except:
    #  logException("unexpected Error")
      
    return midwayCookie_dict
     


