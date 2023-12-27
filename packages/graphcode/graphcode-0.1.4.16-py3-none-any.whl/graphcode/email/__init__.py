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
from graphcode.conf import getSMTPServer, getSMTPUsername, getSMTPPassword

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders


class GcEmail():
  def __init__(self, smtpEndpoint = getSMTPServer()):
    self.smtpEnpoint = smtpEndpoint

    self.defaultEmailDomain = None
    self.emailType = None
    self.fromAlias = None
    self.toAlias_list = []
    self.ccAlias_list = []
    self.bccAlias_list = []
    self.attachement_dict = {}
    self.attachmentCount = 0
    
    self.subject = None
    self.body = None
  
  def getSMTP(self):
    return self.smtpEnpoint
  
  def setSMTP(self, endpoint):
    self.smtpEnpoint = endpoint
  
  def setDefaultEmailDomain(self, emailDomain):
    self.defaultEmailDomain = emailDomain
    logDebug("emailDomain:[{}] is set as the default email domain".format(emailDomain))
  
  def getDefaultEmailDomain(self):
    logDebug("defaultEmailDomain is [{}]".format(self.defaultEmailDomain))
    return self.defaultEmailDomain
    
  def setEmailType(self, emailType):
    self.emailType = emailType
    
  def getEmailType(self):
    return self.emailType

  def setSubject(self, subject):
    self.subject = subject
    logDebug("subject:[{}] is set".format(subject))
  
  def getSubject(self):
    logDebug("subject is [{}]".format(self.subject))
    return self.subject
  
  def setConext(self, context):
    if self.emailType == "html":
      self.body = self.getHTMLConext(context)
    
    else:
      self.body = context

  def getHTMLConext(self, context):
    if self.emailType == "html":
      # Create the body of the message (a plain-text and an HTML version).
      #text = "Hi {},\n".format(ownerInfoDict[aliasId]['masterOwnerFirstName'])
      htmlHeader = """\
  <html>
  <style>
  table {
  border-collapse: collapse;
  }
  
  table, th, td {
      border: 1px solid black;
  }
  </style>
    <head></head>
    <body>
"""
    
      htmlFooter = """\
      </body>
    </html>
  """
    
      return "{}{}{}".format(htmlHeader, context, htmlFooter)
    
  def setFromAlias(self, fromAlias):
    self.fromAlias = fromAlias
    
    logDebug("fromAlias:[{}] is set]".format(self.fromAlias))
  
  def getFromAlias(self):
    logDebug("fromAlias:[{}]".format(self.fromAlias))
    return self.fromAlias
        
  def addToAlias(self, toAlias):
    self.toAlias_list.append(toAlias)
    
    #logDebug("#toAlias:[{}] is added to toAlias_list:[..,{}]".format(toAlias, self.toAlias_list[-1]))
  
  def deleteToAlias(self, toAlias):
    self.toAlias_list.remove(toAlias)
    
    logDebug("toAlias:[{}] is removed from toAlias_list:[..,{}]".format(toAlias, self.toAlias_list[:10]))
  
  def getToAliasList(self):
    logDebug("toAlias_list(len:{}):[{}]".format(len(self.toAlias_list), self.toAlias_list[:10]))
    return self.toAlias_list
    
  def addCCAlias(self, ccAlias):
    self.ccAlias_list.append(ccAlias)
    
    #logDebug("#ccAlias:[{}] is added to ccAlias_list:[..,{}]".format(ccAlias, self.ccAlias_list[-1]))
  
  def deleteCCAlias(self, ccAlias):
    self.ccAlias_list.remove(ccAlias)
    
    logDebug("ccAlias:[{}] is removed from ccAlias_list:[..,{}]".format(ccAlias, self.ccAlias_list[:10]))
    
  def getCCAliasList(self):
    logDebug("ccAlias_list(len:{}):[{}]".format(len(self.ccAlias_list), self.ccAlias_list[:10]))
    return self.ccAlias_list
    
  def addBCCAlias(self, bccAlias):
    self.bccAlias_list.append(bccAlias)
    
    #logDebug("#bccAlias:[{}] is added to bccAlias_list:[..,{}]".format(bccAlias, self.bccAlias_list[-1:]))
  
  def deleteBCCAlias(self, bccAlias):
    self.bccAlias_list.remove(bccAlias)
    
    logDebug("bccAlias:[{}] is removed from bccAlias_list:[..,{}]".format(bccAlias, self.bccAlias_list[:10]))
    
  def getBCCAliasList(self):
    logDebug("bccAlias_list(len:{}):[{}]".format(len(self.bccAlias_list), self.bccAlias_list[:10]))
    return self.bccAlias_list
    
  def addAttachement(self, attachement_dict = None):
    if attachement_dict == None:
      logError("attachement_dict:[{}] is provided. It shouldn't be [{}]".format(attachement_dict, attachement_dict))
      return False
    else:
      #logDebug("attachement_dict:[{}] is provided".format(attachement_dict))
      for toAlias in attachement_dict.keys():
        logDebug("toAlias:[{}] is found at attachement_dict".format(toAlias))
        
        for attachementContent_dict in attachement_dict[toAlias]:
          #logDebug("attachementContent_dict:[{}] is found".format(attachementContent_dict))
          fileToSend = attachementContent_dict['fileToSend']
          binaryData = attachementContent_dict['binaryData'] 
          contentType = attachementContent_dict['contentType']
          
          maintype, subtype = contentType.split("/", 1)
      
          if binaryData == None:
            if maintype == "text":
              f = open(fileToSend)
            else:
              f = open(fileToSend, "rb")
            binaryData = f.read()
            f.close()
            
          if maintype == "text":
              # Note: we should handle calculating the charset
              attachment = MIMEText(binaryData.encode(), _subtype=subtype)       
          elif maintype == "image":
              attachment = MIMEImage(binaryData, _subtype=subtype)
          elif maintype == "audio":
              attachment = MIMEAudio(binaryData, _subtype=subtype)
          else:
              attachment = MIMEBase(maintype, subtype)
              attachment.set_payload(binaryData)
              encoders.encode_base64(attachment)
          attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
          attachment.add_header('X-Attachment-Id', "{}".format(self.attachmentCount))
          attachment.add_header('Content-ID', "{}".format(self.attachmentCount))
          
          if toAlias in self.attachement_dict.keys():
            self.attachement_dict[toAlias].append(attachment)
            #logDebug("self.attachement_dict[{}]:[...,{}]".format(toAlias, self.attachement_dict[toAlias][-1]))
          else:
            self.attachement_dict[toAlias] = [attachment]  
            logDebug("self.attachement_dict[{}]:[len:{:,}]".format(toAlias, len(self.attachement_dict[toAlias][-1])))
          self.attachmentCount += 1

  def sendEmail(self, to_dict = None):
    logDebug("'to_dict':[{}] is provided".format(to_dict))
    
    if to_dict == None:
      subject = None
      context = None
      fromAlias = None
      toAlias_list = None
      ccAlias_list = None
      bccAlias_list = None
    else:
      subject = to_dict['subject']
      context = to_dict['context']
      fromAlias = to_dict['fromAlias']
      toAlias_list = to_dict['toAlias_list']
      ccAlias_list = to_dict['ccAlias_list']
      bccAlias_list = to_dict['bccAlias_list']
    
    msg = MIMEMultipart()
    
    if subject != None:
      thisSubject = subject
    else:
      thisSubject = self.subject
      
    if thisSubject == None:
      logDebug("subject:[{}] is set to (no subject)".format(thisSubject))
      msg['Subject'] = "(no subject)"
    else:
      msg['Subject'] = thisSubject
    logDebug("msg['Subject']:{}".format(msg['Subject']))

    if fromAlias != None:
      thisFromAlias = fromAlias
    else:
      if self.fromAlias == None:
        errorMessage = "thisFromAlias shouldn't be [{}]".format(self.fromAlias)
        logError(errorMessage)
        raise ValueError(errorMessage)
      thisFromAlias = self.fromAlias
    
    if len(thisFromAlias) <= 1:
      errorMessage = "fromAlias:[{}] isn't expected".format(thisFromAlias)
      logError(errorMessage)
      raise ValueError(errorMessage)
    else:
      if len(thisFromAlias.split("@")) == 2:
        msg['From'] = "{}".format(thisFromAlias)
      else:
        if self.defaultEmailDomain == None:
          errorMessage = "self.defaultEmailDomain:[{}] should be set with setDefaultEmailDomain()".format(self.defaultEmailDomain)
          logError(errorMessage)
          raise ValueError(errorMessage)
        else:
          msg['From'] = "{}@{}".format(thisFromAlias, self.defaultEmailDomain)
    me = msg['From']    
    logDebug("msg['From']:{}".format(me))
    
    if toAlias_list != None:
      thisToAlias_list = toAlias_list
    else:
      if self.toAlias_list == None:
        thisToAlias_list = ""
      else:
        thisToAlias_list = self.toAlias_list
    
    aliases = ""
    for toAlias in thisToAlias_list:
      if len(toAlias.split("@")) == 2:
        if aliases == "":
          aliases = toAlias
        else:
          aliases = "{};{}".format(aliases, toAlias)
      else:
        if aliases == "":
          if self.defaultEmailDomain == None:
            errorMessage = "self.defaultEmailDomain:[{}] should be set with setDefaultEmailDomain()".format(self.defaultEmailDomain)
            logError(errorMessage)
            raise ValueError(errorMessage)
          else:
            aliases = "{}@{}".format(toAlias, self.defaultEmailDomain)
        else:
          aliases = "{};{}@{}".format(aliases, toAlias, self.defaultEmailDomain)
            
    msg['To']  = "{}".format(aliases)
    logDebug("msg['To']:{}".format(msg['To']))
    
    if ccAlias_list != None:
      thisCcAlias_list = ccAlias_list
    else:
      if self.ccAlias_list == None:
        thisCcAlias_list = ""
      else:
        thisCcAlias_list = self.ccAlias_list
        
    aliases = ""
    for ccAlias in thisCcAlias_list:
      if len(ccAlias.split("@")) == 2:
        if aliases == "":
          aliases = ccAlias
        else:
          aliases = "{};{}".format(aliases, ccAlias)
      else:
        if aliases == "":
          if self.defaultEmailDomain == None:
            errorMessage = "self.defaultEmailDomain:[{}] should be set with setDefaultEmailDomain()".format(self.defaultEmailDomain)
            logError(errorMessage)
            raise ValueError(errorMessage)
          else:
            aliases = "{}@{}".format(ccAlias, self.defaultEmailDomain)
        else:
          aliases = "{};{}@{}".format(aliases, ccAlias, self.defaultEmailDomain)
          
    msg['Cc']  = "{}".format(aliases)
    logDebug("msg['Cc']:{}".format(msg['Cc']))
    
    if bccAlias_list != None:
      thisBccAlias_list = bccAlias_list
    else:
      if self.bccAlias_list == None:
        thisBccAlias_lis = ""
      else:
        thisBccAlias_list = self.bccAlias_list
      
    aliases = ""
    for bccAlias in thisBccAlias_list:
      if isinstance(bccAlias, str):
        if len(bccAlias.split("@")) == 2:
          if aliases == "":
            aliases = bccAlias
          else:
            aliases = "{};{}".format(aliases, bccAlias)
        else:
          if aliases == "":
            if self.defaultEmailDomain == None:
              errorMessage = "self.defaultEmailDomain:[{}] should be set with setDefaultEmailDomain()".format(self.defaultEmailDomain)
              logError(errorMessage)
              raise ValueError(errorMessage)
            else:
              aliases = "{}@{}".format(bccAlias, self.defaultEmailDomain)
          else:
            aliases = "{};{}@{}".format(aliases, bccAlias, self.defaultEmailDomain)
      else:
        logWarn(f"unexpected bccAlias:[{bccAlias}]")
        
    msg['Bcc']  = "{}".format(aliases)
    logDebug("msg['Bcc']:{}".format(msg['Bcc']))
    
    rcpt = ""
    if msg['Cc'] != None or msg['Bcc'] != None or msg['To'] != None:
      rcpt = msg['Cc'].split(";") + msg['Bcc'].split(";") + msg['To'].split(";")
      logDebug("rcpt:[{}]".format(rcpt))
    else:
      errorMessage = "receipt isn't defined -> msg['Cc']:[{}] + msg['Bcc']:[{}] + msg['To']:[{}]".format(msg['Cc'], msg['Bcc'], msg['To'])
      logError(errorMessage)
      raise ValueError(errorMessage)

    if context != None:
      if self.emailType == "html":
        thisBody = self.getHTMLConext(context)
      else:
        thisBody = context
    else:
      thisBody = self.body
      
    # Record the MIME types of both parts - text/plain and text/html.
    if self.emailType == "html":
      part1 = MIMEText(thisBody, 'html', 'utf-8')
    else:
      part1 = MIMEText(thisBody, 'plain', 'utf-8')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    
    isAttached = False
    for thisToAlias in thisToAlias_list:
      if thisToAlias in self.attachement_dict.keys():
        logDebug("toAlias:[{}] is found at self.attachement_dict".format(thisToAlias))
        for attachment in self.attachement_dict[thisToAlias]:
          msg.attach(attachment)
        isAttached = True
    
    if isAttached == False and 'default' in self.attachement_dict.keys():
      for attachment in self.attachement_dict['default']:
        #logDebug("attachement:[{}]".format(attachment))
        msg.attach(attachment)
      
    s = smtplib.SMTP(self.getSMTP())
    s.sendmail(me, rcpt, msg.as_string())
    s.quit()       
    
    msg = f"An email was sent from {msg['From']} to {msg['To']}, CCed:{msg['Cc']}, BCCed:{msg['Bcc']} with {len(msg.as_string()):,} Bytes."
    
    logDebug(msg)
    
    return msg

