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
    pdxMidway = PdxMidway(
      userAccountId= request_dict["metadata"]["awsAccountId"], 
      loginAliasId= request_dict["metadata"]["userName"]
      )
    r = mRequest(pdxMidway, 
                 url="https://isengard-service.amazon.com/", 
                 payload=None, 
                 headers="""
                  User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
                  Accept: application/json, text/plain, */*
                  Accept-Language: en-US,en;q=0.5
                  Accept-Encoding: gzip, deflate, br
                  Content-Type: application/json; charset=UTF-8
                  Content-Encoding: amz-1.0
                  X-Amz-Target: com.amazon.isengard.coral.IsengardService.ListPermissionsForUser
                  anti-csrftoken-a2z-request: true
                  X-ALTERNATE-CONTINGENT-AUTHORIZATION-PROVIDER: shoehorn
                  X-ISENGARD-AUTHORIZATION-VERSION: LATEST
                  Content-Length: 18
                  Origin: https://isengard.amazon.com
                  Connection: keep-alive
                  Referer: https://isengard.amazon.com/
                  Cookie: amzn_sso_rfp=cb893d6f61203bcb; amzn_sso_token=eyJ0eXAiOiJKV1MiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEzMDgzMjMxIn0.eyJpc3MiOiJodHRwczovL21pZHdheS1hdXRoLmFtYXpvbi5jb20iLCJzdWIiOiJob2VzZW9uZyIsImF1ZCI6Imh0dHBzOi8vaXNlbmdhcmQtc2VydmljZS5hbWF6b24uY29tOjQ0MyIsImV4cCI6MTY4NTgyOTgxMiwiaWF0IjoxNjg1ODI4OTEyLCJhdXRoX3RpbWUiOjE2ODU4Mjc2ODYsIm5vbmNlIjoiNTY1NDIxZTVmZTA1YzcyZGM0ZGNkNTIxODQ3MzlhNDk4YWE5ODljODYxN2Q3ZjY0MDViNjBmMjRlNDQ0NjA3NiIsImFtciI6IltcInBpblwiLCBcInUyZlwiXSIsInRydXN0X3Njb3JlIjpudWxsLCJyZXFfaWQiOm51bGwsIm1pZHdheV90cnVzdF9zY29yZSI6bnVsbCwiYXBlc19yZXN1bHRzIjpudWxsLCJpYWwiOjMsImFhbCI6MywianRpIjoiWXYySFJYeFNXYi9HdGVqVGFmMTVEZz09IiwicG9zdHVyZV9jaGVjayI6MCwibXdpIjowfQ.iKCwmKE5Xm-4OH1j-FgeK1FgGVi2QaboFDF07FG3bisq2_pq0XWjtpSjsMb0aHjsz65xbvGuWYWHq9A9RLlT8SHKu5fugX5Gm3pLvwxBsCN678g8fysGD0hUfZAjecOsII2HAfqbR0fEQlivOkb5igVaIZ45NPgXd1ajEWrRixHYW_IwY9e2M3qcn04Z-FatPuA9xnPoxQLqkxlx0Fmlv5hasxfsa_18igtMMiFB17ixuR_esuzg0sBungju_YNu0InilohpYPonT8IM19EerwSH6C_w7Yci1bGZ0xs9wPCU2j4HVeeYrgXsT7CCAtSPFfoa4tHkODdiew6dratUXw
                  Sec-Fetch-Dest: empty
                  Sec-Fetch-Mode: cors
                  Sec-Fetch-Site: same-site
                  TE: trailers
                  """, 
                 verbose=True)
    logDebug("r.content(len:{:,}):[{}]".format(len(r.content), r.content))
    
    isengardAccount_list = []
    url="https://isengard-service.amazon.com/"
    payload_dict = {"AWSAccountID":"","IAMRoleName":"Admin"}
    requestCount = 0
    beginTime = time.time()
    while (time.time() - beginTime) < 930:
      requestCount += 1
      r = pdxMidway.request(url, payload_dict)
      logDebug("(#{:,},{:,.1f}s)\tr.content(len:{:,}):[{}]".format(requestCount, time.time() - beginTime, len(r.content), r.content))
      try:
        r_dict = r.json()
        for isengardAccountItem_dict in r_dict["PermissionsForUserList"]:
          isengardAccount_list.append(isengardAccountItem_dict)
          logDebug("isengardAccountItem_dict(len:{:,}):[{}]".format(len(isengardAccount_list), isengardAccountItem_dict))
        try:
          payload_dict["NextToken"] = r_dict["NextToken"]
        except:
          logException("no NextToken")
          break
      except:
        logException("failed to load json:[{}]".format(r.content))
        break
    
  except Exception as e:
    updateMsg(errorReason_list, logException("unexpected request_dict:[{}]".format(request_dict)))
    isengardAccount_list = []
  
  return {
    "isengardAccounts": isengardAccount_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }
