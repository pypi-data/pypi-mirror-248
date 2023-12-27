
'''Copyright (c) 1998-2124 Ryeojin Moon
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

from graphcode.pandas import gcPandasHtmlToDict

from tammy.midway import PdxMidway

import json

def response(request_dict):
  try:
    response_dict = {
      "apiName": request_dict["apiName"],
      "response": action(request_dict),
      "state":"SUCCEEDED",
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
  
  pdxMidway = PdxMidway(userAccountId=request_dict["metadata"]["awsAccountId"], loginAliasId=request_dict["metadata"]["userName"])

  iamDetails_dict = {}
  for accountId in ["111271783983"]:#, "407842270708", "956483708461", "244747273457", "479241814824"]:
    thisIamDetails_dict = updateIAMDetails(request_dict, pdxMidway, accountId, errorReason_list, logMessage_list)
    for key in thisIamDetails_dict.keys():
      if key in iamDetails_dict.keys():
        for itemDetailsItem_dict in thisIamDetails_dict[key]:
          iamDetails_dict[key].append(itemDetailsItem_dict)
      else:
        iamDetails_dict[key] = thisIamDetails_dict[key]
  
  return {
    **iamDetails_dict,
    "logMessages": logMessage_list,
    "errorReasons": errorReason_list
    }

def updateIAMDetails(request_dict, pdxMidway, accountId, errorReason_list, logMessage_list):  
  
  url = "https://iam-tools.amazon.com/accounts/{}".format(accountId)
  iamOverview_dict = getIAMOverview(pdxMidway, url)
  
  iamOverview_list = []
  for key in iamOverview_dict.keys():
    iamOverview_list.append(
      {
        "name": key,
        "value": iamOverview_dict[key]
        }
      )
  
  iamType_dict = {}
  urlBase = "https://iam-tools.amazon.com/"
  for iamType in ["user", "group", "role"]:
    iamType_dict[iamType] = []
    for key in iamOverview_dict[iamType].keys():
      if isinstance(iamOverview_dict[iamType][key], str) and iamOverview_dict[iamType][key].startswith("/"):
        
        url = "{}{}".format(urlBase, iamOverview_dict[iamType][key])
        iamDetails_dict = getIAMDetails(pdxMidway, url)
        
        thisIAMDetails_dict = {}
        for key2 in iamDetails_dict.keys():
          if key2 in ["role"]:
            try:
              del iamDetails_dict[key2]["Role Information"]
            except:
              logException("unexpected iamDetails_dict['{}'].keys():[{}]".format(key2, iamDetails_dict[key2].keys()))
            
            try:
              beginRoot = iamDetails_dict[key2]["Root Account ID"].find("\">") + 2
              endRoot = iamDetails_dict[key2]["Root Account ID"].find("</a>")
              iamDetails_dict[key2]["Root Account ID"] = "{}".format(iamDetails_dict[key2]["Root Account ID"][beginRoot:endRoot])
            except:
              logException("unexpected {}:{}:[{}]".format(type(iamDetails_dict[key2]).__name__, key2, iamDetails_dict[key2]))
              
            thisIAMDetails_dict = {
              **iamDetails_dict[key2],
              **thisIAMDetails_dict
              }
            
          elif key2 in ["AssumeRole"]:
            excellenceStatus = None
            for key3 in iamDetails_dict[key2].keys():
              if key3.find("<pre>") > 0:
                endPre = key3.find("</pre>")
                if endPre > 0:
                  assumeRole = "{}".format(key3[key3.find("{"):endPre])
                else:
                  assumeRole = "{}".format(key3[key3.find("{"):])
                
                try:
                  assumePolicy_dict = json.loads(assumeRole.replace("\n","").replace("\r","").replace("&quot;",'"'))
                  for statementItem_dict in assumePolicy_dict["Statement"]:
                    if "sts:AssumeRole" in statementItem_dict["Action"]:
                      try:
                        if "Principal" in statementItem_dict.keys() and "AWS" in statementItem_dict["Principal"].keys():
                          if isinstance(statementItem_dict["Principal"]["AWS"], list):
                            if len(statementItem_dict["Principal"]["AWS"])>1:
                              for principlaItem in statementItem_dict["Principal"]["AWS"]:
                                if "arn:aws:iam::{}:role/{}".format(thisIAMDetails_dict["Root Account ID"], thisIAMDetails_dict["Name"]) in principlaItem:
                                  excellenceStatus = "Green"
                                elif thisIAMDetails_dict["ID"] in principlaItem:
                                  excellenceStatus = "Green"
                            else:
                              if "arn:aws:iam::{}:role/{}".format(thisIAMDetails_dict["Root Account ID"], thisIAMDetails_dict["Name"]) in statementItem_dict["Principal"]["AWS"]:
                                excellenceStatus = "Green"
                              elif thisIAMDetails_dict["ID"] in statementItem_dict["Principal"]["AWS"]:
                                excellenceStatus = "Green"
                        else:
                          excellenceStatus = "Green"
                                
                      except:
                        logException("unexpected statementItem_dict.keys():[{}]".format(statementItem_dict.keys()))  
                            
                  if excellenceStatus not in ["Green"]:
                    excellenceStatus = "Yellow"
                except:
                  assumePolicy_dict = assumeRole.replace("\n","").replace("\r","").replace("&quot;",'"')
                  logException("unable to load json:[{}]".format(assumeRole))
              
                thisIAMDetails_dict = {
                  **thisIAMDetails_dict,
                  "excellenceStatus": excellenceStatus,
                  "assumeRole": assumePolicy_dict
                  }
              
          else:
            newIAMDetails_dict = {}
            for key3 in iamDetails_dict[key2].keys():
              if key3.find("<pre>") >= 0:
                endPre = key3.find("</pre>")
                if endPre > 0:
                  newKey3 = "{}".format(key3[key3.find("{"):endPre])
                else:
                  newKey3 = "{}".format(key3[key3.find("{"):])
                
                newKey3 = newKey3.replace("\n","").replace("\r","").replace("&quot;",'"')
              else:
                newKey3 = key3.replace("\n","").replace("\r","").replace("&quot;",'"')
            
              body = iamDetails_dict[key2][key3]
              if body.find("<pre>") >= 0:
                endPre = body.find("</pre>")
                if endPre > 0:
                  newValue3 = "{}".format(body[body.find("{"):endPre])
                else:
                  newValue3 = "{}".format(body[body.find("{"):])
                
                newValue3 = newValue3.replace("\n","").replace("\r","").replace("&quot;",'"')
              else:
                newValue3 = body.replace("\n","").replace("\r","").replace("&quot;",'"')
                
              newIAMDetails_dict[newKey3.strip()] = newValue3.strip()
              
            thisIAMDetails_dict = {
              **thisIAMDetails_dict,
              "{}".format(key2): newIAMDetails_dict
              }
        
        iamType_dict[iamType].append(thisIAMDetails_dict)
        
  return {
    "iamOverview": iamOverview_list,
    **iamType_dict
    }


def getIAMDetails(pdxMidway, url):
  midwayResponse = pdxMidway.request(url)
  plainHtml = midwayResponse.content.decode()
  
  iamDetails_dict = {}
  
  beingRole = plainHtml.find("<table", plainHtml.find("Role arn:aws:iam"))
  endRole = plainHtml.find("</table>", beingRole) + 8
  iamDetails_dict["role"] = getTableItems(plainHtml[beingRole:endRole])
  
  beingAssumeRole = plainHtml.find("<table", endRole)
  endAssumeRole = plainHtml.find("</table>", beingAssumeRole) + 8
  iamDetails_dict["AssumeRole"] = getTableItems(plainHtml[beingAssumeRole:endAssumeRole])

  beingGroup = plainHtml.find("<table", endAssumeRole)
  endGroup = plainHtml.find("</table>", beingGroup) + 8
  iamDetails_dict["Group"] = getTableItems(plainHtml[beingGroup:endGroup])

  beginRole = plainHtml.find("<table",endGroup)
  endRole = plainHtml.find("</table>", beginRole) + 8
  iamDetails_dict["Role"] = getTableItems(plainHtml[beginRole:endRole])
  
  beginManagedPolicy = plainHtml.find("<table",endRole)
  endManagedPolicy = plainHtml.find("</table>", beginManagedPolicy)
  iamDetails_dict["ManagedPolicyBoundary"] = getTableItems(plainHtml[beginManagedPolicy:endManagedPolicy])
  
  beginManagedPolicy = plainHtml.find("<table",endManagedPolicy)
  endManagedPolicy = plainHtml.find("</table>", beginManagedPolicy)
  iamDetails_dict["ManagedPolicyPermission"] = getTableItems(plainHtml[beginManagedPolicy:endManagedPolicy])
  
  return iamDetails_dict

def getIAMOverview(pdxMidway, url):
  midwayResponse = pdxMidway.request(url)
  plainHtml = midwayResponse.content.decode()
  
  iamOverview_dict = {}
  
  beingAccount = plainHtml.find("<table", plainHtml.find("Account"))
  endAccount = plainHtml.find("</table>", beingAccount) + 8
  iamOverview_dict["account"] = getTableItems(plainHtml[beingAccount:endAccount])
  
  beingMFA = plainHtml.find("<table", endAccount)
  endMFA = plainHtml.find("</table>", beingMFA) + 8
  iamOverview_dict["MFA"] = getTableItems(plainHtml[beingMFA:endMFA])

  beingQuota = plainHtml.find("<table", endMFA)
  endQuota = plainHtml.find("</table>", beingQuota) + 8
  iamOverview_dict["quota"] = getTableItems(plainHtml[beingQuota:endQuota])

  beginUser = plainHtml.find("<table",endQuota)
  endUser = plainHtml.find("</table>", beginUser) + 8
  iamOverview_dict["user"] = getTableItems(plainHtml[beginUser:endUser])
  
  beginGroup = plainHtml.find("<table",endUser)
  endGroup = plainHtml.find("</table>", beginGroup)
  iamOverview_dict["group"] = getTableItems(plainHtml[beginGroup:endGroup])
  
  beginRole = plainHtml.find("<table",endGroup)
  endRole = plainHtml.find("</table>", beginRole) + 8
  iamOverview_dict["role"] = getTableItems(plainHtml[beginRole:endRole])
  
  beginInstance = plainHtml.find("<table",endRole)
  endInstance = plainHtml.find("</table>", beginInstance) + 8
  iamOverview_dict["instance"] = getTableItems(plainHtml[beginInstance:endInstance])

  beginPolicy = plainHtml.find("<table",endInstance)
  endPolicy = plainHtml.find("</table>", beginPolicy) + 8
  iamOverview_dict["policy"] = getTableItems(plainHtml[beginPolicy:endPolicy])

  beginMfa = plainHtml.find("<table",endPolicy)
  endMfa = plainHtml.find("</table>", beginMfa) + 8
  iamOverview_dict["mfa"] = getTableItems(plainHtml[beginMfa:endMfa])

  beginSubscriptions = plainHtml.find("<table",endMfa)
  endSubscriptions = plainHtml.find("</table>", beginSubscriptions) + 8
  iamOverview_dict["subscriptions"] = getTableItems(plainHtml[beginSubscriptions:endSubscriptions])
  
  beginRights = plainHtml.find("<table",endSubscriptions)
  endRights = plainHtml.find("</table>", beginRights) + 8
  iamOverview_dict["rights"] = getTableItems(plainHtml[beginRights:endRights])
  
  beginSAML = plainHtml.find("<table",endRights)
  endSAML = plainHtml.find("</table>", beginSAML) + 8
  iamOverview_dict["smal"] = getTableItems(plainHtml[beginSAML:endSAML])
  
  beginPrincipals = plainHtml.find("<table",endSAML)
  endPrincipals = plainHtml.find("</table>", beginPrincipals) + 8
  iamOverview_dict["Principals"] = getTableItems(plainHtml[beginPrincipals: endPrincipals])
  
  return iamOverview_dict

def getTableItems(tableHtml):
  begin = 0
  item_dict = {}
  while True: 
    rowItem_list, begin = getRowItems(tableHtml, begin)
    if isinstance(rowItem_list, list):
      if len(rowItem_list) == 1 and len(rowItem_list[0].strip()) > 0:
        key = rowItem_list[0].strip()
        beginA = key.find("href=", key.find("<a"))
        if beginA > 0:
          beginA += 5
          endA = key.find(">", beginA)
          htmlLink = "{}".format(key[beginA:endA])
          
          beginA = endA + 1
          endA = key.find("</a", beginA)
          htmlLabel = "{}".format(key[beginA:endA])
          
          item_dict[htmlLabel] = htmlLink.replace("'","").replace('"','').replace("\n","").replace("\r","").strip()
          
        else:
          item_dict["{}".format(rowItem_list[0])] = None
                              
      elif len(rowItem_list) == 2:
        item_dict["{}".format(rowItem_list[0])] = "{}".format(rowItem_list[1])
                              
      elif len(rowItem_list) > 2:
        item_dict["{}".format(rowItem_list[0])] = "{}".format(rowItem_list[1:])
        
      if begin < 0:
        break
    else:
      break
    
  return item_dict

  
def getRowItems(tableHtml, begin):
  begin = tableHtml.find(">", tableHtml.find("<tr", begin))
  end = tableHtml.find("</tr", begin)
  
  if begin < 0:
    return None, -1
  
  if end < 0:
    rowHtml=tableHtml[begin:]
  else:
    rowHtml=tableHtml[begin:end]
  #logDebug("#rowHtml:{}:{}:[{}]".format(begin, end, rowHtml))
  
  begin = 0
  item_list = []
  while True: 
    item, begin = getItems(rowHtml, begin)
    if item == None:
      break
    else:
      item_list.append(item)
      if begin < 0:
        break
    
  return item_list, end
  
def getItems(rowHtml, begin):
  begin = rowHtml.find(">", rowHtml.find("<td", begin))
  end = rowHtml.find("</td", begin)
  #logDebug("#{}:{}:[{}]".format(begin, end, rowHtml[begin:end]))
  
  if begin < 0 :
    return None, -1
  
  else:
    if end < 0:
      return rowHtml[begin+1:], end
    
    else:
      return rowHtml[begin+1:end], end
  