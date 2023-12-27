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
from graphcode.conf import getSessionKey

from graphcode.conf import getPathwayHost, getPathwayPort, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode, getPathwayDebugMode
from graphcode.conf import getPathwayMethod, getPathwayRule
from graphcode.conf import getPathwaySSLMode, getPathwaySSLCert, getPathwaySSLKey
from graphcode.conf import getPathwayStaticPath, getPathwayTemplatesPath

from graphcode.path import listDir

from graphcode.itemDB import GcItemDB

from graphcode.lib import getDateString

from os import getcwd
from os.path import dirname, exists, join, abspath, expanduser

from getpass import getuser

from flask import Flask, Response, request

import requests as pyRequests

import time
import json

import inspect

from uuid import uuid4

# Function to start Flask app with SSL and debug mode
def start():
  initItemDBTables()

  if getPathwayStaticPath() is None:
    staticPath = join(join(dirname(__file__), "pathway", "__static__"))
  else:
      staticPath = getPathwayStaticPath()

  if getPathwayTemplatesPath() is None:
    templatesPath = join(join(dirname(__file__), "pathway", "__static__"))
  else:
      templatesPath = getPathwayTemplatesPath()

  pathwayApp = Flask(
    name="pathway",
    static_folder=staticPath,
    template_folder=templatesPath
    )

  pathwayApp.add_url_rule(rule = getPathwayRule(), methods=getPathwayMethod(), view_func = response)

  if getPathwaySSLMode():
    if exists(expanduser(getPathwaySSLCert())) and exists(expanduser(getPathwaySSLKey())):
      context = (expanduser(getPathwaySSLCert()), expanduser(getPathwaySSLKey()))
      logDebug(f"SSL Context:{context}")
      pathwayApp.run(host=getPathwayHost(), port=getPathwayPort(), debug=getPathwayDebugMode(), ssl_context=context)

    else:
      logDebug("pathway:adhoc ssl")
      pathwayApp.run(host=getPathwayHost(), port=getPathwayPort(), debug=getPathwayDebugMode(), ssl_context='adhoc')
  else:
    pathwayApp.run(host=getPathwayHost(), port=getPathwayPort(), debug=getPathwayDebugMode())


def updateStateToResponse(response_dict, state, message):
  state_list = ['NOT IMPLEMENTED','INVALID REQUEST','TOO MANY REQUESTS',
                'PERMISSION DENIED','OPERATION NOT PERMITTED',
                'QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED',
                'UNEXPECTED ERROR', 'INVALID MIDWAY']
  if state in state_list:
    response_dict["state"] = state
    
    if "errorReasons" in response_dict.keys():
      response_dict["errorReasons"].append(message)
    
    else:
      response_dict["errorReasons"] = [message]
  else:
    logError("state:[{}] must be in [{}]".format(state, state_list))
    
  return response_dict
  
def updateMsg(msg_list, errMsg):
  countI = 0
  for stackItem_list in inspect.stack():
    if stackItem_list[3] != "updateMsg":
      break
    #print("{}:[{}]".format(-countI, inspect.stack()[countI][3]))
    countI += 1
  
  #logDebug(#errMsg)
  
  if isinstance(errMsg, str):
    msg_list.append(
      {
        "#":len(msg_list) + 1,
        "time": getDateString("now"),
        "module": "{}:{}".format(inspect.stack()[countI][1][len(abspath("."))+1:], inspect.stack()[countI][2]),
        "function": inspect.stack()[countI][3],
        "message": "{}".format(errMsg)
        }
      )
  elif isinstance(errMsg, dict):
    msg_list.append(
      {
        "#":len(msg_list) + 1,
        "time": getDateString("now"),
        "module": "{}:{}".format(inspect.stack()[countI][1][len(abspath("."))+1:], inspect.stack()[countI][2]),
        "function": inspect.stack()[countI][3],
        **errMsg
        }
      )
  elif isinstance(errMsg, list):
    for thisErrMsg in errMsg:
      msg_list.append(
        {
          "#":len(msg_list) + 1,
          "time": getDateString("now"),
          "module": "{}:{}".format(inspect.stack()[countI][1][len(abspath("."))+1:], inspect.stack()[countI][2]),
          "function": inspect.stack()[countI][3],
          "message": "{}".format(thisErrMsg)
          }
        )
  elif isinstance(errMsg, dict) and "errorReason" in errMsg.keys():
    updateMsg(msg_list, errMsg)
  #else:
  #  logDebug("no error")
  
  if isinstance(errMsg, dict) and "errorReason" in errMsg.keys():
    del errMsg["errorReason"]
  
  return msg_list

def aggregateMsg(result_dict, errorReason_list, logMessage_list):
  errorReason_list = consolidateErrorReasons(errorReason_list, result_dict)
  logMessage_list = consolidateLogMessages(logMessage_list, result_dict)
  
  return errorReason_list, logMessage_list

def consolidateErrorReasons(errorReason_list, result_dict):
  countI = 0
  for stackItem_list in inspect.stack():
    if stackItem_list[3] != "consolidateErrorReasons":
      break
    #print("{}:[{}]".format(-countI, inspect.stack()[countI][3]))
    countI += 1
  
  for key in ["error", "errors", "errorReason", "errorReasons"]:
    if key in result_dict.keys():
        
      for messageItem_dict in result_dict[key]:
        if isinstance(messageItem_dict, dict):
          errorReason_list.append(
            {
              "_f.{}".format(len(messageItem_dict.keys())): inspect.stack()[countI][3],
              **messageItem_dict
              }
            )
        
        elif isinstance(messageItem_dict, list):
          for thisMessage in messageItem_dict:
            errorReason_list.append(
              {
                "_f.1": inspect.stack()[countI][3],
                "errorResaon": thisMessage
                }
              )
        else:
          errorReason_list.append(
            {
              "_f.1": inspect.stack()[countI][3],
              "errorResaon": messageItem_dict
              }
            )
      
      del result_dict[key]
    
  return errorReason_list

def consolidateLogMessages(logMessage_list, result_dict):
  countI = 0
  for stackItem_list in inspect.stack():
    if stackItem_list[3] != "consolidateLogMessages":
      break
    #print("{}:[{}]".format(-countI, inspect.stack()[countI][3]))
    countI += 1
  
  for key in ["log", "logs", "logMessage", "logMessages"]:
    if key in result_dict.keys():
      
      for messageItem_dict in result_dict[key]:
        if isinstance(messageItem_dict, dict):
          logMessage_list.append(
            {
              "_f.{}".format(len(messageItem_dict.keys())): inspect.stack()[countI][3],
              **messageItem_dict
              }
            )
        
        elif isinstance(messageItem_dict, list):
          for thisMessage in messageItem_dict:
            logMessage_list.append(
              {
                "_f.1": inspect.stack()[countI][3],
                "message": thisMessage
                }
              )
        else:
          logMessage_list.append(
            {
              "_f.1": inspect.stack()[countI][3],
              "message": messageItem_dict
              }
            )
      
      del result_dict[key]
    
  return logMessage_list

def consolidateMsg(result_dict, errorReason_list, logMessage_list):
  thisLogMessage_list = consolidateLogMessages(logMessage_list, result_dict)
  thisErrorReason_list = consolidateErrorReasons(errorReason_list, result_dict)

  return {
    "errorReasons": thisErrorReason_list,
    "logMessages": thisLogMessage_list
  }

def initItemDBTables():
  itemDB = GcItemDB()
  
  try:
    tammy =  __import__("tammy")
    logDebug("tammy:[{}]".format(tammy.__file__))
    for dirName in listDir(dirPath=dirname(tammy.__file__), type="dir"):
      if dirName.startswith("__"):
        continue
      
      #logDebug("#dirName:[{}]".format(dirName))
      itemDB.createTable(dirName)
  except:
    logException("unexpected error")

  try:
    wooju =  __import__("tammy")
    logDebug("tammy:[{}]".format(tammy.__file__))
    for dirName in listDir(dirPath=dirname(tammy.__file__), type="dir"):
      if dirName.startswith("__"):
        continue
      
      #logDebug("#dirName:[{}]".format(dirName))
      itemDB.createTable(dirName)
  except:
    logException("unexpected error")

def requests(request_dict, thisUrl="https://localhost:8000/", verify=False):
  try:
    if "__beginTime__" not in request_dict.keys():
      request_dict["__beginTime__"] = time.time()
    else:
      logDebug("__beginTime__:[{}] is already provided".format(request_dict["__beginTime__"]))
    
    if "sessionToken" not in request_dict.keys():
      request_dict["sessionToken"] = getSessionKey()
      
    if False:
      key3Count = 0
      for key in request_dict.keys():
        if isinstance(request_dict[key],dict):
          for key2 in request_dict[key].keys():
            if isinstance(request_dict[key][key2],dict):
              for key3 in request_dict[key][key2].keys():
                if isinstance(request_dict[key][key2][key3], dict) and len(request_dict[key][key2][key3].keys()) > 0:
                  for key4 in request_dict[key][key2][key3].keys():
                    logDebug("{}.{}.{}.{}:[{}]".format(key, key2, key3, key4, request_dict[key][key2][key3][key4]))
                elif isinstance(request_dict[key][key2][key3], list) and len(request_dict[key][key2][key3]) > 0:
                  if isinstance(request_dict[key][key2][key3][-1], dict) and len(request_dict[key][key2][key3][-1].keys()) > 0:
                    for key4 in request_dict[key][key2][key3][-1].keys():
                      logDebug("{}.{}.{}(len:{:,})[-1].{}:[{}]".format(key, key2, key3, len(request_dict[key][key2][key3]), key4, request_dict[key][key2][key3][-1][key4]))
                  else:
                    logDebug("{}.{}.{}(len:{:,})[-1]:[{}]".format(key, key2, key3, len(request_dict[key][key2][key3]), request_dict[key][key2][key3][-1]))
                else:
                  logDebug("{}.{}.{}:[{}]".format(key, key2, key3, request_dict[key][key2][key3]))
                  if key3Count > 100:
                    break
                  else:
                    key3Count += 1
            else:
              logDebug("{}.{}:[{}]".format(key, key2, request_dict[key][key2]))
        else:
          logDebug("{}:[{}]".format(key, request_dict[key]))
    try:    
      headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        }
      r = pyRequests.post(thisUrl, headers = headers, json = request_dict, verify=verify)

      try:
        response_dict = r.json()
        response_dict["__endTime__"] = time.time()
        response_dict["__responseTime__"] = response_dict["__endTime__"] - request_dict["__beginTime__"]
        
      except Exception as e:
        response_dict = {
          "results":r,
          "response":{"error":[{"error":logError("unexpected connection error:[{}]".format(e))}]},
          "errorReasons":[logException("uanble to load json")],
          "__beginTime__": request_dict["__beginTime__"],
          "__endTime__": time.time()
          }
        response_dict["__responseTime__"] = response_dict["__endTime__"] - request_dict["__beginTime__"]
        
    except Exception as e:
      response_dict = {
        "request": request_dict,
        "url":thisUrl,
        "response":{"error":[{"error":logError("unexpected connection error:[{}]".format(e))}]},
        "errorReasons":[logException("uable to request")],
        "__beginTime__": request_dict["__beginTime__"],
        "__endTime__": time.time()
        }
      response_dict["__responseTime__"] = response_dict["__endTime__"] - request_dict["__beginTime__"]
    
  except:
    response_dict = {
      "request": request_dict,
      "url":thisUrl,
      "response":{"error":[{"error":logError("unexpected connection error:[{}]".format(e))}]},
      "errorReasons":[logException("uable to request")],
      "__beginTime__": request_dict["__beginTime__"],
      "__endTime__": time.time()
      }
    response_dict["__responseTime__"] = response_dict["__endTime__"] - request_dict["__beginTime__"]
    
  return response_dict
  
def response():
  __processEndTime__ = 0
  __processBeginTime__ = time.time()
  __requestId__ = "{}".format(uuid4())
  
  if request.method == 'POST':
    try:
      request_dict = request.get_json(force=True)
      #logDebug("#apiName:[{}]->request_dict.keys():[{}]".format(request_dict["apiName"], request_dict.keys()))
      
      if "sessionToken" in request_dict.keys():
        if request_dict["sessionToken"] in [getSessionKey()]:
          request_dict["__processBeginTime__"] = __processBeginTime__
          request_dict["__requestId__"] = __requestId__
          request_dict["__cookies__"] = request.cookies
          #logDebug("#apiName:[{}]->request_dict.keys():[{}]".format(request_dict["apiName"], request_dict.keys()))
          
          response_dict = route(request_dict)
          #logDebug("#apiName:[{}]->request_dict.keys():[{}]".format(request_dict["apiName"], request_dict.keys()))
        else:
          response_dict = updateStateToResponse(response_dict={}, 
                                                state="PERMISSION DENIED", 
                                                message=logError("invalid sessionToken")
                                                )
      else:
        response_dict = updateStateToResponse(response_dict={}, 
                                              state="INVALID REQUEST", 
                                              message=logError("'sessionToken' not found")
                                              )
            
    except:
      response_dict = updateStateToResponse(response_dict={}, 
                                            state="INVALID REQUEST", 
                                            message=logException("unable to load json")
                                            )
    
  else:
    raiseValueError("Method:[{}] Not Allowed".format(request.method))
  
  if "state" in response_dict.keys() and response_dict["state"] in ["INVALID REQUEST", "PERMISSION DENIED"]:
    if request.content_length > 1024:
      response_dict["responseMetadata"] = {
        "method": request.method,
        "requestId": __requestId__,
        "request": "{}....{}".format(request.data[:512], request.data[-512:]),
        "requqestSize": request.content_length,
        "processBeginTime": __processBeginTime__,
        "processEndTime": time.time(),
        "snapshotTime": getDateString(__processBeginTime__)
        }
    else:
      response_dict["responseMetadata"] = {
        "method": request.method,
        "requestId": __requestId__,
        "request": "{}".format(request.data),
        "requqestSize": request.content_length,
        "processBeginTime": __processBeginTime__,
        "processEndTime": time.time(),
        "snapshotTime": getDateString(__processBeginTime__)
        }
  elif "state" in response_dict.keys() and response_dict["state"] in ["FAILED"]:
    response_dict["responseMetadata"] = {
      "method": request.method,
      "requestId": __requestId__,
      "request": request_dict,
      "requqestSize": request.content_length,
      "processBeginTime": __processBeginTime__,
      "processEndTime": time.time(),
      "snapshotTime": getDateString(__processBeginTime__)
      }
    
  else:
    response_dict["responseMetadata"] = {
      "method": request.method,
      "requestId": __requestId__,
      "request": "...redacted...",
      "requqestSize": request.content_length,
      "processBeginTime": __processBeginTime__,
      "processEndTime": time.time(),
      "snapshotTime": getDateString(__processBeginTime__)
      }
    
  #if "apiName" in response_dict.keys():
  #  logDebug("apiName:[{}]\ttype:[{}]:response_dict.keys():[{}]".format(response_dict["apiName"], type(response_dict), response_dict.keys()))
  #else:
  #  if isinstance(response_dict, dict):
  #    logDebug("type:[{}]:response_dict.keys():[{}]".format(type(response_dict), response_dict.keys()))
  #  else:
  #    logDebug("type:[{}]:response_dict:[{}]".format(type(response_dict), response_dict))
    
  if False and isinstance(response_dict, dict):
    
    key3Count = 0
    key4Count = 0
    key5Count = 0
    for key in response_dict.keys():
      if isinstance(response_dict[key],dict):
        for key2 in response_dict[key].keys():
          if isinstance(response_dict[key][key2],dict):
            for key3 in response_dict[key][key2].keys():
              if isinstance(response_dict[key][key2][key3], dict) and len(response_dict[key][key2][key3].keys()) > 0:
                for key4 in response_dict[key][key2][key3].keys():
                  if isinstance(response_dict[key][key2][key3][key4], dict) and len(response_dict[key][key2][key3][key4].keys()) > 10:
                    for key5 in response_dict[key][key2][key3][key4].keys():
                      logDebug("{}.{}.{}.{}.{}:[{}]".format(key, key2, key3, key4, key5, response_dict[key][key2][key3][key4][key5]))
                      
                      if key5Count > 10:
                        logDebug("{}.{}.{}.{}:[..........](len:{:,})".format(key, key2, key3, key4, len(response_dict[key][key2][key3][key4].keys())))
                        break
                      else:
                        key5Count += 1
                        
                  else:
                    logDebug("{}.{}.{}.{}:[{}]".format(key, key2, key3, key4, response_dict[key][key2][key3][key4]))
                  
                  if key4Count > 100:
                    break
                  else:
                    key4Count += 1
                    
              elif isinstance(response_dict[key][key2][key3], list) and len(response_dict[key][key2][key3]) > 0:
                if isinstance(response_dict[key][key2][key3][-1], dict) and len(response_dict[key][key2][key3][-1].keys()) > 0:
                  for key4 in response_dict[key][key2][key3][-1].keys():
                    logDebug("{}.{}.{}(len:{:,})[-1].{}:[{}]".format(key, key2, key3, len(response_dict[key][key2][key3]), key4, response_dict[key][key2][key3][-1][key4]))
                else:
                  logDebug("{}.{}.{}(len:{:,})[-1]:[{}]".format(key, key2, key3, len(response_dict[key][key2][key3]), response_dict[key][key2][key3][-1]))
              else:
                logDebug("{}.{}.{}:[{}]".format(key, key2, key3, response_dict[key][key2][key3]))
                
                if key3Count > 100:
                  break
                else:
                  key3Count += 1
          elif isinstance(response_dict[key][key2], list) and len(response_dict[key][key2]) > 0:
            logDebug("{}.{}(len:{:,})[-1]:[{}]".format(key, key2, len(response_dict[key][key2]), response_dict[key][key2][-1]))
          else:
            logDebug("{}.{}:[{}]".format(key, key2, response_dict[key][key2]))
      else:
        logDebug("{}:[{}]".format(key, response_dict[key]))
  
  try:
    resp = Response(response=json.dumps(response_dict), status=200, mimetype="application/json")
  except:
    response_dict = {
      "apiName": request_dict["apiName"],
      "state":"FAILED",
      "errorReasons":[logException("apiName:[{}] failed {}:response_dict.keys(len:{:,}):[{}]".format(request_dict["apiName"], type(response_dict).__name__, len(response_dict.keys()), response_dict.keys()))],
      "__file__": __file__
      }
    
    for key in response_dict.keys():
      try:
        json.dumps(response_dict[key])
        if isinstance(response_dict[key], dict):
          for key2 in response_dict[key].keys():
            try:
              json.dumps(response_dict[key])
            except:
              response_dict["errorReasons"].append(logException("unable to dump:{}:{}.{}:[{}] in json".format(type(response_dict[key][key2]).__name__, key, key2, response_dict[key][key2])))
        elif isinstance(response_dict[key], list):
          itemCount = 0
          for items in response_dict[key]:
            try:
              json.dumps(items)
              itemCount += 1
            except:
              response_dict["errorReasons"].append(logException("unable to dump:{}:{}[{:,}]:[{}] in json".format(type(items).__name__, key, itemCount, items)))
        else:
          response_dict["errorReasons"].append(logDebug("{}:{}:[{}]".format(type(response_dict[key]).__name__, key, response_dict[key])))
          
      except:
        response_dict["errorReasons"].append(logException("unable to dump:{}:{}:[{}] in json".format(type(response_dict[key]).__name__, key, response_dict[key])))
    
    resp = Response(response=json.dumps(response_dict), status=200, mimetype="application/json")
    
  return resp#jsonify(response_dict)
  
def route(request_dict):
  errorReason_list = []
  #logDebug("#apiName:[{}]->request_dict.keys():[{}]".format(request_dict["apiName"], request_dict.keys()))
  
  try:
    apiName_list = request_dict["apiName"].split(".")
  except:
    return {
        "state": "INVALID REQUEST",
        "errorReasons": [logException("invalid request_dict:[{}]".format(request_dict))]
      }
    
  if len(apiName_list) > 1:
    if apiName_list[0] in ["tammy"] and exists(join(getcwd(), "tammy")):
      if len(apiName_list) > 5:
        packagePath = "tammy.{}.{}.{}.{}".format(apiName_list[1], apiName_list[2], apiName_list[3], apiName_list[4])
        logWarn("{} is taken and apiName:[{}] must be less than 6 items".format(packagePath, request_dict["apiName"]                ))

      elif len(apiName_list) == 5:
        packagePath = "tammy.{}.{}.{}.{}".format(apiName_list[1], apiName_list[2], apiName_list[3], apiName_list[4])
        
      elif len(apiName_list) == 4:
        packagePath = "tammy.{}.{}.{}".format(apiName_list[1], apiName_list[2], apiName_list[3])
      
      elif len(apiName_list) == 3:
        packagePath = "tammy.{}.{}".format(apiName_list[1], apiName_list[2])
      
      elif len(apiName_list) == 2:
        packagePath = "wooju.{}.{}".format(apiName_list[0], apiName_list[1])
      
      else:
        return {
            "state": "INVALID REQUEST",
            "errorReasons": [logError("invalid apiName:[{}]".format(request_dict["apiName"]))]
          }
    
    else:
      if apiName_list[0] in ["wooju"]:
        del apiName_list[0]
        logDebug("apiName_list:[{}]".format(apiName_list))
    
      if len(apiName_list) > 4:
        packagePath = "wooju.{}.{}.{}.{}".format(apiName_list[0], apiName_list[1], apiName_list[2], apiName_list[3])
        logWarn("{} is taken and apiName:[{}] must be less than 5 items".format(packagePath, request_dict["apiName"]))
        
      elif len(apiName_list) > 3:
        packagePath = "wooju.{}.{}.{}.{}".format(apiName_list[0], apiName_list[1], apiName_list[2], apiName_list[3])
      
      elif len(apiName_list) == 3:
        packagePath = "wooju.{}.{}.{}".format(apiName_list[0], apiName_list[1], apiName_list[2])
      
      elif len(apiName_list) == 2:
        packagePath = "wooju.{}.{}".format(apiName_list[0], apiName_list[1])
      
      else:
        return {
            "state": "INVALID REQUEST",
            "errorReasons": [logError("invalid apiName:[{}]".format(request_dict["apiName"]))]
          }
  
    logDebug("packagePath:[{}] is set".format(packagePath))
      
    try:
      apiPackage = __import__(packagePath, fromlist=[''])
      try:
        __processBeginTime__ = time.time()
        
        response_dict = apiPackage.response(request_dict)
          
        return response_dict
      
      except Exception as e:
        return {
          "state": "FAILED",
          "errorReasons": [logException("function:[{}.response()]".format(packagePath))]
          }
      #request_dict["errorReason"] = "serviceName:[{}] is found".format(serviceName)
    except Exception as e:
      return {
          "state": "NOT IMPLEMENTED",
          "errorReasons": [logException("failed to load package:[{}]".format(packagePath))]
          }
  
    return {
        "state": "UNEXPECTED ERROR",
        "errorReasons": [raiseValueError("this return shouldn't be reached")]
      }
  else:
    return {
        "state": "INVALID REQUEST",
        "errorReasons": [logError("invalid apiName:[{}]".format(request_dict["apiName"]))]
      }
