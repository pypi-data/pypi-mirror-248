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
from graphcode.logging import logDebug, logError, logInfo, logException, logExceptionWithValueError
from graphcode.path import createDir
from os.path import dirname, expanduser, abspath, exists, isfile, isdir, islink, ismount
import json

def loadJson(jsonFilePath, verboseMode=True):
    """
    Load JSON data from a file.
    
    :param jsonFilePath: Path to the JSON file.
    :param verboseMode: Flag to enable verbose logging.
    :return: Loaded JSON data or None if loading fails.
    """
    jsonData = None
    absJsonFilePath = abspath(expanduser(jsonFilePath))
    
    if exists(absJsonFilePath) and isfile(absJsonFilePath):
        if verboseMode:
            logDebug(f"type:file:[{jsonFilePath}] is found")
        
        try:
            with open(absJsonFilePath, "r") as f:
                jsonData = json.load(f)
                if verboseMode:
                    logInfo(f"jsonFilePath({len(json.dumps(jsonData))} bytes):[{jsonFilePath}]({absJsonFilePath}) was read")
            return jsonData
        
        except Exception as e:
            logExceptionWithValueError(f"absJsonFilePath:[{absJsonFilePath}]")
            logError(str(e))
    
    else:
        _logFileType(absJsonFilePath, jsonFilePath, verboseMode)
        logExceptionWithValueError(f"jsonFilePath:[{jsonFilePath}] is not found")
    
    return jsonData

def dumpJson(jsonFilePath, jsonData, verboseMode=True):
    """
    Dump JSON data to a file.
    
    :param jsonFilePath: Path to the JSON file.
    :param jsonData: JSON data to be dumped.
    :param verboseMode: Flag to enable verbose logging.
    :return: True if dumping succeeds, False otherwise.
    """
    absJsonFilePath = abspath(expanduser(jsonFilePath))
    
    if exists(absJsonFilePath) and verboseMode:
        logDebug(f"type:file:[{jsonFilePath}] is found")
    
    try:
        with open(absJsonFilePath, "w") as f:
            json.dump(jsonData, f, indent=2)
            logMsg = f"jsonFilePath({len(json.dumps(jsonData))} bytes):[{jsonFilePath}]({absJsonFilePath}) was written"
            if verboseMode:
                logDebug(logMsg)
        return True
    
    except Exception as e:
        logException()
        logError(str(e))
        return False
    
    if verboseMode:
        logInfo(f"file:[{jsonFilePath}] is not found")
    
    absDirPath = dirname(absJsonFilePath)
    if len(absDirPath) > 0 and verboseMode:
        logInfo(f"absDirPath:[{absDirPath}]")
    
    if createDir(absDirPath):
        try:
            with open(absJsonFilePath, "w") as f:
                json.dump(jsonData, f, indent=2)
                logMsg = f"jsonFilePath({len(json.dumps(jsonData))} bytes):[{jsonFilePath}]({absJsonFilePath}) was written"
                if verboseMode:
                    logInfo(logMsg)
            return True
        
        except Exception as e:
            logException()
            logError(str(e))
    
    return False

def _logFileType(absJsonFilePath, jsonFilePath, verboseMode):
    """
    Log the type of file at the given path.
    
    :param absJsonFilePath: Absolute path to the file.
    :param jsonFilePath: Original file path.
    :param verboseMode: Flag to enable verbose logging.
    """
    if exists(absJsonFilePath):
        if isdir(absJsonFilePath) and verboseMode:
            logInfo(f"type:dir:[{jsonFilePath}] is found")
        elif islink(absJsonFilePath) and verboseMode:
            logInfo(f"type:link:[{jsonFilePath}] is found")
        elif ismount(absJsonFilePath) and verboseMode:
            logInfo(f"type:mount:[{jsonFilePath}] is found")
        elif verboseMode:
            logInfo(f"type:others:[{jsonFilePath}] is found")
