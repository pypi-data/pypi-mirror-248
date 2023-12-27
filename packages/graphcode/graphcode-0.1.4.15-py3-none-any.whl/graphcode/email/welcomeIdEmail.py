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

from graphcode.conf import getSMTPDomainName
from graphcode.conf import getSMTPFromEmailAddress, getSMTPBCCedEmailAddress

from graphcode.email import GcEmail

from graphcode.lib import getDateString

from pado.auth import GcAuthToken

import time

def send(request_dict):
  try:

    homeURL = request_dict["metadata"]["homeURL"].split("/")[-1].split(":")[0].split(".")[0]
    ruleName = request_dict["metadata"]["ruleName"]
    userName = request_dict["metadata"]["userName"]
    firstName = request_dict["metadata"]["firstName"]
    lastName = request_dict["metadata"]["lastName"]
    orgName = request_dict["metadata"]["orgName"]

    gcAuthToken = GcAuthToken()
    welcomeId = gcAuthToken.createToken(request_dict["metadata"]["userName"])

    try:
      processTime =  f"{time.time() - request_dict["__beginTime__"]:,.3f}s"
    except:
      processTime =  "n/a"

    gcEmail = GcEmail()
    gcEmail.setDefaultEmailDomain(getSMTPDomainName())
    gcEmail.setEmailType("html")
    gcEmail.setFromAlias(getSMTPFromEmailAddress())
    gcEmail.addToAlias(f"{userName}")
    gcEmail.addCCAlias("hoeseong+moduaws@amazon.com")
    gcEmail.addBCCAlias(getSMTPBCCedEmailAddress())
    gcEmail.setSubject("[moduAWS] welcome, {}({}@)!".format(firstName, userName))
    html = "Hi {},".format(firstName)
    html += "<br>"
    html += "<br>"
    html += "Please complete your registration with the following welcomeId!"
    html += "<br>"
    html += "<ul>"
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("homeURL",homeURL)
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("userName",userName)
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("firstName",firstName)
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("lastName",lastName)
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("orgName",orgName)
    html += "<li><b>{}</b>:&nbsp;&nbsp;&nbsp;&nbsp;{}</li>".format("welcomeId",welcomeId)
    html += "</ul>"
    html += "<br>"
    html += "<br>"
    html += "Thanks,"
    html += "<br>"
    html += "moduAWS"
    html += "<br>"
    html += "---------------------------------"
    html += "<br>"
    html += "date:{}".format(getDateString("now"))
    gcEmail.setConext(html)
    
    return {"status_code":200, "content":gcEmail.sendEmail()}
  except:
    return {"status_code":500, "content":logException("unable to send a test email")}