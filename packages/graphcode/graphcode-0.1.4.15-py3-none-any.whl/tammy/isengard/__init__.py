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
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError, getLogFilename

from graphcode.unittest import unitTest

from pathway import updateMsg
from tammy.midway import PdxMidway, mRequest

import json

import time

import logging

import boto3
import botocore

def describeIsengardAccounts(userAccountId , loginAliasId):
  pdxMidway = PdxMidway(userAccountId = userAccountId, loginAliasId = loginAliasId)
  
  mR = pdxMidway.mRequest( 
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
  logDebug("mR(len:{:,}):[{}]".format(len(mR), mR))
  
  permissionsForUser_list = []
  url="https://isengard-service.amazon.com/"
  payload_dict = {}
  requestCount = 0
  beginTime = time.time()
  while (time.time() - beginTime) < 930:
    requestCount += 1
    mR = pdxMidway.mRequest(url, payload_dict)
    logDebug("(#{:,},{:,.1f}s)\tmR(len:{:,}):[{}]".format(requestCount, time.time() - beginTime, len(mR), mR))
    try:
      r_dict = mR
      for isengardAccountItem_dict in r_dict["PermissionsForUserList"]:
        permissionsForUser_list.append(isengardAccountItem_dict)
        logDebug("isengardAccountItem_dict(len:{:,}):[{}]".format(len(permissionsForUser_list), isengardAccountItem_dict))
      try:
        payload_dict["NextToken"] = r_dict["NextToken"]
      except:
        logException("no NextToken")
        break
    except:
      logException("failed to load json:[{}]".format(mR))
      break
  
  return permissionsForUser_list


def describeAssumeRoleCredential(userAccountId , loginAliasId):
  pdxMidway = PdxMidway(userAccountId = userAccountId, loginAliasId = loginAliasId)
  
  mR = pdxMidway.mRequest(
           url="https://isengard-service.amazon.com/", 
           payload={"AWSAccountID":"682757144375","IAMRoleName":"Admin"}, 
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
  logDebug("mR(len:{:,}):[{}]".format(len(mR), mR))
  
  return json.loads(mR["AssumeRoleResult"])

def runAPIOverAssumeRole(userAccountId , loginAliasId, errorReason_list=[], logMessage_list=[]):
  isengardCrendential_dict = describeAssumeRoleCredential(userAccountId , loginAliasId)
  
  for key in isengardCrendential_dict.keys():
    logDebug("{}:[{}]".format(key, isengardCrendential_dict[key]))
             
  thisResult_list = []
  try:
    thisLogLevel = logging.getLogger().level
    logging.getLogger().setLevel(logging.INFO)
    curAssumedStsClient=boto3.client(
        'sts',
        aws_access_key_id=isengardCrendential_dict["credentials"]['accessKeyId'],
        aws_secret_access_key=isengardCrendential_dict["credentials"]['secretAccessKey'],
        aws_session_token=isengardCrendential_dict["credentials"]['sessionToken'],
    )
    logInfo("assumedAccountId:[{}]".format(curAssumedStsClient.get_caller_identity().get('Account')))
    logging.getLogger().setLevel(thisLogLevel)
    
    try:
      thisLogLevel = logging.getLogger().level
      logging.getLogger().setLevel(logging.INFO)
      session = boto3.Session(
        aws_access_key_id=isengardCrendential_dict["credentials"]['accessKeyId'],
        aws_secret_access_key=isengardCrendential_dict["credentials"]['secretAccessKey'],
        aws_session_token=isengardCrendential_dict["credentials"]['sessionToken'],
        region_name="us-west-2",
      )
      logging.getLogger().setLevel(thisLogLevel)
      
      try:
        thisLogLevel = logging.getLogger().level
        logging.getLogger().setLevel(logging.INFO)
        s3Resource = session.resource('s3')
        s3Client = session.client('s3')
        logging.getLogger().setLevel(thisLogLevel)
        
        try:
          logWarn("credential is expired in {:,} seconds".format(int(isengardCrendential_dict["credentials"]["expiration"]/1000 - time.time())))
          # List all buckets
          for bucket in s3Resource.buckets.all():
            logDebug("s3://{}/".format(bucket.name))
            
          try:
            # Specify your bucket name
            userAccountId = "682757144375"
            bucket_name = '{}-{}-midway'.format(userAccountId, loginAliasId)
            
            # Check if the bucket already exists
            isExistBucket = True
            try:
              s3Resource.meta.client.head_bucket(Bucket=bucket_name)
            except botocore.exceptions.ClientError as e:
              # If a client error is thrown, then check that it was a 404 error.
              # If it was a 404 error, then the bucket does not exist.
              error_code = int(e.response['Error']['Code'])
              if error_code == 404:
                  isExistBucket = False
            
            # If the bucket does not exist, create it
            if not isExistBucket:
              s3Resource.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
              logDebug(f'Bucket {bucket_name} created.')
              
            else:
              logDebug(f'Bucket {bucket_name} already exists.')
              
            try:
              # Enable server-side encryption
              s3Client.put_bucket_encryption(
                  Bucket=bucket_name,
                  ServerSideEncryptionConfiguration={
                      'Rules': [
                          {
                              'ApplyServerSideEncryptionByDefault': {
                                  'SSEAlgorithm': 'AES256'
                              }
                          },
                      ]
                  }
              )
            except botocore.exceptions.ClientError as e:
              # If a client error is thrown, then check that it was a 404 error.
              # If it was a 404 error, then the bucket does not exist.
              error_code = int(e.response['Error']['Code'])
              updateMsg(errorReason_list, logException("failed to apply server-size encryption:{}:[{}]".format(error_code, e)))
            
            try:
              s3BucketPolicy = {
                "Version": "2012-10-17",
                "Statement": [
                  {
                    "Sid": "AddCannedAcl",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::900629971091:user/moduaws-x-midway-access"
                    },
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": "arn:aws:s3:::{}-{}-midway/cookie".format(userAccountId, loginAliasId)
                  }
                ]
              }
              # Convert the policy to a JSON string
              s3BucketPolicy_string = json.dumps(s3BucketPolicy)
              
              # Set the bucket policy
              s3Client.put_bucket_policy(
                  Bucket=bucket_name,
                  Policy=s3BucketPolicy_string
              )
            except botocore.exceptions.ClientError as e:
              # If a client error is thrown, then check that it was a 404 error.
              # If it was a 404 error, then the bucket does not exist.
              error_code = int(e.response['Error']['Code'])
              updateMsg(errorReason_list, logException("failed to put bucket policy:{}:[{}]".format(error_code, e)))
              
          except:
            updateMsg(errorReason_list, logException("unexpected error with query:[{}]".format("curQueries")))
        except:
          updateMsg(errorReason_list, logException("unexpected query:[{}]".format("curQueries")))
      except:
        updateMsg(errorReason_list, logException("unable to initiate 'athenaBoto3Client' with 'bubblewandCrendentials'"))
    except:
      updateMsg(errorReason_list, logException("unable to initiate 'athenaBoto3Client' with 'bubblewandCrendentials'"))
  except:
    updateMsg(errorReason_list, logException("unable to initiate 'assumeStsClient' with 'bubblewandCrendentials'"))
    
  return thisResult_list



def midwayRequestTest(userAccountId = None, loginAliasId = "hoeseong"):
  pdxMidway = PdxMidway(userAccountId = "749952098923", loginAliasId = loginAliasId)
  
  mR = pdxMidway.mRequest(
           url="https://isengard-service.amazon.com/sso/login", 
           payload=None, 
           headers="""
GET /sso/login HTTP/2
Host: isengard-service.amazon.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
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
  logDebug("mR(len:{:,}):[{}]".format(len(mR), mR))

  mR = pdxMidway.mRequest(
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
  logDebug("mR(len:{:,}):[{}]".format(len(mR), mR))
  
  permissionsForUser_list = []
  url="https://isengard-service.amazon.com/"
  payload_dict = {"AWSAccountID":"749952098923","IAMRoleName":"Admin"}
  requestCount = 0
  beginTime = time.time()
  while (time.time() - beginTime) < 930:
    requestCount += 1
    mR = pdxMidway.mRequest(url, payload_dict)
    logDebug("(#{:,},{:,.1f}s)\tmR(len:{:,}):[{}]".format(requestCount, time.time() - beginTime, len(mR), mR))
    try:
      r_dict = mR
      for isengardAccountItem_dict in r_dict["PermissionsForUserList"]:
        permissionsForUser_list.append(isengardAccountItem_dict)
        logDebug("isengardAccountItem_dict(len:{:,}):[{}]".format(len(permissionsForUser_list), isengardAccountItem_dict))
      try:
        payload_dict["NextToken"] = r_dict["NextToken"]
      except:
        logException("no NextToken")
        break
    except:
      logException("failed to load json:[{}]".format(mR))
      break

def localUnitTest():
  unitTestFunction_dict = {#"midwayRequestTest":{"target":midwayRequestTest, "args":()},
                           #"describeIsengardAccounts":{"target":describeIsengardAccounts,  "args":("749952098923", "hoeseong", )}
                           #"describeAssumeRoleCredential":{"target":describeAssumeRoleCredential,  "args":("749952098923", "hoeseong", )}
                           "runAPIOverAssumeRole":{"target":runAPIOverAssumeRole,  "args":("749952098923", "hoeseong", )}
                           
                           
                          }
  
  unitTest(unitTestFunction_dict)
  
if __name__ == "__main__":
  localUnitTest()
