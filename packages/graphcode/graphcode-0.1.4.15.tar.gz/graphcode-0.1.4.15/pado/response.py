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

from graphcode.conf import getServiceName, getVersion, getCopyRight, getBuildNumber
from graphcode.conf import getPrimaryAllowsGroups
from graphcode.conf import getDefaultCookies

from pado.form import GcForm
from graphcode.cipher import GcCipher
from pado.auth import GcAuthToken

from os.path import basename, dirname, join, abspath

from flask import Flask, Response, make_response, render_template, redirect, url_for

from datetime import timedelta, datetime
import time
from graphcode.lib import getDateString

import platform
import sys
from pado.chartV2 import GcChart

import json

class GcResponse:
  def __init__(self, request, form, action):
    self.__beginTime__ = time.time()
    
    # the user should be a member of each group. If the user is not a member of any group, the access is not granted.
    self.allowedPrimaryLdapGroup_list = getPrimaryAllowsGroups()
    
    self.request = request
    self.url_list = self.request.base_url.split("/")
    self.form_dict = form.form_dict
    self.action = action
    
    self.ruleName = self.getRuleName()
    logInfo("======>ruleName:[{}]".format(self.ruleName))
    
    try:
      self.title = f"{getServiceName()}"
      self.version = f"{getVersion()}"
      self.copyRight = f"Copyright &copy; {self.title}{self.version} {getCopyRight()}"
      self.buildNumber = getBuildNumber()
      
    except:
      logException("unable to load 'revision'")
      self.title = "moduAWS"
      self.version = "v12"
      self.copyRight = "Copyright &copy; {} {}".format(self.title, datetime.fromtimestamp(time.time()).strftime("%Y"))
      self.buildNumber = "-999"
    
    platformInfo = platform.uname()
    
    self.isValidAthenticityTokenStatus = None
    self.gcAuthToken = GcAuthToken()
    thisAction = self.request.args.get("action", "")
    if thisAction != "" and isinstance(thisAction, str) and len(thisAction) > 0:
      actionStatus = True
    else:
      actionStatus = False
    
    if len(self.ruleName.split("/")) > 1:
      rulePath = "{}".format(self.ruleName.split("/")[1])
    else:
      rulePath = ""
    
    
    if self.request.method == 'POST':
      
      self.gcResponse_dict = {
        "__beginTime__":time.time(),
        "homeURL":"{}://{}".format(self.url_list[0],self.url_list[2]),
        "platform": "{} {} {} {}".format(platformInfo.node, platformInfo.system, platformInfo.release, platformInfo.version),
        "pythonVersion": "{}".format(sys.version).split(" ")[0],
        "title": self.title,
        "version": self.version,
        "copyRight": self.copyRight,
        "buildNumber": self.buildNumber,
        "ruleName":self.ruleName.split("/")[0], 
        "rulePath": rulePath,
        "actionStatus": actionStatus,
        "action": self.request.form.get("action", ""),
        "outputFormat": False,
        "cookies": None,
        "form":{
          "species":self.request.form.get("species", ""),
          "atk":self.request.form.get("atk", ""),
          "iSL":self.request.form.get("iSL", ""),
          "authenticityTokenId":self.gcAuthToken.createToken(),
          "submit":self.request.form.get("submit", ""),
          },
        "errMsg":[],
        "charts":{},
        "profiles":{},
        "outputs":{}
        }
      
    else:
      self.gcResponse_dict = {
        "__beginTime__":time.time(),
        "homeURL":"{}://{}".format(self.url_list[0],self.url_list[2]),
        "platform": "{} {} {} {}".format(platformInfo.node, platformInfo.system, platformInfo.release, platformInfo.version),
        "pythonVersion": "{}".format(sys.version).split(" ")[0],
        "title": self.title,
        "version": self.version,
        "copyRight": self.copyRight,
        "buildNumber": self.buildNumber,
        "ruleName":self.ruleName.split("/")[0], 
        "rulePath": rulePath,
        "actionStatus": actionStatus,
        "action": self.request.args.get("action", ""),
        "outputFormat": False,
        "cookies": None,
        "form":{
          "species":self.request.args.get("species", ""),
          "atk":self.request.args.get("atk", ""),
          "iSL":self.request.args.get("iSL", ""),
          "authenticityTokenId":self.gcAuthToken.createToken(),
          "submit":self.request.args.get("submit", ""),
          },
        "errMsg":[],
        "charts":{},
        "profiles":{},
        "outputs":{}
        }
      
    self.secondRequest = False
    logDebug("form.form_dict:[{}]".format(form.form_dict.keys()))
    for formName in form.form_dict.keys():
      if formName in ["midwayPin", "midwayToken"]:
        logWarn("formName:[{}] is not updated due to security".format(formName))
        
      thisInput_dict = self.getInputValues(form.form_dict[formName])
      logDebug("formName:[{}]:[{}]".format(formName, thisInput_dict))
      if "iSL" in thisInput_dict.keys() and thisInput_dict["iSL"] == "y" and "atk" in thisInput_dict.keys() and thisInput_dict["atk"]:
        self.secondRequest = True
    
    try:
      #logDebug("================================================")
      #logDebug("provided cookies:[{}]".format(self.request.cookies))
      #if isinstance(self.request.cookies, dict):
      #  for thisKey in self.request.cookies.keys():
      #    logDebug("cookies.{}:[{}]".format(thisKey, self.request.cookies[thisKey]))
      #else:
      #  logDebug("type:[{}]".format(type(self.request.cookies)))
      #logDebug("================================================")
      
      if self.request.cookies.get("gcCookies", "") != "":
        gcCipher = GcCipher()
        try:
          self.gcResponse_dict["cookies"] = json.loads(gcCipher.decrypt(self.request.cookies.get("gcCookies", "").encode()))
          for inputName in self.gcResponse_dict["form"].keys():
            if inputName in self.gcResponse_dict["cookies"].keys() and self.gcResponse_dict["form"][inputName] == "":
              self.gcResponse_dict["form"][inputName] = self.gcResponse_dict["cookies"][inputName]
          if self.gcResponse_dict["cookies"]["userName"] != "":
            self.gcResponse_dict["form"]["authenticityTokenId"] = self.gcAuthToken.createToken(self.gcResponse_dict["cookies"]["userName"])
        except Exception as e:
          logException(f"unable to load cookie->Error:[{e}]")
          self.gcResponse_dict["cookies"] = getDefaultCookies()
      else:
        self.gcResponse_dict["cookies"] = getDefaultCookies()
    except Exception as e:
      self.addErrMsgToGc(logException("unable to get gcCookies->Error:[{}]".format(e)))
      self.gcResponse_dict["cookies"] = getDefaultCookies()
    
  def getRuleName(self):
    
    if self.url_list[3] == "":
      ruleName = "_root"
    else:
      ruleName = self.request.base_url[self.request.base_url.find(self.url_list[2]) + (len(self.url_list[2])) +1:]
    logInfo("ruleName:[{}]".format(ruleName))
    
    return ruleName
  
  def getInputValues(self, form_dict):
    logDebug("form_dict:[{}]".format(form_dict))
    if isinstance(form_dict, dict) and "inputs" in form_dict.keys() and isinstance(form_dict["inputs"], dict):
      if self.request.method == "POST":
        for inputName in form_dict["inputs"].keys():
          if "type" in form_dict["inputs"][inputName].keys() and form_dict["inputs"][inputName]["type"] == "profile":
            logDebug("form:['profile'] is defined")
            for inputId in ["profileTemplates", "profileNames", "serviceNames", "accountIds", "regionCodes"]:
              
              if inputId in self.gcResponse_dict["form"].keys():
                logWarn("inputName:[{}] is alaredy updated")
                continue
              
              self.gcResponse_dict["form"][inputId] = self.request.form.getlist(inputId)
        
        for inputName in form_dict["inputs"].keys():
          if inputName in self.gcResponse_dict["form"].keys():
            logWarn("inputName:[{}] is alaredy updated")
            continue
            
          try:
            thiInputName = "{}{}".format(inputName.strip()[0].lower(), inputName.strip().replace(" ","")[1:])
            
            if self.gcResponse_dict["form"]["iSL"] == "y":
              if form_dict["inputs"][inputName]["type"] == "radio":
                self.gcResponse_dict["form"][thiInputName] = self.request.form.get(thiInputName, "")
              elif form_dict["inputs"][inputName]["type"] in ["checkbox", "select"]:
                self.gcResponse_dict["form"][thiInputName] = self.request.form.getlist(thiInputName)
              elif form_dict["inputs"][inputName]["type"] in ["file"]:
                logDebug("file:[{}] is found:[{}]".format(inputName, self.request.files.keys()))
              else:
                self.gcResponse_dict["form"][thiInputName] = self.request.form.get(thiInputName, "")
            else:
              if "value" in form_dict["inputs"][inputName].keys():
                self.gcResponse_dict["form"][thiInputName] = form_dict["inputs"][inputName]["value"]
              else:
                if form_dict["inputs"][inputName]["type"] == "checkbox":
                  self.gcResponse_dict["form"][thiInputName] = []
                else:
                  self.gcResponse_dict["form"][thiInputName] = ""
          except:
            logException("unable to set inputName:[{}]".format(inputName))
            continue
        
        for submitItem_dict in form_dict["submits"]:
          try:
            if "name" in submitItem_dict.keys():
              submitId = "{}{}".format(submitItem_dict["name"].strip()[0].lower(), submitItem_dict["name"].strip().replace(" ","")[1:])
              self.gcResponse_dict["form"][submitId] = self.request.form.get(submitId, "")
          
          except:
            logException("unable to get submitId with submitItem_dict:[{}]".format(submitItem_dict))
        
      else:
        for inputName in form_dict["inputs"].keys():
          if "type" in form_dict["inputs"][inputName].keys() and form_dict["inputs"][inputName]["type"] == "profile":
            logDebug("form:['profile'] is defined")
            for inputId in ["profileTemplates", "profileNames", "serviceNames", "accountIds", "regionCodes"]:
              
              if inputId in self.gcResponse_dict["form"].keys():
                logWarn("inputName:[{}] is alaredy updated")
                continue
              
              self.gcResponse_dict["form"][inputId] = self.request.args.getlist(inputId)
        
        for inputName in form_dict["inputs"].keys():
          if inputName in self.gcResponse_dict["form"].keys():
            logWarn("inputName:[{}] is alaredy updated")
            continue
            
          logDebug("inputName:[{}]:[{}]".format(inputName, form_dict["inputs"][inputName]))
          if form_dict["inputs"][inputName]["type"] == "object":
            logDebug("object found and objectCount:[{}]............".format(self.request.args.get("objectCount", "")))
            try:
              if self.request.args.get("objectCount", "") != "":
                objectCount = int(self.request.args.get("objectCount"))
              else:
                objectCount = form_dict["inputs"][inputName]["count"]
            except:
              logException("unable to get objectCount")
              objectCount = form_dict["inputs"][inputName]["count"]
            self.gcResponse_dict["form"]["objectCount"] = objectCount
            
            for count in range(objectCount):
              for subInputName in form_dict["inputs"][inputName]["objects"].keys():
                try:
                  thiInputName = "{}{}_{}".format(subInputName.strip()[0].lower(), subInputName.strip().replace(" ","")[1:], count)
                  
                  if self.gcResponse_dict["form"]["iSL"] == "y":
                    if form_dict["inputs"][inputName]["objects"][subInputName]["type"] == "radio":
                      self.gcResponse_dict["form"][thiInputName] = self.request.args.get(thiInputName, "")
                    elif form_dict["inputs"][inputName]["objects"][subInputName]["type"] in ["checkbox", "select"]:
                      self.gcResponse_dict["form"][thiInputName] = self.request.args.getlist(thiInputName)
                    elif form_dict["inputs"][inputName]["type"] in ["file"]:
                      logDebug("file:[{}] is found".format(inputName))
                    else:
                      self.gcResponse_dict["form"][thiInputName] = self.request.args.get(thiInputName, "")
                  else:
                    if "value" in form_dict["inputs"][inputName]["objects"][subInputName].keys():
                      self.gcResponse_dict["form"][thiInputName] = form_dict["inputs"][inputName]["objects"][subInputName]["value"]
                    else:
                      if form_dict["inputs"][inputName]["objects"][subInputName]["type"] == "checkbox":
                        self.gcResponse_dict["form"][thiInputName] = []
                      else:
                        self.gcResponse_dict["form"][thiInputName] = ""
                  
                  logDebug("thisInputName:[{}]->[{}]".format(thiInputName, self.gcResponse_dict["form"][thiInputName]))
                except:
                  logException("unable to set subInputName:[{}]".format(subInputName))
                  continue
          
          else:
            try:
              thiInputName = "{}{}".format(inputName.strip()[0].lower(), inputName.strip().replace(" ","")[1:])
              
              if self.gcResponse_dict["form"]["iSL"] == "y":
                if form_dict["inputs"][inputName]["type"] == "radio":
                  self.gcResponse_dict["form"][thiInputName] = self.request.args.get(thiInputName, "")
                elif form_dict["inputs"][inputName]["type"] in ["checkbox", "select"]:
                  self.gcResponse_dict["form"][thiInputName] = self.request.args.getlist(thiInputName)
                else:
                  self.gcResponse_dict["form"][thiInputName] = self.request.args.get(thiInputName, "")
              else:
                if "value" in form_dict["inputs"][inputName].keys():
                  self.gcResponse_dict["form"][thiInputName] = form_dict["inputs"][inputName]["value"]
                else:
                  if form_dict["inputs"][inputName]["type"] == "checkbox":
                    self.gcResponse_dict["form"][thiInputName] = []
                  else:
                    self.gcResponse_dict["form"][thiInputName] = ""
            except:
              logException("unable to set inputName:[{}]".format(inputName))
              continue
            
            for submitItem_dict in form_dict["submits"]:
              try:
                if "name" in submitItem_dict.keys():
                  
                  submitId = "{}{}".format(submitItem_dict["name"].strip()[0].lower(), submitItem_dict["name"].strip().replace(" ","")[1:])
                  self.gcResponse_dict["form"][submitId] = self.request.args.get(submitId, "")
              
              except:
                logException("unable to get submitId with submitItem_dict:[{}]".format(submitItem_dict))
                
          logDebug("inputName:[{}]:[{}]".format(inputName, self.gcResponse_dict["form"][thiInputName]))
          
      for fileInputId in self.request.files.keys():
        if fileInputId in self.gcResponse_dict["form"].keys():
          logWarn("fileInputId:[{}] is alaredy updated")
          continue

        logDebug("--->fileInputId:[{}]".format(fileInputId))
        self.gcResponse_dict["form"][fileInputId] = self.request.files[fileInputId].read()
        logDebug("--->fileInputId:[{}]({},len:{:,})".format(fileInputId, type(self.gcResponse_dict["form"][fileInputId]).__name__, len(self.gcResponse_dict["form"][fileInputId])))

    self.updateStartDate()
    self.updateEndDate()
    
    return self.gcResponse_dict["form"]
  
  def getInputName(self, inputName):
    try:
      thiInputName = inputName.replace(" ","")
      if len(thiInputName) > 0:
        thiInputName[0] = thiInputName[0].lower()
        
        return thiInputName
      else:
        raise ValueError("inputName:[{}](len:{}) should be larger than 0".format(inputName, len(inputName)))
    except:
      logExceptionWithValueError("unable to set inputName:[{}]".format(inputName))
      
  def addErrMsgToGc(self, errMsg):
    self.gcResponse_dict["errMsg"].append(errMsg)
  
  def wasInvalidKeyErrorMessage(self):
    for errMsg in self.gcResponse_dict["errMsg"]:
      if "invalid key" in errMsg:
        return True
      
    return False
  
  def isValidAthenticityToken(self, userName):
    logDebug("self.isValidAthenticityTokenStatus:[{}]".format(self.isValidAthenticityTokenStatus))
    if self.isValidAthenticityTokenStatus == None:
      try:
        if self.gcResponse_dict["form"]["iSL"] != "":
          if self.gcAuthToken.isValidToken(self.gcResponse_dict["form"]["atk"], userName):
            self.isValidAthenticityTokenStatus = True
            return self.isValidAthenticityTokenStatus
          else:
            self.addErrMsgToGc("unauthorized access with an invalid key")
            self.isValidAthenticityTokenStatus = False
            return self.isValidAthenticityTokenStatus
        else:
          #self.addErrMsgToGc("this is the first landing at the page. Or, 'iSL' isn't set!")
          self.isValidAthenticityTokenStatus = False
          return self.isValidAthenticityTokenStatus
          
      except Exception as e:
        self.addErrMsgToGc(logException("unexpected error:[{}]".format(e)))
        self.isValidAthenticityTokenStatus = False
        return self.isValidAthenticityTokenStatus
    
    return self.isValidAthenticityTokenStatus
        
  def get(self, userAuth = True):
    logDebug("gcCookies_dict:[{}]".format(self.gcResponse_dict["cookies"]))
    if len(self.request.cookies.get("gcCookies", "")) == 0 and self.ruleName not in ["_root", "_smtp", "_signin"]:
      logDebug("gcCookies_dict:[{}]".format(self.gcResponse_dict["cookies"]))
      response = redirect("./", code=307)
      return response
    
    if userAuth != True or (isinstance(self.gcResponse_dict["cookies"], dict) and "verified" in self.gcResponse_dict["cookies"].keys() and self.gcResponse_dict["cookies"]["verified"] == True):
      logDebug("{}:self.gcResponse_dict['cookies']:[{}]".format(type(self.gcResponse_dict["cookies"]), self.gcResponse_dict["cookies"]))
      
      logDebug("user:[{}] is verified".format(self.gcResponse_dict["cookies"]["userName"]))

      if self.isValidAthenticityToken(self.gcResponse_dict["cookies"]["userName"]):
        
        ## add additional authentication logic over ldap and etc. ##
        ##
        ## define isValidUser() for the user authentication logic over ldap and etc.
        ## if isValidUser(): 
        ##   self.gcResponse_dict["authorizedAccess"] = True
        ## else:
        ##   self.gcResponse_dict["authorizedAccess"] = False

        self.gcResponse_dict["authorizedAccess"] = True
        
      else:
        self.gcResponse_dict["authorizedAccess"] = False
      
      try:
        self.gcResponse_dict = self.action.run(request=self.request, form=self.form_dict, gc_dict = self.gcResponse_dict)
        
        if "form" in self.gcResponse_dict.keys() and "action" in self.gcResponse_dict["form"].keys() and self.gcResponse_dict["form"]["action"] != "":
          self.gcResponse_dict["active"] = "{}:{}".format(self.ruleName, self.gcResponse_dict["form"]["action"])
        else:
          self.gcResponse_dict["active"] = "{}".format(self.ruleName)
        
        if "__objectCount__" in self.gcResponse_dict["form"].keys():
          gcForm = GcForm()
          self.gcResponse_dict["form"]["__objects__"] = {}
          objectCount_dict = {}
          for objectName in self.gcResponse_dict["form"]["__objectCount__"].keys():
            
            try:
              if self.gcResponse_dict["form"]["__objectCount__"][objectName] > self.form_dict["default"]["inputs"][objectName]["count"]:
                objectId = "{}{}".format(objectName.strip()[0].lower(),objectName.strip().replace(" ","")[1:])
                logDebug("objectId:[{}]".format(objectId))
                objectCount_dict[objectId] = self.gcResponse_dict["form"]["__objectCount__"][objectName]
                self.gcResponse_dict["form"]["__objects__"][objectId] = gcForm.generateObjectFormTags(objectName= objectName, 
                                                                                                     objectForm_dict= self.form_dict["default"]["inputs"][objectName]["objects"], 
                                                                                                     objectCount= self.gcResponse_dict["form"]["__objectCount__"][objectName], 
                                                                                                     start= self.form_dict["default"]["inputs"][objectName]["count"],
                                                                                                     formValue_dict = self.gcResponse_dict["form"]) 
            except:
              logException("unable to generate object form")
              continue
          
          for objectId in objectCount_dict.keys():
            self.gcResponse_dict["form"]["__objectCount__"][objectId] = objectCount_dict[objectId]
        
        if "charts" in self.gcResponse_dict.keys():
          self.gcResponse_dict["outputs"]["charts"] = {}
          gcChart = GcChart()
          for chartName in self.gcResponse_dict["charts"].keys():
            chartId = gcChart.getChartId(chartName)
            self.gcResponse_dict["outputs"]["charts"][chartId] = gcChart.getChartTags(chartName, chart_dict=self.gcResponse_dict["charts"][chartName])
            #logDebug("#chartId:[{}]\n{}".format(chartId, self.gcResponse_dict["outputs"]["charts"][chartId]))
          
          self.gcResponse_dict["jsCharts"] = "{}".format(gcChart.getJsChartCode())
          #logDebug("#jsCharts:{}".format(self.gcResponse_dict["jsCharts"]))
        
        self.gcResponse_dict["renderingDate"] = getDateString()
        self.gcResponse_dict["renderingTime"] = time.time()
        self.gcResponse_dict["renderingRUntime"] = time.time() - self.__beginTime__
        
        if "download" in self.gcResponse_dict.keys():
          response = self.gcResponse_dict["download"]
          
        elif "redirect" in self.gcResponse_dict.keys():
          response = redirect(self.gcResponse_dict["redirect"], code=307)
          
          #flask.redirect(flask.url_for('operation'), code=307)
          
        else:
          if self.ruleName != "_root":
            if len(self.ruleName.split("/")) > 1:
              logDebug("==>template:[{}]".format("{}.html".format(self.ruleName.replace("/", "."))))
              response = make_response(render_template("{}.html".format(self.ruleName.replace("/", ".")), gc = self.gcResponse_dict))
            else:
              #logDebug("==>template:[{}]".format("{}.html".format(self.ruleName)))
              response = make_response(render_template("{}.html".format(self.ruleName), gc = self.gcResponse_dict))
          else:
            logDebug("==>template:[{}]".format("index.html".format(self.ruleName)))
            response = make_response(render_template("index.html".format(self.ruleName), gc = self.gcResponse_dict))
            
        if isinstance(self.gcResponse_dict["cookies"], dict):
          gcCipher = GcCipher()
          encryptedCookies = gcCipher.encrypt(json.dumps(self.gcResponse_dict["cookies"])).decode()
          try:
            response.set_cookie("gcCookies", encryptedCookies, max_age=3600*24*30)
            
            #try:
            #  logDebug("extented cookie TTL:[{}+{}]:[{}]".format(datetime.now(), timedelta(days=30), datetime.now() + timedelta(days=30)))
            #except:
            #  logException("unexpected error")
              
          except:
            try:
              logException(f"failed to extend cookie TTL:[{datetime.now()}+{timedelta(days=30)}] for encryptedCookies:[{encryptedCookies}]")
            except:
              logException("unexpected error")
        
        else:
          try:
            if isinstance(self.gcResponse_dict["cookies"], dict):
              #response.delete_cookie("gcCookies")
              for cookieItemName in self.gcResponse_dict["cookies"].keys():
                self.gcResponse_dict["cookies"][cookieItemName] = ""
                if cookieItemName in self.gcResponse_dict["form"].keys():
                  self.gcResponse_dict["form"][cookieItemName] = ""
              response.set_cookie("gcCookies", gcCipher.encrypt(json.dumps(self.gcResponse_dict["cookies"])).decode(), expires= datetime.now())
          except:
            logException("unable to delete cookies")
      except:
        logException("'{}' has an error".format(self.ruleName))
        response = render_template("_e500thml", gc_dict = self.gcResponse_dict), 500
    
    else:
      try:
        self.addErrMsgToGc("UnauthorizedAccess")
        response = make_response(render_template("index.html", gc = self.gcResponse_dict)), 401
        
        try:
          if isinstance(self.gcResponse_dict["cookies"], dict):
            #response.delete_cookie("gcCookies")
            for cookieItemName in self.gcResponse_dict["cookies"].keys():
              self.gcResponse_dict["cookies"][cookieItemName] = ""
              if cookieItemName in self.gcResponse_dict["form"].keys():
                self.gcResponse_dict["form"][cookieItemName] = ""
            response.set_cookie("gcCookies", gcCipher.encrypt(json.dumps(self.gcResponse_dict["cookies"])).decode(), expires= datetime.now())
        except:
          logException("unable to delete cookies")
      except:
        logException("'index.html' isn't responded.")
        response = render_template("_e500thml", gc_dict = self.gcResponse_dict), 500
    
    return response

  def updateStartDate(self):
    if "startTime" in self.gcResponse_dict["form"].keys():
      startTimeString = "startTime"
    elif "startDate" in self.gcResponse_dict["form"].keys():
      startTimeString = "startDate"
    else:
      startTimeString = None

    if startTimeString is not None:
      try:
        if self.gcResponse_dict["form"][startTimeString] == "":
          self.gcResponse_dict["form"][startTimeString] = "7 days ago"
        self.gcResponse_dict["form"][startTimeString] = getDateString(self.gcResponse_dict["form"][startTimeString]).split("T")[0]
      except:
        try:
          self.gcResponse_dict["form"][startTimeString] = datetime.strptime(self.gcResponse_dict["form"][startTimeString], "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
          try:
            self.gcResponse_dict["form"][startTimeString] = datetime.strptime(self.gcResponse_dict["form"][startTimeString], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
          except:
            try:
              self.gcResponse_dict["form"][startTimeString] = datetime.strptime(self.gcResponse_dict["form"][startTimeString], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            except:
              try:
                self.gcResponse_dict["form"][startTimeString] = datetime.strptime(self.gcResponse_dict["form"][startTimeString], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
              except:
                try:
                  self.gcResponse_dict["form"][startTimeString] = datetime.strptime(self.gcResponse_dict["form"][startTimeString], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
                except:
                  logError("unable to set 'startDate' with form:[{}]".format(self.gcResponse_dict["form"]))
                  self.gcResponse_dict["form"][startTimeString] = "7 days ago"
                  self.gcResponse_dict["form"][startTimeString] = getDateString(self.gcResponse_dict["form"][startTimeString]).split("T")[0]
    
    return self.gcResponse_dict["form"]
    
  def updateEndDate(self):
    if "endTime" in self.gcResponse_dict["form"].keys():
      endTimeString = "endTime"
    elif "endDate" in self.gcResponse_dict["form"].keys():
      endTimeString = "endDate"
    else:
      endTimeString = None

    if endTimeString is not None:
      try:
        if self.gcResponse_dict["form"][endTimeString] == "":
          self.gcResponse_dict["form"][endTimeString] = "now"
        self.gcResponse_dict["form"][endTimeString] = getDateString(self.gcResponse_dict["form"][endTimeString]).split("T")[0]
      except:
        try:
          self.gcResponse_dict["form"][endTimeString] = datetime.strptime(self.gcResponse_dict["form"][endTimeString], "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
          try:
            self.gcResponse_dict["form"][endTimeString] = datetime.strptime(self.gcResponse_dict["form"][endTimeString], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
          except:
            try:
              self.gcResponse_dict["form"][endTimeString] = datetime.strptime(self.gcResponse_dict["form"][endTimeString], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            except:
              try:
                self.gcResponse_dict["form"][endTimeString] = datetime.strptime(self.gcResponse_dict["form"][endTimeString], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
              except:
                try:
                  self.gcResponse_dict["form"][endTimeString] = datetime.strptime(self.gcResponse_dict["form"][endTimeString], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
                except:
                  logError("unable to set 'endDate' with form:[{}]".format(self.gcResponse_dict["form"]))
                  self.gcResponse_dict["form"][endTimeString] = "now"
                  self.gcResponse_dict["form"][endTimeString] = getDateString(self.gcResponse_dict["form"][endTimeString]).split("T")[0]
                
    return self.gcResponse_dict["form"]
  