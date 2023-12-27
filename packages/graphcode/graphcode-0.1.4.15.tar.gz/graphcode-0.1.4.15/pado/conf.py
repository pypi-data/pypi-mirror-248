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
Created on June 21, 1998

@author: Ryeojin Moon
'''
#from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError
from graphcode.conf import loadDefaultServiceConfigurations, loadFrame, loadCSS, loadJS, loadModal, loadNav, getRoot, getRulesPath, getStaticPath, getTemplatePath, getDefaultAccounts
from graphcode.path import createDir

from os.path import basename, dirname, join, abspath, exists, expanduser

from cryptography.fernet import Fernet

import platform

import json

class GcConf:
  def __init__(self, homeDir = "./"):
    
    try:
      self.homeDir = abspath(homeDir)
      #logDebug("#homeDir:[{}]".format(self.homeDir))
      
      self.confPath = join(self.homeDir, "conf")
      #logDebug("#confPath:[{}]".format(self.confPath))
      createDir(self.confPath)
      
      self.serviceConf_dict = loadDefaultServiceConfigurations()
      #logDebug("#serviceConf_dict:[{}]".format(self.serviceConf_dict))
      
      self.frameConf_dict = loadFrame()
      #logDebug("#frameConf_dict:[{}]".format(self.frameConf_dict))
      
      self.cssConf_dict = loadCSS()
      #logDebug("#cssConf_dict:[{}]".format(self.cssConf_dict))
      
      self.jsConf_dict = loadJS()
      #logDebug("#jsConf_dict:[{}]".format(self.jsConf_dict))
      
      self.modalConf_dict = loadModal()
      #logDebug("#modalConf_dict:[{}]".format(self.modalConf_dict))
      
      self.nav_conf = loadNav()
      #logDebug("#nav_conf:[{}]".format(self.nav_conf))
      
      self.static_dir = getStaticPath()
      #logInfo("#static_dir:[{}]".format(self.static_dir))
      createDir(self.static_dir)
      
      self.template_dir = getTemplatePath()
      #logInfo("#template_dir:[{}]".format(self.template_dir))
      
      self.rulesPath = getRulesPath()
      #logDebug("#rulesPath:[{}]".format(self.rulesPath))
      createDir(self.rulesPath)
      
    except:
      logExceptionWithValueError("unable to load configuration at homeDir:[{}]".format(homeDir))
    
    
  def loadConf(self, confPath):
    try:
      f = open(confPath, "r")
      return json.load(f)
    except:
      logExceptionWithValueError("unable to load conf:[{}]".format(confPath))
  
  def getHomeDirectory(self):
    
    return getRoot()
  
  def getDefaultAccounts(self):
    return getDefaultAccounts()  
    
