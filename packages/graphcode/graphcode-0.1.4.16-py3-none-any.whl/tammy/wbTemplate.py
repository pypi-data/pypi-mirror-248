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

import json

pdxWbTemplate_dict = {
  # begin: Template Items
  "__Template__" : {
    "meta" : {
      "reportName": "",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"1",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         }
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[A.UnitTest] setTargetValues" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946,393495018094,132064880640;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946,393495018094,132064880640;regionCode_=us-east-1,us-west-2",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         }
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[A.UnitTest] filterResults" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script with filtering results",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946,393495018094,132064880640;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946,393495018094,132064880640;regionCode_=us-east-1,us-west-2",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_,regionCode_:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         }
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[A.UnitTest] combineResults" : {
    "meta" : {
      "reportName": "moduAWS' UnitTest: 'combineResults'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=021824079065,028009399290,035580655376,041003132611,044096650143,052684788981,078499015708,099356522462,101661720690,103641018243,109434410235,110145862301,116448481841,134001856083,166440397761,181489996397,209772739983,210157577452,213413494671,214790005682,224670914335,232388941425,257325184575,260637879381,265263573940,273104076548,273114391775,274186386842,279767409586,282643525406,286564069533,292012218142",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv", #;addAccountDetails=yes;accountDetailColumns=masterOwnerAliasId,masterOwnerJobLevel,conduitName
         "conditions":"",
         "limit":"1",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;combineWith=ec2.describeRegions;asValues=regionCode:regionName;nocsv",
         "conditions":"accountId_ != accountId_",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId_:accountId_,regionCode_:us-east-1,regionCode_list:regionCode_list",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[A.UnitTest] joinResults" : {
    "meta" : {
      "reportName": "UnitTest: 'joinResults'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=982499846871;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode_:us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_,regionCode_:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkIds\":${__checkIds__}}",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkIds:checkIds_list;primaryKeys=resourcesSummary,categorySpecificSummary",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeCheckItems",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\",\"count\":100,\"start\":0}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"totalCount > 0",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.joinResults",
         "args":"",
         "inputs":"sourceApiName=trustedadvisor.describeCheckItems;targetValues=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;targetColumns=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;joinWith=trustedadvisor.describeTrustedAdvisorChecks;indexKeys=checkId:id;joinValues=category:category,name:name",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[A.UnitTest] conditions v1" : {
    "meta" : {
      "reportName": "UnitTest: conditions v1",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2;clusterIdentifier=cluster-1;nodeType=ds2.8xlarge;numberOfNodes=8;automatedSnapshotRetentionPeriod=11;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+123",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=us-east-1,eu-west-1;clusterIdentifier=cluster-2;nodeType=ds2.8xlarge;numberOfNodes=4;automatedSnapshotRetentionPeriod=12;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000001;regionCode_=eu-west-1,us-west-2;clusterIdentifier=cluster-3;nodeType=ds2.8xlarge;numberOfNodes=6;automatedSnapshotRetentionPeriod=13;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+123",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=us-west-2,ap-northeast-1;clusterIdentifier=cluster-4;nodeType=ds2.8xlarge;numberOfNodes=3;automatedSnapshotRetentionPeriod=14;fleetName=PlusTAM2;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=,ap-northeast-1,ap-northeast-2;clusterIdentifier=cluster-5;nodeType=ds2.8xlarge;numberOfNodes=7;automatedSnapshotRetentionPeriod=14;fleetName=PlusTAM2;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=,ap-northeast-1,ap-northeast-2;clusterIdentifier=cluster-6;nodeType=ds2.8xlarge;numberOfNodes=6;automatedSnapshotRetentionPeriod=14;fleetName=PlusTAM2;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"fleetName==PlusTAM2",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"fleetName!=PlusTAM",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"regionCode_==\"\"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"regionCode!=\"\"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"regionCode<>\"\"",
         "limit":"",
         "pt":"1x1"
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"us-east-1,eu-west-1 in regionCode",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"regionCode<>us-east-1",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"numberOfNodes>3",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"numberOfNodes>=3",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"numberOfNodes<=6",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName;nocsv",
         "conditions":"numberOfNodes<6",
         "limit":"",
         "pt":""
          },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[A.UnitTest] conditions v2" : {
    "meta" : {
      "reportName": "UnitTest: conditions v2",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"today",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"rds.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=021824079065,028009399290,035580655376,041003132611,044096650143,052684788981,078499015708,099356522462,101661720690,103641018243,109434410235,110145862301,116448481841,134001856083,166440397761,181489996397,209772739983,210157577452,213413494671,214790005682,224670914335,232388941425,257325184575,260637879381,265263573940,273104076548,273114391775,274186386842,279767409586,282643525406,286564069533,292012218142",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache",
         "conditions":"engineVersion startsWith 5.7.mysql_,5.6.mysql_",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items  # begin: Template Items
  # begin: Template Items
  "[A.UnitTest] primaryKeys" : {
    "meta" : {
      "reportName": "UnitTest: primaryKeys",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"today",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=015162136117,190225106431,159586396623,225836362124,213741646905,268889722472,344691037878,458036547247,580952770835,264534990656,317108535030,255060517824,427896624473,462887716314,306701351329,589352793208,971771347730,513396412904,529339670897,601565657821,022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items  # begin: Template Items
  # begin: Template Items
  "[A.UnitTest] gcWorker" : {
    "meta" : {
      "reportName": "simple gcWorker with 'ec2.describeRegions'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000329793683,001296614954,001296614954,003165184628,003750325075,006367750530,006877342108,007847965835,008816838810,009232224236,009317442756,013961087900,014827827310,014094952746,015126675781,017346173817,017346173817,019359821655,014700897649,018461279294,017595932766,017595932766,017595932766,019068282770,019068282770,019068282770,022241274188,023394019542,025855969140,026978028269,023245816879,023245816879,026466494910,028019436642,029773783190,033681564839,034543630514,028617553031,037440828910,037825720272,042088423083,043702531683,030642824637,045518652857,046315329157,050471633556,049582645670,054278508970,055708428572,055746098824,056316637276,055757804653,057631253129,062466298097,063035930465,062928457341,061064852545,065473930595,065473930595,065622908326,067477145022,071783920447,071526322190,074594706144,077133846967,076847879360,080759781363,076287230973,083381731785,084301292476,090624670839,087996303655,087996303655,087350076831,087350076831,087350076831,091924841599,091924841599,095592909384,097325747696,097325747696,099401977503,099379748324,099379748324,098187645741,097325747696,101294758116,101239549872,103617466507,104405634662,106319821491,104250483325,108253656547,108582510160,104720108972,110304820781,104728609414,112252611752,112252611752,116221945093,110669586418,113878760346,118143952654,116495818219,116495818219,116495818219,116414772574,122485286853,120427139534,123896679585,123896679585,124461370093,123854306897,126618032726,125704643346,126648622561,127424005255,127513330695,127513330695,125264553657,128714475912,128631447701,129424065119,128897925358,129775668773,130202251701,129423269365,135129598374,133339299872,135295371550,135570291122,135809287734,134922358275,136679104205,133096428928,137161761431,141429874596,143302960083,143302960083,143302960083,143510767938,141576387080,146785944316,148057179496,148407204176,145388651995,145388651995,145388651995,149267624824,149035339608,151795757168,151795757168,148928884632,148928884632,148928884632,154427569070,153296682161,153296682161,153296682161,158687082845,159447222712,159447222712,157068072895,157813472004,162940651508,164787093381,166188460781,167650521883,163130619424,166324077247,165697249114,170208030609,163900054030,166440397761,175517081540,173245911106,173245911106,173245911106,173245911106,173245911106,172388888774,172388888774,172388888774,172388888774,177607377190,177607377190,179508555488,179562296833,175597527982,175038910433,181260841849,179508555488,177607377190,177607377190,183211140689,179196476213,183703362924,173791657605,173791657605,173791657605,173791657605",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"20",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"20",
         "pt":"1x2"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"20",
         "pt":"2x2"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"20",
         "pt":"4x4"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=173791657605,173791657605,173791657605,184210370075,187419755406,187419755406,193292859011,191739929183,193092826592,195671117483,199396420469,195002208138,198626806141,198626806141,201077281628,195002208138,204742525914,204742525914,206395122802,205716101922,211159821154,207551056681,208754896688,208754896688,208754896688,203086089599,212754733528,215444340651,219846761515,221928594302,220436760551,220436760551,229250341897,227472729388,227059491784,227778750723,227778750723,232506540267,232940318313,228499644484,228499644484,228895086958,228895086958,228895086958,234247224352,230291048615,231329507939,230257644885,230257644885,230257644885,230257644885,230257644885,230257644885,230257644885,238213668761,238842934746,239223005171,237274843635,240863366520,243107287761,238258148368,238258148368,238258148368,238258148368,245658940982,247865103217,250582001414,247822705840,251835715680,253666071958,253715324151,256365639555,256531637837,257700410668,255795624902,255491646761,255491646761,255491646761,255491646761,255491646761,255491646761,264354949529,261868325606,264938696210,263773377697,265093408162,264904912585,270304315320,269074218892,271667415556,272431307106,272431307106,271046053347,272247947445,275957715724,275768039747,280341680746,278407181058,281294611242,281294611242,281294611242,281294611242,281294611242,282754956369,286001588900,285397154863,286847699088,297027794159,297025927541,296325891127,295704874868,298255032128,291428775132,302152441892,297664461520,305147448587,304977213075,299789551061,307967312063,306652714457,306652714457,311521508443,312097123782,316488361389,312726812299,316550374861,316550374861,321357527106,321717027744,321376006657,322501589544,323369557988,320686849287,324752265808,330975014577,330254618156,330254618156,327597887447,328013042116,330524338235,330801203043,330801203043,333217932916,336473673731,336473673731,331582574546,331582574546,331582574546,335958447558,335958447558,340787569010,341601687788,341855472306,341855472306,340601203962,340601203962,348008215064,348802193101,348802193101,351048237671,351048237671,355548666665,355548666665,354958825018,354958825018,354958825018,359315761917,359048081192,359048081192,359182851103,357973626758,362486724382,360617868296,360617868296,360617868296,365372228066,366176457946,361635393421,361635393421,361635393421,366943732680,369910267373,374101486847,373378166616,382439410445,379465194282,379465194282,382194065056,384618036985,381669516200,387007552908,392431065556,392431065556,389064547767,392047214295,392047214295,396882386025,392653884982,398189610229,400577501318,403044179878,403380951071,401702013472,405011868927,405011868927,404787441142,404940326529,404940326529,408776769476,408776769476,408776769476,408776769476,412688533494,411453145397,410032269524,415691916567,413804790683,417423247104,417556863011,417556863011,417556863011,417556863011,418410395865,418107464722,418721161500,418410395865,418410395865,418410395865,419392876308,424255581144,424255581144,420235933266,420235933266,420235933266,418721571849,423021027057,426273902372,426273902372,428410964248,428410964248,428410964248,429015652749,433343227396,429866930877,431808850450,428692134250,439406533952,437979813554,436722826590,442113390062,440424277418,437289334404,443118612835,447666759503,446719958359,444659959678,446567294750,449386515065,454839265530,459149796389,455978179168,456792862910,454604630859,458933854353,458933854353,458933854353,458933854353,458933854353,456257508612,464969708333,468320167683,476661036218,478237332583,477322658813,477322658813,477322658813,479924080659,479924080659,494800821764,486945565862,490402366029,495558875261,494800821764,497921794547,498762148899,496400366764,501227804824,494800821764,494800821764,494800821764,502874022509,501221294148,502257195121,504619545186,503658896756,503658896756,503600885884,507086023554,507086023554,505425699908,505425699908,509651510223,513566894637,509651510223,512685637007,512107398930,512107398930,514686788991,514946557544,516614242606,516614242606,516336264508,518855391546,520436872184,520436872184,518389211895,518389211895,527517527045,521994816191,521994816191,521994816191,531254035343,528987001739,525260373493,532017376979,534761160048,534863053320,535621169259,535525985741,538394939592,534908316875,534908316875,539040832729,539672091648,539672091648,537889504681,542282540856,540734382552,539672091648,545862023671,544055925088,546977253982,544249845999,550415838089,549889021425,550865727611,550562467464,549073162761,552755470235,552755470235,554390797621,556162099287,556162099287,557916386253,559159669221,555658464217,555658464217,552929162109,552929162109,556532785517,552929162109,563885087084,562887058884,564142706006,560587263722,564269543180,563299767174,564878433832,564878433832,564878433832,564878433832,564878433832,559875748285,566986268470,565909519604,568185385710,569456961653,570058527293,572403768812,572403768812,575626908832,579543709451,579543709451,576694657041,581152931290,581001671492,583635506537,580733870549,573797080752,578860762227,582549501291,583127333080,583127333080,585039668622,585039668622,585039668622,585039668622,585039668622,585039668622,585039668622,578457045416,578457045416,585194553397,590220165699,589322623153,590220165699,592592853216,590305710930,591938332231,592069268835,590672172367,592319933906,592319933906,594352672171,599974187934,600707530200,599748404309,605006185751,609273206340,608132050907,612188748514,608292486723,614540059676,614540059676,610840366085,610838143689,610838143689,614954247069,617180728163,614727502325,616882873929,610998306924,610998306924,610998306924,610998306924,610998306924,616283686529,616375136225,622636351908,623948198680,624795640991,624560244903,624560244903,625937666460,627459610072,627459610072,627459610072,626604985312,634998619167,635518756937,633731934467,637304138898,637304138898,641113671333,641113671333,639515405961,637512096403,637512096403,647363740995,644650238765,644650238765,654492621873,653964530899,651572782767,656043438700,657317918350,657350921402,656043438700,657018391063,657018391063,657512166465,657051926755,657051926755,660526271402,662688591944,662426358452,666921696942,662957305949,665448329738,667869208744,665145855371,667833275882,667700492575,670224922795,672287344102,671530538177,669225328263,669225328263,669225328263,669225328263,669225328263,676928108425,679192728740,675874886680,675874886680,679703056607,677763292306,684499138540,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,673385534282,689233868829,689735871768,691151434628,691882732873,697184828953,695797383594,696448918100,701004869671,701102681275,698438953816,698438953816,704244056411,701367514220,705384086425,705384086425,705537144360,705537144360,708630184122,709608990362,713273840555,714933982414,714933982414,714131305234,719363555814,715983024208,716599625984,719899310365,719744160437,720960275437,727595612155,722378490160,731632893994,728369368508,726422461855,731716036949,730167430579,730167430579,730167430579,730167430579,730167430579,730167430579,735165518788,733357332728,734190661318,738462021157,741537507491,730927465629,730927465629,730927465629,730927465629,730927465629,731612419148,731612419148,731612419148,731612419148,731612419148,731612419148,729021728316,729021728316,736899304759,745307335980,746391156699,746391156699,747118528785,744622736866,744622736866,748817547182,746950721301,746950721301,750662078340,755840738472,751170926685,751170926685,751170926685,751170926685,751170926685,768234628229,768061111968,768879299511,768105912660,767709958174,768838084945,768838084945,768222027863,769690751364,771604386909,775129918171,773938212369,776937900829,779356323519,778146362239,779792137174,779195120033,783644466077,782068482191,781024548603,783644466077,779940235857,783644466077,784514946934,784514946934,787055673683,787543296852,787543296852,786822822720,788936522797,789961471372,789961471372,788370161278,786199351466,787415093188,788354713624,795689685041,792528545229,792146759042,792275472017,797899015553,795291916159,800140160957,800061266592,800261124827,801527512531,804934456786,802186535730,802186535730,802186535730,802186535730,807564238314,813552494197,812065978683,812073004561,812073004561,813614817327,817972593424,816412960395,816412960395,812065978683,820789164175,820191205953,823190234294,823190234294,820234496171,821325050343,821325050343,824876266604,823260963621,824536183797,824536183797,824438620528,826152162798,826152162798,826152162798,826152162798,832382923097,833413971997,833108852567,831865383457,830880331518,835596416679,838590096234,838476866803,835731356302,836612856323,839002355101,838476866803,836790072983,836790072983,836790072983,836790072983,836790072983,838476866803,842666396395,841631579559,843700614504,841737567649,842380212714,847915245642,847780067294,840785816044,840785816044,840785816044,839430550009,839430550009,847357478208,851592290188,847460339551,846665638365,851206257882,854717454119,850586551722,850586551722,850586551722,851170259539,853624848959,857224189487,854971433644,856720810451,854605751242,860951108493,857570274937,861276052759,860861218333,856863762344,862411402583,857626688762,857626688762,862814238953,856863762344,856863762344,856863762344,856863762344,856863762344,856863762344,856863762344,856863762344,863944306515,863944306515,863944306515,865258189129,873624430394,868653755646,868653755646,868653755646,868653755646,868653755646,868653755646,874650622006,873201765632,873201765632,873201765632,873201765632,874091887885,874117545505,876715736989,880918510484,879398671514,877052650256,877747842282,877747842282,882821796113,892231984916,886493890244,891676106660,895799599216,889596722188,898437527959,895763055142,897963408722,894210074590,902268789844,903423002429,901834348909,907824790985,904747083714,899561508533,899561508533,905536703371,906529323700,906529323700,911678815677,911678815677,914037250613,919833413337,918140592619,921019319901,921805017580,925937187722,921232273325,923686165227,923116177876,923116177876,923116177876,921019319901,921019319901,921019319901,924637445623,924637445623,924637445623,924637445623,926084843267,926084843267,926084843267,926084843267,926084843267,926084843267,926084843267,926084843267,924073652755,924073652755,924073652755,924073652755,924073652755,924073652755,924073652755,924073652755,934714903970,930174789969,930174789969,932501224203,932438937876,932438937876,934727388548,934727388548,932185418089,932185418089,937915940396,934181291337,936669141694,940149484202,941837803842,941837803842,938264988051,941596354548,941596354548,941019354859,952829627313,951099399227,952523777466,952523777466,953529694912,953529694912,961492582528,957189322033,959090772145,960572535373,957692748486,957692748486,970173614275,970173614275,969544337710,968761973157,969991223233,969991223233,969991223233,969731471597,969991223233,969991223233,969991223233,969991223233,969991223233,969991223233,971194227195,971689922504,969991223233,969991223233,969991223233,969991223233,982794338965,981907103865,982429840325,984737787211,984737787211,987618679499,985152408570,985152408570,987186832690,991755236981,987745976635,989560875978,988716064909,988716064909,989560875978,994698236012,989470033077,989470033077,989560875978,991929992584,991929992584,991929992584,991929992584,991929992584,991580769585,994171604129,998511035472,998310328250",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"#ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"100",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"#ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"100",
         "pt":"24x8"
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[A.UnitTest] gcWorker with local Cache*" : {
    "meta" : {
      "reportName": "Simple gcWorker with local cache",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=642824637,033681564839,034543630514,042088423083,043702531683,045518652857,046315329157,054278508970,055708428572,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,077133846967,080759781363,084301292476,087350076831,090624670839,091924841599,095592909384,097325747696,099401977503",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache;localCacheTTL=0;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[A.UnitTest] getRegions" : {
    "meta" : {
      "reportName": "getRegions",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"serviceName=EC2;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId,regionCode:regionCode;primaryKeys=instances,state",
         "conditions":"",
         "limit":"10",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"#ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=EC2;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"moduAWS",
         "apiName":"eks.getRegions",
         "args":"",
         "inputs":"serviceName=EC2,EKS;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=eks.getRegions;targetValues=accountId:accountId,regionCode:regionCode;primaryKeys=instances,state",
         "conditions":"",
         "limit":"10",
         "pt":"16x8"
         },
      ]
    }, # end: Template Item#  
  # begin: Template Items
  "[A.UnitTest] account Id Chunks" : {
    "meta" : {
      "reportName": "get accountId chunks",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"1 days ago",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"getDwServiceUsages",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"getDwServiceRegionCodes",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"getDwActiveS3Resources",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"getDwActiveS3Resources",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;accountIdChunkCount=10",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items

  # begin: Template Items
  "[A.UnitTest] deletePreviousK2Results" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu1.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=015162136117,190225106431,159586396623,225836362124,213741646905,268889722472,344691037878,458036547247,580952770835,264534990656,317108535030,255060517824",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=modu1.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=427896624473,462887716314,306701351329,589352793208,971771347730,513396412904,529339670897,601565657821,022241274188,023245816879,023394019542,025855969140",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=modu2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"modu3.setTargetValues",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;regionCode_=us-east-1;nocsv;accountId_=026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=modu3.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[A.UnitTest] uploadCsvResultToS3" : {
    "meta" : {
      "reportName": "moduAWS' UnitTest: 'uploadCsvResultToS3'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=273982773946;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/unitTest/;csvFilename=unitTest-describeRegions-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadJsonResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/unitTest/;jsonFilename=unitTest-describeRegions-${{SNAPSHOT_DATE}}.json",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[D.UnitTest] Email Notification" : {
    "meta" : {
      "reportName": "[${__fleetName__}]  Email Notification Test",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using Amazon RDS MySQL/MariaBD/PostgreSQL databases which will be ended the support of your <b>${__affectedResourceCount__} databases</b> by Feb. 9, 2021 which has already published on October 16, 2020 and notified you via <a href='https://phd.aws.amazon.com/phd/home#/dashboard/open-issues'>AWS Personal Health Dashboard</a>.<br>
<br>
After <b>the Feb. 9, 2021 deadline</b>,<br>
<br>
1) <b>RDS will upgrade your MySQL 5.5 databases to 5.7</b> during a scheduled maintenance window between Feb 9, 2021 00:00:01 UTC and March 9, 2021 00:00:01 UTC. On March 9, 2021 00:00:01 AM UTC, any Amazon RDS for MySQL 5.5 databases that remain will be upgraded to version 5.7 regardless of whether the instances are in a maintenance window or not.<br>
<br>
2) <b>RDS will upgrade your MariaDB 10.0 and 10.1 databases to 10.3</b> during a scheduled maintenance window between Feb 9, 2021 00:00:01 UTC and March 9, 2021 00:00:01 UTC. On March 9, 2021 00:00:01 AM UTC, any Amazon RDS for MariaDB 10.0 and 10.1 databases that remain will be upgraded to version 10.3 regardless of whether the instances are in a maintenance window or not.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8175'>Announcement: Amazon RDS for MySQL 5.5 End-of-Life date is approaching</a></li>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8174'>Announcement: Amazon RDS for MariaDB 10.0 and 10.1 End-of-Life date is approaching</a></li>
  <li><a href='https://aws.amazon.com/premiumsupport/knowledge-center/notification-maintenance-rds-redshift/'>How do I configure notifications for Amazon RDS?</a></li>
  <li><a href='https://www.mysql.com/support/eol-notice.html'>[External] MySQL Product Support EOL Announcements</a></li>
  <li><a href='https://mariadb.org/about/#maintenance-policy'>[External] MariaDB Maintenance policy</a></li>
</ul>
Please, create a support request at your AWS Console that AWS Support can help you get the paths to green. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a></b><br>
AWS RDS team<br>
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1;clusterIdentifier=cluster-1;nodeType=ds2.8xlarge;numberOfNodes=8;automatedSnapshotRetentionPeriod=11;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+123",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=us-east-1;clusterIdentifier=cluster-2;nodeType=ds2.8xlarge;numberOfNodes=8;automatedSnapshotRetentionPeriod=12;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000001;regionCode_=us-east-1;clusterIdentifier=cluster-3;nodeType=ds2.8xlarge;numberOfNodes=8;automatedSnapshotRetentionPeriod=13;fleetName=PlusTAM;masterOwnerAliasId=hoeseong+123",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=us-east-1;clusterIdentifier=cluster-4;nodeType=ds2.8xlarge;numberOfNodes=3;automatedSnapshotRetentionPeriod=14;fleetName=PlusTAM2;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000002;regionCode_=us-east-1;clusterIdentifier=cluster-5;nodeType=ds2.8xlarge;numberOfNodes=8;automatedSnapshotRetentionPeriod=14;fleetName=PlusTAM2;masterOwnerAliasId=hoeseong+911",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=masterOwnerAliasId:masterOwnerAliasId,accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier,nodeType:nodeType,numberOfNodes:numberOfNodes,automatedSnapshotRetentionPeriod:automatedSnapshotRetentionPeriod,fleetName:fleetName",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
          },
        {"platform":"moduAWS",
         "apiName":"modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.filterResults;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,clusterIdentifier,nodeType,numberOfNodes,automatedSnapshotRetentionPeriod,fleetName;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, 
  # end: Template Items#  
  # begin: Template Items
  "[B.UnitTest] gcApi - analyze" : {
    "meta" : {
      "reportName": "",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"analyze.servicequotas",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         }
      ]
    }, # end: Template Items,
  # begin: Template Items
  "[B.UnitTest] gcApi - profile" : {
    "meta" : {
      "reportName": "",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"profile.list",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         }
      ]
    }, # end: Template Items,
  # begin: Template Items
  "[B.UnitTest] avs.getAccountStatus" : {
    "meta" : {
      "reportName": "moduAWS' UnitTest: 'avs.getAccountStatus'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=021824079065,028009399290,035580655376,041003132611,044096650143,052684788981,078499015708,099356522462,101661720690,103641018243,109434410235,110145862301,116448481841,134001856083,166440397761,181489996397,209772739983,210157577452,213413494671,214790005682,224670914335,232388941425,257325184575,260637879381,265263573940,273104076548,273114391775,274186386842,279767409586,282643525406,286564069533,292012218142",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
          "platform":"k2",
          "apiName":"avs.getAccountStatus",
          "args":"{\"accountIds\":[\"${__accountId__}\"]}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:us-east-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
          "platform":"k2",
          "apiName":"avs.getAccountStatus",
          "args":"{\"accountIds\":[\"${__accountId__}\"]}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:us-east-1",
          "conditions":"accountStatus == Active",
          "limit":"",
          "pt":"1x1"
          },
        {"platform":"moduAWS",
         "apiName":"modu.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=regionCode:regionCode_;combineWith=modu.setTargetValues;asValues=accountIds:accountId_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
          "platform":"k2",
          "apiName":"avs.getAccountStatus",
          "args":"{\"accountIds\":${__accountIds__}}",
          "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:us-east-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[B.UnitTest] cloudwatch.getMetricStatistics: boto3 / k2": {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId=132064880640;regionCode=us-east-1;tableName=test;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:endpointName;period=300",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName;period=3600",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName;mode=summary",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName;period=3600",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId,regionCode:regionCode,tableName:tableName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;dimensions=TableName:tableName;period=3600;mode=summary",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[B.UnitTest] cloudwatch.getMetricStatistics: paginating" : {
    "meta" : {
      "reportName": "cloudwatch.getMetricStatistics - paginating for multiple time periods",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000;arnV4=app/customization-scene7/f75fe3076432b70b,app/classification-smartlogic-alb/8cb19b9d4eda1f3f,app/Eureka-ALBVPC1/05faf62f19b6b203,app/sfx-lbfarga-KQCG0NEEX3KA/f188c3ba55d30b92,app/uxf-ecs/ca48b9773d8d70d6,app/athleaderboardv1-lb/54a38aec6d5565be,app/uxf-ecs-tourguide-commerce-prod/e734473036e4e3e4,app/uxf-ecs-commerce-prod/100b1fbb055c5d1c,app/netwo-LoadB-8XY11HHLZOPV/e3d7b27c4c7312c1,app/uxf-bowerman-commerce-prod/738b0fbe44aeff2c,app/launchmetrics-vpc-main/8770ffc453167984,app/uxf-ecs-commerce-prod-non-prod/3c7e1b5c092ba788,app/STERLINGAPP-US-R180421-prod-om/c81ac898ba4fa02f,app/nio-adminopsext-router-alb/d75871eb581bf029,app/nio-adminopsint-router-alb/76e76095d7e56652,app/catalog-main-loadbalancer/e0ddec13eb6a83c2,app/vendor-main-loadbalancer/a0599597cb598ab9,app/merch-main-loadbalancer/c363483b3ad75726,app/merch-vpc1-loadbalancer/aedd7bafaf2ea227,app/STERLINGAPP-EU-R201026-prod-som/bc3c934c62220f22,app/STERLINGAPP-US-R201027-prod-som/87e81bf5b9b6667a,app/STERLINGAPP-CN-R201027-prod-som/b394739e723b6eaf,app/gbi-copyjobservice-alb/c6cce031f48400f2,app/content-cms-loadbalancer/97e43d571c9bc0e3,app/content-halcyon-loadbalancer/7521c7c9546049c0,app/consumerproductapi-vpc1-alb/88473a597942aa36,app/unified-edge-router-alb/8c389b7f14f5b2fa,app/unified-edge-router-alb-int/38e17d9337d207cc,app/customization-services-int-alb/2861a35d45b4dbcd,app/Eureka-External-Alb/da5cb9f6b72e503b,app/unified-edge-migration-alb/e275b0038e7df82c,app/STERLINGAPP-CNR-R220315-prod-ps/838bb3a9277be9ba,app/STERLINGAPP-CND-R220314-prod-ps/0bfd64e321505b00,app/STERLINGAPP-JPD-R220314-prod-ps/76a94064ad5afe5b,app/STERLINGAPP-EUD-R220314-prod-ps/180ff1121bb3d830,app/STERLINGAPP-USD-R220314-prod-ps/f0a29d6b4a9048e0,app/STERLINGAPP-GBL-R0422-prod-nby/9f077a18f164947f,app/payment-notification-ext-alb/218c1a61be6e682f,app/custo-LoadB-1MXBFY40TCV7R/77bf67f1825f71b5,app/netwo-LoadB-1UHCDPNM3K2D1/82ed00435cf8aecb,app/STERLINGAPP-USR-R221116-prod-ps/fe40de2ab4571f38,app/STERLINGAPP-EUR-R221116-prod-ps/19b1b57a0c0721c1,app/STERLINGAPP-JPR-R221116-prod-ps/d8c6c1074628f672,app/STERLINGAPP-CNR-R221116-prod-ps/8b6164a0e4928ef5,app/mp-fulfillmentoptions-prod-alb/cf4c685347061192",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[B.UnitTest] cloudwatch.getMetricStatistics: paginating v2" : {
    "meta" : {
      "reportName": "cloudwatch.getMetricStatistics - paginating for multiple time periods",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"2 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000;arnV4=app/Eureka-ALB/4c26814f3ad16301,app/unified-edge-router-alb/a49eccad161c20e9,app/Eureka-External-Alb/b9234ed067c67e79,app/Eureka-ALB/f1b40a957ab7c97c,app/unified-edge-router-alb/6ac6be0312ee312d,app/Eureka-External-Alb/f8ab4c88134e9822,app/Eureka-ALB/cadea709876f5f86,app/unified-edge-router-alb/48d57314a2f0a630,app/Eureka-External-Alb/ab0039ff17f6f894,app/customization-scene7/f75fe3076432b70b,app/classification-smartlogic-alb/8cb19b9d4eda1f3f,app/Eureka-ALBVPC1/05faf62f19b6b203,app/sfx-lbfarga-KQCG0NEEX3KA/f188c3ba55d30b92,app/uxf-ecs/ca48b9773d8d70d6,app/athleaderboardv1-lb/54a38aec6d5565be,app/uxf-ecs-tourguide-commerce-prod/e734473036e4e3e4,app/uxf-ecs-commerce-prod/100b1fbb055c5d1c,app/netwo-LoadB-8XY11HHLZOPV/e3d7b27c4c7312c1,app/uxf-bowerman-commerce-prod/738b0fbe44aeff2c,app/launchmetrics-vpc-main/8770ffc453167984,app/uxf-ecs-commerce-prod-non-prod/3c7e1b5c092ba788,app/STERLINGAPP-US-R180421-prod-om/c81ac898ba4fa02f,app/nio-adminopsext-router-alb/d75871eb581bf029,app/nio-adminopsint-router-alb/76e76095d7e56652,app/catalog-main-loadbalancer/e0ddec13eb6a83c2,app/vendor-main-loadbalancer/a0599597cb598ab9,app/merch-main-loadbalancer/c363483b3ad75726,app/merch-vpc1-loadbalancer/aedd7bafaf2ea227,app/STERLINGAPP-EU-R201026-prod-som/bc3c934c62220f22,app/STERLINGAPP-US-R201027-prod-som/87e81bf5b9b6667a,app/STERLINGAPP-CN-R201027-prod-som/b394739e723b6eaf,app/gbi-copyjobservice-alb/c6cce031f48400f2,app/content-cms-loadbalancer/97e43d571c9bc0e3,app/content-halcyon-loadbalancer/7521c7c9546049c0,app/consumerproductapi-vpc1-alb/88473a597942aa36,app/unified-edge-router-alb/8c389b7f14f5b2fa,app/unified-edge-router-alb-int/38e17d9337d207cc,app/customization-services-int-alb/2861a35d45b4dbcd,app/Eureka-External-Alb/da5cb9f6b72e503b,app/unified-edge-migration-alb/e275b0038e7df82c,app/STERLINGAPP-CNR-R220315-prod-ps/838bb3a9277be9ba,app/STERLINGAPP-CND-R220314-prod-ps/0bfd64e321505b00,app/STERLINGAPP-JPD-R220314-prod-ps/76a94064ad5afe5b,app/STERLINGAPP-EUD-R220314-prod-ps/180ff1121bb3d830,app/STERLINGAPP-USD-R220314-prod-ps/f0a29d6b4a9048e0,app/STERLINGAPP-GBL-R0422-prod-nby/9f077a18f164947f,app/payment-notification-ext-alb/218c1a61be6e682f,app/custo-LoadB-1MXBFY40TCV7R/77bf67f1825f71b5,app/netwo-LoadB-1UHCDPNM3K2D1/82ed00435cf8aecb,app/STERLINGAPP-USR-R221116-prod-ps/fe40de2ab4571f38,app/STERLINGAPP-EUR-R221116-prod-ps/19b1b57a0c0721c1,app/STERLINGAPP-JPR-R221116-prod-ps/d8c6c1074628f672,app/STERLINGAPP-CNR-R221116-prod-ps/8b6164a0e4928ef5,app/mp-fulfillmentoptions-prod-alb/cf4c685347061192,app/Eureka-ALB/b4794a52fec79cb6,app/uxf-ecs-commerce-prod/1b527a00aa9367bd,app/nio-auth-router-alb/83c8a43a4dd1aceb,app/payment-storedpaymentsbatch-alb/13fa79bbe846b2a7,app/payment-logging-alb/d24732a15449f764,app/merch-vpc1-loadbalancer/eb38d070e8622fd2,app/merch-main-loadbalancer/cdf52aca3d4cb52e,app/unified-edge-router-alb/0c3f7c7f0f683e00,app/Eureka-External-Alb/c1adb531d2839c55,app/unified-edge-migration-alb/cab043b3af81f153,app/payment-notification-ext-alb/af0164eec1aec174,app/nio-adminopsint-router-alb/0b8d49a0616c9bb6,app/STERLINGAPP-JPD-R221010-prod-ps/a9d207c233f98db4",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
      ]
    }, # end: Template Items#
  
  "[B.UnitTest] cloudwatch.getMetricStatistics: paginating v3" : {
    "meta" : {
      "reportName": "cloudwatch.getMetricStatistics - paginating for multiple time periods (DO NOT USE Condtions)",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"2 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[B.UnitTest] dynamoDB + cloudwatch.getMetricStatistics - boto3" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script for cloudwatch.getMetricStatistics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=132064880640;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x2"
         },
        {"platform":"boto3",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x2"
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[B.UnitTest] dynamoDB + cloudwatch.getMetricStatistics - k2" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script for cloudwatch.getMetricStatistics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=132064880640,179149847469,273982773946;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x2"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"4x4"
         },
      ]
    }, # end: Template Items#
    # begin: Template Items
  "[B.UnitTest] cloudwatch.listMetrics - boto3" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"accountId_=132064880640;regionCode_=us-east-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"boto3",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"1",
          "pt":"8x8"
          },
        {"platform":"boto3",
         "apiName":"cloudwatch.listMetrics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"boto3",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
    # begin: Template Items
  "[B.UnitTest] cloudwatch.listMetrics - k2" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"accountId_=000000000000;regionCode_=eu-west-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {"platform":"k2",
         "apiName":"ec2.listMetrics",
         "args":"{\"namespace\":\"AWS/EC2\",\"metricName\":\"CPUUtilization\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary;modeStatic=maximum;modeStaticCount=16",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
    # begin: Template Items
  "[B.UnitTest] cloudwatch.listMetrics - k2 v2" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"accountId_=132064880640;regionCode_=us-east-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"1",
          "pt":"8x8"
          },
        {"platform":"k2",
         "apiName":"cloudwatch.listMetrics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
    # begin: Template Items
  "[B.UnitTest] cloudwatchinternal.searchMetricsForAccount - k2 only" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"accountId_=132064880640;regionCode_=us-east-1",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"1",
          "pt":"8x8"
          },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/Usage\",\"maxResults\":500}",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[B.UnitTest] describeResource.ipAddress" : {
    "meta" : {
      "reportName": "get describeResource.ipAddress",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"ipAddress=146.75.37.63,146.75.33.63,52.94.0.42,52.119.234.232,146.75.33.63,146.75.37.63,52.119.232.78,52.119.232.112,3.5.87.130,3.5.79.191,52.119.228.112,52.94.1.244,3.5.87.117,3.5.81.165,52.92.131.50,20.36.241.212,3.5.86.186,3.5.84.110,3.5.76.184,3.5.78.111,3.5.86.182,3.5.82.186,3.5.76.184,13.56.121.58",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"describeResource.ipAddress",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=ipAddress:ipAddress",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          }
      ]
    }, # end: Template Items#
  
  
    # begin: Template Items
  "[unittest] discoverResources.EC2" : {
    "meta" : {
      "reportName": "get describeResource.ipAddress",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;serviceName=EC2",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"discoverResources.EC2",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[U[C.UnitTest]iscoverServiceQuotas" : {
    "meta" : {
      "reportName": "discover Service Quotas for all available services",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=CloudWatch,DynamoDB,EC2,ELB,KMS,Lambda,OpenSearch,RDS,SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.CloudWatch" : {
    "meta" : {
      "reportName": "CloudWatch Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=CloudWatch",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.CloudWatch",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.DynamoDB" : {
    "meta" : {
      "reportName": "DynamoDB Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=DynamoDB",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.DynamoDB",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
    
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.EC2" : {
    "meta" : {
      "reportName": "OpenSearch Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=EC2",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.EC2",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.ELB" : {
    "meta" : {
      "reportName": "ELB Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=ELB",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.ELB",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.KMS" : {
    "meta" : {
      "reportName": "KMS Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=KMS",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.KMS",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.Lambda" : {
    "meta" : {
      "reportName": "Lambda Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=Lambda",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.Lambda",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.OpenSearch" : {
    "meta" : {
      "reportName": "OpenSearch Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=OpenSearch",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.OpenSearch",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.RDS" : {
    "meta" : {
      "reportName": "RDS Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=RDS",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.RDS",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
    "[C.UnitTest] discoverServiceQuotas.SageMaker" : {
    "meta" : {
      "reportName": "SageMaker Service Limits",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.midwayRequest",
         "args":"",
         "inputs":"url=https://sagemaker-tools.corp.amazon.com/api/limits/us-west-2/067440223434/limits",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=910523329506;regionCode_=us-east-1,us-west-2,eu-west-1;serviceName=SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=360201567367;regionCode_=us-east-1,us-west-2,eu-west-1;serviceName=SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=067440223434;regionCode_=us-east-1,us-west-2,eu-west-1;serviceName=SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=387122980739;regionCode_=us-east-1,us-west-2,eu-west-1;serviceName=SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=529473040773,529237099986,;regionCode_=cn-northwest-1;serviceName=SageMaker",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"discoverServiceQuotas.SageMaker",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas.SageMaker",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"satusColor != Green",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[C.UnitTest] discoverServiceQuotas.SQS" : {
    "meta" : {
      "reportName": "SQS Service Quotas",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=SQS",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceQuotas",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.RDS",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[C.UnitTest] discoverRisks.RDS" : {
    "meta" : {
      "reportName": "RDS Risks",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=RDS",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.discoverRisks",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName,debug:true",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #{"platform":"moduAWS",
        # "apiName":"discoverServiceQuotas.RDS",
        # "args":"",
        # "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[D.UnitTest] Simple Workbench Script - boto3 / k2 with local cache" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=132064880640;regionCode_=us-east-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache;localCacheTTL=0",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"boto3",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache;localCacheTTL=0",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[D.UnitTest] Simple Workbench Script with CN Midway - k2" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script with CN Midway",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=268567822408;regionCode_=cn-north-1",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[D.UnitTest] Simple Workbench Script with Global + CN Midway - k2" : {
    "meta" : {
      "reportName": "Simple moduAWS' Workbench Script with Global and CN Midway",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"cn.setTargetValues",
         "args":"",
         "inputs":"regionCode_=cn-north-1;nocsv;accountId_=004244877001,029752209515,030457427454,030915263494,060866797588,071325582287,096370184348,128763440914,150377450097,150377450097,180724749811,180724749811,195954329327,197385487255,203033652329,230043489214,248674422601,262590116575,268567822408,302980747802,312876897933,314170009407,342343220910,360419527201,369952000899,373321856738,377913298578,486570871508,492776795379,546232066245,554134747561,576604951101,594271083938,624463716149,624572224387,630364620112,630368596392,676634006072,677296654689,677425795008,723179795905,747810879888,782555769305,796521129498,828781696622,834384407997,847827417252,856707768101,915918431428,928864214696,932867256124",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"global.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=642824637,033681564839,034543630514,042088423083,043702531683,045518652857,046315329157,054278508970,055708428572,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,077133846967,080759781363,084301292476,087350076831,090624670839,091924841599,095592909384,097325747696,099401977503",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=cn.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"16",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=global.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"16",
         "pt":"4x4"
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] API Gateway Status" : {
    "meta" : {
      "reportName": "API Gateway Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"apigateway.setTargetValues",
          "args":"",
          "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          },
          { "platform":"k2",
            "apiName":"apigateway.getRestApis", 
            "args":"",
            "inputs":"sourceApiName=apigateway.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
            "pt":"12x8"
            },
          { "platform":"k2",
            "apiName":"apigateway.getStages", 
            "args":"{\"restApiId\":\"${__restApiId__}\"}",
            "inputs":"sourceApiName=apigateway.getRestApis;targetValues=accountId:accountId_,regionCode:regionCode_,restApiId:id",
            "pt":"12x8"
            },
          { "platform":"k2",
            "apiName":"apigateway.getDomainNames", 
            "args":"",
            "inputs":"sourceApiName=apigateway.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
            "pt":"12x8"
            },
          { "platform":"k2",
            "apiName":"apigatewayv2.getApis", 
            "args":"",
            "inputs": "sourceApiName=apigateway.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
            "pt":"12x8"
            },
          { "platform":"k2",
            "apiName":"apigatewayv2.getStages", 
            "args":"{\"apiId\":\"${__apiId__}\"}",
            "inputs":"sourceApiName=apigatewayv2.getApis;targetValues=accountId:accountId_,regionCode:regionCode_,apiId:id",
            "pt":"12x8"
            },
          { "platform":"k2",
            "apiName":"apigatewayv2.getDomainNames", 
            "args":"",
            "inputs":"sourceApiName=apigateway.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
            "pt":"12x8"
            },
        ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 PrefixId Status" : {
    "meta" : {
      "reportName": "EC2 PrefixId Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"accountId_=450881533027;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describePrefixLists",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.getIpAddressesWithCidr",
         "args":"",
         "inputs":"sourceApiName=ec2.describePrefixLists;targetValues=accountId:accountId_,regionCode:regionCode_,cidrs:cidrs,prefixListId:prefixListId,prefixListName:prefixListName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] EC2 VPC Subnet Status - boto3 / k2" : {
    "meta" : {
      "reportName": "[unittest] EC2 VPC Subnet Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"accountId_=132064880640;regionCode_=us-east-1,us-west-2;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"boto3",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] EC2 VPC Details" : {
    "meta" : {
      "reportName": "[unittest] EC2 VPC Details",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVpcs",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRouteTables",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=associations,routes,tags",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInternetGateways",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describePrefixLists",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=serviceNames",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVpcEndpointServices",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=serviceNames",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVpcEndpoints",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVpcEndpointConnections",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeTransitGateways",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeTransitGateways;targetValues=accountId:accountId_,regionCode:regionCode_,transitGatewayId:transitGatewayId;namespace=AWS/TransitGateway;metricName=BytesIn;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TransitGateway:transitGatewayId;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeTransitGateways;targetValues=accountId:accountId_,regionCode:regionCode_,transitGatewayId:transitGatewayId;namespace=AWS/TransitGateway;metricName=BytesOut;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TransitGateway:transitGatewayId;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeNatGateways",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=natGatewayAddresses,tags",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeNatGateways;targetValues=accountId:accountId_,regionCode:regionCode_,natGatewayId:natGatewayId;namespace=AWS/NATGateway;metricName=BytesOutToDestination;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=NatGatewayId:natGatewayId;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeNatGateways;targetValues=accountId:accountId_,regionCode:regionCode_,natGatewayId:natGatewayId;namespace=AWS/NATGateway;metricName=BytesInFromDestination;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=NatGatewayId:natGatewayId;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] ELB Status" : {
    "meta" : {
      "reportName": "ELB Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"elb.setTargetValues",
          "args":"",
          "inputs":"accountId_=000000000000;regionCode_=us-east-1",
          "conditions":"",
          "limit":"",
          "pt":""
          },
        { "platform":"k2",
          "apiName":"elb.describeLoadBalancers", 
          "args":{},
          "inputs":"sourceApiName=elb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;resourceName=serviceName_,regionCode_,accountId_,loadBalancerName",
          "pt":"8x8"
          },
        {"platform":"moduAWS",
         "apiName":"elb.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId_:accountId_,regionCode_:regionCode_;combineWith=elb.describeLoadBalancers;asValues=loadBalancerNames:loadBalancerName;chunkSize=20",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        { "platform":"k2",
          "apiName":"elb.describeTags", 
          "args":"{\"loadBalancerNames\":${__loadBalancerNames__}}",
          "inputs":"sourceApiName=elb.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerNames:loadBalancerNames_list;resourceName=serviceName_,regionCode_,accountId_,loadBalancerName",
          "pt":"8x8"
          }
        ]
    }, # end: Template Items#
      
  # begin: Template Items
  "[unittest] ELB Status - getRegions" : {
    "meta" : {
      "reportName": "ELB Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"elb.getRegions",
          "args":"",
          "inputs":"serviceName=ELB",
          "conditions":"",
          "limit":"",
          "pt":""
          },
        {
          "platform":"k2",
          "apiName":"elb.describeLoadBalancers",
          "args":"",
          "inputs":"sourceApiName=elb.getRegions;targetValues=accountId:accountId,regionCode:regionCode;primaryKeys=policies",
          "conditions":"",
          "limit":"",
          "pt":""
          },
        {
          "platform":"k2",
          "apiName":"cloudwatch.getMetricStatistics",
          "args":"",
          "startTime":"59.9 Days ago",
          "endTime":"now",
          "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=RequestCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:loadBalancerName;mode=Summary",
          "conditions":"",
          "limit":"",
          "pt":""
          },
        {
          "platform":"k2",
          "apiName":"alb.describeLoadBalancers",
          "args":"",
          "inputs":"sourceApiName=elb.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
          "conditions":"",
          "limit":"",
          "pt":""
         },
        {
          "platform":"k2",
          "apiName":"cloudwatch.getMetricStatistics",
          "args":"",
          "startTime":"59.9 Days ago",
          "endTime":"now",
          "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerName:loadBalancerName;namespace=AWS/ApplicationELB;metricName=RequestCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:loadBalancerName;mode=Summary",
          "conditions":"",
          "limit":"",
          "pt":""
          }        
        ]
    }, # end: Template Items#
      
  # begin: Template Items
  "[unittest] ELB Target Group Status*" : {
    "meta" : {
      "reportName": "get Target Group Host Count",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=568383657092",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerName:loadBalancerName,targetGroupName:targetGroupName;namespace=AWS/NetworkELB;metricName=HealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:targetGroupName,LoadBalancer:loadBalancerName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTags",
         "args":"\"resourceArns\":[\"${__loadBalancerArn__}\"]}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"elb.filterResults",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:LoadBalancer,TargetGroup:TargetGroup,granularity(sec):granularity(sec),startTime:startTime,endTime:endTime,dataPoints:dataPoints,average:average,minimum:minimum,maximum:maximum,unit:unit,InUse:InUse;addAccountDetails=yes",
         "conditions":"maximum>=5",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] ApplicationELB Metrics  - consumer experience" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics - consumer experience",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_Target_5XX_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=ConsumedLCUs;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] ApplicationELB HealthCheck Metrics - consumer experience - 24 hours ago" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"maxOfMax > 1",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetConnectionErrorCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=ConsumedLCUs;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=maximum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] ApplicationELB HealthCheck Metrics - consumer experience - 24 hours ago - getRegions" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.getRegions",
         "args":"",
         "inputs":"serviceName=ApplicationELB",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"maxOfMax > 1",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetConnectionErrorCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] ApplicationELB HealthCheck Metrics - consumer experience - 16 days - 1min - getRegions" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"16 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.getRegions",
         "args":"",
         "inputs":"serviceName=ApplicationELB",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetConnectionErrorCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[Launch Events] ApplicationELB HealthCheck Metrics - consumer experience - 15 days ago" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"maxOfMax > 1",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetConnectionErrorCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[Launch Events] ApplicationELB HealthCheck Metrics - all prod - 15 days ago" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=675187343264,694932753931,548566750698,856323016481,598256275489,191814221326,381935921053,231738951007,230766151005,683339605493,671997087067,554697901422,613703198018,433719404598,355070953457,353556761890,556458627866,079911930160,436726303481,059499913308,165526785268,057220673095,016152999979,742467298099,370680818641,437667293086,415304672366,617394139813,607899199937,845887853628,291829135576,649527443076,423098377865,934777727034,257947106429,483263294630,391195385792,733796157310,878163342443,647400204775,341908542378,140492103125,929032588586,573738471095,086889020015,747260357079,108775199478,536555827358,477944742332,566762129515,414771670080,915313319302,591142930755,006379771997,853517228249,354852822151,765335004154,034893609206,496767662009,984441521015,370708114365,420937882366,851202709352,941209011676,437815327823,349083890981,055342878591,820289444515,305447951102,854480901636,887631223894,892496292990,777497332714,242797321510,128712185541,477764622205,919740896133,548706247775,757262564613,927714088631,059289126277,077100256360,125149255836,140021409435,893225414602,783291344678,619115286229,030174363477,118119029295,642519545437,123842044300,643257441225,726896467349,236655354521,668285129948,736653156559,775892074791,229714392941,548330541175,248957249702,374322998561,609521493282,164996877390,534832385698,561280031863,939937965389,504269423921,127345046654,168254019775,378376160408,583269311046,728227005623,076275742054,166024938531,832845695685,621386740946,563177518345,082070760758,097243094682,402085650492,035450287168,360820454324,619752470675,733103895081,926239361991,640118002321,216333391471,626052043195,569088908774,750355576552,880669761768,517928488811,750202118857,503675182586,015350302030,637904411950,687662248257,107876486217,434521655550,000000000000,667734572507,924561449313,560749724582,157759633741,541406732840,967534497917,379767101427,928949352672,831312320476,501224640861,576429187634,574776663885,426551879247,848927227190,144770792259,944807178991,692398283538,962610448740,909209288517,935986877796,073329621521,259697563740,142287549164,754520222449,118866852582,246346416592,845346430498,063891294803,686440132868,133211774478,403212439324,639093664512,525974220579,552667846668,344846362216,325524018083,712667561039,118746129420,445105812741,714792870839,063043818802,612037695117,577936112098,530615860851,491283761170,042070407208,348387353606,397029661066,565292077821,531714700922,243375556525,540968912262,142023473066,063883474696,033284175399,382152805637,742617195046,680159468246,520084927359,999904766088,898198856680,081380948729,876969159949,334696401286,867183384685,461254032735,243923977404,612522568317,046193071273,660134747877,597314698617,548673387398,467128999827,764874649068,083120681051,482038169294,661067436059,373428735865,992480074694,770278825412,994493528555,253908670668,359714541012,237901581861,733569249960,518689392762,104636225068,135657235999,359726500881,146047007952,045748577629,152416170051,287064739817,451746848004,982155066914,934442535328,257844434863,324762497681,925132557169,949308154263,062984079109,551442567918,648347805205,170025367501,292322675470,114361920721,731454348287,149540730537,275853731244,758069237013,375138344757,422291751558,084376588688,423122531253,802377670286,539785324859,568225445654,129623073998,051465757517,938166811786,924417653661,753442902086,095197189537,180543039451,623226990203,531057653290,130715786028,866774220332,715957030150,774767054473,100653509078,538714038616,673643514546,502954657688,420368275242,381978352327,919484679069,228770805677,122280356913,397864428583,286028826102,717147554153,844906824187,622023719607,153108717324,830334984184,875870961176,799877353134,463463342168,159676249862,460493258900,190111491038,479544771523,567893769155,521759315637,875445469402,284185843393,228369200000,927160670506,433174745374,975449850829,123102147581,602923205559,663638510227,996207755572,137235379828,433265895211,590004764688,843507924409,558110724290,000000000000,100098063638,298876281336,024759385443,039808956707,255479074508,002777230731,423502194085,443154216562,896522994279,037022705054,876684145988,292667491772,447452557152,587150138645,697557150666,841591709431,722987513393,443938910386,814552791690,404692024941,412661042033,378173282036,197810631838,565475689595,672573537448,837111340404,145837005752,232467433306,289474188929,559548544732,467367579176,018843893501,451123730037,213885799539,205857894628,245012523099,267489780609,179942311650,698729420478,601579179579,637138304026,512363189157,608898705804,680814905614,877049657432,738471402357,931829841365,779498280780,503530546980,736912206701,674872411453,677780884059,938528360018,174241849982,025891688826,998132092021,749991730207,028997125135,870131621513,216142192209,133614276542,506122439099,785095751600,180159804786,567546912947,944840461140,075174616825,235372617315,000000000000,978099172172,538146750428,463137498994,702721481084,339335539743,520095548653,818979557426,993736609249,438956650301,626222367221,440676120024,185458415094,102671227235,529363209591,493244245697,674653831326,423844257650,087660466352,359804509760,910553138255,656745116619,369551651993,123393010596,910523329506,025461062541,284642499453,719813308691,489957898670,068450681418,173298430612,052852011374,135747138848,725215824324,799394622761,276561676684,142162276931,856409471037,687099058668,605067275927,196339533918,048885382488,244546665232,889466886213,059446332267,786995526688,062649814741,468773836582,922923860624,633172313049,779347231867,366792430539,998734454818,567944309494,474247328737,562947401788,499819885500,000000000000,333305023352,460063236433,836087980978,070662189277,126190501570,474498224381,070948067691,870439269062,356623176356,966657230740,782828323207,695370420698,534999213837,531572832565,309632601280,187866540173,197004204405,550202007170,199388946801,667635270669,586899911946,037537868683,591575983514,313159353534,463656602360,335385301882,877080213714,354360073182,952729215972,439851440557,214225321783,204079741340,680427445313,857069700355,688026838185,545666512835,640598578606,447436043444,865422087295,714823208268,806224071948,798391262600,645973590831,357126491496,623244905753,164376313862,213986886835,264637097463,463820153159,156652473040,641225932385,380525367777,915105194267,236785139186,522452501562,649289500325,772261832009,373949309420,229783550070,471655526001,673873592633,115039710420,869535244626,237583541556,650887814303,780249556402,115021171547,852964174427,158163280210,184555362817,348128672012,387122980739,487970328024,063794881583,243676664977,375821324318,418630054634,294855260814,054702201138,788889859008,794651967606,178928422231,847475412370,867244746267,923732300371,317566832020,129816847298,250556970131,391433907867,088251879437,832844619813,067440223434,183754648597,855110530208,632285889341,419000340690,737082280064,331078587791,118660000176,225945064454,779891692089,765359557030,178330703403,370180977388,596983670911,142709126060,618295799011,222933456218,365632193755,763268361697,789390408286,062711226102,149939807652,203367902250,235240887867,269334419746,251012265860,774475901473,823318890686,586884718913,520797679225,998982526853,404359343680,449883526716,131907944798,948349142778,137965736774,026297181211,781318804736,521851481881,179374150550,844086157255,785146769030,875644078874,022979034283,147277567226,687378323699,712485829774,446802202443,378472802568,018678282827,372879557643,945795829572,489582254329,579163533794,579563577636,827773065320,227860895736,708443330255,274868111244,574486685567,307870788387,404443498944,335229360565,663232060412,571555949018,314760337835,244378616991,883629411111,484322932171,474491873857,342249735114,573788863304,646359468015,675599259848,834712125638,768904925612,791772033787,448676076476,097142443852,599869035376,412918434037,154469619113,892201690593,802795789469,546391016021,467664322522,241667773673,325071552919,808180657344,883072818378,094776610618,743039260076,092479283505,326511031916,219618970644,411873080737,931043691043,296012323783,300814606917,303822575542,420814345532,899188398691,093973853253,960639112596,723205702811,436383514842,312946089387,600310625339,306109670684,381260490747,372004125320,764482557331,782645973791,289143163514,351951630132,166391985076,068011249945,163220562780,393402838373,063829613942,314642499074,570878255064,243964310975,436995157701,963690474723,328528749406,069721401477,518368631528,494342409922,010014027154,483440131694,011812592349,456163172512,172814097302,180754852103,109992134225,135706656868,913142095474,575275655865,276322113591,244110146703,245080968959,631951072441",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == application",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=HTTPCode_ELB_5XX_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetResponseTime;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"maxOfMax > 1",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/ApplicationELB;metricName=TargetConnectionErrorCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/ApplicationELB;metricName=UnHealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] NetworkELB HealthCheck Metrics - consumer experience - 24 hours ago" : {
    "meta" : {
      "reportName": "get NetworkELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == network",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_TCP;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_TLS;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_UDP;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_Target_Reset_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_ELB_Reset_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/NetworkELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[Launch Events] NetworkELB HealthCheck Metrics - consumer experience - 24 hours ago - getRegions" : {
    "meta" : {
      "reportName": "get NetworkELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.getRegions",
         "args":"",
         "inputs":"serviceName=NetworkELB",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
         "conditions":"type == network",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_TCP;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_TLS;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=ActiveFlowCount_UDP;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_Target_Reset_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_ELB_Reset_Count;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/NetworkELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[Launch Events] NetworkELB HealthCheck Metrics - consumer experience - 15 days ago" : {
    "meta" : {
      "reportName": "get NetworkELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == network",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_Target_Reset_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_ELB_Reset_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/NetworkELB;metricName=UnHealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[Launch Events] NetworkELB HealthCheck Metrics - all prod - 15 days ago" : {
    "meta" : {
      "reportName": "get NetworkELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=675187343264,694932753931,548566750698,856323016481,598256275489,191814221326,381935921053,231738951007,230766151005,683339605493,671997087067,554697901422,613703198018,433719404598,355070953457,353556761890,556458627866,079911930160,436726303481,059499913308,165526785268,057220673095,016152999979,742467298099,370680818641,437667293086,415304672366,617394139813,607899199937,845887853628,291829135576,649527443076,423098377865,934777727034,257947106429,483263294630,391195385792,733796157310,878163342443,647400204775,341908542378,140492103125,929032588586,573738471095,086889020015,747260357079,108775199478,536555827358,477944742332,566762129515,414771670080,915313319302,591142930755,006379771997,853517228249,354852822151,765335004154,034893609206,496767662009,984441521015,370708114365,420937882366,851202709352,941209011676,437815327823,349083890981,055342878591,820289444515,305447951102,854480901636,887631223894,892496292990,777497332714,242797321510,128712185541,477764622205,919740896133,548706247775,757262564613,927714088631,059289126277,077100256360,125149255836,140021409435,893225414602,783291344678,619115286229,030174363477,118119029295,642519545437,123842044300,643257441225,726896467349,236655354521,668285129948,736653156559,775892074791,229714392941,548330541175,248957249702,374322998561,609521493282,164996877390,534832385698,561280031863,939937965389,504269423921,127345046654,168254019775,378376160408,583269311046,728227005623,076275742054,166024938531,832845695685,621386740946,563177518345,082070760758,097243094682,402085650492,035450287168,360820454324,619752470675,733103895081,926239361991,640118002321,216333391471,626052043195,569088908774,750355576552,880669761768,517928488811,750202118857,503675182586,015350302030,637904411950,687662248257,107876486217,434521655550,000000000000,667734572507,924561449313,560749724582,157759633741,541406732840,967534497917,379767101427,928949352672,831312320476,501224640861,576429187634,574776663885,426551879247,848927227190,144770792259,944807178991,692398283538,962610448740,909209288517,935986877796,073329621521,259697563740,142287549164,754520222449,118866852582,246346416592,845346430498,063891294803,686440132868,133211774478,403212439324,639093664512,525974220579,552667846668,344846362216,325524018083,712667561039,118746129420,445105812741,714792870839,063043818802,612037695117,577936112098,530615860851,491283761170,042070407208,348387353606,397029661066,565292077821,531714700922,243375556525,540968912262,142023473066,063883474696,033284175399,382152805637,742617195046,680159468246,520084927359,999904766088,898198856680,081380948729,876969159949,334696401286,867183384685,461254032735,243923977404,612522568317,046193071273,660134747877,597314698617,548673387398,467128999827,764874649068,083120681051,482038169294,661067436059,373428735865,992480074694,770278825412,994493528555,253908670668,359714541012,237901581861,733569249960,518689392762,104636225068,135657235999,359726500881,146047007952,045748577629,152416170051,287064739817,451746848004,982155066914,934442535328,257844434863,324762497681,925132557169,949308154263,062984079109,551442567918,648347805205,170025367501,292322675470,114361920721,731454348287,149540730537,275853731244,758069237013,375138344757,422291751558,084376588688,423122531253,802377670286,539785324859,568225445654,129623073998,051465757517,938166811786,924417653661,753442902086,095197189537,180543039451,623226990203,531057653290,130715786028,866774220332,715957030150,774767054473,100653509078,538714038616,673643514546,502954657688,420368275242,381978352327,919484679069,228770805677,122280356913,397864428583,286028826102,717147554153,844906824187,622023719607,153108717324,830334984184,875870961176,799877353134,463463342168,159676249862,460493258900,190111491038,479544771523,567893769155,521759315637,875445469402,284185843393,228369200000,927160670506,433174745374,975449850829,123102147581,602923205559,663638510227,996207755572,137235379828,433265895211,590004764688,843507924409,558110724290,000000000000,100098063638,298876281336,024759385443,039808956707,255479074508,002777230731,423502194085,443154216562,896522994279,037022705054,876684145988,292667491772,447452557152,587150138645,697557150666,841591709431,722987513393,443938910386,814552791690,404692024941,412661042033,378173282036,197810631838,565475689595,672573537448,837111340404,145837005752,232467433306,289474188929,559548544732,467367579176,018843893501,451123730037,213885799539,205857894628,245012523099,267489780609,179942311650,698729420478,601579179579,637138304026,512363189157,608898705804,680814905614,877049657432,738471402357,931829841365,779498280780,503530546980,736912206701,674872411453,677780884059,938528360018,174241849982,025891688826,998132092021,749991730207,028997125135,870131621513,216142192209,133614276542,506122439099,785095751600,180159804786,567546912947,944840461140,075174616825,235372617315,000000000000,978099172172,538146750428,463137498994,702721481084,339335539743,520095548653,818979557426,993736609249,438956650301,626222367221,440676120024,185458415094,102671227235,529363209591,493244245697,674653831326,423844257650,087660466352,359804509760,910553138255,656745116619,369551651993,123393010596,910523329506,025461062541,284642499453,719813308691,489957898670,068450681418,173298430612,052852011374,135747138848,725215824324,799394622761,276561676684,142162276931,856409471037,687099058668,605067275927,196339533918,048885382488,244546665232,889466886213,059446332267,786995526688,062649814741,468773836582,922923860624,633172313049,779347231867,366792430539,998734454818,567944309494,474247328737,562947401788,499819885500,000000000000,333305023352,460063236433,836087980978,070662189277,126190501570,474498224381,070948067691,870439269062,356623176356,966657230740,782828323207,695370420698,534999213837,531572832565,309632601280,187866540173,197004204405,550202007170,199388946801,667635270669,586899911946,037537868683,591575983514,313159353534,463656602360,335385301882,877080213714,354360073182,952729215972,439851440557,214225321783,204079741340,680427445313,857069700355,688026838185,545666512835,640598578606,447436043444,865422087295,714823208268,806224071948,798391262600,645973590831,357126491496,623244905753,164376313862,213986886835,264637097463,463820153159,156652473040,641225932385,380525367777,915105194267,236785139186,522452501562,649289500325,772261832009,373949309420,229783550070,471655526001,673873592633,115039710420,869535244626,237583541556,650887814303,780249556402,115021171547,852964174427,158163280210,184555362817,348128672012,387122980739,487970328024,063794881583,243676664977,375821324318,418630054634,294855260814,054702201138,788889859008,794651967606,178928422231,847475412370,867244746267,923732300371,317566832020,129816847298,250556970131,391433907867,088251879437,832844619813,067440223434,183754648597,855110530208,632285889341,419000340690,737082280064,331078587791,118660000176,225945064454,779891692089,765359557030,178330703403,370180977388,596983670911,142709126060,618295799011,222933456218,365632193755,763268361697,789390408286,062711226102,149939807652,203367902250,235240887867,269334419746,251012265860,774475901473,823318890686,586884718913,520797679225,998982526853,404359343680,449883526716,131907944798,948349142778,137965736774,026297181211,781318804736,521851481881,179374150550,844086157255,785146769030,875644078874,022979034283,147277567226,687378323699,712485829774,446802202443,378472802568,018678282827,372879557643,945795829572,489582254329,579163533794,579563577636,827773065320,227860895736,708443330255,274868111244,574486685567,307870788387,404443498944,335229360565,663232060412,571555949018,314760337835,244378616991,883629411111,484322932171,474491873857,342249735114,573788863304,646359468015,675599259848,834712125638,768904925612,791772033787,448676076476,097142443852,599869035376,412918434037,154469619113,892201690593,802795789469,546391016021,467664322522,241667773673,325071552919,808180657344,883072818378,094776610618,743039260076,092479283505,326511031916,219618970644,411873080737,931043691043,296012323783,300814606917,303822575542,420814345532,899188398691,093973853253,960639112596,723205702811,436383514842,312946089387,600310625339,306109670684,381260490747,372004125320,764482557331,782645973791,289143163514,351951630132,166391985076,068011249945,163220562780,393402838373,063829613942,314642499074,570878255064,243964310975,436995157701,963690474723,328528749406,069721401477,518368631528,494342409922,010014027154,483440131694,011812592349,456163172512,172814097302,180754852103,109992134225,135706656868,913142095474,575275655865,276322113591,244110146703,245080968959,631951072441",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"type == network",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_Target_Reset_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:arnV4;namespace=AWS/NetworkELB;metricName=TCP_ELB_Reset_Count;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancer:LoadBalancer;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"nlb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:loadBalancer,TargetGroup:arnV1;namespace=AWS/NetworkELB;metricName=UnHealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:TargetGroup,LoadBalancer:LoadBalancer;mode=Summary;modeStatic=average",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
         
  # begin: Template Items
  "[Launch Events] Classic ELB HealthCheck Metrics - consumer experience - 24 hours ago" : {
    "meta" : {
      "reportName": "get Classic ELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"elb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"elb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=elb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=RequestCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=SpilloverCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=HTTPCode_ELB_5XX;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=BackendConnectionErrors;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=UnHealthyHostCount;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[Launch Events] Classic ELB HealthCheck Metrics - consumer experience - 15 days ago" : {
    "meta" : {
      "reportName": "get Classic ELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"15 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"elb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"elb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=elb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=SpilloverCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=HTTPCode_ELB_5XX;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=BackendConnectionErrors;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"elb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=elb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancerName:loadBalancerName;namespace=AWS/ELB;metricName=UnHealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=LoadBalancerName:LoadBalancerName;mode=Summary;modeStatic=sum",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"4x8"
         }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[unittest] ApplicationELB Metrics - listMetrics" : {
    "meta" : {
      "reportName": "get ApplicationELB Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"alb.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.listMetrics",
         "args":"{\"namespace\":\"AWS/ApplicationELB\",\"metricName\":\"RequestCount\"}",
         "inputs":"sourceApiName=alb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x8"
         },
        {"platform":"k2",
         "apiName":"alb.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"2x8"
         }
      ]
    }, # end: Template Items#

  # begin: Template Items
  "[unittest] EC2 Instance Status - 000000000000 - asg" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances",
         "conditions":"",
         "limit":"",
         "pt":"1x8"
         },
        {
          "platform":"k2",
          "apiName":"ec2.describeInstances",
          "args":"{\"instanceIds\":[\"${__instanceId__}\"]}",
          "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;primaryKeys=instances,state;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x8"
          },#{"instanceIds":["i-0df192389801a191b"]},"apiName":"ec2.describeInstances","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 Instance Status - 000000000000 - asg - Unhealthy" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances",
         "conditions":"",
         "limit":"",
         "pt":"1x8"
         },
        {
          "platform":"k2",
          "apiName":"ec2.describeInstances",
          "args":"{\"instanceIds\":[\"${__instanceId__}\"]}",
          "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;primaryKeys=instances,state;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x8"
          },#{"instanceIds":["i-0df192389801a191b"]},"apiName":"ec2.describeInstances","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 Instance Status - 000000000000" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"ec2.describeInstances",
          "args":"",
          "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;primaryKeys=instances,state,tags;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x8"
          },#{"instanceIds":["i-0df192389801a191b"]},"apiName":"ec2.describeInstances","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"10",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 Instance Status - getRegions" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"serviceName=EC2",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId,regionCode:regionCode;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 Instance Status v2" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=eu-west-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionName;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EC2 Instance Status v3 - 000000000000" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state,tags",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic:maximum",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         },
      ]
    }, # end: Template Items#
  
          
          
  # begin: Template Items
  "[unittest] EC2 Instance Status v3" : {
    "meta" : {
      "reportName": "get EC2 Instance Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=015162136117,190225106431,159586396623,225836362124,213741646905,268889722472,344691037878,458036547247,580952770835,264534990656,317108535030,255060517824,427896624473,462887716314,306701351329,589352793208,971771347730,513396412904,529339670897,601565657821,022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-west-2;nocsv;accountId_=173245911106",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeReservedInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId,state:name",
         "conditions":"state==running",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
           
  # begin: Template Items
  "[unittest] EC2 Instance Status v4" : {
    "meta" : {
      "reportName": "EC2 Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=450881533027;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionName;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"10",
         "pt":"32x8"
         }
        ]
    }, # end: Template Items#  
  
  # begin: Template Items
  "[unittest] EBS Volume Status" : {
    "meta" : {
      "reportName": "get EBS Volume Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ebs.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVolumes",
         "args":"",
         "inputs":"sourceApiName=ebs.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeVolumes;targetValues=accountId:accountId_,regionCode:regionCode_,volumeId:volumeId;namespace=AWS/EBS;metricName=VolumeWriteBytes;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=VolumeId:volumeId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsUtilization",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] EBS Snapshot Status" : {
    "meta" : {
      "reportName": "get EBS Snapshot Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"3 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ebs.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1,us-west-2,eu-west-1;nocsv;accountId_=239575778557,022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeSnapshots",
         "args":"{\"ownerIds\":[\"${__accountId__}\"]}",
         "inputs":"sourceApiName=ebs.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"16x2"
         },
        #{"platform":"moduAWS",
        # "apiName":"dw.discoverDwEbsSnapshots",
        # "args":"",
        # "inputs":"sourceApiName=ec2.describeSnapshots;targetValues=accountId:accountId_;accountIdChunkCount=-1",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsSnapshots",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] Lambda Resource Status" : {
    "meta" : {
      "reportName": "get Lambda Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"lambda.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listFunctions",
         "args":"",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"runtime==python2.7",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getFunction",
         "args":"{\"functionName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=lambda.listFunctions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:functionName;primaryKeys=configuration,tags",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getFunctionConcurrency",
         "args":"{\"functionName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=lambda.listFunctions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:functionName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getFunctionEventInvokeConfig",
         "args":"{\"functionName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=lambda.listFunctions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:functionName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getProvisionedConcurrencyConfig",
         "args":"{\"functionName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=lambda.listFunctions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:functionName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listLayers",
         "args":"",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=latestMatchingVersion",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listEventSourceMappings",
         "args":"",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getAccountSettings",
         "args":"",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] Lambda ConcurrentExecutions Status" : {
    "meta" : {
      "reportName": "get Lambda ConcurrentExecutions Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"lambda.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listFunctions",
         "args":"",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"runtime==python2.7",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listMetrics",
         "args":"{\"namespace\":\"AWS/Lambda\",\"metricName\":\"ConcurrentExecutions\"}",
         "inputs":"sourceApiName=lambda.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"lambda.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=lambda.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         }
      ]
    }, # end: Template Items#

  # begin: Template Items
  "[unittest] ElastiCache Status - 000000000000" : {
    "meta" : {
      "reportName": "get ElastiCache Status ",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"elasticache.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"elasticache.describeCacheClusters",
         "args":"{\"showCacheNodeInfo\":true}",
         "inputs":"sourceApiName=elasticache.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=cacheNodes,endpoint",
         "conditions":"",
         "limit":"",
         "pt":"1x8"
         },
        {"platform":"k2",
         "apiName":"#ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state,tags",
         "conditions":"",
         "limit":"",
         "pt":"1x8"
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;modeStatic:maximum",
         "conditions":"",
         "limit":"10",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  
        
  # begin: Template Items
  "[unittest] Redshift Resource Status" : {
    "meta" : {
      "reportName": "get Redshift Resources",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"today",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"5",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=PercentageDiskSpaceUsed;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items
  
  # begin: Template Items
  "[unittest] RDS Resource Status - getRegions" : {
    "meta" : {
      "reportName": "get RDS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"today",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"serviceName=RDS",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBInstanceArn;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"rds.describeDBClusters",
          "args":"",
          "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId,regionCode:regionCode",
          "conditions":"",
          "limit":"",
          "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBClusterArn;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeResources",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items  # begin: Template Items
  
  # begin: Template Items
  "[unittest] RDS Resource Status - setTargetValues" : {
    "meta" : {
      "reportName": "get RDS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"today",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"rds.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=021824079065,028009399290,035580655376,041003132611,044096650143,052684788981,078499015708,099356522462,101661720690,103641018243,109434410235,110145862301,116448481841,134001856083,166440397761,181489996397,209772739983,210157577452,213413494671,214790005682,224670914335,232388941425,257325184575,260637879381,265263573940,273104076548,273114391775,274186386842,279767409586,282643525406,286564069533,292012218142",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBInstanceArn;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRDSInstance",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items  # begin: Template Items
  
  
  # begin: Template Items
  "[unittest] QuickSight Metrics - listMetrics" : {
    "meta" : {
      "reportName": "get QuickSight Metrics",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=QuickSight",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"quicksight.listMetrics",
         "args":"{\"namespace\":\"AWS/QuickSight/Dashboard Metrics\"}",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
         "conditions":"regionCode == us-east-1",
         "limit":"",
         "pt":"2x8"
         },
        {"platform":"k2",
         "apiName":"quicksight.listMetrics",
         "args":"{\"namespace\":\"AWS/QuickSight/Ingestion Metrics\",\"metricName\":\"IngestionRowCount\"}",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"2x8"
         },
        {"platform":"k2",
         "apiName":"quicksight.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=quicksight.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=60;mode=Summary;moduStatic=sum",
         "conditions":"",
         "limit":"",
         "pt":"2x8"
         }
      ]
    }, # end: Template Items#

  "[Launch Events] DynamoDB Resource Status - consumer experience - 24 hours ago" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status - consumer experience - 24 hours ago",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  

  "[Launch Events] DynamoDB Resource Status - consumer experience - 24 hours ago - getRegions" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status - consumer experience - 24 hours ago",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=DynamoDB",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=SystemErrors;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  

  "[Launch Events] DynamoDB Resource Status - consumer experience - 15 days ago" : {
    "meta" : {
      "reportName": "DynamoDB Resource Status - consumer experience - 15 days ago",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"14 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=529363209591,742617195046,876969159949,000000000000,482038169294,550202007170,245012523099,934442535328,647400204775,275853731244,697557150666",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  
  "[Launch Events] DynamoDB Resource Status - all prod - 15 days" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"14 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=675187343264,694932753931,548566750698,856323016481,598256275489,191814221326,381935921053,231738951007,230766151005,683339605493,671997087067,554697901422,613703198018,433719404598,355070953457,353556761890,556458627866,079911930160,436726303481,059499913308,165526785268,057220673095,016152999979,742467298099,370680818641,437667293086,415304672366,617394139813,607899199937,845887853628,291829135576,649527443076,423098377865,934777727034,257947106429,483263294630,391195385792,733796157310,878163342443,647400204775,341908542378,140492103125,929032588586,573738471095,086889020015,747260357079,108775199478,536555827358,477944742332,566762129515,414771670080,915313319302,591142930755,006379771997,853517228249,354852822151,765335004154,034893609206,496767662009,984441521015,370708114365,420937882366,851202709352,941209011676,437815327823,349083890981,055342878591,820289444515,305447951102,854480901636,887631223894,892496292990,777497332714,242797321510,128712185541,477764622205,919740896133,548706247775,757262564613,927714088631,059289126277,077100256360,125149255836,140021409435,893225414602,783291344678,619115286229,030174363477,118119029295,642519545437,123842044300,643257441225,726896467349,236655354521,668285129948,736653156559,775892074791,229714392941,548330541175,248957249702,374322998561,609521493282,164996877390,534832385698,561280031863,939937965389,504269423921,127345046654,168254019775,378376160408,583269311046,728227005623,076275742054,166024938531,832845695685,621386740946,563177518345,082070760758,097243094682,402085650492,035450287168,360820454324,619752470675,733103895081,926239361991,640118002321,216333391471,626052043195,569088908774,750355576552,880669761768,517928488811,750202118857,503675182586,015350302030,637904411950,687662248257,107876486217,434521655550,000000000000,667734572507,924561449313,560749724582,157759633741,541406732840,967534497917,379767101427,928949352672,831312320476,501224640861,576429187634,574776663885,426551879247,848927227190,144770792259,944807178991,692398283538,962610448740,909209288517,935986877796,073329621521,259697563740,142287549164,754520222449,118866852582,246346416592,845346430498,063891294803,686440132868,133211774478,403212439324,639093664512,525974220579,552667846668,344846362216,325524018083,712667561039,118746129420,445105812741,714792870839,063043818802,612037695117,577936112098,530615860851,491283761170,042070407208,348387353606,397029661066,565292077821,531714700922,243375556525,540968912262,142023473066,063883474696,033284175399,382152805637,742617195046,680159468246,520084927359,999904766088,898198856680,081380948729,876969159949,334696401286,867183384685,461254032735,243923977404,612522568317,046193071273,660134747877,597314698617,548673387398,467128999827,764874649068,083120681051,482038169294,661067436059,373428735865,992480074694,770278825412,994493528555,253908670668,359714541012,237901581861,733569249960,518689392762,104636225068,135657235999,359726500881,146047007952,045748577629,152416170051,287064739817,451746848004,982155066914,934442535328,257844434863,324762497681,925132557169,949308154263,062984079109,551442567918,648347805205,170025367501,292322675470,114361920721,731454348287,149540730537,275853731244,758069237013,375138344757,422291751558,084376588688,423122531253,802377670286,539785324859,568225445654,129623073998,051465757517,938166811786,924417653661,753442902086,095197189537,180543039451,623226990203,531057653290,130715786028,866774220332,715957030150,774767054473,100653509078,538714038616,673643514546,502954657688,420368275242,381978352327,919484679069,228770805677,122280356913,397864428583,286028826102,717147554153,844906824187,622023719607,153108717324,830334984184,875870961176,799877353134,463463342168,159676249862,460493258900,190111491038,479544771523,567893769155,521759315637,875445469402,284185843393,228369200000,927160670506,433174745374,975449850829,123102147581,602923205559,663638510227,996207755572,137235379828,433265895211,590004764688,843507924409,558110724290,000000000000,100098063638,298876281336,024759385443,039808956707,255479074508,002777230731,423502194085,443154216562,896522994279,037022705054,876684145988,292667491772,447452557152,587150138645,697557150666,841591709431,722987513393,443938910386,814552791690,404692024941,412661042033,378173282036,197810631838,565475689595,672573537448,837111340404,145837005752,232467433306,289474188929,559548544732,467367579176,018843893501,451123730037,213885799539,205857894628,245012523099,267489780609,179942311650,698729420478,601579179579,637138304026,512363189157,608898705804,680814905614,877049657432,738471402357,931829841365,779498280780,503530546980,736912206701,674872411453,677780884059,938528360018,174241849982,025891688826,998132092021,749991730207,028997125135,870131621513,216142192209,133614276542,506122439099,785095751600,180159804786,567546912947,944840461140,075174616825,235372617315,000000000000,978099172172,538146750428,463137498994,702721481084,339335539743,520095548653,818979557426,993736609249,438956650301,626222367221,440676120024,185458415094,102671227235,529363209591,493244245697,674653831326,423844257650,087660466352,359804509760,910553138255,656745116619,369551651993,123393010596,910523329506,025461062541,284642499453,719813308691,489957898670,068450681418,173298430612,052852011374,135747138848,725215824324,799394622761,276561676684,142162276931,856409471037,687099058668,605067275927,196339533918,048885382488,244546665232,889466886213,059446332267,786995526688,062649814741,468773836582,922923860624,633172313049,779347231867,366792430539,998734454818,567944309494,474247328737,562947401788,499819885500,000000000000,333305023352,460063236433,836087980978,070662189277,126190501570,474498224381,070948067691,870439269062,356623176356,966657230740,782828323207,695370420698,534999213837,531572832565,309632601280,187866540173,197004204405,550202007170,199388946801,667635270669,586899911946,037537868683,591575983514,313159353534,463656602360,335385301882,877080213714,354360073182,952729215972,439851440557,214225321783,204079741340,680427445313,857069700355,688026838185,545666512835,640598578606,447436043444,865422087295,714823208268,806224071948,798391262600,645973590831,357126491496,623244905753,164376313862,213986886835,264637097463,463820153159,156652473040,641225932385,380525367777,915105194267,236785139186,522452501562,649289500325,772261832009,373949309420,229783550070,471655526001,673873592633,115039710420,869535244626,237583541556,650887814303,780249556402,115021171547,852964174427,158163280210,184555362817,348128672012,387122980739,487970328024,063794881583,243676664977,375821324318,418630054634,294855260814,054702201138,788889859008,794651967606,178928422231,847475412370,867244746267,923732300371,317566832020,129816847298,250556970131,391433907867,088251879437,832844619813,067440223434,183754648597,855110530208,632285889341,419000340690,737082280064,331078587791,118660000176,225945064454,779891692089,765359557030,178330703403,370180977388,596983670911,142709126060,618295799011,222933456218,365632193755,763268361697,789390408286,062711226102,149939807652,203367902250,235240887867,269334419746,251012265860,774475901473,823318890686,586884718913,520797679225,998982526853,404359343680,449883526716,131907944798,948349142778,137965736774,026297181211,781318804736,521851481881,179374150550,844086157255,785146769030,875644078874,022979034283,147277567226,687378323699,712485829774,446802202443,378472802568,018678282827,372879557643,945795829572,489582254329,579163533794,579563577636,827773065320,227860895736,708443330255,274868111244,574486685567,307870788387,404443498944,335229360565,663232060412,571555949018,314760337835,244378616991,883629411111,484322932171,474491873857,342249735114,573788863304,646359468015,675599259848,834712125638,768904925612,791772033787,448676076476,097142443852,599869035376,412918434037,154469619113,892201690593,802795789469,546391016021,467664322522,241667773673,325071552919,808180657344,883072818378,094776610618,743039260076,092479283505,326511031916,219618970644,411873080737,931043691043,296012323783,300814606917,303822575542,420814345532,899188398691,093973853253,960639112596,723205702811,436383514842,312946089387,600310625339,306109670684,381260490747,372004125320,764482557331,782645973791,289143163514,351951630132,166391985076,068011249945,163220562780,393402838373,063829613942,314642499074,570878255064,243964310975,436995157701,963690474723,328528749406,069721401477,518368631528,494342409922,010014027154,483440131694,011812592349,456163172512,172814097302,180754852103,109992134225,135706656868,913142095474,575275655865,276322113591,244110146703,245080968959,631951072441",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"sumOfSum > 0",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  

  "[unittest] DynamoDB Resource Status - getRegions" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=DynamoDB",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"4x8"
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;modeStatic=sum;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
  
  "[unittest] DynamoDB Resource Status" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000006612683,000024256683,000024710191,000036892640,000058960170,000065539461,000070820998,000108650099",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeLimits",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName,billingMode:billingMode;nocsv",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeDynamoDBAccountLimit",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeDynamoDBTableLimitRisk",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  "[unittest] DynamoDB Resource Status with localCache" : {
    "meta" : {
      "reportName": "get DynamoDB Resource Status with localCache",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000006612683,000024256683,000024710191,000036892640,000058960170,000065539461,000070820998,000108650099",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeLimits",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBAccountLimit",
         "args":"",
         "inputs":"#addAccountDetails=yes;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBAccountLimit",
         "args":"",
         "inputs":"#addAccountDetails=yes;nocsv",
         "conditions":"riskStatus!=\"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTableLimitRisk",
         "args":"",
         "inputs":"#addAccountDetails=yes;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTableLimitRisk",
         "args":"",
         "inputs":"#addAccountDetails=yes;nocsv",
         "conditions":"riskStatus<>\"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] DynamoDB Consumed Capacity - setTargetValues" : {
    "meta" : {
      "reportName": "get DynamoDB Consumed Capacity",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59.9 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ProvisionedReadCapacityUnits\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ProvisionedWriteCapacityUnits\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ConsumedReadCapacityUnits\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ConsumedWriteCapacityUnits\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ddb.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         }
        ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] DynamoDB Consumed Capacity - getRegions" : {
    "meta" : {
      "reportName": "get DynamoDB Consumed Capacity",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59.9 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"serviceName=DynamoDB",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ConsumedReadCapacityUnits\"}",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"ddb.listMetrics",
         "args":"{\"namespace\":\"AWS/DynamoDB\",\"metricName\":\"ConsumedWriteCapacityUnits\"}",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ddb.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         }
        ]
    }, # end: Template Items#
  
  "[unittest] DynamoDB Streams Status" : {
    "meta" : {
      "reportName": "get DynamoDB Streams Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=000000000000",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ddbstreams.listStreams",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
        {"platform":"k2",
         "apiName":"ddbstreams.describeStream",
         "args":"{\"streamArn\":\"${__streamArn__}\"}",
         "inputs":"sourceApiName=ddbstreams.listStreams;targetValues=accountId:accountId_,regionCode:regionCode_,streamArn:streamArn;",
         "conditions":"",
         "limit":"",
         "pt":"4x2"
         },
      ]
    },
  
  # begin: Template Items
  "[unittest] EMR Resource Status" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"2.9 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"emr.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"emr.listBootstrapActions",
         "args":"{\"clusterId\":\"${__clusterId__}\"}",
         "inputs":"sourceApiName=emr.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:id;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"emr.describeCluster",
         "args":"{\"clusterId\":\"${__clusterId__}\"}",
         "inputs":"sourceApiName=emr.describeCluster;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:id;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"emr.listInstances",
         "args":"{\"clusterId\":\"${__clusterId__}\"}",
         "inputs":"sourceApiName=emr.describeCluster;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:id;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
      ]
    }, # end: Template Items#
        
  # begin: Template Items
  "[unittest] EMR Resource Status v2" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"emr.listMetrics", 
          "args":"{\"namespace\":\"AWS/ElasticMapReduce\", \"metricName\":\"IsIdle\"}",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "pt":"12x8"
          },
        {"platform":"k2",
         "apiName":"emr_IsIdle.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=emr.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"activeCount > 0",
         "limit":"100",
         "pt":"32x8"
         },
        {
          "platform":"k2",
          "apiName":"emr.listBootstrapActions",
          "args":"{\"clusterId\":\"${__clusterId__}\"}",
          "inputs":"sourceApiName=emr_IsIdle.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:JobFlowId;addAccountDetails=yes",
          "conditions":"",
          "limit":"1",
          "pt":"1x4"
          },
        {
          "platform":"k2",
          "apiName":"emr.describeCluster",
          "args":"{\"clusterId\":\"${__clusterId__}\"}",
          "inputs":"sourceApiName=emr_IsIdle.getMetricStatistic;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:JobFlowId;primaryKeys=ec2InstanceAttributes,status;addAccountDetails=yes",
          "conditions":"",
          "limit":"1",
          "pt":"1x4"
          },
        {
          "platform":"k2",
          "apiName":"emr.listInstances",
          "args":"{\"clusterId\":\"${__clusterId__}\"}",
          "inputs":"sourceApiName=emr_IsIdle.getMetricStatistic;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:JobFlowId;primaryKeys=status,timeline,stateChangeReason;addAccountDetails=yes",
          "conditions":"",
          "limit":"",
          "pt":"4x1"
          },
        {
          "platform":"k2",
          "apiName":"emr_ec2.getMetricStatistics",
          "args":"",
          "inputs":"sourceApiName=emr.listInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:ec2InstanceId;mode=Summary",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EMR Resource Status v3" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"emr.listMetrics", 
          "args":"{\"namespace\":\"AWS/ElasticMapReduce\", \"metricName\":\"IsIdle\"}",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "pt":"12x8"
          },
        {"platform":"k2",
         "apiName":"emr_IsIdle.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=emr.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"activeCount > 0",
         "limit":"100",
         "pt":"32x8"
         },
        {
          "platform":"moduAWS",
          "apiName":"describeResource.ElasticMapReduce",
          "args":"",
          "inputs":"sourceApiName=emr_IsIdle.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:JobFlowId;addAccountDetails=yes",
          "conditions":"",
          "limit":"1",
          "pt":"1x4"
          },
        {
          "platform":"k2",
          "apiName":"#emr.listInstances",
          "args":"{\"clusterId\":\"${__clusterId__}\"}",
          "inputs":"sourceApiName=emr_IsIdle.getMetricStatistic;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:JobFlowId;primaryKeys=status,timeline,stateChangeReason;addAccountDetails=yes",
          "conditions":"",
          "limit":"",
          "pt":"4x1"
          },
        {
          "platform":"k2",
          "apiName":"#emr_ec2.getMetricStatistics",
          "args":"",
          "inputs":"sourceApiName=emr.listInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:ec2InstanceId;mode=Summary",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] EMR Resource Status v4" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"emr.listMetrics", 
          "args":"{\"namespace\":\"AWS/ElasticMapReduce\", \"metricName\":\"IsIdle\"}",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=dimensions",
          "pt":"12x8"
          },
        {
          "platform":"moduAWS",
          "apiName":"describeResource.ElasticMapReduce",
          "args":"",
          "inputs":"sourceApiName=emr.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:dimension/JobFlowId;ttl=-1;addAccountDetails=yes",
          "conditions":"",
          "limit":"100",
          "pt":"1x4"
          },
        {"platform":"moduAWS",
         "apiName":"#emr.filterResults",
         "args":"",
         "inputs":"sourceApiName=describeResource.ElasticMapReduce;targetValues=accountId_:accountId_,regionCode_:regionCode_,clusterId:clusterId,State:State",
         "conditions":"State != ENDED",
         "limit":"",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"#emr.listInstances",
          "args":"{\"clusterId\":\"${__clusterId__}\"}",
          "inputs":"sourceApiName=emr.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,clusterId:clusterId;primaryKeys=status,timeline,stateChangeReason;addAccountDetails=yes",
          "conditions":"",
          "limit":"10",
          "pt":"4x1"
          },
        {
          "platform":"k2",
          "apiName":"#emr_ec2.getMetricStatistics",
          "args":"",
          "inputs":"sourceApiName=emr.listInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:ec2InstanceId;mode=Summary",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] SNS Resource Status" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=073029588280;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"#sns.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Simple Notification Service;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"sns.listSubscriptions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"sns.getSubscriptionAttributes",
         "args":"{\"subscriptionArn\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=sns.listSubscriptions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:subscriptionArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[unittest] SNS Utilization Metrics - getRegions" : {
    "meta" : {
      "reportName": "get SNS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"sns.getRegions",
         "args":"",
         "inputs":"serviceName=SNS",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"sns.listMetrics", 
          "args":"{\"namespace\":\"AWS/SNS\", \"metricName\":\"${__metricName__}\"}",
          "inputs": "sourceApiName=sns.getRegions;targetValues=accountId:accountId,regionCode:regionCode,metricName:NumberOfMessagesPublished",
          "limit":"",
          "pt":"8x8"
          },
        {
          "platform":"k2",
          "apiName":"sns.getMetricStatistics", 
          "inputs": "sourceApiName=sns.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;mode=Summary;modeStatic=sum",
          "limit":"",
          "pt":"32x8"
          }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] S3 Resource Status" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         #"inputs":"regionCode_=us-east-1;nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=001021966979,004936720820,007225946228,011462031405,015412669528,017595932766,018140111239,018625789578,019419057661,019663671740,022453619711,025171603963,031747008998,032225828555,032752001513,034732318111,035366522769,036810467918,037221463423,038350090545,044836873729,046077224557,047861376280,050326653968,051622341696,055241993554,062147603158,064791318906,065284116995,069103890367,075576879578,076816849230,077747001298,080208654979,081094348956,083001620099,091580165780,096581195568,101701947710,107055034741,107887377454,111877695556,112463388893,120929875626,121207594131,122664425162,122766593987,123878803236,131445638284,131551438844,132474328055,134841937311,136517795196,136900373398,139575350133,142391681048,143694612088,145015701200,148534749685,148854877803,150240520581,153324083341,157992868384,158322793601,162509291995,164873163631,169605406323,170832783737,173422545192,175302818187,177050674279,177394158488,179344813127,179547195354,182884026689,185682115242,187267213898,189578040712,195117145120,199706195734,202380523568,205768376595,209005782362,212388985171,214674611331,215173848830,215270503916,216004057036,224543217789,225518562558,226155409167,227733067781,232020330000,235376042741,235488158788,239496101648,240127557415,241928750097,248931771071,249770558448,252048700983,252567705216,255595704457,255771770578,257072834198,257211149240,258646356429,260693627855,267565671650,268102799199,272064604174,273875257893,273941044160,275905469650,281255733988,285693544190,288865833343,291132088516,293975193263,295984362375,297041200625,297666849420,299319930995,303045307423,303804202106,304039133846,305700060755,307222833476,312726047710,313952162152,314125218338,319067556270,319969684883",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/S3\",\"maxResults\":500}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,BucketName:BucketName,StorageType:StorageType;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=BucketName:BucketName,StorageType:StorageType:clusterName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] S3 Bucket Policies - getRegions" : {
    "meta" : {
      "reportName": "get S3 Bucket Policies",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         #"inputs":"regionCode_=us-east-1;nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "inputs":"serviceName=S3",
         "conditions":"serviceName==S3",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"s3.listBuckets",
         "args":"",
         "inputs":"sourceApiName=getRegions;targetValues=accountId:accountId,regionCode:regionCode",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"s3.getBucketLifecycleConfiguration",
         "args":"{\"bucket\":\"${__bucketName__}\"}",
         "inputs":"sourceApiName=s3.listBuckets;targetValues=accountId:accountId_,regionCode:regionCode_,bucketName:name",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
    
  # begin: Template Items
  "[unittest] S3 Bucket Policies - setTargetValues" : {
    "meta" : {
      "reportName": "get S3 Bucket Policies",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         #"inputs":"regionCode_=us-east-1;nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "inputs":"regionCode_=us-east-1;accountId_=306102952128",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"s3.listBuckets",
         "args":"",
         "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionName",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.s3finderRequest",
         "args":"",
         "inputs":"sourceApiName=s3.listBuckets;targetValues=accountId:accountId_,regionCode:regionCode_,bucketName:name",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] S3 Resource Status v2" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000000000000;metricName=BucketSizeBytes",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"s3.listMetrics",
         "args":"{\"namespace\":\"AWS/S3\", \"metricName\":\"${__metricName__}\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,metricName:metricName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=s3.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;mode=Summary;modeStatic=maximum",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
    # begin: Template Items
  "[unittest] SQS Resource Status" : {
    "meta" : {
      "reportName": "get SQS Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-east-1,us-west-2;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"sqs.listQueues", 
          "args":"",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "pt":"12x8"
          },
        {
          "platform":"k2",
          "apiName":"sqs.getQueueAttributes", 
          "args":"{\"queueUrl\":\"${__queueUrl__}\"}",
          "inputs": "sourceApiName=sqs.listQueues;targetValues=accountId:accountId_,regionCode:regionCode_,queueUrl:result",
          "pt":"12x8"
          },
        {
          "platform":"k2",
          "apiName":"sqs.listMetrics", 
          "args":"{\"namespace\":\"AWS/SQS\", \"metricName\":\"NumberOfMessagesSent\"}",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "pt":"12x8"
          },
        {
          "platform":"k2",
          "apiName":"sqs.listMetrics", 
          "args":"{\"namespace\":\"AWS/SQS\", \"metricName\":\"NumberOfMessagesReceived\"}",
          "inputs": "sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "pt":"12x8"
          },
        {"platform":"k2",
         "apiName":"sqs.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=sqs.listMetrics;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         }
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[unittest] ECS Status" : {
    "meta" : {
      "reportName": "get ECS+Fargate Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         #"inputs":"regionCode_=us-east-1;nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=001021966979,004936720820,007225946228,011462031405,015412669528,017595932766,018140111239,018625789578,019419057661,019663671740,022453619711,025171603963,031747008998,032225828555,032752001513,034732318111,035366522769,036810467918,037221463423,038350090545,044836873729,046077224557,047861376280,050326653968,051622341696,055241993554,062147603158,064791318906,065284116995,069103890367,075576879578,076816849230,077747001298,080208654979,081094348956,083001620099,091580165780,096581195568,101701947710,107055034741,107887377454,111877695556,112463388893,120929875626,121207594131,122664425162,122766593987,123878803236,131445638284,131551438844,132474328055,134841937311,136517795196,136900373398,139575350133,142391681048,143694612088,145015701200,148534749685,148854877803,150240520581,153324083341,157992868384,158322793601,162509291995,164873163631,169605406323,170832783737,173422545192,175302818187,177050674279,177394158488,179344813127,179547195354,182884026689,185682115242,187267213898,189578040712,195117145120,199706195734,202380523568,205768376595,209005782362,212388985171,214674611331,215173848830,215270503916,216004057036,224543217789,225518562558,226155409167,227733067781,232020330000,235376042741,235488158788,239496101648,240127557415,241928750097,248931771071,249770558448,252048700983,252567705216,255595704457,255771770578,257072834198,257211149240,258646356429,260693627855,267565671650,268102799199,272064604174,273875257893,273941044160,275905469650,281255733988,285693544190,288865833343,291132088516,293975193263,295984362375,297041200625,297666849420,299319930995,303045307423,303804202106,304039133846,305700060755,307222833476,312726047710,313952162152,314125218338,319067556270,319969684883",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__endpointName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:arnV2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listContainerInstances",
         "args":"",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeContainerInstances",
         "args":"{\"containerInstances\":\"${__containerInstances__}\"}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,containerInstances:containerInstances",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listTaskDefinitions",
         "args":"",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeTaskDefinition",
         "args":"{\"taskDefinition\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.listTaskDefinitions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:result;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
        
        
  # begin: Template Items
  "[unittest] ECS+Fargate Resource Status" : {
    "meta" : {
      "reportName": "get ECS+Fargate Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         #"inputs":"regionCode_=us-east-1;nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=001021966979,004936720820,007225946228,011462031405,015412669528,017595932766,018140111239,018625789578,019419057661,019663671740,022453619711,025171603963,031747008998,032225828555,032752001513,034732318111,035366522769,036810467918,037221463423,038350090545,044836873729,046077224557,047861376280,050326653968,051622341696,055241993554,062147603158,064791318906,065284116995,069103890367,075576879578,076816849230,077747001298,080208654979,081094348956,083001620099,091580165780,096581195568,101701947710,107055034741,107887377454,111877695556,112463388893,120929875626,121207594131,122664425162,122766593987,123878803236,131445638284,131551438844,132474328055,134841937311,136517795196,136900373398,139575350133,142391681048,143694612088,145015701200,148534749685,148854877803,150240520581,153324083341,157992868384,158322793601,162509291995,164873163631,169605406323,170832783737,173422545192,175302818187,177050674279,177394158488,179344813127,179547195354,182884026689,185682115242,187267213898,189578040712,195117145120,199706195734,202380523568,205768376595,209005782362,212388985171,214674611331,215173848830,215270503916,216004057036,224543217789,225518562558,226155409167,227733067781,232020330000,235376042741,235488158788,239496101648,240127557415,241928750097,248931771071,249770558448,252048700983,252567705216,255595704457,255771770578,257072834198,257211149240,258646356429,260693627855,267565671650,268102799199,272064604174,273875257893,273941044160,275905469650,281255733988,285693544190,288865833343,291132088516,293975193263,295984362375,297041200625,297666849420,299319930995,303045307423,303804202106,304039133846,305700060755,307222833476,312726047710,313952162152,314125218338,319067556270,319969684883",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ecs.listTaskDefinitions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;#sourceApiName=ecs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeTaskDefinition",
         "args":"{\"taskDefinition\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.listTaskDefinitions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:value;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__clusterName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:arnV2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listServices",
         "args":"{\"cluster\":\"${__clusterName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:clusterName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeServices",
         "args":"{\"cluster\":\"${__clusterName__}\",\"services\":[\"${__serviceName__}\"]}",
         "inputs":"sourceApiName=ecs.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:cluster_,serviceName:arnV2;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listTasks",
         "args":"{\"cluster\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listContainerInstances",
         "args":"{\"cluster\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeContainerInstances",
         "args":"{\"cluster\":\"${__endpointName__}\",\"containerInstances\":${__containerInstance__}}",
         "inputs":"sourceApiName=ecs.listContainerInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName,containerInstance:containerInstanceArns",
         "conditions":"",
         "limit":"",
         "pt":""
         }, #"include":["ATTACHMENTS"]},"apiName":"ecs.describeClusters","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"{\"instanceIds\":[\"${__instanceId__}\"]}",
         "inputs":"sourceApiName=ecs.describeContainerInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;primaryKeys=instances,state;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },#{"instanceIds":["i-0df192389801a191b"]},"apiName":"ec2.describeInstances","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/ECS\",\"maxResults\":500}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,serviceName:ServiceName,clusterName:ClusterName;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ServiceName:serviceName_,ClusterName:clusterName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEcsAwsLogsRisk",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeEcsRiskReport",
         "args":"to run, comment out",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] DirectConnect Status" : {
    "meta" : {
      "reportName": "get AWS DirectConnect Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"nocsv;regionCode_=us-east-1;accountId_=125045214519,156473568459,237713249721,253503506339,269684609367,278243021885,341017068458,425895262676,436482704436,441322091643,501491263702,514255145852,548937513695,583494550716,598391869624,604970084501,610804702590,784269182957,785370285395,831344028569,885837828261,957986369084,968738427600,993484252755",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/DX\",\"maxResults\":500}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace;nocsv",
         "conditions":"ConnectionState,ConnectionErrorCount in metricName",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,ConnectionId:ConnectionId,VirtualInterfaceId:VirtualInterfaceId,OpticalLaneNumber:OpticalLaneNumber;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ConnectionId:ConnectionId,VirtualInterfaceId:VirtualInterfaceId,OpticalLaneNumber:OpticalLaneNumber;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] OpenSearch Status" : {
    "meta" : {
      "reportName": "get OpenSearch Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"regionCode_=ap-southeast-1,eu-central-1,eu-west-1,regionCode_,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2;accountId_=002777230731,004730732493,029176679838,044794144721,046979685931,051465757517,052852011374,062091326320,062711226102,068011249945,069272765570,083124926037,084376588688,087660466352,091369708580,092479283505,102671227235,103262953349,104636225068,107274433934,122833486767,126190501570,127345046654,144790999774,148679622671,158364073093,164108474161,169344650340,178525769593,180754852103,188942795616,191582840397,192735705417,196863821692,197756049917,205857894628,212483508239,218741990574,221719365909,233367263614,235372617315,237135062076,243969040095,253908670668,274868111244,276164778726,280924275668,284722348816,289036058743,296012323783,301527105559,306320624757,314642499074,317247770270,326511031916,331078587791,341908542378,347668657311,356623176356,357126491496,359804509760,368969384759,373428735865,378376160408,381260490747,383778099404,393287210976,404443498944,409620516115,412944794664,416324547236,421238934528,431703225954,433265895211,441483007058,446802202443,448184564114,462017216899,463137498994,463656602360,469308961519,470025801381,494342409922,501429885192,513583567099,514712878770,516239874946,518368631528,522240571317,526657233363,529363209591,532358706936,000000000000,539783510382,554036784086,554589799061,579257000140,581725896129,584291268218,586899911946,588354806407,599869035376,601323899993,607899199937,617186983611,625301487095,632211784174,632285889341,633332969123,639172912969,640894516468,653731015166,000000000000,668735325459,672714205403,674247937597,675034299699,680427445313,680814905614,693621782543,694689889109,707987546577,717922525904,718658585106,728227005623,729456622915,730836146782,742617195046,747260357079,750202118857,751689567599,765335004154,782378930297,793196732353,799877353134,813646640714,820169455853,832844619813,867183384685,882413164269,883072818378,890011560610,890831765352,894182077310,911976450587,913142095474,916964652363,919740896133,921482183954,926239361991,934442535328,935986877796,944807178991,966831709730,968332798967,970586292401,973848555221",
        "conditions":"",
        "limit":"10",
        "pt":""
        },
      {
        "platform":"k2",
        "apiName":"es.listDomainNames",
        "args":"",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"es.describeElasticsearchDomain",
         "args":"{\"domainName\":\"${__domainName__}\"}",
         "inputs":"sourceApiName=es.listDomainNames;targetValues=accountId:accountId_,regionCode:regionCode_,domainName:domainName",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
      ]
    }, # end: Template Items#
        
  # begin: Template Items
  "[unittest] SageMaker Studio Status" : {
    "meta" : {
      "reportName": "get SageMaker Studio Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=910523329506,067440223434,360201567367;regionCode_=us-east-1",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
          "conditions":"",
          "limit":"1",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"modu.combineResults",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
        {"platform":"k2",
         "apiName":"sagemaker.listDomains",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"sagemaker.describeDomain",
         "args":"{\"domainId\":\"${__domainId__}\"}",
         "inputs":"sourceApiName=sagemaker.listDomains;targetValues=accountId:accountId_,regionCode:regionCode_,domainId:domainId;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"{\"subnetIds\":${__subnetIds__}}",
         "inputs":"sourceApiName=sagemaker.describeDomain;targetValues=accountId:accountId_,regionCode:regionCode_,subnetIds:subnetIds;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeNetworkInterfaces",
         "args":"",
         "inputs":"sourceApiName=sagemaker.describeDomain;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeNetworkInterfaces",
         "args":"{\"filters\":[{\"name\": \"description\",\"values\": [\"*${__domainId__}*\"]}]}",
         "inputs":"sourceApiName=sagemaker.describeDomain;targetValues=accountId:accountId_,regionCode:regionCode_,domainId:domainId;nocsv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  
  # begin: Template Items
  "[unittest] CloudTrail Events Lookup" : {
    "meta" : {
      "reportName": "get CloudTrail Events",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"5 minutes ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=000000000000;regionCode_=us-west-2",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"cloudtrail.describeTrails",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          },
        {
          "platform":"k2",
          "apiName":"cloudtrail.lookupEvents",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=cloudTrailEvent,cloudTrailEvent/userIdentity/sessionContext,cloudTrailEvent/userAgent,cloudTrailEvent/resources,cloudTrailEvent/requestParameters/resourceSpec;updateIpAddresses=cloudTrailEvent/sourceIPAddress;lookupAttributes=EventSource:s3.amazonaws.com;maxPaginatingCount=1",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          },
        {
          "platform":"k2",
          "apiName":"#cloudtrail.lookupEvents",
          "args": "{\"endTime\": 1654324867000,\"lookupAttributes\": [{\"attributeKey\": \"Username\",\"attributeValue\": \"tagSync\"}],\"startTime\": 1654324567000}",
          #"args": {
          #  "endTime": 1654324867000,
          #  "lookupAttributes": [
          #    {
          #      "attributeKey": "Username",
          #      "attributeValue": "tagSync"
          #    }
          #  ],
          #  "startTime": 1654324567000
          #},
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
        {
          "platform":"k2",
          "apiName":"#cloudtrail.lookupEvents",
          #"args":"{\"endTime\": 1654324867000,\"startTime\": 1654324567000}
          "args":"{\"startTime\":${__startTime__},\"endTime\":${__endTime__}}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
      ]
    }, # end: Template Items#
  
  

  # begin: Template Items
  "[unittest] Health Events - setTargetValues" : {
    "meta" : {
      "reportName": "get AWS Health Events Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"nocsv;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.getDwActiveAccessedAccounts",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1;nocsv",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"health.describeEvents",
         "args":"{\"filter\":{\"eventStatusCodes\":[\"open\",\"upcoming\"]}}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"health.describeEventDetails",
         "args":"{\"eventArns\":[\"${__endpointName__}\"],\"locale\":\"en\"}",
         "inputs":"sourceApiName=health.describeEvents;targetValues=accountId:accountId_,regionCode:us-east-1,endpointName:arn;primaryKeys=event,eventDescription",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] Health Events - getAccounts" : {
    "meta" : {
      "reportName": "get AWS Health Events Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getAccounts",
         "args":"",
         "inputs":"",
         "conditions":"accountStatus == Active",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"health.describeEvents",
         "args":"{\"filter\":{\"eventStatusCodes\":[\"open\",\"upcoming\"]}}",
         "inputs":"sourceApiName=modu.getAccounts;targetValues=accountId:accountId,regionCode:primaryRegion;nocsv",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"health.describeEventDetails",
         "args":"{\"eventArns\":[\"${__endpointName__}\"],\"locale\":\"en\"}",
         "inputs":"sourceApiName=health.describeEvents;targetValues=accountId:accountId_,regionCode:us-east-1,endpointName:arn;primaryKeys=event,eventDescription",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] Service Quotas - k2" : {
    "meta" : {
      "reportName": "get AWS Service Quotas Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=000000000000",
         #"inputs":"nocsv;regionCode_=us-east-1,us-west-2;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"servicequotas.listServices",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=services",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"servicequotas.listAWSDefaultServiceQuotas",
         "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;primaryKeys=quotas",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"servicequotas.listServiceQuotas",
         "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;primaryKeys=quotas",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"servicequotas.getServiceQuota",
         "args":"{\"serviceCode\":\"${__serviceCode__}\",\"quotaCode\":\"${__quotaCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listAWSDefaultServiceQuotas;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode,quotaCode:quotaCode",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"servicequotas.listRequestedServiceQuotaChangeHistory",
         "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;nocsv",
         "conditions":"",
         "limit":"1",
         "pt":""
         }
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] Service Quotas - k2 v2" : {
    "meta" : {
      "reportName": "get AWS Service Quotas Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"sq.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=550202007170,876969159949,742617195046,245012523099,934442535328,742617195046,647400204775,275853731244",
         #"inputs":"nocsv;regionCode_=us-east-1,us-west-2;accountId_=427945842608,728530619017,420333725640,217907265575,625850340992,811638776122,259972792949,707418130092,564228134318,297869649028,116723841685,536007973389,047015970086,285494791500,490686735290,667745860491,374273138463,007151677815,740211480089,395961451816,241468775643,975340937595,337296087877,057575031399,695325901967,005424429174,624011181711,434646116308,185044545307,939979298949,511425887085,367680965068,691151434628,555989621042,965344406679,349787692915,663646683190,730704820681,721512357240,716024182626,446767646693,815611182608,176493635416,696003787994,245567265523,315707684151,628618566172,682577484452,278099998695,900220213706,578127021068,315815825025,928065573155,701060243197,310701860530,257336783850,225952583976,609746069400,561279980848,615657125838,489518540378,779965715604,243559778240,939408468652,821210393816,017652622216,980128333007,112009290641,421525064356,049322865075,576127759380,729253156267,694360817678,120754304818,600636175464,648723230879,138095018599,630979271797,980912687923,569307791389,988326039141,520466059738,531869628843,639323261939,142141077163,651692584145,622801415664,252570295510,543083052860,402096869094,024331715902,618458174671,358461429827,407645170213,985810621601,728797481826,932026535033,837779584898,152445837306,591817020287,439211114201,573298784784,576472852999,312122144264,723709227021,995801282319,507779333965,670724675978,060057142442,368144868825,539040832729,557313604773,576022732266,734317985263,050709520264,109635152635,024248659068,886140117267,961585277208,855837714716,573766042964,928223755644,833759359994,956719310983,584382608272,295985375720,197684780861,995405021314,326917611516,756095380250,609599880397,483337878387,665510281918,500371356079,904164890034,472052004344,771718672770,031126985389,500637060569,899736751139,257694131448,947114806411,344320315996,201388263002,174869565779,808851785163,137895572659,878903742750,668653513723,226966462507,663575338818,977307258527,134612068756,076726034761,360704552743,160892777486,402339383212,691147410654,906884740013,987351795236,762463801350,672729938572,252271153744,869579802485,992236886450,923481514985,799983782075,747025564505,443319606395,525062545098,378242289052,753386001330,008896111484,132830317640,841972115946,255914666153,425839570375,976902502269,348943020176,586688205929,716379450707,470217404723,345029389065,916818569812,637876949190,819377084500,463704315857,032225828555,472371395705,427095376100,426511756460,541515446886,465437252404,695223818216,968042363948,808780364587,287775224950,236886662125,081191905642,065230691846,370930610156,515815772312,018427413975,072197632768,067376866414,867785020276,768643713700,760221304544,727956702644,743788802727,200521923776,999757495161,060887346771,697788136851,816596761318,343959289337,450831664022,601004557349,951266633832,339037037539,337494346560,464620636071,747503890418,307775763817,804520257287,685324779038,661593919715,544055538831,408062760677,148000086933,437640904951,112035854834,913118591559,361797794302,876984788703,079703623260,345301010778,127446200199,731956760637,964734155898,139748985827,066701722827,566494245102,901592826430,193641745523,852261503344,853126036468,493625265029,454602648341,825464657731,022654238605,760541463512,807341249223,837289647712,985395101222,765953956820,534029189824,913855544450,455860882765,940257917997,643200432761,261435181829,714016060284,435452684675,655494236542,673987358968,403810694830,161957915098,978566430726,434857305668,511923599351,241328928294,923776338499,175595011903,055449777576,837247620847,912532601716,606149647722,978103302105,138590152455,467101125475,065853655954,235394992754,350582994650,165807803836,792024984523,348245319734,249934023183,109212638691,440563683899,232255457729,633815352428,547007983359,518541428617,743916033698,150914250974,587299008436,346597535352,827281608826,890452240102,854579513211,213821570209,935043638528,902380777341,397656653270,244862934322,897852276193,033352146516,926860981256,003209108278,499708628651,247780671696,228461870557,896708795334,660703753266,411010732387,348664399020,953009672510,184493454956,185693061807,647365954702,090408959049,191680075842,732633795717,800872381460,335396736074,153341984620,523037194898,656672294153,679212610363,447438572172,810758242441,495860749345,955866602645,465949743084,114132262795,372682250419,714320024241,783436530450,737799045451,285384875875,617180728163,572082461278,382434237373,001801837429,515457738014,007546291469,951189161844,549156912664,252855267018,154131452176,053422649775,474809315656,456740574861,138419986546,295595404131,217268829424,423622120418,659628812653,495237088078,035288683798,375680107385,574058752548,260447750387,878735952097,964237259483,375281822450,035261117412,080531683175,048610986077,292507398481,212302138597,761372054766,131834524554,770991406382,358885416727,581708796205,273418976292,763130357948,132886338704,803266514593,409148992933,679828101704,821056988371,981139964680,459044455442,957362905297,105518533125,555728544146,885868085171,211129616084,820881388768,543689851567,419741197617,534442817896,386032830181,852469753185,200691254848,266159761617,349667731870,401415984523,201195850704,504859804033,399011056660,684934547185,971667361291,769344395659,194032996414,137236545769,921848989829,350430924258,317141266490,426737219782,316410006187,312543394821,089522401509,957509496585,533168844947,269079498055,780444199014,336352095920,516397287871",
         "conditions":"",
         "limit":"10",
         "pt":"1x1"
         },
        {
          "platform":"k2",
           "apiName":"servicequotas.listServices",
           "args":"",
           "inputs":"sourceApiName=sq.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=services",
           "conditions":"",
           "limit":"",
           "pt":"8x8"
          },
        {"platform":"k2",
         "apiName":"servicequotas.listServiceQuotas",
         "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;primaryKeys=quotas",
         "conditions":"",
         "limit":"1",
         "pt":""
         },
        {
          "platform":"k2",
          "apiName":"#ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=sq.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
          "conditions":"",
          "limit":"1",
          "pt":"1x1"
          },
        {
          "platform":"k2",
           "apiName":"#servicequotas.listServices",
           "args":"",
           "inputs":"sourceApiName=ec2.describeRegions;targetValues=accountId:accountId_,regionCode:regionName;primaryKeys=services",
           "conditions":"",
           "limit":"",
           "pt":"8x8"
          },
        {
          "platform":"moduAWS",
          "apiName":"#modu.combineResults",
          "args":"",
          "inputs":"sourceApiName=sq.setTargetValues;targetValues=accountId_:accountId_;combineWith=servicequotas.listServices;asValues=regionCode_:regionCode_,serviceCode:serviceCode;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          },
        {
          "platform":"k2",
          "apiName":"#servicequotas.listServiceQuotas",
          "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
          "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;primaryKeys=quotas",
          "conditions":"",
          "limit":"1",
          "pt":""
          }
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] Trusted Advisor" : {
    "meta" : {
      "reportName": "[unittest] Trusted Advisor",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=982499846871;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"language":"en"},"apiName":"trustedadvisor.describeTrustedAdvisorChecks","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_,regionCode_:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId_:accountId_,regionCode_:regionCode_,checkIds_list:checkIds_list",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#trustedadvisor.refreshCheck",
         "args":"",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkIds":["Qch7DwouX1"]},"apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkIds\":${__checkIds__}}",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkIds:checkIds_list;primaryKeys=resourcesSummary,categorySpecificSummary",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkId":"Hs4Ma3G163"},"apiName":"trustedadvisor.describeTrustedAdvisorCheckResult","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"#trustedadvisor.describeTrustedAdvisorCheckResult",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\"}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeCheckItems",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\",\"count\":100,\"start\":0}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"totalCount > 0",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.joinResults",
         "args":"",
         "inputs":"sourceApiName=trustedadvisor.describeCheckItems;targetValues=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;targetColumns=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;joinWith=trustedadvisor.describeTrustedAdvisorChecks;indexKeys=checkId:id;joinValues=category:category,name:name",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=trustedadvisor.describeCheckItems;targetValues=accountId:accountId_,regionCode_:region,checkId:checkId",
         "conditions":"checkId == G31sQ1E9U",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=modu.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ta/;csvFilename=cdo-ta-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[unittest] Trusted Advisor v1" : {
    "meta" : {
      "reportName": "[unittest] Trusted Advisor",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=982499846871;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"language":"en"},"apiName":"trustedadvisor.describeTrustedAdvisorChecks","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.combineResultsAsList",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_,regionCode_:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.filterResults",
         "args":"",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId_:accountId_,regionCode_:regionCode_,checkIds_list:checkIds_list",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkIds":["Qch7DwouX1"]},"apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkIds\":${__checkIds__}}",
         "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkIds:checkIds_list;primaryKeys=resourcesSummary,categorySpecificSummary",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkId":"Hs4Ma3G163"},"apiName":"trustedadvisor.describeTrustedAdvisorCheckResult","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
          "platform":"k2",
         "apiName":"#trustedadvisor.describeTrustedAdvisorCheckResult",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\"}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeCheckItems",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\",\"count\":100,\"start\":0}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
         "conditions":"totalCount > 0",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.joinResults",
         "args":"",
         "inputs":"sourceApiName=trustedadvisor.describeCheckItems;targetValues=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;targetColumns=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;joinWith=trustedadvisor.describeTrustedAdvisorChecks;indexKeys=checkId:id;joinValues=category:category,name:name",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         }
      ]
    }, # end: Template Items#

  # begin: Template Items
  "[unittest] Trusted Advisor v2" : {
    "meta" : {
      "reportName": "[unittest] Trusted Advisor",
      "bcaDescription": "",
      "emailTemplate":"""cost_optimizing
fault_tolerance
performance
security
service_limits""",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=000000000000,482038169294,550202007170,876969159949,742617195046,245012523099,934442535328,742617195046,647400204775,275853731244;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        { 
          "platform":"k2",
          "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
          "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
          "conditions":"category == service_limits",
          "limit":"1",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"modu.combineResultsAsList",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId_:accountId_,regionCode:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
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
    }, # end: Template Items#
  "[unittest] internal AZ Mapping" : {
    "meta" : {
      "reportName": "internal AZ Mapping",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=062899627182,071526322190,077214743270,101501168676,128763887799,132560308323,167441482148,183278788232,313101196837,327620956293,331497817310,409510345044,426919580194,431650700249,501805413449,507527666758,512771429873,536780466184,542673382863,545688498300,552048274550,576101733904,599748404309,681249303254,695111649385,714677060918,730025460986,756429910560,799849535758,948829301388,966390519541,972641986213,980912687923,985395101222;regionCode_=ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-south-1,ap-southeast-1,ap-southeast-2,ca-central-1,cn-north-1,eu-central-1,eu-north-1,eu-west-1,eu-west-2,eu-west-3,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2internal.describeAvailabilityZoneMappings",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] Enterprise Customer Profile - k2 only" : {
    "meta" : {
      "reportName": "",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisMonth",
      "endTime":"today"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"profile.list",
        "args":"",
        "inputs":"#sourceMedia=remote;query=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
        "inputs":"sourceApiName=profile.list;targetValues=customerDomainName:customerDomainName",
        "conditions":"",
        "limit":"",
        "pt":""
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id",
        "conditions":"",
        "limit":"1",
        "pt":""
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id",
        "conditions":"status == Active",
        "limit":"1",
        "pt":""
        },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1",
        "conditions":"accountStatus == Active",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"awsadms.getAccountIdentifiersByAccountId",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"awsadms.getAccountIdentifiersByAccountId",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1",
        "conditions":"AccountIdType != \"\"",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"iss.searchCustomers",
        #{"accountId":"982499846871","region":"us-east-1","args":{"query":{"terms":[{"field_":"CustomerAccountPoolId","value_":"5827011","prefix":false,"phonetic":false},{"field_":"CustomerId","value_":"A37M5YNSUQXT7G","prefix":false,"phonetic":false}]},"includeDeactivatedCustomers":false,"pageSize":10},"apiName":"iss.searchCustomers","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
        "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=CustomerIdType:CustomerIdType,regionCode:us-east-1",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      #{
      #  "platform":"k2",
      #  "apiName":"awsadms.getAccountRole",
      #  "args":"",
      #  "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId",
      #  "conditions":"accountRole == PAYER",
      #  "limit":"",
      #  "pt":""
      #  },
      #{
      #  "platform":"k2",
      #  "apiName":"awsadms.getChildAccountsForParentAccount",
      #  "args":"",
      #  "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId;primaryKeys=childAccountList",
      #  "conditions":"",
      #  "limit":"",
      #  "pt":""
      #  },
      {
        "platform":"moduAWS",
        "apiName":"#profile.details",
        "args":"",
        "inputs":"",
        "conditions":"",
        "limit":"",
        "pt":""
        },
      ]
    }, # end: Template Items,
  # begin: Template Items
  "[unittest] iterating all resources by getRegions" : {
    "meta" : {
      "reportName": "getRegions",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"elb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=Elastic Load Balancing",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=EC2;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=EC2;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeVolumes",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=EC2;primaryKeys=attachments",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=EC2",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=ECS,EKS,Fargate",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__clusterName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:arnV2",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=DynamoDB",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
      {
        "platform":"k2",
        "apiName":"rds.describeDBInstances",
        "args":"",
        "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=RDS",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=RDS",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode,serviceName:serviceName;serviceName=Redshift",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Item#  
  
  # begin: Template Items
  "[unittest] iterating all resources by scanning all regions" : {
    "meta" : {
      "reportName": "getRegions",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"",
      "endTime":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"nocsv;",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId,regionCode:regionCode_;nocsv",
          "conditions":"",
          "limit":"1",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"modu.combineResults",
          "args":"",
          "inputs":"sourceApiName=modu.getRegions;targetValues=accountId_:accountId;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
        {"platform":"k2",
         "apiName":"elb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeVolumes",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=attachments",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__clusterName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:arnV2",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
      {
        "platform":"k2",
        "apiName":"rds.describeDBInstances",
        "args":"",
        "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Item#  
  
  # begin: Template Items
  "[unittest] Support Status" : {
    "meta" : {
      "reportName": "Support Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;accountId_=000000000000",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {
          "platform":"k2",
          "apiName":"support.searchCases",
          #{"filterBy": {"createdBy": [{"accountId": "000000000000"}, {"accountId": "000000000000"}], "language": "en"}}
          "args": "{\"filterBy\": {\"createdBy\": [{\"accountId\": \"${__accountId__}\"}], \"language\": \"en\"}}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
          "conditions":"",
           "limit":"",
           "pt":"4x2"
        },
        {
          "platform":"k2",
          "apiName":"support.describeCase",
          "args":"{\"caseId\":\"${__caseId__}\"}",
          "inputs":"sourceApiName=support.searchCases;targetValues=accountId:accountId,regionCode:us-east-1,caseId:caseId;primaryKeys=caseDetails,caseDetails/recentCommunications/communications",
          "conditions":"",
          "conditions":"",
           "limit":"",
           "pt":"4x2"
        },
      ]
    }, # end: Template Item#  
      
  # begin: Template Items
  "[ent] Enterprise Customer Profile v1 - k2 only" : {
    "meta" : {
      "reportName": "Enterprise Customer Profile - getRegions - k2 only",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"customerDomainName=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
        "conditions":"",
        "limit":"",
        "pt":""
        },
      ]
    }, # end: Template Item#  
      
  
  # begin: Template Items
  "[ent] Enterprise Customer Profile v2 - k2 only" : {
    "meta" : {
      "reportName": "Enterprise Customer Profile - getRegions - k2 only",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"customerDomainName=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
        "conditions":"",
        "limit":"",
        "pt":""
        },
      {
        "platform":"moduAWS",
        "apiName":"avs.combineResultsAsList",
        "args":"",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=regionCode_:us-east-1;combineWith=kumoscp.getCustomerAccountFullList;asValues=accountIds:accountId;chunkSize=50",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
       },
      { 
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=avs.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      { 
        "platform":"k2",
        "apiName":"avs.getSupportLevel",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=avs.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"moduAWS", 
        "apiName":"globalAccountStatus.filterResults", 
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId,regionCode_:us-east-1,accountStatus:accountStatus",
        "conditions":"accountStatus == Active",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAccountIdentifiersByAccountId", 
        "args":"{\"accountId\":\"${__accountId__}\"}", 
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"16x1"
        },
      {
        "platform":"k2", 
        "apiName":"iss.searchCustomers", 
        #"args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
        "args": "{\"includeDeactivatedCustomers\": false,\"marketplaceId\": \"ATVPDKIKX0DER\",\"pageSize\": 10,\"query\": {\"terms\": [{\"field_\": \"CustomerId\",\"phonetic\": false,\"prefix\": false,\"value_\": \"${__CustomerIdType__}\"}]}}",
        "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=accountId:accountId_,regionCode:regionCode_,CustomerIdType:CustomerIdType",
        "limit":"",
        "pt":"12x1"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAlternateContacts",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x1"
        },
      {
        "platform":"k2", 
        "apiName":"kumoscp.getTags",
        "args":"{\"resourceIds\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x1"
        },
      {
        "platform":"moduAWS", 
        "apiName":"cnAccountStatus.filterResults", 
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId,regionCode_:cn-north-1,accountStatus:accountStatus",
        "conditions":"accountStatus == Not Found",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"cnAccountStatus.combineResultsAsList",
        "args":"",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=regionCode_:cn-north-1;combineWith=cnAccountStatus.filterResults;asValues=accountIds:accountId_;chunkSize=50",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
       },
      { 
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=cnAccountStatus.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      { 
        "platform":"k2",
        "apiName":"avs.getSupportLevel", 
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=cnAccountStatus.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAccountIdentifiersByAccountId", 
        "args":"{\"accountId\":\"${__accountId__}\"}", 
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"16x1"
        },
      {
        "platform":"moduAWS", 
        "apiName":"cnCustomerId.filterResults", 
        "args":"",
        "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=accountId_:accountId,regionCode_:regionCode,CustomerIdType:CustomerIdType",
        "conditions":"regionCode == cn-north-1",
        "limit":"",
        "pt":"1x8"
        },
      {
        "platform":"k2", 
        "apiName":"iss.searchCustomers", 
        #"args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
        "args": "{\"includeDeactivatedCustomers\": false,\"marketplaceId\": \"AAHKV2X7AFYLW\",\"pageSize\": 10,\"query\": {\"terms\": [{\"field_\": \"CustomerId\",\"phonetic\": false,\"prefix\": false,\"value_\": \"${__CustomerIdType__}\"}]}}",
        "inputs":"sourceApiName=cnCustomerId.filterResults;targetValues=accountId:accountId,regionCode:regionCode,CustomerIdType:CustomerIdType",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAlternateContacts",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x1"
        },
      {
        "platform":"k2", 
        "apiName":"kumoscp.getTags",
        "args":"{\"resourceIds\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x1"
        },
      {
        "platform":"k2",
         "apiName":"#cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/Usage\",\"maxResults\":500}",
         "inputs":"sourceApiName=activeAccount.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=dimensions;nocsv",
         "conditions":"name == Service",
         "limit":"",
         "pt":"16x8"
         },
      {
        "platform":"moduAWS",
        "apiName":"#modu.filterResults",
        "args":"",
        "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId_:accountId_,regionCode_:regionCode_,serviceName:value;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
        "apiName":"#ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"16x8"
        },
      ]
    }, # end: Template Items,
  
  # begin: Template Items
  "[ent] Enterprise Customer Profile v3 - k2 only" : {
    "meta" : {
      "reportName": "Enterprise Customer Profile - getRegions - k2 only",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"customerDomainName=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
        "conditions":"status == Active",
        "limit":"",
        "pt":""
        },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"1",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/Usage\",\"maxResults\":500}",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
      {
        "platform":"k2",
        "apiName":"cloudwatch.getMetricStatistics",
        "args":"",
        "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
        "conditions":"activeCount > 0",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"moduAWS",
        "apiName":"getMetric.filterResults",
        "args":"",
        "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId_:accountId_,regionCode_:regionCode_,serviceName:Service;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      ]
    }, # end: Template Items,
  
  # begin: Template Items
  "[ent] Enterprise Customer Profile v4 - k2 only" : {
    "meta" : {
      "reportName": "Enterprise Customer Profile - getRegions - k2 only",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"customerDomainName=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
        "conditions":"status == Active",
        "limit":"",
        "pt":""
        },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"1",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/Usage\",\"maxResults\":500}",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
      {
        "platform":"moduAWS",
        "apiName":"searchMetrics.filterResults",
        "args":"",
        "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId_:accountId_,regionCode_:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions,dimensions2:dimensions;primaryKeys=dimensions2;nocsv",
        "conditions":"name == Resource",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"moduAWS",
        "apiName":"searchMetrics2.filterResults",
        "args":"",
        "inputs":"sourceApiName=searchMetrics.filterResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,controlPlaneApiName:value,namespace:namespace,metricName:metricName,dimensions:dimensions;nocsv",
        "conditions":"controlPlaneApiName not startsWith Describe,List,Get",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
        "apiName":"cloudwatch.getMetricStatistics",
        "args":"",
        "inputs":"sourceApiName=searchMetrics2.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
        "conditions":"activeCount > 0",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"moduAWS",
        "apiName":"getMetric.filterResults",
        "args":"",
        "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId_:accountId_,regionCode_:regionCode_,serviceName:Service;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      ]
    }, # end: Template Items,
  
  # begin: Template Items
  "[ent] Enterprise Customer Profile v5 - k2 only" : {
    "meta" : {
      "reportName": "Enterprise Customer Profile - getRegions - k2 only",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.setTargetValues",
        "args":"",
        "inputs":"customerDomainName=nike.com",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.searchCustomers",
        "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"moduAWS@\"}",
        "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2",
        "apiName":"kumoscp.getCustomerAccountFullList",
        "args":"{\"id\":\"${__id__}\"}",
        "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id",
        "conditions":"",
        "limit":"",
        "pt":"1x8"
        },
      {
        "platform":"moduAWS",
        "apiName":"avs.combineResultsAsList",
        "args":"",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=regionCode_:us-east-1;combineWith=kumoscp.getCustomerAccountFullList;asValues=accountIds:accountId;chunkSize=50",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      { 
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=avs.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
      { 
        "platform":"k2",
        "apiName":"avs.getSupportLevel",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=avs.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
      {
        "platform":"moduAWS", 
        "apiName":"globalAccountStatus.filterResults", 
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId,regionCode_:us-east-1,accountStatus:accountStatus",
        #"conditions":"accountStatus == Active",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAccountIdentifiersByAccountId", 
        "args":"{\"accountId\":\"${__accountId__}\"}", 
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2", 
        "apiName":"iss.searchCustomers", 
        #"args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
        "args": "{\"includeDeactivatedCustomers\": false,\"marketplaceId\": \"ATVPDKIKX0DER\",\"pageSize\": 10,\"query\": {\"terms\": [{\"field_\": \"CustomerId\",\"phonetic\": false,\"prefix\": false,\"value_\": \"${__CustomerIdType__}\"}]}}",
        "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=accountId:accountId_,regionCode:regionCode_,CustomerIdType:CustomerIdType",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAlternateContacts",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2", 
        "apiName":"kumoscp.getTags",
        "args":"{\"resourceIds\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=globalAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"moduAWS", 
        "apiName":"cnAccountStatus.filterResults", 
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId,regionCode_:cn-north-1,accountStatus:accountStatus",
        "conditions":"accountStatus == Not Found",
        "limit":"",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"cnAccountStatus.combineResultsAsList",
        "args":"",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=regionCode_:cn-north-1;combineWith=cnAccountStatus.filterResults;asValues=accountIds:accountId_;chunkSize=50",
        "conditions":"",
        "limit":"",
        "pt":"1x1"
       },
      { 
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=cnAccountStatus.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"8x8"
        },
      { 
        "platform":"k2",
        "apiName":"avs.getSupportLevel", 
        "args":"{\"accountIds\":${__accountIds__}}",
        "inputs":"sourceApiName=cnAccountStatus.combineResultsAsList;targetValues=accountIds:accountIds_list,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"4x8"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAccountIdentifiersByAccountId", 
        "args":"{\"accountId\":\"${__accountId__}\"}", 
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"4x1"
        },
      {
        "platform":"moduAWS", 
        "apiName":"cnCustomerId.filterResults", 
        "args":"",
        "inputs":"sourceApiName=awsadms.getAccountIdentifiersByAccountId;targetValues=accountId_:accountId,regionCode_:regionCode,CustomerIdType:CustomerIdType",
        "conditions":"regionCode == cn-north-1",
        "limit":"",
        "pt":"1x8"
        },
      {
        "platform":"k2", 
        "apiName":"iss.searchCustomers", 
        #"args":"{\"query\":{\"terms\":[{\"field_\":\"CustomerAccountPoolId\",\"value_\":\"5827011\",\"prefix\":false,\"phonetic\":false},{\"field_\":\"CustomerId\",\"value_\":\"${__CustomerIdType__}\",\"prefix\":false,\"phonetic\":false}]},\"includeDeactivatedCustomers\":false,\"pageSize\":10}",
        "args": "{\"includeDeactivatedCustomers\": false,\"marketplaceId\": \"AAHKV2X7AFYLW\",\"pageSize\": 10,\"query\": {\"terms\": [{\"field_\": \"CustomerId\",\"phonetic\": false,\"prefix\": false,\"value_\": \"${__CustomerIdType__}\"}]}}",
        "inputs":"sourceApiName=cnCustomerId.filterResults;targetValues=accountId:accountId,regionCode:regionCode,CustomerIdType:CustomerIdType",
        "limit":"",
        "pt":"4x8"
        },
      {
        "platform":"k2", 
        "apiName":"awsadms.getAlternateContacts",
        "args":"{\"accountId\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"4x1"
        },
      {
        "platform":"k2", 
        "apiName":"#kumoscp.getTags",
        "args":"{\"resourceIds\":\"${__accountId__}\"}",
        "inputs":"sourceApiName=cnAccountStatus.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "limit":"",
        "pt":"4x1"
        }
      ]
    }, # end: Template Items,
  
  
  # begin: Template Items
  "[ent] RDS Status" : {
    "meta" : {
      "reportName": "get RDS Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"4",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
        "apiName":"rds.describeDBInstances",
        "args":"",
        "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__dBInstanceArn__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceArn:dBInstanceArn",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeRDSInstance",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/rds/;csvFilename=cdo-rds-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items

  # begin: Template Items
  "[ent] EC2 Network Interface status" : {
    "meta" : {
      "reportName": "get RDS Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
        { 
          "platform":"k2",
          "apiName":"avs.getAccountStatus",
          "args":"{\"accountIds\":[\"${__accountId__}\"]}",
          "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
          "conditions":"accountStatus == Active",
          "limit":"",
          "pt":"12x8"
          },
        {
          "platform":"k2",
          "apiName":"ec2.describeRegions",
          "args":"",
          "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
          "conditions":"",
          "limit":"1",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"modu.combineResults",
          "args":"",
          "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"32x8"
          },
        {
          "platform":"k2",
          "apiName":"ec2.describeNetworkInterfaces",
          "args":"",
          "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=association,attachment,privateIpAddresses",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
      ]
    }, # end: Template Items

  # begin: Template Items
  "[ent] RDS Status v2" : {
    "meta" : {
      "reportName": "get RDS Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
      {
        "platform":"k2",
        "apiName":"rds.describeDBInstances",
        "args":"",
        "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__dBInstanceArn__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceArn:dBInstanceArn",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[ent] EKS/ECS Status" : {
    "meta" : {
      "reportName": "get RDS Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__endpointName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:arnV2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listContainerInstances",
         "args":"",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeContainerInstances",
         "args":"{\"containerInstances\":\"${__containerInstances__}\"}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,containerInstances:containerInstances",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listTaskDefinitions",
         "args":"",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.describeTaskDefinition",
         "args":"{\"taskDefinition\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.listTaskDefinitions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:result;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"eks.listNodegroups",
         "args":"{\"clusterName\":\"${__clusterName__}\"}",
         "inputs":"sourceApiName=eks.describeCluster;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:name",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"eks.describeNodegroup",
         "args":"{\"clusterName\":\"${__clusterName__}\",\"nodegroupName\":\"${__nodegroupName__}\"}",
         "inputs":"sourceApiName=eks.listNodegroups;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:clusterName,nodegroupName:result",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        {"platform":"k2",
         "apiName":"eks.listClusters",
         "args":"",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"eks.describeClusters",
         "args":"{\"name\":\"${__name__}\"}",
         "inputs":"sourceApiName=eks.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,name:result",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"eks.listNodegroups",
         "args":"{\"clusterName\":\"${__clusterName__}\"}",
         "inputs":"sourceApiName=eks.describeCluster;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:name",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"eks.describeNodegroup",
         "args":"{\"clusterName\":\"${__clusterName__}\",\"nodegroupName\":\"${__nodegroupName__}\"}",
         "inputs":"sourceApiName=eks.listNodegroups;targetValues=accountId:accountId_,regionCode:regionCode_,clusterName:clusterName,nodegroupName:result",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[ent] OpenSearch Status" : {
    "meta" : {
      "reportName": "get RDS Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"1x16"
        },
      {
        "platform":"k2",
        "apiName":"es.listDomainNames",
        "args":"",
        "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_",
        "conditions":"",
        "limit":"",
        "pt":"16x8"
        },
        {"platform":"k2",
         "apiName":"es.describeElasticsearchDomain",
         "args":"{\"domainName\":\"${__domainName__}\"}",
         "inputs":"sourceApiName=es.listDomainNames;targetValues=accountId:accountId_,regionCode:regionCode_,domainName:domainName",
         "conditions":"",
         "limit":"",
         "pt":"16x8"
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[ent] Health Events - all" : {
    "meta" : {
      "reportName": "get AWS Health Events Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
        {"platform":"k2",
         "apiName":"health.describeEvents",
         "args":"{}",
         "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
         "conditions":"",
         "limit":"64",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"health.describeEventDetails",
         "args":"{\"eventArns\":[\"${__endpointName__}\"],\"locale\":\"en\"}",
         "inputs":"sourceApiName=health.describeEvents;targetValues=accountId:accountId_,regionCode:us-east-1,endpointName:arn;primaryKeys=event,eventDescription",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[ent] Health Events - open+upcoming" : {
    "meta" : {
      "reportName": "get AWS Health Events Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
        {"platform":"k2",
         "apiName":"health.describeEvents",
         "args":"{\"filter\":{\"eventStatusCodes\":[\"open\",\"upcoming\"]}}",
         "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
         "conditions":"",
         "limit":"64",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"health.describeEventDetails",
         "args":"{\"eventArns\":[\"${__endpointName__}\"],\"locale\":\"en\"}",
         "inputs":"sourceApiName=health.describeEvents;targetValues=accountId:accountId_,regionCode:us-east-1,endpointName:arn;primaryKeys=event,eventDescription",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  # begin: Template Items
  "[ent] Service Quotas" : {
    "meta" : {
      "reportName": "get AWS Service Quotas Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"1",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
        {
          "platform":"k2",
           "apiName":"servicequotas.listServices",
           "args":"",
           "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=services",
           "conditions":"",
           "limit":"",
           "pt":"8x8"
          },
        {
          "platform":"k2",
          "apiName":"servicequotas.listAWSDefaultServiceQuotas",
          "args":'{"serviceCode":"${__serviceCode__}"}',
          "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;primaryKeys=quotas",
          "conditions":"",
          "limit":"1",
          "pt":"16x8"
         },
        {"platform":"k2",
         "apiName":"servicequotas.getServiceQuota",
         "args":"{\"serviceCode\":\"${__serviceCode__}\",\"quotaCode\":\"${__quotaCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listAWSDefaultServiceQuotas;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode,quotaCode:quotaCode",
         "conditions":"",
         "limit":"1",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"servicequotas.listRequestedServiceQuotaChangeHistory",
         "args":"{\"serviceCode\":\"${__serviceCode__}\"}",
         "inputs":"sourceApiName=servicequotas.listServices;targetValues=accountId:accountId_,regionCode:regionCode_,serviceCode:serviceCode;nocsv",
         "conditions":"",
         "limit":"1",
         "pt":"8x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":'',
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items
    # begin: Template Items
  "[ent] Resource Status - k2 only" : {
    "meta" : {
      "reportName": "get S3 Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
      { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
        "platform":"k2",
        "apiName":"avs.getAccountStatus",
        "args":"{\"accountIds\":[\"${__accountId__}\"]}",
        "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
        "conditions":"accountStatus == Active",
        "limit":"4",
        "pt":"12x8"
        },
      {
        "platform":"k2",
        "apiName":"ec2.describeRegions",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
        "conditions":"",
        "limit":"1",
        "pt":"1x1"
        },
      {
        "platform":"moduAWS",
        "apiName":"modu.combineResults",
        "args":"",
        "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_;combineWith=ec2.describeRegions;asValues=regionCode_:regionName;nocsv",
        "conditions":"",
        "limit":"",
        "pt":"32x8"
        },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/Usage\",\"maxResults\":500}",
         "inputs":"sourceApiName=modu.combineResults;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,dimensions:dimensions;period=3600;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[ent] Trusted Advisor - k2" : {
    "meta" : {
      "reportName": "[ent] Trusted Advisor - k2",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"customerDomainName=nike.com",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.searchCustomers",
          "args":"{\"searchFilter\":\"WEB_DOMAIN\",\"searchFilterValue\":\"${__customerDomainName__}\",\"requestedBy\":\"K2account-details\"}",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=customerDomainName:customerDomainName;nocsv",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"k2",
          "apiName":"kumoscp.getCustomerAccountFullList",
          "args":"{\"id\":\"${__id__}\"}",
          "inputs":"sourceApiName=kumoscp.searchCustomers;targetValues=id:id;nocsv",
          "conditions":"status == Active",
          "limit":"",
          "pt":""
          },
        { #{"region":"us-east-1","accountId":"982499846871","args":{"accountIds":["982499846871"]},"apiName":"avs.getAccountStatus","sessionMetadata":{"segment":"asgard_workbench","instance_id":"9c6ffc42-2f31-47b4-9100-63be727cb24e-2","name":"ta"}}
          "platform":"k2",
          "apiName":"avs.getAccountStatus",
          "args":"{\"accountIds\":[\"${__accountId__}\"]}",
          "inputs":"sourceApiName=kumoscp.getCustomerAccountFullList;targetValues=accountId:accountId,regionCode:us-east-1;nocsv",
          "conditions":"accountStatus == Active",
          "limit":"4",
          "pt":"12x8"
          },
          { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"language":"en"},"apiName":"trustedadvisor.describeTrustedAdvisorChecks","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
            "platform":"k2",
           "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
           "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"language\":\"en\"}",
           "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
           "conditions":"",
           "limit":"1",
           "pt":"1x1"
           },
          {"platform":"moduAWS",
           "apiName":"modu.combineResultsAsList",
           "args":"",
           "inputs":"sourceApiName=avs.getAccountStatus;targetValues=accountId_:accountId_,regionCode:regionCode_;combineWith=trustedadvisor.describeTrustedAdvisorChecks;asValues=checkIds:id;nocsv",
           "conditions":"",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"k2",
           "apiName":"#trustedadvisor.refreshCheck",
           "args":"",
           "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
           "conditions":"",
           "limit":"",
           "pt":""
           },
          { #{"region":"us-east-1","accountId":"982499846871","args":{"accountInfo":{"accountId":"982499846871"},"checkIds":["Qch7DwouX1"]},"apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries","sessionMetadata":{"segment":"asgard_workbench","instance_id":"387c4685-251f-4751-ad30-17728c7e64df-2","name":"ta"}}
            "platform":"k2",
           "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
           "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkIds\":${__checkIds__}}",
           "inputs":"sourceApiName=modu.combineResultsAsList;targetValues=accountId:accountId_,regionCode:regionCode_,checkIds:checkIds_list;primaryKeys=resourcesSummary,categorySpecificSummary",
           "conditions":"",
           "limit":"",
           "pt":"8x8"
           },
          {"platform":"k2",
           "apiName":"trustedadvisor.describeCheckItems",
           "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__checkId__}\",\"count\":100,\"start\":0}",
           "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
           "conditions":"totalCount > 0",
           "limit":"",
           "pt":"8x8"
           },
          {"platform":"moduAWS",
           "apiName":"modu.joinResults",
           "args":"",
           "inputs":"sourceApiName=trustedadvisor.describeCheckItems;targetValues=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;targetColumns=accountId_:accountId_,regionCode_:region,status:status,properties:properties,checkId:checkId;joinWith=trustedadvisor.describeTrustedAdvisorChecks;indexKeys=checkId:id;joinValues=category:category,name:name",
           "conditions":"",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"security.filterResults",
           "args":"",
           "inputs":"sourceApiName=modu.joinResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,status:status,properties:properties,checkId:checkId,category:category,name:name;primaryKeys=properties",
           "conditions":"category == security",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"tolerance.filterResults",
           "args":"",
           "inputs":"sourceApiName=modu.joinResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,status:status,properties:properties,checkId:checkId,category:category,name:name;primaryKeys=properties",
           "conditions":"category == fault_tolerance",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"performance.filterResults",
           "args":"",
           "inputs":"sourceApiName=modu.joinResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,status:status,properties:properties,checkId:checkId,category:category,name:name;primaryKeys=properties",
           "conditions":"category == performance",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"limits.filterResults",
           "args":"",
           "inputs":"sourceApiName=modu.joinResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,status:status,properties:properties,checkId:checkId,category:category,name:name;primaryKeys=properties",
           "conditions":"category == service_limits",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"cost.filterResults",
           "args":"",
           "inputs":"sourceApiName=modu.joinResults;targetValues=accountId_:accountId_,regionCode_:regionCode_,status:status,properties:properties,checkId:checkId,category:category,name:name;primaryKeys=properties",
           "conditions":"category == cost_optimizing",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"moduAWS",
           "apiName":"redshift.filterResults",
           "args":"",
           "inputs":"sourceApiName=cost.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,checkId:checkId",
           "conditions":"checkId == G31sQ1E9U",
           "limit":"",
           "pt":"32x8"
           },
          {"platform":"k2",
           "apiName":"#redshift.describeClusters",
           "args":"",
           "inputs":"sourceApiName=redshift.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_",
           "conditions":"",
           "limit":"",
           "pt":""
           },
          {"platform":"moduAWS",
           "apiName":"#modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources",
           "args":"",
           "inputs":"addAccountDetails=yes",
           "conditions":"",
           "limit":"",
           "pt":""
           },
          {"platform":"moduAWS",
           "apiName":"#modu.uploadCsvResultToS3",
           "args":"",
           "inputs":"sourceApiName=modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ta/;csvFilename=cdo-ta-${{SNAPSHOT_DATE}}.csv",
           "conditions":"",
           "limit":"",
           "pt":""
           },
          {"platform":"moduAWS",
           "apiName":"#modu.uploadResultsToS3",
           "args":"",
           "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
           "conditions":"",
           "limit":"",
           "pt":""
           },
      ]
    }, # end: Template Items#
  "[campaign] Redshift Automated Snapshot excluding Advertising" : {
    "meta" : {
      "reportName": "* Time sensitive * Billing changes to Redshift backup charges (${__fleetName__})",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
It has been brought to our attention that your account has new charges related to use of Automated Redshift System Backups, this due to Redshift charging for system backups (snapshots) over one day old starting on May 1st, 2021. An email was sent to the system account email and posted to the account’s Personal Health Dashboards (PHD) on or around March 4, 2021 with this information. We are sending this note to account owners to ensure you, or a team member with access to this account, takes action to review and modify your Redshift automated system account backups to ensure you have minimal unexpected costs for their use.
<br><br>
Timeline: Billing for these started May 1, these backups will be charged at default discount 65% of S3 the public pricing, this can be a significant cost. The Redshift team is in the process of requesting a credit for May charges.  It is requested that you or a team member immediately reviews your Redshift Automated Redshift system backups and adjust it to a level acceptable for your Amazon business needs. Anything more than 1 day will be charged. You should update your budgets and estimate your ongoing costs related to the system backups at the default discount rate of 65% for AWS products . Our teams are looking to update this to S3 pricing when possible. Current IMR can be found here: <a href='https://w.amazon.com/bin/view/IMR/2021_IMR_Rate_Card/'>https://w.amazon.com/bin/view/IMR/2021_IMR_Rate_Card/</a>. 
<br><br>
It is recommended that you reduce your automated Redshift system costs to use the free 1 day retention and then augment it with a manual snapshot schedule. 
<br><br>
Please see additional information below. 1) Frequently Asked Questions (FAQ) 2) Your affected resources.
<br><br>
Please reach out to <a href='https://w.amazon.com/bin/view/Plus/tams/TAAS'>Plus TAM team<a>, if you have any additional questions. 
<br><br>
<br> 
Thank you for your prompt attention to this notice.
<br><br>
Sincerely,<br>
AWS Enterprise Support - <a href='https://w.amazon.com/bin/view/Plus/tamsver2'>PlusTAM team</a><br>
and Redshift Team<br>
<br><br>
<b>[Appendix]</b>
<br>
<b>1) Internal Wiki with information and FAQ’s :</b> 
<ul>
  <li><a href='https://w.amazon.com/bin/view/Redshift_System_SnapshotBilling/'>https://w.amazon.com/bin/view/Redshift_System_SnapshotBilling/</a></li>
</ul>
<br>
<b>2) Affected Resource List(${__affectedResourceCount__}):</b>
${__resourceListTable__}
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Redshift;sourceMedia=local;addAccountDetails=yes;nocsv",
         "conditions":"f3!=Advertising",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"automatedSnapshotRetentionPeriod>1",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=PercentageDiskSpaceUsed;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRedshiftCluster;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,clusterIdentifier,nodeType,numberOfNodes,automatedSnapshotRetentionPeriod,PercentageDiskSpaceUsed:maximum,fleetName;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong,baluluka;bccAliasIds=;dryRun=True;",#
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#  # begin: Template Items
  # begin: Template Items
  "[campaign] Redshift Automated Snapshot for Advertising" : {
    "meta" : {
      "reportName": "* Time sensitive * Billing changes to Redshift backup charges (${__fleetName__})",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
It has been brought to our attention that your account has new charges related to use of Automated Redshift System Backups, this due to Redshift charging for system backups (snapshots) over one day old starting on May 1st, 2021. An email was sent to the system account email and posted to the account’s Personal Health Dashboards (PHD) on or around March 4, 2021 with this information. We are sending this note to account owners to ensure you, or a team member with access to this account, takes action to review and modify your Redshift automated system account backups to ensure you have minimal unexpected costs for their use.
<br><br>
Timeline: Billing for these started May 1, these backups will be charged at default discount 65% of S3 the public pricing, this can be a significant cost. The Redshift team is in the process of requesting a credit for May charges.  It is requested that you or a team member immediately reviews your Redshift Automated Redshift system backups and adjust it to a level acceptable for your Amazon business needs. Anything more than 1 day will be charged. You should update your budgets and estimate your ongoing costs related to the system backups at the default discount rate of 65% for AWS products . Our teams are looking to update this to S3 pricing when possible. Current IMR can be found here: <a href='https://w.amazon.com/bin/view/IMR/2021_IMR_Rate_Card/'>https://w.amazon.com/bin/view/IMR/2021_IMR_Rate_Card/</a>. 
<br><br>
It is recommended that you reduce your automated Redshift system costs to use the free 1 day retention and then augment it with a manual snapshot schedule. 
<br><br>
Please see additional information below. 1) Frequently Asked Questions (FAQ) 2) Your affected resources.
<br><br>
Please reach out to <a href='https://w.amazon.com/bin/view/Plus/tams/TAAS'>Plus TAM team<a>, if you have any additional questions. 
<br><br>
<br> 
Thank you for your prompt attention to this notice.
<br><br>
Sincerely,<br>
AWS Enterprise Support - <a href='https://w.amazon.com/bin/view/Plus/tamsver2'>PlusTAM team</a><br>
and Redshift Team<br>
<br><br>
<b>[Appendix]</b>
<br>
<b>1) Internal Wiki with information and FAQ’s :</b> 
<ul>
  <li><a href='https://w.amazon.com/bin/view/Redshift_System_SnapshotBilling/'>https://w.amazon.com/bin/view/Redshift_System_SnapshotBilling/</a></li>
</ul>
<br>
<b>2) Affected Resource List(${__affectedResourceCount__}):</b>
${__resourceListTable__}
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Redshift;sourceMedia=local;addAccountDetails=yes;nocsv",
         "conditions":"f3==Advertising",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"automatedSnapshotRetentionPeriod>1",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=PercentageDiskSpaceUsed;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRedshiftCluster;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,clusterIdentifier,nodeType,numberOfNodes,automatedSnapshotRetentionPeriod,PercentageDiskSpaceUsed:maximum,fleetName;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=aws-plus-ads-tams,baluluka;bccAliasIds=;dryRun=True;",#
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] Redshift - End of Support for DS2 Nodes" : {
    "meta" : {
      "reportName": "**Action Required** your DS2 Redshift End-of-Life date is approaching [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using DS2 Redshift Nodes which will be ended the support of your <b>${__affectedResourceCount__} Redshift Clusters</b> by Dec. 31, 2021 and notified you via <a href='https://phd.aws.amazon.com/phd/home#/dashboard/open-issues'>AWS Personal Health Dashboard</a>.<br>
<br>
<u><b>1) After the August 1, 2021</b></u>,<br>
New DS2 clusters cannot be created.
<br>
<u><b>2) After the Dec. 31, 2021 deadline</b></u>,<br>
DS2 node type will be deprecated which means your DS2 Redshift cluster will be upgraded to RA3 immediately to prevent any availability risk.
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href=''>Announcement: Amazon Redshift DS2 Node Deprecation is December 31, 2021</a></li>
  <li><a href='https://aws.amazon.com/blogs/big-data/simplify-amazon-redshift-ra3-migration-evaluation-with-simple-replay-utility/'>Simplify Amazon Redshift RA3 migration evaluation with Simple Replay utility</a></li>
</ul>
Please, create a support request at your AWS Console if you need to have an exception for the mandatory upgrade. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
Sincerely,<br>
AWS Enterprise Support - <a href='https://w.amazon.com/bin/view/Plus/tamsver2'>PlusTAM team</a><br>
AWS Redshift team<br>
<br><br>
<b>[Appendix]</b>
<br>
<b>1) Internal Wiki with information and FAQ’s :</b> 
<ul>
  <li><a href='https://quip-amazon.com/KdIDA45EeR3r/DS2-Deprecation-E2M-Notice-Internal-FAQ'>DS2 Deprecation Internal FAQ</a></li>
</ul>
<br>
<b>2) Affected Resource List(${__affectedResourceCount__}):</b>
${__resourceListTable__}
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Redshift;sourceMedia=local;addAccountDetails=yes;nocsv",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeReservedNodes",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"ds2.8xlarge,ds2.xlarge in nodeType",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"ds2.8xlarge,ds2.xlarge in nodeType",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRedshiftCluster;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,clusterIdentifier,nodeType,numberOfNodes,clusterStatus,clusterCreateDate,$maxSaving-Mo,nextAction,reasons,$riMo,$odMo,fleetName;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=;bccAliasIds=;dryRun=True;",#
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] DynamoDB - Low Utilized Tables for WWOps/Global Customer Fulfillment": {
    "meta" : {
      "reportName": "Identified savings of ${__12x_affectedTotalCost__} with Low Utilized DynamoDB Tables [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We have identified an opportunity for you to save <b>${__12x_affectedTotalCost__}</b> on your IMR in 2021.<br>
<br>
<b>Description</b><br>
We identified ${__affectedResourceCount__} DynamoDB tables with low utilization. These tables are currently configured with provisioned capacity greater than the actual usage, resulting in IMR overspend. See below for details regarding these DynamoDB tables.<br>
<br> 
<b>Recommendation</b><br>
We recommend enabling On-Demand billing on these table(s). DynamoDB On-Demand mode eliminates the need provision capacity for your table(s). Enabling DynamoDB On-Demand may reduce your IMR spend by ${__12x_affectedTotalCost__} annually.<br>
<br>
<b>Next Steps</b><br>
1. Review your DynamoDB utilization using <a href='https://dynamite.a2z.com/'>Dynamite</a>,<br>
2. Enable On-Demand Billing or terminate the tables.<br>
3. Please <a href='https://w.amazon.com/bin/view/Dynamite/#HOnboarding'>be onboard</a> if your tables aren't listed at <a href='https://dynamite.a2z.com/'>Dynamite</a>.<br>
<br>
If you need assistance, please create an AWS Support case via the AWS Console. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
Regards,<br>
AWS <b><a href='https://w.amazon.com/bin/view/Plus/tamsver2'>Plus TAM</a> Team<br>
<br>
<b>Appendix</b><br>
<b>==========</b><br>
<b>1. References</b>
<ul>
  <li><a href='https://aws.amazon.com/dynamodb/pricing/on-demand/'>Pricing for On-Demand Capacity</a></li>
  <li><a href='https://w.amazon.com/bin/view/DynamoDB_Operational_Best_Practices/'>DynamoDB Operational Best Practices</a>
  <li><a href=‘https://w.amazon.com/bin/view/Dynamite/’>Dynamite for DynamoDB</a></li>
  <li><a href=‘https://w.amazon.com/bin/view/Dynamite/dynamite.sh/’>an automated script (dynamite.sh)</a></li>
</ul>
<b>2. Your low utilized DynamoDB Tables:(${__affectedResourceCount__})</b><br>
${__resourceListTable__}<br>

* <b>Total Saving: <span style="color:red;">${__12x_affectedTotalCost__}</span> in 2021</b><br>
* $Mo < $10 DynamoDB Table isn't listed.<br>
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#ddb.setTargetValues",
         "args":"",
         "inputs":"nocsv;regionCode_=us-east-1;accountId_=280901691416,173206762502,360444127360,173483361843,878562893896,902582620794,515249113066,336259967879,236216371265,461525128025,659070613934,122604242384,002047392432,849606575134,161310111677,162951011619,071526322190,825226713482,735472006622,962021230618,356266878646,930680387489,697753815799,028788164335,142987347922,576205862611,251318452219,112297545575,726709536928,269083589084,334239440173,645375960424,722879468497",
         "conditions":"",
         "limit":"",
         "pt":""
         },     
        {"platform":"k2",
         "apiName":"#dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=ddb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         }, 
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"orgName=Global Customer Fulfillment;targetValues=accountId:accountId_;serviceName=DynamoDB;searchCondition=match",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,billingMode:billingMode,tableName:tableName,indexName:indexName",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"dynamicAutoScaling->On-Demand,fixedAutoScaling->On-Demand,provisionedCapacity->On-Demand,terminate in nextAction",
         "limit":"",
         "pt":""
         },
        {
         "platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBTables;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,tableName,indexName,itemCount,$maxSaving-Mo,nextAction,reasons,$monthlyCost,fleetName;costColumnName=$maxSaving-Mo;minResourceCost=10;minTotalCost=1000;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
      ]
    }, # end: Template Items#  # begin: Template Items
    "[campaign] DynamoDB - Low Utilized Tables for top 20 owners in CDO": {
    "meta" : {
      "reportName": "Identified savings of ${__12x_affectedTotalCost__} with Low Utilized DynamoDB Tables [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We have identified an opportunity for you to save <b>${__12x_affectedTotalCost__}</b> on your IMR in 2021.<br>
<br>
<b>Description</b><br>
We identified ${__affectedResourceCount__} DynamoDB tables with low utilization. These tables are currently configured with provisioned capacity greater than the actual usage, resulting in IMR overspend. See below for details regarding these DynamoDB tables.<br>
<br> 
<b>Recommendation</b><br>
We recommend enabling On-Demand billing on these table(s). DynamoDB On-Demand mode eliminates the need provision capacity for your table(s). Enabling DynamoDB On-Demand may reduce your IMR spend by ${__12x_affectedTotalCost__} annually.<br>
<br>
<b>Next Steps</b><br>
1. Review your DynamoDB utilization using <a href='https://dynamite.a2z.com/'>Dynamite</a>,<br>
2. Enable On-Demand Billing or terminate the tables.<br>
3. Please <a href='https://w.amazon.com/bin/view/Dynamite/#HOnboarding'>be onboard</a> if your tables aren't listed at <a href='https://dynamite.a2z.com/'>Dynamite</a>.<br>
<br>
If you need assistance, please create an AWS Support case via the AWS Console. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
Regards,<br>
AWS <b><a href='https://w.amazon.com/bin/view/Plus/tamsver2'>Plus TAM</a> Team<br>
<br>
<b>Appendix</b><br>
<b>==========</b><br>
<b>1. References</b>
<ul>
  <li><a href='https://aws.amazon.com/dynamodb/pricing/on-demand/'>Pricing for On-Demand Capacity</a></li>
  <li><a href='https://w.amazon.com/bin/view/DynamoDB_Operational_Best_Practices/'>DynamoDB Operational Best Practices</a>
  <li><a href=‘https://w.amazon.com/bin/view/Dynamite/’>Dynamite for DynamoDB</a></li>
  <li><a href=‘https://w.amazon.com/bin/view/Dynamite/dynamite.sh/’>an automated script (dynamite.sh)</a></li>
</ul>
<b>2. Your low utilized DynamoDB Tables:(${__affectedResourceCount__})</b><br>
${__resourceListTable__}<br>

* <b>Total Saving: <span style="color:red;">${__12x_affectedTotalCost__}</span> in 2021</b><br>
* $Mo < $10 DynamoDB Table isn't listed.<br>
"""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#ddb.setTargetValues",
         "args":"",
         "inputs":"nocsv;regionCode_=us-east-1;accountId_=280901691416,173206762502,360444127360,173483361843,878562893896,902582620794,515249113066,336259967879,236216371265,461525128025,659070613934,122604242384,002047392432,849606575134,161310111677,162951011619,071526322190,825226713482,735472006622,962021230618,356266878646,930680387489,697753815799,028788164335,142987347922,576205862611,251318452219,112297545575,726709536928,269083589084,334239440173,645375960424,722879468497",
         "conditions":"",
         "limit":"",
         "pt":""
         },     
        {"platform":"k2",
         "apiName":"#dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=ddb.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         }, 
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"targetValues=accountId:accountId_;serviceName=DynamoDB;searchCondition=match",
         "conditions":"bansag,mitupa,alekseyd,robbgilm,jaamourr,shutekas,vinagarg,mathurs,wulffjw,rengasar,easonliu,anjaney,mukeshb,adamstev,divyasn,jdr,pavneet,tomarere,kiranpe,bdog in masterOwnerAliasId",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,billingMode:billingMode,tableName:tableName,indexName:indexName",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"dynamicAutoScaling->On-Demand,fixedAutoScaling->On-Demand,provisionedCapacity->On-Demand,terminate in nextAction",
         "limit":"",
         "pt":""
         },
        {
         "platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBTables;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,tableName,indexName,itemCount,$maxSaving-Mo,nextAction,reasons,$monthlyCost,fleetName;costColumnName=$maxSaving-Mo;minResourceCost=10;minTotalCost=1000;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
      ]
    }, # end: Template Items#  # begin: Template Items
  # begin: Template Items
  "[campaign] S3 Incomplete Multi-Part Uploads": {
    "meta" : {
      "reportName": "saving ${__12x_affectedTotalCost__} with S3 Incomplete Multi-Part Uploads (${__snapshotDate__})",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We identified a number of S3 incomplete multipart uploads which present an opportunity to save <b>${__12x_affectedTotalCost__}</b> in S3 storage costs. (If you have already set the lifecycle policy for the S3 Buckets, you can ignore this notification.) <br>
<br>
We recognize your team has a number of S3 incomplete multipart uploads that haven't been uploaded to S3 fully and could be cleaned up to save S3 storage costs.<br>
<br> 
When a multipart upload fails to complete (for example if the upload process is killed or an instance is terminated), the individual parts are kept until the upload is manually aborted or completed. These parts are not visible in the console or the normal S3 list commands, but they do accrue storage charges and over time the accumulated storage (and costs) can be fairly high.<br>
<br>
The incomplete uploads can be listed using the AWS CLI ‘s3api list-multipart-uploads’ [1] command, and it is worth investigating some of the recent incomplete uploads to ensure there are no problems in the systems responsible for performing uploads. After this you can add a lifecycle policy [2] to abort incomplete uploads in that bucket. This lifecycle policy will delete the old uploads and prevent future incomplete uploads from accumulating. Jeff Barr’s blog [3] has some screenshots showing how to do this through the console a it can also be done programmatically. See this [4] non-AWS blog post for some examples. Below is the list of buckets with incomplete uploads, the MPU Size column is the total size of incomplete multipart uploads that have been in that bucket for more than 7 days.<br>
<br>
[1] http://docs.aws.amazon.com/cli/latest/reference/s3api/list-multipart-uploads.html<br>
[2] http://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config<br>
[3] https://aws.amazon.com/blogs/aws/s3-lifecycle-management-update-support-for-multipart-uploads-and-delete-markers/<br>
[4] http://www.deplication.net/2016/06/aws-tip-save-s3-costs-with-abort.html<br>
<br>
If you create a support request at your AWS Console that AWS Support can help you get the paths to green. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>) Or, you can reach out to <a href='https://w.amazon.com/bin/view/Plus/tams/TAAS'>Plus TAM team<a>, if you have any additional questions. <br>
<br>
<b>Your affected S3 Buckets:(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
* <b>Total Saving: <span style="color:red;">${__12x_affectedTotalCost__}</span> in 2021</b><br>
* $Mo < $10 bucket isn't listed.<br>
<br>
Sincerely,<br>
AWS Enterprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a></b><br>
AWS Systems Manager<br>
"""
      },
    "apiList": [
        {
          "platform":"moduAWS",
          "apiName":"modu.analyzeS3Mpu",
          "args":"",
          "inputs":"#sourceMedia=remote;addAccountDetails=yes",
          "conditions":"f1==CDO",
          "groupBy":"",
          "orderBy":"",
          "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeS3Mpu;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,bucketName,mpuSize(GBytes),imr2021_MonthlyCost($),fleetName;costColumnName=imr2021_MonthlyCost($);minResourceCost=10;minTotalCost=100;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeS3Mpu;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/s3mpu/;csvFilename=cdo-s3-mpu-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
        {
         "platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
        },
      ]
    }, # end: Template Items#  # begin: Template Items
  # begin: Template Items
  "[campaign] Aurora/RDS - End of Support for Open Source Database Engines, MySQL v5.6/PostgrSQL v9.6.x" : {
    "meta" : {
      "reportName": "**Action Required** your RDS MySQL 5.6/PostgreSQL 9.6 End-of-Life date is approaching [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using Amazon RDS <a href='https://forums.aws.amazon.com/ann.jspa?annID=8498'>MySQL</a>/<a href='https://forums.aws.amazon.com/ann.jspa?annID=8499'>PostgreSQL</a> databases which will be ended the support of your <b>${__affectedResourceCount__} databases</b> by Aug. 3, 2021 and Jan. 18, 2022 which has already published on January 17, 2021 and notified you via <a href='https://phd.aws.amazon.com/phd/home#/dashboard/open-issues'>AWS Personal Health Dashboard</a>.<br>
<br>
<u>1) After <b>the Aug. 3, 2021 deadline for MySQL v5.6 or older versions</b></u>,<br>
<b>RDS will not provide any security updates and bug fixes</b> until your MySQL 5.6 databases to 5.7 or later versions. And, RDS will start upgrading your MySQL 5.6 databases to 5.7 by March 1st, 2022. Then, any Amazon RDS for MySQL 5.6 databases that remain will be upgraded to version 5.7 regardless of whether the instances are in a maintenance window or not.<br>
<br>
<u>2) After <b>the Jan. 18, 2021 deadline for Aurora/MySQL v9.6 or older versions</b></u>,<br>
<b>RDS will upgrade your PostgreSQL 9.6 databases to 12</b> during a scheduled maintenance window between January 18, 2022 00:00:01 UTC and February 22, 2022 00:00:01 UTC. On February 22, 2022 00:00:01 AM UTC, any PostgreSQL 9.6 databases that remain will be upgraded to version 12 regardless of whether the instances are in a maintenance window or not.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8175 (https://forums.aws.amazon.com/ann.jspa?annID=8498)'>*Announcement: Amazon Relational Database Service (RDS) for MySQL 5.6 End-of-Life date is August 3, 2021*</a></li>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8174 (https://forums.aws.amazon.com/ann.jspa?annID=8499)'>*Announcement: Amazon Relational Database Service (RDS) for PostgreSQL 9.6 End-of-Life date is January 18, 2022*</a></li>
  <li><a href='https://aws.amazon.com/premiumsupport/knowledge-center/notification-maintenance-rds-redshift/'>How do I configure notifications for Amazon RDS?</a></li>
  <li><a href='https://www.mysql.com/support/eol-notice.html'>[External] MySQL Product Support EOL Announcements</a></li>
  <li><a href='Versioning Policy'>[External] PostgreSQL Versioning Policy</a></li>
</ul>
Please, create a support request at your AWS Console if you need to have an exception for the mandatory upgrade. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a>
AWS RDS team<br>
""",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#rds.setTargetValues",
         "args":"",
         "inputs":"accountId_=657512166465,181228633593,713232703133,659247806949;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"",
         "limit":"",
         "pt":""
         },        
        {"platform":"k2",
         "apiName":"#rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"5.5.46,5.5.53,5.5.54,5.5.57,5.5.59,5.5.61,5.6.10a,5.6.19,5.6.34,5.6.35,5.6.37,5.6.39,5.6.40,5.6.41,5.6.44,5.6.51,5.6.mysql_aurora.1.19.5,5.6.mysql_aurora.1.19.6,5.6.mysql_aurora.1.22.0,5.6.mysql_aurora.1.22.1,5.6.mysql_aurora.1.22.1.3,5.6.mysql_aurora.1.22.2,5.6.mysql_aurora.1.22.3,5.6.mysql_aurora.1.22.3.1,5.6.mysql_aurora.1.22.4,5.6.mysql_aurora.1.22.5,5.6.mysql_aurora.1.23.0,5.6.mysql_aurora.1.23.1,5.6.mysql_aurora.1.23.2,5.6.mysql_aurora.1.23.3,9.3.25,9.4.25,9.5.15,9.5.24,9.6.1,9.6.10,9.6.11,9.6.12,9.6.14,9.6.15,9.6.16,9.6.17,9.6.18,9.6.19,9.6.2,9.6.20,9.6.21,9.6.22,9.6.3,9.6.5,9.6.6,9.6.8,9.6.9 in engineVersion",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=maws.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"5.5.46,5.5.53,5.5.54,5.5.57,5.5.59,5.5.61,5.6.10a,5.6.19,5.6.34,5.6.35,5.6.37,5.6.39,5.6.40,5.6.41,5.6.44,5.6.51,5.6.mysql_aurora.1.19.5,5.6.mysql_aurora.1.19.6,5.6.mysql_aurora.1.22.0,5.6.mysql_aurora.1.22.1,5.6.mysql_aurora.1.22.1.3,5.6.mysql_aurora.1.22.2,5.6.mysql_aurora.1.22.3,5.6.mysql_aurora.1.22.3.1,5.6.mysql_aurora.1.22.4,5.6.mysql_aurora.1.22.5,5.6.mysql_aurora.1.23.0,5.6.mysql_aurora.1.23.1,5.6.mysql_aurora.1.23.2,5.6.mysql_aurora.1.23.3,9.3.25,9.4.25,9.5.15,9.5.24,9.6.1,9.6.10,9.6.11,9.6.12,9.6.14,9.6.15,9.6.16,9.6.17,9.6.18,9.6.19,9.6.2,9.6.20,9.6.21,9.6.22,9.6.3,9.6.5,9.6.6,9.6.8,9.6.9 in engineVersion",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=RDS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"5.5.46,5.5.53,5.5.54,5.5.57,5.5.59,5.5.61,5.6.10a,5.6.19,5.6.34,5.6.35,5.6.37,5.6.39,5.6.40,5.6.41,5.6.44,5.6.51,5.6.mysql_aurora.1.19.5,5.6.mysql_aurora.1.19.6,5.6.mysql_aurora.1.22.0,5.6.mysql_aurora.1.22.1,5.6.mysql_aurora.1.22.1.3,5.6.mysql_aurora.1.22.2,5.6.mysql_aurora.1.22.3,5.6.mysql_aurora.1.22.3.1,5.6.mysql_aurora.1.22.4,5.6.mysql_aurora.1.22.5,5.6.mysql_aurora.1.23.0,5.6.mysql_aurora.1.23.1,5.6.mysql_aurora.1.23.2,5.6.mysql_aurora.1.23.3,9.3.25,9.4.25,9.5.15,9.5.24,9.6.1,9.6.10,9.6.11,9.6.12,9.6.14,9.6.15,9.6.16,9.6.17,9.6.18,9.6.19,9.6.2,9.6.20,9.6.21,9.6.22,9.6.3,9.6.5,9.6.6,9.6.8,9.6.9 in engineVersion",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBInstanceArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRDSInstance",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,instanceType,multiAZ,dBInstanceIdentifier,dbEngineVersion,endOfSupport,dBInstanceStatus,dBCreationDate,nextAction,reasons,$riMo,$odMo,MAWS-IIBS-Tag,Tags,fleetName,snapshotDate;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] Aurora/RDS - RDS Instances in EC2 Classic" : {
    "meta" : {
      "reportName": "**Action Required** your RDS Instances in EC2 Classic [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using Amazon RDS <a href='https://forums.aws.amazon.com/ann.jspa?annID=8498'>MySQL</a>/<a href='https://forums.aws.amazon.com/ann.jspa?annID=8499'>PostgreSQL</a> databases which will be ended the support of your <b>${__affectedResourceCount__} databases</b> by Aug. 3, 2021 and Jan. 18, 2022 which has already published on January 17, 2021 and notified you via <a href='https://phd.aws.amazon.com/phd/home#/dashboard/open-issues'>AWS Personal Health Dashboard</a>.<br>
<br>
<u>1) After <b>the Aug. 3, 2021 deadline for MySQL v5.6 or older versions</b></u>,<br>
<b>RDS will upgrade your MySQL 5.6 databases to 5.7</b> during a scheduled maintenance window between August 3, 2021 00:00:01 UTC and September 1, 2021 00:00:01 UTC. On September 1, 2021 00:00:01 AM UTC, any Amazon RDS for MySQL 5.6 databases that remain will be upgraded to version 5.7 regardless of whether the instances are in a maintenance window or not.<br>
<br>
<u>2) After <b>the Jan. 18, 2021 deadline for Aurora/MySQL v9.6 or older versions</b></u>,<br>
<b>RDS will upgrade your PostgreSQL 9.6 databases to 12</b> during a scheduled maintenance window between January 18, 2022 00:00:01 UTC and February 22, 2022 00:00:01 UTC. On February 22, 2022 00:00:01 AM UTC, any PostgreSQL 9.6 databases that remain will be upgraded to version 12 regardless of whether the instances are in a maintenance window or not.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8175 (https://forums.aws.amazon.com/ann.jspa?annID=8498)'>*Announcement: Amazon Relational Database Service (RDS) for MySQL 5.6 End-of-Life date is August 3, 2021*</a></li>
  <li><a href='https://forums.aws.amazon.com/ann.jspa?annID=8174 (https://forums.aws.amazon.com/ann.jspa?annID=8499)'>*Announcement: Amazon Relational Database Service (RDS) for PostgreSQL 9.6 End-of-Life date is January 18, 2022*</a></li>
  <li><a href='https://aws.amazon.com/premiumsupport/knowledge-center/notification-maintenance-rds-redshift/'>How do I configure notifications for Amazon RDS?</a></li>
  <li><a href='https://www.mysql.com/support/eol-notice.html'>[External] MySQL Product Support EOL Announcements</a></li>
  <li><a href='Versioning Policy'>[External] PostgreSQL Versioning Policy</a></li>
</ul>
Please, create a support request at your AWS Console if you need to have an exception for the mandatory upgrade. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a>
AWS RDS team<br>
""",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#rds.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,003428312939,015391222128,021339480998,021677843507,025159697747,028014450417,039579326863,050906944712,052243325673,055839978525,072279425524,089913812461,093665973544,099890080648,101159671626,104728609414,110504962622,125463133163,128568392217,131834524554,136679104205,141934393310,177021191313,177280384306,200402032998,209452008893,214415503121,217015164351,233735749897,236255665551,244835557479,259555524445,264938696210,277797598253,289497978546,294123255832,294537252295,301766397615,316843376260,317314025092,347901270313,349166505026,373298732609,380547507856,397725682905,403659734880,408663460106,413070407688,429258689555,452436046126,473421469635,473857715383,478037606772,479819860331,482221258154,483087092556,487512104228,501221294148,503270934557,521402426732,521479886834,527309466893,536673046002,540943074470,542245766645,555828831204,561983453283,568718707095,571559346954,571937906973,576101733904,579203837275,583669540242,587659417312,605677951100,606421911645,621662906823,624011181711,628244914102,641719893274,659247806949,701367514220,718423755097,731564964100,742910227504,749801920358,751849814575,769132067178,776467488489,779356323519,787347057677,793064538767,799849535758,802523254721,803054435725,852147364037,856818505970,874091887885,878993442419,883645059794,885124689389,890588025547,902219932398,923686165227,928261997191,938836420846,964273817557,978326523180,988584522751;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"",
         "limit":"",
         "pt":""
         },        
        {"platform":"k2",
         "apiName":"#rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"vpcId == \"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=maws.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"vpcId == \"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=RDS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"vpcId == \"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,instanceType,multiAZ,dBInstanceIdentifier,dbEngineVersion,endOfSupport,dBInstanceStatus,dBCreationDate,nextAction,reasons,$riMo,$odMo,MAWS-IIBS-Tag,Tags,fleetName,snapshotDate;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] End of Support for EC2 Classic Instances" : {
    "meta" : {
      "reportName": "**Action Required** your EC2 Classic Instances' End-of-Life date is approaching [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"7 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using <a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic Instances</a> which will be ended the support of your <b>${__affectedResourceCount__} EC2 Instances</b> by June. 30, 2022 which has to improve the security and the availability risk in CDO/Amazon.<br>
<br>
<u>After <b>the June. 30, 2022 deadline for the EC2 Classic Instances</b></u>,<b>EC2 will no longer allow the creation of new instances (Spot or on-demand) or other AWS services in the Classic environment which will cause availability risk at your services. So, EC2 strongly recommend you to migrate your AWS resources from EC2-Classic to VPC as soon as possible and then disable EC2-Classic on your account.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic</a></li>
  <li><a href='https://w.amazon.com/bin/view/AWS/PSE/CalendarofEvents/EC2ClassicMigration#HFAQs'>EC2 Classic Migration FAQ</a></li>
</ul>
Please, create a support request at your AWS Console if you need any assistance to migrate your EC2 Classic Instances into VPC. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a>
AWS EC2 team<br>
""",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#ec2.setTargetValues",
         "args":"",
         "inputs":"nocsv;regionCode_=us-east-1;accountId_=563885087084,404659798929,620308156200,177607377190,701676736223,249276804983,853636619763,252021269929,187971698213,380547507856,406034328191,025159697747,622677666763,727241348333,978416762848,576101733904,802523254721,347901270313,940668160067,167158389134,592277094468,055839978525,186229595854,100716527516,682408118152,546531427139,014373610015,236851578547,332750255191,402085449947,739957545881",
         "conditions":"",
         "limit":"",
         "pt":""
         },      
        {"platform":"moduAWS",
         "apiName":"#ec2.getDwEC2ClassicInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.setTargetValues;targetValues=accountId:accountId_;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },  
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=EC2;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.getDwEC2ClassicInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getDwEC2ClassicInstances;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state;addAccountDetails=yes",
         "conditions":"vpcId==None",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,instanceType,instanceId,launchDate,tags,name,launchedBy,launchGroup,fleetName,snapshotDate;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] Lambda - End of Support for Python 2.7" : {
    "meta" : {
      "reportName": "**Action Required** your Lambda Python 2.7 End-of-Life date is approaching [${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"7 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using <a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic Instances</a> which will be ended the support of your <b>${__affectedResourceCount__} EC2 Instances</b> by June. 30, 2022 which has to improve the security and the availability risk in CDO/Amazon.<br>
<br>
<u>After <b>the June. 30, 2022 deadline for the EC2 Classic Instances</b></u>,<b>EC2 will no longer allow the creation of new instances (Spot or on-demand) or other AWS services in the Classic environment which will cause availability risk at your services. So, EC2 strongly recommend you to migrate your AWS resources from EC2-Classic to VPC as soon as possible and then disable EC2-Classic on your account.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic</a></li>
  <li><a href='https://w.amazon.com/bin/view/AWS/PSE/CalendarofEvents/EC2ClassicMigration#HFAQs'>EC2 Classic Migration FAQ</a></li>
</ul>
Please, create a support request at your AWS Console if you need any assistance to migrate your EC2 Classic Instances into VPC. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a>
AWS EC2 team<br>
""",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"lambda.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Lambda;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listFunctions",
         "args":"",
         "inputs":"sourceApiName=lambda.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;addAccountDetails=yes",
         "conditions":"runtime==python2.7",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=lambda.listFunctions;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,functionName,runtime,lastModified,fleetName,snapshotDate;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[campaign] EMR - Deprecation of Bucket support.elasticmapreduce" : {
    "meta" : {
      "reportName": "**Action Required** your EMR Deprecation of S3 Bucket:'support.elasticmapreduce' date is approaching[${__fleetName__}]",
      "bcaDescription": "",
      "startTime":"7 days ago",
      "endTime":"now",
      "emailTemplate":"""Hi ${__firstName__},<br>
<br>
We're contacting you, because your team owns services that are using <a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic Instances</a> which will be ended the support of your <b>${__affectedResourceCount__} EC2 Instances</b> by June. 30, 2022 which has to improve the security and the availability risk in CDO/Amazon.<br>
<br>
<u>After <b>the June. 30, 2022 deadline for the EC2 Classic Instances</b></u>,<b>EC2 will no longer allow the creation of new instances (Spot or on-demand) or other AWS services in the Classic environment which will cause availability risk at your services. So, EC2 strongly recommend you to migrate your AWS resources from EC2-Classic to VPC as soon as possible and then disable EC2-Classic on your account.<br>
<br>
You can see the details at the followings:<br>
<ul>
  <li><a href='https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html'>EC2 Classic</a></li>
  <li><a href='https://w.amazon.com/bin/view/AWS/PSE/CalendarofEvents/EC2ClassicMigration#HFAQs'>EC2 Classic Migration FAQ</a></li>
</ul>
Please, create a support request at your AWS Console if you need any assistance to migrate your EC2 Classic Instances into VPC. (<a href='https://w.amazon.com/bin/view/Plusteam/Help/SupportCase#HHowtoOpenanAWSSupportCase'>Getting Started with AWS Support</a>)<br>
<br>
<b>Affected Resource List(${__affectedResourceCount__}):</b><br>
${__resourceListTable__}<br>
<br>
Sincerely,<br>
AWS Entereprise Support - <b><a href='https://w.amazon.com/bin/view/Plus/tams/'>PlusTAM</a>
AWS EC2 team<br>
""",
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#emr.setTargetValues",
         "args":"",
         "inputs":"accountId_=563885087084,671765535111,012681505764,255148740632,313143050470,932710724747,628833418668,773048889367,031892955173,240033045552,637042629487,595407731493,118034810511,497957719845,681685694812,828363953741,179968894747,535715087958,067221727829,731822897991,451270415408,863595899769,021732063925,733585711144,968192988180,878213685642,366186092921,903094584798,668189537597,455021090894,124494998611,903311481925,726997296112,555482640159,499080132385,723749258261,377105494970,196304153320,008441260763,942050825292,694813427473,004896155832,560668093439,197323679409,549447713466,505278613891,960177007924,552727262045,884441722776,099838986439,483139417296,413000313257,116819520513,603150879823,952474482550,094883567921,934181291337,395968227317,723494132027,007258654415,507786327009,395836225302,649037252677,261947573181,505389038679,629804172322,228051970027,263045624572,166409903884,644064922061,588445656595,618548148494,865471051061,771604386909,375937567384,720562049624,053147769819,548622725432,836196164208,008189486233,211479383440,750862500987,467545174150,764054885295,265373095845,323266665198,515853937990,952493666022,748762807827;regionCode_=us-east-1,us-west-2,eu-west-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         }, 
        {"platform":"k2",
         "apiName":"#emr.listClusters",
         "args":"",
         "inputs":"sourceApiName=emr.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"4x1"
         },
        {"platform":"moduAWS",
         "apiName":"emr.getRegions",
         "args":"",
         "inputs":"orgName=CDO;serviceName=Amazon Elastic MapReduce;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"emr.listClusters",
         "args":"",
         "inputs":"sourceApiName=emr.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"4x1"
         },
        {"platform":"k2",
         "apiName":"emr.listBootstrapActions",
         "args":"{\"clusterId\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=emr.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:id;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":"4x1"
         },
        {"platform":"k2",
         "apiName":"#emr.describeCluster",
         "args":"{\"clusterId\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=emr.describeCluster;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:id;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":"4x1"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.generateEmailTemplates",
         "args":"",
         "inputs":"sourceApiName=lambda.listFunctions;media=email;textFormat=html;toCloumnNames=masterOwnerAliasId;columnNames=accountId,regionCode,functionName,runtime,lastModified,fleetName,snapshotDate;primaryKeyName=masterOwnerAliasId;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sendNotifications",
         "args":"",
         "inputs":"sourceApiName=modu.generateEmailTemplates;media=email;fromAliasId=;toAliasIds=;ccAliasIds=hoeseong;bccAliasIds=;dryRun=True;",
         "conditions":"",
         "groupBy":"",
         "orderBy":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[Reliability Engineering] Aurora ReadIO Analysis" : {
    "meta" : {
      "reportName": "[CDO] Aurora ReadIO Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"auroa,auroa-mysql,aurora-postgresql in engine",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=maws.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=RDS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"auroa,auroa-mysql,aurora-postgresql in engine",
         "limit":"",
         "pt":"16x2"
         },
        {"platform":"moduAWS",
         "apiName":"rds.filterResults",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;nocsv",
         "conditions":"regionCode == us-east-1",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=ReadIOPS;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"idlePercentage(%) == 0.0",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"moduAWS",
         "apiName":"cw.filterResults",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:DBInstanceIdentifier;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cw.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=ReadIOPS;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier",
         "conditions":"",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/rds/;csvFilename=cdo-rds-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items, 
  "[Reliability Engineering] MAWS EC2 Exceeded Networking PPS" : {
    "meta" : {
      "reportName": "[Reliability Engineering] MAWS EC2 Exceeded Networking Packet Per Second",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"23.9 hours ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.discoverMawsAsgDetails",
         "args":"",
         "inputs":"sourceMedia=remote;nocsv",
         "conditions":"desiredInstances>0",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"{\"autoScalingGroupNames\":[\"${__asgName__}\"]}",
         "inputs":"sourceApiName=maws.discoverMawsAsgDetails;targetValues=accountId:accountId_,regionCode:regionCode_,asgName:asgName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"maximum>10",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"cw.filterResults",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:InstanceId;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cw.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=NetworkPacketsIn;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cw.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=NetworkPacketsOut;period=60;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"maws.analyzeEC2NetworkPerformance",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"usedAvgPPS(%)>30",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=maws.analyzeEC2NetworkPerformance;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/maws-ec2-pps/;csvFilename=cdo-maws-ec2-pps-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#  # begin: Template Items
  "[PoC] DynamoDB Consumed Capacity Analysis" : {
    "meta" : {
      "reportName": "[PoC] DynamoDB Consumed Capacity Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"365 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000006612683,000024256683,000024710191,000036892640,000058960170,000065539461,000070820998,000108650099",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;targetValues=accountId:accountId_;serviceName=DynamoDB;searchCondition=match",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName,billingMode:billingMode;nocsv",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBUsage",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=30;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBUsage;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/dynamodb-usage/;csvFilename=cdo-dynamodb-usage-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  "[PoC] DynamoDB Povisioned Capacity Utilization Analysis" : {
    "meta" : {
      "reportName": "[PoC] DynamoDB Povisioned Capacity Utilization Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"365 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=000006612683,000024256683,000024710191,000036892640,000058960170,000065539461,000070820998,000108650099",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;targetValues=accountId:accountId_;serviceName=DynamoDB;searchCondition=match",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName,billingMode:billingMode;nocsv",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=86400;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBUsage",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=30;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBUsage;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/dynamodb-utilization/;csvFilename=cdo-dynamodb-utilization-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  
  
  
  # begin: Template Items
  "[data provisioning] Enteprise Support Customer Profiles" : {
    "meta" : {
      "reportName": "[data provisioning] Enteprise Support Customer Profiles",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"profile.list",
        "args":"",
        "inputs":"sourceMedia=remote;query=nike.com",
        "conditions":"",
        "limit":"",
        "pt":""
        },
      ]
    }, # end: Template Items#
  
      
  # begin: Template Items
  "[data provisioning] EC2 Prefix Lists" : {
    "meta" : {
      "reportName": "[data provisioning] EC2 Prefix Lists",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"discoverResources.ipRanges",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {
          "platform":"moduAWS",
          "apiName":"modu.setTargetValues",
          "args":"",
          "inputs":"ipAddress=146.75.37.63,146.75.33.63,52.94.0.42,52.119.234.232,146.75.33.63,146.75.37.63,52.119.232.78,52.119.232.112,3.5.87.130,3.5.79.191,52.119.228.112,52.94.1.244,3.5.87.117,3.5.81.165,52.92.131.50,20.36.241.212,3.5.86.186,3.5.84.110,3.5.76.184,3.5.78.111,3.5.86.182,3.5.82.186,3.5.76.184,13.56.121.58",
          "conditions":"",
          "limit":"",
          "pt":"1x1"
          },
        {
          "platform":"moduAWS",
          "apiName":"describeResource.ipAddress",
          "args":"",
          "inputs":"sourceApiName=modu.setTargetValues;targetValues=ipAddress:ipAddress",
          "conditions":"",
          "limit":"",
          "pt":"8x8"
          }
      ]
    }, # end: Template Items#
        
  # begin: Template Items
  "[data provisioning] getK2Api Compatibility against boto3" : {
    "meta" : {
      "reportName": "[data provisioning] getK2Api Compatibility against boto3",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"getK2ApiNames",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
      
    }, # end: Template Items#
        
  }
  
'''
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
#========================================================================================================================
  # begin: Template Items
  "[unittest] discoverImrCost" : {
    "meta" : {
      "reportName": "moduAWS' UnitTest: 'discoverImrCost'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.discoverImrCost",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[unittest] discoverConduitCTI" : {
    "meta" : {
      "reportName": "moduAWS' UnitTest: 'discoverConduitCTI'",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"regionCode_=us-east-1;nocsv;accountId_=329423638140,671452935478,794024896263,880918510484,787149559823,787149559823,453833195546,018067754818,589506732331,923922636701,645130450452,958817629565,958836777662,113640595394,645130450452,453833195546,393655935354,679828101704,924637445623,001591884629,401078640101,077362005997,999515204624,501319536573,567184638716,580331739765,755840738472,609746069400,238842934746,946879801923,994136867826,130208003613,189449584780,522398581884,523910602058,741861391206,913118591559,501319536573,787149559823,099862914649,736332675735,736332675735,340242244871,755840738472,092139262562,595120469341,947114806411,052888222935,061323516734,436767835580,439619022406,549073162761,688083973275,219087926005,977626780948,408494063124,297385687169,432481853822,021561903526,403606113971,628671981940,628671981940,501319536573,397809160425,645130450452,340242244871,331561918276,124553194471,702056039310,595320780533,873948649698,430122390659,190375001379,094481201583,580331739765,857171411193,054278508970,718029022396,942485322649,719131906445,051728687787,113640595394,806208655666,339037037539,296585923145,296585923145,080531683175,677787312706,848744099708,038378679116,196915980276,085569058413,287775224950,714621683280,371405419496,254219213657,810758242441,555989621042,836008867703,877791447439,157383839067,584908256761,087854010904,598225452377,595320780533,233384191134,408062760677,540382611553,033352146516,678005932087,859517684765,465369119046,362678056512,260628162409,157787312516,232255457729,389518046836,501794629557,349787692915,501794629557,986857415990,461919009995,977756770664,018067754818,958761666246,057578146906,509547968559,038123293457,340242244871,036421095165,014827827310,832274259582,261435181829,130208003613,483623210144,230081805624,958845620234,556979164935,189449584780,261059558073,923922636701,650605780484,652613392143,028901742175,854495847392,218112259388,579420950482,015957721237,164838574598,005087123760,662482135884,555989621042,301254254823,907480283968,613225557329,073440770570,395582249821,608360078936,755271705284,720603942490,150171956305,483600360996,716366860843,579420950482,426511756460,087569601934,898437527959,429179731886,424537884062,069289935426,603200399373,579420950482,107591710736,867437980406,246232734983,579420950482,914569885343,308847491472,065433645055,251505162208,519180376673,164838574598,362818900774,501794629557,550365368796,678005932087,829730563400,895246551340,556979164935,943648433132,389518046836,160801650284,075758494382,015513797474,677787312706,155462313948,853126036468,579420950482,501319536573,277567848935,007754987285,896703871396,047062552417,656369806662,673385534282,379725042036,277674828973,167082580766,483623210144,954268612818,379725042036,050902935759,274997858894,509467670710,227778750723,613225557329,560487228701,660320533052,379725042036,623779288384,816692805244,816541353011,877759331505,320194472796,574977834358,053875078407,400577501318,862224793132,738865330415,334128564984,334586116988,911991941275,240451068018,114132262795,476424756474,796552731990,738953339491,065433645055,250582001414,202211233757,517788875162,611563864357,740248930772,062497989561,236110518990,029834125258,381599803528,239530023759,172388888774,027398970194,093416163188,589383341589,289423984879,556429543300,663646683190,111981653092,036751646246,654805363533,175001591008,347901270313,428393337726,515433315415,662586755485,712697260786,613289689979,721938063588,676582165246,248953866850,873388258415,634047383455,164560611355,101818225730,548394723462,548394723462,Core,ML,India,436852434754,458492755823,985397800574,175860761267,955113730834,261059558073,652613392143,847377887626,732446128418,860320408930,378416923495,111175713373,636874578776,746361076297,396560657073,227890819116,938372295080,910590995326,735612164109,054098690298,896102521091,922278515330,377060137263,579420950482,955291343377,971697623861,479819860331,639966304739,797743463538,541615846154,651129418634,848870997264,814541445604,034583088656,202211233757,907568163573,774185239182,308424044060,459658676658,916709106640,565915620853,031134323843,762890862368,995367761609,375121467453,711511410472,486029164573,099891866410,131491961440,295778349693,595048535311,614842336368,196902209557,519176020856,657051926755,895342871178,147025004534,318182912263,523779543164,620263627323,183211140689,501218183560,120497153371,302840744080,374339732326,075576879578,185566974780,316480664867,185566974780,806626924229,809411737580,192960249206,225685961548,571157245005,701630911417,125335762762,342135511598,972277501601,168435146619,283533222494,606192475191,814541445604,432833427593,550365368796,240656623008,362818900774,059023621032,034276152988,423302830879,287775224950,290385804985,381066881181,527476657057,846553545540,944312045139,300248759947,958416494912,588267997662,569307791389,193092826592,877558938018,538244385301,603200399373,389947071127,400722465521,579420950482,349667731870,436526578226,436526578226,436526578226,436526578226,444092117824,332146052505,476799542768,435569175256,315414308593,771451333594,255795783062,065305400592,374006122387,436526578226,542609084014,570388465206,107873746872,693450037126,880918510484,043714768218,182878055170,352413989091,352413989091,398089656185,941718346887,941718346887,168650923808,309277787449,352413989091,352413989091,617384926563,789822861367,000079582833,000079582833,228545202992,671665128970,671665128970,890058511826,690250847267,136443502416,346420300241,671665128970,671665128970,579420950482,788293143211,034583088656,104192906053,689471291327,070102187621,232866261553,427589185960,577164224985,896708795334,087443751987,094674464564,319981647167,503637364407,638191067669,071008587449,633815352428,889663202731,433343386846,968403895548,692423882172,850291037855,327632528808,381599803528,657034774730,688493999520,139173797521,708228387880,168650923808,565147392976,960608786107,146196196723,308424044060,424891565725,006367750530,603200399373,978325234930,383521453872,392034857741,132886338704,629844520609,662762114373,684726282907,854495847392,929731600128,956343527192,176430240057,691065527241,708585550248,716588955679,629844520609,049382095256,392034857741,568383657092,381599803528,381599803528,393461836511,517784230962,702186037461,798751895070,861193496548,686073353471,308424044060,425294847576,468736696738,997323895400,029834125258,067647736677,322537140423,638132034261,850311831009,012681505764,194734798959,303299792464,410489562072,274570575716,152548578290,716965352102,716965352102,325143435634,553661299166,958836777662,249639535688,952120036862,100355424060,252021269929,227778750723,429778411080,433397531694,505345203727,546875159916,716965352102,716965352102,465369119046,265829148821,578084145834,716965352102,952120036862,957948914136,637759532834,814460322838,055114799497,456253627531,595805188478,716965352102,716965352102,716965352102,716965352102,716965352102,991729659840,473855308343,425859009394,691509643345,742618683871,792920620965,490476226896,121059683371,233384191134,716965352102,716965352102,257294426293,031364962423,031364962423,099891866410,242146646995,321669974225,814810426968,124967988468,099891866410",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"discoverConduitCTI",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;nocsv", #;addAccountDetails=yes;accountDetailColumns=masterOwnerAliasId,masterOwnerJobLevel,conduitName
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] listOpenCases@K2": {
    "meta":{
      "reportName": "[CDO]  istOpenCases@K2 ${__snapshotDate__}",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":""
    },
    "apiList":[
      {
        "platform":"moduAWS",
        "apiName":"modu.discoverCase",
        "args":"",
        "inputs":"sourceMedia=local;addAccountDetails=yes",
        "conditions":"/CDO/ in fqfn",
         "limit":"100",
         "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.searchCases",
        "args":"",
        "inputs":"sourceApiName=modu.discoverCase;targetValues=accountId:accountId_,regionCode:us-east-1;addAccountDetails=yes",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/archive/;csvFilename=CDO_openCaseList-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/latest/;csvFilename=CDO_openCaseList-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"case.filterResults",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;targetValues=accountId:accountId_,regionCode:regionCode_,caseId:caseId,severity:severity;nocsv;",
        "conditions":"critical,urgent in severity",
        "limit":"",
        "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.describeCase",
        "args":"",
        "inputs":"sourceApiName=case.filterResults;targetValues=accountId:accountId_,regionCode:us-east-1,caseId:caseId;addAccountDetails=yes",
        "conditions":"",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.describeCase;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/details/archive/;csvFilename=CDO_openCaseDetails-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=case.filterResults;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/details/latest/;csvFilename=CDO_openCaseDetails-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"#modu.leftJoinWithTargetValues",
        "args":"",
        "inputs":"sourceApiName=ec2.getAccounts;targetValues=accountId:accountId_,severity:severity,categoryCode:categoryCode,subject:subject,serviceCode:serviceCode,assignedAgent:assignedAgent,createDateTime:createDateTime,lastIncomingMessageDateTime:lastIncomingMessageDateTime,lastOutgoingMessageDateTime:lastOutgoingMessageDateTime,correspondenceMethod:correspondenceMethod,status:status,caseId:caseId;joinWith=support.describeCase;joinValues=caseId:caseId;nocsv",
        "conditions":"",
        "limit":"",
        "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"#modu.uploadResultsToS3",
        "args":"",
        "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
    ]
  }, 
  # end: Template Items#  
  
  # begin: Template Items
  "[CDO] listResolvedCases@K2": {
    "meta":{
      "reportName": "[CDO]  istOpenCases@K2 ${__snapshotDate__}",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":""
    },
    "apiList":[
      {
        "platform":"moduAWS",
        "apiName":"modu.discoverCase",
        "args":"",
        "inputs":"sourceMedia=local;addAccountDetails=yes",
        "conditions":"/CDO/ in fqfn",
         "limit":"100",
         "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.searchCasesForResolved",
        "args":"",
        "inputs":"sourceApiName=modu.discoverCase;targetValues=accountId:accountId_,regionCode:us-east-1,endpointType:resolved;addAccountDetails=yes",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCasesForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/archive/;csvFilename=CDO_resolvedCaseList-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCasesForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/latest/;csvFilename=CDO_resolvedCaseList-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"case.filterResultsForResolved",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;targetValues=accountId:accountId_,regionCode:regionCode_,caseId:caseId,severity:severity;nocsv;",
        "conditions":"critical,urgent in severity",
        "limit":"",
        "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.describeCaseForResolved",
        "args":"",
        "inputs":"sourceApiName=case.filterResultsForResolved;targetValues=accountId:accountId_,regionCode:us-east-1,caseId:caseId;addAccountDetails=yes",
        "conditions":"",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.describeCaseForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/details/archive/;csvFilename=CDO_resolvedCaseDetails-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.describeCaseForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/details/latest/;csvFilename=CDO_resolvedCaseDetails-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"#modu.uploadResultsToS3",
        "args":"",
        "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
    ]
  }, 
  # end: Template Items#  
  
  # begin: Template Items
  "[CDO] listingAllCases@K2": {
    "meta":{
      "reportName": "[CDO]  istOpenCases@K2 ${__snapshotDate__}",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":""
    },
    "apiList":[
      {
        "platform":"moduAWS",
        "apiName":"modu.getAccounts",
        "args":"",
        "inputs":"orgName=${__orgName__};isActiveOnly=True;noBurnerAccount=True;orgCondition=containswith;searchCondition=combine",
        "conditions":"",
         "limit":"100",
         "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.searchCases",
        "args":"",
        "inputs":"sourceApiName=modu.getAccounts;targetValues=accountId:accountId_,regionCode:us-east-1",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/archive/;csvFilename=CDO_openCaseList-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCases;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/latest/;csvFilename=CDO_openCaseList-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"k2",
        "apiName":"support.searchCasesForResolved",
        "args":"",
        "inputs":"sourceApiName=modu.getAccounts;targetValues=accountId:accountId_,regionCode:us-east-1,caseId:caseId,endpointType:resolved",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCasesForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/archive/;csvFilename=CDO_resolvedCaseList-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=support.searchCasesForResolved;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/caseInfoAtK2/list/latest/;csvFilename=CDO_resolvedCaseList-latest.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {
        "platform":"moduAWS",
        "apiName":"#modu.uploadResultsToS3",
        "args":"",
        "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
        "conditions":"",
         "limit":"",
         "pt":"4x2"
      },
    ]
  }, # end of "listRedshiftClusters"
    # begin: Template Items
  "[CDO] Fleet Usage Info" : {
    "meta" : {
      "reportName": "Fleet Usage Info",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"#modu.discoverUsageSummary",
         "args":"",
         "inputs":"sourceMedia=cdo360;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.discoverServiceNames",
         "args":"",
         "inputs":"sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=AWS WAF;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"orgName=NA Consumer;serviceName=WAF;granualrity=month;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.getRegions",
         "args":"",
         "inputs":"orgName=NA Consumer;serviceName=WAF;granualrity=day;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items
  "[CDO] internal AZ Mapping" : {
    "meta" : {
      "reportName": "internal AZ Mapping",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"thisYear",
      "endTime":"thisYear"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=393495018094;regionCode_=us-east-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeRegions",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"1x1"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.getAccounts",
         "args":"",
         "inputs":"orgName=CDO;isActiveOnly=True;noBurnerAccount=True;orgCondition=containswith;searchCondition=combine;addAccountDetails=yes;accountDetailColumns=masterOwnerAliasId,masterOwnerJobLevel,conduitName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.joinResults",
         "args":"",
         "inputs":"sourceApiName=ec2.getAccounts;targetValues=accountId:accountId_;joinWith=ec2.describeRegions;joinValues=regionCode:regionName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2internal.describeAvailabilityZoneMappings",
         "args":"",
         "inputs":"sourceApiName=modu.joinResults;targetValues=accountId:accountId_,regionCode:regionCode_;localCache;localCacheTTL=31536000",
         "conditions":"",
         "limit":"",
         "pt":"32x3"
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2internal.describeAvailabilityZoneMappings;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/azMapping/;csvFilename=cdo-azMapping-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadJsonResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2internal.describeAvailabilityZoneMappings;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/azMapping/;jsonFilename=cdo-azMapping-${{SNAPSHOT_DATE}}.json",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] MAWS VPC Analysis" : {
    "meta" : {
      "reportName": "[CDO] MAWS VPC Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.discoverMawsAsgDetails",
         "args":"",
         "inputs":"nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=935219088151;regionCode_=cn-north-1,cn-northwest-1;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.filterResults",
         "args":"",
         "inputs":"sourceApiName=maws.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"ec2.describeSubnets",
         "args":"",
         "inputs":"sourceApiName=maws.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"maws.analyzeMawsVpcStatus",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=maws.analyzeMawsVPCs;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/maws-vpc/;csvFilename=maws-vpc-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "*[CDO] MAWS EC2 Placement Analysis" : {
    "meta" : {
      "reportName": "[CDO] MAWS EC2 Placement Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.discoverMawsAsgDetails",
         "args":"",
         "inputs":"apolloEnvFilters=Cache,Cachi;fleetFilters=Amazon/CDO/Consumer,fqfn<>Amazon/CDO/Consumer/Global Customer Fulfillment;sourceMedia=remote",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"{\"autoScalingGroupNames\":[\"${__endpointName__}\"]}",
         "inputs":"sourceApiName=maws.discoverAsgDetails;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:asgName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#maws.discoverSpreadIds",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#maws.analyzeEC2ColocationStatus",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#maws.analyzeEc2Neighbors",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=maws.analyzeEc2Neighbors;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/mawsPlacementStatus/;csvFilename=maws-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items, 
  "[CDO] MAWS EC2 Analysis" : {
    "meta" : {
      "reportName": "[CDO] MAWS EC2 Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.discoverMawsAsgDetails",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"{\"autoScalingGroupNames\":[\"${__asgName__}\"]}",
         "inputs":"sourceApiName=maws.discoverMawsAsgDetails;targetValues=accountId:accountId_,regionCode:regionCode_,asgName:asgName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"maws.analyzeEC2Instances",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=maws.analyzeEC2Instances;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/maws-ec2/;csvFilename=cdo-maws-ec2-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "*[CDO] MAWS EBS Analysis" : {
    "meta" : {
      "reportName": "[CDO] MAWS EBS Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ebs/;csvFilename=cdo-maws-ebs-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] NLB/ALB Target Group Analysis" : {
    "meta" : {
      "reportName": "[CDO] NLB/ALB Target Group Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"elb.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Elastic Load Balancing;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"10",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeLoadBalancers",
         "args":"",
         "inputs":"sourceApiName=elb.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"alb.describeTargetGroups",
         "args":"{\"loadBalancerArn\":\"${__loadBalancerArn__}\"}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=alb.describeTargetGroups;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerName:loadBalancerName,targetGroupName:targetGroupName;namespace=AWS/NetworkELB;metricName=HealthyHostCount;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TargetGroup:targetGroupName,LoadBalancer:loadBalancerName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"elb.filterResults",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;targetValues=accountId:accountId_,regionCode:regionCode_,LoadBalancer:LoadBalancer,TargetGroup:TargetGroup,granularity(sec):granularity(sec),startTime:startTime,endTime:endTime,dataPoints:dataPoints,average:average,minimum:minimum,maximum:maximum,unit:unit,InUse:InUse;addAccountDetails=yes",
         "conditions":"maximum>=5",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"alb.describeTags",
         "args":"\"resourceArns\":[\"${__loadBalancerArn__}\"]}",
         "inputs":"sourceApiName=alb.describeLoadBalancers;targetValues=accountId:accountId_,regionCode:regionCode_,loadBalancerArn:loadBalancerArn",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] EC2 Analysis" : {
    "meta" : {
      "reportName": "[CDO] EC2 Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Public EC2;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeReservedInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"24x2"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId,state:name;nocsv",
         "conditions":"state==running",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        #{"platform":"moduAWS",
        # "apiName":"dw.getDwActivePaidEc2Instances",
        # "args":"",
        # "inputs":"sourceApiName=ec2.filterResults;targetValues=accountId:accountId_;accountIdChunkCount=-1",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.analyzeEC2Instances;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ec2/;csvFilename=cdo-ec2-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] EC2 Analysis v2 (Do not use!)" : {
    "meta" : {
      "reportName": "[CDO] EC2 Analysis v2",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Public EC2;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeReservedInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"ec2.describeResources",
         "args":"",
         "inputs":"sourceApiName=ec2.getAccounts;targetValues=accountId:accountId_;serviceName=EC2;resourceStatus=Active",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeTags",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeResources;targetValues=accountId:accountId_,regionCode:regionCode_;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.analyzeEC2Instances;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ec2/;csvFilename=cdo-ec2-v2-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] EC2 DW RI Utilization" : {
    "meta" : {
      "reportName": "[CDO] EC2 RI Utilization",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"17 days ago",
      "endTime":"2 days ago"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Public EC2;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.getDwDailyEc2RIUtilization",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_;;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.getDwDailyEc2OdUsage",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_;;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"ec2.analyzeEc2DwRiUtilization",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.analyzeEc2RiUtilization;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ec2-ri/;csvFilename=cdo-ec2-ri-utilization-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Lambda Analysis" : {
    "meta" : {
      "reportName": "get Lambda Resource Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"lambda.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Lambda;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listFunctions",
         "args":"",
         "inputs":"sourceApiName=lambda.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getFunction",
         "args":"{\"functionName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=lambda.listFunctions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:functionName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listLayers",
         "args":"",
         "inputs":"sourceApiName=lambda.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.listEventSourceMappings",
         "args":"",
         "inputs":"sourceApiName=lambda.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"lambda.getAccountSettings",
         "args":"",
         "inputs":"sourceApiName=lambda.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] EBS Analysis" : {
    "meta" : {
      "reportName": "[CDO] EBS Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ebs.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=EBS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeVolumes",
         "args":"",
         "inputs":"sourceApiName=ebs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"16x3"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeVolumes;targetValues=accountId:accountId_,regionCode:regionCode_,volumeId:volumeId;namespace=AWS/EBS;metricName=VolumeWriteBytes;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=VolumeId:volumeId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsUtilization",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeEbsUtilization;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ebs/;csvFilename=cdo-ebs-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] EBS Snapshot Analysis" : {
    "meta" : {
      "reportName": "[CDO] EBS Snapshot Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"2 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=EBS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ec2.describeSnapshots",
         "args":"{\"ownerIds\":[\"${__accountId__}\"]}",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"16x2"
         },
        #{"platform":"moduAWS",
        # "apiName":"dw.discoverDwEbsSnapshots",
        # "args":"",
        # "inputs":"sourceApiName=ec2.describeSnapshots;targetValues=accountId:accountId_;accountIdChunkCount=-1",
        # "conditions":"",
        # "limit":"",
        # "pt":""
        # },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsSnapshots",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeEbsSnapshots;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ebs-snapshot/;csvFilename=cdo-ebs-snapshot-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] RDS Analysis" : {
    "meta" : {
      "reportName": "[CDO] RDS Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"maws.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=maws.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=RDS;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBInstanceArn",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRDSInstance",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/rds/;csvFilename=cdo-rds-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Redshift Analysis" : {
    "meta" : {
      "reportName": "[CDO] Redshift Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"redshift.setTargetValues",
         "args":"",
         "inputs":"accountId_=963362704314,123367104812;regionCode_=us-east-1,us-west-2,eu-west-1,ap-southeast-1,ap-northeast-1,ap-northeast-2;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeStorage",
         "args":"",
         "inputs":"sourceApiName=redshift.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.setTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Redshift;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeReservedNodes",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=redshift.describeReservedNodes;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/redshift-ri/;csvFilename=cdo-redshift-ri-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeStorage",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftStorage",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=redshift.describeReservedNodes;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/redshift-backupStorage/;csvFilename=cdo-redshift-backupStorage-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=PercentageDiskSpaceUsed;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"addAccountDetails=yes",
         #"inputs":"columnName=accountId,regionCode,clusterIdentifier,nodeType,clusterStatus,clusterCreateTime,availabilityZone,preferredMaintenanceWindow,numberOfNodes,tags,$od-Mo,$ri-Mo,$maxSaving-Mo,nextAction,reasons,DatabaseConnections:InUse,DatabaseConnections:idlePercentage(%),DatabaseConnections:startTime,DatabaseConnections:endTime,snapshotDate",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRedshiftCluster;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/redshift/;csvFilename=cdo-redshift-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] DynamoDB Analysis" : {
    "meta" : {
      "reportName": "[CDO] DynamoDB Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;targetValues=accountId:accountId_;serviceName=DynamoDB;searchCondition=match",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"#dynamodb.describeLimits",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;#sourceApiName=modu.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv;localCache",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName,billingMode:billingMode;nocsv",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ReadThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"#cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=WriteThrottleEvents;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeDynamoDBAccountLimit",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"riskStatus!=\"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeDynamoDBTableLimitRisk",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"riskStatus!=\"\"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBTables;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/dynamodb/;csvFilename=cdo-dynamodb-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "*[CDO] CloudFront Analysis" : {
    "meta" : {
      "reportName": "[CDO] CloudFront Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/cloudfront/;csvFilename=cdo-cloudfront-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] S3 Analysis" : {
    "meta" : {
      "reportName": "[CDO] S3 Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"s3.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=S3;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/S3\",\"maxResults\":500}",
         "inputs":"sourceApiName=s3.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,BucketName:BucketName,StorageType:StorageType;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=BucketName:BucketName,StorageType:StorageType:clusterName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/s3/;csvFilename=cdo-s3-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] ECS+Fargate Analysis" : {
    "meta" : {
      "reportName": "[CDO] ECS+Fargate Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"ecs.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Container;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#ecs.listTaskDefinitions",
         "args":"",
         "inputs":"sourceApiName=ecs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"#ecs.describeTaskDefinition",
         "args":"{\"taskDefinition\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.listTaskDefinitions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:value",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.listClusters",
         "args":"",
         "inputs":"sourceApiName=ecs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeClusters",
         "args":"{\"clusters\":[\"${__endpointName__}\"],\"include\":[\"ATTACHMENTS\"]}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:value",
         "conditions":"registeredContainerInstancesCount != 0",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#ecs.listServices",
         "args":"{\"cluster\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#ecs.listTasks",
         "args":"{\"cluster\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"ecs.listContainerInstances",
         "args":"{\"cluster\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=ecs.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName",
         "conditions":"",
         "limit":"",
         "pt":"8x4"
         },
        {"platform":"k2",
         "apiName":"ecs.describeContainerInstances",
         "args":"{\"cluster\":\"${__endpointName__}\",\"containerInstances\":${__containerInstance__}}",
         "inputs":"sourceApiName=ecs.listContainerInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:clusterName,containerInstance:containerInstanceArns",
         "conditions":"",
         "limit":"",
         "pt":""
         }, #"include":["ATTACHMENTS"]},"apiName":"ecs.describeClusters","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"{\"instanceIds\":[\"${__instanceId__}\"]}",
         "inputs":"sourceApiName=ecs.describeContainerInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;primaryKeys=instances,state;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },#{"instanceIds":["i-0df192389801a191b"]},"apiName":"ec2.describeInstances","sessionMetadata":{"segment":"rds_workbench","instance_id":"9252797a-2d24-4c92-804e-6de9759d842d-2","name":"ecs/single_ecs_cluster_overview"}}
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:ec2InstanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatchinternal.searchMetricsForAccount",
         "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/ECS\",\"maxResults\":500}",
         "inputs":"sourceApiName=ecs.listClusters;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace;nocsv",
         "conditions":"CPUUtilization,CPUReservation,MemoryUtilization,MemoryReservation in metricName",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,serviceName:ServiceName,clusterName:ClusterName;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ServiceName:serviceName,ClusterName:clusterName;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeEcsAwsLogsRisk",
         "args":"",
         "inputs":"#addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeEcsAwsLogsRisk",
         "args":"",
         "inputs":"addAccountDetails=yes;#addConduitCTI=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.analyzeEcsRiskReport",
         "args":"",
         "inputs":"addAccountDetails=yes;#addConduitCTI=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeEcsRiskReport;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ecs/;csvFilename=cdo-ecs-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] SNS Analysis" : {
    "meta" : {
      "reportName": "[CDO] SNS Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"sns.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Simple Notification Service;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"100",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"sns.listSubscriptions",
         "args":"",
         "inputs":"sourceApiName=sns.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"sns.getSubscriptionAttributes",
         "args":"{\"subscriptionArn\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=sns.listSubscriptions;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:subscriptionArn;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=sns.getSubscriptionAttributes;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/sns/;csvFilename=cdo-sns-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Dicover Resources" : {
    "meta" : {
      "reportName": "[CDO] Dicover Resources",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.discoverActiveUsageAccounts",
         "args":"",
         "inputs":"sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.getKeyMetricNames",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.leftJoinWithTargetValues",
         "args":"",
         "inputs":"sourceApiName=modu.getRegionsFromFMBI;targetValues=accountId:accountId_,regionCode:regionCode_,serviceName:serviceName;joinWith=modu.getKeyMetricNames;joinValues=serviceName:serviceName,nameSpace:nameSpace,metricName:metricName;primaryKeys=serviceName",
         "conditions":"namespace!=nameSpace,null",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.listMetrics",
         "args":"",
         "inputs":"sourceApiName=modu.leftJoinWithTargetValues;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:nameSpace,metricName:metricName",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=cloudwatch.getMetricStatistics;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/s3/;csvFilename=cdo-s3-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Direct Connect Analysis" : {
    "meta" : {
      "reportName": "get AWS Direct Connect Analysis",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
      {"platform":"moduAWS",
       "apiName":"dx.getRegions",
       "args":"",
       "inputs":"#orgName=CDO;serviceName=AWS Direct Connect;sourceMedia=local;nocsv",
       "conditions":"",
       "limit":"100",
       "pt":""
       },
  
      {"platform":"k2",
       "apiName":"cloudwatchinternal.searchMetricsForAccount",
       "args":"{\"accountId\":\"${__accountId__}\",\"query\":\"AWS/DX\",\"maxResults\":500}",
       "inputs":"sourceApiName=dx.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
       "conditions":"ConnectionState,ConnectionErrorCount in metricName",
       "limit":"",
       "pt":""
       },
      {"platform":"k2",
       "apiName":"cloudwatch.getMetricStatistics",
       "args":"",
       "inputs":"sourceApiName=cloudwatchinternal.searchMetricsForAccount;targetValues=accountId:accountId_,regionCode:regionCode_,namespace:namespace,metricName:metricName,ConnectionId:ConnectionId,VirtualInterfaceId:VirtualInterfaceId,OpticalLaneNumber:OpticalLaneNumber;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ConnectionId:ConnectionId,VirtualInterfaceId:VirtualInterfaceId,OpticalLaneNumber:OpticalLaneNumber;mode=Summary;addAccountDetails=yes",
       "conditions":"",
       "limit":"",
       "pt":""
       },
      {
        "platform":"moduAWS",
        "apiName":"#modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=health.describeEventDetails;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/moduAWS/operationalExcellence/directconnect/;csvFilename=cdo-dx-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {"platform":"moduAWS",
       "apiName":"#modu.uploadResultsToS3",
       "args":"",
       "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
       "conditions":"",
       "limit":"",
       "pt":""
       },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Health Events Analysis" : {
    "meta" : {
      "reportName": "get AWS Health Events Status",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"7 days ago",
      "endTime":"now"
      },
    "apiList": [
      {
        "platform":"moduAWS",
        "apiName":"modu.getAccounts",
        "args":"",
        "inputs":"orgName=CDO;isActiveOnly=True;noBurnerAccount=True;orgCondition=containswith;searchCondition=combine",
        "conditions":"",
         "limit":"100",
         "pt":""
      },
      {"platform":"k2",
       "apiName":"health.describeEvents",
       "args":"{\"filter\":{\"eventStatusCodes\":[\"open\",\"upcoming\"]}}",
       "inputs":"sourceApiName=modu.getAccounts;targetValues=accountId:accountId_,regionCode:us-east-1;nocsv",
       "conditions":"",
       "limit":"",
       "pt":""
       },
      {"platform":"k2",
       "apiName":"health.describeEventDetails",
       "args":"{\"eventArns\":[\"${__endpointName__}\"],\"locale\":\"en\"}",
       "inputs":"sourceApiName=health.describeEvents;targetValues=accountId:accountId_,regionCode:us-east-1,endpointName:arn;primaryKeys=event,eventDescription",
       "conditions":"",
       "limit":"",
       "pt":""
       },
      {
        "platform":"moduAWS",
        "apiName":"modu.uploadCsvResultToS3",
        "args":"",
        "inputs":"sourceApiName=health.describeEventDetails;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/moduAWS/operationalExcellence/phd/;csvFilename=cdo-health-events-${{SNAPSHOT_DATE}}.csv",
        "conditions":"",
         "limit":"",
         "pt":""
      },
      {"platform":"moduAWS",
       "apiName":"#modu.uploadResultsToS3",
       "args":"",
       "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
       "conditions":"",
       "limit":"",
       "pt":""
       },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Trusted Advisor" : {
    "meta" : {
      "reportName": "[CDO] Truested Advisor",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.setTargetValues",
         "args":"",
         "inputs":"accountId_=256455912682;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorChecks",
         "args":"",
         "inputs":"sourceApiName=modu.setTargetValues;targetValues=accountId:accountId_;chunkSize=50000;chunkOffset=-1",
         "conditions":"category=cost_optimizing",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.discoverActiveUsageAccounts",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.joinResults",
         "args":"",
         "inputs":"sourceApiName=modu.discoverActiveUsageAccounts;targetValues=accountId:accountId_;joinWith=trustedadvisor.describeTrustedAdvisorChecks;joinValues=regionCode:regionCode_,name:name,checkId:checkId,category:category",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"#trustedadvisor.refreshCheck",
         "args":"",
         "inputs":"sourceApiName=modu.joinResults;targetValues=accountId:accountId_,endpointType:checkId",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"trustedadvisor.describeTrustedAdvisorCheckSummaries",
         "args":"",
         "inputs":"sourceApiName=modu.joinResults;targetValues=accountId:accountId_,checkIds:checkId",
         "conditions":"status=warning,error",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"trustedadvisor.describeCheckItems",
         "args":"{\"accountInfo\":{\"accountId\":\"${__accountId__}\"},\"checkId\":\"${__endpointName__}\",\"count\":100,\"start\":0}",
         "inputs":"sourceApiName=trustedadvisor.describeTrustedAdvisorCheckSummaries;targetValues=accountId:accountId_,endpointName:checkId",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=Redshift;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources",
         "args":"",
         "inputs":"addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeTrustedAdvisorCostOptimizedFlaggedResources;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ta/;csvFilename=cdo-ta-${{SNAPSHOT_DATE}}.csv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  # begin: Template Items
  "[CDO] Resource Analysis" : {
    "meta" : {
      "reportName": "Resource Analysis for EC2, EBS, EBS Snapshot, RDS, Redshift, and DynamoDB",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"59 days ago",
      "endTime":"now"
      },
    "apiList": [
        #-------------#
        # Set OrgName #
        #-------------#
        {"platform":"moduAWS",
         "apiName":"org.setTargetValues",
         "args":"",
         "inputs":"orgName=/CDO/;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #-----#
        # RDS #
        #-----#
        {"platform":"moduAWS",
         "apiName":"rds.getRegions",
         "args":"",
         "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=RDS;nocsv;",
         "conditions":"",
         "limit":"1009",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"rds.describeDBInstances",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"#rds.describeDBClusters",
         "args":"",
         "inputs":"sourceApiName=rds.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"rds.listTagsForResource",
         "args":"{\"resourceName\":\"${__endpointName__}\"}",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,endpointName:dBInstanceArn;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=rds.describeDBInstances;targetValues=accountId:accountId_,regionCode:regionCode_,dBInstanceIdentifier:dBInstanceIdentifier;namespace=AWS/RDS;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=DBInstanceIdentifier:dBInstanceIdentifier;mode=Summary",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRDSInstance",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRDSInstance;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/rds/;csvFilename=cdo-rds-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        #---------#
        # Redshit # 
        #---------#
        {"platform":"moduAWS",
         "apiName":"redshift.getRegions",
         "args":"",
         "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=Redshift;nocsv;",
         "conditions":"",
         "limit":"1009",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"redshift.describeClusters",
         "args":"",
         "inputs":"sourceApiName=redshift.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=DatabaseConnections;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=redshift.describeClusters;targetValues=accountId:accountId_,regionCode:regionCode_,clusterIdentifier:clusterIdentifier;namespace=AWS/Redshift;metricName=PercentageDiskSpaceUsed;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=ClusterIdentifier:clusterIdentifier;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeRedshiftCluster",
         "args":"",
         "inputs":"addAccountDetails=yes",
         #"inputs":"columnName=accountId,regionCode,clusterIdentifier,nodeType,clusterStatus,clusterCreateTime,availabilityZone,preferredMaintenanceWindow,numberOfNodes,tags,$od-Mo,$ri-Mo,$maxSaving-Mo,nextAction,reasons,DatabaseConnections:InUse,DatabaseConnections:idlePercentage(%),DatabaseConnections:startTime,DatabaseConnections:endTime,snapshotDate",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeRedshiftCluster;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/redshift/;csvFilename=cdo-redshift-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        {"platform":"moduAWS",
         "apiName":"maws.discoverMawsAsgDetails",
         "args":"",
         "inputs":"",
         "conditions":"",
         "limit":"1009",
         "pt":""
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"{\"autoScalingGroupNames\":[\"${__asgName__}\"]}",
         "inputs":"sourceApiName=maws.discoverMawsAsgDetails;targetValues=accountId:accountId_,regionCode:regionCode_,asgName:asgName;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"maws.analyzeEC2Instances",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=maws.analyzeEC2Instances;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/maws-ec2/;csvFilename=cdo-maws-ec2-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        #-----#
        # EC2 #
        #-----#
        {"platform":"moduAWS",
         "apiName":"ec2.getRegions",
         "args":"",
         "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=Public EC2;nocsv;",
         "conditions":"",
         "limit":"1009",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeReservedInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"16x2"
         },
        {"platform":"k2",
         "apiName":"asg.describeAutoScalingGroups",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x2"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=asg.describeAutoScalingGroups;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"ec2.describeInstances",
         "args":"",
         "inputs":"sourceApiName=ec2.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;primaryKeys=instances,state",
         "conditions":"",
         "limit":"",
         "pt":"24x2"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.filterResults",
         "args":"",
         "inputs":"sourceApiName=ec2.describeInstances;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId,state:name;nocsv",
         "conditions":"state==running",
         "limit":"",
         "pt":""
          },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,instanceId:instanceId;namespace=AWS/EC2;metricName=CPUUtilization;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=InstanceId:instanceId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"ec2.analyzeEC2Instances",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=ec2.analyzeEC2Instances;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ec2/;csvFilename=cdo-ec2-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        #-----#
        # EBS #
        #-----#
        {"platform":"moduAWS",
         "apiName":"ebs.getRegions",
         "args":"",
         "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=EBS;nocsv;",
         "conditions":"",
         "limit":"1009",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"ec2.describeVolumes",
         "args":"",
         "inputs":"sourceApiName=ebs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"16x3"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=ec2.describeVolumes;targetValues=accountId:accountId_,regionCode:regionCode_,volumeId:volumeId;namespace=AWS/EBS;metricName=VolumeWriteBytes;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=VolumeId:volumeId;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsUtilization",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeEbsUtilization;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ebs/;csvFilename=cdo-ebs-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        #--------------#
        # EBS Snapshot # 
        #--------------#
        #{"platform":"moduAWS",
        # "apiName":"ebss.getRegions",
        # "args":"",
        # "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=EBS;nocsv;",
        # "conditions":"",
        # "limit":"",
        # "pt":"1x1"
        # },
        {"platform":"k2",
         "apiName":"ec2.describeSnapshots",
         "args":"{\"ownerIds\":[\"${__accountId__}\"]}",
         "inputs":"sourceApiName=ebs.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;",
         "conditions":"",
         "limit":"",
         "pt":"16x2"
         },
        {"platform":"moduAWS",
         "apiName":"dw.discoverDwEbsSnapshots",
         "args":"",
         "inputs":"sourceApiName=ec2.describeSnapshots;targetValues=accountId:accountId_;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeEbsSnapshots",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeEbsSnapshots;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/ebs-snapshot/;csvFilename=cdo-ebs-snapshot-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        
        #----------#
        # DynamoDB #
        #----------#
        {"platform":"moduAWS",
         "apiName":"dynamodb.getRegions",
         "args":"",
         "inputs":"sourceApiName=org.setTargetValues;targetValues=orgName:orgName;serviceName=DynamoDB;nocsv;",
         "conditions":"",
         "limit":"1009",
         "pt":"1x1"
         },
        {"platform":"k2",
         "apiName":"dynamodb.listTables",
         "args":"",
         "inputs":"sourceApiName=dynamodb.getRegions;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"tableName != \"\"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeTable",
         "args":"{\"tableName\":\"${__tableName__}\"}",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:result;primaryKeys=billingModeSummary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"dynamodb.filterResults",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName,billingMode:billingMode;nocsv",
         "conditions":"billingMode != PAY_PER_REQUEST",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"dynamodb.describeScalableTargets",
         "args":"",
         "inputs":"sourceApiName=dynamodb.listTables;targetValues=accountId:accountId_,regionCode:regionCode_;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x4"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.describeTable;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ConsumedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedReadCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"k2",
         "apiName":"cloudwatch.getMetricStatistics",
         "args":"",
         "inputs":"sourceApiName=dynamodb.filterResults;targetValues=accountId:accountId_,regionCode:regionCode_,tableName:tableName,indexName:indexName;namespace=AWS/DynamoDB;metricName=ProvisionedWriteCapacityUnits;period=3600;statistics=Average,Sum,Minimum,Maximum,SampleCount;dimensions=TableName:tableName,GlobalSecondaryIndexName:indexName;mode=Summary;nocsv",
         "conditions":"",
         "limit":"",
         "pt":"32x8"
         },
        {"platform":"moduAWS",
         "apiName":"modu.analyzeDynamoDBTables",
         "args":"",
         "inputs":"deletePreviousK2Results=yes;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=60;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.analyzeDynamoDBTables;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/operationalExcellence/dynamodb/;csvFilename=cdo-dynamodb-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        #---------------------#
        # Aggregating Results #
        #---------------------#
        {"platform":"moduAWS",
         "apiName":"modu.aggregateOptimizationAnalysis",
         "args":"",
         "inputs":"serviceNames=EC2,EBS,EBS-Snapshot,DynamoDB,RDS,Redshift,MAWS;sourceMedia=remote;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=120;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.aggregateOptimizationAnalysis;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/fleetOptimization/latest/;csvFilename=cdo-optimization-latest.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.aggregateOptimizationAnalysis;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/fleetOptimization/archive/;csvFilename=cdo-optimization-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        
        #-----------------------#
        # Uploading the results #
        #-----------------------#
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Item#  
  # begin: Template Items
  "[CDO] Aws Optimization Analysis" : {
    "meta" : {
      "reportName": "[CDO] Aws Optimization Analysis",
      "bcaDescription": "",
      "startTime":"59 days ago",
      "endTime":"now",
      "emailTemplate":""
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"modu.aggregateOptimizationAnalysis",
         "args":"",
         "inputs":"serviceNames=EC2,EBS,EBS-Snapshot,DynamoDB,RDS,Redshift,MAWS;sourceMedia=remote;addAccountDetails=yes",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.sleepTime",
         "args":"",
         "inputs":"sleepTime=300;nocsv;",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.aggregateOptimizationAnalysis;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/fleetOptimization/latest/;csvFilename=cdo-optimization-latest.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"modu.uploadCsvResultToS3",
         "args":"",
         "inputs":"sourceApiName=modu.aggregateOptimizationAnalysis;credentialName=S3-MODUAWS-PAO-BI;s3BucketName=pao-bi;s3Prefix=moduAWS/fleetOptimization/archive/;csvFilename=cdo-optimization-${{SNAPSHOT_DATE}}.csv;nocsv",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items#
  "[Operational Excellence] listing Active S3 Buckets" : {
    "meta" : {
      "reportName": "listing Active S3 Buckets",
      "bcaDescription": "",
      "emailTemplate":"",
      "startTime":"1 days ago",
      "endTime":"today"
      },
    "apiList": [
        {"platform":"moduAWS",
         "apiName":"s3.setTargetValues",
         "args":"",
         "inputs":"#regionCode_=us-east-1;nocsv;accountId_=022241274188,023245816879,023394019542,025855969140,026466494910,026978028269,028019436642,028617553031,029773783190,030642824637,033681564839,034543630514,037440828910,037825720272,042088423083,043702531683,045518652857,046315329157,049582645670,050471633556,054278508970,055708428572,055746098824,055757804653,056316637276,057631253129,061064852545,062466298097,062928457341,063035930465,065473930595,065622908326,067477145022,071526322190,071783920447,074594706144,076287230973,076847879360,077133846967,080759781363,083381731785,084301292476,087350076831,087996303655,090624670839,091924841599,095592909384,097325747696,098187645741,099379748324,099401977503,101239549872",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#getDwActiveS3Resources",
         "args":"",
         "inputs":"sourceApiName=s3.setTargetValues;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"s3.getRegions",
         "args":"",
         "inputs":"#orgName=CDO;serviceName=S3;sourceMedia=local;nocsv",
         "conditions":"",
         "limit":"5",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"getDwActiveS3Resources",
         "args":"",
         "inputs":"sourceApiName=s3.getRegions;targetValues=accountId:accountId_;serviceName=AmazonS3;accountIdChunkCount=-1",
         "conditions":"",
         "limit":"",
         "pt":""
         },
        {"platform":"moduAWS",
         "apiName":"#modu.uploadResultsToS3",
         "args":"",
         "inputs":"s3BucketName=pao-bi;s3Prefix=moduAWS/__results__/;credentialName=S3-MODUAWS-PAO-BI",
         "conditions":"",
         "limit":"",
         "pt":""
         },
      ]
    }, # end: Template Items## begin: Template Items
'''