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

from graphcode.path import listDir
from pado.conf import GcConf

from os import getcwd
from os.path import basename, dirname, join, abspath

import platform

class GcRules:
  def __init__(self, gcConf):
    if isinstance(gcConf, GcConf):
      self.homeDir = gcConf.homeDir
      logDebug("homeDir:[{}]".format(self.homeDir))
      
      self.confPath = gcConf.confPath
      logDebug("confPath:[{}]".format(self.confPath))
      
      self.serviceConf_dict = gcConf.serviceConf_dict
      logDebug("serviceConf_dict:[{}]".format(self.serviceConf_dict))
      
      self.frameConf_dict = gcConf.frameConf_dict
      logDebug("frameConf_dict:[{}]".format(self.frameConf_dict))
      
      self.cssConf_dict = gcConf.cssConf_dict
      logDebug("cssConf_dict:[{}]".format(self.cssConf_dict))
      
      self.jsConf_dict = gcConf.jsConf_dict
      logDebug("jsConf_dict:[{}]".format(self.jsConf_dict))
      
      self.modalConf_dict = gcConf.modalConf_dict
      logDebug("modalConf_dict:[{}]".format(self.modalConf_dict))
      
      self.nav_conf = gcConf.nav_conf
      logDebug("nav_conf:[{}]".format(self.nav_conf))
      
      self.static_dir = gcConf.static_dir
      logInfo("static_dir:[{}]".format(self.static_dir))
      
      self.template_dir = gcConf.template_dir
      logInfo("template_dir:[{}]".format(self.template_dir))
      
      self.rulesPath = gcConf.rulesPath
      logDebug("rulesPath:[{}]".format(self.rulesPath))
    
      self.rules_dict = self.loadRules(self.rulesPath)
      logDebug("rules:[{}]".format(self.rules_dict))
    
    else:
      raise ValueError("gcTemplates:[{}] is not the type:GcConf".format(gcConf))
    
    
  def loadRules(self, rulesPath):
    rules_dict = {}
    for ruleName in listDir(rulesPath, type="dir"):
      if ruleName.startswith("__"):
        continue
      
      logDebug("thisRule:[{}]".format(ruleName))
      rules_dict[ruleName] = self.importRules(ruleName)
      rules_dict[ruleName]["view"].view.__name__ = "{}_{}".format(ruleName, rules_dict[ruleName]["view"].view.__name__)
      
      
      for subRuleName in listDir(join(rulesPath, ruleName), type = "dir"):
        if subRuleName.startswith("__"):
          continue
        
        logDebug("thisRule:[{}]->subRule:[{}]".format(ruleName, subRuleName))
        try:
          rules_dict["{}/{}".format(ruleName, subRuleName)] = self.importRules("{}.{}".format(ruleName, subRuleName))
          rules_dict["{}/{}".format(ruleName, subRuleName)]["view"].view.__name__ = "{}_{}".format("{}.{}".format(ruleName, subRuleName), rules_dict[ruleName]["view"].view.__name__)
        except:
          logException("unable to import rule:[{}]".format("{}/{}".format(ruleName, subRuleName)))
    
    return rules_dict
  
  def importRules(self, ruleName):
    logDebug("cwd:[{}/]".format(getcwd()))
    logDebug("self.rulesPath:[{}]".format(abspath(self.rulesPath)))
    if platform.system().startswith("Win"):
      ruleRoot = abspath(self.rulesPath).replace(f"{getcwd()}\\","").replace("/",".")
    else:
      ruleRoot = abspath(self.rulesPath).replace(f"{getcwd()}/","").replace("/",".")
    logDebug("ruleRoot:[{}]->ruleName:[{}]".format(ruleRoot, ruleName))
    
    form = __import__("{}.{}.form".format(ruleRoot, ruleName), fromlist=[''])
    view = __import__("{}.{}.view".format(ruleRoot, ruleName), fromlist=[''])
    action = __import__("{}.{}.action".format(ruleRoot, ruleName), fromlist=[''])
    
    logInfo("{}:action:[{}]".format(ruleName, view.view.__name__))
    
    if "methods" in form.form_dict.keys() and isinstance(form.form_dict["methods"], list):
      methods = form.form_dict["methods"]
    else:
      methods = ["POST", "GET"]
    
    if ruleName == "_root":
      return {"name":ruleName, "endpoint":"/", "methods": methods, "form":form, "view":view, "action":action}
    else:
      if len(ruleName.split(".")) > 1:
        return {"name":ruleName, "endpoint":"/{}".format(ruleName.replace(".","/")), "methods": methods, "form":form, "view":view, "action":action}
      else:
        return {"name":ruleName, "endpoint":"/{}".format(ruleName), "methods": methods, "form":form, "view":view, "action":action}
    
def get(action, gc_dict, wbResult_dict):
  try:
    targetPackage = __import__("rules.{}.{}".format(gc_dict["ruleName"], action), fromlist=[''])
    
    thisRequest_dict = {}
    thisWbResult_dict = getattr(targetPackage, "do")(action=action, request_dict=thisRequest_dict, gc_dict=gc_dict, wbResult_dict=wbResult_dict)
    
    for wbResultIndexKey in thisWbResult_dict.keys():
      wbResult_dict[wbResultIndexKey] = thisWbResult_dict[wbResultIndexKey]
      logDebug("#wbResultIndex:[{}](len:{:,})".format(wbResultIndexKey, len(wbResult_dict[wbResultIndexKey])))
    
    logDebug("wbResult_dict.keys(len:{:,}):[{}]".format(len(wbResult_dict.keys()),wbResult_dict.keys()))
    
    gc_dict["actionStatus"] = True
    
    if gc_dict["ruleName"] in ["overview"] and action != "":
      gc_dict["redirect"] = "/{}".format(gc_dict["ruleName"])
      
  except:
    errMsg = logException("unable to discovery resources")
    gc_dict["errMsg"].append(errMsg)
  
  return wbResult_dict