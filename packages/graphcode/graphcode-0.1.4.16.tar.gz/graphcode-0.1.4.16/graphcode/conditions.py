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

from graphcode.io import *
from graphcode.path import createDir
from graphcode.unittest import *

import copy

class GcConditions():
  def __init__(self, conditions, results):
    #logDebug("#initalized....")
    
    self.type = type
    self.conditions = conditions
    #self.results = copy.deepcopy(results)
    self.results = results

  def get(self):
    if self.conditions != None and self.conditions.strip() != "" and isinstance(self.results, list) and len(self.results) > 0:
      conditions = self.conditions.strip()
      
      thisResult_list = []
      
      #logDebug("conditions:[{}]".format(conditions))
      offset = 0
      if conditions.find("&&", 0) > 0 and conditions.find("||", 0):
        pass#logDebug("multiple AND/OR operator with '&&' and '||' at conditions:[{}]".format(conditions))
      elif conditions.find("&&", 0) > 0:
        pass#logDebug("AND operator with '&&' and '||' at conditions:[{}]".format(conditions))
      elif conditions.find("||", 0) > 0:
        pass#logDebug("OR operator with '&&' and '||' at conditions:[{}]".format(conditions))
      else:
        pass#logDebug("No AND/OR operator:['&&' and '||'] at conditions:[{}]".format(conditions))
        
        if " in " in conditions:
          conditionItem_list = conditions.split(" in ")
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[1].strip()
            conditionItemValue_list = []
            for conditionItemValue in conditionItem_list[0].strip().split(","):
              
              if conditionItemValue == '""' or conditionItemValue == "''":
                conditionItemValue = ""
              elif conditionItemValue == "None":
                conditionItemValue = None
              elif conditionItemValue == "True":
                conditionItemValue = True
              elif conditionItemValue == "False":
                conditionItemValue = False
              #logDebug("#conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              if conditionItemValue in conditionItemValue_list:
                logWarn("conditionItemValue:[{}] is duplicated at conditionItemValue_list:[{}]".format(conditionItemValue_list))
              else:
                conditionItemValue_list.append(conditionItemValue)
                
            #logDebug("#conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
            
            for thisResultItmes in self.results:
              #logDebug("thisResultItems:[{}]".format(thisResultItmes))
              if isinstance(thisResultItmes, dict):
                try:
                  if conditionItemName in thisResultItmes.keys():
                    for conditionItemValue in conditionItemValue_list:
                      if  conditionItemValue in  thisResultItmes[conditionItemName]:
                        thisResult_list.append(thisResultItmes)
                except:
                  logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
          else:
            logWarn("insufficient arguments for '==' with [{}]".format(conditionItemName))
        
        elif "not start" in conditions:
          if " not startsWith " in conditions:
            conditionItem_list = conditions.split(" not startsWith ")
          elif " not startswith " in conditions:
            conditionItem_list = conditions.split(" not startswith ")
          elif " not startWith " in conditions:
            conditionItem_list = conditions.split(" not startWith ")
          elif " not startswith " in conditions:
            conditionItem_list = conditions.split(" not startwith ")
          else:
            logInfo("no valid conditions:[{}]".format(self.conditions))
            
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue_list = []
            for conditionItemValue in conditionItem_list[1].strip().split(","):
              
              if conditionItemValue == '""' or conditionItemValue == "''":
                continue
              logDebug("conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              if conditionItemValue in conditionItemValue_list:
                logWarn("conditionItemValue:[{}] is duplicated at conditionItemValue_list:[{}]".format(conditionItemValue_list))
              else:
                conditionItemValue_list.append(conditionItemValue)
                
            logDebug("conditionItemName:[{}] != conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
            
            for thisResultItmes in self.results:
              #logDebug("thisResultItems:[{}]".format(thisResultItmes))
              if isinstance(thisResultItmes, dict):
                isNotStartsWith = False
                for conditionItemValue in conditionItemValue_list:
                  try:
                    if conditionItemName in thisResultItmes.keys() and "{}".format(thisResultItmes[conditionItemName]).startswith(conditionItemValue):
                      isNotStartsWith = True
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
                
                if isNotStartsWith == False:
                  thisResult_list.append(thisResultItmes)
          else:
            logWarn("insufficient arguments for '==' with [{}]".format(conditionItemName))
        
        elif "start" in conditions:
          if " startsWith " in conditions:
            conditionItem_list = conditions.split(" startsWith ")
          elif " startswith " in conditions:
            conditionItem_list = conditions.split(" startswith ")
          elif " startWith " in conditions:
            conditionItem_list = conditions.split(" startWith ")
          elif " startswith " in conditions:
            conditionItem_list = conditions.split(" startwith ")
          else:
            logInfo("no valid conditions:[{}]".format(self.conditions))
            
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue_list = []
            for conditionItemValue in conditionItem_list[1].strip().split(","):
              
              if conditionItemValue == '""' or conditionItemValue == "''":
                continue
              logDebug("conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              if conditionItemValue in conditionItemValue_list:
                logWarn("conditionItemValue:[{}] is duplicated at conditionItemValue_list:[{}]".format(conditionItemValue_list))
              else:
                conditionItemValue_list.append(conditionItemValue)
                
            logDebug("conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
            
            for thisResultItmes in self.results:
              #logDebug("thisResultItems:[{}]".format(thisResultItmes))
              if isinstance(thisResultItmes, dict):
                for conditionItemValue in conditionItemValue_list:
                  try:
                    if conditionItemName in thisResultItmes.keys() and "{}".format(thisResultItmes[conditionItemName]).startswith(conditionItemValue):
                      thisResult_list.append(thisResultItmes)
                      break
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
          else:
            logWarn("insufficient arguments for '==' with [{}]".format(conditionItemName))
        
        elif "==" in conditions:
          conditionItem_list = conditions.split("==")
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            if conditionItemValue == '""' or conditionItemValue == "''":
              conditionItemValue = ""
            elif conditionItemValue == "None":
              conditionItemValue = None
            elif conditionItemValue == "True":
              conditionItemValue = True
            elif conditionItemValue == "False":
              conditionItemValue = False
            #logDebug("#conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
            
            for thisResultItmes in self.results:
              #logDebug("thisResultItems:[{}]".format(thisResultItmes))
              if isinstance(thisResultItmes, dict):
                try:
                  if conditionItemValue in [None, False, True] and conditionItemValue == thisResultItmes[conditionItemName]:
                    thisResult_list.append(thisResultItmes)
                    
                  elif conditionItemName in thisResultItmes.keys() and conditionItemValue == "{}".format(thisResultItmes[conditionItemName]):
                    thisResult_list.append(thisResultItmes)
                except:
                  logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes))
          
          else:
            logWarn("insufficient arguments for '==' with [{}]".format(conditionItemName))
        
        elif "!=" in conditions or "<>" in conditions:
          if "!=" in conditions:
            conditionItem_list = conditions.split("!=")
          else:
            conditionItem_list = conditions.split("<>")
          
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            if conditionItemValue == '""' or conditionItemValue == "''":
              conditionItemValue = ""
            elif conditionItemValue == "None":
              conditionItemValue = None
            elif conditionItemValue == "True":
              conditionItemValue = True
            elif conditionItemValue == "False":
              conditionItemValue = False
            logDebug("conditionItemName:[{}] == conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
            
            for thisResultItmes in self.results:
              if isinstance(thisResultItmes, dict) and conditionItemName in thisResultItmes.keys():
                try:
                  if conditionItemValue in [None, False, True] and conditionItemValue == thisResultItmes[conditionItemName]:
                    thisResult_list.append(thisResultItmes)
                    
                  elif conditionItemValue != "{}".format(thisResultItmes[conditionItemName]):
                    thisResult_list.append(thisResultItmes)
                except:
                  logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
          else:
            logWarn("insufficient arguments for '==' with [{}]".format(conditionItemName))
          
        elif ">=" in conditions:
          conditionItem_list = conditions.split(">=")
          
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            try:
              conditionItemValue = float(conditionItemValue)            
              
              logDebug("conditionItemName:[{}] >= conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              for thisResultItmes in self.results:
                #logDebug("thisResultItems:[{}]".format(thisResultItmes))
                if isinstance(thisResultItmes, dict) and conditionItemName in thisResultItmes.keys():
                  try:
                    if isinstance(thisResultItmes[conditionItemName], str):
                      if thisResultItmes[conditionItemName] != "":
                        try:
                          thisResultItmes[conditionItemName] = float(thisResultItmes[conditionItemName])
                        except:
                          logException("unable to parst resultValue:[{}] to float".format(thisResultItmes[conditionItemName]))
                          continue
                      else:
                        thisResultItmes[conditionItemName] = 0
                    #endif isinstance(thisResultItmes[conditionItemName], str):
                    
                    if thisResultItmes[conditionItemName] >= conditionItemValue:
                      thisResult_list.append(thisResultItmes)
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
                
                else:
                  logWarn("insufficient arguments for '{}' >= {} with thisResultItmes.keys():[{}]".format(conditionItemName, conditionItemValue, thisResultItmes.keys()))
                #endif isinstance(thisResultItmes, dict):
              #endfor thisResultItmes in self.results:
            except:
              logException("unable to parse conditionItemValue:[{}] to numeric one".format(conditionItemValue))
            
            
        elif ">" in conditions:
          conditionItem_list = conditions.split(">")
          
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            try:
              conditionItemValue = float(conditionItemValue)            
              
              logDebug("conditionItemName:[{}] > conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              for thisResultItmes in self.results:
                #logDebug("thisResultItems:[{}]".format(thisResultItmes))
                if isinstance(thisResultItmes, dict) and conditionItemName in thisResultItmes.keys():
                  try:
                    if isinstance(thisResultItmes[conditionItemName], str):
                      if thisResultItmes[conditionItemName] != "":
                        try:
                          thisResultItmes[conditionItemName] = float(thisResultItmes[conditionItemName])
                        except:
                          logException("unable to parst resultValue:[{}] to float".format(thisResultItmes[conditionItemName]))
                          continue
                      else:
                        thisResultItmes[conditionItemName] = 0
                    #endif isinstance(thisResultItmes[conditionItemName], str):
                    
                    if thisResultItmes[conditionItemName] > conditionItemValue:
                      thisResult_list.append(thisResultItmes)
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
                
                else:
                  logWarn("'{}' is not found for '> {}' with thisResultItmes.keys():[{}]".format(conditionItemName, conditionItemValue, thisResultItmes.keys()))
                #endif isinstance(thisResultItmes, dict):
              #endfor thisResultItmes in self.results:
            except:
              logException("unable to parse conditionItemValue:[{}] to numeric one".format(conditionItemValue))
            
        elif "<=" in conditions:
          conditionItem_list = conditions.split("<=")
          
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            try:
              conditionItemValue = float(conditionItemValue)            
              
              logDebug("conditionItemName:[{}] <= conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              for thisResultItmes in self.results:
                #logDebug("thisResultItems:[{}]".format(thisResultItmes))
                if isinstance(thisResultItmes, dict) and conditionItemName in thisResultItmes.keys():
                  try:
                    if isinstance(thisResultItmes[conditionItemName], str):
                      if thisResultItmes[conditionItemName] != "":
                        try:
                          thisResultItmes[conditionItemName] = float(thisResultItmes[conditionItemName])
                        except:
                          logException("unable to parst resultValue:[{}] to float".format(thisResultItmes[conditionItemName]))
                          continue
                      else:
                        thisResultItmes[conditionItemName] = 0
                    #endif isinstance(thisResultItmes[conditionItemName], str):
                    
                    if thisResultItmes[conditionItemName] <= conditionItemValue:
                      thisResult_list.append(thisResultItmes)
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
                
                else:
                  logWarn("insufficient arguments for '{}' <= {} with thisResultItmes.keys():[{}]".format(conditionItemName, conditionItemValue, thisResultItmes.keys()))
                #endif isinstance(thisResultItmes, dict):
              #endfor thisResultItmes in self.results:
            except:
              logException("unable to parse conditionItemValue:[{}] to numeric one".format(conditionItemValue))
            
            
        elif "<" in conditions:
          conditionItem_list = conditions.split("<")
          
          if len(conditionItem_list) >= 2:
            conditionItemName = conditionItem_list[0].strip()
            conditionItemValue = conditionItem_list[1].strip()
            
            try:
              conditionItemValue = float(conditionItemValue)            
              
              logDebug("conditionItemName:[{}] < conditionItemValue:[{}]".format(conditionItemName, conditionItemValue))
              
              for thisResultItmes in self.results:
                #logDebug("thisResultItems:[{}]".format(thisResultItmes))
                if isinstance(thisResultItmes, dict) and conditionItemName in thisResultItmes.keys():
                  try:
                    if isinstance(thisResultItmes[conditionItemName], str):
                      if thisResultItmes[conditionItemName] != "":
                        try:
                          thisResultItmes[conditionItemName] = float(thisResultItmes[conditionItemName])
                        except:
                          logException("unable to parst resultValue:[{}] to float".format(thisResultItmes[conditionItemName]))
                          continue
                      else:
                        thisResultItmes[conditionItemName] = 0
                    #endif isinstance(thisResultItmes[conditionItemName], str):
                    
                    if thisResultItmes[conditionItemName] < conditionItemValue:
                      thisResult_list.append(thisResultItmes)
                  except:
                    logException("unable to determine the condition by conditionItemName:[{}],conditionItemValue:[{}],resultValue:[{}]".format(conditionItemName,conditionItemValue,thisResultItmes[conditionItemName]))
                
                else:
                  logWarn("insufficient arguments for '{}' < {} with thisResultItmes.keys():[{}]".format(conditionItemName, conditionItemValue, thisResultItmes.keys()))
                #endif isinstance(thisResultItmes, dict):
              #endfor thisResultItmes in self.results:
            except:
              logException("unable to parse conditionItemValue:[{}] to numeric one".format(conditionItemValue))
            
        else:
          logDebug("no valid conditions:[{}]".format(self.conditions))
        
        #if len(thisResult_list) > 0:
        #  logInfo("conditions:[{}]->results(len:{}):[{}]".format(self.conditions, len(thisResult_list), thisResult_list[-1]))
        #else:
        #  logInfo("conditions:[{}]->results(len:{}):[{}]".format(self.conditions, len(thisResult_list), thisResult_list))
          
        return copy.deepcopy(thisResult_list)
          
    else:
      logDebug("no conditions:[{}]".format(self.conditions))
      
      return self.results
      