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
from graphcode.conf import getATKPath
from graphcode.path import createDir

from os import mkdir, remove
from os.path import join, exists, expanduser

import os
import stat
import platform
import time

import secrets

class GcAuthToken():
  def __init__(self):
    
    self.atkDir = getATKPath()
    
    if exists(expanduser(self.atkDir)):
      logDebug("atkDir:[{}] is found".format(self.atkDir))
    else:
      createDir(self.atkDir)
      logDebug("atkDir:[{}] is created".format(self.atkDir))
    
  def createToken(self, aliasId = "", length=32):
    if length < 16:
      logWarn("token length should be larger than 16, so the length is set to 16")
      length = 16
      
    token = secrets.token_urlsafe(length) 
    #logDebug("token:[{}]".format(token))
    
    f = open(join(expanduser(self.atkDir), "{}.{}".format(aliasId,token)), "w")
    f.write("")
    f.close()
    #logDebug("token:[{}]".format(join(expanduser(self.atkDir), token)))
    
    return token 
  
  def isValidToken(self, token, aliasId = ""):
    if isinstance(token, str) and len(token) >= 16:
      #logDebug("token:[{}]".format(join(expanduser(self.atkDir), token)))
      tokeFile = join(expanduser(self.atkDir), "{}.{}".format(aliasId,token))
      if exists(tokeFile):
        if platform.system() == 'Windows':
          createTime =  os.path.getctime(tokeFile)
        else:
          stat = os.stat(tokeFile)
          try:
            createTime = stat.st_birthtime
          except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            createTime = stat.st_mtime
        logDebug("createTime:[{}]->currentTime:[{}](ttL:{})".format(createTime, time.time(), time.time() - createTime))   
        remove(tokeFile)
        if (time.time() - createTime) <= 86400:
          return True
        else:
          return False
      else:
        return False
    else:
      return False
              

  