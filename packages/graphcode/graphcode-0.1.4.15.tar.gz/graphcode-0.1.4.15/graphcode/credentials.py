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
from graphcode.logging import logDebug, logError, logException, logExceptionWithValueError, raiseValueError
from graphcode.conf import getCredentialsPath, getCredentials, setSecretKeyWithAccessKey
from graphcode.json import dumpJson, loadJson
from os.path import join, exists
import secrets

class GcCredentials:
  def __init__(self):
    """
    Initialize the GcCredentials class, creating a credentials file if it does not exist.
    """
    credentialsDir = getCredentialsPath()

  def get(self, name):
    """
    Retrieve credentials based on the provided credential name.

    :param name: The name of the credential to retrieve.
    :return: A tuple of (username/accessKey, password/secretKey).
    :raises ValueError: If the credential name is not found.
    """
    try:
      credential_dict = getCredentials()
      
      if name in credential_dict.keys():
        return self.extract_credentials(credential_dict[name])
      else:
        raiseValueError(f"credentialName:[{name}] is not found")

    except Exception as e:
      logExceptionWithValueError(f"credentialName:[{name}] is not found->Error:[{e}]")

  def extract_credentials(self, credentialItem_dict):
    """
    Extract username and password from the credentials dictionary.

    :param credentials: The credentials dictionary.
    :param credential_name: The name of the credential.
    :param verbose_mode: Flag to enable verbose logging.
    :return: A tuple of (username/accessKey, password/secretKey).
    """
    if "username" in credentialItem_dict.keys():
      return credentialItem_dict["username"], credentialItem_dict["password"][3:-4]
    elif "accessKey" in credentialItem_dict.keys():
      return credentialItem_dict["accessKey"], credentialItem_dict["secretKey"][3:-4]
    else:
      raiseValueError(f"unexpected credentialItem_dict:[{credentialItem_dict}] that must have 'username' or 'accessKey' at least")

  def update(self, name, accessKey, secretKey):
    """
    Update the credentials with the provided access key and secret key.

    :param name: The name of the credential to update.
    :param accessKey: The access key to set.
    :param secretKey: The secret key to set.
    :return: The name of the updated credential.
    """
    logDebug(f'credentialName:[{name}]')
    
    try:
      credential_dict = setSecretKeyWithAccessKey(
        name=name, 
        accessKey=accessKey,
        secretKey=f"{secrets.token_urlsafe(2)}{secretKey}{secrets.token_urlsafe(3)}"
        )

      return name
    
    except Exception:
      logExceptionWithValueError(f"Unable to update credentials for [{name}]")

  def create(self, name):
    """
    Create a new credential with a generated access key and secret key.

    :param credential_name: The name of the credential to create.
    :param verbose_mode: Flag to enable verbose logging.
    :return: A tuple of the generated (accessKey, secretKey).
    """
    try:
      accessKey = secrets.token_urlsafe(16)
      secretKey = secrets.token_urlsafe(32)
      credential_dict = setSecretKeyWithAccessKey(
        name=name, 
        accessKey=accessKey,
        secretKey=f"{secrets.token_urlsafe(2)}{secretKey}{secrets.token_urlsafe(3)}"
        )

      storedAccessKey, storedSecretKey = self.get(name)

      logDebug(f'{secretKey}(len:{len(secretKey)}):[{storedSecretKey}](len:{len(storedSecretKey)})')
      return accessKey, secretKey
    
    except Exception:
      logExceptionWithValueError(f"Unable to create credentials for [{name}]")
