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
Created on Jan 1, 2020

@author: hoeseong
'''
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from graphcode.csv import GcCsv

from graphcode.lib import getDateString
from graphcode.delimiter import getDelimiter, displayItemDetails
from graphcode.sqlLib import updateQueryWithAccountIds

from pathway import requests
from pathway import updateMsg, consolidateErrorReasons, consolidateLogMessages

from wooju.args import getSQLQueries, getTTL_s
from wooju.smtm import loadQueryResultCache_dict, saveQueryResultCache_dict, deleteQueryResultCache_dict
from tammy.awsdw import GcDw

import psycopg2

from datetime import datetime

import json

def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "state": "SUCCEEDED",
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
  ttl_s = getTTL_s(request_dict)
  
  dwResultDict_list = cacheQueryRun(request_dict, ttl_s, errorReason_list, logMessage_list)
     
  return {
    "dwResults":dwResultDict_list,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def queryRun(request_dict, queryName, queryStatement_list, errorReason_list, logMessage_list):
  ttl_s = getTTL_s(request_dict)

  queryResult_dict = {}
  queryCount = 0
  for queryStatement in queryStatement_list:
    if len(queryStatement.strip()) > 0:
      request_dict["attributes"]["queryStatement"] = queryStatement
      
      queryCount +=1
      
      resultKey = "{}_{}".format(queryName, queryCount)
      queryResult_dict[resultKey] = cacheQueryRun(request_dict, ttl_s, errorReason_list, logMessage_list)
      logDebug("resultKey:[{}]:[{:,}]".format(resultKey, len(queryResult_dict[resultKey])))
  
  return queryResult_dict
    
def cacheQueryRun(request_dict, ttl_s=300, errorReason_list=[], logMessage_list=[]):
  logDebug("ttl_s:[{}] is set".format(ttl_s))
  try:
    if ttl_s < 0:
      raiseValueError("ttl_s:[{}] is set".format(ttl_s))
    elif ttl_s == 0:
      try:
        queryResult_list = dwRun(request_dict, errorReason_list, logMessage_list)
      except:
        queryResult_list = [
          {
            "error":logExceptionWithValueError("unable to load 'dwRun'->file:[{}]".format(__file__))
            }
          ]
      try:
        deleteQueryResultCache_dict(request_dict)
      except:
        logException("unable to delete wbResultCache_dict")
        
    else:
      queryResult_list = loadQueryResultCache_dict(request_dict)
      itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=queryResult_list, divider=3)
      for queryRequestItem in queryResult_list:
        itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, queryRequestItem, itemName="queryResult_list")
  except:
    try:
      queryResult_list = dwRun(request_dict, errorReason_list, logMessage_list)
    except:
      queryResult_list = [
        {
          "error":logExceptionWithValueError("unable to 'dwRun'->file:[{}]".format(__file__))
          }
        ]
    
    if abs(ttl_s) > 0:
      saveQueryResultCache_dict(request_dict, queryResult_list, abs(ttl_s))
      logDebug("saved queryResult_list(len:{:,})".format(len(queryResult_list)))
    else:
      deleteQueryResultCache_dict(request_dict)
  
  return queryResult_list
    
def dwRun(request_dict, errorReason_list=[], logMessage_list=[]):
  gcDw = GcDw()
  
  queryStatement=request_dict["attributes"]["queryStatement"]
  dwName=request_dict["attributes"]["dbType"]
  fetchedRow_list, columnName_list = gcDw.queryAWSDW(dwName=dwName, queryStatement=queryStatement)
  
  logDebug("columnName_list(len:{:,}):[{}]".format(len(columnName_list), columnName_list))
  if len(fetchedRow_list) > 0:
    logDebug("{}:thisResult_list[0]:[{}]".format(type(fetchedRow_list).__name__, fetchedRow_list[0]))
    logDebug("{}:thisResult_list[-1]:[{}]".format(type(fetchedRow_list).__name__, fetchedRow_list[-1]))
  else:
    logDebug("{}:thisResult_list:[{}]".format(type(fetchedRow_list).__name__, fetchedRow_list))
    
  dwResultDict_list = []
  itemCount, totalNumber, percentageDelimiter = getDelimiter(result_list=fetchedRow_list, divider=3)
      
  #logDebug("#percentageDelimiter:[{:,}], itemCount:[{:,}], totalNumber:[{:,}]".format(percentageDelimiter, itemCount, totalNumber))
  for dwRowItem_list in fetchedRow_list:
    #logDebug("#percentageDelimiter:[{:,}], itemCount:[{:,}], totalNumber:[{:,}]".format(percentageDelimiter, itemCount, totalNumber))
    itemCount = displayItemDetails(itemCount, totalNumber, percentageDelimiter, itemDetails=dwRowItem_list, itemName="dwRowItem_list")
    
    thisRowItem_dict = {}
    itemPosition = 0
    for itemValue in dwRowItem_list:
      try:
        json.dumps(itemValue)
        thisRowItem_dict[columnName_list[itemPosition]] = itemValue
      except:
        try:
          thisRowItem_dict[columnName_list[itemPosition]] = "{}".format(itemValue)
        except:
          logException("-------->unable to convert itemValue[{}]:[{}] to string".format(itemPosition, itemValue))
        
      itemPosition +=1
    
    #logDebug("#thisRowItem_dict:[{}]".format(thisRowItem_dict))
    dwResultDict_list.append(thisRowItem_dict)
  
  return dwResultDict_list
    
def getDwQuery():
  
  dwQueryTemplate_dict = {
    
    "unitPrice_list": """ 
      SELECT DISTINCT
        w.account_id,
        w.product_code,
        w.usage_type,
        sum(w.usage_value_sum) as usave_value,
        sum(w.usd_amount_before_tax_sum) as usage_cost,
        (SUM(w.usd_amount_before_tax_sum)::float / NULLIF(SUM(w.usage_value_sum), 0))::float AS unit_price
      FROM 
        dm_billing.d_weekly_est_charge_items_sum w
      WHERE 
        w.product_code = 'AmazonEC2'
        AND w.cal_week_end_date >= (CURRENT_DATE - INTERVAL '41 days')
        AND account_id IN (
          SELECT 
            DISTINCT
              w.account_id
          FROM
            d_weekly_est_charge_items_sum w
          WHERE 
            w.cal_week_end_date >= (CURRENT_DATE - INTERVAL '41 days')
            AND w.account_id in (
              SELECT DISTINCT
                d.account_id
              FROM
                O_AWS_PRODUCT_OFFERINGS a,
                o_aws_products b,
                o_aws_subscriptions c,
                o_aws_accounts d,
                d_customers e
              WHERE
                d.account_status_code = 'Active'
                AND a.product_id = b.product_id
                AND b.product_name IN (
                  SELECT DISTINCT 
                    b.product_name
                  FROM 
                    o_aws_products
                  WHERE
                    b.product_name LIKE '%Support%'
                    AND (b.product_name LIKE '%Enterprise%' OR b.product_name LIKE '%Platinum%')
                  )
                AND d.account_id = c.account_id
                AND d.enc_customer_id = e.enc_customer_id
                AND a.offering_id = c.offering_id
                AND c.account_id = d.account_id
                AND d.enc_customer_id = e.enc_customer_id 
                AND c.end_date IS NULL
                AND e.email_domain = 'nike.com'
                )
            AND product_code IN ('AmazonEC2')
            AND usage_type LIKE '%NatGateway-Hours'
          )
        AND w.usage_type NOT LIKE '%BoxUsage%'
        AND w.usage_type NOT LIKE '%EBS%'
        AND w.usage_type NOT LIKE '%HeavyUsage:%'
        AND w.usage_value_sum > 0
      GROUP BY 
        w.account_id, 
        w.product_code, 
        w.usage_type
      """,
      
    # beginning of queryTemplate_dict
    "listingEnterpriseCustomers": {
      'dwName':'awsdw',
      'columnNames':[
        'accountId',
        'usageResource',
        'usageType',
        'operation',
        'usageValue',
        ],
      'queryString':""" 
        select 
          g.account_id,
          g.usage_resource,
          g.usage_type,
          g.operation,
          sum(g.usage_value) as usage_value
        from
          o_daily_aws_usage_history g
        where g.REQUEST_DAY = '2023-06-01'
          and g.account_id in (
              select distinct account_id
              from 
                dm_billing.d_weekly_est_charge_items_sum w
              where 
                w.cal_week_end_date >= (current_date - INTERVAL '99 days')
                and usage_type like '%NatGateway-Hours'
                and account_id in (
                  select distinct
                    d.account_id
                  from
                    O_AWS_PRODUCT_OFFERINGS a,
                    o_aws_products b,
                    o_aws_subscriptions c,
                    o_aws_accounts d,
                    d_customers e
                  where
                    d.account_status_code = 'Active'
                    AND a.product_id = b.product_id
                    AND b.product_name in (select b.product_name
                      from o_aws_products
                      where
                        b.product_name like '%Support%'
                        AND (b.product_name like '%Enterprise%' or b.product_name like '%Platinum%')
                      )
                    and d.account_id = c.account_id
                    and d.enc_customer_id = e.enc_customer_id
                    and a.offering_id = c.offering_id
                    and c.account_id = d.account_id
                    and d.enc_customer_id = e.enc_customer_id 
                  )
              )
          and g.usage_resource like '%:natgateway/%'
        group by g.account_id,g.usage_resource,g.usage_type,g.operation
        HAVING sum(g.usage_value) >= 1
        """
      },
      #end of queryTemplate_dict
    
    # beginning of queryTemplate_dict
    "listingEnterpriseCustomers": {
      'dwName':'awsdw',
      'columnNames':[
        'accountId',
        'accountRole',
        'payerAccountId',
        'accountStatusCode',
        'creationDate',
        'last_update_date',
        'serviceName',
        'emailDomain',
        ],
      'queryString':""" 
        select distinct
          d.account_id,
          d.account_role,
          d.payer_account_id,
          d.account_status_code,
          d.creation_date,
          d.last_update_date,
          b.product_name,
          e.email_domain
        from
          O_AWS_PRODUCT_OFFERINGS a,
          o_aws_products b,
          o_aws_subscriptions c,
          o_aws_accounts d,
          d_customers e
        where
          d.account_status_code = 'Active'
          AND a.product_id = b.product_id
          AND b.product_name in (select b.product_name
            from o_aws_products
            where
              b.product_name like '%Support%'
              AND (b.product_name like '%Enterprise%' or b.product_name like '%Platinum%')
            )
          and d.account_id = c.account_id
          and d.enc_customer_id = e.enc_customer_id
          and a.offering_id = c.offering_id
          and c.account_id = d.account_id
          and d.enc_customer_id = e.enc_customer_id 
          and c.end_date is null
          and e.email_domain <> 'amazon.com'
          """
      },
      #end of queryTemplate_dict

     
    # beginning of queryTemplate_dict
    "listingAccountIdOfEnterpriseCustomers": {
       'dwName':'awsdw',
       'columnNames':[
          'accountId',
          'productCode',
          'usageType',
          'operation',
          'usageValue',
          'usageCost'
      ],
       'queryString':"""
          select 
            distinct 
              w.account_id,
              w.payer_id,
              w.product_code,
              w.usage_type,
              w.operation,
              sum(w.usage_value_sum),
              sum(w.usd_amount_before_tax_sum)
          from
            d_weekly_est_charge_items_sum w
          where 
            w.cal_week_end_date between '2023-06-01' and '2023-06-10'
            and w.product_code in ('AmazonEC2')
            and w.usage_type like '%Nat%'
            and w.account_id in (
              select distinct
                d.account_id
              from
                O_AWS_PRODUCT_OFFERINGS a,
                o_aws_products b,
                o_aws_subscriptions c,
                o_aws_accounts d,
                d_customers e
              where
                d.account_status_code = 'Active'
                AND a.product_id = b.product_id
                AND b.product_name in (select b.product_name
                  from o_aws_products
                  where
                    b.product_name like '%Support%'
                    AND (b.product_name like '%Enterprise%' or b.product_name like '%Platinum%')
                  )
                and d.account_id = c.account_id
                and d.enc_customer_id = e.enc_customer_id
                and a.offering_id = c.offering_id
                and c.account_id = d.account_id
                and d.enc_customer_id = e.enc_customer_id 
                and c.end_date is null
              )
          group by w.account_id, w.product_code, w.usage_type, w.operation
          """
      }
      #end of queryTemplate_dict
    
    #end of dwQueryTemplate_dict
    }
  
          


