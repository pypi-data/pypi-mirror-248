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

from os.path import dirname, basename, abspath

import inspect

def getDanteResults(danteResult_dict):
  countI = 0
  for stackItem_list in inspect.stack():
    if stackItem_list[3] != "getWbResults":
      break
    #print("{}:[{}]".format(-countI, inspect.stack()[countI][3]))
    countI += 1
  danteScriptName = basename(dirname(inspect.stack()[countI][1][len(abspath("."))+1:]))
           
  if "response" in danteResult_dict.keys():
    
    thisDanteResult_dict = {}
    if len(danteResult_dict["response"].keys()) > 0:
      logDebug("danteResult_dict.keys(len:{:,})]:[{}]".format(len(danteResult_dict["response"].keys()), danteResult_dict["response"].keys()))
      
      if danteScriptName in ["dante"]:
        for key in danteResult_dict["response"].keys():
          if isinstance(danteResult_dict["response"][key], list):
            if len(danteResult_dict["response"][key]) > 0:
              logDebug("{}(len:{:,})[-1]:[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key][-1]))
            else:
              logDebug("{}(len:{:,}):[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key]))
            
            thisDanteResult_dict[key] = danteResult_dict["response"][key]
          else:
            logWarn("unexpected {}:{}:[{}]".format(type(danteResult_dict["response"][key]).__name__, key, danteResult_dict["response"][key]))
            
            thisDanteResult_dict[key] = [{"data":danteResult_dict["response"][key]}]
      
      else:
            
        for key in danteResult_dict["response"].keys():
          if isinstance(danteResult_dict["response"][key], list):
            if len(danteResult_dict["response"][key]) > 0:
              logDebug("{}(len:{:,})[-1]:[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key][-1]))
            else:
              logDebug("{}(len:{:,}):[{}]".format(key, len(danteResult_dict["response"][key]), danteResult_dict["response"][key]))
            
            thisDanteResult_dict["{}_{}".format(danteScriptName, key)] = danteResult_dict["response"][key]
          else:
            logWarn("unexpected {}:{}:[{}]".format(type(danteResult_dict["response"][key]).__name__, key, danteResult_dict["response"][key]))
            
            thisDanteResult_dict["{}_{}".format(danteScriptName, key)] = [{"data":danteResult_dict["response"][key]}]
            
    else:
      logDebug("danteResult_dict.keys(len:{:,})]:[{}]".format(len(danteResult_dict["response"].keys()), danteResult_dict["response"].keys()))
     
    return thisDanteResult_dict
  
  else:
    return danteResult_dict