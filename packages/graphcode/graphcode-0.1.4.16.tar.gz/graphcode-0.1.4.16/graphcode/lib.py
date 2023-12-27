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
from graphcode.conf import getRoot

from threading import Thread

import time
from pytz import timezone
from datetime import datetime

import json
import copy

from os import listdir
from os.path import exists, expanduser, join

import hashlib

class ThreadWithReturnValueV2(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)



class ThreadWithReturnValue(Thread):
  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
    Thread.__init__(self, group, target, name, args, kwargs)
    self._return = None
  
  def run(self):
    #print(type(self._target))
    if self._target is not None:
      res = self._target(*self._args, **self._kwargs)
      
      #try:
      #  if isinstance(res, list):
      #    if len(res) > 0:
      #      logDebug("res(len:{:,})".format(len(res)))
      #    else:
      #      logDebug("res(len:{:,}):[{}]".format(len(res),res))
      #      
      #  elif isinstance(res, dict):
      #    logDebug("res:[len:{:,}]".format(len(res.keys())))
      #  else:
      #    logDebug("res:[len:{:,}]".format(len(res)))
      #except:
      #  logException("unexpected error with res:type:{}".format(type(res)))
      
      self._return = res
    
    
  def join(self, *args):
    Thread.join(self, *args)
    
    return self._return

def getTshirtsSize(tSize = None):
  if tSize == None:
    return -1
  else:
    if isinstance(tSize, str):
      try:
        tSize = int(tSize)
      except:
        logException("tSize:[{}] is not number".format(tSize))
        
    if isinstance(tSize, str):
      tSize = tSize.lower()
      if "5xlarge" in tSize or "xxxxxlarge" in tSize:
        return 512
      if "4xlarge" in tSize or "xxxxlarge" in tSize:
        return 256
      elif "3xlarge" in tSize or "xxxlarge" in tSize:
        return 128
      elif "2xlarge" in tSize or "xxlarge" in tSize:
        return 64
      elif "xlarge" in tSize:
        if len(tSize.replace("xlarge","")) > 0:
          try:
            if int(tSize.replace("xlarge","")) > 5:
              return 1024
            else:
              return 48
          except:
            return 32
        else:
          return 32
      elif "large" in tSize:
        return 16
      elif "medium" in tSize:
        return 8
      elif "small" in tSize:
        return 4
      elif "micro" in tSize:
        return 2
      elif "nano" in tSize:
        return 1
      else:
        return -1
      
    elif isinstance(tSize, int) or isinstance(tSize, float):
      if tSize < 10:
        return "nano"
      elif tSize < 100:
        return "micro"
      elif tSize < 1000:
        return "small"
      elif tSize < 10000:
        return "medium"
      elif tSize < 100000:
        return "large"
      elif tSize < 1000000:
        return "xlarge"
      elif tSize < 10000000:
        return "2xlarge"
      elif tSize < 100000000:
        return "3xlarge"
      elif tSize < 1000000000:
        return "4xlarge"
      else:
        return "5xlarge"
      
    else:
      return -1
  
def getEc2NormlaizedFactor(tSize):
  normlaizedFactor_dict = {
    "nano":0.25,
    "micro":0.5,
    "small":1,
    "medium":2,
    "large":4,
    "xlarge":8,
    "2xlarge":16,
    "3xlarge":24,
    "4xlarge":32,
    "6xlarge":48,
    "8xlarge":64,
    "9xlarge":72,
    "10xlarge":80,
    "12xlarge":96,
    "16xlarge":128,
    "18xlarge":144,
    "24xlarge":192,
    "32xlarge":256,
    "56xlarge":448,
    "112xlarge":896
    }
  
  if tSize in normlaizedFactor_dict.keys():
    return normlaizedFactor_dict[tSize]
  else:
    return -0.0000000001
    
def printValue(value, depth = 0):
  valueMsg = ""
  if isinstance(value, dict):
    value_list = []
    for key in value.keys():
      value_list.append(key)
    
    valueCount = len(value_list)
    if valueCount == 0:
      valueCount_list = []
    elif valueCount > 10:
      valueCount_list = [0, int(valueCount/3), int(valueCount/3 * 2), valueCount-1]
    else:
      valueCount_list = range(valueCount)
    
    for valueOffset in valueCount_list:
      valueKey = value_list[valueOffset]
      valueMsg += "[{}][{}]:{}:[{}]\n".format(depth, valueKey, type(value[valueKey]), printValue(value[valueKey]))
      
  elif isinstance(value, list):
    valueCount = len(value)
    if valueCount == 0:
      valueCount_list = []
    if valueCount > 10:
      valueCount_list = [0, int(valueCount/3), int(valueCount/3 * 2), valueCount-1]
    else:
      valueCount_list = range(valueCount)
    
    for valueOffset in valueCount_list:
      valueMsg += "[{}]({}):{}:[{}]\n".format(depth, valueOffset, type(value[valueOffset]), printValue(value[valueOffset-1]))
      
  else:
    valueMsg += "[{}]:{}:[{}]\n".format("\t"* depth, type(value), value)
    
  return valueMsg

def getStringToDatetime(dateTime):
  try:
    thisDatetime = datetime.strptime(dateTime, '%m/%d/%y %H:%M:%S.%f')
  except:
    try:
      thisDatetime = datetime.strptime(dateTime, '%m/%d/%y %H:%M:%S')
    except:
      try:
        thisDatetime = datetime.strptime(dateTime, '%m/%d/%y %H:%M')
      except:
        try:
          thisDatetime = datetime.strptime(dateTime, '%m/%d/%y')
        except:
          try:
            thisDatetime = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
          except:
            try:
              thisDatetime = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%SZ')
            except:
              try:
                thisDatetime = datetime.strptime(dateTime, '%Y-%m-%d')
              except:
                raiseValueError("unexpected format:[{}]".format(dateTime))
    
  return thisDatetime

def getUTCTime(dateTime):
  utcTime = None
  if isinstance(dateTime, str):
    if "T" in dateTime:
      #logDebug(f"#dateTime:[{dateTime}]")
      try:
        if "Z" in dateTime:
          #logDebug(f"#dateTime:[{dateTime}]")
          if "." in dateTime:
            #logDebug(f"#dateTime:[{dateTime}]")
            utcTime = datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S.%fZ")
          else:
            #logDebug(f"#dateTime:[{dateTime}]")
            utcTime = datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%SZ")
        elif "." in dateTime:
          #logDebug(f"#dateTime:[{dateTime}]")
          utcTime = datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S.%f")
        else:
          #logDebug(f"#dateTime:[{dateTime}]")
          utcTime = datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S")
          
      except Exception as e:
        logError("Error:[{}] -> dateTime:[{}] is failed to convert to epochTime".format(e, dateTime))
        raise ValueError(e)
      
    elif "-" in dateTime:
      #logDebug(f"#dateTime:[{dateTime}]")
      try:
        if "Z" in dateTime:
          #logDebug(f"#dateTime:[{dateTime}]")
          if "." in dateTime:
            #logDebug(f"#dateTime:[{dateTime}]")
            utcTime = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S.%fZ")
          else:
            #logDebug(f"#dateTime:[{dateTime}]")
            utcTime = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%SZ")
        elif "." in dateTime:
          #logDebug(f"#dateTime:[{dateTime}]")
          utcTime = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S.%f")
        else:
          #logDebug(f"#dateTime:[{dateTime}]")
          try:
            utcTime = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
          except:
            utcTime = datetime.strptime(dateTime, "%Y-%m-%d")
      except Exception as e:
        logError("Error:[{}] -> dateTime:[{}] is failed to convert to epochTime".format(e, dateTime))
        raise ValueError(e)
  
  return utcTime

def getDateString(dateTime = "now", returnFormat = "datetime"):
  if isinstance(dateTime, float) or isinstance(dateTime, int):
    #logDebug(f"#dateTime:[{dateTime}]")
    if dateTime > 10000000000:
      targetDateString = datetime.fromtimestamp(dateTime/1000).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
      targetDateString = datetime.fromtimestamp(dateTime).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')
    #logDebug("dateTime:[{}] is converted to epochTime:[{}] -> targetDate:[{}]".format(dateTime, dateTime, targetDateString))
    return targetDateString
  
  elif isinstance(dateTime, str):
    utcTime = getUTCTime(dateTime)
    #logDebug(f"#dateTime:[{dateTime}]->utcTime:[{utcTime}]")
    if utcTime == None:

      try:
        dateTime = float(dateTime)
        if dateTime > 10000000000:
          targetDateString = datetime.fromtimestamp(dateTime/1000).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
          targetDateString = datetime.fromtimestamp(dateTime).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')
        #logDebug("dateTime:[{}] is converted to epochTime:[{}] -> targetDate:[{}]".format(dateTime, dateTime, targetDateString))
        return targetDateString
      
      except:
        logWarn(f"dateTime:[{dateTime}] is not a valid date format or float")
        
    else:
      epochTime = (utcTime - datetime(1970, 1, 1)).total_seconds()
      #logDebug(f"#dateTime:[{dateTime}] is converted to epochTime:[{epochTime}]")
        
      if returnFormat == "epochtime":
        #logDebug("#epochTime:[{}]".format(epochTime))
        return epochTime
      elif returnFormat == "cloudwatch":
        logDebug("#dateTime:[{}] is converted to epochTime:[{}]".format(dateTime, epochTime))
        return int(epochTime * 1000)
      else:
        logDebug("#dateTime:[{}] is converted to epochTime:[{}]".format(dateTime, epochTime))
        return dateTime
  
    #logDebug(f"##dateTime:[{dateTime}] might be a relative time!")
    if dateTime in ["", "now", None, "None"]:
      targetTime = time.time()
    
    elif isinstance(dateTime, str) and len(dateTime.split(' ')) > 0:
      date_list = dateTime.split(' ')
      #logDebug( "date_list:[{}]".format(date_list))
      firstNumber = float(date_list[0])
      #logDebug("firstNumber:[{}]".format(firstNumber))
      
      if "sec" in date_list[1]:
        numberOfSeconds = firstNumber
      elif "min" in date_list[1]:
        numberOfSeconds = firstNumber * 60
      elif "hour" in dateTime:
        numberOfSeconds = firstNumber * 3600
      elif "day" in dateTime:
        numberOfSeconds = firstNumber * 24 * 3600
      elif "week" in dateTime:
        numberOfSeconds = firstNumber * 7 * 24 * 3600
      elif "month" in dateTime:
        numberOfSeconds = firstNumber * 365 * 24 * 3600 / 12
      elif "year" in dateTime:
        numberOfSeconds = firstNumber * 365 * 24 * 3600 
      else:
        numberOfSeconds = firstNumber
        
      if "ago" in dateTime:
        targetTime = time.time() - numberOfSeconds
        #logDebug( "now:[{}] -> seconds:[{}] -> targetTime:[{}]".format(now, numberOfSeconds, targetTime))
      else:
        targetTime = time.time() + numberOfSeconds
    else:
      targetTime = dateTime
      
    targetDateString = datetime.fromtimestamp(targetTime).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #logDebug( "dateTime:[{}] is converted to epochTime:[{}] -> targetDate:[{}]".format(dateTime, targetTime, targetDateString))
    
    if returnFormat == "datetime":
      #logDebug("dateTime:[{}] -> returnValue:{}".format(dateTime, targetDateString))
      return targetDateString
    elif returnFormat == "cloudwatch":
      returnValue = int(targetTime * 1000)
      #logDebug("dateTime:[{}] -> returnValue:{}".format(dateTime, returnValue))
      return returnValue
    elif returnFormat in ["fileTimestamp","timestamp"]:
      returnValue = datetime.fromtimestamp(targetTime).astimezone(timezone('UTC')).strftime('%Y-%m-%dT%H-%M-%S-%fZ')
      #logDebug("dateTime:[{}] -> returnValue:{}".format(dateTime, returnValue))
      return returnValue
    elif returnFormat in ["date"]:
      returnValue = datetime.fromtimestamp(targetTime).astimezone(timezone('UTC')).strftime('%Y-%m-%d')
      #logDebug("dateTime:[{}] -> returnValue:{}".format(dateTime, returnValue))
      return returnValue
    else:
      #logDebug("dateTime:[{}] -> returnValue:{}".format(dateTime, targetTime))
      return targetTime
    
  else:
    #logDebug(f"#dateTime:[{dateTime}]")
    raiseValueError(f"dateTime:{dateTime} isn't able to be parted to date format:[{returnFormat}]")

def getValueFromRequest(keyword, request_dict):
  #logDebug("keyword:[{}]".format(keyword))
  #for key in request_dict.keys():
  #  logInfo("key:[{}]:[{}]".format(key, request_dict[key]))
    
  if len(keyword.strip()) > 1:
    lowerKeyword = keyword.strip()[0].lower() + keyword.strip()[1:]
    upperKeyword = keyword.strip()[0].upper() + keyword.strip()[1:]
  elif len(keyword.strip()) != 0:
    lowerKeyword = keyword.strip()[0].lower()
    upperKeyword = keyword.strip()[0].upper()
  else:
    return None
  
  if "inputs" in request_dict.keys() and isinstance(request_dict["inputs"], dict):
    for key in request_dict["inputs"].keys():
      if key in [lowerKeyword, upperKeyword]:
        return request_dict["inputs"][key]

  for key in request_dict.keys():
    if key in [lowerKeyword, upperKeyword]:
      return request_dict[key]
    
def getIPv4AddressDetails(ipAddress):
  if isinstance(ipAddress, str):
    pass
  else:
    return [
      {
        "error": "unexpected type:{}:ipAddress:[{}]".format(type(ipAddress), ipAddress)
        }
      ]
    
  thisResult_list = []
  
  ipAddress_list = ipAddress.split(".")
  if len(ipAddress_list) == 4 and  ipAddress_list[0][-1] in ["0","1","2","3","4","5","6","7","8","9"]:
    if ipAddress_list[0] == "0":
      thisResult_list.append(
        {
          "ipAddress": ipAddress,
          "cidr":"0.0.0.0/8",
          "regionCode": None,
          "prefixListId": None,
          "prefixListName": None,
          "partition":"local",
          "notice":"rfc6890"
          }
        )
    elif ipAddress_list[0] == "10":
      thisResult_list.append(
        {
          "ipAddress": ipAddress,
          "cidr":"10.0.0.0/8",
          "regionCode": None,
          "prefixListId": None,
          "prefixListName": None,
          "partition": "private",
          "notice": "RFC 1918/RFC 6761, Used for local communications within a private network"
          }
        )
    elif ipAddress_list[0] == "100" and ipAddress_list[1] in ["64","65","66","67","68","69","70","71",
                                                              "72","73","74","75","76","77","78","79",
                                                              "80","81","82","83","84","85","86","87",
                                                              "88","89","90","91","92","93","94","95",
                                                              "96","97","98","99","101","102","103","104",
                                                              "105","106","107","108","109","110","111","112",
                                                              "113","114","115","116","117","118","119","120",
                                                              "121""122","123","124","125","126","127"]:
      thisResult_list.append(
        {
          "ipAddress": ipAddress,
          "cidr":"100.64.0.0/10",
          "regionCode": None,
          "prefixListId": None,
          "prefixListName": None,
          "partition": "carrier-nat",
          "notice": "RFC 6598, Shared address space for communications between a service provider and its subscribers when using a carrier-grade NAT"
          }
        )

    elif ipAddress_list[0] == "127":
      thisResult_list.append(
        {
          "ipAddress": ipAddress,
          "cidr":"127.0.0.0/8",
          "regionCode": None,
          "prefixListId": None,
          "prefixListName": None,
          "partition": "localhost",
          "notice":"RFC 6890, Used for loopback addresses to the local host."
          }
        )
    elif ipAddress_list[0] == "169" and ipAddress_list[1] == "254":
      thisResult_list.append(
        {
        "ipAddress": ipAddress,
        "cidr":"169.254.0.0/16",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "subnet",
        "notice": "Used for link-local addresses[6] between two hosts on a single link when no IP address is otherwise specified, such as would have normally been retrieved from a DHCP server."
        }
      )
    elif ipAddress_list[0] == "172" and ipAddress_list[1] in ["16","17","18","19","20","21","22","23",
                                                              "24","25","26","27","28","29","30","31",
                                                              "32","33","34","35","36","37","38","39",
                                                              "40","41","42","43","44","45","46","47"]:
      thisResult_list.append(
        {
        "ipAddress": ipAddress,
        "cidr":"172.16.0.0/12",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "private",
        "notice":"RFC 1918/RFC 6761, Used for local communications within a private network"
        }
      )
    elif ipAddress_list[0] == "192" and ipAddress_list[1] == "168":
      thisResult_list.append(
      {
        "ipAddress": ipAddress,
        "cidr":"192.168.0.0/16",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "private",
        "notice": "RFC 1918/RFC 6761, Used for local communications within a private network"
        }
      )
    elif ipAddress_list[0] == "198" and ipAddress_list[1] in ["18","19"]:
      thisResult_list.append(
        {
        "ipAddress": ipAddress,
        "cidr":"198.18.0.0/15",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "asn",
        "notice":"RFC 6201 and RFC 6815, Used for benchmark testing of inter-network communications between two separate subnets"
        }
      )
    elif ipAddress_list[0] == "255" and ipAddress_list[1] == "255"and ipAddress_list[2] == "255"and ipAddress_list[3] == "255" :
      thisResult_list.append(
        {
        "ipAddress": ipAddress,
        "cidr":"255.255.255.255/32",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "broadcast",
        "notice":"RFC 6890, Reserved for the 'limited broadcast destination address"
        }
      )
    elif ipAddress_list[0] in ["240","241","242","243","244","245","246","247","248","249",
                               "250","251","252","253","254","255"]:
      thisResult_list.append(
        {
        "ipAddress": ipAddress,
        "cidr":"240.0.0.0/4",
        "regionCode": None,
        "prefixListId": None,
        "prefixListName": None,
        "partition": "Internet(Reserved)",
        "notice":"RFC 6201 and RFC 6815, Used for benchmark testing of inter-network communications between two separate subnets"
        }
      )
    elif exists(join(expanduser(getRoot()), "awsIpRanges")):
      try:
        ipRangeHomeDir = join(expanduser(getRoot()), "awsIpRanges")
        
        thisIpAddressPath = ipRangeHomeDir
        for thisIpNumber in ipAddress.split(".")[:-1]:
          thisIpAddressPath = join(thisIpAddressPath, thisIpNumber)
          
        #logDebug("#thisIpAddressPath:[{}]".format(thisIpAddressPath))
        
        if exists(thisIpAddressPath):
          dirs = listdir( thisIpAddressPath )
          isIpAddressFound = False
          for filename in dirs:
            #logDebug("#filename:[{}]".format(filename))
            try:
              fp = open(join(thisIpAddressPath, filename))
              ipDetails_dict = json.load(fp)
              if "ipList" in ipDetails_dict.keys() and ipAddress in ipDetails_dict["ipList"]:
                thisResult_list.append(
                  {
                    "ipAddress": ipAddress,
                    **ipDetails_dict["ipInfo"]
                    }
                  )
              #else:
              #  thisResult_list.append(
              #  {
              #    "ipAddress": ipAddress,
              #    **ipDetails_dict
              #    }
              #  )
              isIpAddressFound = True
              #logDebug("ipDetails_dict:[{}]".format(ipDetails_dict))
            except:
              logException("unexpected information:[{}] at ipAddress:[{}]".format(ipDetails_dict, ipAddress))
              
                
          
          if isIpAddressFound == False:
            thisResult_list.append(
              {
                "ipAddress": ipAddress,
                "cidr": None,
                "regionCode": None,
                "prefixListId": None,
                "prefixListName": None,
                "partition": "public"
                }
            )
          else:
            if len(thisResult_list) > 1:
              newResult_dict = {
                "ipAddress": ipAddress,
                "cidr": None,
                "regionCode": None,
                "prefixListId": None,
                "prefixListName": None,
                "partition": None
                }
              
              for thisIpAddress_dict in thisResult_list:
                for key in ["cidr", "regionCode", "prefixListId", "prefixListName", "partition", "notice"]:
                  if key in thisIpAddress_dict.keys() and thisIpAddress_dict[key] != None:
                    thisIpAddress_dict[key] = thisIpAddress_dict[key].lower()
                    if newResult_dict[key] == thisIpAddress_dict[key]:
                      continue
                    elif newResult_dict[key] == None:
                      newResult_dict[key] = thisIpAddress_dict[key]
                    elif isinstance(newResult_dict[key], list):
                      if thisIpAddress_dict[key] not in newResult_dict[key]:
                        newResult_dict[key].append(thisIpAddress_dict[key])
                    else:
                      if "amazon" in newResult_dict[key]:
                        newResult_dict[key] = thisIpAddress_dict[key]
                      elif "amazon" in thisIpAddress_dict[key] and "amazon" not in newResult_dict[key]:
                        pass
                      elif newResult_dict[key]!= thisIpAddress_dict[key]:
                        newResult_dict[key] = [newResult_dict[key], thisIpAddress_dict[key]]
                      else:
                        pass
            
              thisResult_list = [newResult_dict]
        else:
          thisResult_list.append(
            {
              "ipAddress": ipAddress,
              "cidr": None,
              "regionCode": None,
              "prefixListId": None,
              "prefixListName": None,
              "partition": "public"
              }
          )
      except:
        thisResult_list.append(
          {
            "error":logException("unexpected error:[{}]".format(ipAddress))
            }
          )
    else:
      thisResult_list.append(
        {
          "ipAddress": ipAddress,
          "cidr": None,
          "regionCode": None,
          "prefixListId": None,
          "prefixListName": None,
          "partition": "public",
          "notice":"{} is not provisioned. Run '[Data Provisioning] EC2 Prefix Lists' template!".format(join(expanduser(getRoot()), "awsIpRanges"))
          }
        )
  
  return thisResult_list

def getChunkedLists(original_list, chunkSize=10):
  chunked_list = []
  chunkSize = chunkSize
  thisChunk_list = []
  
  if isinstance(original_list, list):
    for thisItem in original_list:
      if len(thisChunk_list) >= chunkSize:
        chunked_list.append(thisChunk_list)
        thisChunk_list = []
      
      thisChunk_list.append(thisItem)
        
    if len(thisChunk_list) > 0:
      chunked_list.append(thisChunk_list)
  
  elif isinstance(original_list, dict):
    for key in original_list.keys():
      if len(thisChunk_list) >= chunkSize:
        chunked_list.append(thisChunk_list)
        thisChunk_list = []
        
      thisChunk_list.append(
        {
          "key": key,
          "value": original_list[key]
          }
        )
    
    if len(thisChunk_list) > 0:
      chunked_list.append(thisChunk_list)
  
  elif isinstance(original_list, str):
    for thisLetter in original_list:
      if len(thisChunk_list) >= chunkSize:
        chunked_list.append(thisChunk_list)
        thisChunk_list = ""
      
      thisChunk_list += thisLetter
        
    if len(thisChunk_list) > 0:
      chunked_list.append(thisChunk_list)
       
  else:
    raiseValueError("type:[{}] is not supported".format(type(original_list)))
  
  return chunked_list


def getMD5ChecksumForData(data):
    hasher = hashlib.md5()
    # Encode the data to bytes, as the hashing function expects bytes-like objects
    data = data.encode()
    hasher.update(data)
    
    return hasher.hexdigest()


    
