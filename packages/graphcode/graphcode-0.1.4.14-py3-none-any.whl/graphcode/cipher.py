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

from graphcode.credentials import GcCredentials

from cryptography.fernet import Fernet

import base64

import json

class GcCipher():
  def __init__(self, cipherKey='DEFAULT-CIPHER-KEY'):

    #logDebug(f"#cipherKey:[{cipherKey}]")
    if cipherKey in ['None']:
      cipherKey='DEFAULT-CIPHER-KEY'
    #logDebug(f"#{type(cipherKey).__name__}:cipherKey:[{cipherKey}]")
    
    if isinstance(cipherKey, str) and len(cipherKey) >= 32:
      self.cipher_key = base64.urlsafe_b64decode(cipherKey.encode('utf-8'))
    else: 
      try:
        gcCredentials = GcCredentials()
        accessKey, secretKey = gcCredentials.get(cipherKey)
        #logDebug(f"#{type(secretKey).__name__}:accessKey:[{secretKey}](len:{len(secretKey)})")
      except:
        logException("creating cipherKey:[{}]".format(cipherKey))
        accessKey, secretKey= self.creatDefaultCipherKey(cipherKey=cipherKey)
      
      try:
        self.cipher_key = base64.urlsafe_b64decode(secretKey.encode('utf-8'))
        #logDebug(f"#{type(self.cipher_key).__name__}:self.cipher_key:[{self.cipher_key}]")
      except:
        logExceptionWithValueError(f"unexpected error in secretKey:[{secretKey}](len:{len(secretKey)})->encodedSecretKey:[{secretKey.encode('utf-8')}](len:{len(secretKey.encode('utf-8'))})")
        
    self.fernetCipher = Fernet(self.cipher_key)
  
  def creatDefaultCipherKey(self, cipherKey):
    logDebug('#cipherKey:[{}]'.format(cipherKey))

    gcCredentials = GcCredentials()

    accessKey, secretKey = gcCredentials.create(cipherKey)
    logDebug("#{}:accessKey:[{}](len:{:,})".format(type(accessKey).__name__, accessKey, len(accessKey)))
    logDebug("#{}:secretKey:[{}](len:{:,})".format(type(secretKey).__name__, secretKey, len(secretKey)))

    self.cipher_key = Fernet.generate_key()
    logDebug("#{}:self.cipher_key:[{}]".format(type(self.cipher_key).__name__, self.cipher_key))
  
    secretKey = base64.b64encode(self.cipher_key).decode('utf-8')
    logDebug("#{}:secretKey:[{}](len:{:,})".format(type(secretKey).__name__, secretKey, len(secretKey)))
    
    cipherKey = gcCredentials.update(cipherKey, accessKey, secretKey)
    accessKey, secretKey = gcCredentials.get(cipherKey)
    logDebug("#{}:accessKey:[{}](len:{:,})".format(type(accessKey).__name__, accessKey, len(accessKey)))
    logDebug("#{}:secretKey:[{}](len:{:,})".format(type(secretKey).__name__, secretKey, len(secretKey)))

    return accessKey, secretKey
  
  def encrypt(self, plainData):    
    try:
      if plainData != None:
        #logDebug("#plainData:(len:{}) -> type:{} -> plainData:[{}]".format(len(plainData), type(plainData), plainData))
        jsonData =  {"data":plainData}
        #logDebug("#plainData:(len:{}) -> type:{} -> plainData:[{}]".format(len(jsonData), type(jsonData), jsonData))
        
        encodedJsonData = json.dumps(jsonData).encode()
        #logDebug("#encodedJsonData:(len:{}) -> type:{} -> plainData:[{}]".format(len(encodedJsonData), type(encodedJsonData), encodedJsonData))
        
        encryptedData = self.fernetCipher.encrypt(encodedJsonData)
        #logDebug("#encryptedData:[{}]".format(encryptedData))
      else:
        encryptedData = None
    except Exception as e: 
      errorMessage = "Error:[{}] -> unable to encrypt the data:[{}]".format(e, plainData)
      logError(errorMessage)
      raise ValueError(errorMessage)
    
    return encryptedData
  
  def decrypt(self, encryptedData):    
    try:
      #logDebug("#encryptedData:(len:{}) -> type:{} -> encryptedData:[{}]".format(len(encryptedData), type(encryptedData), encryptedData))
      if isinstance(encryptedData, bytes):
        decryptedData = json.loads(self.fernetCipher.decrypt(encryptedData).decode())
      else:
        try:
          encryptedData = encryptedData.encode()
          #logDebug("#encryptedData:(len:{}) -> type:{} -> encryptedData:[{}]".format(len(encryptedData), type(encryptedData), encryptedData))
          decryptedData = json.loads(self.fernetCipher.decrypt(encryptedData).decode())
        except Exception as e:
          errorMessage = "Error:[{}] -> unable to decrypt encryptedData:[{}]".format(e, encryptedData)
          logError(errorMessage)
          raise ValueError(errorMessage)
      
      #logDebug("#decryptedData:(len:{}) -> type:{} -> decryptedData:[{}]".format(len(decryptedData), type(decryptedData), decryptedData))
      
      return decryptedData['data']
      
    except Exception as e: 
      errorMessage = "Error:[{}] -> unable to decrypt the data:[{}]".format(e, encryptedData)
      logError(errorMessage)
      raise ValueError(errorMessage)
    
    #logDebug("#Credentials:[{}]".format(self.credential_dict.keys()))
