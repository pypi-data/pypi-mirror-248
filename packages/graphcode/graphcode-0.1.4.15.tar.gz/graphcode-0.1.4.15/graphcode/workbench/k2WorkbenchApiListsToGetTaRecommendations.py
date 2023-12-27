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


def getK2WorkbenchApiListsToGetTaRecommendations(categoryName="cost_optimizing"):
  return [
            
            {
              "platform":"moduAWS",
              "apiName":"nosave-ta.setTargetValues", 
              "args":{},
              #"inputs": {"primaryKeys": "instances,state"},
              "pt":"1x1"
              },
            { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"language":"en"},"apiName":"trustedadvisor.describeTrustedAdvisorChecks","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
              "platform":"k2",
              "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
              "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
              "inputs":"sourceApiName=nosave-ta.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
              "conditions":"category == {}".format(categoryName),
              "limit":"1",
              "pt":"1x1"
              },
            {
              "platform":"moduAWS",
              "apiName":"modu.combineResultsAsList",
              "args":"",
              "inputs":"sourceApiName=nosave-ta.setTargetValues;targetValues=accountId_:accountId_,regionCode_:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
              "conditions":"",
              "limit":"",
              "pt":"32x8"
              },
            { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkIds":["Qch7DwouX1"]},"apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
              "platform":"k2",
              "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
              "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkIds\":${__checkIds__}}",
              "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkIds:checkIds_list;primaryKeys=resourcesSummary,categorySpecificSummary,costOptimizing",
              "conditions":"",
              "limit":"",
              "pt":"8x8"
              },
            {
              "platform":"k2",
              "apiName":"trustedadvisor.describeCheckItems",
              "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\",\"count\":100,\"start\":0}",
              "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId;primaryKeys=properties",
              "conditions":"totalCount > 0",
              "limit":"",
              "pt":"8x8"
              }
            ]