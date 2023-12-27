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

from graphcode.delimiter import getDelimiter, displayItemDetails
from graphcode.path import createDir
from graphcode.credentials import GcCrednitals
from graphcode.conf import GcConf
from graphcode.lib import getDateString
from graphcode.unittest import unitTest

import time
from pytz import timezone
from datetime import datetime

import psycopg2

import copy


from os.path import join

#import gcDwTemplates as queryTemplates

#sql_awsdw_dict = queryTemplates.sql_awsdw_dict

from tammy.awsdw.templates import GcDwTemplates

import json

ec2BillingProdcut_dict = {
  "bp-68a54001":   "Windows 2003 Enterprise",#
  "bp-6ba54002":   "Windows 2003 Datacenter",#   #RunInstances:0002
  "bp-6aa54003":   "SQL Server 2005 Standard",#  #RunInstances:0004
  "bp-6da54004":   "Licensed (Unused)",#   RunInstances:0008
  "bp-6ca54005":   "Novell Paid Linux (Suse)",#   RunInstances:000g
  "bp-6fa54006":   "Red Hat Paid Linux",#   RunInstances:0010
  "bp-6ea54007":   "RDS Oracle SE1 License Included",#   RunInstances:0020
  "bp-61a54008":   "RDS Oracle SE2 License Included",#  RunInstances:0040
  "bp-60a54009":   "Cluster Corp Paid Linux",# (mostly unused)",#   RunInstances:0080
  "bp-63a5400a":   "Red Hat BYOL Linux",#   RunInstances:00g0
  "bp-62a5400b":   "SQL Server Enterprise",#   RunInstances:0100
  "bp-65a5400c":   "SQL Server Web",#   RunInstances:0200
  "bp-64a5400d":   "RDS Oracle BYOL",#   RunInstances:0400
  "bp-67a5400e":   "Windows BYOL",#   RunInstances:0800
  "bp-66a5400f":   "Ubuntu Pro Linux",# (Placeholder)   RunInstances:0g00 
  }

'''
https://w.amazon.com/bin/view/EC2/DropletMeteringService/BillingProducts/
1   bp-68a54001   Windows 2003 Enterprise (Not actively used, where it still exists it maps to RunInstances:0002)   RunInstances:0002
2   bp-6ba54002   Windows 2003 Datacenter   RunInstances:0002
3   bp-6aa54003   SQL Server 2005 Standard   RunInstances:0004
4   bp-6da54004   Licensed (Unused)   RunInstances:0008
5   bp-6ca54005   Novell Paid Linux (Suse)   RunInstances:000g
6   bp-6fa54006   Red Hat Paid Linux   RunInstances:0010
7   bp-6ea54007   RDS Oracle SE1 License Included   RunInstances:0020
8   bp-61a54008   RDS Oracle SE2 License Included   RunInstances:0040
9   bp-60a54009   Cluster Corp Paid Linux (mostly unused)   RunInstances:0080
10   bp-63a5400a   Red Hat BYOL Linux   RunInstances:00g0
11   bp-62a5400b   SQL Server Enterprise   RunInstances:0100
12   bp-65a5400c   SQL Server Web   RunInstances:0200
13   bp-64a5400d   RDS Oracle BYOL   RunInstances:0400
14   bp-67a5400e   Windows BYOL   RunInstances:0800
15   bp-66a5400f   Ubuntu Pro Linux (Placeholder)   RunInstances:0g00 
'''


class GcDw():
  def __init__(self):
    logDebug("started")
    
    self.__beginTime__ = time.time()
    
    gcConf = GcConf("./")
    self.CSV_HOME_DIR = createDir(join(gcConf.getHomeDirectory(), "moduAWS-temp"))
    
    self.gcCredentials = GcCrednitals()
    
    self.gcDwTemplates = GcDwTemplates()
  
  def connectDW(self, dwName):
    if dwName == 'aws':
      try:
        username, pw = self.gcCredentials.get("AWSDW")
        #logDebug("username:[{}], pw:[{}]".format(username, pw))
        return psycopg2.connect(database='awsdw', 
                              user=username, 
                              password=pw, 
                              host='awsdw-rs-adhoc1.db.amazon.com', 
                              port='8192', 
                              sslmode='require')
      except Exception as e: 
        errorMessage = "Error({}): Unable to connect to the database!".format(e)
        logError(errorMessage)
        raise ValueError(errorMessage)
      
    elif dwName == 'awssupportdw':
      try:
        username, pw = self.gcCredentials.get("AWSDWSUPPORT")
        #logDebug("username:[{}], pw:[{}]".format(username, pw))
        return psycopg2.connect(database='awssupportdw02', 
                              user=username, 
                              password=pw, 
                              #host='awssupport-rs-secondary-ro.db.amazon.com', #Deprecated
                              #host='awssupport-rs-primary-ro.db.amazon.com',  #Deprecated
                              #host='awssupportdw-rs-cluster2.db.amazon.com',  #Deprecated
                              host='awssupportdw-rs-cluster2.db.amazon.com',
                              port='8192', 
                              sslmode='require')
      except Exception as e: 
        errorMessage =   "Error({}): Unable to connect to the database!".format(e.replace("\n",""))
        logError(errorMessage)
        raise ValueError(errorMessage)
      
    else:
      return None   
  
  def run_awsdw_query(self, dwName, query_string):  
    __beginTime__ = time.time()
    
    #if getLogLevel() == "UNITTEST":
    #  print (query_string.replace("  ", ""))
    
    try:
      logInfo("Trying to connect DW:[{}]...".format( dwName))
      
      conn = self.connectDW(dwName)
      
      if conn != None:
        logInfo("Connected successfully at [{}]!".format(conn))
      
      else:
        raiseValueError("failed to connect at {}:[{}]!".format(dwName, ""))
    
    except Exception as e: 
      logExceptionWithValueError("failed to connect at {}:[{}]!".format(dwName, ""))
      
    try:
      logInfo("Trying to access DW:[{}]...".format(dwName))
      cur = conn.cursor()
      logInfo("database:[{}] accessed successfully!".format(dwName))
      
    except Exception as e: 
      logExceptionWithValueError("Unable to access to the database:[{}]!".format(dwName))
    
      if len(query_string.replace("   ","")) > 500:
        logInfo("Start the query to DW:[{}] with [{}\n...\n{}]".format( dwName, (query_string.replace("   ",""))[:300], (query_string.replace("   ",""))[-199:]))
        #print(query_string.replace("   ",""))
      else:
        logInfo("Start the query to DW:[{}] with[{}]".format( dwName, query_string.replace("   ","")))
      
    result_list = []
    statement_list = []
    for thisSqlStatment in query_string.split(";"):
      if len(thisSqlStatment.strip()) > 0:
        statement_list.append(thisSqlStatment)

    statementNumber = len(statement_list)
    statementCount = 0
    for statement in statement_list:
      statementCount += 1
      
      thisResult_dict = {
        "#": statementCount,
        "statement": statement,
        "columnName_list":[],
        "rows":None,
        "errorReasons":[]
        }
      
      try:
        statement = statement.strip() + "\n;"
        statementSize = len(statement)
        if statementSize > 0:
          if statementSize > 2000:
            logDebug("(#{:,}/{:,},statementSize:{:,}Bytes):[{}....{}]".format(statementCount, statementNumber, statementSize, statement[:500], statement[-500:]))
          else:
            logDebug("(#{:,}/{:,},statementSize:{:,}Bytes):[{}]".format(statementCount, statementNumber, statementSize, statement))
        else:
          logDebug("(#{:,}/{:,},statementSize:{:,}Bytes):[{}]".format(statementCount, statementNumber, statementSize, statement))
          continue
        
        cur.execute(statement)
        logInfo("Query was executed successfully!n" )
        
        try:
          thisResult_dict["columnName_list"] = [desc[0] for desc in cur.description]
        except Exception as e:
          thisResult_dict["columnName_list"] = []
          thisResult_dict["errorReasons"].append(logError("unexpected cur.description:[{}]->Error:[{}]".format(cur.description, e)))
          continue
      except Exception as e: 
        thisResult_dict["errorReasons"].append(logError("failed to execute the query:[{}]->Error:[{}]".format(query_string, e)))
      
      try:
        if thisResult_dict["rows"] == None:
          logInfo("runTime:[{:.3f}]s fetching and storing rows to [{}]".format(time.time()-__beginTime__, thisResult_dict["rows"]))
          thisResult_dict["rows"] = cur.fetchall()
        else:
          logInfo("runTime:[{:.3f}]s fetching and storing rows into [{:,}]".format(time.time()-__beginTime__, len(thisResult_dict["rows"])))
          for thisRow in cur.fetchall():
            thisResult_dict["rows"].append(thisRow)
        logInfo("runTime:[{:.3f}]s fetched rows with {:,} rows...".format(time.time()-__beginTime__, len(thisResult_dict["rows"])) )
            
      except Exception as e: 
        thisResult_dict["errorReasons"].append("Unable to fetch the rows!->Error:[{}]".format(e))
      
      result_list.append(thisResult_dict)
      
    try:
      logInfo("runTime:[{:.3f}]s Closing the DW connection with {:,} rows...".format(time.time()-__beginTime__, len(thisResult_dict["rows"])) )
      cur.close()
      conn.close()
      logInfo("Done" )
    except Exception as e: 
      logExceptionWithValueError("Error({}): Unable to close the DW:{} connection!".format( e, dwName))
    
    return result_list
  
  def queryAWSDW(self, dwName, queryStatement = None):
    __beginTime__ = time.time()
    
    fetchedRow_list = []
    columnName_list = []
    try:
      if len(queryStatement.replace("  ","")) > 300:
        logInfo("Task-001:[query] query to database:[{}] with [{}......\n......\n{}](len:{:,})".format(dwName, (queryStatement)[:150],queryStatement[-150:], len(queryStatement)))
      else:
        logInfo("Task-001:[query] query to database:[{}] with [{}](len:{:,})".format(dwName, queryStatement, len(queryStatement)))
     
      result_list = self.run_awsdw_query(dwName, queryStatement)
      
      
      logInfo("Task-001:[query] (runTime:[{:.3f}] Completed successfully!!!!".format(time.time()-__beginTime__))
      
    except: 
      logExceptionWithValueError("Task-001:[query] wasn't able to be completed...")
    
    
    itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=result_list, divider=3)
    for resultItem_dict in result_list:
      itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, resultItem_dict.keys(), itemName="resultItem_dict.keys()")

      thisFetchedRow_list =  resultItem_dict["rows"]
      thisColumnName_list = resultItem_dict["columnName_list"]
      
      if thisColumnName_list != None and len(thisColumnName_list) > 0:
        try:
          logInfo("Task-002:[fetching] Writing {:,} rows to CSV".format(len(thisColumnName_list)))
          
          for thisColumnName in thisColumnName_list:
            if thisColumnName not in columnName_list:
              columnName_list.append(thisColumnName)

          filename = "{}/{}_{}_{}.csv".format(self.CSV_HOME_DIR, dwName, "results", getDateString("now", "fileTimestamp  "))
          f = open(filename,'w')
          logInfo("Task-002:[fetching] opened a CSV file:[{}] to write the results of the query successfully.".format( filename) )
            
          countColumnName = 0
          totalColumnName = len(thisColumnName_list)
          msg = ""
          for columnName in thisColumnName_list:
            countColumnName += 1
            
            msg += columnName
            
            if countColumnName < totalColumnName:
              msg += ","
        
          f.write(msg +"\n")
          logInfo("Task-002: Writing results of query to CSV with columnNames:[{}]".format( msg))
          
          for row in thisFetchedRow_list:
            
            fetchedRow_list.append(row)

            try:
              json.dumps(row)
              line = row
            
            except:
              line = row[0]
              for column in row[1:]:   
                if isinstance(column, type(None)):
                    column = ""
                else:
                  column = "{}".format(column)   
                  try:
                    column = "{}".format(column.encode('ascii', 'ignore'))
                    column = "{}".format(column[2:len(column)-1])
                  except Exception as e: 
                    column = "{}".format(bytes(column,'utf-8'))
                    column = "{}".format(column[2:len(column)-1])
                    
                    logError("Task-002:[fetching] unable to write column data:[{}] by ASCII. So, it's encoded to utf-8.->Error:[{}]".format(bytes(column,'utf-8',e)))
                      
                line = "{},\"{}\"".format(line, column)
      
            line = "{}\n".format(line)
            f.write(line)
          f.close() 
      
          logInfo("Task-002:[fetching] (runTime:[{:.3f}] Completed successfully!!!!".format(time.time()-__beginTime__))
          
        except Exception as e: 
          raiseValueError("Task-002:[fetching] wasn't able to be completed...".format(e))
          
      else:
        logInfo("Task-002:[fetching] (runTime:[{:.3f}] Completed, but the result is none!!".format(time.time()-__beginTime__) )
  
    return fetchedRow_list, columnName_list
  
  def queryRunToAWSDWWithSQL(self, dwName, sqlFilename):
    f = open(sqlFilename, "r")
    sql = f.read()  
    logInfo("SQL is called with [{}].".format( sql))
    self.queryAWSDW(dwName, sql)
  
  def getAccountInfoFromAWSDW(self, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryStatement = self.gcDwTemplates.getQueryString('aws_account')
    
    self.gcDwTemplates.updateQueryString('aws_account', queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW('aws_account', self.gcDwTemplates.getQueryString('aws_account'))
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    accountInfo_dict = {}
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format( numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      countColumn = 0
    
      if accountId not in accountInfo_dict.keys():
        accountInfo_dict[accountId] = {}
  
      for columnName in columnNames:
        if columnName in accountInfo_dict[accountId].keys():
          if accountInfo_dict[accountId][columnName] != "":
            logWarn("{} is already updated at accountId:{}".format( columnName, accountId))
          else:
            accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
            #logInfo("{} is updated at accountId:{}, as the column data was empty.".format( columnName, accountId))
        else:
          accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
          #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
        countColumn += 1
    
    return accountInfo_dict
  
  def getNoneInternalAccountInfoFromAWSDW(self, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryStatement = self.gcDwTemplates.getQueryString('none_internal_account')
    
    self.gcDwTemplates.updateQueryString('aws_account', queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW('aws_account', self.gcDwTemplates.getQueryString('aws_account'))
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    accountInfo_dict = {}
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format( numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      countColumn = 0
    
      if accountId not in accountInfo_dict.keys():
        accountInfo_dict[accountId] = {}
  
      for columnName in columnNames:
        if columnName in accountInfo_dict[accountId].keys():
          if accountInfo_dict[accountId][columnName] != "":
            logWarn("{} is already updated at accountId:{}".format( columnName, accountId))
          else:
            accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
            #logInfo("{} is updated at accountId:{}, as the column data was empty.".format( columnName, accountId))
        else:
          accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
          #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
        countColumn += 1
    
    return accountInfo_dict
  
  def updateAccountInfoFromAWSDW(self, accountInfo_dict, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString('aws_account')
    
    self.gcDwTemplates.updateQueryString('aws_account', queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW('aws_account', self.gcDwTemplates.getQueryString('aws_account'))
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format( numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      countColumn = 0
    
      if accountId not in accountInfo_dict.keys():
        accountInfo_dict[accountId] = {}
  
      for columnName in columnNames:
        if columnName in accountInfo_dict[accountId].keys():
          if accountInfo_dict[accountId][columnName] != "":
            logDebug("{} is already updated at accountId:{}".format( columnName, accountId))
          else:
            accountInfo_dict[accountId][columnName] = row[countColumn]
            logInfo("{} is updated at accountId:{}, as the column data was empty.".format( columnName, accountId))
        else:
          accountInfo_dict[accountId][columnName] = row[countColumn]
          logDebug("{} is updated at accountId:{}".format(columnName, accountId))
        countColumn += 1
      
      if 'dataSource' in accountInfo_dict[accountId].keys():
        if "NoInternal" not in accountInfo_dict[accountId]['dataSource']:
          accountInfo_dict[accountId]['dataSource'].append("NoInternal")
        else:
          accountInfo_dict[accountId]['dataSource'] = ["NoInternal"]
      else:
        accountInfo_dict[accountId]['dataSource'] = ["NoInternal"]
  
      
  def getInternalAccountsFromAWSDW(self):
    queryResult_list, columnNames = self.queryAWSDW('internal_account')
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results: {} rows with column names(len:{}):[{}]".format(totalRows, totalColumns, columnNames))
    
    accountInfo_dict = {}
    accountCount = 0
    accountDelimiter = int(totalRows/6)
    for row in queryResult_list:
      try:
        accountCount += 1
        
        numberOfItemsOfRow = len(row)
        if numberOfItemsOfRow != totalColumns:
          logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
        
        accountId = row[0]
        countColumn = 0
      
        if accountId in accountInfo_dict.keys():
          if (accountCount % accountDelimiter) == 0:
            logDebug('accountId:[{}] is already added at accountInfo_dict!'.format(accountId))   
        else:
          accountInfo_dict[accountId] = {}
          if (accountCount % accountDelimiter) == 0:
            logDebug("({}/{}) accountId:{} is added at accountInfo_dict!".format(accountCount, totalRows, accountId))
    
        for columnName in columnNames:
          accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
          countColumn += 1
      except:
        logException("unable to set the results")
    
    logDebug("total {} accounts are updated".format(len(accountInfo_dict.keys())))
    
    return accountInfo_dict

  def getInternalAccountInfoWithList(self, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryStatement = self.gcDwTemplates.getQueryString('internal_account_list')
    
    self.gcDwTemplates.updateQueryString('internal_account_list', queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW('internal_account_list', self.gcDwTemplates.getQueryString('internal_account_list'))
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    accountInfo_dict = {}
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format( numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      countColumn = 0
    
      if accountId not in accountInfo_dict.keys():
        accountInfo_dict[accountId] = {}
  
      for columnName in columnNames:
        if columnName in accountInfo_dict[accountId].keys():
          if accountInfo_dict[accountId][columnName] != "":
            logWarn("{} is already updated at accountId:{}".format( columnName, accountId))
          else:
            accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
            #logInfo("{} is updated at accountId:{}, as the column data was empty.".format( columnName, accountId))
        else:
          accountInfo_dict[accountId][columnName] = "{}".format(row[countColumn])
          #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
        countColumn += 1
      
    return accountInfo_dict
  
  def updateInternalAccountsFromAWSDW(self, accountInfo_dict):
    queryResult_list, columnNames = self.queryAWSDW('internal_account')
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results: {} rows with column names(len:{}):[{}]".format(totalRows, totalColumns, columnNames))
    
    accountCount = 0
    accountDelimiter = int(totalRows/6)
    for row in queryResult_list:
      accountCount += 1
      
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      countColumn = 0
    
      if accountId in accountInfo_dict.keys():
        if (accountCount % accountDelimiter) == 0:
          logDebug('accountId:[{}] is already added at accountInfo_dict!'.accountId)   
      else:
        accountInfo_dict[accountId] = {}
        if (accountCount % accountDelimiter) == 0:
          logDebug("accountId:{} is added at accountInfo_dict!".format( accountId))
  
      for columnName in columnNames:
        accountInfo_dict[accountId][columnName] = row[countColumn]
        countColumn += 1
      
      if 'dataSource' in accountInfo_dict[accountId].keys():
        if "AWSDW" in accountInfo_dict[accountId]['dataSource']:
          logDebug("accountId:[{}] is already added with AWSDW!")
        else:
          accountInfo_dict[accountId]['dataSource'].append("AWSDW")
      else:
        accountInfo_dict[accountId]['dataSource'] = ["AWSDW"]
  
  def updateEC2InEC2Classic(self, accountId_list):
    logInfo("{}")
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString('ec2_in_EC2_CLASSIC')
    self.gcDwTemplates.updateQueryString('ec2_in_EC2_CLASSIC', queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW('ec2_in_EC2_CLASSIC', self.gcDwTemplates.getQueryString('ec2_in_EC2_CLASSIC'))
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
  def getAWSResourcesFromAWSDW(self, startDate, endDate):
    queryName = 'awsResourcesByUsageOfInternalAccounts'
    
    logInfo("{}")
    
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    return [queryResult_list, columnNames]
  
  def getAwsProductUsageByProductName(self, accountId_list, startDate, endDate, serviceName = None):
    
    if serviceName != None:
      queryName = 'awsProductUsageByProductName'
    else:
      queryName = "awsProductUsageByAccountId"
    
    logInfo("accountId_list:[len:{}], startDate:[{}], endDate:[{}], serviceName:[{}]".format(len(accountId_list), startDate, endDate, serviceName))
    
    accountIds = ""
    if isinstance(accountId_list, list):
      for accountId in accountId_list:
        if accountIds == "":
          accountIds = "'{}'".format(accountId)
        else:
          accountIds = "{},'{}'".format(accountIds, accountId)
    elif isinstance(accountId_list, str):
      accountIds = accountId_list
        
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = copy.deepcopy(self.gcDwTemplates.getQueryString(queryName))
    if serviceName != None:
      thisQueryString = queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate).replace("${{PRODUCT_NAME}}", serviceName).replace("  "," ")
    else:
      thisQueryString = queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate).replace("  "," ")
    logDebug("thisQueryString:[{}]".format(thisQueryString))
    #print(thisQueryString)
    self.gcDwTemplates.updateQueryString(queryName, thisQueryString)
    
    try:
      queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    except Exception as e:
      errorMessage = "Error[{}] -> unable to query".format(e)
      logError(errorMessage)
      
      queryResult_list = []
    
    service_dict = {}
    if queryResult_list != None:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
        #[queryResult_list, columnNames]
      for queryResultItems in queryResult_list:
        logDebug("queryResultItems:[{}]".format(queryResultItems))
        
        thisResult_dict = {}
        
        columnCount = 0
        for colunName in columnNames:
          thisResult_dict[colunName] = queryResultItems[columnCount]
          columnCount+=1
        
        if thisResult_dict["account_id"] in service_dict.keys():
          if thisResult_dict["product_name"] in service_dict[thisResult_dict["account_id"]].keys():
            if thisResult_dict["region_name"] in service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]].keys():
              pass
            else:
              service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]][thisResult_dict["region_name"]] = {}
          else:
            service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]] = {}
            service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]][thisResult_dict["region_name"]] = {}
        else:
          service_dict[thisResult_dict["account_id"]] = {}
          service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]] = {}
          service_dict[thisResult_dict["account_id"]][thisResult_dict["product_name"]][thisResult_dict["region_name"]] = {}
        
    result_list = []
    for accountId in service_dict.keys():
      for serviceName in service_dict[accountId].keys():
        for regionCode in service_dict[accountId][serviceName].keys():
          #if regionCode != "" or regionCode.replace(" ","") != "":
          if regionCode != "":
            if regionCode[-1] in ["a","b","c","e","f","g","h","i"]:
              avaiabilityZone = regionCode
              regionCode = regionCode[:-1]
            else:
              avaiabilityZone = ""
              regionCode = regionCode
          else:
            avaiabilityZone = ""
            
          result_list.append({"accountId":accountId, "serviceName":serviceName, "regionCode":regionCode, "avaiabilityZone":avaiabilityZone})
    
    logInfo("total {} accounts have {} items with serviceName:[{}]".format(len(service_dict.keys()), len(result_list), serviceName))
    
    return result_list

  
  def getAWSProductNamesFromCDOUsage(self, accountId_list, startDate, endDate):
    queryName = 'awsProductNamesByusage'
    
    logInfo("{}")
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
      
    
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    return [queryResult_list, columnNames]

  
  def getAWSProductNamesFromAllInternalAccounts(self, startDate, endDate):
    queryName = 'awsProductNamesByusageWithInternalAccounts'
    
    logInfo("{}")
    
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    return [queryResult_list, columnNames]
  
  def getCaseDetailsWithAccountIDList(self, accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    thisTime = time.time()
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'case_details_with_account_ids_v2'
    if startDate == None:
      startDate = getDateString(time.time() - 365 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time()).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      caseDetails_dict = {}
      for lineItems in queryResult_list:
        try:
          if lineItems[5] != "" and lineItems[5] != None:
            caseTopic = lineItems[5].replace('"',"'").replace(",",";")
          else:
            caseTopic = ""
        except:
          logException("unable to parse [] to a safe csv column".format(lineItems[5]))
          caseTopic = ""
        
        if lineItems[8] != None and lineItems[8] != "":
          resolutiontime = (lineItems[8] - lineItems[7]).total_seconds() / 3600
        else:
          resolutiontime = ""
        
        if lineItems[30] == None:
          agentAliasId = ""
        else:
          agentAliasId = lineItems[30]
          
        caseDetails_dict[lineItems[0]] = {"caseId" : lineItems[0],
                                          "accountId": lineItems[1],
                                          "serviceName": lineItems[2],
                                          "supportCategory": "",
                                          "contactMethod": "",
                                          "caseType": lineItems[3],
                                          "caseCategory": lineItems[4],
                                          "caseTopic": caseTopic,
                                          "caseReason": lineItems[6],
                                          "abstractedReason": "",
                                          "creationDate": lineItems[7],
                                          "resolvedDate": lineItems[8],
                                          "firstOutboundDate" : lineItems[9],
                                          "resolutiontime": resolutiontime,
                                          "caseStatus": lineItems[10],
                                          "severity": lineItems[11],
                                          "missed": lineItems[12],
                                          "autoResolved": lineItems[13],
                                          "isOutboundCase": "",
                                          'inboundPhone': lineItems[14],
                                          'outboundPhone': lineItems[15],
                                          'inboundEmail': lineItems[16],
                                          'outboundEmail': lineItems[17],
                                          'last_inbound_date_pst': lineItems[18],
                                          'last_outbound_date_pst': lineItems[19],
                                          'first_outbound_date_pst': lineItems[20],
                                          'ttr_days': lineItems[21],
                                          'no_of_inbound_phone_contacts': lineItems[22],
                                          'no_of_outbound_phone_contacts': lineItems[23],
                                          'no_of_inbound_email_contacts': lineItems[24],
                                          'no_of_outbound_email_contacts': lineItems[25],
                                          'angry_case': lineItems[26],
                                          'is_reopen': lineItems[27],
                                          'ever_severity_upgrade': lineItems[28],
                                          'ever_severity_downgrade': lineItems[29],
                                          'agentAliasId': agentAliasId
                                          }
                                                                  
      return caseDetails_dict
    else:
      return []
    
  def updateCaseDetailsWithAccountIDList(self, accountId_list, startDate, endDate):
    caseDetails_dict = {}
    
    logInfo("accountIds(len:{}):{}".format(len(accountId_list), accountId_list))
    logInfo("startDate:[{}]".format(startDate))
    logInfo("endDate:[{}]".format(endDate))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryName = 'case_details_with_account_ids'
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
    if queryResult_list != None:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      for row in queryResult_list:
        numberOfItemsOfRow = len(row)
        if numberOfItemsOfRow != totalColumns:
          logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
        
        caseId = "{}".format(row[0])
        countColumn = 0
      
        if caseId not in caseDetails_dict.keys():
          caseDetails_dict[caseId] = {}
          
          for columnName in columnNames:
            caseDetails_dict[caseId][columnName] = row[countColumn]
            countColumn += 1
          
        else:
          logError("caseId:[{}] is already updated.".format(caseId))
  
    return caseDetails_dict
  
  def updateCaseDetailsOfInternalAccounts(self):
    queryResult_list, columnNames = self.queryAWSDW('case_details_of_internal_accounts')
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    if queryResult_list != None:
      for row in queryResult_list:
        numberOfItemsOfRow = len(row)
        if numberOfItemsOfRow != totalColumns:
          logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
        
        accountId = row[0]
        countColumn = 0
      
        if accountId not in self.accountInfo_dict.keys():
          self.accountInfo_dict[accountId] = {}
    
        for columnName in columnNames:
          self.accountInfo_dict[accountId][columnName] = row[countColumn]
          countColumn += 1
        
        if 'dataSource' in self.accountInfo_dict[accountId].keys():
          if "ASDW" not in self.accountInfo_dict[accountId]['dataSource']:
            self.accountInfo_dict[accountId]['dataSource'] += "," + "ASDW"
          else:
            self.accountInfo_dict[accountId]['dataSource'] = "ASDW"
        else:
          self.accountInfo_dict[accountId]['dataSource'] = "ASDW"
  
  def updateCaseDetailsofFMC(self):
    queryResult_list, columnNames = self.queryAWSDW('case_details_of_fmc')
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    if queryResult_list != None:
      for row in queryResult_list:
        numberOfItemsOfRow = len(row)
        if numberOfItemsOfRow != totalColumns:
          logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
        
        accountId = row[0]
        countColumn = 0
      
        if accountId not in self.accountInfo_dict.keys():
          self.accountInfo_dict[accountId] = {}
    
        for columnName in columnNames:
          self.accountInfo_dict[accountId][columnName] = row[countColumn]
          countColumn += 1
        
        if 'dataSource' in self.accountInfo_dict[accountId].keys():
          if "ASDW" not in self.accountInfo_dict[accountId]['dataSource']:
            self.accountInfo_dict[accountId]['dataSource'] += "," + "ASDW"
          else:
            self.accountInfo_dict[accountId]['dataSource'] = "ASDW"
        else:
          self.accountInfo_dict[accountId]['dataSource'] = "ASDW"
  
    
  def getSupportLevel(self, supportProduct):
    supportLevel_dict = {}
    supportLevel_dict['AWS Support (Enterprise)'] = "enterprise"
    supportLevel_dict['AWS Support BJS (Enterprise)'] = "enterprise"
    supportLevel_dict['AWS Premium Support (Platinum)'] = "enterprise"
    supportLevel_dict['AWS SDK Metrics for Enterprise Support'] = "enterprise"
    
    supportLevel_dict['AWS Support (Business)'] = "business"
    supportLevel_dict['AWS Support BJS (Business)'] = "business"
    supportLevel_dict['AWS Support BJS (Business)'] = "business"
    supportLevel_dict['AWS Support Minimum Fee (Business)'] = "business"
    supportLevel_dict['AWS Premium Support (Gold)'] = "business"
    supportLevel_dict['AWS Premium Support Minimum Fee (Gold)'] = "business"
    
    supportLevel_dict['AWS Premium Support (Fixed Price)'] = "developer"
    supportLevel_dict['AWS Premium Support (PS Charge)'] = "developer"
    supportLevel_dict['AWS Premium Support Minimum Fee (Bronze)'] = "developer"
    supportLevel_dict['AWS Premium Support (Bronze)'] = "developer"
    supportLevel_dict['AWS Support (Developer)'] = "developer"
    supportLevel_dict['AWS Support BJS (Developer)'] = "developer"
    supportLevel_dict['AWS Premium Support (Silver)'] = "developer"
    supportLevel_dict['AWS Premium Support Minimum Fee (Silver)'] = "developer"
    supportLevel_dict['AWS Support Minimum Fee (Developer)'] = "developer"
                                      
    supportLevel_dict['AWS Support'] = "basic"
    supportLevel_dict['AWS Support (Basic)'] = "basic"
    supportLevel_dict['AWS Premium Support'] = "basic"
    supportLevel_dict['AWS Support AISPL (Basic)'] = "basic"
    supportLevel_dict['AWS Support BJS (Basic)'] = "basic"
    
    if supportProduct in supportLevel_dict.keys():
      return supportLevel_dict[supportProduct]
    elif "enterprise" in supportProduct.lower():
      return "enterprise"
    elif "platinum" in supportProduct.lower():
      return "enterprise"
    elif "business" in supportProduct.lower():
      return "business"
    elif "gold" in supportProduct.lower():
      return "business"
    elif "bronze" in supportProduct.lower():
      return "developer"
    elif "silver" in supportProduct.lower():
      return "developer"
    elif "silver" in supportProduct.lower():
      return "developer"
    elif "basic" in supportProduct.lower():
      return "basic"
    else:
      return "basic"

  def getAWSSupportLevelWithInternalAccounts(self):
    queryResult_list, columnNames = self.queryAWSDW('aws_support_level')
  
    accountInfo_dict = {}
    
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results:{} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
    for row in queryResult_list:
      accountId = row[0]
      supportProduct = row[1]
      supportLevel = self.getSupportLevel(supportProduct)
      
      countColumn = 0
    
      if accountId in accountInfo_dict.keys():
        #logWarn("row:[{}] is duplicated with accountId:{}->[{}]".format(row, accountId, accountInfo_dict[accountId]))
                
        if supportLevel == "enterprise" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "business" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "developer" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business"]:
          pass
        elif supportLevel == "basic" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business", "developer"]:
          pass
        else:
          accountInfo_dict[accountId]["supportProduct"] = supportProduct
          accountInfo_dict[accountId]["supportLevel"] = supportLevel
      else:
        accountInfo_dict[accountId] = {}
        
        for columnName in columnNames:
          accountInfo_dict[accountId][columnName] = row[countColumn]
            #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
          countColumn += 1
        
        accountInfo_dict[accountId]["supportLevel"] = supportLevel
    
    return accountInfo_dict

  def updateAWSSupportLevelWithInternalAccounts(self, accountInfo_dict):
    queryResult_list, columnNames = self.queryAWSDW('aws_support_level')
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results:{} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
    for row in queryResult_list:
      accountId = row[0]
      supportProduct = row[1]
      supportLevel = self.getSupportLevel(supportProduct)
      
      countColumn = 0
    
      if accountId in accountInfo_dict.keys():
        logWarn("row:[{}] is duplicated with accountId:{}->[{}]".format(row, accountId, accountInfo_dict[accountId]))
                
        if supportLevel == "enterprise" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "business" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "developer" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business"]:
          pass
        elif supportLevel == "basic" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business", "developer"]:
          pass
        else:
          accountInfo_dict[accountId]["supportProduct"] = supportProduct
          accountInfo_dict[accountId]["supportLevel"] = supportLevel
      else:
        accountInfo_dict[accountId] = {}
        
        for columnName in columnNames:
          accountInfo_dict[accountId][columnName] = row[countColumn]
            #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
          countColumn += 1
        
        accountInfo_dict[accountId]["supportLevel"] = supportLevel
    
    return accountInfo_dict
      
  def getAWSSupportLevelWithAccountIds(self, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryName = 'aws_support_level_with_accountIds'
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results: {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    accountInfo_dict = {}
    
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      supportProduct = row[1]
      supportLevel = self.getSupportLevel(supportProduct)
      
      countColumn = 0
    
      if accountId in accountInfo_dict.keys():
        logWarn("row:[{}] is duplicated with accountId:{}->[{}]".format(row, accountId, accountInfo_dict[accountId]))
                
        if supportLevel == "enterprise" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "business" and accountInfo_dict[accountId]["supportLevel"] == "enterprise":
          pass
        elif supportLevel == "developer" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business"]:
          pass
        elif supportLevel == "basic" and accountInfo_dict[accountId]["supportLevel"] in ["enterprise", "business", "developer"]:
          pass
        else:
          accountInfo_dict[accountId]["supportProduct"] = supportProduct
          accountInfo_dict[accountId]["supportLevel"] = supportLevel
      else:
        accountInfo_dict[accountId] = {}
        
        for columnName in columnNames:
          accountInfo_dict[accountId][columnName] = row[countColumn]
            #logDebug("{} is updated at accountId:{}".format(columnName, accountId))
          countColumn += 1
        
        accountInfo_dict[accountId]["supportLevel"] = supportLevel
        
      
    return accountInfo_dict
  
  def updateAWSSupportLevelWithAccountIds(self, accountInfo_dict, accountId_list):
    logInfo("with {} accounts".format( len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
    
    queryName = 'aws_support_level_with_accountIds'
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds))
    queryResult_list, columnNames = self.queryAWSDW(queryName, self.gcDwTemplates.getQueryString(queryName))
    
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results: {} rows with {} columns: {}".format( totalRows, totalColumns, columnNames))
    
    for row in queryResult_list:
      numberOfItemsOfRow = len(row)
      if numberOfItemsOfRow != totalColumns:
        logError("the number of columns({}) of row isn't equal to the number of columnNames({}).".format(numberOfItemsOfRow, totalColumns))
      
      accountId = row[0]
      
      countColumn = 0
    
      if accountId not in accountInfo_dict.keys():
        accountInfo_dict[accountId] = {}
  
      for columnName in columnNames:
        if columnName in accountInfo_dict[accountId].keys():
          if accountInfo_dict[accountId][columnName] != "":
            logDebug("{} is already updated at accountId:{}".format( columnName, accountId))
          else:
            accountInfo_dict[accountId][columnName] = row[countColumn]
            logInfo("{} is updated at accountId:{}, as the column data was empty.".format( columnName, accountId))
        else:
          accountInfo_dict[accountId][columnName] = row[countColumn]
          logDebug("{} is updated at accountId:{}".format(columnName, accountId))
        countColumn += 1
      
      if 'dataSource' in accountInfo_dict[accountId].keys():
        if "NoInternal" not in accountInfo_dict[accountId]['dataSource']:
          accountInfo_dict[accountId]['dataSource'].append("NoInternal")
        else:
          accountInfo_dict[accountId]['dataSource'] = ["NoInternal"]
      else:
        accountInfo_dict[accountId]['dataSource'] = ["NoInternal"]
  
  def updateEC2InstancesOfSuspendedAccounts(self):
    queryResult_list, columnNames = self.queryAWSDW('ec2_instances_of_suspended_accounts')
  
  def getAllEnterpriseAccounts(self):
    queryResult_list, columnNames = self.queryAWSDW('all_enterprsie_accounts')
  
    accountInfo_dict = {}
    
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results:{} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
    for row in queryResult_list:
      accountId = row[0]
      payerAccountId = row[1]
      supportName = row[2]
      emailDomain = row[3]      
                
      supportLevel = self.getSupportLevel(supportName)
      #logDebug("INPUT: accountId:{}, supportName:{}, supportLevel:{}".format( accountId, supportName, supportLevel))
      if accountId in accountInfo_dict.keys():
        if 'supportLevel' in accountInfo_dict[accountId].keys():   
          if accountInfo_dict[accountId]['supportLevel'] == "":
            logDebug("accountId:{} has an empty support level. It'll be updated with {}:{}".format( accountId, supportName, supportLevel))
            accountInfo_dict[accountId]['supportLevel'] = supportLevel
            accountInfo_dict[accountId]['supportProducts'] = supportName        
          else:
            currentSupportLevel = accountInfo_dict[accountId]['supportLevel']
            currentSupportProduct = accountInfo_dict[accountId]['supportProducts']
             
            if  currentSupportLevel == 'enterprise' :
              logDebug("Duplicated Support Level with accountID:{} with {}".format(accountId, currentSupportProduct) )  
            elif currentSupportLevel == 'business':
              if supportLevel == 'enterprise':
                accountInfo_dict[accountId]['supportLevel'] = 'enterprise' 
            elif currentSupportLevel == 'developer':
              if supportLevel == 'enterprise':
                accountInfo_dict[accountId]['supportLevel'] = 'enterprise'
              elif supportLevel == 'business':
                accountInfo_dict[accountId]['supportLevel'] = 'business'  
              # end of supportLevel == 'enterprise':
            elif currentSupportLevel == 'basic':
              if supportLevel == 'enterprise':
                accountInfo_dict[accountId]['supportLevel'] = 'enterprise'
              elif supportLevel == 'business':
                accountInfo_dict[accountId]['supportLevel'] = 'business'
              elif supportLevel == 'developer':
                accountInfo_dict[accountId]['supportLevel'] = 'developer'          
            # end of supportLevel == 'enterprise':
            
            accountInfo_dict[accountId]['supportProducts'] += "," + supportName   
          
        else:
          accountInfo_dict[accountId]['supportLevel'] = supportLevel
          accountInfo_dict[accountId]['supportProducts'] = supportName
      else:
          accountInfo_dict[accountId] = {}
          accountInfo_dict[accountId]['payerAccountId'] = payerAccountId
          accountInfo_dict[accountId]['supportLevel'] = supportLevel
          accountInfo_dict[accountId]['supportProducts'] = supportName
          accountInfo_dict[accountId]['emailDomain'] = emailDomain
          
    
    logDebug("RESULT: accountId:{}, supportName:{}, supportLevel:{}".format( accountId, 
                                                                                       accountInfo_dict[accountId]['supportProducts'], 
                                                                                       accountInfo_dict[accountId]['supportLevel']))
   
    logInfo("Task-002: Writing Internal AWS Account Information to CSV" )
    
    return accountInfo_dict

  def listActivePaidLicensedEC2Instances(self, accountId_list, startDate, endDate):
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'list_active_paid_licenced_ec2_instances'
    dwSnapshotDate = getDateString(time.time() - 24 * 3600)
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_dict = {}
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        instanceId = lineItems[2]
        if instanceId in activeEC2InstanceId_dict.keys() and lineItems[15].timestamp() <= activeEC2InstanceId_dict[instanceId]:
          logWarn("instanceId:[{}] is duplicated with lineItems:[{}]".format(instanceId, lineItems))
        else:
          activeEC2InstanceId_dict[instanceId] = lineItems[15].timestamp()
          
          if isinstance(lineItems[3], str) and len(lineItems[3]) > 0:
            regionCode = lineItems[3][:-1]
          else:
            regionCode = ""
            
          if lineItems[5] == False or lineItems[5] == "FALSE":
            tenancy = "shared"
          else:
            tenancy = "dedicated"
          
          if lineItems[8] == None or lineItems[8] == "None":
            ec2BillingProductIds = ""
            ec2BillingProdcuts = "Linux"
          else:
            ec2BillingProductIds = lineItems[7]
            ec2BillingProdcuts = ""
            for ec2BillingProdcutId in lineItems[8].split(":"):
              if ec2BillingProdcutId in ec2BillingProdcut_dict.keys():
                if ec2BillingProdcuts == "":
                  ec2BillingProdcuts = ec2BillingProdcut_dict[ec2BillingProdcutId]
                else:
                  ec2BillingProdcuts = "{}+{}".format(ec2BillingProdcuts, ec2BillingProdcut_dict[ec2BillingProdcutId])
                  
          if lineItems[9] == None or lineItems[9] == "":
            pendingTime = ""
          else:
            pendingTime = lineItems[9]
          
          if lineItems[10] == None or lineItems[10] == "":
            runningTime = ""
          else:
            runningTime = lineItems[10]
          
          if lineItems[11] == None or lineItems[11] == "":
            shuttingDownTime = ""
          else:
            shuttingDownTime = lineItems[11]
          
          if lineItems[12] == None or lineItems[12] == "":
            terminatedTime = ""
          else:
            terminatedTime = lineItems[12]
          
          if lineItems[13] == None or lineItems[13] == "":
            stateChangeMessage = ""
          else:
            stateChangeMessage = lineItems[13]
            
          activeEC2InstanceId_list.append( {"accountId" : lineItems[0],
                                            "instanceId": instanceId,
                                            "physicalLocation" : lineItems[1],
                                            "regionCode": regionCode,
                                            "availabilityZone" : lineItems[3],
                                            "dropletIp" : lineItems[4],
                                            "tenancy" : tenancy,
                                            "instanceType" : lineItems[6],
                                            "billingIds" : ec2BillingProductIds,
                                            "billingProducts" : ec2BillingProdcuts,
                                            "pendingTime" : pendingTime,
                                            "runningTime" : runningTime,
                                            "shuttingDownTime" : shuttingDownTime,
                                            "terminatedTime": terminatedTime,
                                            "stateChangeMessage": stateChangeMessage,
                                            "dwStartDate":  lineItems[14],
                                            "dwSnapshotDate":  lineItems[15]
                                            })
        
          
      return activeEC2InstanceId_list
    else:
      return []
  
  def listActiveEC2Instances(self, accountId_list):
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'list_active_ec2_instances'
    dwSnapshotDate = getDateString(time.time() - 24 * 3600)
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{DW_SNAPSHOT_DATE}}", dwSnapshotDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_dict = {}
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        instanceId = lineItems[3]
        if instanceId in activeEC2InstanceId_dict.keys() and lineItems[16].timestamp() <= activeEC2InstanceId_dict[instanceId]:
          logWarn("instanceId:[{}] is duplicated with lineItems:[{}]".format(instanceId, lineItems))
        else:
          activeEC2InstanceId_dict[instanceId] = lineItems[16].timestamp()
          
          if isinstance(lineItems[4], str) and len(lineItems[4]) > 0:
            regionCode = lineItems[4][:-1]
          else:
            regionCode = ""
            
          if lineItems[6] == False or lineItems[6] == "FALSE":
            tenancy = "shared"
          else:
            tenancy = "dedicated"
          
          if lineItems[9] == None or lineItems[9] == "None":
            ec2BillingProductIds = ""
            ec2BillingProdcuts = "Linux"
          else:
            ec2BillingProductIds = lineItems[8]
            ec2BillingProdcuts = ""
            for ec2BillingProdcutId in lineItems[9].split(":"):
              if ec2BillingProdcutId in ec2BillingProdcut_dict.keys():
                if ec2BillingProdcuts == "":
                  ec2BillingProdcuts = ec2BillingProdcut_dict[ec2BillingProdcutId]
                else:
                  ec2BillingProdcuts = "{}+{}".format(ec2BillingProdcuts, ec2BillingProdcut_dict[ec2BillingProdcutId])
                  
          if lineItems[10] == None or lineItems[10] == "":
            pendingTime = ""
          else:
            pendingTime = lineItems[10]
          
          if lineItems[11] == None or lineItems[11] == "":
            runningTime = ""
          else:
            runningTime = lineItems[11]
          
          if lineItems[12] == None or lineItems[12] == "":
            shuttingDownTime = ""
          else:
            shuttingDownTime = lineItems[12]
          
          if lineItems[13] == None or lineItems[13] == "":
            terminatedTime = ""
          else:
            terminatedTime = lineItems[13]
          
          if lineItems[14] == None or lineItems[14] == "":
            stateChangeMessage = ""
          else:
            stateChangeMessage = lineItems[14]
            
          activeEC2InstanceId_list.append( {"accountId" : lineItems[0],
                                            "accountStatusCode" : lineItems[1],
                                            "instanceId": instanceId,
                                            "physicalLocation" : lineItems[2],
                                            "regionCode": regionCode,
                                            "availabilityZone" : lineItems[4],
                                            "dropletIp" : lineItems[5],
                                            "tenancy" : tenancy,
                                            "instanceType" : lineItems[7],
                                            "billingIds" : ec2BillingProductIds,
                                            "billingProducts" : ec2BillingProdcuts,
                                            "pendingTime" : pendingTime,
                                            "runningTime" : runningTime,
                                            "shuttingDownTime" : shuttingDownTime,
                                            "terminatedTime": terminatedTime,
                                            "stateChangeMessage": stateChangeMessage,
                                            "dwStartDate":  lineItems[15],
                                            "dwSnapshotDate":  lineItems[16]
                                            })
        
          
      return activeEC2InstanceId_list
    else:
      return []
  
  def listEC2Instances(self, accountId_list, startDate, endDate):
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'list_ec2_instances'
    dwSnapshotDate = getDateString(time.time() - 24 * 3600).split("T")[0]
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_dict = {}
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        instanceId = lineItems[3]
        if instanceId in activeEC2InstanceId_dict.keys():
          logError("instanceId:[{}] is duplicated with lineItems:[{}]".format(instanceId, lineItems))
        else:
          activeEC2InstanceId_dict[instanceId] = lineItems[16].timestamp()
          
          if isinstance(lineItems[4], str) and len(lineItems[4]) > 0:
            regionCode = lineItems[4][:-1]
          else:
            regionCode = ""
            
          if lineItems[6] == False or lineItems[6] == "FALSE":
            tenancy = "shared"
          else:
            tenancy = "dedicated"
          
          if lineItems[9] == None or lineItems[9] == "None":
            ec2BillingProductIds = ""
            ec2BillingProdcuts = "Linux"
          else:
            ec2BillingProductIds = lineItems[8]
            ec2BillingProdcuts = ""
            for ec2BillingProdcutId in lineItems[9].split(":"):
              if ec2BillingProdcutId in ec2BillingProdcut_dict.keys():
                if ec2BillingProdcuts == "":
                  ec2BillingProdcuts = ec2BillingProdcut_dict[ec2BillingProdcutId]
                else:
                  ec2BillingProdcuts = "{}+{}".format(ec2BillingProdcuts, ec2BillingProdcut_dict[ec2BillingProdcutId])
                  
          if lineItems[10] == None or lineItems[10] == "":
            pendingTime = ""
          else:
            pendingTime = lineItems[10]
          
          if lineItems[11] == None or lineItems[11] == "":
            runningTime = ""
          else:
            runningTime = lineItems[11]
          
          if lineItems[12] == None or lineItems[12] == "":
            shuttingDownTime = ""
          else:
            shuttingDownTime = lineItems[12]
          
          if lineItems[13] == None or lineItems[13] == "":
            terminatedTime = ""
          else:
            terminatedTime = lineItems[13]
          
          if lineItems[14] == None or lineItems[14] == "":
            stateChangeMessage = ""
          else:
            stateChangeMessage = lineItems[14]
            
          activeEC2InstanceId_list.append( {"accountId" : lineItems[0],
                                            "accountStatusCode" : lineItems[1],
                                            "instanceId": instanceId,
                                            "physicalLocation" : lineItems[2],
                                            "regionCode": regionCode,
                                            "availabilityZone" : lineItems[4],
                                            "dropletIp" : lineItems[5],
                                            "tenancy" : tenancy,
                                            "instanceType" : lineItems[7],
                                            "billingIds" : ec2BillingProductIds,
                                            "billingProducts" : ec2BillingProdcuts,
                                            "pendingTime" : pendingTime,
                                            "runningTime" : runningTime,
                                            "shuttingDownTime" : shuttingDownTime,
                                            "terminatedTime": terminatedTime,
                                            "stateChangeMessage": stateChangeMessage,
                                            "dwStartDate":  lineItems[15],
                                            "dwSnapshotDate":  lineItems[16]
                                            })
          
      return activeEC2InstanceId_list
    else:
      return []
  
  def getEC2ClassicInstanceList(self, accountId_list, startDate, endDate):
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'list_ec2_classic_instances'
    dwSnapshotDate = getDateString(time.time() - 24 * 3600).split("T")[0]
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_dict = {}
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        instanceId = lineItems[0]
        if instanceId in activeEC2InstanceId_dict.keys():
          logError("instanceId:[{}] is duplicated with lineItems:[{}]".format(instanceId, lineItems))
        else:
          activeEC2InstanceId_dict[instanceId] = dwSnapshotDate
          
          if lineItems[3] == True:
            tenancy = "dedicated"
          else:
            tenancy = "shared"
            
          if lineItems[4] == True:
            category = "VPC"
          else:
            category = "classic"
            
          if isinstance(lineItems[6], str) and len(lineItems[6]) > 0:
            regionCode = lineItems[6][:-1]
          else:
            regionCode = ""
            
          if lineItems[7] == None or lineItems[7] == "":
            pendingTime = ""
          else:
            pendingTime = lineItems[7]
          
          if lineItems[8] == None or lineItems[8] == "":
            runningTime = ""
          else:
            runningTime = lineItems[8]
          
          if lineItems[9] == None or lineItems[9] == "":
            shuttingDownTime = ""
          else:
            shuttingDownTime = lineItems[9]
          
          if lineItems[10] == None or lineItems[10] == "":
            terminatedTime = ""
          else:
            terminatedTime = lineItems[10]
            
          activeEC2InstanceId_list.append( {"accountId" : lineItems[1],
                                            "accountStatusCode" : lineItems[2],
                                            "instanceId": instanceId,
                                            "regionCode": regionCode,
                                            "availabilityZone" : lineItems[6],
                                            "tenancy" : tenancy,
                                            "category" : category,
                                            "instanceType" : lineItems[7],
                                            "pendingTime" : pendingTime,
                                            "runningTime" : runningTime,
                                            "shuttingDownTime" : shuttingDownTime,
                                            "terminatedTime": terminatedTime,
                                            "snapshotDate":  dwSnapshotDate
                                            })
          
      return activeEC2InstanceId_list
    else:
      return []
  
  def getDailyEc2RIUtilization(self, accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'dailyEc2RIUtilization'
    if startDate == None:
      startDate = getDateString(time.time() - 15 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time() - 2 * 24 * 3600).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        
        activeEC2InstanceId_list.append( {"date" : lineItems[0],
                                          "payerAccountId": lineItems[1],
                                          "accountId": lineItems[2],
                                          "region": lineItems[3],
                                          "instanceType": lineItems[4],    
                                          "billingMode" : lineItems[5],
                                          "rawHours": lineItems[6],
                                          "committed_normalizedHours": lineItems[7],
                                          "used_normalizedHours" : lineItems[8]
                                          })
          
      return activeEC2InstanceId_list
    else:
      return []
    
  def getDailyEc2OdUsage(self, accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'dailyEc2OdUsage'
    if startDate == None:
      startDate = getDateString(time.time() - 15 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time() - 2 * 24 * 3600).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      activeEC2InstanceId_list = []
      for lineItems in queryResult_list:
        activeEC2InstanceId_list.append( {"date" : lineItems[0],
                                          "payerAccountId": lineItems[1],
                                          "accountId": lineItems[2],
                                          "region": lineItems[3],
                                          "instanceType": lineItems[4],
                                          "billingMode": lineItems[5],
                                          "rawInstanaceHours": lineItems[6],
                                          "normalizedInstanceHours" : lineItems[7]
                                          })
          
      return activeEC2InstanceId_list
    else:
      return []
    
  def getAccessedAccounts(self, accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'accessed_accounts'
    if startDate == None:
      startDate = getDateString(time.time() - 2 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time()).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      accessedAccoundId_dict = {}
      for lineItems in queryResult_list:
        accessedAccoundId_dict[lineItems[0]] = {"accountId":lineItems[0]}
          
      return accessedAccoundId_dict
    else:
      return {}
    
  def getServiceUsageList(self, serviceName = "AmazonS3", accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("serviceName:[{}]->startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(serviceName, startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'serviceUsages'
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{SERVICENAME}}",serviceName).replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      serviceUsage_list = []
      for lineItems in queryResult_list:
        serviceUsage_list.append( {"accountId" : lineItems[0],
                                    "serviceName": lineItems[1],
                                    "operation": lineItems[2],
                                    "availability_zone": lineItems[3],
                                    "usage_type": lineItems[4],
                                    "usage_value": lineItems[5],
                                    "usage_resource": lineItems[6],
                                    "request_day" : lineItems[7]
                                    })
          
      return serviceUsage_list
    else:
      return []
  
  def getRegionCodeList(self, serviceName = "AmazonS3", accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("serviceName:[{}]->startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(serviceName, startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'serviceRegionCodes'
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{SERVICENAME}}",serviceName).replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    serviceUsage_list = []
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      for lineItems in queryResult_list:
        try:
          if lineItems[3] != "" and lineItems[3][-1] in ["a","b","c","d","e","f","g"]:
            regionCode = lineItems[3][0:-1]
          else:
            regionCode = lineItems[3]
        except:
          logException("unable to set regionCode with [{}]".format(lineItems[3]))
          regionCode = lineItems[3]
        
        serviceUsage_list.append( {"accountId" : lineItems[0],
                                    "serviceName": lineItems[1],
                                    "regionCode": regionCode
                                    })
          
    return serviceUsage_list
    
  
  def getActiveResourceList(self, serviceName = "AmazonS3", accountId_list = ['689819985789'], startDate = None, endDate = None, usageType = None):
    logDebug("serviceName:[{}]->startDate:[{}]->endDate:[{}]->usageType:[{}]->accountId_list:[len:({})]".format(serviceName, startDate, endDate, usageType, len(accountId_list)))
    
    if usageType == None:
      return []
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'activeServiceResources'
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{SERVICENAME}}",serviceName).replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate).replace("${{USAGE_TYPE}}", usageType))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      serviceUsage_list = []
      for lineItems in queryResult_list:
        serviceUsage_list.append({"accountId":lineItems[0],
                                  'availabilityZone':lineItems[1],
                                  'usageResouce':lineItems[2],
                                  'usageType':lineItems[3],
                                  'operation':lineItems[4],
                                  'usageValue':lineItems[5],
                                  })
          
          
      return serviceUsage_list
    else:
      return []

  def getEbsSnapshotList(self, accountId_list = ['239575778557'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'ebsSnapshotUsage'
    if startDate == None:
      startDate = getDateString(time.time() - 2 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time()).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    activeS3resouce_list = []
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      for lineItems in queryResult_list:
        try:
          snapshotId_list = lineItems[3].split(":")
          #logDebug("regionCode:[{}]".format(snapshotId_list[3]))
          #logDebug("snapshotId:[{}]".format(snapshotId_list[5].split("/")[1]))
          
          gibUsageValue = lineItems[2] / 25769803776
          
          activeS3resouce_list.append({"accountId":lineItems[0],
                                       "regionCode":snapshotId_list[3],
                                        'snapshotId':snapshotId_list[5].split("/")[1],
                                        'usageType':lineItems[1],
                                        'usageValue(GiB)':gibUsageValue,
                                        })
        except:
          logException("unable to get the snapshotId with lineItems:[{}]".format(lineItems))
          
    return activeS3resouce_list
        
  def getActiveS3ResourceList(self, accountId_list = ['689819985789'], startDate = None, endDate = None):
    logDebug("startDate:[{}]->endDate:[{}]->accountId_list:[len:({})]".format(startDate, endDate, len(accountId_list)))
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "('{}')".format(accountId)
      else:
        accountIds += ",('{}')".format(accountId)
      
    queryName = 'activeS3resouces'
    if startDate == None:
      startDate = getDateString(time.time() - 2 * 24 * 3600).split("T")[0]
    else:
      startDate = startDate.split("T")[0].split(" ")[0]
    
    if endDate == None: 
      endDate  = getDateString(time.time()).split("T")[0]
    else:
      endDate = endDate.split("T")[0].split(" ")[0]
      
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    activeS3resouce_list = []
    if queryResult_list != None and isinstance(queryResult_list, list) and len(queryResult_list) > 0:
      totalRows = len(queryResult_list)
      totalColumns = len(columnNames)
      logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
      
      for lineItems in queryResult_list:
        activeS3resouce_list.append({"accountId":lineItems[0],
                                  'usageResouce':lineItems[1],
                                  'usageType':lineItems[2],
                                  'operation':lineItems[3],
                                  'usageValue':lineItems[4],
                                  })
          
    return activeS3resouce_list
        
  def getAllServiceUsageValuesByAz(self, accountId_list, startDate, endDate):
    queryName = 'all_service_usage_value'
    
    accountIds = ""
    for accountId in accountId_list:
      if len(accountIds) == 0:
        accountIds += "'{}'".format(accountId)
      else:
        accountIds += ",'{}'".format(accountId)
      
    queryName = 'aws_support_level_with_accountIds'
    self.gcDwTemplates = GcDwTemplates()
    queryStatement = self.gcDwTemplates.getQueryString(queryName)
    self.gcDwTemplates.updateQueryString(queryName, queryStatement.replace("${{ACCOUNT_ID_LIST}}", accountIds).replace("${{START_DATE}}", startDate).replace("${{END_DATE}}", endDate))
    queryResult_list, columnNames = self.queryAWSDW(queryName)
  
    totalRows = len(queryResult_list)
    totalColumns = len(columnNames)
    logInfo("results with {} rows with {} columns: {}".format(totalRows, totalColumns, columnNames))
    
    accountUsageValue_dict = {}
    for lineItems in queryResult_list:
      accountId = lineItems[0]
      productCode =  lineItems[1]
      serviceOperation = lineItems[2]
      availabilityZone =  lineItems[3]
      if availabilityZone == "":
        availabilityZone = "global"
      usageType =  lineItems[4]
      usageValue =  int(lineItems[5])
      
      if availabilityZone in accountUsageValue_dict.keys():
        if productCode in accountUsageValue_dict[availabilityZone].keys():
          if usageType in accountUsageValue_dict[availabilityZone][productCode].keys():
            if accountId  in accountUsageValue_dict[availabilityZone][productCode][usageType].keys():
              accountUsageValue_dict[availabilityZone][productCode][usageType][accountId] += usageValue
            else:
              accountUsageValue_dict[availabilityZone][productCode][usageType][accountId] = usageValue  
          else:
            accountUsageValue_dict[availabilityZone][productCode][usageType] = {}
            accountUsageValue_dict[availabilityZone][productCode][usageType][accountId] = usageValue    
        else:
          accountUsageValue_dict[availabilityZone][productCode] = {}
          accountUsageValue_dict[availabilityZone][productCode][usageType] = {}
          accountUsageValue_dict[availabilityZone][productCode][usageType][accountId] = usageValue          
      else:
        accountUsageValue_dict[availabilityZone] = {}
        accountUsageValue_dict[availabilityZone][productCode] = {}
        accountUsageValue_dict[availabilityZone][productCode][usageType] = {}
        accountUsageValue_dict[availabilityZone][productCode][usageType][accountId] = usageValue    
        
    return accountUsageValue_dict
  
  def isEffectiveProductCode(self, productCode):
    effectiveProductCode_dict = {}
    inEffectiveProductCode_dict = {}
    
    if productCode in inEffectiveProductCode_dict.keys():
      logDebug("prodcuctCode:[{}] is already regigerted at ineffective product codes".format(productCode))
      
      return False
    else:
      if productCode in effectiveProductCode_dict.keys():
        logDebug("prodcuctCode:[{}] is already regigerted at ineffective product codes".format(productCode))
      else:
        inEffectiveProductCode_dict[productCode] = productCode
        logDebug("prodcuctCode:[{}] is newly regigerted at effective product codes".format(productCode))
      
      return True

def getQuery(templateName):
  logInfo("templateName:[{}]".format(templateName))
  gcDw = GcDw()
  queryResult_list, columnNames = gcDw.queryAWSDW(templateName)
  
def getQueryWithTempTable():
  gcDw = GcDw()
  
  templateName = "create_temp_accountId_table"
  logInfo("templateName:[{}]".format(templateName))
  queryResult_list, columnNames = gcDw.queryAWSDW(templateName)
  if queryResult_list != None:
    logInfo("queryResult_list(len:{}):[{}]".format(len(queryResult_list), queryResult_list))
  
def getQueryWithSuspendedEC2Instances():
  gcDw = GcDw()
  
  templateName = "suspended_ec2_instances"
  logInfo("templateName:[{}]".format(templateName))
  queryResult_list, columnNames = gcDw.queryAWSDW(templateName)
  if queryResult_list != None:
    logInfo("queryResult_list(len:{}):[{}]".format(len(queryResult_list), queryResult_list))
  

def getDailyEc2Ri():
  gcDw = GcDw()
  
  gcDw.getDailyEc2RIUtilization()   
  
def getServiceUsages():
  gcDw = GcDw()
  
  gcDw.getServiceUsage()    
  
def getAccessedAccounts():
  gcDw = GcDw()
  
  gcDw.getAccessedAccounts()

def getCaseDetailsWithAccountIDList():
  gcDw = GcDw()
  
  count = 0
  for caseItems in gcDw.getCaseDetailsWithAccountIDList():
    count += 1
    logInfo("{}:[{}]".format(count, caseItems))

def getEC2ClassicInstances():
  gcDw = GcDw()
  
  count = 0
  for caseItems in gcDw.listEC2ClassicInstances(['135490680010'], '2021-01-01', '2021-02-14'):
    count += 1
    logInfo("{}:[{}]".format(count, caseItems))

def getEbsSnapshots():
  gcDw = GcDw()
  
  count = 0
  for caseItems in gcDw.getEbsSnapshotList(['000000000000'], '2023-05-29', '2023-06-01'):
    count += 1
    logInfo("{}:[{}]".format(count, caseItems))
    
def getPiadLicensedEC2Instances():
  gcDw = GcDw()
  
  count = 0
  for caseItems in gcDw.listActivePaidLicensedEC2Instances(['173245911106']):
    count += 1
    logInfo("{}:[{}]".format(count, caseItems))



def getInternalAccountsFromAWSDW():
  gcDw = GcDw()
  accountInfo_dict = gcDw.getInternalAccountsFromAWSDW()
  
          
  count = 0
  totalAccountNumber = len(accountInfo_dict.keys())
  logInfo("total {} accounts are listed".format(totalAccountNumber))
  percentageDelimeter = int(totalAccountNumber/100)
  
  thisActiveAccountTrend24M_dict = {}
  for accountId in accountInfo_dict.keys():
    accountItems = accountInfo_dict[accountId]
    
    count += 1
    if (count % percentageDelimeter) == 0:
      logInfo("(#{}/{}) [{}]->[{}]".format(count,totalAccountNumber, accountId, accountItems))
    
    createdEpochTime = getDateString(accountItems["creationDate"])
    dateString = datetime.fromtimestamp(createdEpochTime).astimezone(timezone('UTC')).strftime('%Y-%m-01')
    if dateString in thisActiveAccountTrend24M_dict.keys():
      thisActiveAccountTrend24M_dict[dateString] += 1
    else:
      thisActiveAccountTrend24M_dict[dateString] = 1
    
  sortedKeys = sorted(set(thisActiveAccountTrend24M_dict.keys()))
  logInfo("total {} keys found -> sortedKey:[{}]".format(len(sortedKeys), sortedKeys))
  
  for month in sortedKeys:  
    logInfo("month:[{}] -> count:[{}]".format(month, thisActiveAccountTrend24M_dict[month]))

def connectDw(dwName = 'aws'):
  logDebug("dwName:[{}]".format(dwName))
  
  gcDw = GcDw()
  gcDw.connectDW("dwName")

def localUnitTest():
  unitTestFunction_dict = {#"connectDw":{"target":connectDw, "args":("awsdw",)},
                           #"connectDw":{"target":connectDw, "args":("awssupportdw",)},
                           #"getQueryWithSuspendedEC2Instances":{"target":getQueryWithSuspendedEC2Instances, "args":()},
                           #"getServiceUsages":{"target":getServiceUsages, "args":()},
                           #"getDailyEc2Ri":{"target":getDailyEc2Ri, "args":()},
                           #"getQuery":{"target":getQuery, "args":("ec2_instances",)},
                           #"getQueryWithTempTable":{"target":getQueryWithTempTable, "args":()},
                           #"getAccessedAccounts":{"target":getAccessedAccounts, "args":()},
                           #"getEbsSnapshots":{"target":getEbsSnapshots, "args":()},
                           #"getCaseDetailsWithAccountIDList":{"target":getCaseDetailsWithAccountIDList, "args":()},
                           #"getInternalAccountsFromAWSDW":{"target":getInternalAccountsFromAWSDW, "args":()}
                           #"getEC2ClassicInstances":{"target":getEC2ClassicInstances, "args":()}
                           #"getPiadLicensedEC2Instances":{"target":getPiadLicensedEC2Instances, "args":()}
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()
  