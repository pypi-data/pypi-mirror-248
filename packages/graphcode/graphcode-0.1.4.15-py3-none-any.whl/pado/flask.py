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

from pado.conf import *

from pado.templates import GcTemplates

from flask import Flask, request, render_template, redirect, url_for, send_from_directory

from os.path import basename, dirname, join, abspath

import socket

from multiprocessing import Process

import time

import os

def isHtmlTag(value):
  if isinstance(value, str) and value.startswith("__htmlTag__."):
    #logDebug("value:[{}]".format(value))
    return True
  else:
    return False
 
def htmlTag(value):
  if isinstance(value, str) and value.startswith("__htmlTag__."):
    #logDebug("value:[{}]".format(value))
    return value[12:]
  else:
    return value
 
def dollar(value):
  if isinstance(value, int) or isinstance(value, float):
    return "${:,}".format(value)
  else:
    return "${}".format(value)
  
def usdollar(value):
  if isinstance(value, float):
    if value > 1000000:
      return "${:,.2f}M".format(value/1000000)
    elif value > 1000:
      return "${:,.2f}K".format(value/1000)
    else:
      return "${:,.2f}".format(value)
  elif isinstance(value, int):
    if value > 1000000:
      return "${:,.2f}M".format(value/1000000)
    elif value > 1000:
      return "${:,.2f}K".format(value/1000)
    else:
      return "${:,}".format(value)
  else:
    return value

def usdollar12m(value):
  if isinstance(value, float):
    if value*12 > 1000000:
      return "${:,.2f}M".format(value*12/1000000)
    elif value*12 > 1000:
      return "${:,.2f}K".format(value*12/1000)
    else:
      return "${:,.2f}".format(value*12)
  else:
    return value*12

def number(value):
  if isinstance(value, float):
    return "{:,.2f}".format(value)
  elif isinstance(value, int):
    return "{:,}".format(value)
  else:
    return value
  
def percentage(value):
  if isinstance(value, float):
    return "{:,.2f}%".format(value)
  elif isinstance(value, int):
    return "{:,}%".format(value)
  else:
    return value
  
def length25000(value):
  if isinstance(value, list):
    if len(value) > 25000:
      return value[:25000]
    else:
      return value
  elif isinstance(value, dict):
    if len(value.keys()) > 25000:
      thisValue_dict = {}
      thisItemCount = 0
      for thisKey in thisValue_dict.keys():
        thisValue_dict[thisKey] = thisValue_dict[thisKey]
      
      thisItemCount += 1
      if thisItemCount > 25000:
        return thisValue_dict
    else:
      return value
  else:
    return value

def iterate(value):
  resultTag = ""
  try:
    if isinstance(value, dict):
      for key in value.keys():
        if key in ["outputs", "charts"]:
          resultTag += "<b>{}</b>:<br>".format(key)
          for key2 in value[key].keys():
            if key2 in ["wbResults", "charts"]:
              resultTag += "&nbsp;&nbsp;&nbsp;&nbsp;<b>{}</b>:<br>".format(key2)
            
            elif isinstance(value[key][key2], dict):
              resultTag += "&nbsp;&nbsp;&nbsp;&nbsp;<b>{}</b>:<br>".format(key2)
              for key3 in value[key][key2].keys():
                resultTag += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>{}</b>:{}<br>".format(key3, value[key][key2][key3])
            else:
              resultTag += "&nbsp;&nbsp;&nbsp;&nbsp;<b>{}</b>:{}<br>".format(key2, value[key][key2])
        elif key in ["profileSelect"]:
          resultTag += "<b>{}</b>:<br>".format(key)
          for key2 in value[key].keys():
            resultTag += "&nbsp;&nbsp;&nbsp;&nbsp;<b>{}</b>:<br>".format(key2, len(value[key][key2]))
            
        elif key in ["jsCharts"]:
          resultTag += "<b>{}</b>:len:{:,}<br>".format(key, len(value[key]))
        else:
          resultTag += "<b>{}</b>:{}<br>".format(key, value[key])
    else:
      resultTag = json.dump(value)
  except Exception as e:
    resultTag =  logException("Error:[{}]->unable to unpack value:[{}]".format(e, value))
  
  if len(resultTag) > 25000:
    resultTag = "size:{:,}Bytes<br>displaying the first 25K in the value:<br>{}..........{}".format(len(resultTag),resultTag[:25000],resultTag[-1000:])
    
  return resultTag

class GcFlask:
  def __init__(self, gcTemplates = None):
    if isinstance(gcTemplates, GcTemplates):
      self.homeDir = gcTemplates.homeDir
      logDebug("homeDir:[{}]".format(self.homeDir))
      
      self.confPath = gcTemplates.confPath
      logDebug("confPath:[{}]".format(self.confPath))
      
      self.serviceConf_dict = gcTemplates.serviceConf_dict
      logDebug("serviceConf_dict:[{}]".format(self.serviceConf_dict))
      
      self.frameConf_dict = gcTemplates.frameConf_dict
      logDebug("frameConf_dict:[{}]".format(self.frameConf_dict))
      
      self.cssConf_dict = gcTemplates.cssConf_dict
      logDebug("cssConf_dict:[{}]".format(self.cssConf_dict))
      
      self.jsConf_dict = gcTemplates.jsConf_dict
      logDebug("jsConf_dict:[{}]".format(self.jsConf_dict))
      
      self.nav_conf = gcTemplates.nav_conf
      logDebug("nav_conf:[{}]".format(self.nav_conf))
      
      self.static_dir = gcTemplates.static_dir
      logInfo("static_dir:[{}]".format(self.static_dir))
      
      self.template_dir = gcTemplates.template_dir
      logInfo("template_dir:[{}]".format(self.template_dir))
      
      self.rules_dict = gcTemplates.rules_dict
      logInfo("rules_dict:[{}]".format(self.rules_dict))
      
    else:
      raise ValueError("gcTemplates:[{}] is not the type:GcTemplates".format(gcTemplates))
    
    self.homeURL = None
    self.allowedHost = None
    self.servicePortNumber = None
    self.debugMode = None
    self.sslMode = None
    self.sslContext = None
    
    localHostname = None
    externalHostname = None
    try:
      for stage in self.serviceConf_dict.keys():
        if isinstance(self.serviceConf_dict[stage], dict) and "homeURL" in self.serviceConf_dict[stage].keys():
          logDebug("stage:[{}]:[{}]".format(stage, self.serviceConf_dict[stage]))
          
          localHostname = socket.gethostname()
          #logDebug("localHostname:[{}]".format(localHostname))
          localIp = socket.gethostbyname(localHostname)
          externalHostname = self.serviceConf_dict[stage]["homeURL"]
          confIp = socket.gethostbyname(externalHostname)
          #logDebug("local:[{}] -> confIp:[{}]".format(localIp, confIp))
          if localIp == confIp:
            self.loadServiceParameters(stage)
            break
    except:
      try:
        logException("unable to determine the stage of this localHostname:[{}]->externalHostname:[{}] (Please check '$ dig {}'".format(localHostname, externalHostname, externalHostname))
      except:
        logException("unable to determine the stage of this host")
        
      if self.homeURL == None:
        self.loadServiceParameters("localhost")
    
    if self.homeURL == None:
      self.loadServiceParameters("localhost")
        
    self.request = request
    self.app = Flask(self.serviceConf_dict["name"], static_folder=self.static_dir, template_folder=self.template_dir)
    
    self.addFilters()
    self.addRules()
    
    
  def loadServiceParameters(self, stage):
    if stage in self.serviceConf_dict.keys():
      self.homeURL = self.serviceConf_dict[stage]["homeURL"]
      self.allowedHost = self.serviceConf_dict[stage]["host"]
      self.servicePortNumber = self.serviceConf_dict[stage]["port"]
      self.debugMode = self.serviceConf_dict[stage]["debug"]
      self.sslMode = self.serviceConf_dict["localhost"]["ssl"]
      if self.sslMode:
        if "cert" in self.serviceConf_dict["localhost"].keys() and "key" in self.serviceConf_dict["localhost"].keys():
          if exists(self.serviceConf_dict["localhost"]["cert"]) and exists(self.serviceConf_dict["localhost"]["key"]):
            self.sslContext = (self.serviceConf_dict["localhost"]["cert"], self.serviceConf_dict["localhost"]["key"])
          else:
            self.sslContext = "adhoc"
        else:
          self.sslContext = "adhoc"
      else:
        self.sslContext = None
    else:
      self.homeURL = self.serviceConf_dict["localhost"]["homeURL"]
      self.allowedHost = self.serviceConf_dict["localhost"]["host"]
      self.servicePortNumber = self.serviceConf_dict["localhost"]["port"]
      self.debugMode = self.serviceConf_dict["localhost"]["debug"]
      self.sslMode = self.serviceConf_dict["localhost"]["ssl"]
      if self.sslMode:
        if "cert" in self.serviceConf_dict["localhost"].keys() and "key" in self.serviceConf_dict["localhost"].keys():
          if exists(self.serviceConf_dict["localhost"]["cert"]) and exists(self.serviceConf_dict["localhost"]["key"]):
            self.sslContext = (self.serviceConf_dict["localhost"]["cert"], self.serviceConf_dict["localhost"]["key"])
          else:
            self.sslContext = "adhoc"
        else:
          self.sslContext = "adhoc"
      else:
        self.sslContext = None
      
      
  def loadFlaskConf(self, stage):
    if stage in self.serviceConf_dict.keys():
      try:
        logInfo("allowedHost:[{}]".format(self.serviceConf_dict[stage]["allowedHost"]))
        self.allowedHost = self.serviceConf_dict[stage]["allowedHost"]
      except:
        logException("unable to set 'allowedHost' with gcApp_dict:[{}]".format(self.serviceConf_dict[stage]))
        self.allowedHost = "127.0.0.1"
      
      try:
        logInfo("servicePortNumber:[{}]".format(self.serviceConf_dict[stage]["servicePortNumber"]))
        self.servicePortNumber = self.serviceConf_dict[stage]["servicePortNumber"]
      except:
        logException("unable to set 'servicePortNumber' with gcApp_dict:[{}]".format(self.serviceConf_dict[stage]))
        self.servicePortNumber = "443"
      
      try:
        logInfo("debugMode:[{}]".format(self.serviceConf_dict[stage]["debugMode"]))
        self.debugMode = self.serviceConf_dict[stage]["debugMode"]
      except:
        logException("unable to set 'debugMode' with gcApp_dict:[{}]".format(self.serviceConf_dict[stage]))
        self.debugMode = True
      
      try:
        logInfo("sslMode:[{}]".format(self.serviceConf_dict[stage]["sslMode"]))
        self.sslMode = self.serviceConf_dict[stage]["sslMode"]
      except:
        logException("unable to set 'sslMode' with gcApp_dict:[{}]".format(self.serviceConf_dict[stage]))
        self.sslMode = True
      
      try:
        logInfo("sslContext:[{}]".format(self.serviceConf_dict[stage]["sslContext"]))
        self.sslContext = self.serviceConf_dict[stage]["sslContext"]
      except:
        logException("unable to set 'sslContext' with gcApp_dict:[{}]".format(self.serviceConf_dict[stage]))
        self.sslContext = 'adhoc'
  
  def setAllowedHost(self, allowedHost):
    if allowedHost == "localhost":
      allowedHost = "127.0.0.1"
      
    if isinstance(allowedHost, str) != True:
      logWarn("allowedHost:[{}] should be 'str' type instead of '{}' type".format(allowedHost, type(allowedHost)))
      return None
    
    allowedHost_list = allowedHost.split(".")
    if len(allowedHost_list) != 4:
      logWarn("allowedHost should be 'x.x.x.x' format instead of '{}'".format(allowedHost))
      return None
    
    n = 0
    for x in allowedHost_list:
      n += 1
      try:
        x = int(x)
        if x < 1 or x > 255:
          logWarn("allowedHost:[{}]({}) should be 'int' type between 1 and 255".format(allowedHost, n))
          return None
      except:
        logWarn("allowedHost:[{}]({}) should be 'int' type".format(allowedHost, n))
        return None
      
    self.allowedHost = allowedHost
  
  def getAllowedHost(self):
    return self.allowedHost
  
  def setServicePort(self, servicePortNumber):
    if isinstance(servicePortNumber, str):
      try:
        servicePortNumber = int(servicePortNumber)
      except:
        logWarn("servicePortNumber couldn't be converted to 'int' from '{}'".format(servicePortNumber))
        return None
    
    if isinstance(servicePortNumber, int) != True:
      logWarn("servicePortNumber should be 'int' instead of '{}' type".format(type(servicePortNumber)))
      return None
    
    if servicePortNumber < 1 or servicePortNumber > 65530:
      logWarn("servicePortNumber:[{}] should be between 1 and 65530".format(servicePortNumber))
      return None
    
    self.servicePortNumber = servicePortNumber
  
  def getServicePort(self):
    return self.servicePortNumber
  
  def setDebugMode(self, debugMode):
    if isinstance(debugMode, bool):
      self.debugMode = debugMode
    else:
      logWarn("debugMode should be 'bool' type instead of '{}' type".format(type(debugMode)))
  
  def getDebugMode(self):
    return self.debugMode
  
  def setSslMode(self, sslMode):
    if isinstance(sslMode, bool):
      self.sslMode = sslMode
    else:
      logWarn("sslMode should be 'bool' type instead of '{}' type".format(type(sslMode)))
  
  def getSslMode(self):
    return self.sslMode
  
  def getSslContext(self):
    return self.sslContext

  def default_view(self):
    return render_template("index.html")
  
  def page_not_found(self, e):
    return render_template('_e404.html'), 404
  
  def internal_server_error(self, e):
    return render_template('_e500.html'), 500
  
  def favicon(self):
    return send_from_directory(join(self.app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')
  
  def addFavicon(self):
    self.app.add_url_rule(rule = "/favicon.ico", view_func = self.favicon)
    
  def addPageNotFoundRule(self):
    self.app.register_error_handler(404, self.page_not_found)
  
  def addInternalServerErrorRule(self):
    self.app.register_error_handler(500, self.internal_server_error)
  
  def addFilters(self):
    self.app.add_template_filter(isHtmlTag)
    self.app.add_template_filter(htmlTag)
    self.app.add_template_filter(number)
    self.app.add_template_filter(number)
    self.app.add_template_filter(dollar)
    self.app.add_template_filter(usdollar)
    self.app.add_template_filter(percentage)
    self.app.add_template_filter(iterate)
    
  def addRules(self):
    self.addPageNotFoundRule()
    self.addInternalServerErrorRule()
    self.addFavicon()
    
    for ruleName in self.rules_dict.keys():
      if ruleName.startswith("__"):
        logWarn("ruleName:[{}] is ignored".format(ruleName))
        continue
      
      try:
        logDebug("ruleName:[{}], method:[{}]".format(ruleName, self.rules_dict[ruleName]["methods"]))
        #self.app.add_url_rule(rule = self.rules_dict[ruleName]["endpoint"], methods = self.rules_dict[ruleName]["methods"], view_func = self.rules_dict[ruleName]["view"].view)
        if ruleName in ["midway","signin2","login", "overview"]:
          self.app.add_url_rule(rule = self.rules_dict[ruleName]["endpoint"], view_func = self.rules_dict[ruleName]["view"].view, methods=['POST','GET'])
        else:
          self.app.add_url_rule(rule = self.rules_dict[ruleName]["endpoint"], view_func = self.rules_dict[ruleName]["view"].view)
          
        logInfo("endpoint:[{}]({}) is added with view_func:[{}]".format(self.rules_dict[ruleName]["endpoint"], self.rules_dict[ruleName]["name"], self.rules_dict[ruleName]["view"].view))

      except:
        logExceptionWithValueError("unable to add rule[{}]({}:{}):[{}]".format(self.rules_dict[ruleName]["endpoint"], self.rules_dict[ruleName]["name"], self.rules_dict[ruleName]["methods"], self.rules_dict[ruleName]["view"].view)) 

  def run(self):
    logInfo("allowedHost:[{}]".format(self.getAllowedHost()))
    logInfo("getServicePort:[{}]".format(self.getServicePort()))
    logInfo("getDebugMode:[{}]".format(self.getDebugMode()))
    logInfo("getSslContext:[{}]".format(self.getSslContext()))

    gcConf = GcConf()
  
    if self.getSslMode():
      if exists(join(gcConf.getHomeDirectory(), "certs/moduaws_aka_amazon_com.crt")):
        context = (join(gcConf.getHomeDirectory(), "certs/moduaws_aka_amazon_com.crt"), join(gcConf.getHomeDirectory(), "certs/moduaws_aka_amazon_com.pem"))
        logDebug(f"context:{context}")
        self.app.run(host=self.getAllowedHost(), port=self.getServicePort(), debug=self.getDebugMode(), ssl_context=context)
        
      else:
        self.app.run(host=self.getAllowedHost(), port=self.getServicePort(), debug=self.getDebugMode(), ssl_context=self.getSslContext())
        
    else:
      self.app.run(host=self.getAllowedHost(), port=self.getServicePort(), debug=self.getDebugMode())