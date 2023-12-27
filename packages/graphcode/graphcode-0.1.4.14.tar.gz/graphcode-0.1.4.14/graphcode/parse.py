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

from graphcode.conditions import GcConditions
from graphcode.lib import printValue, getDateString
from graphcode.lib import getIPv4AddressDetails

import json
import time


nextTokenKeyword_list = ["nextToken", "NextToken", "marker", "Marker", "nextMarker", "NextMarker", "paginationToken", "PaginationToken", "lastEvaluatedTableName", "LastEvaluatedTableName", "position", "lastEvaluatedStreamArn"]

class GcParse():
  def __init__(self, result, inputs, payload= None):
    
    self.result = result
    #logInfo("type:{}:self.result:[{}]".format(type(self.result), self.result))
    
    self.input_dict = inputs
    #logInfo("type:{}:self.inputs:[{}]".format(type(self.input_dict), self.input_dict))
    
    self.payload_dict = payload
    #logInfo("type:{}:self.payload_dict:[{}]".format(type(self.payload_dict), self.payload_dict))
    
    if isinstance(self.payload_dict, dict) and "args" in self.payload_dict.keys() and isinstance(self.payload_dict["args"], dict):
      #self.args_dict = self.payload_dict["args"]
      
      self.args_dict = {}
      if isinstance(self.args_dict, dict):
        for argKeyName in set(self.payload_dict["args"].keys()):
          if argKeyName in nextTokenKeyword_list:
            continue
          
          if isinstance(self.payload_dict["args"][argKeyName], list) and len(self.payload_dict["args"][argKeyName]) == 1:
            self.args_dict["{}_".format(argKeyName)] = self.payload_dict["args"][argKeyName][-1]
          else:
            self.args_dict["{}_".format(argKeyName)] = self.payload_dict["args"][argKeyName]
    else:
      self.args_dict = {}
    
    try:
      self.platform = self.input_dict["platform"]
    except:
      self.platform = "boto3"
    
    try:
      apiName_list = self.input_dict["apiName"].split(".")
      if len(apiName_list) < 2:
        if "serviceName" in self.input_dict.keys():
          self.serviceName = self.input_dict["serviceName"]
        else:
          self.serviceName = ""
      else:
        self.serviceName = apiName_list[0]
      self.apiName = apiName_list[-1]
    except:
      try:
        logException("unexpected apiName:[{}]".format(self.input_dict["apiName"]))
        self.serviceName = ""
        self.apiName = self.input_dict["apiName"]
      except:
        logExceptionWithValueError("unexpected input_dict.keys:[{}]".format(self.input_dict.keys()))
        
      
    if "accountId" in self.input_dict.keys():
      self.accountId = self.input_dict["accountId"]
    else:
      self.accountId = None
    
    if "regionCode" in self.input_dict.keys():
      self.regionCode = self.input_dict["regionCode"]
    else:
      self.regionCode = None
      
    self.primaryKey_list = self.updatePrimaryKeys()
    #logDebug("#primaryKey_list:[{}]".format(self.primaryKey_list))
    
    self.additionalValue_dict = self.updateAdditionalValues()
    
    
    self.resourceName_list = []
    if "resourceName" in self.input_dict.keys():
      self.resourceName_list = []
      for key in self.input_dict["resourceName"].strip().split(","):
        if len(key.strip()) > 0:
          self.resourceName_list.append(key.strip())
          
    elif "inputs" in self.input_dict.keys():
      if isinstance(self.input_dict["inputs"],dict) and "resourceName" in self.input_dict["inputs"].keys():
        
        for key in self.input_dict["inputs"]["resourceName"].strip().split(","):
          if len(key.strip()) > 0:
            self.resourceName_list.append(key.strip())
            
      elif isinstance(self.input_dict["inputs"],str):
        for inputItems in self.input_dict["inputs"].strip().split(";"):
          
          inputItem_list = inputItems.split("=")
          if "resourceName" == inputItem_list[0]: 
            try:
              for key in inputItem_list[0].strip().split(","):
                if len(key.strip()) > 0:
                  self.resourceName_list.append(key.strip())
            except:
              logError("unexpected inputs:[{}]".format(self.input_dict["inputs"]))
        
    else:
      self.resourceName_list = []
     
    
    
  def updateAdditionalValues(self):
    
    moduApi_list = [
      "profile",
      "analyze",
      "getRegions", 
      "filterResults", 
      "describeResource", 
      "describeServiceLimits", 
      "discoverRegions",
      "discoverResources"
      ]
    if self.apiName.split(".")[-1] in moduApi_list:
      additionalValue_dict = {}
      
    elif self.serviceName in moduApi_list:
      additionalValue_dict = {}
      
    elif self.accountId != "000000000000":
      additionalValue_dict = {"serviceName_":self.serviceName, "apiName_":self.apiName, "accountId_":self.accountId, "regionCode_":self.regionCode, "resourceName_":None}
    
    else:
      additionalValue_dict = {"serviceName_":self.serviceName, "apiName_":self.apiName}
    
    if "additionalKeys" in self.input_dict.keys():
      logDebug("additionalKeys:[{}]".format(self.input_dict["additionalKeys"]))
      for key in self.input_dict["additionalKeys"].strip().split(","):
        if key in self.input_dict.keys():
          additionalValue_dict[key] = self.input_dict[key]
      
    elif "inputs" in self.input_dict.keys() and self.serviceName not in ["avs"]:
      if isinstance(self.input_dict["inputs"], str):
        for inputItems_str in self.input_dict["inputs"].split(";"):
          inputItem_list = inputItems_str.strip().split("=")
          if len(inputItem_list) > 1 and inputItem_list[0] in ["additionalKeys"]:
            for key in self.input_dict["inputs"]["additionalKeys"].strip().split(","):
              if key in self.input_dict["inputs"].keys():
                additionalValue_dict[key] = self.input_dict["inputs"][key]
      elif isinstance(self.input_dict["inputs"], dict) and "additionalKeys" in self.input_dict["inputs"].keys():
        for key in self.input_dict["inputs"]["additionalKeys"].strip().split(","):
          if key in self.input_dict["inputs"].keys():
            additionalValue_dict[key] = self.input_dict["inputs"][key]
      else:
        pass
      #logDebug("#inputs:[{}]".format(self.input_dict["inputs"]))
    '''
    elif "inputs" in self.input_dict.keys() and "additionalKeys" in self.input_dict["inputs"].keys():
      logDebug("additionalKeys:[{}]".format(self.input_dict["inputs"]["additionalKeys"]))
      for key in self.input_dict["inputs"]["additionalKeys"].strip().split(","):
        if key in self.input_dict["inputs"].keys():
          additionalValue_dict[key] = self.input_dict["inputs"][key]
    '''
    #logDebug("#additionalValue_dict:[{}]".format(additionalValue_dict))

    return additionalValue_dict
  
  def getAdditionalValues(self):
    return self.additionalValue_dict
  
  def addAdditionalValues(self, resultItem_dict):
    if isinstance(resultItem_dict, dict):
      for key in self.additionalValue_dict.keys():
        resultItem_dict[key] = self.additionalValue_dict[key]
        
    return resultItem_dict
  
  def updatePrimaryKeys(self):
    if "primaryKeys" in self.input_dict.keys():
      #logDebug("#primaryKeys:[{}]".format(self.input_dict["primaryKeys"]))
      primaryKey_list = self.input_dict["primaryKeys"].strip().split(",")
    elif "inputs" in self.input_dict.keys():
      if isinstance(self.input_dict["inputs"], str):
        primaryKey_list = []
        for inputItems_str in self.input_dict["inputs"].split(";"):
          inputItem_list = inputItems_str.strip().split("=")
          if len(inputItem_list) > 1 and inputItem_list[0] in ["primaryKeys"]:
            #logDebug("#primaryKeys:[{}]".format(inputItem_list[1]))
            for primaryKey in inputItem_list[1].strip().split(","):
              if primaryKey != "" and primaryKey not in primaryKey_list:
                primaryKey_list.append(primaryKey)
      elif isinstance(self.input_dict["inputs"], dict) and "primaryKeys" in self.input_dict["inputs"].keys():
        primaryKey_list = self.input_dict["inputs"]["primaryKeys"].strip().split(",")
        #logDebug("#primaryKeys:[{}]".format(primaryKey_list))
      else:
        primaryKey_list = []
        #logDebug("#primaryKeys:[{}]".format(primaryKey_list))
      #logDebug("#inputs:[{}]".format(self.input_dict["inputs"]))
      
    else:
      #logDebug("#'primaryKeys' is not found:[{}]".format(self.input_dict.keys()))
      primaryKey_list = []
    #logDebug("#primaryKey_list:[{}]".format(primaryKey_list))
    
    if len(primaryKey_list) > 0:
      if "platform" in self.input_dict.keys() and self.input_dict["platform"] == "boto3":
        thisPrimaryKey_list = []
        for primaryKey in primaryKey_list:
          stripedPrimaryKey = primaryKey.strip()
          if len(stripedPrimaryKey) > 2:
            thisPrimaryKey_list.append("{}{}".format(stripedPrimaryKey[0].upper(), stripedPrimaryKey[1:]))
      else:
        thisPrimaryKey_list = []
        for primaryKey in primaryKey_list:
          stripedPrimaryKey = primaryKey.strip()
          if len(stripedPrimaryKey) > 2:
            thisPrimaryKey_list.append("{}{}".format(stripedPrimaryKey[0].lower(), stripedPrimaryKey[1:]))
      primaryKey_list = thisPrimaryKey_list
    
    #logDebug("#primaryKey_list:[{}]".format(primaryKey_list))
    return primaryKey_list
          
    
  def getPrimaryKeys(self):
    return self.primaryKey_list
  
  def get(self):
    
    if "dynamodb" == self.serviceName and "describeTable" == self.apiName:
      
      newThisResult_list = []
      parsedResult_list = self.getDynamoDBDescribeTable(self.result)
      if isinstance(parsedResult_list, list):
        for newResult_dict in parsedResult_list:
          newThisResult_list.append(newResult_dict)
      else:
        newThisResult_list = parsedResult_list
          
      self.result = newThisResult_list
      
    elif "trustedadvisor" == self.serviceName and "describeCheckItems" == self.apiName:
      
      try:
        if "checkId" in self.input_dict.keys():
          self.result["checkId"] = self.input_dict["checkId"]
        elif "args" in self.input_dict.keys():
          if isinstance(self.input_dict["args"], dict) and "checkId" in self.input_dict["args"].keys():
            self.result["checkId"] = self.input_dict["args"]["checkId"]
          elif isinstance(self.input_dict["args"], str) and "checkId" in json.loads(self.input_dict["args"]).keys():
            self.result["checkId"] = json.loads(self.input_dict["args"])["checkId"]
          else:
            raiseValueError("unexpected type:{}:input_dict:[{}]".format(type(self.input_dict["args"]), self.input_dict["args"]))
        else:
          raiseValueError("unexpected type:{}:input_dict:[{}]".format(type(self.input_dict), self.input_dict))
      except:
        logException("unexpected self.input_dict:[{}]".format(self.input_dict))
     
        
    elif "awscbresourceadminservice" == self.serviceName and "getParentAccountForChildAccount" == self.apiName:
      
      try:
        self.result = {
          "accountId": self.payload_dict["args"]["accountId"],
          **self.result
          }
        logDebug("{}:[{}]".format(self.apiName, self.result))
          
      except:
        logException("unexpected results:[{}]".format(self.result))
    
    elif "avs" == self.serviceName and "getAccountStatus" == self.apiName:
      try:
        if len(self.payload_dict["args"]["accountIds"]) == len(self.result["accountStatus"]):
          newThisResult_list = []
          accountIdCount = 0
          for accountId in self.payload_dict["args"]["accountIds"]:
            newThisResult_list.append(
              {
                "accountId":accountId,
                "regionCode": self.input_dict["regionCode"],
                "accountStatus":self.result["accountStatus"][accountIdCount]
                }
              )
          
          self.result = newThisResult_list
        else:
          logWarn("requested accountIds Count:[{}] is not matched with the result Count:[{}]".format(len(self.payload_dict["args"]["accountIds"]), len(self.result["accountStatus"])))
      
      except:
        logException("unexpected results:[{}]".format(self.result))
    
    elif "avs" == self.serviceName and "getSupportLevel" == self.apiName:
      try:
        if len(self.payload_dict["args"]["accountIds"]) == len(self.result["supportLevels"]):
          newThisResult_list = []
          accountIdCount = 0
          for accountId in self.payload_dict["args"]["accountIds"]:
            newThisResult_list.append(
              {
                "accountId":accountId,
                "regionCode": self.input_dict["regionCode"],
                "supportLevel":self.result["supportLevels"][accountIdCount]
                }
              )
          
          self.result = newThisResult_list
        else:
          logWarn("requested accountIds Count:[{}] is not matched with the result Count:[{}]".format(len(self.payload_dict["args"]["accountIds"]), len(self.result["accountStatus"])))
      
      except:
        logException("unexpected results:[{}]".format(self.result))
    
    elif "support" == self.serviceName and "describeCase" == self.apiName:
      #logDebug("#type:{}:[{}]".format(type(self.result), self.result))
      
      newThisResult_list = []
      if "caseDetails" in self.result.keys():
        caseDetails_dict = self.result["caseDetails"]
        del self.result["caseDetails"]
        
        if "recentCommunications" in caseDetails_dict.keys():
          recentCommunications_dict = caseDetails_dict["recentCommunications"]
          del caseDetails_dict["recentCommunications"]
          
          if "communications" in recentCommunications_dict.keys():
            communications_list = recentCommunications_dict["communications"]
            del recentCommunications_dict["communications"]
          else:
            communications_list = []
        
        else:
          recentCommunications_dict = {}
          communications_list = []
      
      else:
        caseDetails_dict = {}
        recentCommunications_dict = {}
        communications_list = []
      
      if "annotations" in self.result.keys():
        #logDebug("#type:{}:annotations:[{}]".format(type(self.result["annotations"]), self.result["annotations"]))
        annotations_list = self.result["annotations"]
        del self.result["annotations"]
        
        for annotation_dict in annotations_list:
          newThisResult_list.append(
            {
              "commType":"annotation",
              **caseDetails_dict,
              **annotation_dict,
              **self.result,
              **recentCommunications_dict
              }
            )
      
      for communication_dict in communications_list:
        newThisResult_list.append(
          {
            "commType":"correspondence",
            **caseDetails_dict,
            **communication_dict,
            **self.result,
            **recentCommunications_dict
            }
          )
      
      self.result = newThisResult_list
      
    elif "alb" == self.serviceName and "describeTargetGroups" == self.apiName:
      try:
        loadBalancer = self.payload_dict["args"]["loadBalancerArn"].split("loadbalancer/")[-1]
        
        logInfo("self.result:{}:[{}]".format(loadBalancer, self.result))
        newThisResult_list = []
        for resultItem_dict in self.result["targetGroups"]:
          newThisResult_list.append(
            {
              "loadBalancer": loadBalancer,
              **resultItem_dict
              }
            )
        
        self.result = newThisResult_list
      except:
        logException("unexpected results:[{}]".format(self.result))
    
    '''
    elif "avs" == self.serviceName and "getAccountStatus" == self.apiName:
      
      try:
        arg_dict = json.loads(self.input_dict["args"].replace("'",'"'))
        if "args" in self.input_dict.keys() \
          and "accountIds" in arg_dict.keys() \
          and isinstance(arg_dict["accountIds"], list) \
          and "accountStatus" in self.result.keys() \
          and isinstance(self.result["accountStatus"],list) \
          and len(arg_dict["accountIds"]) == len(self.result["accountStatus"]):
      
          newThisResult_list = []
          for offset in range(len(arg_dict["accountIds"])):
            newThisResult_list.append({"accountId":arg_dict["accountIds"][offset], "accountStatus":self.result["accountStatus"][offset]})
          
          self.result = newThisResult_list
      except:
        logException("unable to load json with args:[{}]".format(self.input_dict["args"]))
    '''
    thisResult_list = self.parseResults(self.result)
    #logDebug("type:{}:thisResult_list(len:{:,}):[{}]".format(type(thisResult_list), len(thisResult_list), thisResult_list))
    
    if len(self.additionalValue_dict.keys()) > 0:
      thisResultWithAdditionalValues_list = []
      
      if isinstance(thisResult_list, dict):
        '''
        if "createdDate" in thisResult_list.keys() and thisResult_list["createdDate"] not in ["", None]:
          try:
            thisResult_list["createdDate"] = getDateString(thisResult_list["createdDate"]/1000)
            thisResult_list["age_d"] = float("{:.2f}".format((time.time() - thisResult_list["createdDate"]/1000) /86400))
          except:
            logWarn("unable to parse 'createdDate':[{}]".format(thisResult_list["createdDate"]))
        
        elif "creationDate" in thisResult_list.keys() and thisResult_list["creationDate"] not in ["", None]:
          try:
            thisResult_list["creationDate"] = getDateString(thisResult_list["creationDate"]/1000)
            thisResult_list["age_d"] = float("{:.2f}".format((time.time() - thisResult_list["creationDate"]/1000) /86400))
          except:
            logWarn("unable to parse 'creationDate':[{}]".format(thisResult_list["creationDate"]))
        '''
        if "completionDate" in thisResult_list.keys() and thisResult_list["completionDate"] not in ["", None]:
          try:
            thisResult_list["completionDate"] = getDateString(thisResult_list["completionDate"]/1000)
          except:
            logWarn("unable to parse 'completionDate':[{}]".format(thisResult_list["completionDate"]))
            
        thisResultWithAdditionalValues_list = {**self.additionalValue_dict, **self.args_dict, **thisResult_list}
      
      elif isinstance(thisResult_list, list):
        for resultItem_dict in thisResult_list:
          
          #logDebug("type:{}:additionalValue_dict:[{}]".format(type(self.additionalValue_dict), self.additionalValue_dict))
          #logDebug("type:{}:resultItem_dict:[{}]".format(type(resultItem_dict), resultItem_dict))
          
          try:
            if isinstance(resultItem_dict, dict):
              '''
              if "createdDate" in resultItem_dict.keys() and resultItem_dict["createdDate"] not in [None, "", "None"]:
                if isinstance(resultItem_dict["createdDate"], str):
                  continue
                else: 
                  try:
                    resultItem_dict["createdDate"] = getDateString(resultItem_dict["createdDate"]/1000)
                    thisResult_list["age_d"] = float("{:.2f}".format((time.time() - thisResult_list["createdDate"]/1000) /86400))
                  except:
                    logWarn("unable to parse 'createdDate':[{}]".format(resultItem_dict["createdDate"]))
                
              elif "creationDate" in resultItem_dict.keys() and resultItem_dict["creationDate"] not in [None, "", "None"]:
                if isinstance(resultItem_dict["creationDate"], str):
                  continue
                else: 
                    
                  try:
                    resultItem_dict["creationDate"] = getDateString(resultItem_dict["creationDate"]/1000)
                    thisResult_list["age_d"] = float("{:.2f}".format((time.time() - thisResult_list["creationDate"]/1000) /86400))
                  except:
                    logWarn("unable to parse 'creationDate':[{}]".format(resultItem_dict["creationDate"]))
              '''
              
              if "completionDate" in resultItem_dict.keys() and resultItem_dict["completionDate"] not in [None, "", "None"]:
                try:
                  resultItem_dict["completionDate"] = getDateString(resultItem_dict["completionDate"]/1000)
                except:
                  logWarn("unable to parse 'completionDate':[{}]".format(resultItem_dict["completionDate"]))
                  
              thisResultWithAdditionalValues_list.append({**self.additionalValue_dict, **self.args_dict, **resultItem_dict})
            else:
              thisResultWithAdditionalValues_list.append({**self.additionalValue_dict, **self.args_dict, "result":resultItem_dict})
          except Exception as e:
            logException("unable to add additional values:[{}] with resultItem_dict".format(self.additionalValue_dict, resultItem_dict))
            thisResultWithAdditionalValues_list.append({**self.additionalValue_dict, **self.args_dict, **{"error":{"result":resultItem_dict, "error":"{}".format(e)}}})
            
      else:
        thisResultWithAdditionalValues_list.append({**self.additionalValue_dict, **self.args_dict, **{"error":thisResult_list}})
        
      thisResult_list = thisResultWithAdditionalValues_list
    
    # filter results with conditions
    '''
    try:
      if "conditions" in self.input_dict.keys() and self.input_dict["conditions"].strip() != "" and "getMetricStatistics" not in self.apiName:
        gcConditions = GcConditions(self.input_dict["conditions"], thisResult_list)
        thisResult_list = gcConditions.get()
        if len(thisResult_list) > 0:
          logInfo("conditions:[{}]->results(len:{}):[{}]".format(self.input_dict["conditions"], len(thisResult_list), thisResult_list[-1]))
        else:
          logInfo("conditions:[{}]->results(len:{}):[{}]".format(self.input_dict["conditions"], len(thisResult_list), thisResult_list))
    except Exception as e:
      logException("unable to filter the result with conditions:[{}]")
    ''' 
      
    '''
    if isinstance(thisResult_list, list) and len(thisResult_list) > 0:
      logDebug("type:{}:thisResult_list(len:{:,})[-1]:[{}]".format(type(thisResult_list), len(thisResult_list), thisResult_list[-1]))
    elif isinstance(thisResult_list, dict) and len(thisResult_list.keys()) > 0:
      logDebug("type:{}:thisResult_list(len:{:,})[-1]:[{}]".format(type(thisResult_list), len(thisResult_list.keys()), thisResult_list.keys()))
    else:
      logDebug("type:{}:thisResult_list(len:{:,}):[{}]".format(type(thisResult_list), len(thisResult_list), thisResult_list))
    '''
      

    if isinstance(thisResult_list, list) and len(thisResult_list) > 0 and isinstance(thisResult_list[0], dict):
      if "result" in thisResult_list[0].keys() and isinstance(thisResult_list[0]["result"], str) and thisResult_list[0]["result"].lower().startswith("arn"):
        for result_dict in thisResult_list:
          try:
            result_dict["arnV1"] = result_dict["result"].split(":")[-1]
            result_dict["arnV2"] = result_dict["result"].split(":")[-1].split("/")[-1]
            if len(result_dict["result"].split("/")) > 2:
              result_dict["arnV3"] = "{}/{}".format(result_dict["result"].split("/")[-2], result_dict["result"].split("/")[-1])
            
            #logInfo("------>arnV4:[{}]".format(result_dict["result"]))
            if len(result_dict["result"].split("/")) > 3:
              result_dict["arnV4"] = "{}/{}/{}".format(result_dict["result"].split("/")[-3], result_dict["result"].split("/")[-2], result_dict["result"].split("/")[-1])
          except:
            logException("unexpected result_dict:[{}]".format(result_dict))
      
      elif "result" in thisResult_list[0].keys() and isinstance(thisResult_list[0]["result"], str) and thisResult_list[0]["result"].lower().startswith("http"):
        for result_dict in thisResult_list:
          try:
            result_dict["urlV1"] = result_dict["result"].split("/")[-1]
          except:
            logException("unexpected result_dict:[{}]".format(result_dict))
      else:
        thisArnKey = None
        for key in thisResult_list[0].keys():
          if key.lower().find("arn") and key[-3:].lower() == "arn" and isinstance(thisResult_list[0][key], str) and len(thisResult_list[0][key]) > 3:
            thisArnKey = key
            break
        
        if thisArnKey != None:
          for result_dict in thisResult_list:
            if thisArnKey in result_dict.keys() and isinstance(result_dict[thisArnKey], str) and len(result_dict[thisArnKey]) > 0:
              result_dict["arnV1"] = result_dict[thisArnKey].split(":")[-1]
              result_dict["arnV2"] = result_dict[thisArnKey].split("/")[-1]
              if len(result_dict[thisArnKey].split("/")) > 2:
                result_dict["arnV3"] = "{}/{}".format(result_dict[thisArnKey].split("/")[-2], result_dict[thisArnKey].split("/")[-1])
              
              #logInfo("------>arnV4:[{}]".format(result_dict[thisArnKey]))
              if len(result_dict[thisArnKey].split("/")) > 3:
                result_dict["arnV4"] = "{}/{}/{}".format(result_dict[thisArnKey].split("/")[-3], result_dict[thisArnKey].split("/")[-2], result_dict[thisArnKey].split("/")[-1])
                
        thisUrlKey = None
        for key in thisResult_list[0].keys():
          if key.lower().find("url") and key[-3:].lower() == "url" and isinstance(thisResult_list[0][key], str) and len(thisResult_list[0][key]) > 3:
            thisUrlKey = key
            break
        
        if thisUrlKey != None:
          for result_dict in thisResult_list:
            if thisUrlKey in result_dict.keys() and isinstance(result_dict[thisUrlKey], str) and len(result_dict[thisUrlKey]) > 0:
              result_dict["urlV1"] = result_dict[thisUrlKey].split("/")[-1]
        
    elif isinstance(thisResult_list, dict):
      if "result" in thisResult_list.keys() and thisResult_list["result"].lower().startswith("arn"):
        for result_dict in thisResult_list:
          try:
            result_dict["arnV1"] = result_dict["result"].split(":")[-1]
            result_dict["arnV2"] = result_dict["result"].split("/")[-1]
            if len(result_dict["result"].split("/")) > 2:
              result_dict["arnV3"] = "{}/{}".format(result_dict["result"].split("/")[-2], result_dict["result"].split("/")[-1])
            
            #logInfo("------>arnV4:[{}]".format(result_dict["result"]))
            if len(result_dict["result"].split("/")) > 3:
              result_dict["arnV4"] = "{}/{}/{}".format(result_dict["result"].split("/")[-3], result_dict["result"].split("/")[-2], result_dict["result"].split("/")[-1])
          except:
            logException("unexpected result_dict:[{}]".format(result_dict))
            
      elif "result" in thisResult_list.keys() and thisResult_list["result"].lower().startswith("http"):
        for result_dict in thisResult_list:
          try:
            result_dict["urlV1"] = result_dict["url"].split("/")[-1]
          except:
            logException("unexpected result_dict:[{}]".format(result_dict))
            
      else:
        thisArnKey = None
        for key in thisResult_list.keys():
          if key.lower().find("arn") and key[-3:].lower() == "arn" and isinstance(thisResult_list[key], str) and len(thisResult_list[key]) > 3:
            thisArnKey = key
            break
        
        if thisArnKey != None and thisArnKey in thisResult_list.keys():
          try:
            thisResult_list["arnV1"] = thisResult_list[thisArnKey].split(":")[-1]
            thisResult_list["arnV2"] = thisResult_list[thisArnKey].split("/")[-1]
            if len(thisResult_list[thisArnKey].split("/")) > 2:
              thisResult_list["arnV3"] = "{}/{}".format(thisResult_list[thisArnKey].split("/")[-2], thisResult_list[thisArnKey].split("/")[-1])
            
            #logInfo("------>arnV4:[{}]".format(thisResult_list[thisArnKey]))
            if len(thisResult_list[thisArnKey].split("/")) > 3:
              thisResult_list["arnV4"] = "{}/{}/{}".format(thisResult_list[thisArnKey].split("/")[-3], thisResult_list[thisArnKey].split("/")[-2], thisResult_list[thisArnKey].split("/")[-1])
          except:
            logException("unexpected thisResult_list:[{}]".format(thisResult_list))
            
          
        thisUrlKey = None
        for key in thisResult_list.keys():
          if key.lower().find("url") and key[-3:].lower() == "url" and isinstance(thisResult_list[key], str) and len(thisResult_list[key]) > 3:
            thisUrlKey = key
            break
        
        if thisUrlKey != None and thisUrlKey in thisResult_list.keys():
          try:
            thisResult_list["urlV1"] = thisResult_list[thisUrlKey].split("/")[-1]
          except:
            logException("unexpected thisResult_list:[{}]".format(thisResult_list))
          
          
    #logDebug("#thisResult_list(len:{})".format(len(thisResult_list)))
    
    if "getMetricStatistics" in self.apiName:
      pass
    else:
      thisResult_list = self.updateEpochTimeToDate(thisResult_list)
      thisResult_list = self.updateResourceName(thisResult_list)
      
      if "updateIpAddresses" in self.input_dict.keys():
        logDebug("'updateIpAddresses' will be processed")
        thisResult_list = self.updateIpAddresses(thisResult_list=thisResult_list, updateIpAddressKeys=self.input_dict["updateIpAddresses"])
      elif "inputs" in self.input_dict.keys() and isinstance(self.input_dict["inputs"], dict) and "updateIpAddresses" in self.input_dict["inputs"].keys():
        logDebug("'updateIpAddresses' will be processed")
        thisResult_list = self.updateIpAddresses(thisResult_list=thisResult_list, updateIpAddressKeys=self.input_dict["inputs"]["updateIpAddresses"])
      #else:
      #  
       
    #for thisItem_dict in thisResult_list:
    #  if "resourceName_" in thisItem_dict.keys():
    #    logDebug("resourceName_:[{}]".format(thisItem_dict["resourceName_"]))
    #logInfo("#thisResult_list(len:{})".format(len(thisResult_list)))
    
     
    return thisResult_list
  
  def serializedJsonWithList(self, parsedResultItem_list):
    for subResultItem_dict in parsedResultItem_list:
      if isinstance(subResultItem_dict, str) or isinstance(subResultItem_dict, int) or isinstance(subResultItem_dict, float):
        continue
      
      elif subResultItem_dict in ["", None]:
        logWarn(f"subResultItem_dict:[{subResultItem_dict}] is not json serializable")
        subResultItem_dict = ""

      elif isinstance(subResultItem_dict, dict):
        subResultItem_dict = self.serializedJsonWithDict(subResultItem_dict)
      
      elif isinstance(subResultItem_dict, list):
        if len(subResultItem_dict) == 1:
          subResultItem_dict = subResultItem_dict[0]
          if isinstance(subResultItem_dict, dict):
            subResultItem_dict = self.serializedJsonWithDict(subResultItem_dict)
          elif isinstance(subResultItem_dict, list):
            subResultItem_dict = self.serializedJsonWithList(subResultItem_dict)
          else:
            try:
              json.dump(subResultItem_dict)
            except:
              logWarn(f"subResultItem_dict:[{subResultItem_dict}] is not json serializable")
              subResultItem_dict = f"{subResultItem_dict}"
        else:
          subResultItem_dict = self.serializedJsonWithList(subResultItem_dict)

      else:
        try:
          json.dump(subResultItem_dict)
        except:
          subResultItem_dict = f"{subResultItem_dict}"
    
    return parsedResultItem_list

  def serializedJsonWithDict(self, parsedResultItem_dict):
    for key in set(parsedResultItem_dict.keys()):
      if isinstance(parsedResultItem_dict[key], str) or isinstance(parsedResultItem_dict[key], int) or isinstance(parsedResultItem_dict[key], float):
        continue
      
      elif parsedResultItem_dict[key] in ["", None]:
        logWarn(f"parsedResultItem_dict[{key}]:[{parsedResultItem_dict[key]}] is not json serializable")
        parsedResultItem_dict[key] = ""

      elif isinstance(parsedResultItem_dict[key], dict):
        #logDebug(f"{type(parsedResultItem_dict[key]).__name__}:{key}:[{parsedResultItem_dict[key]}]")
        parsedResultItem_dict[key] = self.serializedJsonWithDict(parsedResultItem_dict[key])
        if isinstance(parsedResultItem_dict[key], dict):
          for key2 in parsedResultItem_dict[key].keys():
            if key2 in parsedResultItem_dict.keys():
              postfixString = "_"
              while f"{key2}{postfixString}" in parsedResultItem_dict.keys():
                postfixString += "_"
              parsedResultItem_dict[f"{key2}{postfixString}"] = parsedResultItem_dict[key][key2]
            else:
              parsedResultItem_dict[key2] = parsedResultItem_dict[key][key2]

          del parsedResultItem_dict[key]
          
      elif isinstance(parsedResultItem_dict[key], list):
        #logDebug(f"{type(parsedResultItem_dict[key]).__name__}:{key}:[{parsedResultItem_dict[key]}]")
        if len(parsedResultItem_dict[key]) == 1:
          parsedResultItem_dict[key] = parsedResultItem_dict[key][0]
          if isinstance(parsedResultItem_dict[key], dict):
            parsedResultItem_dict[key] = self.serializedJsonWithDict(parsedResultItem_dict[key])
          elif isinstance(parsedResultItem_dict[key], list):
            parsedResultItem_dict[key] = self.serializedJsonWithList(parsedResultItem_dict[key])
          else:
            try:
              json.dump(parsedResultItem_dict[key])
            except:
              logWarn(f"parsedResultItem_dict[{key}]:[{parsedResultItem_dict[key]}] is not json serializable")
              parsedResultItem_dict[key] = f"{parsedResultItem_dict[key]}"
        else:
          parsedResultItem_dict[key] = self.serializedJsonWithList(parsedResultItem_dict[key])

      else:
        try:
          json.dump(parsedResultItem_dict[key])
        except:
          logWarn(f"parsedResultItem_dict[{key}]:[{parsedResultItem_dict[key]}] is not json serializable")
          parsedResultItem_dict[key] = f"{parsedResultItem_dict[key]}"
  
    return parsedResultItem_dict
  
  def serializedJson(self, result_list):
    for parsedResultItem_dict in result_list:
      if isinstance(parsedResultItem_dict, str) or isinstance(parsedResultItem_dict, int) or isinstance(parsedResultItem_dict, float):
        continue
      
      elif parsedResultItem_dict in ["", None]:
        parsedResultItem_dict = ""

      elif isinstance(parsedResultItem_dict, dict):
        parsedResultItem_dict = self.serializedJsonWithDict(parsedResultItem_dict)
      
        for key in set(parsedResultItem_dict.keys()):
          if isinstance(parsedResultItem_dict[key], dict):
            for key2 in parsedResultItem_dict[key].keys():
              if key2 in parsedResultItem_dict.keys():
                postfixString = "_"
                while f"{key2}{postfixString}" in parsedResultItem_dict.keys():
                  postfixString += "_"
                parsedResultItem_dict[f"{key2}{postfixString}"] = parsedResultItem_dict[key][key2]
              else:
                parsedResultItem_dict[key2] = parsedResultItem_dict[key][key2]

            del parsedResultItem_dict[key]

      elif isinstance(parsedResultItem_dict, list):
        parsedResultItem_dict = self.serializedJsonWithList(parsedResultItem_dict)

      else:
        try:
          json.dump(parsedResultItem_dict)
        except:
          parsedResultItem_dict = f"{parsedResultItem_dict}"
      
    return result_list

  def updateResourceName(self, thisResult_list):
    if len(self.resourceName_list) > 0:
      #logInfo("#---yyy--->\tself.resourceName_list:[{}]".format(self.resourceName_list))
      
      for thisResultItem_dict in thisResult_list:
        #logInfo("#thisResultItem_dict.keys():[{}]".format(thisResultItem_dict.keys()))
        
        thisResourceName = ""
        if isinstance(thisResultItem_dict, dict):
          for resourceNameKey in self.resourceName_list:
            if resourceNameKey in thisResultItem_dict.keys():
              resourceNameValue = "{}".format(thisResultItem_dict[resourceNameKey])
              
            elif thisResourceName == None:
              resourceNameValue = resourceNameKey
              
            else:
              resourceNameValue = None
            
            #if resourceNameKey.startswith("dimension/") and resourceNameValue != None:
            #  logInfo("#ddd\t{}:[{}]".format(resourceNameKey, resourceNameValue))
            
            if resourceNameValue != None:
              if thisResourceName == "":
                thisResourceName = "{}".format(resourceNameValue)
              else:
                thisResourceName += "|{}".format(resourceNameValue)
            
            #else:
            #  pass
            
            #logInfo("#resourceName:[{}]->thisResourceName:[{}]".format(resourceName, thisResourceName))
          
          thisResultItem_dict["resourceName_"] = thisResourceName
            
          #logInfo("#ddd\tthisResourceName:[{}]".format(thisResultItem_dict["resourceName_"]))
        #logInfo("#resourceName:[{}]->thisResourceName:[{}]".format(resourceName, thisResultItem_dict["resourceName_"]))
        
    return thisResult_list
  
  def updateIpAddresses(self, thisResult_list, updateIpAddressKeys):
    updateIpAddressKey_list = []
    for updateIpAddressesKey in updateIpAddressKeys.split(","):
      if len(updateIpAddressesKey.strip()) > 0:
        updateIpAddressKey_list.append(updateIpAddressesKey)
        
    if len(updateIpAddressKey_list) > 0:
      if len(updateIpAddressKey_list) == 1:
        for thisResultItem_dict in thisResult_list:
          if updateIpAddressKey_list[-1] in thisResultItem_dict.keys():
            getIpAddressDetails_list = getIPv4AddressDetails(ipAddress=thisResultItem_dict[updateIpAddressKey_list[-1]])
            
            for getIpAddressDetailsItem_dict in getIpAddressDetails_list:
              for thisKey in getIpAddressDetailsItem_dict.keys():
                thisResultItem_dict["{}|{}".format(updateIpAddressKey_list[-1],thisKey)] = getIpAddressDetailsItem_dict[thisKey]
            
      else:
        for thisResultItem_dict in thisResult_list:
          for thisIpAddressKey in updateIpAddressKey_list:
            if thisIpAddressKey in thisResultItem_dict.keys():
              getIpAddressDetails_dict = getIPv4AddressDetails(ipAddress=thisResultItem_dict[thisIpAddressKey])
              
              for getIpAddressDetailsItem_dict in getIpAddressDetails_list:
                for thisKey in getIpAddressDetailsItem_dict.keys():
                  thisResultItem_dict["{}|{}".format(updateIpAddressKey_list[-1],thisKey)] = getIpAddressDetailsItem_dict[thisKey]
        
    return thisResult_list
  
  def getCwGetMetricStatistics(self, result_list):
    thisResult_list = []
    
    if "mode" in self.input_dict.keys():
      cwMode = self.input_dict["mode"]
    else:
      cwMode = None
      
    dimensionValue_dict = {}
    try:
      #logInfo("#===>dimensions:[{}]".format(self.input_dict["dimensions"]))
      if isinstance(self.input_dict["dimensions"], str):
        try:
          self.input_dict["dimensions"] = json.loads(self.input_dict["dimensions"])
        except:
          try:
            for thisDimensionItem in self.input_dict["dimensions"].split(","):
              thisDimensionItem_list = thisDimensionItem.split(":")
              if len(thisDimensionItem_list) > 1 and thisDimensionItem_list[1] in self.input_dict.keys():
                dimensionValue_dict["dimension/{}".format(thisDimensionItem_list[0])] = self.input_dict[thisDimensionItem_list[1]]
                
          except:
            logException("unexpected self.input_dict['dimensions']:[{}]".format(self.input_dict["dimensions"]))
          
            #self.input_dict["dimensions"] = []
            return thisResult_list
          
      #logDebug("#======>thisResultItem_dict[{}]:type:[{}]:[{}]".format(thisPrimaryKey, type(thisResultItem_dict[thisPrimaryKey]), thisResultItem_dict[thisPrimaryKey]))
      elif isinstance(self.input_dict["dimensions"], list):
        try:
          if len(self.input_dict["dimensions"]) > 0 and "value" in self.input_dict["dimensions"][0].keys():
            for dimensionItem_dict in self.input_dict["dimensions"]:
              dimensionValue_dict["dimension/{}".format(dimensionItem_dict["name"])] = dimensionItem_dict["value"]
          else:
            for dimensionItem_dict in self.input_dict["dimensions"]:
              dimensionValue_dict["dimension/{}".format(dimensionItem_dict["Name"])] = dimensionItem_dict["Value"]
              
        except:
          logException("unable to unpack dimensionItem_dict:[{}]".format(dimensionItem_dict))
          
    except:
      logException("unable to parse self.input_dict:[{}]".format(self.input_dict))
    #logInfo("#===>dimensionValue_dict:[{}]".format(dimensionValue_dict))
      
      
    if "period" in self.input_dict.keys():
      periodString = "period"
    else:
      periodString = "Period"
      
    if isinstance(self.input_dict[periodString], str):
      try:
        self.input_dict[periodString] = int(self.input_dict[periodString])
        period = self.input_dict[periodString]
      except:
        logException("unexpected type:{}:period:[{}]".format(type(self.input_dict[periodString]), self.input_dict[periodString]))
        
        return thisResult_list
        
    elif isinstance(self.input_dict[periodString], int) or isinstance(self.input_dict[periodString], float):
      try:
        period = self.input_dict[periodString]
      except:
        logException("unexpected type:{}:period:[{}]".format(type(self.input_dict[periodString]), self.input_dict[periodString]))
        
        return thisResult_list
        
    else:
      logException("unexpected type:{}:period:[{}]".format(type(self.input_dict[periodString]), self.input_dict[periodString]))
      
      return thisResult_list
    
    
    if "namespace" in self.input_dict.keys():
      namespaceString = "namespace"
    else:
      namespaceString = "Namespace"
    
    if "metricName" in self.input_dict.keys():
      metricNameString = "metricName"
    else:
      metricNameString = "MetricName"
    
    cwIndexKey = None
    if isinstance(self.input_dict[namespaceString], str) and len(self.input_dict[namespaceString]) > 0:
      cwServiceName = self.input_dict[namespaceString].split("/")[-1]
      regionCode = self.input_dict["regionCode"]
      accountId = self.input_dict["accountId"]
      
      cwIndexKey = "{}:{}:{}".format(cwServiceName, regionCode, accountId)
      for key in dimensionValue_dict.keys():
        cwIndexKey += ":{}".format(dimensionValue_dict[key])

    if cwMode != None and cwMode.lower() == "summary":
      
      if "modeStatic" in self.input_dict.keys():
        if ":" in self.input_dict["modeStatic"]:
          for modeStaticString in self.input_dict["modeStatic"].split("|"):
            modeStaticString_list = modeStaticString.split(":")
            if self.input_dict[metricNameString] in modeStaticString_list[1].split(","):
              self.input_dict["modeStatic"] = modeStaticString_list[0]
              break
            
        if self.input_dict["modeStatic"].lower() not in ["maximum", "minimum", "average", "sum", "sample"]:
          self.input_dict["modeStatic"] = "maximum"  
      
      if "modeStaticAverage" in self.input_dict.keys():
        modeStaticAverage = self.input_dict["modeStaticAverage"]
      else:
        modeStaticAverage = None
            
      if "modeStaticCount" in self.input_dict.keys():
        if isinstance(self.input_dict["modeStaticCount"], str):
          modeStaticCount = int(self.input_dict["modeStaticCount"])
        elif isinstance(self.input_dict["modeStaticCount"], int):
          modeStaticCount = self.input_dict["modeStaticCount"]
        else:
          logWarn("unexpected type:{}:modeStaticCount:[{}]".format(self.input_dict["modeStaticCount"]))
          modeStaticCount = -1
      else:
        modeStaticCount = -1
      
      currentTime = time.time()
      statistics_dict = {
        "last2m":False, 
        "last10m":False, 
        "last30m":False, 
        "last120m":False, 
        "lastActiveTimestamp":0, 
        "lastActiveAge_s":currentTime, 
        "lifeSpan_h":0, 
        "minTimestamp":0, 
        "maxTimestamp":0, 
        "sampleCountSum":0, 
        "maxSampleCount":0,
        "minSampleCount":0, 
        "maxAverage":0,  
        "minAverage":0, 
        "maxAverageSumBySampleCount":0,
        "avgOfMaxHitCount":0,
        "avgOfMax": 0,
        "maxOfMax": 0,
        "maxOfMaxTime":None,
        "minOfMin": 0,
        "avgOfSumHitCount":0,
        "avgOfSum": 0,
        "maxOfSum": 0,
        "maxOfSumTime":None,
        "sumOfSum": 0,
        "threshold":0,
        "thresholdHhitCount":0,
        "activeCount":0, 
        "idleCount":0, 
        "sum":0,  
        "minimum":0,  
        "maximum":0
        }
      #logInfo("#===>input:[{}]".format(self.input_dict))
      
      threshold = None
      timestampString = None
      if len(result_list) > 0 and isinstance(result_list[0], dict):
        
        if "timestamp" in result_list[0].keys():
          timestampString = "timestamp"
          sampleCountString = "sampleCount"
          sumString = "sum"
          averageString = "average"
          minimumString = "minimum"
          maximumString = "maximum"
          
          if "modeStatic" in self.input_dict.keys():
            modeStatic = "{}{}".format(self.input_dict["modeStatic"][0].lower(),self.input_dict["modeStatic"][1:])
            
          else:
            modeStatic = None
          
        elif "Timestamp" in result_list[0].keys():
          timestampString = "Timestamp"
          sampleCountString = "SampleCount"
          sumString = "Sum"
          averageString = "Average"
          minimumString = "Minimum"
          maximumString = "Maximum"
          
          
          if "modeStatic" in self.input_dict.keys():
            modeStatic = "{}{}".format(self.input_dict["modeStatic"][0].upper(),self.input_dict["modeStatic"][1:])
          else:
            modeStatic = None
          
          try:
            if "threshold" in self.input_dict.keys():
              threshold = float(self.input_dict["threshold"])
          except:
            logError("unexpected {}:threshold:[{}]".format(type(self.input_dict["threshold"]).__name__, self.input_dict["threshold"]))
              
        else:
          return [
            {
              "cwIndexKey": cwIndexKey,
              "apiName_":self.input_dict["apiName"], 
              "accountId_":self.input_dict["accountId"], 
              "regionCode_":self.input_dict["regionCode"], 
              "resourceName_":None,
              "namespace":self.input_dict[namespaceString], 
              "metricName":self.input_dict[metricNameString], 
              "period":self.input_dict[periodString],
              **dimensionValue_dict,
              **statistics_dict,
              "errorReason":"no datapoints"
              } 
            ]
      
      statistics_dict["modeStatic"] = modeStatic
      statistics_dict["threshold"] = threshold
      datapoint_dict = {}
      if timestampString != None:
        sum_list = []
        maximum_list = []
        for result_dict in result_list:
          if isinstance(result_dict, dict):
            if modeStatic != None:
              
              if self.input_dict[periodString] >= 3600:
                timestampOffset = 13
              else:
                timestampOffset = 18
                
              try:
                datapoint_dict["t.{}".format(getDateString(result_dict[timestampString]/1000)[5:timestampOffset])] = result_dict[modeStatic]
                try:
                  if threshold != None and result_dict[modeStatic] >= threshold:
                    statistics_dict["thresholdHhitCount"] += 1
                except:
                  logException("unexpected error")
                  
              except:
                datapoint_dict["t.{}".format(getDateString(result_dict[timestampString]/1000)[5:timestampOffset])] = result_dict[sumString]
              
            if statistics_dict["minTimestamp"] == 0:
              statistics_dict["minTimestamp"] = result_dict[timestampString]
            elif result_dict[timestampString] < statistics_dict["minTimestamp"]:
              statistics_dict["minTimestamp"] = result_dict[timestampString]
            
            if statistics_dict["maxTimestamp"] == 0:
              statistics_dict["maxTimestamp"] = result_dict[timestampString]
              
              statistics_dict["sum"] = result_dict[sumString]
              statistics_dict["minimum"] = result_dict[minimumString]
              statistics_dict["maximum"] = result_dict[maximumString]
              
            elif result_dict[timestampString] > statistics_dict["maxTimestamp"]:
              statistics_dict["maxTimestamp"] = result_dict[timestampString]
              
              statistics_dict["sum"] = result_dict[sumString]
              statistics_dict["minimum"] = result_dict[minimumString]
              statistics_dict["maximum"] = result_dict[maximumString]
            
            sum_list.append(statistics_dict["sum"])
            maximum_list.append(statistics_dict["maximum"])
            statistics_dict["sampleCountSum"] += result_dict[sampleCountString]
            
            if statistics_dict["maxSampleCount"] == 0:
              statistics_dict["maxSampleCount"] = result_dict[sampleCountString]
            elif result_dict[sampleCountString] > statistics_dict["maxSampleCount"]:
              statistics_dict["maxSampleCount"] = result_dict[sampleCountString]
            
            if statistics_dict["minSampleCount"] == 0:
              statistics_dict["minSampleCount"] = result_dict[sampleCountString]
            elif result_dict[sampleCountString] < statistics_dict["minSampleCount"]:
              statistics_dict["minSampleCount"] = result_dict[sampleCountString]
            
            if result_dict[averageString] != 0 or result_dict[sumString] != 0 or result_dict[maximumString] != 0:
              
              statistics_dict["activeCount"] += 1
              
              if statistics_dict["lastActiveTimestamp"] == 0:
                statistics_dict["lastActiveTimestamp"] = result_dict[timestampString]
              elif result_dict[timestampString] > statistics_dict["lastActiveTimestamp"]:
                statistics_dict["lastActiveTimestamp"] = result_dict[timestampString]
              
              if statistics_dict["minAverage"] == 0:
                statistics_dict["minAverage"] = result_dict[averageString]
              elif result_dict[averageString] < statistics_dict["minAverage"]:
                statistics_dict["minAverage"] = result_dict[averageString]
              
              if statistics_dict["maxAverage"] == 0:
                statistics_dict["maxAverage"] = result_dict[averageString]
              elif result_dict[averageString] > statistics_dict["maxAverage"]:
                statistics_dict["maxAverage"] = result_dict[averageString]
              
              if statistics_dict["maxAverageSumBySampleCount"] == 0:
                statistics_dict["maxAverageSumBySampleCount"] = (result_dict[sumString] / result_dict[sampleCountString])
              elif (result_dict[sumString] / result_dict[sampleCountString]) > statistics_dict["maxAverageSumBySampleCount"]:
                statistics_dict["maxAverageSumBySampleCount"] = (result_dict[sumString] / result_dict[sampleCountString])
              
              statistics_dict["sumOfSum"] += result_dict[sumString]
              
              if statistics_dict["maxOfSum"] == None:
                statistics_dict["maxOfSum"] = result_dict[sumString]
                statistics_dict["maxOfSumTime"] = result_dict[timestampString]
              elif result_dict[sumString] > statistics_dict["maxOfSum"]:
                statistics_dict["maxOfSum"] = result_dict[sumString]
                statistics_dict["maxOfSumTime"] = result_dict[timestampString]
              
              if statistics_dict["minOfMin"] == 0:
                statistics_dict["minOfMin"] = result_dict[minimumString]
              elif result_dict[minimumString] < statistics_dict["minOfMin"]:
                statistics_dict["minOfMin"] = result_dict[minimumString]
              
              if statistics_dict["maxOfMax"] == 0:
                statistics_dict["maxOfMax"] = result_dict[maximumString]
                statistics_dict["maxOfMaxTime"] = result_dict[timestampString]
              elif result_dict[maximumString] > statistics_dict["maxOfMax"]:
                statistics_dict["maxOfMax"] = result_dict[maximumString]
                statistics_dict["maxOfMaxTime"] = result_dict[timestampString]
              
            else:
              statistics_dict["idleCount"] += 1
        
        if statistics_dict["minTimestamp"] != 0 and statistics_dict["maxTimestamp"] != 0:
          statistics_dict["lifeSpan_h"] = float("{:.2f}".format((statistics_dict["maxTimestamp"] - statistics_dict["minTimestamp"])/1000/3600))
          statistics_dict["lastActiveAge_s"] = float("{:.2f}".format(currentTime - statistics_dict["maxTimestamp"]/1000))
          
          if statistics_dict["lastActiveTimestamp"] >= (self.input_dict["endTime"] - 120000):
            statistics_dict["last2m"] = True
            statistics_dict["last10m"] = True
            statistics_dict["last30m"] = True
            statistics_dict["last120m"] = True
          elif statistics_dict["lastActiveTimestamp"] >= (self.input_dict["endTime"] - 600000):
            statistics_dict["last10m"] = True
            statistics_dict["last30m"] = True
            statistics_dict["last120m"] = True
          elif statistics_dict["lastActiveTimestamp"] >= (self.input_dict["endTime"] - 1800000):
            statistics_dict["last30m"] = True
            statistics_dict["last120m"] = True
          elif statistics_dict["lastActiveTimestamp"] >= (self.input_dict["endTime"] - 7200000):
            statistics_dict["last120m"] = True
          statistics_dict["lastActiveTimestamp"] = getDateString(statistics_dict["lastActiveTimestamp"]/1000)
          
        if statistics_dict["minTimestamp"] != 0:
          if isinstance(statistics_dict["minTimestamp"], int):
            statistics_dict["minTimestamp"] = getDateString(statistics_dict["minTimestamp"]/1000)
          else:
            statistics_dict["minTimestamp"] = "{}".format(statistics_dict["minTimestamp"])
        
        if statistics_dict["maxTimestamp"] != 0:
          if isinstance(statistics_dict["maxTimestamp"], int):
            statistics_dict["maxTimestamp"] = getDateString(statistics_dict["maxTimestamp"]/1000)
          else:
            statistics_dict["maxTimestamp"] = "{}".format(statistics_dict["maxTimestamp"])
        
        try:
          statistics_dict["avgOfSum"] = sum(sum_list) / len(sum_list)
          statistics_dict["avgOfMax"] = sum(maximum_list) / len(maximum_list)
          for result_dict in result_list:
            if isinstance(result_dict, dict):
              if result_dict[sumString] > statistics_dict["avgOfSum"]:
                statistics_dict["avgOfSumHitCount"] += 1
                
              if result_dict[maximumString] > statistics_dict["avgOfMax"]:
                statistics_dict["avgOfMaxHitCount"] += 1
                
        except:
          logException("unexpected Error")
          
      sortedDatapoint_dict = {}
      #if modeStatic.lower() in ["sum"] and modeStaticCount > 0 and len(datapoint_dict.keys()) >= modeStaticCount:
      #  datapointTimestamp_list = []
      #  for timestamp in sorted(datapoint_dict.keys()):
      #    datapointTimestamp_list.append(timestamp)
      # 
       
      #  for thisTimestamp in datapointTimestamp_list[-1*modeStaticCount:]:
      #    try:
      #      sortedDatapoint_dict[thisTimestamp] = datapoint_dict[thisTimestamp]/period
      #    except:
      #      sortedDatapoint_dict[thisTimestamp] = datapoint_dict[thisTimestamp]
      #      logException("unable to get the value:{:,} divided by period:{:,}".formAT(datapoint_dict[thisTimestamp], period))
          
      
      if modeStatic != None and modeStatic == modeStaticAverage:
        for thisTimestamp in sorted(datapoint_dict.keys()):
          try:
            datapoint_dict[thisTimestamp] = datapoint_dict[thisTimestamp]/period
          except:
            datapoint_dict[thisTimestamp] = datapoint_dict[thisTimestamp]
            logException("unable to get the value:{:,} divided by period:{:,}".formAT(datapoint_dict[thisTimestamp], period))
      
      for thisTimestamp in sorted(datapoint_dict.keys()):
        sortedDatapoint_dict[thisTimestamp] = datapoint_dict[thisTimestamp]
        
      thisResult_list.append(
        {
          "cwIndexKey": cwIndexKey,
          "serviceName_":self.input_dict[namespaceString].split("/")[-1],
          "apiName_":self.input_dict["apiName"], 
          "accountId_":self.input_dict["accountId"], 
          "regionCode_":self.input_dict["regionCode"], 
          "resourceName_":None,
          "namespace":self.input_dict[namespaceString], 
          "metricName":self.input_dict[metricNameString], 
          "period":self.input_dict[periodString], 
          **dimensionValue_dict,
          **statistics_dict,
          **sortedDatapoint_dict
          }
        )
      
     #apiName  args  conditions  limit  pt  reportName  bcaDescription  emailTemplate  startTime  endTime  accountId  regionCode  tableName  requestId  namespace  metricName  dimensions  period  mode  paginatingNumber  user  accessOverrideSession
      
    #if cwMode != None and cwMode.lower() == "summary":
    else:
      '''
      dimensionValue_dict = {}
      try:
        if "dimensions" in self.input_dict.keys():
          if isinstance(self.input_dict["dimensions"], str):
            for dimensionKey in self.input_dict["dimensions"].split(","):
              thisDimensionValueName = dimensionKey.split(":")[-1]
              thisDimensionValueName_upper = "{}{}".format(thisDimensionValueName[0].upper(), thisDimensionValueName[1:])
              thisDimensionValueName_lower = "{}{}".format(thisDimensionValueName[0].lower(), thisDimensionValueName[1:])
              
              if thisDimensionValueName_upper in self.input_dict.keys() and thisDimensionValueName_upper != self.input_dict[thisDimensionValueName_upper]:
                dimensionValue_dict[thisDimensionValueName_upper] = self.input_dict[thisDimensionValueName_upper]
              elif thisDimensionValueName_lower in self.input_dict.keys() and thisDimensionValueName_lower != self.input_dict[thisDimensionValueName_lower]:
                dimensionValue_dict[thisDimensionValueName_lower] = self.input_dict[thisDimensionValueName_lower]
              else:
                logWarn("something wrong with dimensionKey[{}] at input_dict:[{}]".format(dimensionKey, self.input_dict))
          elif isinstance(self.input_dict["dimensions"], list):
            for dimentionItem_dict in self.input_dict["dimensions"]:
              if "name" in dimentionItem_dict.keys():
                dimensionValue_dict[dimentionItem_dict["name"]] = dimentionItem_dict["value"]
              elif "Name" in dimentionItem_dict.keys():
                dimensionValue_dict[dimentionItem_dict["Name"]] = dimentionItem_dict["Value"]
              #else:
                #pass
          else:
            if "name" in self.input_dict["dimensions"].keys():
              dimensionValue_dict[dimentionItem_dict["name"]] = dimentionItem_dict["value"]
            elif "Name" in self.input_dict["dimensions"].keys():
              dimensionValue_dict[dimentionItem_dict["Name"]] = dimentionItem_dict["Value"]
            #else:
              #pass
      except:
        logException("unable to parse dimensions:[{}]".format(self.input_dict["dimensions"]))
      '''
      
      for result_dict in result_list:
        if isinstance(result_dict, dict):
          if "timestamp" in result_dict.keys():
            result_dict["timestamp"] = getDateString(result_dict["timestamp"]/1000)
            
            thisResult_list.append(
              {
                "cwIndexKey": cwIndexKey,
                "serviceName_":self.input_dict[namespaceString].split("/")[-1],
                "apiName_":self.input_dict["apiName"], 
                "accountId_":self.input_dict["accountId"], 
                "regionCode_":self.input_dict["regionCode"],
                "resourceName_":None, 
                "namespace":self.input_dict[namespaceString], 
                "metricName":self.input_dict[metricNameString], 
                "period":self.input_dict[periodString], 
                **dimensionValue_dict,
                **result_dict
                }
                                    )   
          elif "Timestamp" in result_dict.keys():
            result_dict["Timestamp"] = "{}".format(result_dict["Timestamp"])
            
            thisResult_list.append(
              {
                "cwIndexKey": cwIndexKey,
                "serviceName_":self.input_dict[namespaceString].split("/")[-1],
                "apiName_":self.input_dict["apiName"], 
                "accountId_":self.input_dict["accountId"], 
                "regionCode_":self.input_dict["regionCode"], 
                "resourceName_":None,
                "namespace":self.input_dict[namespaceString], 
                "metricName":self.input_dict[metricNameString], 
                "period":self.input_dict[periodString], 
                **dimensionValue_dict,
                **result_dict
               }
              )        
    
    thisResult_list = self.updateResourceName(thisResult_list)
    
    return thisResult_list
  
  def getDynamoDBDescribeTable(self, result_dict):
    
    thisResult_list = []
    if "table" in result_dict.keys() and  "globalSecondaryIndexes" in result_dict["table"].keys():
      if isinstance(result_dict["table"]["globalSecondaryIndexes"], list):
        for globalSecondaryIndex_dict in result_dict["table"]["globalSecondaryIndexes"]:
          for key in result_dict["table"].keys():
            if key != "globalSecondaryIndexes":
              if key in globalSecondaryIndex_dict.keys():
                logWarn("key:[{}] is duplicated".format(key))
              else:
                globalSecondaryIndex_dict[key] = result_dict["table"][key]
            #else:
            #  pass
          thisResult_list.append(globalSecondaryIndex_dict)
        del result_dict["table"]["globalSecondaryIndexes"]
        thisResult_list.append(result_dict["table"])
      else:
        del result_dict["table"]["globalSecondaryIndexes"]
        thisResult_list.append(result_dict["table"])
                                                                                                                                                                  
    elif "Table" in result_dict.keys():
      if "GlobalSecondaryIndexes" in result_dict["Table"].keys():
        if isinstance(result_dict["Table"]["GlobalSecondaryIndexes"], list):
          for globalSecondaryIndex_dict in result_dict["Table"]["GlobalSecondaryIndexes"]:
            for key in result_dict["Table"].keys():
              if key != "GlobalSecondaryIndexes":
                if key in globalSecondaryIndex_dict.keys():
                  logWarn("key:[{}] is duplicated".format(key))
                else:
                  globalSecondaryIndex_dict[key] = result_dict["Table"][key]
              #else:
              #  pass
            thisResult_list.append(globalSecondaryIndex_dict)
          del result_dict["Table"]["GlobalSecondaryIndexes"]
          thisResult_list.append(result_dict["Table"])
        else:
          del result_dict["Table"]["GlobalSecondaryIndexes"]
          thisResult_list.append(result_dict["Table"])
      else:
        thisResult_list.append(result_dict["Table"])
    else:
      thisResult_list.append(result_dict)
      
    return thisResult_list
  
  def updateEpochTimeToDate(self, result_list):
    for result_dict in result_list:
      if isinstance(result_dict, dict):
        date_dict = {}
        for columnName in result_dict.keys():
          loweredColumnName = columnName.lower()
          if "time" in loweredColumnName and "time" in loweredColumnName[-4:]:
            if isinstance(result_dict[columnName], int) or isinstance(result_dict[columnName], float):
              if result_dict[columnName] >= 10000000000:
                date_dict["{}Date".format(columnName[:-4])] = getDateString(result_dict[columnName]/1000)
                if loweredColumnName in ["launchtime", "createdtime"]:
                  date_dict["age_d"] = float("{:.2f}".format((time.time() - result_dict[columnName]/1000)/86400))
              else:
                date_dict["{}Date".format(columnName[:-4])] = getDateString(result_dict[columnName])
                if columnName in ["launchTime", "createdTime"]:
                  date_dict["age_d"] = float("{:.2f}".format((time.time() - result_dict[columnName])/86400))
                
          elif "creat" in loweredColumnName and (loweredColumnName.find("date") > 0 or loweredColumnName.find("at") > 0):
            if isinstance(result_dict[columnName], int) or isinstance(result_dict[columnName], float):
              if result_dict[columnName] >= 10000000000:
                date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName]/1000)
                date_dict["age_d"] = float("{:.2f}".format((time.time() - result_dict[columnName]/1000)/86400))
              else:
                date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName])
                date_dict["age_d"] = float("{:.2f}".format((time.time() - result_dict[columnName])/86400))
            elif isinstance(result_dict[columnName], str) and ("T" in result_dict[columnName] or " " in result_dict[columnName]):
              try:
                date_dict["age_d"] = float("{:.2f}".format((time.time() - getDateString(result_dict[columnName], "epochtime"))/86400))
              except:
                logWarn("unexpected {}:[{}]".format(columnName, result_dict[columnName]))
            elif isinstance(result_dict[columnName], str) and len(result_dict[columnName]) > 0:
              if result_dict[columnName][0] == result_dict[columnName][0].lower() and result_dict[columnName][0] == result_dict[columnName][0].upper():
                try:
                  startTime_epoch = float(result_dict[columnName])
                  if startTime_epoch >= 10000000000:
                    date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName]/1000)
                    date_dict["age_d"] = float("{:.2f}".format((time.time() - startTime_epoch/1000)/86400))
                  else:
                    date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName])
                    date_dict["age_d"] = float("{:.2f}".format((time.time() - startTime_epoch)/86400))
                except:
                  logWarn("unexpected {}:[{}]".format(columnName, result_dict[columnName]))
            #else:
              #pass
                
          elif columnName in ["modifiedAt"]:
            if isinstance(result_dict[columnName], int) or isinstance(result_dict[columnName], float):
              if result_dict[columnName] >= 10000000000:
                date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName]/1000)
              else:
                date_dict["{}{}".format(columnName,"Date")] = getDateString(result_dict[columnName])

        for key in date_dict.keys():
          result_dict[key] = date_dict[key]
        
    return result_list
          
  def unpackSingleList(self, result, depth = 0):
    #logDebug("#{}:type:{}:[{}]".format(depth, type(result), result))
    
    thisResult = result
    if isinstance(result, dict):
      listTypeKey_list = []
      otherTypeKey_list = []
      for key in result.keys():
        if isinstance(result[key], list):
          if len(result[key]) > 0:
            listTypeKey_list.append(key)
        else:
          otherTypeKey_list.append(key)
          
      if len(listTypeKey_list) == 1 and len(result[listTypeKey_list[0]]) and isinstance(result[listTypeKey_list[0]][0], dict):
        thisResult = []
        firstResulttResult_list = result[listTypeKey_list[0]]
        for resultItem in firstResulttResult_list:
          for key in otherTypeKey_list:
            resultItem[key] = result[key]
            
          thisResult.append(resultItem)
      else:
        thisResult = result
    
    #logDebug("#{}:type:{}:[{}]".format(depth, type(thisResult), thisResult))
    
    return thisResult
  
  def unpackSingleDict(self, result, depth = 0):
    #logDebug("#{}:type:{}:[{}]".format(depth, type(result), result))
    
    thisResult = result
    if isinstance(result, dict) and len(result.keys()) == 1:
      for key in result.keys():
        thisResult = result[key]
      #else:
      #  thisResult = result
    
    #logDebug("#{}:type:{}:[{}]".format(depth, type(thisResult), thisResult))
    
    return thisResult
          
          
        
  def parseResults(self, result = None):
    #logDebug("original result:[{}]".format(printValue(result)))
    #logDebug("#original result:[{}]".format(result))
    
    if isinstance(result, dict):
      #nextTokenKeyword_list = ["nextToken", "NextToken", "marker", "Marker", "paginationToken", "PaginationToken", "lastEvaluatedTableName", "LastEvaluatedTableName"]
      for nextTokenKeyword in nextTokenKeyword_list:
        if nextTokenKeyword in result.keys():
          #logDebug("nextTokenKeyword:[{}] is deleted".format(result[nextTokenKeyword]))
          del result[nextTokenKeyword]
          
    thisResult = self.serializedJson(self.unpackSingleList(self.unpackSingleDict(result)))
    
    thisPrimaryKey_list = []
    #logDebug("#primaryKey_list:[{}]".format(self.primaryKey_list))
    for primaryKey in self.primaryKey_list:
      stripedPrimaryKey = primaryKey.strip()
      if len(stripedPrimaryKey) > 2:
        if primaryKey in thisPrimaryKey_list:
          pass
        else:
          thisPrimaryKey_list.append("{}{}".format(stripedPrimaryKey[0].lower(), stripedPrimaryKey[1:]))
          thisPrimaryKey_list.append("{}{}".format(stripedPrimaryKey[0].upper(), stripedPrimaryKey[1:]))
    #logDebug("#primaryKeys->thisPrimaryKey_list:[{}]".format(thisPrimaryKey_list))
    
    for thisPrimaryKey in thisPrimaryKey_list:
      #logDebug("#primaryKeys:thisPrimaryKey:[{}]->before result:[{}]".format(thisPrimaryKey, thisResult))
      if "tags" == thisPrimaryKey:
        if isinstance(thisResult, dict):
          thisResult = [thisResult]
          
        for thisResultItem_dict in thisResult:
          #logWarn("#primaryKeys:======>thisResultItem_dict:type:[{}]:[{}]".format(type(thisResultItem_dict), thisResultItem_dict))
          if isinstance(thisResultItem_dict, str):
            try:
              thisResultItem_dict = json.loads(thisResultItem_dict)
            except:
              logException("unexpected thisResultItem_dict:[{}] with payload:[{}]".format(thisResultItem_dict, self.payload_dict))
              thisResultItem_dict = {}
              
          if thisPrimaryKey in thisResultItem_dict.keys() and thisResultItem_dict[thisPrimaryKey] != None:
            #logDebug("#primaryKeys:======>thisResultItem_dict[{}]:type:[{}]:[{}]".format(thisPrimaryKey, type(thisResultItem_dict[thisPrimaryKey]), thisResultItem_dict[thisPrimaryKey]))
            try:
              if isinstance(thisResultItem_dict[thisPrimaryKey], dict):
                for tagKeyname in  thisResultItem_dict[thisPrimaryKey].keys():
                  thisResultItem_dict["tag/{}".format(tagKeyname)] = thisResultItem_dict[thisPrimaryKey][tagKeyname]
                
                del thisResultItem_dict[thisPrimaryKey]
              
              elif isinstance(thisResultItem_dict[thisPrimaryKey], list):  
                if len(thisResultItem_dict[thisPrimaryKey]) > 0 and "value" in thisResultItem_dict[thisPrimaryKey][0].keys():
                  for tagItem_dict in thisResultItem_dict[thisPrimaryKey]:
                    thisResultItem_dict["tag/{}".format(tagItem_dict["key"])] = tagItem_dict["value"]
                else:
                  for tagItem_dict in thisResultItem_dict[thisPrimaryKey]:
                    thisResultItem_dict["tag/{}".format(tagItem_dict["Key"])] = tagItem_dict["Value"]
                    
                del thisResultItem_dict[thisPrimaryKey]
              
              else:
                logWarn("unexpected tags:[{}]".format(thisResultItem_dict[thisPrimaryKey]))
            except:
                logException("unable to unpack tags:[{}]".format(thisResultItem_dict[thisPrimaryKey]))
            
      elif "dimensions" == thisPrimaryKey:
        if isinstance(thisResult, dict):
          thisResult = [thisResult]
          
        for thisResultItem_dict in thisResult:
          #logDebug("#primaryKeys:======>thisResultItem_dict:type:[{}]:[{}]".format(type(thisResultItem_dict), thisResultItem_dict))
          if isinstance(thisResultItem_dict, str):
            if len(thisResultItem_dict) >= 2 and thisResultItem_dict[0] in ["[", "{"] and thisResultItem_dict[0] in ["]", "}"]:
              try:
                thisResultItem_dict = json.loads(thisResultItem_dict)
              except:
                logException("unexpected thisResultItem_dict:[{}]".format(thisResultItem_dict))
                continue
              
            else:
              continue
            
          #else:
          #  pass
            
              
          if isinstance(thisResultItem_dict, dict) and thisPrimaryKey in thisResultItem_dict.keys() and thisResultItem_dict[thisPrimaryKey] != None:
            #logDebug("#primaryKeys:======>thisResultItem_dict[{}]:type:[{}]:[{}]".format(thisPrimaryKey, type(thisResultItem_dict[thisPrimaryKey]), thisResultItem_dict[thisPrimaryKey]))
            try:
              if len(thisResultItem_dict[thisPrimaryKey]) > 0 and "value" in thisResultItem_dict[thisPrimaryKey][0].keys():
                for dimensionItem_dict in thisResultItem_dict[thisPrimaryKey]:
                  thisResultItem_dict["dimension/{}".format(dimensionItem_dict["name"])] = dimensionItem_dict["value"]
              else:
                for dimensionItem_dict in thisResultItem_dict[thisPrimaryKey]:
                  thisResultItem_dict["dimension/{}".format(dimensionItem_dict["Name"])] = dimensionItem_dict["Value"]
              
              try:
                if "listMetrics" not in self.payload_dict["apiName"]:
                  del thisResultItem_dict[thisPrimaryKey]
              except:
                logException("unexepcteed payload_dict:[{}]".format(self.payload_dict))
                del thisResultItem_dict[thisPrimaryKey]
            except:
              logException("unable to unpack dimensions:[{}]".format(thisResultItem_dict[thisPrimaryKey]))
                          
              
      else:
        #logDebug("#primaryKeys:thisPrimaryKey:[{}]->type:[{}]:thisResult:[{}]".format(thisPrimaryKey, type(thisResult), thisResult))
        
        if isinstance(thisResult, dict):
          #logDebug("#primaryKeys:hisPrimaryKey:[{}]->thisResult:type:[{}](len:{:,}):[{}]".format(type(thisResult), len(thisResult.keys()), thisResult.keys()))
          if thisPrimaryKey in thisResult.keys():
            
            thisPrimaryValue = thisResult[thisPrimaryKey]
            del thisResult[thisPrimaryKey]
            #logDebug("#primaryKeys:thisPrimaryValue:type:[{}]:[{}]".format(type(thisPrimaryValue), thisPrimaryValue))
            
            if isinstance(thisPrimaryValue, str) and len(thisPrimaryValue) > 4 and thisPrimaryValue[0] in ["[", "{"] and thisPrimaryValue[-1] in ["}", "]"]: 
              try:
                thisPrimaryValue = json.loads(thisPrimaryValue)
              except:
                logException("unable to load json with thisPrimaryValue:[{}]".format(thisPrimaryValue))
                
            if isinstance(thisPrimaryValue, dict):
              # type -> dict
              #logDebug("#primaryKeys:thisResult:type:[{}]:[{}]".format(type(thisPrimaryValue), thisPrimaryValue.keys()))
              
              thisResult = {**thisResult, **thisPrimaryValue}
            elif isinstance(thisPrimaryValue, list):
              # type -> list
              #logDebug("#primaryKeys:thisResult:type:[{}]:[len:{:,}]".format(type(thisPrimaryValue), len(thisPrimaryValue)))
              
              newResult = []
              pCount = 0
              for thisPrimaryValueItem in thisPrimaryValue:
                if isinstance(thisPrimaryValueItem, dict):
                  #logInfo("type:{}:thisPrimaryValueItem.keys(len:{:,}):[{}]".format(type(thisPrimaryValueItem), len(thisPrimaryValueItem.keys()), thisPrimaryValueItem))
                  primaryValue_dict = {}
                  for thisKey in thisPrimaryValueItem.keys():
                    if isinstance(thisPrimaryValueItem[thisKey], dict):
                      for thisSubKey in thisPrimaryValueItem[thisKey].keys():
                        primaryValue_dict["{}/{}".format(thisKey,thisSubKey)] = thisPrimaryValueItem[thisKey][thisSubKey]
                    else:
                      primaryValue_dict[thisKey] = thisPrimaryValueItem[thisKey]
                      
                  newResult.append({**thisResult, "{}_".format(thisPrimaryKey):pCount, **primaryValue_dict})
                else:
                  newResult.append({**thisResult, "{}_".format(thisPrimaryKey):pCount, thisPrimaryKey:thisPrimaryValueItem})
                pCount += 1
            
              thisResult = newResult
              
            else:
              if thisPrimaryKey == "eventArns":
                try:
                  thisPrimaryValue = json.loads(thisPrimaryValue)
                except:
                  logException("unable to load json with thisPrimaryValue:[{}]".format(thisPrimaryValue))
              # type -> others
              #logDebug("#primaryKeys:thisResult:type:[{}]:[len:{:,}]".format(type(thisPrimaryValue), len(thisPrimaryValue)))
              
              thisResult = {**thisResult, thisPrimaryKey:thisPrimaryValue}
              
            
        elif isinstance(thisResult, list):
          #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisResult:type:[{}](len:{:,})".format(thisPrimaryKey, type(thisResult), len(thisResult)))
          
          thisNewResult_list = []
          for thisResultItem in thisResult:
            #if "instances" in thisResultItem.keys():
            #  logDebug("#primaryKeys:hisPrimaryKey:[{}]->type:[{}]:thisResultItem:[{}]".format(thisPrimaryKey, type(thisResultItem), thisResultItem))
            
            if isinstance(thisResultItem, dict) and thisPrimaryKey in thisResultItem.keys():
              #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisResult:type:[{}]:[{}]".format(thisPrimaryKey, type(thisResultItem), thisResultItem.keys()))
            
              thisPrimaryValue = thisResultItem[thisPrimaryKey]
              del thisResultItem[thisPrimaryKey]
              #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisPrimaryValue:type:[{}]:[{}]".format(thisPrimaryKey, type(thisPrimaryValue), thisPrimaryValue))
              
              if isinstance(thisPrimaryValue, str) and len(thisPrimaryValue) > 4 and thisPrimaryValue[0] in ["[", "{"] and thisPrimaryValue[-1] in ["}", "]"]: 
                try:
                  thisPrimaryValue = json.loads(thisPrimaryValue)
                except:
                  logException("unable to load json with thisPrimaryValue:[{}]".format(thisPrimaryValue))
              #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisPrimaryValue:type:[{}]:[{}]".format(thisPrimaryKey, type(thisPrimaryValue), thisPrimaryValue))
              
              #if isinstance(thisPrimaryValue, str) and len(thisPrimaryValue) > 4:
              #  thisPrimaryValue = thisPrimaryValue.strip()
              #  
              #  
              #  if thisPrimaryValue[0] == "[" and thisPrimaryValue[-1] == "]":
              #    if len(thisPrimaryValue[1:-1]) > 2 and thisPrimaryValue[1] in ["{", "["]:
              #      try:
              #        thisPrimaryValue = json.loads(thisPrimaryValue[1:-1])
              #      except:
              #        logException("unexpected thisPrimaryValue:[{}]".format(thisPrimaryValue))
              #    else:
              #      thisPrimaryValue = thisPrimaryValue[1:-1]
              #  elif thisPrimaryValue[0] == "{" and thisPrimaryValue[-1] == "}":
              #    try:
              #      thisPrimaryValue = json.loads(thisPrimaryValue)
              #   except:
              #      logException("unexpected thisPrimaryValue:[{}]".format(thisPrimaryValue))
              
              if isinstance(thisPrimaryValue, dict):
                if len(thisResultItem.keys()) <= 1:
                  # type -> dict
                  #logDebug("#primaryKeys:thisResult:type:[{}]:[{}]".format(type(thisPrimaryValue), thisPrimaryValue.keys()))
                  
                  thisNewResult_list.append({**thisResultItem, **thisPrimaryValue})
                else:
                  #logInfo("#thisPrimaryKey:[{}]->thisResult:type:[{}]:[{}]".format(type(thisPrimaryValue), thisPrimaryValue.keys()))
                  primaryValue_dict = {}
                  for thisKey in thisPrimaryValue.keys():
                    if isinstance(thisPrimaryValue[thisKey], dict):
                      for thisSubKey in thisPrimaryValue[thisKey].keys():
                        primaryValue_dict["{}/{}/{}".format(thisPrimaryKey, thisKey, thisSubKey)] = thisPrimaryValue[thisKey][thisSubKey]
                    else:
                      primaryValue_dict["{}/{}".format(thisPrimaryKey,thisKey)] = thisPrimaryValue[thisKey]
                      
                  thisNewResult_list.append({**thisResultItem, **primaryValue_dict})
                
              elif isinstance(thisPrimaryValue, list):
                # type -> list
                #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisResult:type:[{}]:[len:{:,}]".format(thisPrimaryKey, type(thisPrimaryValue), len(thisPrimaryValue)))
                
                if len(thisPrimaryValue) == 0:
                  thisNewResult_list.append({**thisResultItem, thisPrimaryKey:""})
                elif len(thisPrimaryValue) == 1:
                  if isinstance(thisPrimaryValue[-1], dict):
                    thisNewResult_list.append({**thisResultItem, **thisPrimaryValue[-1]})
                  elif isinstance(thisPrimaryValue[-1], list):
                    if len(thisPrimaryValue[-1]) == 0:
                      thisNewResult_list.append({**thisResultItem, thisPrimaryKey:None})
                    elif len(thisPrimaryValue[-1]) == 1:
                      thisNewResult_list.append({**thisResultItem, thisPrimaryKey:thisPrimaryValue[-1]})
                    else:
                      newResult = []
                      pCount = 0
                      for thisPrimaryValueItem in thisPrimaryValue[-1]:
                        if isinstance(thisPrimaryValueItem, dict):
                          logDebug("#primaryKeys:type:{}:thisPrimaryValueItem.keys(len:{:,}):[{}]".format(type(thisPrimaryValueItem), len(thisPrimaryValueItem.keys()), thisPrimaryValueItem))
                          primaryValue_dict = {}
                          for thisKey in thisPrimaryValueItem.keys():
                            if isinstance(thisPrimaryValueItem[thisKey], dict):
                              for thisSubKey in thisPrimaryValueItem[thisKey].keys():
                                primaryValue_dict["{}/{}".format(thisKey,thisSubKey)] = thisPrimaryValueItem[thisKey][thisSubKey]
                            else:
                              primaryValue_dict[thisKey] = thisPrimaryValueItem[thisKey]
                              
                          thisNewResult_list.append({**thisResultItem, "{}_".format(thisPrimaryKey):pCount, **primaryValue_dict})
                        else:
                          thisNewResult_list.append({**thisResultItem, "{}_".format(thisPrimaryKey):pCount, thisPrimaryKey:thisPrimaryValueItem})
                        pCount += 1
                  
                else:
                  newResult = []
                  pCount = 0
                  for thisPrimaryValueItem in thisPrimaryValue:
                    if isinstance(thisPrimaryValueItem, dict):
                      #logDebug("#primaryKeys:type:{}:thisPrimaryValueItem.keys(len:{:,}):[{}]".format(type(thisPrimaryValueItem), len(thisPrimaryValueItem.keys()), thisPrimaryValueItem))
                      primaryValue_dict = {}
                      for thisKey in thisPrimaryValueItem.keys():
                        if isinstance(thisPrimaryValueItem[thisKey], dict):
                          for thisSubKey in thisPrimaryValueItem[thisKey].keys():
                            primaryValue_dict["{}/{}".format(thisKey,thisSubKey)] = thisPrimaryValueItem[thisKey][thisSubKey]
                        else:
                          primaryValue_dict[thisKey] = thisPrimaryValueItem[thisKey]
                          
                      thisNewResult_list.append({**thisResultItem, "{}_".format(thisPrimaryKey):pCount, **primaryValue_dict})
                    else:
                      thisNewResult_list.append({**thisResultItem, "{}_".format(thisPrimaryKey):pCount, thisPrimaryKey:thisPrimaryValueItem})
                    pCount += 1
              
              else:
                # type -> others
                #logDebug("#primaryKeys:thisResult:type:[{}]:[len:{:,}]".format(type(thisPrimaryValue), len(thisPrimaryValue)))
                
                thisNewResult_list.append({**thisResultItem, thisPrimaryKey:thisPrimaryValue})
                    
              
            elif isinstance(thisResultItem, list):
              #logDebug("#primaryKeys:thisResultItem:type:[{}](len:{:,})".format(type(thisResultItem), len(thisResultItem)))
              for subResultItem in thisResultItem:
                thisNewResult_list.append(subResultItem)
            else:
              #logDebug("#primaryKeys:thisResultItem:type:[{}](len:{:,})".format(type(thisResultItem), len(thisResultItem)))
              thisNewResult_list.append(thisResultItem)
          thisResult = thisNewResult_list
        else:
          #logDebug("#primaryKeys:thisPrimaryKey:[{}]->thisResult:type:[{}]:[{}]".format(thisPrimaryKey, type(thisResult), thisResult))
          
          thisResult = thisResult
            
        #end if isinstance(thisResult, dict):
      
      #logDebug("#primaryKeys:thisPrimaryKey:[{}]->parsed result:[{}]".format(thisPrimaryKey, printValue(thisResult)))
      #logDebug("#primaryKeys:tthisPrimaryKey:[{}]->after result:[{}]".format(thisPrimaryKey, thisResult))
    
    
    #logDebug("#primaryKeys:ype:{}:thisResult(len:{:,}):[{}]".format(type(thisResult), len(thisResult), thisResult))
    #end for thisPrimaryKey in self.primaryKey_list:
    
    return thisResult