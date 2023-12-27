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
from graphcode.conf import getLogPath
from graphcode.conf import getLogLevel

import sys
import linecache
import inspect

import platform

import os
from os import mkdir, getpid, getppid
from os.path import join, exists, expanduser, abspath

import time
from pytz import timezone
from datetime import datetime

import logging

import json

def get_stack_info(countI):
    try:
        return f"{inspect.stack()[countI+1][1][len(abspath('.'))+1:]}:{inspect.stack()[countI+1][2]}:{inspect.stack()[countI+1][3]}"
    except IndexError:
        return "Unknown location"

def logMsg(msg):
    skip_functions = {
        "logInfo", "logError", "logTrace", "logUnitTest", "logDebug", "logMsg",
        "logException", "logMsgForException", "logExceptionWithValueError",
        "logWarn", "logCritical", "raiseValueError", "loadJson", "getItem",
        "putItemW", "deleteItem", "getItemWithS3", "putItemWithS3",
        "deleteItemWithS3", "displayItemDetails"
    }

    countI = 0
    for stackItem in inspect.stack():
        if stackItem.function not in skip_functions:
            break
        countI += 1

    stack_info = get_stack_info(countI)
    return f"\t{getppid()}:{getpid()}\t{stack_info}\t{msg}"

def logMsgForException(msg=None):
    # Retrieve the current exception information
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename[len(abspath("./"))+1:]
    
    # Initialize the stack counter
    countI = 0
    
    # Iterate through the call stack to find the caller function
    for stackItem in inspect.stack():
        if stackItem.function not in {"logException", "logMsgForException"}:
          break
        countI += 1
    
    # Define a helper function to format the message
    def format_msg(extra_info=""):
      nonlocal msg
      try:
        location_info = f"{inspect.stack()[countI+2][1][len(abspath('.'))+1:]}:{inspect.stack()[countI+2][2]}:{inspect.stack()[countI+2][3]}"
        caller_info = f"{inspect.stack()[countI+1][1][len(abspath('.'))+1:]}:{inspect.stack()[countI+1][2]}:{inspect.stack()[countI+1][3]}"
      except IndexError:
        location_info = "Unknown location"
        caller_info = "Unknown caller"
      
      current_info = f"{filename}:{lineno}:{inspect.stack()[countI][3]}"
      exception_info = f"EXCEPTION IN ({current_info}) \"{exc_type}: {exc_obj}\""
      
      if msg:
        exception_info += f" -> Error: [{msg}]"
      
      return f"\t{getppid()}:{getpid()}\t{location_info}\t{caller_info}\t{exception_info}{extra_info}"
    
    # Format the message based on whether a custom message was provided
    if msg is None:
        msg = format_msg()
    else:
        msg = format_msg(extra_info=f" -> Custom Msg: [{msg}]")
    
    return msg

def initLog(logLevel="DEBUG"):
    # Get the log directory path
    logDir = abspath(expanduser(getLogPath()))
    
    # Define a helper function to read log filename from a file
    def read_log_filename(filename):
      if os.path.exists(filename):
        with open(filename, "r") as f:
          return f.readline().strip()
      return None
    
    # Define a helper function to write log filename to a file
    def write_log_filename(filename, log_filename):
      with open(filename, "w") as f:
        f.write(log_filename)
    
    # Attempt to load existing log filename
    logMetaFilename = os.path.join(logDir, "graphcode-{}.log".format(os.getppid()))
    logFilename = read_log_filename(logMetaFilename)
    
    if logFilename:
      print(logMsg("logFilename:[{}] is loaded from '{}'".format(logFilename, logMetaFilename)))
    else:
      logMetaFilename = os.path.join(logDir, "graphcode-{}.log".format(os.getpid()))
      logFilename = read_log_filename(logMetaFilename)
      if not logFilename:
        logFileTimestamp = datetime.fromtimestamp(time.time()).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H-%M-%S_%f%Z')
        logFilename = os.path.join(logDir, "graphcode-{}.log".format(logFileTimestamp))
    
    # Save the log filename for the current process
    thisLogMetaFilename = os.path.join(logDir, "graphcode-{}.log".format(os.getpid()))
    write_log_filename(thisLogMetaFilename, logFilename)
    print(logMsg("logFilename:[{}] is saved at '{}'".format(logFilename, thisLogMetaFilename)))
    
    # Set up logging
    logPriorityNumber = getLogPriorityNumber(logLevel)
    logging.basicConfig(
      handlers=[
        logging.FileHandler(logFilename),
        logging.StreamHandler()
      ],
      format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', 
      datefmt='%Y/%m/%d %H:%M:%S',
      level=logPriorityNumber
    )
    
    logInfo("logging is initialized with filename:[{}](level:{}:{})".format(logFilename, logLevel, logging.getLogger().level))
    
    return True

def getLogFilename():
    """Retrieve the filename of the first logging handler."""
    try:
        return logging.getLogger().handlers[0].baseFilename
    except (IndexError, AttributeError):
        return None

def setLogLevel(logLevel):
    """Set the logging level for the root logger."""
    logPriorityNumber = getLogPriorityNumber(logLevel)
    logging.getLogger().setLevel(logPriorityNumber)
    logDebug("logLevel:[{}]({}) is set".format(logLevel, logging.getLogger().level))

def getLogPriorityNumber(logLevel):
    """Convert a log level string to a logging level number."""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return log_levels.get(logLevel, logging.INFO)
    
def logDebug(msg):
  if logging.getLogger().level <= logging.DEBUG:
    logging.debug(logMsg(msg))
  
  return msg
  
def logInfo(msg):
  if logging.getLogger().level <= logging.INFO:
    logging.info(logMsg(msg))
  
  return msg
  
def logWarn(msg):
  if logging.getLogger().level <= logging.WARN:
    logging.warn(logMsg(msg))
  
  return msg
  
def logError(msg):
  if logging.getLogger().level <= logging.ERROR:
    logging.error(logMsg(msg))
  
  return msg

def raiseValueError(msg):
  if logging.getLogger().level <= logging.ERROR:
    logging.error(logMsg(msg))
    raise ValueError(msg)

def logException(msg = ""):
  if logging.getLogger().level <= logging.ERROR:
    errMsg = logMsgForException(msg)
    logging.exception(errMsg)
  
  return errMsg

def logExceptionWithValueError(msg = ""):
  if logging.getLogger().level <= logging.ERROR:
    errMsg = logMsgForException(msg)
    logging.exception(errMsg)
    raise ValueError(errMsg)

def logCritical(msg):
  if logging.getLogger().level <= logging.CRITICAL:
    logging.critical(logMsg(msg))
  
  return msg

def iterateValue(value, maxDepth=3):
  """Iterate through the values recursively and format them as plain text."""
  plainText = recuseValue(value, maxDepth=maxDepth).strip()
  return plainText

def recuseValue(value, depth=0, maxDepth=3):
  """Recursively process the value based on its type."""
  if depth > maxDepth:
    return json.dumps(value)
  
  plainText = ''
  indent = "\t" * depth
  
  if isinstance(value, dict):
    for key, val in value.items():
      valueType = type(val).__name__
      if isinstance(val, (dict, list)):
        plainText += f'\n{indent}({valueType})\t{key}:{recuseValue(val, depth+1, maxDepth)}'
      else:
        plainText += f"\n{indent}({valueType})\t{key}:[{val}]"
              
  elif isinstance(value, list):
    for i, item in enumerate(value):
      valueType = type(item).__name__
      plainText += f'\n{indent}({valueType})\t[{i}]:{recuseValue(item, depth+1, maxDepth)}'
          
  else:
    valueType = type(value).__name__
    plainText += f"\n{indent}({valueType})\t{value}"
      
  return plainText
