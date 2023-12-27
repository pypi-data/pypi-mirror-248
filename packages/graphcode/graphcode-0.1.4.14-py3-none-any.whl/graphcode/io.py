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
from graphcode.path import createDir
from graphcode.lib import getDateString

from graphcode.aws.s3 import awsS3, getS3Object, putS3Object, putS3Objects, downloadS3Object

import os
from os.path import dirname, expanduser, abspath, exists, isfile, isdir, islink, ismount
import shutil

import json
from threading import Thread

import time

import logging

def readFile(filePath, decodeMode = "utf-8"):
  data = None
  
  absFilePath = abspath(expanduser(filePath))
  logInfo("absFilePath:[{}]".format(absFilePath))
  
  if exists(absFilePath) and isfile(absFilePath):
    logDebug("type:file:[{}] is found".format(filePath))
    try:
      if decodeMode != None and decodeMode != "b":
        f = open(absFilePath, "r")
      else:
        f = open(absFilePath, "rb")
        
      data = f.read()
      logMsg = "filePath({:,} bytes):[{}]({}) was read".format(len(data), filePath, absFilePath)
      f.close()
      
      logInfo(logMsg)
      return data
    
    except Exception as e:
      logException("unable to read file as text for [{}]".format(absFilePath))
      try:
        f = open(absFilePath, "rb")
        data = f.read()
        logMsg = "filePath({:,} bytes):[{}]({}) was read(b)".format(len(data), filePath, absFilePath)
        f.close()
        
        logInfo(logMsg)
        return data
      
      except Exception as e:
        logException("unable to read file as binary for [{}]".format(absFilePath))
        return data
  else:
    if exists(absFilePath):
      if isdir(absFilePath):
        logInfo("type:dir:[{}] is found".format(filePath))
      elif islink(absFilePath):
        logInfo("type:link:[{}] is found".format(filePath))
      elif ismount(absFilePath):
        logInfo("type:mount:[{}] is found".format(filePath))
      else:
        logInfo("type:others:[{}] is found".format(filePath))
    else:
      logInfo("filePath:[{}] is not found".format(filePath))
  
    return data
  
  raiseValueError("An unexpected behavior happens")

def writeFile(filePath, data, dataType = "text"):
  absFilePath = abspath(expanduser(filePath))
  
  if exists(absFilePath):
    logDebug("type:file:[{}] is found".format(filePath))
  else:
    logInfo("file:[{}] is not found".format(filePath))
    createDir(dirname(absFilePath))
    
  try:
    if dataType == "text":
      f = open(absFilePath, "w")
    else:
      f = open(absFilePath, "wb")
    logInfo("file:[{}] is open".format(f))
    
    f.write(data)
    logInfo("filePath({:,} bytes):[{}]({}) was written".format(len(data), filePath, absFilePath))
    f.close()
    
    return True
  
  except:
    logException()
    return False
    
  raiseValueError()

def getObject(source, credentialName = None, decodeMode = 'utf-8'):
  if source != None and source[:5] == "s3://":
    sources3BucketName = source[5:source.find("/", 5)]
    sourcess3Key = source[source.find("/", 5)+1:].replace("\\","/")
    
    return getS3Object(sources3BucketName, sourcess3Key, credentialName, decodeMode)
  else:
    return readFile(source, decodeMode)
        
def putObject(target, data, credentialName = None):
  if target != None and target[:5] == "s3://":
    targetS3BucketName = target[5:target.find("/", 5)]
    targetS3Key = target[target.find("/", 5)+1:].replace("\\","/")
    
    return putS3Object(targetS3BucketName, targetS3Key, data, credentialName)
  else:
    return writeFile(target, data)
        
def copyObject(source, target, credentialName = None):
  if source != None and source[:5] == "s3://":
    sources3BucketName = target[5:target.find("/", 5)]
    sourceKey = target[target.find("/", 5):]
    
    if target[:5] == "s3://":
      targetS3BucketName = target[5:target.find("/", 5)]
      targets3Key = target[target.find("/", 5)+1:]
    
      logInfo("mock: source(s3):[{}]:[{}] -> target(s3):[{}][{}]".format(sources3BucketName, sourceKey, targetS3BucketName, targets3Key))
    else:
      targetFilename = target
      logInfo("mock: source(s3):[{}]:[{}] -> target(local):[{}]".format(sources3BucketName, sourceKey, targetS3BucketName, targets3Key))

  else:
    
    if target[:5] == "s3://":
      targetS3BucketName = target[5:target.find("/", 5)]
      if os.name == 'nt':
        targets3Key = target[target.find("/", 5)+1:].replace("\\","/")
      else:
        targets3Key = target[target.find("/", 5)+1:]
    
      if credentialName != None:
        if source == None:
          putS3Object(targetS3BucketName, targets3Key, "", credentialName)
        else:
          putS3Object(targetS3BucketName, targets3Key, readFile(source), credentialName)
        logInfo("source(local):[{}] -> target(s3):[{}][{}]".format(source, targetS3BucketName, targets3Key))
      else:
        logError("Error:[credentialName is '{}'] -> source(local):[{}] -> target(s3):[{}][{}]".format(credentialName, source, targetS3BucketName, targets3Key))
      
    else:
      if source != None:
        shutil.copy2(source, target)
        #logInfo("source(local):[{}] -> target(local):[{}]".format(source, target))
      else:
        createDir(target)

def downloadFile(self, bucketName, objectKey, downloadFilePath):
  
  response = self.s3Client.download_file(bucketName,objectKey,downloadFilePath)
  
  logInfo("res:[{}]".format(response))
  
  return downloadFilePath
    
    
def copyObjects(object_list, credentialName = None):
  copyObject_dict = {}
  if isinstance(object_list, list) and len(object_list) > 0:
    for objectItems in object_list:
      if isinstance(objectItems, dict) and "source" in objectItems.keys() and "target" in objectItems.keys():
        
        
        if objectItems["source"] != None and objectItems["source"][:5] == "s3://":
          sources3BucketName = objectItems["target"][5:objectItems["target"].find("/", 5)]
          sourceKey = objectItems["target"][objectItems["target"].find("/", 5):]
          
          if objectItems["target"][:5] == "s3://":
            targetS3BucketName = objectItems["target"][5:objectItems["target"].find("/", 5)]
            targets3Key = objectItems["target"][objectItems["target"].find("/", 5)+1:]
          
            logInfo("mock: source(s3):[{}]:[{}] -> target(s3):[{}][{}]".format(sources3BucketName, sourceKey, targetS3BucketName, targets3Key))
          else:
            targetFilename = objectItems["target"]
            logInfo("mock: source(s3):[{}]:[{}] -> target(local):[{}]".format(sources3BucketName, sourceKey, targetS3BucketName, targets3Key))
      
        else:
          
          if objectItems["target"][:5] == "s3://":
            targetS3BucketName = objectItems["target"][5:objectItems["target"].find("/", 5)]
            if os.name == 'nt':
              targets3Key = objectItems["target"][objectItems["target"].find("/", 5)+1:].replace("\\","/")
            else:
              targets3Key = objectItems["target"][objectItems["target"].find("/", 5)+1:]
          
            if credentialName != None:
              if credentialName in copyObject_dict.keys():
                if targetS3BucketName in copyObject_dict[credentialName].keys():
                  copyObject_dict[credentialName][targetS3BucketName].append({"filename":objectItems["source"], "key":targets3Key})
                  #logInfo("source(local):[{}] -> target(s3):[{}][{}]".format(objectItems["source"], targetS3BucketName, targets3Key))
                else:
                  copyObject_dict[credentialName][targetS3BucketName] = [{"filename":objectItems["source"], "key":targets3Key}]
                  #logInfo("source(local):[{}] -> target(s3):[{}][{}]".format(objectItems["source"], targetS3BucketName, targets3Key))
              else:
                copyObject_dict[credentialName] = {}
                copyObject_dict[credentialName][targetS3BucketName] = [{"filename":objectItems["source"], "key":targets3Key}]
                #logInfo("source(local):[{}] -> target(s3):[{}][{}]".format(objectItems["source"], targetS3BucketName, targets3Key))
                
            else:
              logError("Error:[credentialName is '{}'] -> source(local):[{}] -> target(s3):[{}][{}]".format(credentialName, objectItems["source"], targetS3BucketName, targets3Key))
            
          else:
            if objectItems["source"] != None:
              shutil.copy2(objectItems["source"], objectItems["target"])
              #logInfo("source(local):[{}] -> target(local):[{}]".format(objectItems["source"], objectItems["target"]))
            else:
              createDir(objectItems["target"])
              
  for credentialName in copyObject_dict.keys():
    for targetBucketName in copyObject_dict[credentialName].keys():
      putS3Objects(copyObject_dict[credentialName][targetBucketName], targetBucketName, credentialName)

