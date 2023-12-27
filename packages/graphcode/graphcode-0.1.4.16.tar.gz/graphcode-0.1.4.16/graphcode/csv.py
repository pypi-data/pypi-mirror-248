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
from graphcode.conf import getDownloadPath

from graphcode.aws.s3 import downloadS3Object

from graphcode.lib import getDateString

from os.path import expanduser, join

import secrets

import csv

import time

class GcCsv():
  def __init__(self, result, gc_dict = None, columnNames= None, csvFilename = None):
    if isinstance(result, list):
      if len(result) > 0:
        #logDebug("type:{}:result(len:[{}])[-1]:{}".format(type(result), len(result), result[-1]))
        logDebug("type:{}:result(len:[{}])".format(type(result), len(result)))
        #if isinstance(result[0], dict):
        #  logDebug("keys:[{}]".format(result[0].keys()))
      else:
        logDebug("type:{}:result(len:[{}]):{}".format(type(result), len(result), result))
      
    else:
      if isinstance(result, dict):
        raiseValueError("Error:[type:{} is provided that must be be 'list' type]->result.keys(len:{:,}):{}".format(type(result), len(result.keys()), result.keys()))
      else:
        raiseValueError("Error:[type:{} is provided that must be be 'list' type]->result(len:[{:,}]):{}".format(type(result), len(result), result))
    
    #self.gc_dict = gc_dict
    self.result_list = result
    self.columnName_list = columnNames
    self.csvFilename = csvFilename
    self.csvData_list = None
    self.csvData = None
    
    
    self.totalNumberOfRows = len(self.result_list)
    if self.totalNumberOfRows  > 2000000:
      self.percentageDelimiter = int(self.totalNumberOfRows / 10)
    elif self.totalNumberOfRows  > 500000:
      self.percentageDelimiter = int(self.totalNumberOfRows / 5)
    elif self.totalNumberOfRows  > 10:
      self.percentageDelimiter = int(self.totalNumberOfRows / 3)
    else:
      self.percentageDelimiter = 1
    logDebug("loaded {:,} rows->percentageDelimiter:[{}]".format(self.totalNumberOfRows, self.percentageDelimiter))
    
    
  def get(self, format=None):
    logDebug("generating csvFile with {:,} rows".format(self.totalNumberOfRows))
    if isinstance(self.result_list, list):
      if isinstance(format, str) and format == "binary":
        self.csvData = self.getCsvDataFromList()
        
        return self.getCsvRows().encode()
      
      elif isinstance(self.result_list, list):
        try:
          self.csvData = self.getCsvDataFromList()
        except:
          self.csvData = "error\n{}".format(logException("unable to get CSV Data"))
    
      else:
        logError("result:type:{} must be 'list'".format(type(self.result_list)))
        self.csvData = None
    else:
      logError("result:type:{} must be 'list'".format(type(self.result_list)))
      self.csvData = None
      
    return self.csvData
  
  def getSample(self, length=1000):
    logDebug("generating csvFile with {:,} rows".format(self.totalNumberOfRows))
    if isinstance(self.result_list, list):
      try:
        self.csvData = self.getCsvDataFromList(length=length)
      except:
        self.csvData = "error\n{}".format(logException("unable to get CSV Data"))
  
    else:
      logError("result:type:{} must be 'list'".format(type(self.result_list)))
      self.csvData = None
      
    return self.csvData
  
  def getCsvDataFromList(self, length=None):
    logDebug("collecting the columnNames")
    
    rowCount = 0
    previousColumnCount = 0
    noDeltaRowCount = 0
    self.columnName_list = []
    self.columnName_dict = {}
    __beginTime__ = time.time()
    for resultItem_dict in self.result_list:
      for columnName in resultItem_dict.keys():
        if columnName in self.columnName_dict.keys():
          pass
        else:
          self.columnName_list.append(columnName)
          self.columnName_dict[columnName] = None
      
      rowCount += 1
      if (rowCount % self.percentageDelimiter) == 0:
        logDebug("(#{:,}/{:,})\tprocessed with columnName_list(len:{:,}):[{}]".format(rowCount, self.totalNumberOfRows, len(self.columnName_list), self.columnName_list))
        
        if previousColumnCount == len(self.columnName_list):
          if noDeltaRowCount > 1:
            break
          else:
            noDeltaRowCount += 1
        else:
          previousColumnCount = len(self.columnName_list)
          noDeltaRowCount = 0
    
    if (time.time()-__beginTime__) > 0.5:
      logDebug("#---->processTime:{:.2f}s".format(time.time()-__beginTime__))
    
    self.csvData_list = []
    logDebug("generating {:,} rows".format(self.totalNumberOfRows))
    rowCount = 0
    __beginTime__ = time.time()
    for resultItem_dict in self.result_list:
      rowCount += 1
      if rowCount == 1 or (rowCount % self.percentageDelimiter) == 0:
        
        processTime = ((time.time() - __beginTime__) / rowCount) * 1000
        if processTime > 1:
          logWarn("(#{:,}/{:,})\taverage process time:[{:.3f}]ms per row with {:,} columns".format(rowCount, self.totalNumberOfRows, processTime, len(self.columnName_list)))
          logWarn("(#{:,}/{:,})\tself.csvData_list[-1]:[{}]".format(rowCount, self.totalNumberOfRows,self.csvData_list[-1]))
          
        #else:
        #  logDebug("(#{:,}/{:,})\taverage process time:[{:.3f}]ms per row to generate a csv row".format(rowCount, self.totalNumberOfRows, processTime))
      
      line_list = []
      for columnName in self.columnName_list:
        try:
          if columnName in resultItem_dict.keys():
            if resultItem_dict[columnName] in [None, "None"]:
              line_list.append("")
            else:
              line_list.append(resultItem_dict[columnName])
          else:
            line_list.append("")
        except:
          line_list.append("")
          #logException("unable to append:[{}] with resultItem_dict:[{}]".format(columnName, resultItem_dict.keys()))
      self.csvData_list.append(line_list)
      
      if length != None and len(self.csvData_list) > length:
        return {"count":len(self.result_list)*-1, "labels": self.columnName_list, "data": self.csvData_list}
    
    if len(self.csvData_list) > 1000:
      thisCsvData_list = []
      for csvItem_dict in self.csvData_list:
        thisCsvData_list.append(csvItem_dict)
        if len(thisCsvData_list) > 1000:
          break
        
      return {"count":len(self.csvData_list), "labels": self.columnName_list, "data": thisCsvData_list}
    
    else:
      return {"count":len(self.csvData_list), "labels": self.columnName_list, "data": self.csvData_list}
   
  def save(self, csvFilename = "a.csv", tokenSize = 16, attachingDate = True):
    csvOffset = csvFilename.lower().find(".csv")
    if tokenSize > 0:
      if attachingDate:
        thisCsvFilename = csvFilename[:csvOffset] + "_{}_".format(secrets.token_urlsafe(tokenSize)) + "_{}".format(getDateString("now", "fileTimestamp")) + csvFilename[csvOffset:]
      else:
        thisCsvFilename = csvFilename[:csvOffset] + "_{}_".format(secrets.token_urlsafe(tokenSize)) + csvFilename[csvOffset:]
    else:
      if attachingDate:
        thisCsvFilename = csvFilename[:csvOffset] + "_{}".format(getDateString("now", "fileTimestamp")) + csvFilename[csvOffset:]
      else:
        pass
        #csvFilename = csvFilename[:csvOffset] + csvFilename[csvOffset:]
    
    f = open(thisCsvFilename,"w")
    logDebug("opened: csvFilename:[{}]".format(thisCsvFilename))
    csvData = self.getCsvRows()
    logDebug("filename:[{}](size:{:,})".format(csvFilename, len(csvData)))
    
    f.write(csvData)
    logDebug("completed to write data tofile:///{}".format(thisCsvFilename))
      
    f.close()
    
    return thisCsvFilename
  
  def getCsvRows(self):
    csvHeadLine = ""
    if len(self.columnName_list) == 0:
      logWarn("no column names")
    else:
      if isinstance(self.columnName_list, list):
        for columnName in self.columnName_list:
          if csvHeadLine == "":
            csvHeadLine += "\"{}\"".format(columnName)
          else:
            csvHeadLine += ",\"{}\"".format(columnName)
        csvHeadLine += "\n"
        #f.write(csvHeadLine)
    
    csvRows = ""    
    if len(self.columnName_list) == 0:
      logWarn("no csv data rows")
    else:
      if isinstance(self.csvData_list, list):
        for csvValue_list in self.csvData_list:
          csvDataRow = ""
          for columnValue in csvValue_list:
            if csvDataRow == "":
              csvDataRow += "\"{}\"".format("{}".format(columnValue).replace('"',"'"))
            else:
              csvDataRow += ",\"{}\"".format("{}".format(columnValue).replace('"',"'"))
          csvDataRow += "\n"
          #f.write(csvDataRow)
          csvRows += csvDataRow
    csvData = csvHeadLine + csvRows
  
    return csvData
  
  def getCsvText(self, result_list):
  
    csvRows = ""
    columnName_list = []
    for resultItem_dict in result_list:
      for columnName in resultItem_dict.keys():
        if columnName in columnName_list:
          pass
        else:
          columnName_list.append(columnName)
          if csvRows == "":
            csvRows += "\"{}\"".format(columnName)
          else:
            csvRows += ",\"{}\"".format(columnName)
    csvRows += "\n"
    #f.write(csvHeadLine)
    
    if len(columnName_list) == 0:
      logWarn("no csv data columns")
      
    else:
      for rowItem_dict in result_list:
        csvDataRow = ""
        for columnName in columnName_list:
          try:
            if rowItem_dict[columnName] not in [None, "None"]:
              cellValue = rowItem_dict[columnName]
            else:
              cellValue = ""
          except:
            cellValue = ""
            
          if csvDataRow == "":
            csvDataRow += "\"{}\"".format("{}".format(cellValue).replace('"',"'"))
          else:
            csvDataRow += ",\"{}\"".format("{}".format(cellValue).replace('"',"'"))
            
        csvDataRow += "\n"
        #f.write(csvDataRow)
        csvRows += csvDataRow
    
    return csvRows

  def csvFilename2dicts(self, csvFilename = None, numberOfLineDelimiter = 3):
    # Get inherited Function Stack Names to see hierarcy of API calls
    logInfo("started loading csvFilename:[{}]".format(csvFilename))
    
    if csvFilename == None:
      raise ValueError("csvFilename shouldn't be None")
    
    csvFilePath = expanduser(csvFilename)
    try:
      f = open(csvFilePath,"r")
    except Exception as e: 
      raiseValueError("failed to open filename:[{}]".format(csvFilePath))
     
    try:
      logDebug("reading csvFile:[{}]".format(csvFilePath))
      
      reader = csv.reader(f)
      lines = list(reader)
      f.close()
      
    except Exception as e: 
      raiseValueError("failed to read CSV lines at filename:[{}]".format(csvFilePath))
    
    try:  
      totalNumberOfCSVRows = len(lines)
      
      logInfo("csvFile:[{}] -> row:{:,} are updated successfully".format(csvFilePath, totalNumberOfCSVRows))
      
      if totalNumberOfCSVRows > 10:
        progressDivider = int(totalNumberOfCSVRows / numberOfLineDelimiter -1)
      else:
        progressDivider = 1
      
      rowCount = 0
      
      if len(lines) < 2: 
        logWarn("csvFile:[{}] has a single line".format(csvFilePath))
        return {}
      
      names = lines[0] # csvColumnNames
      rowCount += 1
      
      targetCsvDict_list = []
      if len(names) < 1: 
        logWarn("csvFile:[{}] dosn't have any line".format(csvFilePath))
        return {}
      
      for values in lines[1:]:
        if len(values) != len(names): 
          logWarn("{}/{}: # of columnNames:[{}] is not equal with csvItems:[{}]".format(rowCount, totalNumberOfCSVRows, names, values))
        
        d = {}
        if len(values) < len(names):
          for i,_ in enumerate(names[:len(values)]):
            if names[i] == "" and values[i] == "":
              continue
            
            d[names[i]] = values[i]
          targetCsvDict_list.append(d)
        else:
          for i,_ in enumerate(names):
            if names[i] == "" and values[i] == "":
              continue
            
            d[names[i]] = values[i]
          targetCsvDict_list.append(d)
        
        rowCount += 1
        if (rowCount % progressDivider) == 0:
          logDebug("csvFile:[{}] -> {:,}/{:,}:converted to type:dict".format(f.name,rowCount,  totalNumberOfCSVRows))
      
      logInfo("csvFile:[{}] -> {:,}/{:,}:converted to type:dict finally".format(f.name, rowCount, totalNumberOfCSVRows))
    except Exception as e: 
      raiseValueError("failed to parse csv data at filename:[{}]".format(csvFilePath))
    
    return targetCsvDict_list


def s3csvObject2dicts(self, bucketName, key, credentialName):
  '''
  try:
    logDebug("reading to S3:[{}]->Key:[{}]".format(bucketName, key))
    
    binaryData = getS3Object("pao-bi", key, "S3-MODUAWS-PAO-BI")
    
    if binaryData == None:
      raise ValueError("key:[{}] in 'None'".format(key))
    
  except Exception as e:
    errorMessage = "Error:[{}] -> failed to read S3://{}/{}".format(e, bucketName, key)
    logError(errorMessage)
    raise ValueError(errorMessage)
  '''
  csvFilename = "{}".format(key)
  '''
  for days in range(30):
    timeStamp = time.time() - days*24*3600
    
    snapshotDate = datetime.fromtimestamp(timeStamp).astimezone(timezone('UTC')).strftime('%Y-%m/%d')
    
    if snapshotDate in key:
      csvFilename = csvFilename.replace(snapshotDate, "")
      snapshotDate = datetime.fromtimestamp(timeStamp).astimezone(timezone('UTC')).strftime('%Y-%m-%d')
      csvFilename = "{}-{}.csv".format(key.replace(".csv",""), snapshotDate)
      break
  '''
  
  homeDir = createDir(join(expanduser(getDownloadPath()), "moduAWS-temp/s3Buckets/{}".format(bucketName)))
  #homeDir = createDir("~/moduAWS-temp/s3Buckets/{}".format(bucketName))
  logDebug("working directory path:[{}]".format(createDir("{}/{}".format(homeDir, csvFilename[:csvFilename.find(csvFilename.split("/")[-1])-1]))))
  csvFilePath = expanduser("{}/{}".format(homeDir, csvFilename))
  
  try:
    logInfo("downloading s3://{}/{} to local:///{}".format(bucketName, key, csvFilePath))
    response = downloadS3Object(bucketName, key, csvFilePath, credentialName)
  except:
    raiseValueError("unable to download s3://{}/{} to csvFilePath:[{}]".format(bucketName, key, csvFilePath))
  
  '''  
  try:
    logDebug("writing:[{}]".format(csvFilePath))
    
    f = open(csvFilePath, "wb")
    f.write(binaryData)
    f.close()
  except:
    logException("unable to write the object as a binary".format("s3://{}/{}".format("pao-bi", key), csvFilePath))
    
    try:
      f = open(csvFilePath, "w")
      f.write(binaryData)
      f.close()
    except:
      logException("unable to write the object of key:[{}] to file:[{}] as text".format("s3://{}/{}".format("pao-bi", key), csvFilePath))
      
      raiseValueError()
  logDebug("listing to S3:[{}]->Key:[{}]".format(bucketName, key))
  '''  
  
  targetCsv_list = self.csvFilename2dicts(csvFilePath)
  
  return targetCsv_list

      
          