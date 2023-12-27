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
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from pathway import updateMsg
from graphcode.aws.parse import GcParse
from wooju.args import getInputs, getAccountId, getRegionCode, getApiName, getArguments, getPrimaryKeys, getDanteScriptId

from uuid import uuid4

import json

def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "__file__": __file__
      }
  except:
    response_dict = {
      "apiName": request_dict["apiName"],
      "state":"FAILED",
      "errorReasons":[logException("apiName:[{}] failed".format(request_dict["apiName"]))],
      "__file__": __file__
      }

  return response_dict

def action(request_dict):
  logMessage_list = []
  errorReason_list = []
  
  danteResult_list = getInputs(request_dict)["danteResults"]
  
  if len(danteResult_list) > 0:
    logDebug("danteResult_list(len:{:,})][-1]:[{}]".format(len(danteResult_list), danteResult_list[-1]))
  else:
    logDebug("danteResult_list(len:{:,})]:[{}]".format(len(danteResult_list), danteResult_list))
  
  parse_dict = {}
  resultCount = 0
  for danteResultItem_dict in danteResult_list:
    resultCount +=1
    resultIndexKey = "{}".format(resultCount).zfill(2)
    try:
      json.dumps(danteResultItem_dict)
      
      parse_dict = iterateResults(resultIndexKey, parse_dict, result_dict=danteResultItem_dict["output"], depth=0)
      parse_dict = cleanUpResults(parse_dict)
    except:
      logException("danteResultItem_dict:[{}]".format(danteResultItem_dict))
     
  if len(parse_dict.keys()) > 0:
    logDebug("parse_dict.keys(len:{:,})]:[{}]".format(len(parse_dict.keys()), parse_dict.keys()))
    
    if "_K2" in parse_dict.keys():
      k2Result_dict = {}
      for key in set(parse_dict.keys()):
        logDebug("key:{}:[{}]".format(key, parse_dict[key]))
        
        if key in ['sdkResponseMetadata', 'sdkHttpMetadata', 'danteCallStatus']:
          del parse_dict[key]
        elif key in ["_K2"]:
          
          input_dict = {}
          payload_dict = {}
          if len(parse_dict[key]) == 1:
            logDebug("k2APICount:[{:,}]".format(len(parse_dict[key])))
          else:
            logWarn("k2APICount:[{:,}]".format(len(parse_dict[key])))
            
          for k2ResultItem_dict in parse_dict[key]:
            for key2 in k2ResultItem_dict.keys():
              if key2 in ["inputArgsAsJson"]:
                payload_dict["args"] = k2ResultItem_dict[key2]
                for key3 in k2ResultItem_dict[key2].keys():
                  input_dict[key3] = k2ResultItem_dict[key2][key3]
                  
              else:
                if key2 in ["region"]:
                  input_dict["regionCode"] = k2ResultItem_dict[key2]
                else:
                  input_dict[key2] = k2ResultItem_dict[key2]
                  
                payload_dict[key2] = k2ResultItem_dict[key2]
      
      del parse_dict["_K2"]    
      
      gcParse = GcParse(result=parse_dict, inputs=input_dict, payload=payload_dict)
      parse_dict = {
        payload_dict["apiName"]:gcParse.get()
        }
  else:
    logDebug("parse_dict.keys(len:{:,})]:[{}]".format(len(parse_dict.keys()), parse_dict.keys()))
  
  
  return {
    **parse_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def updateParseWithData(parse_dict, key, data_list):
  if key in parse_dict.keys():
    if isinstance(parse_dict[key], list):
      for dataItem_dict in data_list:
        parse_dict[key].append(dataItem_dict)
    else:
      logWarn(" unexpected {}:parse_dict[{}]:[{}]".format(type(parse_dict[key]).__name__, key, parse_dict[key]))
      parse_dict[key] = [parse_dict[key]]
      for dataItem_dict in data_list:
        parse_dict[key].append(dataItem_dict)
  else:
    parse_dict[key] = data_list
  
def iterateResults(resultIndexKey, parse_dict, result_dict, depth=0):
  if depth > 3:
    return parse_dict
  
  if isinstance(result_dict, dict):
    for outputKey in result_dict.keys():
      if isinstance(result_dict[outputKey], list):
        #parse_dict[outputKey] = result_dict[outputKey]
        updateParseWithData(parse_dict, outputKey, result_dict[outputKey])
        
      else:
        #parse_dict[outputKey] = [{"dict":result_dict[outputKey]}]
        updateParseWithData(parse_dict, outputKey, [{"dict":result_dict[outputKey]}])
        
  elif isinstance(result_dict, list):
    if len(result_dict) == 1 and isinstance(result_dict[0], dict):
      for outputKey in result_dict[0].keys():
        
        if isinstance(result_dict[0][outputKey], list):
          #parse_dict[outputKey] = result_dict[0][outputKey]
          updateParseWithData(parse_dict, outputKey, result_dict[0][outputKey])
          
        else:
          #parse_dict[outputKey] = [{"list":result_dict[0][outputKey]}]
          updateParseWithData(parse_dict, outputKey, [{"list":result_dict[0][outputKey]}])
          
  elif isinstance(result_dict, str):
    try:
      result_dict=json.loads(result_dict)
      #parse_dict["{}.{}".format(resultIndexKey, depth)] = iterateResults(parse_dict, result_dict, depth+1)
      #updateParseWithData(parse_dict, "{}.{}".format(resultIndexKey, depth), iterateResults(parse_dict, result_dict, depth+1))
          
      if isinstance(result_dict, dict):
        for outputKey in result_dict.keys():
          if isinstance(result_dict[outputKey], list):
            #parse_dict[outputKey] = result_dict[outputKey]
            updateParseWithData(parse_dict, outputKey, result_dict[outputKey])
            
          else:
            #parse_dict[outputKey] = [{"dict":result_dict[outputKey]}]
            updateParseWithData(parse_dict, outputKey, [{"dict":result_dict[outputKey]}])
            
      elif isinstance(result_dict, list):
        if len(result_dict) == 1 and isinstance(result_dict[0], dict):
          for outputKey in result_dict[0].keys():
            
            if isinstance(result_dict[0][outputKey], list):
              #parse_dict[outputKey] = result_dict[0][outputKey]
              updateParseWithData(parse_dict, outputKey, result_dict[0][outputKey])
              
            else:
              #parse_dict[outputKey] = [{"list":result_dict[0][outputKey]}]
              updateParseWithData(parse_dict, outputKey, [{"list":result_dict[0][outputKey]}])
      else:
        #parse_dict["{}.{}".format(resultIndexKey, depth)] = [{"data":result_dict}]
        updateParseWithData(parse_dict, "{}.{}".format(resultIndexKey, depth), [{"data":result_dict}])
        
    except:
      #parse_dict["{}.{}".format(resultIndexKey, depth)] = [{"str":result_dict}]
      if result_dict in ['The requested script output does not exist. Consult the Get Output section in https://w.amazon.com/bin/view/AWS/Kumo/Hellas/GettingStarted/#HDanteAPIs for troubleshooting instructions.']:
        logWarn("ignored:[{}]".format(result_dict))
      else:  
        updateParseWithData(parse_dict, "{}".format(resultIndexKey), [{"str":result_dict}])
      
  else:
    #parse_dict["{}.{}".format(resultIndexKey, depth)] = [{"data":result_dict}]
    updateParseWithData(parse_dict, "{}.{}".format(resultIndexKey, depth), [{"data":result_dict}])
    
  return parse_dict

def cleanUpResults(parse_dict):
  for resultIndexKey in parse_dict.keys():
    logDebug("resultIndexKey:[{}](len:[{:,}]".format(resultIndexKey, len(parse_dict[resultIndexKey])))
    
    rowCount = 0
    for resultItem_dict in parse_dict[resultIndexKey]:
      if isinstance(resultItem_dict, dict):
        #if rowCount == 0:
        #  logDebug("resultItem_dict.keys:[{}]".format(resultItem_dict.keys()))
        #logDebug("#resultItem_dict.keys:[{}]".format(resultItem_dict.keys()))
        
        for itemKey in set(resultItem_dict.keys()):
          
          #if rowCount == 0:
          #  if isinstance(resultItem_dict[itemKey], dict) or isinstance(resultItem_dict[itemKey], list):
          #    logDebug("{}:resultItem_dict[{}]:[{}]".format(type(resultItem_dict[itemKey]).__name__, itemKey, resultItem_dict[itemKey]))
            
          if isinstance(resultItem_dict[itemKey], dict):
            if "__type" in resultItem_dict[itemKey].keys():
              if "label" in resultItem_dict[itemKey].keys():
                resultItem_dict["{}.".format(itemKey)] = resultItem_dict[itemKey]["value"]
                resultItem_dict[itemKey] = resultItem_dict[itemKey]["label"]
                
              elif "options" in resultItem_dict[itemKey].keys():
                #logDebug("#{}:{}:[{}]".format(itemKey, type(resultItem_dict[itemKey]["options"]).__name__, resultItem_dict[itemKey]["options"]))
                if isinstance(resultItem_dict[itemKey]["options"], dict):
                  if "label" in resultItem_dict[itemKey]["options"].keys():
                    resultItem_dict["{}_".format(itemKey)] = resultItem_dict[itemKey]["value"]
                    resultItem_dict[itemKey] = resultItem_dict[itemKey]["options"]["label"]
                  else:
                    resultItem_dict[itemKey] = resultItem_dict[itemKey]["value"]
                    
                elif isinstance(resultItem_dict[itemKey]["options"], str) and "label" in resultItem_dict[itemKey]["options"]:
                  
                  try:
                    resultItem_dict[itemKey] = json.loads(resultItem_dict[itemKey]["options"])["label"]
                    resultItem_dict["{}_".format(itemKey)] = resultItem_dict[itemKey]["value"]
                  except:
                    resultItem_dict[itemKey] = resultItem_dict[itemKey]["value"]
                    resultItem_dict["{}_".format(itemKey)] = resultItem_dict[itemKey]["options"]
                  
              elif "value" in resultItem_dict[itemKey].keys():
                resultItem_dict[itemKey] = resultItem_dict[itemKey]["value"]
            
            else:
              for subKey in resultItem_dict[itemKey].keys():
                if subKey in resultItem_dict.keys():
                  if resultItem_dict[itemKey][subKey] not in ["",None, resultItem_dict[itemKey][subKey]]:
                    resultItem_dict["{}_".format(subKey)] = resultItem_dict[itemKey][subKey]
                else:
                  resultItem_dict[subKey] = resultItem_dict[itemKey][subKey]
                  
              try:
                del resultItem_dict[itemKey]
              except:
                logException("failed to delete itemKey:[{}]".format(itemKey))
        
          elif isinstance(resultItem_dict[itemKey], list) and len(resultItem_dict[itemKey])==1 and isinstance(resultItem_dict[itemKey][0], dict):
            if "__type" in resultItem_dict[itemKey][0].keys():
              if "label" in resultItem_dict[itemKey][0].keys():
                resultItem_dict["{}_".format(itemKey)] = resultItem_dict[itemKey][0]["value"]
                resultItem_dict[itemKey] = resultItem_dict[itemKey][0]["label"]
              
              elif "options" in resultItem_dict[itemKey][0].keys() and "label" in resultItem_dict[itemKey][0]["options"].keys():
                  resultItem_dict["{}_".format(itemKey)] = resultItem_dict[itemKey][0]["value"]
                  resultItem_dict[itemKey] = resultItem_dict[itemKey][0]["options"]["label"]
                  
              elif "value" in resultItem_dict[itemKey][0].keys():
                resultItem_dict[itemKey] = resultItem_dict[itemKey][0]["value"]
                
      rowCount += 1
  
  return parse_dict
          
      
      