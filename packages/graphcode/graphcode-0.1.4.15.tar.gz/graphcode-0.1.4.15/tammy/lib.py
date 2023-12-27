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
Created on Jan 1, 2001
Modified on Jun 30, 2023

@contributor: hoeseong
'''
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

def getRegionCodeWithUsageType(usageType):
  
  # Original Source
  # https://w.amazon.com/bin/view/Region%28AWS%29/
  
  regionCode_dict = {
    "USE1":{"regionCode":"us-east-1", "airportCode":"IAD", "partition":"aws", "regionName":"US East (N. Virginia)", "AZ":"us-east-1[abcdef]"},
    "EUW1":{"regionCode":"eu-west-1", "airportCode":"DUB", "partition":"aws", "regionName":"Europe (Ireland)", "AZ":"eu-west-1[abc]"},
    "USW1":{"regionCode":"us-west-1", "airportCode":"SFO", "partition":"aws", "regionName":"US West (N. California)", "AZ":"us-west-1[abc]"},
    "APS1":{"regionCode":"ap-southeast-1", "airportCode":"SIN", "partition":"aws", "regionName":"Asia Pacific (Singapore)", "AZ":"ap-southeast-1[abc]"},
    "APN1":{"regionCode":"ap-northeast-1", "airportCode":"NRT", "partition":"aws", "regionName":"Asia Pacific (Tokyo)", "AZ":"ap-northeast-1[abcd]"},
    "UGW1":{"regionCode":"us-gov-west-1", "airportCode":"PDT", "partition":"aws-us-gov", "regionName":"AWS GovCloud (US-West)", "AZ":"us-gov-west-1[abc]"},
    "USW2":{"regionCode":"us-west-2", "airportCode":"PDX", "partition":"aws", "regionName":"US West (Oregon)", "AZ":"us-west-2[abcd]"},
    "SAE1":{"regionCode":"sa-east-1", "airportCode":"GRU", "partition":"aws", "regionName":"South America (Sao Paulo)", "AZ":"sa-east-1[abc]"},
    "APS2":{"regionCode":"ap-southeast-2", "airportCode":"SYD", "partition":"aws", "regionName":"Asia Pacific (Sydney)", "AZ":"ap-southeast-2[abc]"},
    "CNN1":{"regionCode":"cn-north-1", "airportCode":"BJS", "partition":"aws-cn", "regionName":"China (Beijing)", "AZ":"cn-north-1[ab]"},
    "UIE1":{"regionCode":"us-iso-east-1", "airportCode":"DCA", "partition":"aws-iso", "regionName":"US ISO East", "AZ":"us-iso-east-1[abc]"},
    "EUC1":{"regionCode":"eu-central-1", "airportCode":"FRA", "partition":"aws", "regionName":"Europe (Frankfurt)", "AZ":"eu-central-1[abc]"},
    "APN2":{"regionCode":"ap-northeast-2", "airportCode":"ICN", "partition":"aws", "regionName":"Asia Pacific (Seoul)", "AZ":"ap-northeast-2[ab]"},
    "APS3":{"regionCode":"ap-south-1", "airportCode":"BOM", "partition":"aws", "regionName":"Asia Pacific (Mumbai)", "AZ":"ap-south-1[abc]"},
    "USE2":{"regionCode":"us-east-2", "airportCode":"CMH", "partition":"aws", "regionName":"US East (Ohio)", "AZ":"us-east-2[abc]"},
    "CAN1":{"regionCode":"ca-central-1", "airportCode":"YUL", "partition":"aws", "regionName":"Canada (Central)", "AZ":"ca-central-1[ab]"},
    "EUW2":{"regionCode":"eu-west-2", "airportCode":"LHR", "partition":"aws", "regionName":"Europe (London)", "AZ":"eu-west-2[abc]"},
    "UBE1":{"regionCode":"us-isob-east-1", "airportCode":"LCK", "partition":"aws-iso-b", "regionName":"US ISOB East (Ohio)", "AZ":"us-isob-east-1[abc]"},
    "CNW1":{"regionCode":"cn-northwest-1", "airportCode":"ZHY", "partition":"aws-cn", "regionName":"China (Ningxia)", "AZ":"cn-northwest-1[abc]"},
    "EUW3":{"regionCode":"eu-west-3", "airportCode":"CDG", "partition":"aws", "regionName":"Europe (Paris)", "AZ":"eu-west-3[abc]"},
    "APN3":{"regionCode":"ap-northeast-3", "airportCode":"KIX", "partition":"aws", "regionName":"Asia Pacific (Osaka)", "AZ":"ap-northeast-3[a]"},
    "UGE1":{"regionCode":"us-gov-east-1", "airportCode":"OSU", "partition":"aws-us-gov", "regionName":"AWS GovCloud (US-East)", "AZ":"us-gov-east-1[abc]"},
    "EUN1":{"regionCode":"eu-north-1", "airportCode":"ARN", "partition":"aws", "regionName":"Europe (Stockholm)", "AZ":"eu-north-1[abc]"},
    "APE1":{"regionCode":"ap-east-1", "airportCode":"HKG", "partition":"aws", "regionName":"Asia Pacific (Hong Kong)", "AZ":"ap-east-1[abc]"},
    "MES1":{"regionCode":"me-south-1", "airportCode":"BAH", "partition":"aws", "regionName":"Middle East (Bahrain)", "AZ":"me-south-1[abc]"},
    "EUS1":{"regionCode":"eu-south-1", "airportCode":"MXP", "partition":"aws", "regionName":"Europe (Milan)", "AZ":"eu-south-1[abc]"},
    "AFS1":{"regionCode":"af-south-1", "airportCode":"CPT", "partition":"aws", "regionName":"Africa (Cape Town)", "AZ":"af-south-1[abc]"},
    "UIW1":{"regionCode":"us-iso-west-1", "airportCode":"APA", "partition":"aws-iso", "regionName":"US ISO West", "AZ":"us-iso-west-1[abc]"},
    "EUS2":{"regionCode":"eu-south-2", "airportCode":"ZAZ", "partition":"aws", "regionName":"Europe (Spain)", "AZ":"eu-south-2[abc]"},
    "APS4":{"regionCode":"ap-southeast-3", "airportCode":"CGK", "partition":"aws", "regionName":"Asia Pacific (Jakarta)", "AZ":"ap-southeast-3[abc]"},
    "MEC1":{"regionCode":"me-central-1", "airportCode":"DXB", "partition":"aws", "regionName":"Middle East (UAE)", "AZ":"me-central-1[abc]"},
    "EUC2":{"regionCode":"eu-central-2", "airportCode":"ZRH", "partition":"aws", "regionName":"Europe (Zurich)", "AZ":""},
    "APS5":{"regionCode":"ap-south-2", "airportCode":"HYD", "partition":"aws", "regionName":"Asia Pacific (Hyderabad)", "AZ":""},
    "APS6":{"regionCode":"ap-southeast-4", "airportCode":"MEL", "partition":"aws", "regionName":"Asia Pacific (Melbourne)", "AZ":"ap-southeast-4[abc]"},
    "ILC1":{"regionCode":"il-central-1", "airportCode":"TLV", "partition":"aws", "regionName":"Israel (Tel Aviv)", "AZ":""},
    "LAX1":{"regionCode":"us-west-2-lax", "airportCode":"LAX", "partition":"aws", "regionName":"Los Angelis(us-west-2)", "AZ":"us-west-2-lax-1"},
    }
  
  if usageType in [None, "null"]:
    
    return {
      "usageType":"",
      "regionCode":"", 
      "airportCode":"",
      "partition":"", 
      "regionName":"", 
      "AZ":""
      }
    
  else:
    usageType_list = usageType.split("-")
    usageTypePrefix = "{}".format(usageType_list[0]).strip().upper()
    if len(usageType) > len(usageType_list[0]):
      usageTypePost = "{}".format(usageType[len(usageType_list[0])+1:])
    else:
      usageTypePost = usageType
    
    if usageTypePrefix in regionCode_dict.keys():
      return {
        "usageType":usageTypePost,
        **regionCode_dict[usageTypePrefix]
        }
    else:
      if usageTypePrefix in ["EU"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["EUW1"]
          }
      
      elif usageTypePrefix in ["AP", "JP"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["APN1"]
          }
      
      elif usageTypePrefix in ["CA"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["CAN1"]
          }
      
      elif usageTypePrefix in ["CA"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["CAN1"]
          }
        
      elif usageTypePrefix in ["IN"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["APS3"]
          }
      
      elif usageTypePrefix in ["IN"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["APS3"]
          }
      
      elif usageTypePrefix in ["ME"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["MES1"]
          }
      
      elif usageTypePrefix in ["SA"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["SAE1"]
          }
        
      elif usageTypePrefix in ["AU"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["APS2"]
          }
        
      elif usageTypePrefix in ["ZA"]:
        return {
          "usageType":usageTypePost,
          **regionCode_dict["EUS2"]
          }
      
      elif len(usageTypePrefix) > 3\
          or (len(usageTypePrefix) == 3 and usageTypePrefix[-1] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])\
          or usageTypePrefix in ["US", "NA", "IAD"]:
      
        return {
          "usageType":usageType,
          **regionCode_dict["USE1"]
          }
        
      elif len(usageTypePrefix) == 1 or usageTypePrefix in ["QS", "IA", "AF"]:
        
        return {
          "usageType":usageType,
          **regionCode_dict["USE1"]
          }
        
      else:
        
        return {
          "usageType":usageType,
          "regionCode":usageTypePrefix, 
          "airportCode":None,
          "partition":"aws", 
          "regionName":None, 
          "AZ":None
          }
    
    