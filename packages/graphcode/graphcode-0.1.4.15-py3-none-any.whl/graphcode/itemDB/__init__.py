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
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, raiseValueError, logExceptionWithValueError, logExceptionWithValueError
from graphcode.logging import iterateValue

from graphcode.conf import saveItemDBConfiguration, loadItemDBConfiguration
from graphcode.conf import getItemDBPath
from graphcode.path import createDir

import os
from os.path import expanduser, join, exists, abspath

import base64

import stat

import json

class GcItemDB():
  def __init__(self):
    self.itemDBConf_dict = loadItemDBConfiguration()

    self.itemDBRootPath = abspath(expanduser(getItemDBPath())) 
    
    self.connItemDB = self.connectModuDB()
    
  def connectModuDB(self, dbName="itemDB"):
    
    self.connItemDB = join(self.itemDBRootPath, dbName)
    
    #logDebug('itemDB is connected:[{}]'.format(self.connItemDB))
    
    return self.connItemDB
    
  def initItemDB(self):
    
    if exists(self.connItemDB):
      try:
        table_list = self.initItemTables()
        logDebug("initialized table(s):[{}].".format(table_list))
      except Exception as e: 
        logExceptionWithValueError("failed to to initializ table(s) at [{}] -> Error:{}".format(self.connItemDB , e))
      
      try:
        queue_list = self.initItemQueues()
        logDebug("initialized queue(s):[{}].".format(queue_list))
      except Exception as e: 
        logExceptionWithValueError("failed to initializ queues -> Error:{}".format(e))
    
    else:
      try:
        os.mkdir(self.connItemDB)
        logDebug("'gcItemDB':[{}] is created.".format(self.connItemDB))
      except Exception as e: 
        logExceptionWithValueError("failed to create DB:[{}]  -> {}".format(self.connItemDB , e))
      
      table_list, queue_list = self.initItemDB()

    return table_list, queue_list
    
  def initItemTables(self):
    table_list = []
    for table in self.itemDBConf_dict["tables"].keys():
      try:
        self.createTable(table)

        table_list.append(table)
      except Exception as e: 
        logExceptionWithValueError("failed to create DB Table:[{}] -> {}".format(table, e))

    return table_list
  
  def createTable(self, table):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    if exists(tablePath) == False:
      try:
        createDir(tablePath)
        self.itemDBConf_dict['tables'][table] = {
          "cache":False,
          "ttl_s":-1
          }
        logInfo("Table:[{}]:[{}] is created.".format(table, self.itemDBConf_dict['tables'][table]))
        #logInfo(iterateValue(value=self.itemDBConf_dict))
      except Exception as e: 
        logExceptionWithValueError("failed to create DB Table:[{}] at [{}]  -> {}".format(table, tablePath, self.itemDBConf_dict))
    else:
      logDebug("table:[{}] is already created".format(table))

    return table
  
  def listTables(self, maxNumberOfTables = -1):
    numberOfTables = 0
    
    tableList = []
    dirEntryList = os.listdir(self.connItemDB)
    
    for dirEntryName in dirEntryList:
      dirEntryPath = "{}/{}".format(self.connItemDB, dirEntryName)
      
      dirEntryStatInfo = os.stat(dirEntryPath)
      #logDebug("dirEntryName:[{}] -> dirEntryStatInfo:[{}]".format(dirEntryName, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__table__" in dirEntryName:
        #logDebug("table:[{}] is found".format(dirEntryName))
        tableList.append(dirEntryName)
        numberOfTables += 1
        
        if maxNumberOfTables > 0 and numberOfTables >= maxNumberOfTables:
      
          return tableList
    
    return tableList
  
  def deleteTable(self, table):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
      
    if exists(tablePath) and table not in ['itemDB']:
      try:
        os.rmdir(tablePath)
        iterateValue(value=self.itemDBConf_dict)
        del self.itemDBConf_dict['tables'][table]
        saveItemDBConfiguration(self.itemDBConf_dict)

        logInfo("Table:[{}] is deleted.".format(table))
      except Exception as e: 
        logExceptionWithValueError("failed to delete table:[{}] at [{}]  -> {}".format(table, tablePath, e))
    else:    
      if table in ['itemDB']:
        raiseValueError("Table:[{}] can't be deleted".format(table))
      else:
        raiseValueError("Table:[{}] is not found".format(tablePath))
      
    return table
  
  def existTable(self, table):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
      
    if exists(tablePath):
      #logDebug("table:[{}] is existed.".format(table))
      return True
    else:    
      #logDebug("table:[{}] is not found".format(table))
      return False
        
  def put(self, table, key, value, mode = "w"):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    if exists(tablePath):
      dirEntryStatInfo = os.stat(tablePath)
      #logDebug("tablePath:[{}] -> dirEntryStatInfo:[{}]".format(tablePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__table__" in tablePath:
        #logDebug("Table:[{}] is found".format(tablePath))
        
        try:
          hashedB64Key = base64.b64encode(key.encode()).decode()
          objectPath = "{}/{}".format(tablePath, hashedB64Key)
          if len(objectPath) > 254:
            objectPath = objectPath[:254]
            logWarn("omitted objectPath:[{}]..[{}] with gc://{}/{}".format(objectPath[:254], objectPath[254:], table, key))
            
          f = open(objectPath, mode)
          if isinstance(value, dict) or isinstance(value, list):
            try:
              f.write(json.dumps(value))
            except Exception as e:
              logError("something wrong->Error:[{}]".format(e))
              f.write("{}".format(value))
          else:
            f.write(value)
            
          f.close()
          #logDebug("{}(Table:[{}], Key:[{}]) -> hashedB64Key:[{}] -> Value:[len({})] is stored.".format(objectPath, tablePath, key, hashedB64Key, len(value)))
        except Exception as e: 
          logExceptionWithValueError( "Error:[{}] -> failed to store key:[{}] ->hashedB64Key:[{}], value:[len({})] at Table:[{}]  -> {}".format(e, key, hashedB64Key, len(value), tablePath, value))   
          
    else:
      raiseValueError("Table:[{}] is not found".format(tablePath))
  
    return table  
  
  def get(self, table, key, mode = "r"):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    value = None
    
    if exists(tablePath):
      dirEntryStatInfo = os.stat(tablePath)
      #logDebug("#tablePath:[{}] -> dirEntryStatInfo:[{}]".format(tablePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__table__" in tablePath:
        #logDebug("#Table:[{}] is found".format(tablePath))
        
        hashedB64Key = base64.b64encode(key.encode()).decode()
        
        objectPath = "{}/{}".format(tablePath, hashedB64Key)
        if len(objectPath) > 254:
          objectPath = objectPath[:254]
          logWarn("omitted objectPath:[{}]..[{}] with gc://{}/{}".format(objectPath[:254], objectPath[254:], table, key))
            
        if exists(objectPath):
          try:
            f = open(objectPath, mode)
            value = f.read()
            f.close()
            #logDebug("Table:[{}], Key:[{}] -> hashedB64Key:[{}], Value:[len({})] is read.".format(tablePath, key, hashedB64Key, len(value)))
          except Exception as e: 
            logExceptionWithValueError("Error:[{}] -> failed to read key:[{}] -> hashedB64Key:[{}] at Table:[{}]".format(e, key, hashedB64Key, tablePath))
        else:
          raiseValueError("Table:[{}]->Key:[{}] is not found".format(table, key))   
          
    else:
      raiseValueError("Table:[{}] is not found".format(tablePath))
    
    return value
  
  def delete(self, table, key):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    if exists(tablePath):
      dirEntryStatInfo = os.stat(tablePath)
      #logDebug("tablePath:[{}] -> dirEntryStatInfo:[{}]".format(tablePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__table__" in tablePath:
        #logDebug("Table:[{}] is found".format(tablePath))
        
        hashedB64Key = base64.b64encode(key.encode()).decode()
        try:
          objectPath = "{}/{}".format(tablePath, hashedB64Key)
          os.remove(objectPath)
          #logDebug("Table:[{}], Key:[{}] -> hashedB64Key:[{}] is deleted.".format(tablePath, key, hashedB64Key))
        except Exception as e: 
          logExceptionWithValueError("Error:[{}] -> failed to delete key:[{}] at tablePath:[{}]".format(e, key, tablePath)) 
          
    else:
      raiseValueError("Table:[{}] is not found".format(tablePath))
      
    return "{}/{}".format(table, key)
    
  def listItems(self, table, maxNumberOfItems = -1):
    
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    numberOfItems = 0
    item_list = []
    
    if exists(tablePath):
      
      dirEntryList = os.listdir(tablePath)
      
      for dirEntryName in dirEntryList:
        dirEntryPath = "{}/{}".format(tablePath, dirEntryName)
        
        dirEntryStatInfo = os.stat(dirEntryPath)
        #logDebug("dirEntryName:[{}] -> dirEntryStatInfo:[{}]".format(dirEntryName, dirEntryStatInfo))
        
        if stat.S_ISREG(dirEntryStatInfo.st_mode):
          decodedHashedB64Key = base64.b64decode(dirEntryName.encode()).decode()
          #logDebug("hashedB64Key:[{}] -> key:[{}]is found".format(dirEntryName, decodedHashedB64Key))
          item_list.append(decodedHashedB64Key)
          
          numberOfItems += 1
          if maxNumberOfItems > 0 and numberOfItems >= maxNumberOfItems:
            break
          
    else:
      raiseValueError("Table:[{}] is not found".format(tablePath))
    
    return item_list
  
  def exist(self, table, key):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    if exists(tablePath):
      hashedB64Key = base64.b64encode(key.encode()).decode()
      objectPath = "{}/{}".format(tablePath, hashedB64Key)
      if exists(objectPath):
        #logDebug("table:[{}] -> key:[{}] -> hashedB64Key:[{}] is existed.".format(table, key, hashedB64Key))
      
        return True
      else:    
        #logDebug("table:[{}] -> key:[{}] -> hashedB64Key:[{}] is not found".format(table, key, hashedB64Key))
      
        return False
    
    else:
      #logDebug("table:[{}] is not found".format(table))
      
      return False
  
  def initItemQueues(self):
    queue_list = []
    for queueName in self.itemDBConf_dict["tables"].keys():
      try:
        self.createQueue(queueName)
        
        queue_list.append(queueName)

      except Exception as e: 
        logExceptionWithValueError("failed to create a queue:[{}]  -> {}".format(queueName, e))
      
    return queue_list
  
  def createQueue(self, queueName):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
      
    if exists(queuePath) == False:
      try:
        os.mkdir(queuePath)
        self.itemDBConf_dict['queues'][queueName] = {
          "fifo":False,
          "ttl_s":-1
          }
        saveItemDBConfiguration(self.itemDBConf_dict)
        logInfo("Queue:[{}] is created.".format(queuePath))
      except Exception as e: 
        logExceptionWithValueError("failed to create a queue:[{}] at [{}]  -> {}".format(queueName, queuePath, e))   

    return queueName  
  
  def listQueues(self, maxNumberOfQueues = -1):
    numberOfQueues = 0
    
    queue_list = []
    dirEntryList = os.listdir(self.connItemDB)
    
    for dirEntryName in dirEntryList:
      dirEntryPath = "{}/{}".format(self.connItemDB, dirEntryName)
      
      dirEntryStatInfo = os.stat(dirEntryPath)
      #logDebug("dirEntryName:[{}] -> dirEntryStatInfo:[{}]".format(dirEntryName, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__queue__" in dirEntryName:
        #logDebug("queue:[{}] is found".format(dirEntryName))
        queue_list.append(dirEntryName)
        numberOfQueues += 1
        
        if maxNumberOfQueues > 0 and numberOfQueues >= maxNumberOfQueues:
          break
      
    return queue_list
   
  def deleteQueue(self, queueName):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
      
    if exists(queuePath):
      try:
        os.rmdir(queuePath)
        del self.itemDBConf_dict['queues'][queueName]
        saveItemDBConfiguration(self.itemDBConf_dict)
        logInfo("Queue:[{}] is deleted".format(queuePath))
      except Exception as e: 
        logExceptionWithValueError("failed to delete a queue:[{}] at [{}]  -> {}".format(queueName, queuePath, e))
    else:    
      if queueName in ['itemDB']:
        raiseValueError("Queue:[{}] can't be deleted".format(queueName))
      else:
        raiseValueError("Queue:[{}] is not found".format(queuePath))

    return queueName   
  
  def existQueue(self, queueName):
    tablePath = "{}/__queue__{}".format(self.connItemDB, queueName)
      
    if exists(tablePath):
      #logDebug("queue:[{}] is existed.".format(queueName))
      return True
    else:    
      #logDebug("queue:[{}] is not found".format(queueName))
      return False
    
  def putQueue(self, queueName, key, value):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
    
    if exists(queuePath):
      dirEntryStatInfo = os.stat(queuePath)
      #logDebug("queuePath:[{}] -> dirEntryStatInfo:[{}]".format(queuePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__queue__" in queuePath:
        #logDebug("Queue:[{}] is found".format(queuePath))
        
        try:
          hashedB64Key = base64.b64encode(key.encode()).decode()
          objectPath = "{}/{}".format(queuePath, hashedB64Key)
          f = open(objectPath, "w")
          f.write(value)
          f.close()
          #logDebug("Queue:[{}], Key:[{}] -> hashedB64Key:[{}] -> Value:[len({})] is stored.".format(queuePath, key, hashedB64Key, len(value)))
        except Exception as e: 
          logExceptionWithValueError("failed to store key:[{}],value:[len({})] at Queue:[{}]  -> {}".format(key, len(value), queuePath, e))   
          
    else:
      raiseValueError("Queue:[{}] is not found".format(queuePath))
    
    return queueName
  
  def getQueue(self, queueName, key):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
    
    value = None
    
    if exists(queuePath):
      dirEntryStatInfo = os.stat(queuePath)
      #logDebug("queuePath:[{}] -> dirEntryStatInfo:[{}]".format(queuePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__queue__" in queuePath:
        #logDebug("Queue:[{}] is found".format(queuePath))
        
        hashedB64Key = base64.b64encode(key.encode()).decode()
        objectPath = "{}/{}".format(queuePath, hashedB64Key)
        if exists(objectPath):
          try:
            f = open(objectPath, "r")
            value = f.read()
            f.close()
            #logDebug("Queue:[{}], Key:[{}] -> hashedB64Key:[{}] -> Value:[len({})] is read.".format(queuePath, key, hashedB64Key, len(value)))
            
            os.remove(objectPath)
            #logDebug("Queue:[{}], Key:[{}] is deleted.".format(queuePath, key))
            
          except Exception as e:
            logExceptionWithValueError("failed to read key:[{}] at Queue:[{}] -> {}".format(key, len(value), queuePath, e))
        else:
          raiseValueError("Queue:[{}]->Key:[{}] is not found".format(queueName, key))   
          
    else:
      raiseValueError("Queue:[{}] is not found".format(queuePath))
    
    return value
  
  def deleteQueueItem(self, queueName, key):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
    
    if exists(queuePath):
      dirEntryStatInfo = os.stat(queuePath)
      #logDebug("queuePath:[{}] -> dirEntryStatInfo:[{}]".format(queuePath, dirEntryStatInfo))
      
      if stat.S_ISDIR(dirEntryStatInfo.st_mode) and "__queue__" in queuePath:
        #logDebug("Queue:[{}] is found".format(queuePath))
        
        hashedB64Key = base64.b64encode(key.encode()).decode()
        objectPath = "{}/{}".format(queuePath, hashedB64Key)
        if exists(objectPath):
          try:
            os.remove(objectPath)
            logInfo("Queue:[{}], Key:[{}] -> hashedB64Key:[{}] is deleted.".format(queuePath, key, hashedB64Key))
          except Exception as e: 
            logExceptionWithValueError("failed to delete key:[{}] -> hashedB64Key:[{}] at Queue:[{}] -> {}".format(key, hashedB64Key, queuePath, e))  
        else:
          raiseValueError("Queue:[{}]->Key:[{}] is not found".format(queueName, key))
           
    else:
      raiseValueError("Queue:[{}] is not found".format(queuePath))
    
    return queueName
    
  def listQueueItems(self, queueName, maxNumberOfQueueItems = -1):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
    
    item_list = []
    
    if exists(queuePath):
      
      dirEntryList = os.listdir(queuePath)
      
      if maxNumberOfQueueItems > 0:
        
        thisDirEntryCount = 0
        for dirEntryName in dirEntryList:
          if thisDirEntryCount > maxNumberOfQueueItems:
            break
          
          decodedHashedB64Key = base64.b64decode(dirEntryName.encode()).decode()
          item_list.append(decodedHashedB64Key)
          
          thisDirEntryCount += 1
      else:
        for dirEntryName in dirEntryList:
          decodedHashedB64Key = base64.b64decode(dirEntryName.encode()).decode()
          
          item_list.append(decodedHashedB64Key)
          
      return item_list
          
    else:
      raiseValueError("Queue:[{}] is not found".format(queuePath))
      
    return item_list  
  
  def existQueueItem(self, queueName, key):
    queuePath = "{}/__queue__{}".format(self.connItemDB, queueName)
    
    if exists(queuePath):
      #logDebug("'gcItemDB':queue:[{}] -> is existed.".format(queueName))
      
      hashedB64Key = base64.b64encode(key.encode()).decode()
      objectPath = "{}/{}".format(queuePath, hashedB64Key)
      if exists(objectPath):
        #logDebug("'gcItemDB':queue:[{}] -> key:[{}] -> hashedB64Key:[{}] is existed.".format(queueName, key, hashedB64Key))
        return True
      else:    
        #logDebug("'gcItemDB':queue:[{}] -> key:[{}] -> hashedB64Key:[{}] is not found".format(queueName, key, hashedB64Key))
        return False
    
    else:
      #logDebug("'gcItemDB':queue:[{}] is not found".format(queueName))
      return False

  def getAttributes(self, table, key):
    tablePath = "{}/__table__{}".format(self.connItemDB, table)
    
    hashedB64Key = base64.b64encode(key.encode()).decode()
    objectPath = "{}/{}".format(tablePath, hashedB64Key)
    
    try:
      dirEntryStatInfo = os.stat(objectPath)
      #logDebug("objectPath:[{}] -> dirEntryStatInfo:[{}]".format(objectPath, dirEntryStatInfo))
      return {
        "createTime": dirEntryStatInfo.st_birthtime
      }
    
    except Exception as e: 
      logExceptionWithValueError("failed to get the creation date of table:[{}],keyName:[{}] -> Error:[{}]".format(table, key, e))
    
      
    
