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

from pathway import updateMsg
from wooju.args import getInputs, getAccountId, getIAMRoleName

from tammy.midway import PdxMidway, mRequest

import time

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
  
  try:
    input_dict = getInputs(request_dict)
    
    try:
      accountId = getAccountId(input_dict)
      iamRoleName = getIAMRoleName(input_dict)
    except:
      logExceptionWithValueError("invalid isengard account Id or IAM Role")
    
    url="https://isengard-service.amazon.com/"
    payload_dict = {"AWSAccountID":accountId,"IAMRoleName":iamRoleName}
    
    pdxMidway = PdxMidway(
      userAccountId= request_dict["metadata"]["awsAccountId"], 
      loginAliasId= request_dict["metadata"]["userName"]
      )
    r = mRequest(pdxMidway, 
                 url=url, 
                 payload=payload_dict, 
                 headers="""
                  POST / HTTP/2
                  Host: isengard-service.amazon.com
                  User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
                  Accept: application/json, text/plain, */*
                  Accept-Language: en-US,en;q=0.5
                  Accept-Encoding: gzip, deflate, br
                  Content-Type: application/json; charset=UTF-8
                  Content-Encoding: amz-1.0
                  X-Amz-Target: com.amazon.isengard.coral.IsengardService.GetAssumeRoleCredentials
                  anti-csrftoken-a2z-request: true
                  anti-csrftoken-a2z: g9DHttyhZHvDhdT6DF7VuP87V29nUTYD/baGDChh8Z7qAAAAAQAAAABkfMYlcmF3AAAAAFgvVn0PIwwHD+olH/E9xQ==
                  X-ALTERNATE-CONTINGENT-AUTHORIZATION-PROVIDER: shoehorn
                  X-ISENGARD-AUTHORIZATION-VERSION: LATEST
                  Content-Length: 53
                  Origin: https://isengard.amazon.com
                  Connection: keep-alive
                  Referer: https://isengard.amazon.com/
                  Cookie: amzn_sso_rfp=ccef7131718320fd; amzn_sso_token=eyJ0eXAiOiJKV1MiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEzMDgzMjMxIn0.eyJpc3MiOiJodHRwczovL21pZHdheS1hdXRoLmFtYXpvbi5jb20iLCJzdWIiOiJob2VzZW9uZyIsImF1ZCI6Imh0dHBzOi8vaXNlbmdhcmQtc2VydmljZS5hbWF6b24uY29tOjQ0MyIsImV4cCI6MTY4NTkwMjMzOCwiaWF0IjoxNjg1OTAxNDM4LCJhdXRoX3RpbWUiOjE2ODU4OTU4MTMsIm5vbmNlIjoiZmM4MGZjYTUxZTgwMzAzNjkwYjAwYzUxNTZmMTljMzQ5MTg3NWE5MGRhZWRkYjFjMTE3YmFiMjUwMWEyMTdmMSIsImFtciI6IltcInBpblwiLCBcInUyZlwiXSIsInRydXN0X3Njb3JlIjpudWxsLCJyZXFfaWQiOm51bGwsIm1pZHdheV90cnVzdF9zY29yZSI6bnVsbCwiYXBlc19yZXN1bHRzIjpudWxsLCJpYWwiOjMsImFhbCI6MywianRpIjoia2J2aXFuWVl3bTlVZ0VxSU5wZ05HQT09IiwicG9zdHVyZV9jaGVjayI6MCwibXdpIjowfQ.x9f9mocUMkp7PbQWi9CQNMTQJgSTpbSej3TC_tmoWz8hpkv5kDC94ywjzMYvTn0avjfd_wdHUvSh_GGANRIbRx3VamlZc5Z_Ls2FFBRe7iXoh-HGLO6nDWQxM__EiYjtf-eD0j5TTYTSJeaHBrVAKZY30t1v36Uwq9ApUkFSuFs1csRSLpzhFGKzVoAm437hq6OZW09yQ_LqfXQsBR0t8H985_0S05hjtz_nQ-IEmNgWVK63TMHnNLTrOALpNiec3lqgTsH10TZIBvk_1_6cMtgj2g64k4Zg2X_s-ecobVPR-7rhgqCdkVGPQ9qkmEUpGngq9Pclb3WmSJc8SLZGUA
                  Sec-Fetch-Dest: empty
                  Sec-Fetch-Mode: cors
                  Sec-Fetch-Site: same-site
                  TE: trailers
                  """, 
                 verbose=True)
    logDebug("r.content(len:{:,}):[{}]".format(len(r.content), r.content))
    
    assumeRoleResult_list = [r.json()]
    
  except Exception as e:
    updateMsg(errorReason_list, logException("unexpected request_dict:[{}]".format(request_dict)))
    assumeRoleResult_list = [request_dict]
  
  return {
    "assumeRoleResult": assumeRoleResult_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
