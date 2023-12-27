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

from graphcode.path import createDir
from graphcode.credentials import *
from graphcode.unittest import *

import copy

class GcDwTemplates():
  def __init__(self):
    logDebug("started")
  
    self.queryStatement_dict = copy.deepcopy(sql_awsdw_dict)
    
  def getQueryTemplate(self, queryStatementName):
    
    if queryStatementName in self.queryStatement_dict.keys():
      return self.queryStatement_dict[queryStatementName]
    else:
      return None
  
  def getDWName(self, queryStatementName):
    queryStatement_dict = self.getQueryTemplate(queryStatementName)
    
    if queryStatement_dict != None:
      return queryStatement_dict['dwName']
    else:
      return None
  
  def getColumnNames(self, queryStatementName):
    queryStatement_dict = self.getQueryTemplate(queryStatementName)
    
    if queryStatement_dict != None:
      return queryStatement_dict['columnNames']
    else:
      return None
    
  def getQueryString(self, queryStatementName):
    queryStatement_dict = self.getQueryTemplate(queryStatementName)
    
    if queryStatement_dict != None:
      return queryStatement_dict['queryString']
    else:
      return None
  
  def updateQueryString(self, queryStatementName, queryString):
    queryStatement_dict = self.getQueryTemplate(queryStatementName)
    
    if queryStatement_dict != None:
      queryStatement_dict['queryString'] = queryString
      
      return True
    else:
      return False
    
sql_awsdw_dict = {}

sql_awsdw_dict['aws_account'] = {'dwName':'awsdw',
                                      'columnNames':['accountId',
                                                     'payerAccountId',
                                                     'customerId',
                                                     'encryptedCustomerId',
                                                     'accountStatusCode',
                                                     'createdBy',
                                                     'createdByClient',
                                                     'creationDate',
                                                     'emailDomain'],
                                      'queryString': 'select distinct  \
                                                        d.account_id, \
                                                        d.payer_account_id, \
                                                        e.customer_id, \
                                                        d.enc_customer_id, \
                                                        d.account_status_code, \
                                                        d.creation_date, \
                                                        d.created_by_client, \
                                                        d.creation_date, \
                                                        email_domain\
                                                      from \
                                                        o_aws_accounts d, \
                                                        d_customers e \
                                                      where \
                                                        d.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                        and d.enc_customer_id = e.enc_customer_id \
                                                      '
                                      }

sql_awsdw_dict['create_temp_accountId_table'] = {'dwName':'awsdw',
                                       'columnNames':['accountId'],
                                       'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                       insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ('699819188465');\
                                       select account_id from TEMP_ACCOUNT_ID_TABLE;"
                                      }


sql_awsdw_dict['none_internal_account'] = {'dwName':'awsdw',
                                      'columnNames':['accountId',
                                                     'payerAccountId',
                                                     'customerId',
                                                     'encryptedCustomerId',
                                                     'accountStatusCode',
                                                     'createdBy',
                                                     'createdByClient',
                                                     'creationDate',
                                                     'emailDomain'],
                                      'queryString': 'select distinct \
                                                        d.account_id, \
                                                        d.payer_account_id, \
                                                        e.customer_id, \
                                                        d.enc_customer_id, \
                                                        d.account_status_code, \
                                                        d.creation_date, \
                                                        d.created_by_client, \
                                                        d.creation_date, \
                                                        email_domain\
                                                      from \
                                                        o_aws_accounts d, \
                                                        d_customers e, \
                                                        o_aws_internal_accounts f \
                                                      where \
                                                        d.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                        and d.enc_customer_id = e.enc_customer_id \
                                                      '
                                      }
                                       
sql_awsdw_dict['internal_account'] = {'dwName':'awsdw',
                                      'columnNames':['accountId',
                                                     'payerAccountId',
                                                     'customerId',
                                                     'encryptedCustomerId',
                                                     'accountStatusCode',
                                                     'isSuppressed',
                                                     'costCenter',
                                                     'primaryOwner',
                                                     'secondOwner',
                                                     'financeOwner',
                                                     'createdBy',
                                                     'createdByClient',
                                                     'creationDate',
                                                     'modifiedDate',
                                                     'modifiedByClient',
                                                     'emailDomain'],
                                      'queryString': 'select distinct \
                                                        f.account_id, \
                                                        d.payer_account_id, \
                                                        e.customer_id, \
                                                        d.enc_customer_id, \
                                                        d.account_status_code, \
                                                        e.status, \
                                                        f.cost_center,  \
                                                        f.owner, \
                                                        f.second_owner, \
                                                        f.finance_owner, \
                                                        f.created_by, \
                                                        f.created_by_client, \
                                                        d.creation_date, \
                                                        least(f.creation_date) as modified_date, \
                                                        f.last_updated_by_client, \
                                                        e.email_domain\
                                                      from \
                                                        o_aws_accounts d, \
                                                        d_customers e, \
                                                        o_aws_internal_accounts f \
                                                      where \
                                                        f.account_id = d.account_id \
                                                        and d.enc_customer_id = e.enc_customer_id \
                                                        and f.end_date IS NULL \
                                                      '
                                      }  
                                     
sql_awsdw_dict['internal_account_list'] = {'dwName':'awsdw',
                                      'columnNames':['accountId',
                                                     'payerAccountId',
                                                     'customerId',
                                                     'encryptedCustomerId',
                                                     'accountStatusCode',
                                                     'isSuppressed',
                                                     'costCenter',
                                                     'primaryOwner',
                                                     'secondOwner',
                                                     'financeOwner',
                                                     'createdBy',
                                                     'createdByClient',
                                                     'creationDate',
                                                     'modifiedDate',
                                                     'modifiedByClient',
                                                     'emailDomain'],
                                      'queryString': 'select distinct \
                                                        f.account_id, \
                                                        d.payer_account_id, \
                                                        e.customer_id, \
                                                        d.enc_customer_id, \
                                                        d.account_status_code, \
                                                        e.status, \
                                                        f.cost_center,  \
                                                        f.owner, \
                                                        f.second_owner, \
                                                        f.finance_owner, \
                                                        f.created_by, \
                                                        f.created_by_client, \
                                                        d.creation_date, \
                                                        least(f.creation_date) as modified_date, \
                                                        f.last_updated_by_client, \
                                                        e.email_domain\
                                                      from \
                                                        o_aws_accounts d, \
                                                        d_customers e, \
                                                        o_aws_internal_accounts f \
                                                      where \
                                                        f.account_id = d.account_id \
                                                        and d.enc_customer_id = e.enc_customer_id \
                                                        and f.end_date IS NULL \
                                                        and d.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                      '
                                      }
                                       
                                      
sql_awsdw_dict['suspended_date_of_external_account'] = {'dwName':'awsdw',
                                                        'columnNames':['f.account_id',
                                                                       'f.cost_center',
                                                                       'd.enc_customer_id',
                                                                       'd.account_status_code',
                                                                       'f.owner',
                                                                       'f.second_owner',
                                                                       'f.finance_owner',
                                                                       'f.created_by',
                                                                       'f.created_by_client',
                                                                       'd.creation_date',
                                                                       'modified_date',
                                                                       'e.email_domain'],
                                                        'queryString': 'select distinct \
                                                                        d.account_id, \
                                                                        d.account_status_code, \
                                                                        d.creation_date, \
                                                                        least(d.last_update_date) as suspended_date\
                                                                      from \
                                                                        o_aws_accounts d, \
                                                                        o_aws_internal_accounts f, \
                                                                        o_aws_cmdb_instances p \
                                                                      where \
                                                                        d.account_id = p.account_id \
                                                                        and d.account_id <> f.account_id \
                                                                        and d.account_status_code <> \'Active\' \
                                                                        and p.shutting_down_time IS NULL \
                                                                        and p.terminated_time IS NULL \
                                                                      '
                                                      }
                                      
sql_awsdw_dict['suspended_date_internal_account'] = {'dwName':'',
                                                         'columnNames':'',
                                                         'queryString':"select distinct \
                                        d.account_id, \
                                        d.account_status_code, \
                                        d.creation_date, \
                                        d.created_by, \
                                        d.created_by_client, \
                                        least(d.last_update_date) as suspended_date, \
                                        d.last_updated_by, \
                                        d.last_updated_by_client\
                                      from \
                                        o_aws_accounts d, \
                                        o_aws_internal_accounts f, \
                                        o_aws_cmdb_instances p \
                                      where \
                                        f.account_id = d.account_id \
                                        and f.account_id  = p.account_id \
                                        and d.account_status_code <> 'Active' \
                                        and p.shutting_down_time IS NULL \
                                        and p.terminated_time IS NULL \
                                      "
                                      }


sql_awsdw_dict['suspended_ec2_instances'] = {'dwName':'awsdw',
                                   'columnNames':['accountId',
                                                  'accountStatusCod',
                                                  'location',
                                                  'customer_instance_id',
                                                  'customer_availability_zone',
                                                  'p.droplet_ip',
                                                  'dedicated',
                                                  'instance_type',
                                                  'billing_product_ids',
                                                  'external_billing_products',
                                                  'pending_time',
                                                  'running_time',
                                                  'shutting_down_time',
                                                  'terminated_time',
                                                  'creationDate',
                                                  'cretedBy',
                                                  'createByClient',
                                                  'lastModifiedDate',
                                                  'lastModifiedBy',
                                                  'lastModifiedClient'
                                                  ],
                                   'queryString':"select distinct \
                                        d.account_id, \
                                        d.account_status_code, \
                                        p.location, \
                                        p.customer_instance_id, \
                                        p.customer_availability_zone, \
                                        p.droplet_ip, \
                                        p.dedicated, \
                                        p.instance_type, \
                                        p.billing_product_ids, \
                                        p.external_billing_products, \
                                        p.pending_time, \
                                        p.running_time, \
                                        p.shutting_down_time, \
                                        p.terminated_time, \
                                        d.creation_date, \
                                        d.created_by, \
                                        d.created_by_client, \
                                        least(d.last_update_date) as suspended_date, \
                                        d.last_updated_by, \
                                        d.last_updated_by_client\
                                      from \
                                        o_aws_accounts d, \
                                        o_aws_internal_accounts f, \
                                        o_daily_aws_usage_history g, \
                                        o_aws_cmdb_instances p \
                                      where \
                                        g.REQUEST_DAY = '2020-10-01 00:00:00' \
                                        and least(d.last_update_date) < '2020-06-01 00:00:00' \
                                        and g.product_code = 'AmazonEC2' \
                                        and g.account_id = f.account_id \
                                        and f.account_id = d.account_id \
                                        and f.account_id  = p.account_id \
                                        and d.account_status_code <> 'Active' \
                                        and p.shutting_down_time IS NULL \
                                        and p.terminated_time IS NULL \
                                      "
                                      }

sql_awsdw_dict['list_active_ec2_instances'] = {'dwName':'awsdw',
                                   'columnNames':['accountId',
                                                  'accountStatusCode',
                                                  'location',
                                                  'instanceId',
                                                  'availabilityZone',
                                                  'dropletIp',
                                                  'dedicatedTenancy',
                                                  'instanceType',
                                                  'billing_product_ids',
                                                  'external_billing_products',
                                                  'pendingTime',
                                                  'runningTime',
                                                  'shuttingDownTime',
                                                  'terminatedTime',
                                                  'stateChangeMessage',
                                                  'dwStartDate',
                                                  'dwSnapshotDate'
                                                  ],
                                   'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                       insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                       select distinct \
                                        d.account_id, \
                                        d.account_status_code, \
                                        p.location, \
                                        p.customer_instance_id, \
                                        p.customer_availability_zone, \
                                        p.droplet_ip, \
                                        p.dedicated, \
                                        p.instance_type, \
                                        p.billing_product_ids, \
                                        p.external_billing_products, \
                                        p.pending_time, \
                                        p.running_time, \
                                        p.shutting_down_time, \
                                        p.terminated_time ,\
                                        p.state_change_message, \
                                        p.dw_create_date, \
                                        least(p.dw_update_date) as dw_update_date \
                                      from \
                                        o_aws_accounts d, \
                                        o_aws_cmdb_instances p, \
                                        o_aws_internal_accounts f, \
                                        TEMP_ACCOUNT_ID_TABLE t \
                                      where \
                                        f.account_id = t.account_id \
                                        and f.account_id = d.account_id \
                                        and f.account_id  = p.account_id \
                                        and p.shutting_down_time IS NULL \
                                        and p.terminated_time IS NULL \
                                        and p.dw_update_date >= '${{DW_SNAPSHOT_DATE}}' \
                                      "
                                      }

sql_awsdw_dict['list_ec2_instances'] = {'dwName':'awsdw',
                                   'columnNames':['accountId',
                                                  'accountStatusCode',
                                                  'location',
                                                  'instanceId',
                                                  'availabilityZone',
                                                  'dropletIp',
                                                  'dedicatedTenancy',
                                                  'instanceType',
                                                  'billing_product_ids',
                                                  'external_billing_products',
                                                  'pendingTime',
                                                  'runningTime',
                                                  'shuttingDownTime',
                                                  'terminatedTime',
                                                  'stateChangeMessage',
                                                  'dwStartDate',
                                                  'dwSnapshotDate'
                                                  ],
                                   'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                       insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                       select distinct \
                                        d.account_id, \
                                        d.account_status_code, \
                                        p.location, \
                                        p.customer_instance_id, \
                                        p.customer_availability_zone, \
                                        p.droplet_ip, \
                                        p.dedicated, \
                                        p.instance_type, \
                                        p.billing_product_ids, \
                                        p.external_billing_products, \
                                        p.pending_time, \
                                        p.running_time, \
                                        p.shutting_down_time, \
                                        p.terminated_time, \
                                        p.state_change_message, \
                                        p.dw_create_date, \
                                        least(p.dw_update_date) as dw_update_date \
                                      from \
                                        o_aws_accounts d, \
                                        o_aws_cmdb_instances p, \
                                        o_aws_internal_accounts f, \
                                        TEMP_ACCOUNT_ID_TABLE t \
                                      where \
                                        f.account_id = t.account_id \
                                        and f.account_id = d.account_id \
                                        and f.account_id  = p.account_id \
                                        and p.running_time >= '${{START_DATE}}' \
                                        and p.running_time <= '${{END_DATE}}' \
                                        and p.shutting_down_time  >= '${{START_DATE}}' or p.shutting_down_time IS NULL \
                                        and p.terminated_time >= '${{START_DATE}}' or p.terminated_time IS NULL \
                                        and p.dw_update_date >= '${{START_DATE}}' \
                                        and p.dw_update_date <= '${{END_DATE}}' \
                                      limit 1000 \
                                      "
                                      }


sql_awsdw_dict['list_active_paid_licenced_ec2_instances'] = {'dwName':'awsdw',
                                   'columnNames':['accountId',
                                                  'accountStatusCode',
                                                  'location',
                                                  'instanceId',
                                                  'availabilityZone',
                                                  'dropletIp',
                                                  'dedicatedTenancy',
                                                  'instanceType',
                                                  'billing_product_ids',
                                                  'external_billing_products',
                                                  'pendingTime',
                                                  'runningTime',
                                                  'shuttingDownTime',
                                                  'terminatedTime',
                                                  'stateChangeMessage',
                                                  'dwStartDate',
                                                  'dwSnapshotDate'
                                                  ],
                                   'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                       insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                       select distinct \
                                        p.account_id, \
                                        p.location, \
                                        p.customer_instance_id, \
                                        p.customer_availability_zone, \
                                        p.droplet_ip, \
                                        p.dedicated, \
                                        p.instance_type, \
                                        p.billing_product_ids, \
                                        p.external_billing_products, \
                                        p.pending_time, \
                                        p.running_time, \
                                        p.shutting_down_time, \
                                        p.terminated_time, \
                                        p.state_change_message, \
                                        p.dw_create_date, \
                                        least(p.dw_update_date) as dw_update_date \
                                      from \
                                        o_aws_cmdb_instances p, \
                                        TEMP_ACCOUNT_ID_TABLE t \
                                      where \
                                        p.account_id in (select account_id from TEMP_ACCOUNT_ID_TABLE) \
                                        and p.external_billing_products <> '' \
                                        and p.shutting_down_time IS NULL \
                                        and p.terminated_time IS NULL \
                                        and p.dw_update_date >= '${{END_DATE}}' \
                                      "
                                      }

sql_awsdw_dict['list_ec2_classic_instances'] = {'dwName':'awsdw',
                                   'columnNames':['instanceId',
                                                  'accountId',
                                                  'accountStatusCode',
                                                  'isDedicated',
                                                  'isVpc',
                                                  'instanceType',
                                                  'availabilityZone',
                                                  'pendingTime',
                                                  'runningTime',
                                                  'shuttingDownTime',
                                                  'terminatedTime'
                                                  ],
                                   'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};
select distinct 
   p.customer_instance_id, 
   p.account_id, 
   d.account_status_code, 
   p.dedicated, 
   p.is_vpc, 
   p.instance_type, 
   p.customer_availability_zone, 
   p.pending_time, 
   p.running_time, 
   p.shutting_down_time, 
   p.terminated_time 
from 
   o_aws_accounts d, 
   o_aws_cmdb_instances p, 
   TEMP_ACCOUNT_ID_TABLE t 
where 
   (p.terminated_time IS NULL or p.terminated_time > '${{START_DATE}}') 
   and (p.shutting_down_time IS NULL or p.shutting_down_time > '${{START_DATE}}') 
   and p.is_vpc is not TRUE 
   and p.account_id = t.account_id 
   and t.account_id = d.account_id 
"""
                                      }

sql_awsdw_dict['ec2_in_EC2_CLASSIC'] = {'dwName':'awsdw',
                                                         'columnNames':['customer_instance_id',
                                                                        'account_id',
                                                                        'is_dedicated',
                                                                        'is_vpc',
                                                                        'instance_type',
                                                                        'customer_availability_zone',
                                                                        'pending_time',
                                                                        'running_time',
                                                                        'shutting_down_time',
                                                                        'terminated_time'
                                                                        ],
                                                         'queryString':"select distinct \
                                                            p.customer_instance_id, \
                                                            p.account_id, \
                                                            p.dedicated, \
                                                            p.is_vpc, \
                                                            p.instance_type, \
                                                            p.customer_availability_zone, \
                                                            p.pending_time, \
                                                            p.running_time, \
                                                            p.shutting_down_time, \
                                                            p.terminated_time \
                                                          from \
                                                            o_aws_cmdb_instances p \
                                                          where \
                                                            p.terminated_time IS NULL \
                                                            and p.shutting_down_time IS NULL \
                                                            and p.is_vpc is not TRUE \
                                                            and p.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                          "
                                                          }
                                                          

sql_awsdw_dict['ec2_in_EC2_CLASSIC_INTERNAL'] = {'dwName':'awsdw',
                                                         'columnNames':['customer_instance_id',
                                                                        'account_id',
                                                                        'is_dedicated',
                                                                        'is_vpc',
                                                                        'instance_type',
                                                                        'customer_availability_zone',
                                                                        'pending_time',
                                                                        'running_time',
                                                                        'shutting_down_time',
                                                                        'terminated_time'
                                                                        ],
                                                         'queryString':"select distinct \
                                                            p.customer_instance_id, \
                                                            p.account_id, \
                                                            p.dedicated, \
                                                            p.is_vpc, \
                                                            p.instance_type, \
                                                            p.customer_availability_zone, \
                                                            p.pending_time, \
                                                            p.running_time, \
                                                            p.shutting_down_time, \
                                                            p.terminated_time \
                                                          from \
                                                            o_aws_cmdb_instances p, \
                                                            o_aws_internal_accounts f \
                                                          where \
                                                            p.terminated_time IS NULL \
                                                            and p.shutting_down_time IS NULL \
                                                            and p.is_vpc is not TRUE \
                                                            and p.account_id = f.account_id \
                                                          "
                                                          }
                                                          

                                          
sql_awsdw_dict['monthlyEc2RIUtilization'] = { 'dwName':'awsdw',
                                               'columnNames':['date',
                                                              'subscriptionId',
                                                              'offeringId',
                                                              'leaseId',
                                                              'instanceType',
                                                              'regionName',
                                                              'riType',
                                                              'raw_instance_hours',
                                                              'committed_hrs_normalized',
                                                              'used_hrs_normalized'
                                                            ],
                                               'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                            insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                            SELECT f.month_begin_date \
                                                            , acc.account_id \
                                                            , l.subscription_id \
                                                            , l.offering_id \
                                                            , l.lease_id \
                                                            , l.instance_type \
                                                            , act.region \
                                                            , l.ri_type_desc \
                                                            , SUM(f.ec2-inst_hrs_raw) AS raw_hours \
                                                            , SUM(f.ec2_inst_committed_hrs_normalized) AS committed_hrs_normalized \
                                                            , SUM(f.ec2_inst_hrs_normalized) AS used_hrs_normalized \
                                                        FROM TEMP_ACCOUNT_ID_TABLE t, \
                                                          ec2_dm.fact_aws_monthly_est_revenue f \
                                                            INNER JOIN ec2_dm.dim_aws_activity_types act ON f.activity_type_id = act.activity_type_id \
                                                            INNER JOIN ec2_dm.dim_ec2_accounts acc ON f.account_seq_id = acc.account_seq_id \
                                                            LEFT JOIN  ec2_dm.dim_ec2_ri_leases l ON f.subscription_seq_id = l.subscription_seq_id \
                                                        WHERE act.biz_product_group = 'EC2' \
                                                          AND act.biz_product_name IN ('EC2 Instance Usage', 'EC2 RI Leases', 'EC2 Host Usage') \
                                                          AND acc.account_id IN (${{ACCOUNT_ID_LIST}}) \
                                                          AND acc.is_fraud_flag = 'N' \
                                                          AND f.is_compromised_flag = 'N' \
                                                          AND f.pricing_model = 'RI' \
                                                          AND f.ec2_inst_committed_hrs_normalized IS NOT NULL \
                                                          AND f.ec2_inst_committed_hrs_normalized IS NOT NULL \
                                                          AND computation_date BETWEEN '${{START_DATE}}' AND '${{END_DATE}}' \
                                                        GROUP BY 1, 2, 3, 4, 5, 6, 7, 8 \
                                                        ; \
                                                        "
                                                        }


sql_awsdw_dict['dailyEc2RIUtilization'] = {'dwName':'awsdw',
                                           'columnNames':['date',
                                                          'payerAccountId',
                                                          'accountId',
                                                          'regionName',
                                                          'instanceType',
                                                          'billingMode',
                                                          'raw_instance_hours',
                                                          'committed_hrs_normalized',
                                                          'used_hrs_normalized'
                                                        ],
                                           'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                          insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                          SELECT f.computation_date \
                                                          , acc.payer_account_id \
                                                          , acc.account_id \
                                                          , act.region \
                                                          , l.instance_type \
                                                          , f.pricing_model \
                                                          , SUM(f.ec2_inst_hrs_raw) AS raw_hours \
                                                          , SUM(f.ec2_inst_committed_hrs_normalized) AS committed_hrs_normalized \
                                                          , SUM(f.ec2_inst_hrs_normalized) AS used_hrs_normalized \
                                                      FROM \
                                                        TEMP_ACCOUNT_ID_TABLE t, \
                                                        ec2_dm.fact_aws_daily_est_revenue_last2months f \
                                                          left Join ec2_dm.dim_ec2_ri_leases l ON f.subscription_seq_id = l.subscription_seq_id \
                                                            INNER JOIN ec2_dm.dim_aws_activity_types act ON f.activity_type_id = act.activity_type_id \
                                                            INNER JOIN ec2_dm.dim_ec2_accounts acc ON f.account_seq_id = acc.account_seq_id \
                                                      WHERE act.biz_product_group = 'EC2' \
                                                        AND act.biz_product_name IN ('EC2 Instance Usage', 'EC2 RI Leases', 'EC2 Host Usage') \
                                                        AND acc.account_id = t.account_id \
                                                        AND acc.is_fraud_flag = 'N' \
                                                        AND f.is_compromised_flag = 'N' \
                                                        AND f.pricing_model = 'RI' \
                                                        AND f.computation_date BETWEEN '${{START_DATE}}' AND '${{END_DATE}}' \
                                                      GROUP BY 1, 2, 3, 4, 5, 6 \
                                                      ORDER BY f.computation_date \
                                                      ; \
                                                    "
                                                    }

sql_awsdw_dict['dailyEc2RIUtilizationDetails'] = {'dwName':'awsdw',
                                           'columnNames':['date',
                                                          'payerAccountId',
                                                          'accountId',
                                                          'regionName',
                                                          'subscriptionId',
                                                          'offeringId',
                                                          'leaseId',
                                                          'instanceType',
                                                          'riType',
                                                          'raw_instance_hours',
                                                          'committed_hrs_normalized',
                                                          'used_hrs_normalized' ,
                                                        ],
                                           'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                          insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                          SELECT f.computation_date \
                                                          , acc.payer_account_id \
                                                          , acc.account_id \
                                                          , acc.region \
                                                          , l.subscription_id \
                                                          , l.offering_id \
                                                          , l.lease_id \
                                                          , l.instance_type \
                                                          , l.ri_type_desc \
                                                          , SUM(f.ec2_inst_hrs_raw) AS raw_hours \
                                                          , SUM(f.ec2_inst_committed_hrs_normalized) AS committed_hrs_normalized \
                                                          , SUM(f.ec2_inst_hrs_normalized) AS used_hrs_normalized \
                                                      FROM \
                                                        TEMP_ACCOUNT_ID_TABLE t, \
                                                        ec2_dm.fact_aws_daily_est_revenue_last2months f \
                                                          left Join ec2_dm.dim_ec2_ri_leases l ON f.subscription_seq_id = l.subscription_seq_id \
                                                            INNER JOIN ec2_dm.dim_aws_activity_types act ON f.activity_type_id = act.activity_type_id \
                                                            INNER JOIN ec2_dm.dim_ec2_accounts acc ON f.account_seq_id = acc.account_seq_id \
                                                      WHERE act.biz_product_group = 'EC2' \
                                                        AND act.biz_product_name IN ('EC2 Instance Usage', 'EC2 RI Leases', 'EC2 Host Usage') \
                                                        AND acc.account_id = t.account_id \
                                                        AND acc.is_fraud_flag = 'N' \
                                                        AND f.is_compromised_flag = 'N' \
                                                        AND f.pricing_model = 'RI' \
                                                        AND f.computation_date BETWEEN '${{START_DATE}}' AND '${{END_DATE}}' \
                                                      GROUP BY 1, 2, 3, 4, 5, 6, 7, 8 \
                                                      ORDER BY f.computation_date \
                                                      ; \
                                                    "
                                                    }

sql_awsdw_dict['dailyEc2OdUsage'] = {'dwName':'awsdw',
                                   'columnNames':['date',
                                                  'payerAccountId',
                                                  'accountId',
                                                  'regionName',
                                                  'instanceType',
                                                  'billingMode',
                                                  'raw_instance_hours',
                                                  'used_hrs_normalized'
                                                ],
                                   'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                  insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                  select fact.computation_date \
                                                    , acc.payer_account_id \
                                                    , acc.account_id \
                                                    , usage.region \
                                                    , usage.resource_type \
                                                    , fact.pricing_model \
                                                    , sum(fact.ec2_inst_hrs_raw) as sum_raw \
                                                    , sum(fact.ec2_inst_hrs_normalized) as sum_normalized \
                                                  from \
                                                      TEMP_ACCOUNT_ID_TABLE t \
                                                      , ec2_dm.fact_aws_daily_est_revenue_last2months fact \
                                                      , ec2_dm.dim_ec2_accounts acc \
                                                      , ec2_dm.dim_ec2_usage_types usage \
                                                  where fact.account_seq_id = acc.account_seq_id \
                                                    and   fact.usage_type_seq_id = usage.usage_type_seq_id \
                                                    and   acc.account_id =  t.account_id \
                                                    and   fact.computation_date BETWEEN '${{START_DATE}}' AND '${{END_DATE}}' \
                                                    and   usage.primary_usage_type='Instance Usage' \
                                                    and   fact.pricing_model = 'OD' \
                                                    group by  1,  2, 3, 4, 5, 6 \
                                                    ORDER BY fact.computation_date \
                                                    ; \
                                            "
                                            }


                                                                                                                    
sql_awsdw_dict['ebsSnapshotUsage'] = { 'dwName':'awsdw',
                                                                 'columnNames':['account_id',
                                                                                'usage_type',
                                                                                'usage_value',
                                                                                'usage_resource'
                                                                              ],
                                                                 'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};
select distinct 
  g.account_id, 
  g.usage_type,
  g.usage_value,
  g.usage_resource
from 
  o_daily_aws_usage_history g 
where g.account_id in (select distinct t.account_id from TEMP_ACCOUNT_ID_TABLE t)
  and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}'
  and g.usage_type like '%EBS:SnapshotUsage'
limit 5
"""
}
                                                                                                                     
sql_awsdw_dict['awsProductNamesByusageWithInternalAccounts'] = { 'dwName':'awsdw',
                                                                 'columnNames':['account_id',
                                                                                'product_name',
                                                                                'region_name'
                                                                              ],
                                                                 'queryString':"select distinct \
                                                                    g.account_id, \
                                                                    g.product_code, \
                                                                    g.availability_zone \
                                                                  from \
                                                                    o_aws_internal_accounts f, \
                                                                    o_daily_aws_usage_history g \
                                                                  where f.end_date IS NULL \
                                                                    and g.account_id = f.account_id \
                                                                    and g.REQUEST_DAY >= '${{START_DATE}}' \
                                                                    and g.REQUEST_DAY >= '${{END_DATE}}' \
                                                                  order by g.account_id, g.product_code, g.availability_zone \
                                                                  limit 5000000 \
                                                                  "
                                                                  }
                                          
sql_awsdw_dict['awsProductNamesByusage'] = { 'dwName':'awsdw',
                                             'columnNames':['account_id',
                                                            'product_name',
                                                            'region_name'
                                                          ],
                                             'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                          insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                          select distinct \
                                                            g.account_id, \
                                                            g.product_code, \
                                                            g.availability_zone \
                                                          from \
                                                            o_daily_aws_usage_history g \
                                                          where g.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                            and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}' \
                                                          order by g.account_id, g.product_code, g.availability_zone \
                                                          limit 5000000 \
                                                          "
                                                          }
         
sql_awsdw_dict['awsProductUsageByAccountId'] = { 'dwName':'awsdw',
                                             'columnNames':['account_id',
                                                            'product_name',
                                                            'region_name'
                                                          ],
                                             'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                          insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                          select distinct \
                                                            g.account_id, \
                                                            g.product_code, \
                                                            g.availability_zone \
                                                          from \
                                                            TEMP_ACCOUNT_ID_TABLE t, \
                                                            o_daily_aws_usage_history g \
                                                          where g.account_id = t.account_id \
                                                            and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}' \
                                                            and g.usage_value > 0 \
                                                          order by g.account_id, g.product_code, g.availability_zone; \
                                                          "
                                                          }

sql_awsdw_dict['awsProductUsageByProductName'] = { 'dwName':'awsdw',
                                             'columnNames':['account_id',
                                                            'product_name',
                                                            'region_name'
                                                          ],
                                             'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL); \
                                                          insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}}; \
                                                          select distinct \
                                                            g.account_id, \
                                                            g.product_code, \
                                                            g.availability_zone \
                                                          from \
                                                            TEMP_ACCOUNT_ID_TABLE t, \
                                                            o_daily_aws_usage_history g \
                                                          where g.account_id = t.account_id \
                                                            and g.product_code like '%${{PRODUCT_NAME}}%' \
                                                            and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}' \
                                                            and g.usage_value > 0 \
                                                          order by g.account_id, g.product_code, g.availability_zone; \
                                                          "
                                                          }
                                                
sql_awsdw_dict['awsResourcesByUsageOfInternalAccounts'] = { 'dwName':'awsdw',
                                             'columnNames':['account_id',
                                                            'product_name',
                                                            'region_name'
                                                          ],
                                             'queryString':"select distinct \
                                                g.account_id, \
                                                g.product_code, \
                                                g.availability_zone \
                                              from \
                                                o_aws_internal_accounts f, \
                                                o_daily_aws_usage_history g\
                                              where f.end_date IS NULL \
                                                and f.account_id = g.account_id \
                                                and g.REQUEST_DAY >= '${{START_DATE}}' \
                                                and g.REQUEST_DAY <= '${{END_DATE}}' \
                                                and g.usage_value > 0 \
                                              order by g.account_id, g.product_code, g.availability_zone \
                                              limit 5000000 \
                                              "
                                              }
                                                        
sql_awsdw_dict['aws_usage_of_suspended_accounts'] = {'dwName':'',
                                                         'columnNames':'',
                                                         'queryString':"select distinct g.account_id, d.account_status_code, least(d.last_update_date) as suspended_date, g.product_code, g.operation, g.availability_zone, \
                                                        g.usage_type, g.usage_value, g.usage_resource, g.request_day \
                                                        from \
                                                        o_aws_accounts d, \
                                                        o_aws_internal_accounts f, \
                                                        o_daily_aws_usage_history g \
                                                        where g.REQUEST_DAY = '2017-11-12 00:00:00' \
                                                        and least(d.last_update_date) < '2017-07-01 00:00:00' \
                                                        and f.account_id = g.account_id \
                                                        and f.account_id = d.account_id \
                                                        and d.account_status_code = 'Suspended' \
                                                        order by suspended_date \
                                                        limit 1000000 \
                                                        "
                                                        }

sql_awsdw_dict['serviceUsages'] = {'dwName':'awsdw',
                               'columnNames':['accountId',
                                    'serviceName',
                                    'operation', 
                                    'availability_zone', 
                                    'usage_type', 
                                    'usage_value', 
                                    'usage_resource', 
                                    'request_day' 
                                  ],
                              'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};
select distinct g.account_id,
  g.product_code, 
  g.operation, 
  g.availability_zone, 
  g.usage_type, 
  g.usage_value, 
  g.usage_resource, 
  g.request_day 
from 
  o_daily_aws_usage_history g  
where 
  g.product_code = '${{SERVICENAME}}'
  and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}'  
  and g.account_id in (select account_id from TEMP_ACCOUNT_ID_TABLE)
"""
}

sql_awsdw_dict['serviceRegionCodes'] = {'dwName':'awsdw',
                               'columnNames':['accountId',
                                    'serviceName',
                                    'availabilityZone', 
                                  ],
                              'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};
select distinct g.account_id,
  g.product_code, 
  g.availability_zone, 
  g.usage_type, 
  g.usage_value, 
  g.usage_resource, 
  g.request_day 
from 
  o_daily_aws_usage_history g  
where 
  g.product_code = '${{SERVICENAME}}'
  and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}'  
  and g.account_id in (select account_id from TEMP_ACCOUNT_ID_TABLE)
  and g.usage_value <> 0
"""
}

sql_awsdw_dict['activeServiceResources'] = {'dwName':'awsdw',
                                       'columnNames':['accountId',
                                                      'availabilityZone',
                                                      'usageResouce',
                                                      'usageType',
                                                      'operation',
                                                      'usageValue',
                                                    ],
                                       'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}}; 
select distinct g.account_id,g.availability_zone, g.usage_resource,g.usage_type,g.operation,sum(g.usage_value) as usage_value
from
  o_daily_aws_usage_history g
where 
  g.product_code = '${{SERVICENAME}}'
  and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}'
  and g.account_id in (select account_id from TEMP_ACCOUNT_ID_TABLE)
  and g.usage_type like '${{USAGE_TYPE}}'
  and g.usage_resource <> ''
  and g.usage_value <> 0
group by g.account_id,g.availability_zone,g.usage_resource,g.usage_type,g.operation
order by usage_value desc
"""
}


sql_awsdw_dict['activeS3resouces'] = {'dwName':'awsdw',
                                       'columnNames':['accountId',
                                                      'usageResouce',
                                                      'usageType',
                                                      'operation',
                                                      'usageValue',
                                                    ],
                                       'queryString':"""create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);
insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}}; 
select distinct g.account_id,g.usage_resource,g.usage_type,g.operation,sum(g.usage_value) as usage_value
from
  o_daily_aws_usage_history g
where 
  g.product_code = 'AmazonS3'
  and g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}'
  and g.account_id in (select account_id from TEMP_ACCOUNT_ID_TABLE)
  and g.usage_type like '%DataTransfer-In-Bytes'
  and g.usage_resource <> ''
group by g.account_id,g.usage_resource,g.usage_type,g.operation
order by usage_value desc
"""
}

sql_awsdw_dict['accessed_accounts'] = {'dwName':'awsdw',
                               'columnNames':['accountId'
                                  ],
                              'queryString':"create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                            insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                            select distinct g.account_id \
                                            from \
                                              TEMP_ACCOUNT_ID_TABLE t, \
                                              o_daily_aws_usage_history g  \
                                            where \
                                              g.REQUEST_DAY between '${{START_DATE}}' and '${{END_DATE}}' \
                                              and g.account_id = t.account_id \
                                              and g.usage_value > 0 \
                                "
                              }

                                                        
sql_awsdw_dict['ec2_instances_of_suspended_accounts'] = {'dwName':'',
                                                         'columnNames':'',
                                                         'queryString':"SELECT distinct \
                                                           p.account_id, \
                                                           d.account_status_code, \
                                                           d.last_update_date, \
                                                           p.customer_instance_id, \
                                                           p.instance_type, \
                                                           p.customer_availability_zone, \
                                                           p.pending_time, \
                                                           p.running_time, \
                                                           p.shutting_down_time, \
                                                           p.terminated_time \
                                                        From \
                                                          o_aws_accounts d, \
                                                          o_aws_internal_accounts f, \
                                                          o_aws_cmdb_instances p \
                                                        Where \
                                                          p.shutting_down_time IS NOT NULL \
                                                          and p.terminated_time IS NOT NULL \
                                                          and d.account_status_code = 'Suspended' \
                                                          and d.account_id = p.account_id \
                                                          and d.account_id = f.account_id \
                                                        "
                                                        }
                                                        
sql_awsdw_dict['aws_support_level'] =  {'dwName':'awsdw',
                                        'columnNames':['accountId',
                                                       'supportProduct'
                                                       ],
                                        'queryString':"select distinct \
                                          b.product_name\
                                        from \
                                          O_AWS_PRODUCT_OFFERINGS a,\
                                          o_aws_products b, \
                                          o_aws_subscriptions c, \
                                          o_aws_accounts d, \
                                          d_customers e, \
                                          o_aws_internal_accounts f \
                                        where \
                                          a.product_id = b.product_id \
                                          and b.product_name like '%Support%' \
                                          and b.product_name like 'AWS%' \
                                          and f.account_id = d.account_id \
                                          and d.account_id = c.account_id \
                                          and d.enc_customer_id = e.enc_customer_id \
                                          and a.offering_id = c.offering_id \
                                          and c.account_id = d.account_id \
                                          and d.enc_customer_id = e.enc_customer_id  \
                                          and c.end_date is null \
                                        "
                                        }

sql_awsdw_dict['aws_support_level_with_accountIds'] = {'dwName':'awsdw',
                                        'columnNames':['accountId',
                                                       'supportProduct'
                                                       ],
                                        'queryString':"select distinct \
                                          d.account_id, \
                                          b.product_name\
                                        from \
                                          O_AWS_PRODUCT_OFFERINGS a,\
                                          o_aws_products b, \
                                          o_aws_subscriptions c, \
                                          o_aws_accounts d, \
                                          d_customers e \
                                        where \
                                          a.product_id = b.product_id \
                                          and b.product_name like '%Support%' \
                                          and b.product_name like 'AWS%' \
                                          and d.account_id in (${{ACCOUNT_ID_LIST}}) \
                                          and d.account_id = c.account_id \
                                          and d.enc_customer_id = e.enc_customer_id \
                                          and a.offering_id = c.offering_id \
                                          and c.account_id = d.account_id \
                                          and d.enc_customer_id = e.enc_customer_id  \
                                          and c.end_date is null \
                                        "
                                        }

sql_awsdw_dict['case_details_with_account_ids'] = {'dwName': 'awssupportdw',
                                                   'columnNames': ['case_id',
                                                                  'account_id',
                                                                  #'merchant_name',
                                                                  'category_name',
                                                                  'case_type_name',
                                                                  'reason',
                                                                  #'case_description',
                                                                  'creation_date_utc',
                                                                  'case_resolve_date_utc',
                                                                  'first_outbound_date_utc',
                                                                  'case_status_name',
                                                                  'severity',
                                                                  'missed',
                                                                  ],
                                                   'queryString': "SELECT \
                                                                     cd.CASE_ID, \
                                                                     cust.account_id,\
                                                                     " 
                                                                     # ALT_MERCHANT_NAME, \
                                                                     + "\
                                                                     REPLACE(REPLACE(CATEGORY_NAME,'AWS ',''),'Amazon ','') as \"Category_Name\" ,\
                                                                     cd.case_type_name, \
                                                                     cd.REASON, \
                                                                     "
                                                                     # CASE_DESCRIPTION, \
                                                                     + "\
                                                                     CREATION_DATE_UTC, \
                                                                     CASE_RESOLVE_DATE_UTC, \
                                                                     first_outbound_date_utc, \
                                                                     CASE_STATUS_NAME, \
                                                                     SEVERITY , \
                                                                     CASE \
                                                                       WHEN (response_sla_minutes -(EXTRACT(EPOCH FROM first_outbound_date_utc - creation_date_utc)) / 60 >= 0) OR (first_outbound_date_utc IS NULL) THEN 0 \
                                                                       ELSE 1 \
                                                                     END as missed \
                                                                    FROM aws_kumo.d_case_details cd \
                                                                    JOIN dm_billing.d_customers cust ON cd.merchant_customer_id = cust.customer_id \
                                                                    WHERE cust.account_id IN (${{ACCOUNT_ID_LIST}})\
                                                                      AND   cd.creation_date_utc <> case_resolve_date_utc \
                                                                      AND   cd.creation_date_utc <> first_outbound_date_utc \
                                                                      AND   cd.creation_date_utc BETWEEN DATE ('${{START_DATE}}') AND DATE ('${{END_DATE}}') \
                                                                      order by cd.creation_date_utc desc \
                                                                    "
                                                }


sql_awsdw_dict['case_details_with_account_ids_v2'] = {'dwName': 'awssupportdw',
                                                   'columnNames': ['case_id',
                                                                  'account_id',
                                                                  #'merchant_name',
                                                                  'category_name',
                                                                  'case_type_name',
                                                                  'case_resolution_category',
                                                                  'case_topic',
                                                                  'reason',
                                                                  #'case_description',
                                                                  'creation_date_utc',
                                                                  'case_resolve_date_utc',
                                                                  'first_outbound_date_utc',
                                                                  'case_status_name',
                                                                  'severity',
                                                                  'missed',
                                                                  'resolver',
                                                                  'inboundPhone',
                                                                  'outboundPhone',
                                                                  'inboundEmail',
                                                                  'outboundEmail',
                                                                  'last_inbound_date_pst',
                                                                  'last_outbound_date_pst',
                                                                  'first_outbound_date_pst',
                                                                  'ttr_days',
                                                                  'no_of_inbound_phone_contacts',
                                                                  'no_of_outbound_phone_contacts',
                                                                  'no_of_inbound_email_contacts',
                                                                  'no_of_outbound_email_contacts',
                                                                  'angry_case',
                                                                  'is_reopen',
                                                                  'ever_severity_upgrade',
                                                                  'ever_severity_downgrade',
                                                                  'owning_agent_login_id'
                                                                  ],
                                                   'queryString': "create temp table TEMP_ACCOUNT_ID_TABLE (account_id VARCHAR (30) NOT NULL);\
                                                                    insert into TEMP_ACCOUNT_ID_TABLE(account_id) values ${{ACCOUNT_ID_LIST}};\
                                                                    SELECT \
                                                                     cd.CASE_ID, \
                                                                     cust.account_id,\
                                                                     " 
                                                                     # ALT_MERCHANT_NAME, \
                                                                     + "\
                                                                     REPLACE(REPLACE(CATEGORY_NAME,'AWS ',''),'Amazon ','') as \"Category_Name\" ,\
                                                                     cd.case_type_name, \
                                                                     cd.case_resolution_category, \
                                                                     cd.case_topic, \
                                                                     cd.REASON, \
                                                                     "
                                                                     # CASE_DESCRIPTION, \
                                                                     + "\
                                                                     CREATION_DATE_UTC, \
                                                                     CASE_RESOLVE_DATE_UTC, \
                                                                     first_outbound_date_utc, \
                                                                     CASE_STATUS_NAME, \
                                                                     SEVERITY , \
                                                                     CASE \
                                                                       WHEN (response_sla_minutes -(EXTRACT(EPOCH FROM first_outbound_date_utc - creation_date_utc)) / 60 >= 0) OR (first_outbound_date_utc IS NULL) THEN 0 \
                                                                       ELSE 1 \
                                                                     END as missed, \
                                                                     cd.resolver, \
                                                                     cd.no_of_inbound_phone_contacts, \
                                                                     cd.no_of_outbound_phone_contacts, \
                                                                     cd.no_of_inbound_email_contacts, \
                                                                     cd.no_of_outbound_email_contacts, \
                                                                     last_inbound_date_pst, \
                                                                     last_outbound_date_pst, \
                                                                     first_outbound_date_pst, \
                                                                     ttr_days, \
                                                                     no_of_inbound_phone_contacts, \
                                                                     no_of_outbound_phone_contacts, \
                                                                     no_of_inbound_email_contacts, \
                                                                     no_of_outbound_email_contacts, \
                                                                     angry_case, \
                                                                     is_reopen, \
                                                                     ever_severity_upgrade, \
                                                                     ever_severity_downgrade, \
                                                                     owning_agent_login_id \
                                                                    FROM \
                                                                      TEMP_ACCOUNT_ID_TABLE t, \
                                                                      aws_kumo.d_case_details cd \
                                                                        JOIN dm_billing.d_customers cust ON cd.merchant_customer_id = cust.customer_id \
                                                                    WHERE cust.account_id = t.account_id \
                                                                     "
                                                                    # AND   cd.creation_date_utc <> case_resolve_date_utc \
                                                                    # AND   cd.creation_date_utc <> first_outbound_date_utc \
                                                                    + " \
                                                                      AND   cd.creation_date_utc BETWEEN DATE ('${{START_DATE}}') AND DATE ('${{END_DATE}}') \
                                                                      order by cd.creation_date_utc desc \
                                                                    "
                                                }

sql_awsdw_dict['case_details_of_internal_accounts'] = {'dwName': 'awssupportdw',
                                                       'columnNames': ['account_id',
                                                                      'merchant_name',
                                                                      'case_id',
                                                                      'category_name',
                                                                      'case_type_name',
                                                                      'reason',
                                                                      'case_description',
                                                                      'creation_date_utc',
                                                                      'case_resolve_date_utc',
                                                                      'first_outbound_date_utc',
                                                                      'case_status_name',
                                                                      'severity',
                                                                      'missed'
                                                                      ],
                                                       'queryString': "SELECT \
                                                                         cust.account_id, \
                                                                         ALT_MERCHANT_NAME, \
                                                                         cd.CASE_ID, \
                                                                         REPLACE(REPLACE(CATEGORY_NAME,'AWS ',''),'Amazon ','') as \"Category_Name\" , \
                                                                         cd.case_type_name, \
                                                                         cd.REASON, \
                                                                         CASE_DESCRIPTION, \
                                                                         CREATION_DATE_UTC, \
                                                                         CASE_RESOLVE_DATE_UTC, \
                                                                         first_outbound_date_utc, \
                                                                         CASE_STATUS_NAME, \
                                                                         SEVERITY , \
                                                                         CASE \
                                                                           WHEN (response_sla_minutes -(EXTRACT(EPOCH FROM first_outbound_date_utc - creation_date_utc)) / 60 >= 0) OR (first_outbound_date_utc IS NULL) THEN 0 \
                                                                           ELSE 1 \
                                                                         END as missed \
                                                                        FROM aws_kumo.d_case_details cd \
                                                                        JOIN dm_billing.d_customers cust ON cd.merchant_customer_id = cust.customer_id \
                                                                        WHERE cd.merchant_customer_id IN (select distinct o.customer_id \
                                                                                                          from \
                                                                                                            dm_billing.d_customers o, \
                                                                                                            dm_billing.dim_aws_accounts p \
                                                                                                          where o.account_id = p.account_id \
                                                                                                            and o.is_internal = 'Y' \
                                                                                                            and p.is_internal_flag = 'Y' \
                                                                                                            and p.end_effective_date IS NULL \
                                                                        ) \
                                                                        AND   cd.alt_merchant_name not in ('AWS Support API Tester', 'AWS Kumo', 'AWS Dev Support Kumo') \
                                                                        AND   cust.account_id not in ('717041922953', '204483443555', '474832276409', '204216589842', '204313211234', '76062759815', '371814697373', '806205027081', '390972317427', '205835554164', '203900167646', '794767850066', '414646665593', '352673085523', '283538334992', '834488402440', '690951700421', '428554777874', '454581698617', '145021921127', '688635657932', '163760793590', '699684733421',  '279667835983', '565749477985', '530323111691', '965789077213', '858770246048', '858770246048', '818893397435', '134869227492') \
                                                                        AND   cust.account_id not in ('397212192930', '588667327140', '686282390679', '370960121390', '601187650122', '500842391574', '185288277439', '741001768971', '889620617801')\
                                                                        AND   cd.case_description not in ('Test Case - Please Ignore', \
                                                                                                          'Call: Kumo testing', \
                                                                                                          'Kumo Test', \
                                                                                                          'Call: Phone Test', \
                                                                                                          'Call: test',\
                                                                                                          '[Kumo Test] Please ignore',\
                                                                                                          '[KUMO TEST] auto testing', \
                                                                                                          '[KUMO TEST] Automated Test',\
                                                                                                          'Chat: [KUMO TEST] auto testing', \
                                                                                                          'Chat: Kumo Testing - please ignore', \
                                                                                                          'Call: Kumo testing', \
                                                                                                          '[Test] - Please ignore', \
                                                                                                          'Immediate DRT Escalation Required', \
                                                                                                          'AMSTestNoOpsActionRequired', \
                                                                                                          '[Test] - Please ignore', \
                                                                                                          'Call: Test case', \
                                                                                                          'TEST CASE--Please ignore', \
                                                                                                          'test', \
                                                                                                          'Test', \
                                                                                                          'TEST' \
                                                                                                          ) \
                                                                        AND   cd.creation_date_utc <> case_resolve_date_utc \
                                                                        AND   cd.creation_date_utc <> first_outbound_date_utc \
                                                                        AND   cd.creation_date_utc BETWEEN DATE ('20160101') AND DATE ('20171031') \
                                                                        order by cd.creation_date_utc desc \
                                                                        "
                                                        }

sql_awsdw_dict['case_details_of_fmc'] = {'dwName': 'awssupportdw',
                                                       'columnNames': ['account_id',
                                                                      'merchant_name',
                                                                      'case_id',
                                                                      'category_name',
                                                                      'case_description',
                                                                      'creation_date_utc',
                                                                      'case_resolve_date_utc',
                                                                      'first_outbound_date_utc',
                                                                      'case_status_name',
                                                                      'severity',
                                                                      'missed'
                                                                      ],
                                                       'queryString': "SELECT \
                                                                         cust.account_id, \
                                                                         ALT_MERCHANT_NAME, \
                                                                         cd.CASE_ID, \
                                                                         REPLACE(REPLACE(CATEGORY_NAME,'AWS ',''),'Amazon ','') as \"Category_Name\" , \
                                                                         CASE_DESCRIPTION, \
                                                                         CREATION_DATE_UTC, \
                                                                         CASE_RESOLVE_DATE_UTC, \
                                                                         first_outbound_date_utc, \
                                                                         CASE_STATUS_NAME, \
                                                                         SEVERITY , \
                                                                         CASE \
                                                                           WHEN (response_sla_minutes -(EXTRACT(EPOCH FROM first_outbound_date_utc - creation_date_utc)) / 60 >= 0) OR (first_outbound_date_utc IS NULL) THEN 0 \
                                                                           ELSE 1 \
                                                                         END as missed \
                                                                        FROM aws_kumo.d_case_details cd \
                                                                          JOIN dm_billing.d_customers cust ON cd.merchant_customer_id = cust.customer_id \
                                                                        WHERE cust.account_id IN ('717041922953')\
                                                                        AND   cd.creation_date_utc <> case_resolve_date_utc \
                                                                        AND   cd.creation_date_utc <> first_outbound_date_utc \
                                                                        AND   cd.creation_date_utc BETWEEN DATE ('20160101') AND DATE ('20171031') \
                                                                        order by cd.creation_date_utc desc \
                                                                        "
                                        }


sql_awsdw_dict['all_enterprsie_accounts'] = {'dwName':'awsdw',
                                        'columnNames':['accountId',
                                                       'payerAccountId',
                                                       'serviceName',
                                                       'emailDomain',
                                                       ],
                                        'queryString':"select distinct \
                                          d.account_id, \
                                          d.payer_account_id, \
                                          b.product_name, \
                                          e.email_domain \
                                        from \
                                          O_AWS_PRODUCT_OFFERINGS a,\
                                          o_aws_products b, \
                                          o_aws_subscriptions c, \
                                          o_aws_accounts d, \
                                          d_customers e \
                                        where \
                                          d.account_status_code = 'Active' \
                                          and c.end_date is null \
                                          and a.product_id = b.product_id \
                                          and b.product_name like '%Support%' \
                                          and b.product_name like 'AWS%' \
                                          and d.account_id = c.account_id \
                                          and d.enc_customer_id = e.enc_customer_id \
                                          and a.offering_id = c.offering_id \
                                          and c.account_id = d.account_id \
                                          and d.enc_customer_id = e.enc_customer_id  \
                                          and c.end_date is null \
                                        "
                                        }

sql_awsdw_dict['all_service_usage_value'] = { 'dwName':'awsdw',
                                             'columnNames':['accountId',
                                                            'serviceName',
                                                            'serviceOperation',
                                                            'availabilityZone',
                                                            'usageType',
                                                            'usageVale' 
                                                          ],
                                             'queryString':"select distinct \
                                                              g.account_id, \
                                                              g.product_code, \
                                                              g.operation, \
                                                              g.availability_zone, \
                                                              g.usage_type, \
                                                              sum(g.usage_value) as usage_value \
                                                            from \
                                                              o_daily_aws_usage_history g \
                                                            where g.REQUEST_DAY >= '${{START_DATE}}' \
                                                              and g.REQUEST_DAY < '${{END_DATE}}' \
                                                              and g.account_id in (${{ACCOUNT_ID_LIST}}) \
                                                              and g.usage_value > 0 \
                                                              group by g.account_id, g.product_code, g.operation, g.availability_zone, g.usage_type, g.usage_resource \
                                                              order by usage_value desc \
                                              "
                                              }