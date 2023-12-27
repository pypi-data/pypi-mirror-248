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

from wooju.lib import getTargetServiceNames

def getCamapaignServiceNames(campaignName):
  if campaignName.replace("_", " ") in ["NATGW Optimization"]:
    targetService_list = getTargetServiceNames("EC2")
  else:
    logWarn("campaignName:[{}] not supported".format(campaignName))
    targetService_list = []
    
  return targetService_list

def setCampaignAttributes(request_dict):
  #load template values
  template_dict = {}
  key = None
  for templateLine in request_dict["attributes"]["template"].split("\n"):
    if templateLine.strip().lower() in ["[campaign]", "[head]", "[body]"]:
      key = f"{templateLine.strip().lower()[1:-1]}"
      template_dict[key] = {}
    elif key is not None:
      keyword = templateLine.strip().split(":")[0]
      if key in ["campaign", "head"] and keyword.startswith("#"):
        template_dict[key][f"{templateLine[1:len(keyword)]}".strip().lower()] = f"{templateLine[len(keyword)+1:]}".strip()
      elif key in ["body"]:
        if isinstance(template_dict[key], str):
          template_dict[key] += f"{templateLine}\n"
        else:
          template_dict[key] = f"{templateLine}"
      else:
        logWarn("unexpected key:[{}]".format(key))
    else:
      logWarn("unexpected templateLine:[{}]".format(templateLine))
    #endif templateLine.strip().lower() in ["[campaing]", "[head]", "[body]"]:
  #endfor templateLine in request_dict["attributes"]["template"].split("\n"):

  for key in template_dict.keys():
    if isinstance(template_dict[key], dict):
      for key2 in template_dict[key].keys():
        if key in request_dict["attributes"].keys():
          request_dict["attributes"][key][key2] = template_dict[key][key2]
        else:
          request_dict["attributes"][key] = {}
          request_dict["attributes"][key][key2] = template_dict[key][key2]
      
        logDebug("{}.{}:[{}]".format(key, key2, template_dict[key][key2]))
    else:
      request_dict["attributes"][key] = template_dict[key]
      logDebug("{}.[{}]".format(key, template_dict[key]))
  
  request_dict["apiName"] = f"tammy.campaign.discoverCampaigns.{template_dict['campaign']['name'].replace(' ', '_')}"

  return request_dict