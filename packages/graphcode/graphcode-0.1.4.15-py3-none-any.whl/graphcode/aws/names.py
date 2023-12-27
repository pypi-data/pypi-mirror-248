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

from graphcode.nosql import GcNoSQL

import json

registeredServiceNameMap_dict = {
  "016C6FED":"EC2",
  "1455FC70":"EC2",
  "154A458C":"EC2",
  "15ifz3sewlwbamqirgbxavdx3":"Matillion ETL for Snowflake",
  "9fmjj3b9hombuy4jawab1i13i":"Cisco Cloud Services Router (CSR) 1000V - AX Pkg. Max Performance",
  "dqopnmm95odjilthdh7l0hvrm":"Cloud Manager - Deploy & Manage NetApp Cloud Data Services",
  "7b66efupof63vp2q6l8r3ktdj4":"CentOS 7 Latest Minimal AMI",
  "1CBB820A":"EC2",
  "1D041555":"EC2",
  "1FFFB8A5":"EC2",
  "20353730":"EC2",
  "28BEF31B":"EC2",
  "29546292":"EC2",
  "2A491150":"EC2",
  "31939236":"EC2",
  "329289EC":"EC2",
  "3585F660":"EC2",
  "37B9BA06":"EC2",
  "410059ED":"EC2",
  "4317A854":"EC2",
  "49390F8D":"EC2",
  "49BC1A45":"EC2",
  "4B62F323":"EC2",
  "51E4A70F":"EC2",
  "5524ECC6":"EC2",
  "5C38661F":"EC2",
  "5E5DD37E":"EC2",
  "5F1CF23E":"EC2",
  "6E66DC3C":"EC2",
  "6E941178":"EC2",
  "7499A1D5":"EC2",
  "77550B0E":"EC2",
  "7B9BD936":"EC2",
  "8A70A884":"EC2",
  "8EB3756D":"EC2",
  "8FEF6396":"EC2",
  "902E8AC3":"EC2",
  "94EDA07C":"EC2",
  "9B384C0E":"EC2",
  "9BD4D8D5":"EC2",
  "9BF8B344":"EC2",
  "9CC1A4FD":"EC2",
  "9D315FD8":"EC2",
  "A1147D3C":"EC2",
  "A26FF133":"EC2",
  "AC7D9AF4":"EC2",
  "API Gateway":"ApiGateway",
  "AWS Amplify":"Amplify",
  "AWS App Runner":"AppRunner",
  "AWS AppSync":"AppSync",
  "AWS Audit Manager":"AuditManager",
  "AWS Backup":"Backup",
  "AWS Budgets":"Budgets",
  "AWS Cloud Map":"CloudMap",
  "AWS CloudFormation":"CloudFormation",
  "AWS CloudShell":"CloudShell",
  "AWS CloudTrail":"CloudTrail",
  "AWS CodeArtifact":"CodeArtifact",
  "AWS CodeCommit":"CodeCommit",
  "AWS CodePipeline":"CodePipeline",
  "AWS Config":"Config",
  "AWS Cost Explorer":"CostExplorer",
  "AWS DataPipeline":"DataPipeline",
  "AWS Data Transfer":"DataTransfer",
  "AWS DataSync":"DataSync",
  "AWS Database Migration Service":"DMS",
  "AWS Direct Connect":"DirectConnect",
  "AWS Directory Service":"DirectoryService",
  "AWS Elemental MediaConvert":"ElementalMediaConvert",
  "AWS Elemental MediaLive":"ElementalMediaLive",
  "AWS Elemental MediaPackage":"ElementalMediaPackage",
  "AWS Elemental MediaStore":"ElementalMediaStore",
  "AWS Fault Injection Simulator":"FIS",
  "AWS Firewall Manager":"FMS",
  "AWS Global Accelerator":"GlobalAccelerator",
  "AWS Glue":"Glue",
  "AWS Greengrass":"IoT Greengrass",
  "AWS Import/Export Snowball":"Import/Export Snowball",
  "AWS IoT":"IoT",
  "AWS IoT SiteWise":"IoT SiteWise",
  "AWS Key Management Service":"KMS",
  "AWS Lake Formation":"LakeFormation",
  "AWS Lambda":"Lambda",
  "AWS Migration Hub Refactor Spaces":"Migration Hub",
  "AWS Network Firewall":"NetworkFirewall",
  "AWS Premium Support":"Support",
  "AWS Resilience Hub":"Resilience Hub",
  "AWS Route 53 Application Recovery Controller":"Route53 Recovery",
  "AWS Secrets Manager":"SecretsManager",
  "AWS Security Hub":"SecurityHub",
  "AWS Service Catalog":"ServiceCatalog",
  "AWS Shield":"Shield",
  "AWS Step Functions":"States",
  "AWS Storage Gateway":"StorageGateway",
  "AWS Systems Manager":"Systems Manager",
  "AWS Transfer Family":"Transfer",
  "AWS WAF":"WAF",
  "AWS X-Ray":"XRay",
  "AWSAmplify":"Amplify",
  "AWSAppRunner":"AppRunner",
  "AWSAppSync":"AppSync",
  "AWSBackup":"Backup",
  "AWSBudgets":"Budgets",
  "AWSCloudFormation":"CloudFormation",
  "AWSCloudMap":"CloudMap",
  "AWSCloudShell":"CloudShell",
  "AWSCloudTrail":"CloudTrail",
  "AWSCodeArtifact":"CodeArtifact",
  "AWSCodeCommit":"CodeCommit",
  "AWSCodePipeline":"CodePipeline",
  "AWSConfig":"Config",
  "AWSCostExplorer":"CostExplorer",
  "AWSDataSync":"DataSync",
  "AWSDataTransfer":"DataTransfer",
  "AWSDatabaseMigrationSvc":"DMS",
  "AWSDirectConnect":"DirectConnect",
  "AWSDirectoryService":"DirectoryService",
  "AWSELB":"ELB",
  "AWSElementalMediaConvert":"ElementalMediaConvert",
  "AWSElementalMediaLive":"ElementalMediaLive",
  "AWSElementalMediaPackage":"ElementalMediaPackage",
  "AWSElementalMediaStore":"ElementalMediaStore",
  "AWSEvents":"Events",
  "AWSFIS":"FIS",
  "AWSFMS":"FMS",
  "AWSGlobalAccelerator":"GlobalAccelerator",
  "AWSGlue":"Glue",
  "AWSGreengrass":"IoT Greengrass",
  "AWSIoT":"IoT",
  "AWSIoTSiteWise":"IoT SiteWise",
  "AWSLakeFormation":"LakeFormation",
  "AWSLambda":"Lambda",
  "AWSMigrationHubRefactorSpaces":"Migration Hub",
  "AWSNetworkFirewall":"NetworkFirewall",
  "AWSQueueService":"SQS",
  "AWSR53AppRecoveryController":"Route53 Recovery",
  "AWSResilienceHub":"Resilience Hub",
  "AWSSecretsManager":"SecretsManager",
  "AWSSecurityHub":"SecurityHub",
  "AWSServiceCatalog":"ServiceCatalog",
  "AWSShield":"Shield",
  "AWSStorageGateway":"StorageGateway",
  "AWSSystemsManager":"Systems Manager",
  "AWSTransfer":"Transfer",
  "AWSXRay":"XRay",
  "A4B":"A4B",
  "Alexa for Business":"A4B",
  "Amazon API Gateway":"ApiGateway",
  "Amazon AppFlow":"AppFlow",
  "Amazon AppStream":"AppStream",
  "Amazon Athena":"Athena",
  "Amazon CloudFront":"CloudFront",
  "Amazon CloudSearch":"CloudSearch",
  "Amazon Cognito":"Cognito",
  "Amazon Cognito Sync":"Cognito",
  "Amazon Comprehend":"Comprehend",
  "Amazon Connect":"Connect",
  "Amazon Detective":"Detective",
  "Amazon DevOps Guru":"DevOps Guru",
  "Amazon DocumentDB (with MongoDB compatibility)":"DocDB",
  "Amazon DynamoDB":"DynamoDB",
  "Amazon EC2 Container Registry (ECR)":"ECR",
  "Amazon EC2 Container Service":"ECS",
  "Amazon ElastiCache":"ElastiCache",
  "Amazon Elastic Compute Cloud":"EC2",
  "Amazon Elastic Container Registry Public":"ECR Public",
  "Amazon Elastic Container Service":"ECS",
  "Amazon Elastic Container Service for Kubernetes":"EKS",
  "Amazon Elastic File System":"EFS",
  "Amazon Elastic MapReduce":"EMR",
  "Amazon Elasticsearch Service":"OpenSearch",
  "Amazon FSx":"FSx",
  "Amazon Forecast":"Forecast",
  "Amazon Fraud Detector":"FraudDetector",
  "Amazon Glacier":"Glacier",
  "Amazon GuardDuty":"GuardDuty",
  "Amazon HealthLake":"HealthLake",
  "Amazon Inspector":"Inspector",
  "Amazon Interactive Video Service":"Interactive Video Service",
  "Amazon Kendra":"Kendra",
  "Amazon Keyspaces (for Apache Cassandra)":"Keyspaces",
  "Amazon Kinesis":"Kinesis",
  "Amazon Kinesis Analytics":"Kinesis Analytics",
  "Amazon Kinesis Firehose":"Kinesis Firehose",
  "Amazon Lex":"Lex",
  "Amazon Lightsail":"Lightsail",
  "Amazon Location Service":"Location",
  "Amazon MQ":"MQ",
  "Amazon Machine Learning":"ML",
  "Amazon Macie":"Macie",
  "Amazon Managed Grafana":"Grafana",
  "Amazon Managed Service for Prometheus":"Prometheus",
  "Amazon Managed Streaming for Apache Kafka":"Kafka",
  "Amazon MemoryDB":"MemoryDB",
  "Amazon Neptune":"Neptune",
  "Amazon OpenSearch Service":"OpenSearch",
  "Amazon Pinpoint":"Pinpoint",
  "Amazon Polly":"Polly",
  "Amazon Quantum Ledger Database":"QLDB",
  "Amazon QuickSight":"QuickSight",
  "Amazon Redshift":"Redshift",
  "Amazon Registrar":"Registrar",
  "Amazon Rekognition":"Rekognition",
  "Amazon Relational Database Service":"RDS",
  "Amazon Route 53":"Route53",
  "Amazon S3 Glacier Deep Archive":"S3 Glacier Deep Archive",
  "Amazon SageMaker":"SageMaker",
  "Amazon Simple Email Service":"SES",
  "Amazon Simple Notification Service":"SNS",
  "Amazon Simple Queue Service":"SQS",
  "Amazon Simple Storage Service":"S3",
  "Amazon Simple Workflow Service":"SWF",
  "Amazon SimpleDB":"SimpleDB",
  "Amazon Sumerian":"Sumerian",
  "Amazon Textract":"Textract",
  "Amazon Timestream":"Timestream",
  "Amazon Translate":"Translate",
  "Amazon Virtual Private Cloud":"VPC",
  "Amazon WorkDocs":"WorkDocs",
  "Amazon WorkSpaces":"WorkSpaces",
  "AmazonApiGateway":"ApiGateway",
  "AmazonAppStream":"AppStream",
  "AmazonAthena":"Athena",
  "AmazonCloudFront":"CloudFront",
  "AmazonCloudSearch":"CloudSearch",
  "AmazonCloudWatch":"CloudWatch",
  "AmazonCognito":"Cognito",
  "AmazonCognitoSync":"Cognito",
  "AmazonConnect":"Connect",
  "AmazonDAX":"DAX",
  "AmazonDetective":"Detective",
  "AmazonDevOpsGuru":"DevOps Guru",
  "AmazonDocDB":"DocDB",
  "AmazonDynamoDB":"DynamoDB",
  "AmazonEC2":"EC2",
  "AmazonECR":"ECR",
  "AmazonECRPublic":"ECR Public",
  "AmazonECS":"ECS",
  "AmazonEFS":"EFS",
  "AmazonEKS":"EKS",
  "ES":"OpenSearch",
  "AmazonES":"OpenSearch",
  "AmazonElastiCache":"ElastiCache",
  "AmazonFSx":"FSx",
  "AmazonForecast":"Forecast",
  "AmazonFraudDetector":"FraudDetector",
  "AmazonGlacier":"Glacier",
  "AmazonGrafana":"Grafana",
  "AmazonGuardDuty":"GuardDuty",
  "AmazonHealthLake":"HealthLake",
  "AmazonIVS":"InteractiveVideoService",
  "AmazonInspector":"Inspector",
  "AmazonInspectorV2":"Inspector",
  "AmazonKendra":"Kendra",
  "AmazonKinesis":"Kinesis",
  "AmazonKinesisAnalytics":"Kinesis Analytics",
  "AmazonKinesisFirehose":"Kinesis Firehose",
  "AmazonLex":"Lex",
  "AmazonLightsail":"Lightsail",
  "AmazonLocationService":"Location",
  "AmazonMCS":"Keyspaces",
  "AmazonML":"ML",
  "AmazonMQ":"MQ",
  "AmazonMSK":"Kafka",
  "AmazonMacie":"Macie",
  "AmazonMemoryDB":"MemoryDB",
  "AmazonNeptune":"Neptune",
  "AmazonPinpoint":"Pinpoint",
  "AmazonPolly":"Polly",
  "AmazonPrometheus":"Prometheus",
  "AmazonQLDB":"QLDB",
  "AmazonQuickSight":"QuickSight",
  "AmazonRDS":"RDS",
  "AmazonRedshift":"Redshift",
  "AmazonRegistrar":"Registrar",
  "AmazonRekognition":"Rekognition",
  "AmazonRoute53":"Route53",
  "AmazonS3":"S3",
  "AmazonS3GlacierDeepArchive":"Glacier Deep Archive",
  "AmazonSES":"SES",
  "AmazonSNS":"SNS",
  "AmazonSWF":"SWF",
  "AmazonSageMaker":"SageMaker",
  "AmazonSimpleDB":"SimpleDB",
  "AmazonStates":"States",
  "AmazonSumerian":"Sumerian",
  "AmazonTextract":"Textract",
  "AmazonTimestream":"Timestream",
  "AmazonVPC":"VPC",
  "AmazonWorkDocs":"WorkDocs",
  "AmazonWorkMail":"WorkMail",
  "AmazonWorkSpaces":"WorkSpaces",
  "Amplify":"Amplify",
  "App Runner":"AppRunner",
  "AppFlow":"AppFlow",
  "AppStream":"AppStream",
  "AppSync":"AppSync",
  "Athena":"Athena",
  "Aviatrix Secure Networking Platform Metered - Copilot & 24x7 Support":"Aviatrix Secure Networking Platform Metered - Copilot & 24x7 Support",
  "B0BADA36":"EC2",
  "B45FA5D7":"EC2",
  "BB863D06":"EC2",
  "BD4E3D8E":"EC2",
  "Backup":"Backup",
  "Budgets":"Budgets",
  "CDACA090":"EC2",
  "CentOS 7 Latest Minimal AMI":"CentOS 7 Latest Minimal AMI",
  "Cisco Cloud Services Router (CSR) 1000V - AX Pkg. Max Performance":"Cisco Cloud Services Router (CSR) 1000V - AX Pkg. Max Performance",
  "Cloud Manager - Deploy & Manage NetApp Cloud Data Services":"Cloud Manager - Deploy & Manage NetApp Cloud Data Services",
  "Cloud Map":"CloudMap",
  "CloudFormation":"CloudFormation",
  "CloudFront":"CloudFront",
  "CloudSearch":"CloudSearch",
  "CloudShell":"CloudShell",
  "CloudTrail":"CloudTrail",
  "CloudWatch":"CloudWatch",
  "CloudWatch Events":"Events",
  "CodeArtifact":"CodeArtifact",
  "CodeBuild":"CodeBuild",
  "CodeCommit":"CodeCommit",
  "CodePipeline":"CodePipeline",
  "Cognito":"Cognito",
  "Cognito Sync":"Cognito",
  "AWS Savings Plans": "Savings Plans",
  "ComputeSavingsPlans":"Savings Plans for  Compute usage",
  "Config":"Config",
  "Connect":"Connect",
  "Contact Center Telecommunications (service sold by AMCS, LLC)":"Contact Center Telecommunications (service sold by AMCS, LLC)",
  "Cost Explorer":"CostExplorer",
  "D3334223":"EC2",
  "DE772ED8":"EC2",
  "Data Transfer":"DataTransfer",
  "DataSync":"DataSync",
  "Database Migration Service":"DMS",
  "Databricks Lakehouse Platform":"Databricks Lakehouse Platform",
  "Detective":"Detective",
  "DevOps Guru":"DevOps Guru",
  "Direct Connect":"DirectConnect",
  "DX":"DirectConnect",
  "Directory Service":"DirectoryService",
  "DocumentDB (with MongoDB compatibility)":"DocDB",
  "DynamoDB":"DynamoDB",
  "DynamoDB Accelerator (DAX)":"DAX",
  "E05AEA22":"EC2",
  "E128F066":"EC2",
  "E1F2CE57":"EC2",
  "E2B9458E":"EC2",
  "E40ACDEC":"EC2",
  "EC2 Container Registry (ECR)":"ECR",
  "EC2 Container Service":"ECS",
  "EC8995EA":"EC2",
  "ECA7CFA9":"EC2",
  "ECS-Optimized Windows 2019 Full":"ECS-Optimized Windows 2019 Full",
  "Amazon ECS-Optimized Windows 2019 Full":"ECS-Optimized Windows 2019 Full",
  "EE070551":"EC2",
  "ElastiCache":"ElastiCache",
  "Elastic Compute Cloud":"EC2",
  "Elastic Container Registry Public":"ECR Public",
  "Elastic Container Service":"ECS",
  "Elastic Container Service for Kubernetes":"EKS",
  "Elastic File System":"EFS",
  "Elastic Load Balancing":"ELB",
  "Elastic Map Reduce":"EMR",
  "Elastic MapReduce":"EMR",
  "ElasticMapReduce":"EMR",
  "Elasticsearch Service":"OpenSearch",
  "Elemental MediaConvert":"ElementalMediaConvert",
  "Elemental MediaLive":"ElementalMediaLive",
  "Elemental MediaPackage":"ElementalMediaPackage",
  "Elemental MediaStore":"ElementalMediaStore",
  "F0A87FFC":"EC2",
  "F7B9DD09":"EC2",
  "F8CB7904":"EC2",
  "FA4F3EC9":"EC2",
  "FDA70877":"EC2",
  "FF6AF72D":"EC2",
  "FFC80110":"EC2",
  "FSx":"FSx",
  "Fault Injection Simulator":"FIS",
  "Firewall Manager":"FMS",
  "Forecast":"Forecast",
  "Fraud Detector":"FraudDetector",
  "Gatling FrontLine - Continuous Load Testing":"Gatling FrontLine - Continuous Load Testing",
  "Glacier":"Glacier",
  "Global Accelerator":"GlobalAccelerator",
  "Glue":"Glue",
  "Greengrass":"IoT Greengrass",
  "GuardDuty":"GuardDuty",
  "Haproxy with Ubuntu 20.04":"Haproxy with Ubuntu 20.04",
  "HealthLake":"HealthLake",
  "IngestionServiceSnowball":"Import/Export Snowball",
  "Inspector":"Inspector",
  "Interactive Video Service":"Interactive Video Service",
  "IoT":"IoT",
  "IoT SiteWise":"IoT SiteWise",
  "IoTDeviceDefender":"IoT Device Defender",
  "IoTDeviceManagement":"IoT Device Management",
  "Kendra":"Kendra",
  "Key Management Service":"KMS",
  "Keyspaces (for Apache Cassandra)":"Keyspaces",
  "Kinesis":"Kinesis",
  "Kinesis Analytics":"Kinesis Analytics",
  "Kinesis Firehose":"Kinesis Firehose",
  "Lake Formation":"LakeFormation",
  "Lambda":"Lambda",
  "Lex":"Lex",
  "Lightsail":"Lightsail",
  "Location Service":"Location",
  "MQ":"MQ",
  "Machine Learning":"ML",
  "Macie":"Macie",
  "Managed Grafana":"Grafana",
  "Managed Service for Prometheus":"Prometheus",
  "Managed Streaming for Apache Kafka":"Kafka",
  "Matillion ETL - SaaS Billing":"Matillion ETL - SaaS Billing",
  "Matillion ETL for Snowflake":"Matillion ETL for Snowflake",
  "MemoryDB":"MemoryDB",
  "Micro Focus LoadRunner Professional 150 Virtual Users Hourly Fees":"Micro Focus LoadRunner Professional 150 Virtual Users Hourly Fees",
  "Migration Hub Refactor Spaces":"Migration Hub",
  "Neptune":"Neptune",
  "NetApp Cloud Volumes Service (Contract version)":"NetApp Cloud Volumes Service (Contract version)",
  "NetApp Cloud Volumes Service (Metered version)":"NetApp Cloud Volumes Service (Metered version)",
  "Network Firewall":"NetworkFirewall",
  "OCB  CloudSearch":"CloudSearch",
  "OCB  SageMaker":"SageMaker",
  "OCB Amazon CloudSearch":"CloudSearch",
  "OCB Amazon SageMaker":"SageMaker",
  "OCB Global Accelerator":"GlobalAccelerator",
  "OCBAWS Global Accelerator":"GlobalAccelerator",
  "OCBAWSGlobalAccelerator":"GlobalAccelerator",
  "OCBAmazonCloudSearch":"CloudSearch",
  "OCBAmazonSageMaker":"SageMaker",
  "OCBPremiumSupport":"Support",
  "OpenSearch Service":"OpenSearch",
  "OpsWorks":"OpsWorks",
  "AWS OpsWorks":"OpsWorks",
  "Out of Cycle Billing - DataTransfer":"Out of Cycle Billing - DataTransfer",
  "Out of Cycle Billing - ElasticMapReduce":"Out of Cycle Billing - ElasticMapReduce",
  "Pinpoint":"Pinpoint",
  "Polly":"Polly",
  "Quantum Ledger Database":"QLDB",
  "QuickSight":"QuickSight",
  "Redshift":"Redshift",
  "Registrar":"Registrar",
  "Rekognition":"Rekognition",
  "Relational Database Service":"RDS",
  "Resilience Hub":"Resilience Hub",
  "Route 53":"Route53",
  "Route 53 Application Recovery Controller":"Route53 Recovery",
  "S3 Glacier Deep Archive":"Glacier Deep Archive",
  "SageMaker":"SageMaker",
  "Savings Plans for AWS Compute usage":"Savings Plans for  Compute usage",
  "Secrets Manager":"SecretsManager",
  "SecureSphere WAF Management for AWS (On-Demand)":"SecureSphere WAF Management for  (On-Demand)",
  "Security Hub":"SecurityHub",
  "Service Catalog":"ServiceCatalog",
  "Shield":"Shield",
  "Simple Email Service":"SES",
  "Simple Notification Service":"SNS",
  "Simple Queue Service":"SQS",
  "Simple Storage Service":"S3",
  "Simple Workflow Service":"SWF",
  "SimpleDB":"SimpleDB",
  "SnowballExtraDays":"SnowballExtraDays",
  "Step Functions":"States",
  "Storage Gateway":"StorageGateway",
  "Sumerian":"Sumerian",
  "Systems Manager":"Systems Manager",
  "Teradata Vantage Enterprise (DIY)":"Teradata Vantage Enterprise (DIY)",
  "Teradata Viewpoint (Multiple Systems, DIY)":"Teradata Viewpoint (Multiple Systems, DIY)",
  "Textract":"Textract",
  "ThoughtSpot Search & AI-Driven Analytics":"ThoughtSpot Search & AI-Driven Analytics",
  "Timestream":"Timestream",
  "Training Certification Vouchers":"Training Certification Vouchers",
  "Transfer Family":"Transfer",
  "Ubuntu Pro 20.04 LTS":"Ubuntu Pro 20.04 LTS",
  "VM-Series Next-Generation Firewall Bundle 1":"VM-Series Next-Generation Firewall Bundle 1",
  "VMware Cloud on":"VMwareCloudOn",
  "VMware Cloud on AWS":"VMwareCloudOn",
  "VMwareCloudOnAWS":"VMwareCloudOn",
  "Virtual Private Cloud":"VPC",
  "WAF":"WAF",
  "WordPress Base Version":"WordPress Base Version",
  "WorkDocs":"WorkDocs",
  "WorkMail":"WorkMail",
  "WorkSpaces":"WorkSpaces",
  "X-Ray":"XRay",
  "auditmanager":"AuditManager",
  "awskms":"KMS",
  "kms":"KMS",
  "awswaf":"WAF",
  "waf":"WAF",
  "comprehend":"Comprehend",
  "datapipeline":"DataPipeline",
  "hk49j6foeaq0u4o31leix83u":"SecureSphere WAF Management for  (On-Demand)",
  "transcribe":"Transcribe",
  "translate":"Translate",
  "Amazon CodeGuru":"CodeGuru",
  "Amazon Lookout":"Lookout",
  "AWS Migration Hub":"Migration Hub",
  "PrivateLinkServices":"PrivateLink",
  #######################
  # Service Quotas Service Names
  #######################
  "Amazon AppStream 2.0":"AppStream2",
  "Amazon Braket":"Braket",
  "Amazon Chime":"Chime",
  "Amazon CloudWatch Evidently":"CloudWatch Evidently",
  "Amazon CloudWatch Logs":"CloudWatch Logs",
  "Amazon CloudWatch RUM":"CloudWatch RUM",
  "Amazon CodeGuru Profiler":"CodeGuru Profiler",
  "Amazon CodeGuru Reviewer":"CodeGuru Reviewer",
  "Amazon Cognito Federated Identities":"Cognito",
  "Amazon Cognito User Pools":"Cognito",
  "Amazon Comprehend Medical":"Comprehend Medical",
  "Amazon Connect Cases":"Connect Cases",
  "Amazon Connect Customer Profiles":"Connect",
  "Amazon Connect High-Volume Outbound Communications":"Connect",
  "Amazon Connect Wisdom":"Connect Wisdom",
  "Amazon Data Lifecycle Manager":"DataLifecycleManager",
  "DynamoDB Accelerator":"DAX",
  "DynamoDB Accelerator (DAX)":"DAX",
  "Amazon DynamoDB Accelerator (DAX)":"DAX",
  "EC2 Auto Scaling":"AutoScaling",
  "Amazon EC2 Auto Scaling":"AutoScaling",
  "Elastic Block Store ( EBS)":"EBS",
  "Amazon Elastic Block Store (Amazon EBS)":"EBS",
  "Elastic Compute Cloud ( EC2)":"EC2",
  "Amazon Elastic Compute Cloud (Amazon EC2)":"EC2",
  "Elastic Container Registry ( ECR)":"ECR",
  "Amazon Elastic Container Registry (Amazon ECR)":"ECR",
  "Elastic Container Registry Public ( ECR Public)":"ECR Public",
  "Amazon Elastic Container Registry Public (Amazon ECR Public)":"ECR Public",
  "Elastic Container Service ( ECS)":"ECS",
  "Amazon Elastic Container Service (Amazon ECS)":"ECS",
  "Elastic File System (EFS)":"EFS",
  "Amazon Elastic File System (EFS)":"EFS",
  "Amazon Elastic Inference":"Elastic Inference",
  "Elastic Kubernetes Service ( EKS)":"EKS",
  "Amazon Elastic Kubernetes Service (Amazon EKS)":"EKS",
  "Amazon Elastic Transcoder":"Transcoder",
  "Amazon EMR":"EMR",
  "Amazon EMR Serverless":"EMR Serverless",
  "EventBridge (CloudWatch Events)":"EventBridge",
  "Amazon EventBridge (CloudWatch Events)":"EventBridge",
  "CloudWatch Events":"EventBridge",
  "Amazon EventBridge Schema Registry":"EventBridge",
  "Amazon FinSpace":"FinSpace",
  "Amazon GameLift":"GameLift",
  "Amazon GameSparks":"GameSparks",
  "Amazon Interactive Video Service Chat":"Interactive Video Service Chat",
  "Amazon Kinesis Data Analytics":"Kinesis Analytics",
  "Amazon Kinesis Data Firehose":"Kinesis  Firehose",
  "Amazon Kinesis Data Streams":"Kinesis Data Streams",
  "Amazon Kinesis Video Streams":"Kinesis Video Streams",
  "Location Service ( Location)":"Location",
  "Amazon Location Service (Amazon Location)":"Location",
  "Amazon Lookout for Equipment":"Lookout For Equipment",
  "Amazon Lookout for Metrics":"Lookout For Metrics",
  "Amazon Lookout for vision":"Lookout For Vision",
  "Amazon Managed Blockchain":"Blockchain",
  "Amazon Managed Prometheus":"Prometheus",
  "Managed Streaming for Kafka (MSK)":"Kafka",
  "Amazon Managed Streaming for Kafka (MSK)":"Kafka",
  "Amazon Managed Workflows for Apache Airflow":"Airflow",
  "Amazon Monitron":"Monitron",
  "Amazon Nimble Studio":"Nimble Studio",
  "Amazon Personalize":"Personalize",
  "Relational Database Service ( RDS)":"RDS",
  "Amazon Relational Database Service (Amazon RDS)":"RDS",
  "Amazon Route 53 Recovery Control Configuration":"Route53 Recovery Control Configuration",
  "Amazon Route 53 Recovery Readiness":"Route53 Recovery Readiness",
  "Simple Email Service( SES)":"SES",
  "Amazon Simple Email Service(Amazon SES)":"SES",
  "Simple Notification Service ( SNS)":"SNS",
  "Amazon Simple Notification Service (Amazon SNS)":"SNS",
  "Simple Queue Service ( SQS)":"SQS",
  "Amazon Simple Queue Service (Amazon SQS)":"SQS",
  "Simple Storage Service ( S3)":"S3",
  "Amazon Simple Storage Service (Amazon S3)":"S3",
  "Amazon Transcribe":"Transcribe",
  "Virtual Private Cloud ( VPC)":"VPC",
  "Amazon Virtual Private Cloud (Amazon VPC)":"VPC",
  "Amazon WorkSpaces Application Manager":"WorkSpaces",
  "Amazon WorkSpaces Web":"WorkSpaces Web",
  "AWS Account Management":"Organizations",
  "AWS App Mesh":"AppMesh",
  "AWS AppConfig":"AppConfig",
  "AWS Application Cost Profiler":"Application Cost Profiler",
  "AWS Application Discovery Service":"Application Discovery Service",
  "AWS Auto Scaling Plans":"AutoScaling Plans",
  "AWS Batch":"Batch",
  "AWS Billing Conductor":"Billing",
  "AWS Bugbust":"Bugbust",
  "Certificate Manager (ACM)":"ACM",
  "AWS Certificate Manager (ACM)":"ACM",
  "Certificate Manager Private Certificate Authority (ACM PCA)":"ACM",
  "AWS Certificate Manager Private Certificate Authority (ACM PCA)":"ACM",
  "AWS Chatbot":"Chatbot",
  "AWS Cloud WAN":"CloudWAN",
  "AWS Cloud9":"Cloud9",
  "AWS CloudHSM":"CloudHSM",
  "AWS CodeBuild":"CodeBuild",
  "AWS CodeDeploy":"CodeDeploy",
  "AWS Compute Optimizer":"ComputeOptimizer",
  "AWS Data Exchange":"DataExchange",
  "Database Migration Service ( DMS)":"DMS",
  "AWS Database Migration Service (AWS DMS)":"DMS",
  "AWS DeepLens":"DeepLens",
  "AWS DeepRacer":"DeepRacer",
  "AWS Device Farm":"Device Farm",
  "Elastic Beanstalk":"Beanstalk",
  "AWS Elastic Beanstalk":"ElasticBeanstalk",
  "AWS Elemental MediaConnect":"ElementalMediaConnect",
  "AWS Elemental MediaTailor":"ElementalMediaTailor",
  "AWS Fargate":"Fargate",
  "AWS Glue DataBrew":"Glue DataBrew",
  "AWS Ground Station":"GroundStation",
  "Identity and Access Management (IAM)":"IAM",
  "AWS Identity and Access Management (IAM)":"IAM",
  "AWS IoT 1-Click":"IoT 1-Click",
  "AWS IoT Analytics":"IoT Analytics",
  "AWS IoT Core":"IoT Core",
  "AWS IoT Core Device Advisor":"IoT Core Device Advisor",
  "AWS IoT Events":"IoT Events",
  "AWS IoT Fleet Hub":"IoT Fleet Hub",
  "AWS IoT Greengrass":"IoT Greengrass",
  "AWS IoT RoboRunner":"IoT RoboRunner",
  "AWS IoT Things Graph":"IoT Things Graph",
  "AWS IoT TwinMaker":"IoT TwinMaker",
  "AWS IoT Wireless":"IoT Wireless",
  "Key Management Service ( KMS)":"KMS",
  "AWS Key Management Service (AWS KMS)":"KMS",
  "AWS Launch Wizard":"Launch Wizard",
  "AWS License Manager":"LicenseManager",
  "AWS License Manager User Subscriptions":"License Manager User Subscriptions",
  "AWS Mainframe Modernization":"Mainframe Modernization",
  "AWS OpsWorks for Chef Automate and AWS OpsWorks for Puppet Enterprise":"OpsWorks for Chef Automate and  OpsWorks for Puppet Enterprise",
  "AWS OpsWorks Stacks":"OpsWorks Stacks",
  "AWS Organizations":"Organizations",
  "AWS Outposts":"Outposts",
  "AWS Panorama":"Panorama",
  "AWS Private 5G":"Private 5G",
  "AWS Proton":"Proton",
  "AWS Resource Access Manager":"RAM",
  "AWS Resource Groups":"Resource Groups",
  "AWS RoboMaker":"RoboMaker",
  "AWS S3 Outposts":"S3 Outposts",
  "AWS Server Migration Service":"ServerMigration",
  "AWS Serverless Application Repository":"Serverless Application Repository",
  "Shield":"Shield",
  "AWS Shield":"Shield",
  "AWS Shield Advanced":"Shield Advanced",
  "AWS Signer":"Signer",
  "Single Sign-On (SSO)":"SSO",
  "AWS Single Sign-On (SSO)":"SSO",
  "AWS Snow Device Management":"Snow Device Management",
  "AWS Snow Family":"Snow Family",
  "AWS Support":"Support",
  "AWS Systems Manager GUI Connect":"Systems Manager GUI Connect",
  "AWS Systems Manager Incident Manager":"Systems Manager Incident Manager",
  "AWS Systems Manager Incident Manager Contacts":"Systems Manager Incident Manager Contacts",
  "AWS WAF Classic (Global)":"WAF",
  "AWS WAF Classic (Regional)":"WAF",
  "AWS Well-Architected Tool":"Well-Architected",
  "AWS Access Analyzer":"Access Analyzer",
  "Access Analyzer":"Access Analyzer",
  "Amplify UI Builder":"Amplify",
  "AWS Amplify UI Builder":"Amplify",
  "AWS Application Auto Scaling":"Application AutoScaling",
  "Application Auto Scaling":"Application AutoScaling",
  "AWS Application Migration":"ApplicationMigration",
  "Application Migration":"ApplicationMigration",
  "Amazon EC2 Fast Launch":"EC2 Fast Launch",
  "EC2 Fast Launch":"EC2 Fast Launch",
  "Amazon EC2 Image Builder":"EC2 Image Builder",
  "EC2 Image Builder":"EC2 Image Builder",
  "Amazon EC2 VM Import/Export":"VM Import/Export",
  "EC2 VM Import/Export":"VM Import/Export",
  "Elastic Load Balancing (ELB)":"ELB",
  "AWS ElasticDisasterRecovery":"DisasterRecovery",
  "ElasticDisasterRecovery":"DisasterRecovery",
  "AWS IAM Roles Anywhere":"IAM",
  "IAM Roles Anywhere":"IAM Roles Anywhere",
  "IPAM":"IPAM",
  "Mechanical Turk":"MechanicalTurk",
  "Migration Hub Orchestrator":"Migration Hub",
  "AWS Migration Hub Strategy Recommendations":"Migration Hub",
  "Migration Hub Strategy Recommendations":"Migration Hub",
  "AWS Network Insights":"Network Insights",
  "Network Insights":"Network Insights",
  "Route 53 Resolver":"Route53 Resolver",
  "AWS Service Quotas":"ServiceQuotas",
  "Service Quotas":"ServiceQuotas",
  ##################################
  "access-analyzer":"Access Analyzer",
  "account":"Account",
  "acm-pca":"ACM",
  "airflow":"Airflow",
  "application-autoscaling":"Application AutoScaling",
  "application-cost-profiler":"Application Cost Profiler",
  "appstream2":"AppStream2",
  "aps":"Prometheus",
  "autoscaling-plans":"AutoScaling",
  "cases":"Connect",
  "cassandra":"Keyspaces",
  "billingconductor":"Billing",
  "ce":"CostExplorer",
  "codeguru-profiler":"CodeGuru Profiler",
  "codeguru-reviewer":"CodeGuru Reviewer",
  "cognito-identity":"Cognito",
  "cognito-idp":"Cognito",
  "cognito-sync":"Cognito",
  "compute-optimizer":"ComputeOptimizer",
  "connect-campaigns":"Connect",
  "crowdscale-usagelimitservice":"MechanicalTurk",
  "databrew":"Glue DataBrew",
  "discovery":"Application Discovery Service",
  "dlm":"DataLifecycleManager",
  "drs":"DisasterRecovery",
  "ds":"DirectoryService",
  "ec2-ipam":"IPAM",
  "ecr-public":"ECR Public",
  "elastic-inference":"Elastic Inference",
  "emr-serverless":"EMR Serverless",
  "evidently":"CloudWatch Evidently",
  "geo":"Location",
  "imagebuilder":"EC2 Image Builder",
  "inspector2":"Inspector",
  "iot1click":"IoT 1-Click",
  "iotdeviceadvisor":"IoT Core Device Advisor",
  "ivs":"Interactive Video Service",
  "ivschat":"Interactive Video Service Chat",
  "kafka":"Kafka",
  "kinesisvideo":"Kinesis Video Streams",
  "license-manager":"LicenseManager",
  "license-manager-user-subscriptions":"LicenseManager",
  "lookoutequipment":"Lookout For Equipment",
  "lookoutmetrics":"Lookout For Metrics",
  "lookoutvision":"Lookout For Vision",
  "m2":"Mainframe Modernization",
  "macie2":"Macie",
  "mediaconnect":"ElementalMediaConnect",
  "mediaconvert":"ElementalMediaConvert",
  "medialive":"ElementalMediaLive",
  "mediapackage":"ElementalMediaPackage",
  "mediatailor":"ElementalMediaTailor",
  "mgn":"ApplicationMigration",
  "migrationhubstrategy":"Migration Hub",
  "monitoring":"CloudWatch",
  "network-firewall":"NetworkFirewall",
  "networkmanager":"CloudWAN",
  "nimble":"Nimble Studio",
  "opsworks-cm":"OpsWorks",
  "private-networks":"Private 5G",
  "profile":"Connect",
  "ram":"RAM",
  "refactor-spaces":"Migration Hub",
  "resource-groups":"Resource Groups",
  "rolesanywhere":"IAM",
  "route53-recovery-control-config":"Route53 Recovery",
  "route53-recovery-readiness":"Route53 Recovery",
  "rum":"CloudWatch RUM",
  "s3-outposts":"S3 Outposts",
  "schemas":"EventBridge",
  "serverlessrepo":"Serverless Application Repository",
  "sms":"ServerMigration",
  "snow-device-management":"Snow Device Management",
  "snowball":"Snow Family",
  "ssm":"Systems Manager",
  "ssm-contacts":"Systems Manager Incident Manager Contacts",
  "ssm-guiconnect":"Systems Manager GUI Connect",
  "ssm-incidents":"Systems Manager Incident Manager",
  "vendor-insights":"Marketplace",
  "vmimportexport":"VM Import/Export",
  "waf-regional":"WAF",
  "wafv2":"WAF",
  "wam":"WorkSpaces",
  "wellarchitected":"Well-Architected",
  "wisdom":"Connect Wisdom",
  "workspaces-web":"WorkSpaces",
  "Access Analyzer":"Access Analyzer",
  "AWS Account Management":"Organizations",
  "AWS Certificate Manager Private Certificate Authority (ACM PCA)":"ACM",
  "Amazon Managed Workflows for Apache Airflow":"Airflow",
  "Application Auto Scaling":"Application AutoScaling",
  "AWS Application Cost Profiler":"Application Cost Profiler",
  "Amazon AppStream 2.0":"AppStream2",
  "Amazon Managed Prometheus":"Prometheus",
  "AWS Auto Scaling Plans":"AutoScaling Plans",
  "Amazon Connect Cases":"Connect Cases",
  "Amazon Keyspaces (for Apache Cassandra)":"Keyspaces",
  "AWS Cost Explorer":"CostExplorer",
  "Amazon CodeGuru Profiler":"CodeGuru Profiler",
  "Amazon CodeGuru Reviewer":"CodeGuru Reviewer",
  "Amazon Cognito Federated Identities":"Cognito",
  "Amazon Cognito User Pools":"Cognito",
  "Amazon Cognito Sync":"Cognito",
  "AWS Compute Optimizer":"ComputeOptimizer",
  "Amazon Connect High-Volume Outbound Communications":"Connect",
  "Mechanical Turk":"MechanicalTurk",
  "AWS Glue DataBrew":"Glue DataBrew",
  "AWS Application Discovery Service":"Application Discovery Service",
  "Amazon Data Lifecycle Manager":"DataLifecycleManager",
  "ElasticDisasterRecovery":"DisasterRecovery",
  "AWS Directory Service":"DirectoryService",
  "IPAM":"IPAM",
  "Amazon Elastic Container Registry Public (Amazon ECR Public)":"ECR Public",
  "Amazon Elastic Inference":"Elastic Inference",
  "Amazon EMR Serverless":"EMR Serverless",
  "Amazon CloudWatch Evidently":"CloudWatch Evidently",
  "Amazon Location Service (Amazon Location)":"Location",
  "EC2 Image Builder":"EC2 Image Builder",
  "Amazon Inspector":"Inspector",
  "AWS IoT 1-Click":"IoT 1-Click",
  "AWS IoT Core Device Advisor":"IoT Core Device Advisor",
  "Amazon Interactive Video Service Chat":"InteractiveVideoService Chat",
  "Amazon Managed Streaming for Kafka (MSK)":"Kafka",
  "Amazon Kinesis Video Streams":"Kinesis Video Streams",
  "AWS License Manager":"LicenseManager",
  "AWS License Manager User Subscriptions":"LicenseManager User Subscriptions",
  "Amazon Lookout for Equipment":"Lookout For Equipment",
  "Amazon Lookout for Metrics":"Lookout For Metrics",
  "Amazon Lookout for vision":"Lookout For Vision",
  "AWS Mainframe Modernization":"Mainframe Modernization",
  "Amazon Macie":"Macie",
  "AWS Elemental MediaConnect":"ElementalMediaConnect",
  "AWS Elemental MediaConvert":"ElementalMediaConvert",
  "AWS Elemental MediaLive":"ElementalMediaLive",
  "AWS Elemental MediaPackage":"ElementalMediaPackage",
  "AWS Elemental MediaTailor":"ElementalMediaTailor",
  "Application Migration":"ApplicationMigration",
  "Migration Hub Strategy Recommendations":"Migration Hub",
  "Amazon CloudWatch":"CloudWatch",
  "AWS Network Firewall":"NetworkFirewall",
  "AWS Cloud WAN":"CloudWAN",
  "Amazon Nimble Studio":"Nimble Studio",
  "AWS OpsWorks for Chef Automate and AWS OpsWorks for Puppet Enterprise":"OpsWorks",
  "AWS Private 5G":"Private 5G",
  "Amazon Connect Customer Profiles":"Connect",
  "AWS Resource Access Manager":"RAM",
  "AWS Migration Hub Refactor Spaces":"Migration Hub",
  "AWS Resource Groups":"Resource Groups",
  "IAM Roles Anywhere":"IAM",
  "Amazon Route 53 Recovery Control Configuration":"Route53 Recovery",
  "Amazon Route 53 Recovery Readiness":"Route53 Recovery",
  "Amazon CloudWatch RUM":"CloudWatch RUM",
  "AWS S3 Outposts":"S3 Outposts",
  "Amazon EventBridge Schema Registry":"EventBridge",
  "AWS Serverless Application Repository":"Serverless Application Repository",
  "AWS Server Migration Service":"ServerMigration",
  "AWS Snow Device Management":"Snow Device Management",
  "AWS Snow Family":"Snow Family",
  "AWS Systems Manager":"Systems Manager",
  "AWS Systems Manager Incident Manager Contacts":"Systems Manager Incident Manager Contacts",
  "AWS Systems Manager GUI Connect":"Systems Manager GUI Connect",
  "AWS Systems Manager Incident Manager":"Systems Manager Incident Manager",
  "AWS Marketplace Vendor Insights":"Marketplace",
  "EC2 VM Import/Export":"VM Import/Export",
  "AWS WAF Classic (Regional)":"WAF",
  "AWS WAF":"WAF",
  "Amazon WorkSpaces Application Manager":"WorkSpaces",
  "AWS Well-Architected Tool":"Well-Architected",
  "Amazon Connect Wisdom":"Connect Wisdom",
  "Amazon WorkSpaces Web":"WorkSpaces",
  
  #######################
  # CloudWatch Namespaces
  #######################
  "AmplifyHosting":"Amplify",
  "DevOps-Guru":"DevOps Guru",
  "Amazon S3 Glacier": "Glacier",
  "ApplicationELB":"ApplicationELB",
  "Certificate Manager": "Certificate Manager",
  "CodeStar": "CodeStar",
  "Cognito User Pool": "Cognito",
  "EMRShutdown/Cluster-Metric":"EMR",
  "Firehose":"Kinesis Firehose",
  "Amazon Kinesis Data Firehose": "Kinesis Firehose",
  "Kinesis Data Firehose": "Kinesis Firehose",
  "Kinesis Firehose": "Kinesis Firehose",
  "Logs": "CloudWatch Logs",
  "MediaStore":"ElementalMediaStore",
  "NATGateway":"NATGateway",
  "NetworkELB":"NetworkELB",
  "PrivateLinkEndpoints":"PrivateLink",
  "Resource Groups Tagging API": "ResourceGroups",
  ###
  # AWS Health Events
  ###
  "APPLICATIONINSIGHTS": "ApplicationInsights",
  "ApplicationInsights": "ApplicationInsights",
  "CLIENT_VPN": "VPN",
  "VPN": "VPN",
  "IOT_DEVICE_MANAGEMENT": "IoTDeviceManagement",
  "MOBILETARGETING": "Pinpoint",
  "AWS SDK": "SDK",
  "SDK": "SDK",
  "SECURITY": "Security",
  "SERVICEDISCOVERY": "CloudMap",
  ####
  # AWS Support
  ###
  "customer-account": "Account",
  "account-management": "Account",
  "service-limit-increase":"Limit Increase",
  "service-opensearch-successor-to-amazon-elasticsearch": "OpenSearch",
  "Proton":"Proton",
  "service-proton":"Proton",
  "aws-identity-and-access-management":"IAM",
  "service-elastic-compute-cloud-ec2-macos":"EC2 Macos",
  "service-documentdb-with-mongodb-compatibility":"DocDB",
  "amazon-acm-service":"ACM",
  "amazon-batch":"States",
  "amazon-elastic-block-store":"EBS",
  "amazon-virtual-private-network":"VPC",
  "service-eks":"EKS",
  "service-fsx-for-netapp-ontap-linux":"NetApp Ontap Linux",
  "service-vpc-transit-gateway":"TransitGateway",
  "amazon-kinesis":"Kinesis",
  "amazon-marketplace":"Marketplace",
  ##
  ## technical:[Technical support]
  ##
  "amazon-batch":"States",
  "amazon-elastic-transcoder":"Transcoder",
  "amazon-elastic-compute-cloud-windows":"EC2 Windows",
  "amazon-simple-notification-service":"SNS",
  "amazon-virtual-private-network":"VPC",
  "aws-opsworks":"OpsWorks",
  "workmail":"WorkMail",
  "service-fsx-for-open-zfs":"FSx",
  "aws-organizations":"Organizations",
  "dynamodb-accelerator":"DAX",
  "aws-cloudformation":"CloudFormation",
  "amazon-greengrass":"IoT Greengrass",
  "amazon-elastic-file-system":"EFS",
  "service-opensearch-successor-to-amazon-elasticsearch":"OpenSearch",
  "service-ams-operations-service-request":"AMS",
  "service-deep-learning-containers":"DL Containers",
  "mediastore":"ElementalMediaStore",
  "service-santos":"Santos",
  "amazon-workspaces":"WorkSpaces",
  "service-managed-service-for-grafana":"Grafana",
  "service-apprunner":"AppRunner",
  "amazon-elastic-compute-cloud-linux":"EC2 Linux",
  "amazon-cognito":"Cognito",
  "service-macie":"Macie",
  "aws-direct-connect":"DirectConnect",
  "service-cloudendure-disaster-recovery":"Cloudendure",
  "service-lake-formation":"LakeFormation",
  "service-cloud-map":"CloudMap",
  "service-elastic-disaster-recovery-drs-for-windows":"Elastic Disaster Recovery Drs For Windows",
  "amazon-mechanical-turk":"MechanicalTurk",
  "aws-import-export-snowball":"Import/Export Snowball",
  "service-eventbridge":"EventBridge",
  "mandarin-support":"Support(Mandarin)",
  "mediaconvert":"ElementalMediaConvert",
  "chime":"Chime",
  "service-braket":"Braket",
  "alexa-for-business":"A4B",
  "aws-inspector":"Inspector",
  "aws-lambda":"Lambda",
  "service-backup":"Backup",
  "service-lookout-for-vision":"Lookout For Vision",
  "service-resilience-hub":"Resilience Hub",
  "service-appflow":"AppFlow",
  "support-api":"Support",
  "amazon-servermigration-windows":"ServerMigration Windows",
  "amazon-dynamodb":"DynamoDB",
  "amazon-relational-database-service-postgresql":"RDS Postgresql",
  "vcenter-management-portal":"VMware - vCenter",
  "service-healthlake":"HealthLake",
  "service-augmented-ai":"A2I",
  "Augmented Ai":"A2I",
  "guardduty":"GuardDuty",
  "key-management-service":"KMS",
  "Key Management Service":"KMS",
  "amazon-elastic-block-store":"EBS",
  "service-control-tower":"Control Tower",
  "service-security-hub":"SecurityHub",
  "mediatailor":"ElementalMediaTailor",
  "amazon-elastic-mapreduce":"Elastic Mapreduce",
  "service-lightsail-windows":"Lightsail",
  "service-vpc-transit-gateway":"TransitGateway",
  "service-amplify-framework":"Amplify",
  "amazon-kinesis":"Kinesis",
  "service-proton":"Proton",
  "service-cloudshell":"CloudShell",
  "service-finspace":"FinSpace",
  "service-vm-import-export-linux":"VM Import/Export Linux",
  "service-datasync":"DataSync",
  "service-ec2-image-builder-linux":"EC2 Image Builder",
  "amazon-pinpoint":"Pinpoint",
  "connect":"Connect",
  "service-firewall-manager":"FMS",
  "Firewall Manager":"FMS",
  "amazon-opsworks-chef-automate":"OpsWorks",
  "service-ground-station":"GroundStation",
  "opsworks-puppet-enterprise":"OpsWorks",
  "amazon-quicksight":"Quicksight",
  "amazon-machine-learning":"ML",
  "service-resource-groups":"Resource Groups",
  "aws-elastic-beanstalk":"Beanstalk",
  "amazon-redshift":"Redshift",
  "service-well-architected-tool":"Well-Architected",
  "service-fsx-for-lustre":"FSx",
  "service-workspaces-linux":"WorkSpaces",
  "amazon-relational-database-service-aurora-postgres":"RDS Aurora Postgres",
  "service-location-service":"Location",
  "mediapackage":"ElementalMediaPackage",
  "service-personalize":"Personalize",
  "amazon-rekognition":"Rekognition",
  "service-roborunner":"IoT RoboRunner",
  "service-managed-streaming-for-kafka":"Kafka",
  "service-codeartifact":"CodeArtifact",
  "distributed-denial-of-service":"DDoS",
  "service-ec2-image-builder-windows":"EC2 Image Builder",
  "service-application-migration-service-windows":"ApplicationMigration Windows",
  "service-transfer-for-sftp":"Transfer",
  "amazon-glacier":"Glacier",
  "mobile-analytics":"Mobile Analytics",
  "service-global-accelerator":"GlobalAccelerator",
  "aws-application-discovery-windows":"Application Discovery Windows",
  "service-deeplens":"DeepLens",
  "service-codeguru":"CodeGuru",
  "directory-service":"DirectoryService",
  "service-catalog":"Catalog",
  "service-iot-things-graph":"IoT Things Graph",
  "amazon-elasticsearch-service":"OpenSearch",
  "neptune":"Neptune",
  "amazon-cloudsearch":"CloudSearch",
  "service-audit-manager":"AuditManager",
  "service-parallelcluster":"ParallelCluster",
  "amazon-virtual-private-cloud":"VPC",
  "Virtual Private Cloud":"VPC",
  "service-cloud-control-api":"Cloud Control Api",
  "amazon-simple-storage-service":"S3",
  "Simple Storage Service":"S3",
  "service-memorydb":"MemoryDB",
  "service-deadline":"Deadline",
  "aws-step-functions":"States",
  "aws-data-pipeline":"DataPipeline",
  "amazon-simple-email-service":"SES",
  "Simple Email Service":"SES",
  "service-elastic-inference":"Elastic Inference",
  "service-red-hat-openshift-service-on-aws-rosa":"Red Hat Openshift On Aws Rosa",
  "service-databrew":"Glue DataBrew",
  "service-network-manager":"Network Manager",
  "service-forecast":"Forecast",
  "amazon-acm-service":"ACM",
  "service-launch-wizard-sap":"Launch Wizard",
  "service-client-vpn":"VPN",
  "code-star":"CodeStar",
  "service-eks-anywhere-eks-a":"EKS",
  "service-vpc-ip-address-manager":"VPC",
  "amazon-servermigration-linux":"ServerMigration Linux",
  "service-elastic-disaster-recovery-drs-for-linux":"DisasterRecovery",
  "aws-identity-and-access-management":"IAM",
  "service-mediaconnect":"MediaConnect",
  "service-amplify-console":"Amplify",
  "appsync":"AppSync",
  "service-rds-on-vmware":"VMware - RDS",
  "cloudtrail":"CloudTrail",
  "service-application-migration-service-linux":"ApplicationMigration Linux",
  "systems-manager-for-microsoft-scvmm":"Systems Manager For Microsoft",
  "aws-storage-gateway":"StorageGateway",
  "comprehend":"Comprehend",
  "mobile-hub":"Mobile Hub",
  "amazon-lex":"Lex",
  "aws-iot":"IoT",
  "kinesis-video-streams":"Kinesis Video Streams",
  "service-cloudendure-migration":"Cloudendure",
  "service-cloudendure-disaster-recovery-windows":"Cloudendure",
  "single-sign-on":"Single Sign On",
  "service-fsx-for-netapp-ontap-windows":"FSx",
  "service-compute-optimizer-windows":"ComputeOptimizer Windows",
  "service-documentdb-with-mongodb-compatibility":"DocDB",
  "freertos":"FreeRTOS",
  "training-service":"Educate",
  "service-resource-access-manager":"RAM",
  "Resource Access Manager":"RAM",
  "amazon-cloudfront":"CloudFront",
  "cloudfront":"CloudFront",
  "translate":"Translate",
  "service-worklink":"WorkLink",
  "amazon-elasticache":"ElastiCache",
  "transcribe":"Transcribe",
  "device-farm":"Device Farm",
  "service-monitron":"Monitron",
  "service-snowcone":"Snowcone",
  "config-service":"Config",
  "service-vm-import-export-windows":"VM Import/Export Windows",
  "service-robomaker":"RoboMaker",
  "codedeploy":"CodeDeploy",
  "service-relational-database-service-proxy":"RDS Proxy",
  "amazon-relational-database-service-mariadb":"RDS Mariadb",
  "service-deepcomposer":"Deepcomposer",
  "aws-import":"Import",
  "medialive":"ElementalMediaLive",
  "iot-1-click":"IoT 1-Click",
  "zocalo":"WorkDocs",
  "service-honeycode":"Honeycode",
  "amazon-simpledb":"SimpleDB",
  "auto-scaling":"AutoScaling",
  "service-backint-agent-sap":"Backint Agent Sap",
  "service-lookout-for-metrics":"Lookout For Metrics",
  "service-cloud-wan":"CloudWAN",
  "service-eks":"EKS",
  "service-database-migration-service-dms":"DMS",
  "cloud9":"Cloud9",
  "lambda-edge":"Lambda Edge",
  "amazon-lightsail":"Lightsail",
  "service-app-mesh":"AppMesh",
  "service-managed-workflows-for-apache-airflow-mwaa":"Airflow",
  "alexa-services":"Alexa",
  "amazon-cloudwatch":"CloudWatch",
  "aws-iot-analytics":"IoT Analytics",
  "service-panorama":"Panorama",
  "sentinel-service-request":"AMS",
  "service-timestream":"Timestream",
  "serverless-application-repository":"Serverless Application Repository",
  "service-deepracer":"DeepRacer",
  "aws-shield":"Shield",
  "amazon-kinesis-analytics":"Kinesis Analytics",
  "service-textract":"Textract",
  "service-fsx-for-netapp-ontap-linux":"FSx",
  "service-devops-guru":"DevOps Guru",
  "amazon-appstream2":"Appstream2",
  "dcv-desktop-cloud-visualization":"Desktop Cloud Visualization",
  "service-sumerian":"Sumerian",
  "aws-cloud-hsm":"CloudHSM",
  "amazon-kinesis-firehose":"Kinesis Firehose",
  "service-iot-events":"IoT Events",
  "service-outposts":"Outposts",
  "service-detective":"Detective",
  "amazon-polly":"Polly",
  "amazon-simple-queue-service":"SQS",
  "Simple Queue Service":"SQS",
  "service-launch-wizard-linux":"Launch Wizard",
  "service-bugbust":"Bugbust",
  "service-license-manager":"LicenseManager",
  "amazon-relational-database-service-oracle":"RDS Oracle",
  "service-chatbot":"Chatbot",
  "ec2-container-service":"ECS",
  "service-network-firewall":"Network Firewall",
  "workspaces-application-manager":"WorkSpaces",
  "aws-relational-database-service-sql-server":"RDS SQL Server",
  "service-fault-injection-simulator":"FIS",
  "service-ams-operations-report-incident":"AMS",
  "service-cloudendure-migration-windows":"Cloudendure",
  "codepipeline":"CodePipeline",
  "api-gateway":"ApiGateway",
  "aws-glue":"Glue",
  "service-cloud-development-kit-cdk":"CDK",
  "elastic-load-balancing":"ELB",
  "Elastic Load Balancing":"ELB",
  "gamelift":"GameLift",
  "service-fraud-detector":"FraudDetector",
  "service-container-registry-ecr":"ECR",
  "service-compute-optimizer-linux":"ComputeOptimizer Linux",
  "amazon-appstream":"AppStream",
  "iot-device-management":"IoT Device Management",
  "service-kendra":"Kendra",
  "service-nimble-studio":"Nimble Studio",
  "service-launch-wizard":"Launch Wizard",
  "aws-web-application-firewall":"WAF",
  "Web Application Firewall":"WAF",
  "service-systems-manager-incident-manager":"Systems Manager Incident Manager",
  "service-account-management-api":"Organizations",
  "sagemaker":"SageMaker",
  "amazon-relational-database-service-aurora":"RDS Aurora",
  "amazon-codebuild":"CodeBuild",
  "secrets-manager":"SecretsManager",
  "amazon-route53":"Route53",
  "gamesparks":"GameSparks",
  "service-managed-service-for-prometheus":"Prometheus",
  "systems-manager":"Systems Manager",
  "migration-hub":"Migration Hub",
  "service-lookout-for-equipment":"Lookout For Equipment",
  "service-emp-for-windows-server":"EMP For Windows Server",
  "amazon-athena":"Athena",
  "service-workspaces-web":"WorkSpaces",
  "service-managed-apache-cassandra-service":"Keyspaces",
  "aws-trusted-advisor":"TrustedAdvisor",
  "fargate":"Fargate",
  "service-interactive-video-service":"Interactive Video Service",
  "service-iot-device-defender":"IoT Device Defender",
  "amazon-mq":"MQ",
  "amazon-database-migration-service":"DMS",
  "Database Migration Service":"DMS",
  "aws-health":"Health",
  "service-mainframe-modernization":"Mainframe Modernization",
  "amazon-xray":"XRay",
  "amazon-artifact":"Artifact",
  "sentinel-report-incident":"AMS",
  "service-fsx-for-windows-file-server":"FSx",
  "codecommit":"CodeCommit",
  "amazon-simple-workflow-service":"SWS",
  "amazon-relational-database-service-mysql":"RDS MySql",
  "service-quantum-ledger-database":"Quantum Ledger Database",
  "aws-application-discovery-linux":"Application Discovery Linux",
  "service-managed-blockchain":"Blockchain",
  "service-elastic-compute-cloud-ec2-macos":"EC2 MacOS",
  ##
  ## customer-service:[Account and billing support]
  ##
  "account-management":"Account",
  "service-international-expansion":"International Expansion",
  "amazon-marketplace":"Marketplace",
  "service-iq":"IQ",
  "customer-account":"Account",
  "service-academy":"Educate",
  "general-info":"Customer Service",
  "service-educate":"Educate",
  "service-data-exchange":"DataExchange",
  "billing":"Billing",
  "service-free-tier":"Customer Service",
  ##
  ##  service-limit-increase:[Service limit increase]
  ##
  "service-limit-increase":"Limit Increase",
}

def getPreferredServiceName(serviceName, dataSource = None):
  
  if serviceName == None:
    #actions.loadGlobalPreferredServiceName_dict
    dataSource = "default"
    
    gcNosql = GcNoSQL()
    try:
      preferredServiceName_dict = json.loads(gcNosql.getItem(tableName="serviceInsights", key="global.preferredServiceName_dict"))
    except:
      preferredServiceName_dict = {}
      
    for serviceName in registeredServiceNameMap_dict.keys():
      isNativeAws = False
      
      preferredServiceName = registeredServiceNameMap_dict[serviceName]
      
      loweredServiceName = serviceName.lower()
      for keyword in ["aws", "amazon", "alexa"]:
        if keyword.lower() in loweredServiceName:
          isNativeAws = True
          break
      
      if isNativeAws == False:
        for keyword in ["IoTDevice", "OpsWorks", "Snowball"]:
          if keyword.lower() in loweredServiceName:
            isNativeAws = True
            break
      
      if preferredServiceName in preferredServiceName_dict.keys():
        if dataSource in preferredServiceName_dict[preferredServiceName].keys():
          if serviceName not in preferredServiceName_dict[preferredServiceName][dataSource]:
            if serviceName not in preferredServiceName_dict[preferredServiceName][dataSource]:
              preferredServiceName_dict[preferredServiceName][dataSource].append(serviceName)
        else:
          preferredServiceName_dict[preferredServiceName][dataSource] = [serviceName]
      else:
        preferredServiceName_dict[preferredServiceName] = {}
        preferredServiceName_dict[preferredServiceName][dataSource] = [serviceName]
      
      if isNativeAws:
        preferredServiceName_dict[preferredServiceName]["isNativeAws"] = isNativeAws
        
    #actions.saveGlobalPreferredServiceName_dict
    gcNosql.putItem(tableName="serviceInsights", key="global.preferredServiceName_dict", value=preferredServiceName_dict)
                           
    preferredServiceName_list = []
    for preferredServiceName in sorted(preferredServiceName_dict.keys()):
      preferredServiceName_list.append(
        {
          "preferredServiceName": preferredServiceName,
          "isNativeAws": None,
          "cwAws": None,
          "cwUsage": None,    
          "cwOthers": None,
          "sq":None,
          "cur":None,
          "health":None,
          "ta":None,
          "support":None,
          "others":None,
          **preferredServiceName_dict[preferredServiceName]
          }
        )
    gcNosql.putItem(tableName="serviceInsights", key="global.preferredServiceNames", value=preferredServiceName_list)
    
    return preferredServiceName
  
  elif dataSource != None:
    preferredServiceName = None
    
    dataSource_list = ["cwAws", "cwUsage", "cwOthers", "sq", "cur", "health", "ta", "support"]
    if dataSource not in dataSource_list:
      raiseValueError("dataSource:[{}] must be in {}".format(dataSource, dataSource_list))
    
    if serviceName in registeredServiceNameMap_dict.keys():
      preferredServiceName = registeredServiceNameMap_dict[serviceName]
    else:
      
      for thisServiceName in registeredServiceNameMap_dict.keys():
        if dataSource == "support":
          if serviceName.startswith("amazon-elastic-compute-cloud"):
            subServiceName_list = serviceName.split("-")
            if len(subServiceName_list) == 4:
              preferredServiceName = registeredServiceNameMap_dict["AmazonEC2"]
              break
            
            else:
              subServiceName = ""
              for offset in range(4, len(subServiceName_list)):
                if subServiceName == "":
                  subServiceName += "{}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                else:
                  subServiceName += " {}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                  
              preferredServiceName = "{} {}".format(registeredServiceNameMap_dict["AmazonEC2"], subServiceName)
              break
            
          elif serviceName.startswith("service-elastic-compute-cloud-ec2"):
            subServiceName_list = serviceName.split("-")
            if len(subServiceName_list) == 5:
              preferredServiceName = registeredServiceNameMap_dict["AmazonEC2"]
              break
            
            else:
              subServiceName = ""
              for offset in range(5, len(subServiceName_list)):
                if subServiceName == "":
                  subServiceName += "{}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                else:
                  subServiceName += " {}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                  
              preferredServiceName = "{} {}".format(registeredServiceNameMap_dict["AmazonEC2"], subServiceName)
              break
            
          elif serviceName.startswith("amazon-relational-database-service"):
            subServiceName_list = serviceName.split("-")
            if len(subServiceName_list) == 4:
              preferredServiceName = registeredServiceNameMap_dict["AmazonRDS"]
              break
            
            else:
              subServiceName = ""
              for offset in range(4, len(subServiceName_list)):
                if subServiceName == "":
                  subServiceName += "{}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                else:
                  subServiceName += " {}{}".format(subServiceName_list[offset][0].upper(), subServiceName_list[offset][1:].lower())
                  
              preferredServiceName = "{} {}".format(registeredServiceNameMap_dict["AmazonRDS"], subServiceName)
              break
          
          elif serviceName.startswith("service-") and serviceName.replace("-", "").replace("service","").replace("aws","").replace("amazon","").strip() == thisServiceName.lower().replace(" ","").strip():
            preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
            break
          
          elif serviceName.replace("-", "").replace("aws","").replace("amazon","").strip() == thisServiceName.lower().replace(" ","").strip():
            
            preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
            break
          
        elif dataSource == "health" and serviceName.replace("_", "").replace("aws","").replace("amazon","").strip() == thisServiceName.lower().replace(" ","").strip():
          preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
          break
        
        if serviceName.lower().replace(" ","").strip() == thisServiceName.lower().replace(" ","").strip():
          preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
          break
        
        elif serviceName.lower().replace(" ","").strip() == registeredServiceNameMap_dict[thisServiceName].lower().replace(" ","").strip():
          preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
          break
      
      if preferredServiceName == None:
        for keyword in ["aws", "Aws", "AWS", "amazon", "Amazon", "AMAZON"]:
          if keyword in serviceName:
            redactedServiceName = serviceName.replace(keyword, "").strip()
            if redactedServiceName in registeredServiceNameMap_dict.keys():
              preferredServiceName = registeredServiceNameMap_dict[redactedServiceName]
              break
            
            for thisServiceName in registeredServiceNameMap_dict.keys():
              if serviceName.lower().replace(" ","").strip() == thisServiceName.lower().replace(" ","").strip():
                preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
                break
              
              elif serviceName.lower().replace(" ","").strip() == registeredServiceNameMap_dict[thisServiceName].lower().replace(" ","").strip():
                preferredServiceName = registeredServiceNameMap_dict[thisServiceName]
                break
            
            if preferredServiceName != None:
              break
              
      if preferredServiceName == None:
        preferredServiceName = "{}.".format(serviceName)
    
    if dataSource in ["cwAws", "cwUsage", "sq", "health", "ta", "support"]:
      isNativeAws = True
    else:
      isNativeAws = False
      loweredServiceName = serviceName.lower()
      for keyword in ["aws", "amazon", "alexa"]:
        if keyword.lower() in loweredServiceName:
          isNativeAws = True
          break
        
        if isNativeAws == False:
          for keyword in ["IoTDevice", "OpsWorks", "Snowball"]:
            if keyword.lower() in loweredServiceName:
              isNativeAws = True
              break
        
        if isNativeAws == True:
          break
    #logDebug("#preferredServiceName:[{}]->isNativeAws:[{}] with serviceName:[{}] at dataSource:[{}]".format(preferredServiceName, isNativeAws, serviceName, dataSource))
    
    gcNosql = GcNoSQL()
    try:
      preferredServiceName_dict = json.loads(gcNosql.getItem(tableName="serviceInsights", key="global.preferredServiceName_dict"))
    except:
      preferredServiceName_dict = {}
     
    if preferredServiceName in preferredServiceName_dict.keys():
      if dataSource in preferredServiceName_dict[preferredServiceName].keys():
        if serviceName not in preferredServiceName_dict[preferredServiceName][dataSource]:
          preferredServiceName_dict[preferredServiceName][dataSource].append(serviceName)
      else:
        preferredServiceName_dict[preferredServiceName][dataSource] = [serviceName]
    else:
      preferredServiceName_dict[preferredServiceName] = {}
      preferredServiceName_dict[preferredServiceName][dataSource] = [serviceName]
    
    if isNativeAws:
      preferredServiceName_dict[preferredServiceName]["isNativeAws"] = isNativeAws
        
    #actions.saveGlobalPreferredServiceName_dict
    gcNosql.putItem(tableName="serviceInsights", key="global.preferredServiceName_dict", value=preferredServiceName_dict)
                           
    preferredServiceName_list = []
    for thisPreferredServiceName in sorted(preferredServiceName_dict.keys()):
      preferredServiceName_list.append(
        {
          "preferredServiceName": thisPreferredServiceName,
          "isNativeAws": None,
          "cwAws": None,
          "cwUsage": None,
          "cwOthers": None,
          "sq":None,
          "cur":None,
          "health":None,
          "ta":None,
          "support":None,
          "others":None,
          **preferredServiceName_dict[thisPreferredServiceName]
          }
        )
    gcNosql.putItem(tableName="serviceInsights", key="global.preferredServiceNames", value=preferredServiceName_list)
    
    return preferredServiceName
  
  elif serviceName in registeredServiceNameMap_dict.keys():
    return registeredServiceNameMap_dict[serviceName]
  else:
    for thisServiceName in registeredServiceNameMap_dict.keys():
      if serviceName.lower().replace(" ","").strip() == thisServiceName.lower().replace(" ","").strip():
        return registeredServiceNameMap_dict[thisServiceName]
      
      elif serviceName.lower().replace(" ","").strip() == registeredServiceNameMap_dict[thisServiceName].lower().replace(" ","").strip():
        return registeredServiceNameMap_dict[thisServiceName]
    
    for keyword in ["aws-", "amazon-", "service-"]:
      if serviceName.startswith(keyword):
        if serviceName.replace(keyword, "").replace("-","").strip() == thisServiceName.lower().replace(" ","").strip():
          return registeredServiceNameMap_dict[thisServiceName]
        
        elif serviceName.replace(keyword, "").replace("-","").strip() == registeredServiceNameMap_dict[thisServiceName].lower().replace(" ","").strip():
          return registeredServiceNameMap_dict[thisServiceName]
      
        else:
          return "{}.".format(serviceName.replace(keyword, "").strip())
        
    for keyword in ["aws", "Aws", "AWS", "amazon", "Amazon", "AMAZON"]:
      if keyword in serviceName:
        redactedServiceName = "{}.".format(serviceName.replace(keyword, "").strip())
        if redactedServiceName in registeredServiceNameMap_dict.keys():
          return registeredServiceNameMap_dict[redactedServiceName]
        else:
          return "{}.".format(serviceName.replace(keyword, "").strip())
    
    return "{}.".format(serviceName)
  
  
def getServiceNameWithNamespace(serviceName, metricType):
  
  if metricType == "serviceMetric":
    return getPreferredServiceName(serviceName = serviceName, dataSource = "cwAws")
    
  elif metricType == "usageMetric":
    return getPreferredServiceName(serviceName = serviceName, dataSource = "cwUsage")
    
  else:
    return getPreferredServiceName(serviceName = serviceName, dataSource = "cwOthers")
  
def getServiceNameWithServiceQuotas(sqServiceName):
  return getPreferredServiceName(serviceName = sqServiceName, dataSource="sq")
  
def getServiceNameWithCur(curServiceName):
  return getPreferredServiceName(serviceName = curServiceName, dataSource="cur")
  
  
def getServiceNameWithHealth(healthServiceName):
  return getPreferredServiceName(serviceName = healthServiceName, dataSource="health")
  
def getServiceNameWithTa(taServiceName):
  return getPreferredServiceName(serviceName = taServiceName, dataSource="ta")
  
def getServiceNameWithSupportCase(supportServiceName):
  return getPreferredServiceName(serviceName = supportServiceName, dataSource="support")