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
from graphcode.logging import logCritical, logError, logWarn, logInfo, logDebug, logException, logExceptionWithValueError, raiseValueError

from graphcode.cipher import GcCipher
from graphcode.itemDB import GcItemDB

from cryptography.fernet import Fernet

import time
import json

import zlib

import base64
import binascii

def putItem(table, key, data, paginatingSize=5000, ttl_s=None, cipherKey='DEFAULT-CIPHER-KEY'):
  if ttl_s != None:
    __expirationTime__ = time.time() + abs(ttl_s)
    isCacheData = True
    isTTL = True
  else:
    if isinstance(data, dict) and "__expirationTime__" in data.keys():
      __expirationTime__ = data["__expirationTime__"]
      isCacheData = True
      isTTL = True
    else:
      __expirationTime__ = None
      isCacheData = False
      isTTL = False
  
  #logDebug("====>{}:{}/{}(ttl_s:[{}])".format(dataType, table, key, ttl_s))
  
  sizeOfData, itemCount, isPaginatedData, paginatedData_list = paginatingData(data, paginatingSize=paginatingSize)
  
  manifest_dict = {
    "dataType": type(data).__name__,
    "isCacheData": isCacheData,
    "isTTL": isTTL,
    "isPaginatedData": isPaginatedData,
    "paginatingLength": len(paginatedData_list),
    "itemCount": itemCount,
    "sizeOfData": sizeOfData,
    "cipherKeys":[],
    "responses":[],
    "__expirationTime__": __expirationTime__
    }
  
  if isPaginatedData:
    compressedEncryptedData_list = []
    for paginatedDataItem_dict in paginatedData_list:
      compressedEncryptedData_list.append(
        compressThenEncryptData(
          data=paginatedDataItem_dict["data"], 
          cipherKey=paginatedDataItem_dict["cipherKey"]
          )
        )
      #logDebug("compressedEncryptedData_list[-1]:{}".format(compressedEncryptedData_list[-1]))
      
      manifest_dict["cipherKeys"].append(paginatedDataItem_dict["cipherKey"])
    
    response_list = []
    for dataItem_dict in compressedEncryptedData_list:
      response_list.append(
        putData(
          table=table, 
          key="__{}_paginatingId_{}__".format(key, len(response_list)),
          data=dataItem_dict["data"])
        )
    
    #for responseItem_dict in response_list:
    #  logDebug("responseItem_dict:[{}]".format(responseItem_dict))
    
    manifest_dict["responses"] =  response_list
  
    #for thisKey in manifest_dict.keys():
    #  if isinstance(manifest_dict[thisKey], list):
    #    itemCount = 0
    #    for manifestItem_dict in manifest_dict[thisKey]:
    #      logDebug("{}:manifest_dict[{}.{:,}]:[{}]".format(type(manifestItem_dict).__name__, thisKey, itemCount, manifestItem_dict))
    #      itemCount += 1
    #  else:
    #    logDebug("{}:manifest_dict[{}]:[{}]".format(type(manifest_dict[thisKey]).__name__, thisKey, manifest_dict[thisKey]))
    
    manifest_dict_data = compressThenEncryptData(data=manifest_dict, cipherKey=cipherKey)
    response_dict = putData(
      table=table, 
      key=key, 
      data=manifest_dict_data["data"]
      )
  
  else:
    #logDebug("paginatedData_list[-1]:[{}]".format(paginatedData_list[-1]))
    
    manifest_dict["__data__"] = paginatedData_list[-1]["data"]
    manifest_dict_data = compressThenEncryptData(data=manifest_dict, cipherKey=cipherKey)
    response_dict = putData(
      table=table, 
      key=key, 
      data=manifest_dict_data["data"]
      )
  
  return response_dict

def paginatingData(data, paginatingSize=3):
  sizeOfData = 0
  itemCount = 0
  paginatedData_list = []
  if paginatingSize > 0 and isinstance(data, list) and len(data) > paginatingSize:
    isPaginatedData = True
    itemCount =  len(data)
    
    itemChunk_list = []
    for dataItem_dict in data:
      itemChunk_list.append(dataItem_dict)
      if (len(itemChunk_list) % paginatingSize) == 0:
        paginatedData_list.append(
          {
            "cipherKey": base64.b64encode(Fernet.generate_key()).decode('utf-8'),
            "data": json.dumps(
              {
                "__createTime__":time.time(),
                "__chunkId__": len(paginatedData_list),
                "__data__":itemChunk_list
                }
              )
            }
          )
        itemChunk_list = []
        
        sizeOfData += len(paginatedData_list[-1])
    
    paginatedData_list.append(
      {
        "cipherKey": base64.b64encode(Fernet.generate_key()).decode('utf-8'),
        "data": json.dumps(
          {
            "__createTime__":time.time(),
            "__chunkId__": len(paginatedData_list),
            "__data__":itemChunk_list
            }
          )
        }
      )
    sizeOfData += len(paginatedData_list[-1])
    #logDebug("total {}:{:,}({:,}Bytes) itemChunk are added to paginatedData with paginatingSize:{:,}".format(type(data).__name__, len(paginatedData_list), sizeOfData, paginatingSize))
  
  elif isinstance(data, dict):
    itemCount =  len(data.keys())
    isPaginatedData = False
    paginatedData_list.append(
      {
        "cipherKey": base64.b64encode(Fernet.generate_key()).decode('utf-8'),
        "data": data
        }
      )
    sizeOfData += len("{}".format(paginatedData_list[-1]["data"]))
    #logDebug("total {}:{:,}({:,}Bytes) paginatedItems are added to paginatedData with paginatingSize:{:,}".format(type(data).__name__, len(paginatedData_list), sizeOfData, paginatingSize))
  
  elif isinstance(data, str):
    itemCount =  len(data)
    isPaginatedData = False
    paginatedData_list.append(
      {
        "cipherKey": base64.b64encode(Fernet.generate_key()).decode('utf-8'),
        "data": data
        }
      )
    sizeOfData += len(paginatedData_list[-1]["data"])
    #logDebug("total {}:{:,}({:,}Bytes) paginatedItems are added to paginatedData with paginatingSize:{:,}".format(type(data).__name__, len(paginatedData_list), sizeOfData, paginatingSize))
  
  else:
    itemCount =  len(data)
    isPaginatedData = False
    paginatedData_list.append(
      {
        "cipherKey": base64.b64encode(Fernet.generate_key()).decode('utf-8'), 
        "data": data
        }
      )
    sizeOfData += len("{}".format(paginatedData_list[-1]["data"]))
    #logDebug("total {}:{:,}({:,}Bytes) paginatedItems are added to paginatedData with paginatingSize:{:,}".format(type(data).__name__, len(paginatedData_list), sizeOfData, paginatingSize))
  
    
  return sizeOfData, itemCount, isPaginatedData, paginatedData_list

def compressThenEncryptData(data, cipherKey='DEFAULT-CIPHER-KEY'):
  #logDebug("#cipherKey:[{}]".format(cipherKey))
  
  try:
    data = json.dumps(data)
    
    sizeOfData = len(data)
    
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("unable to 'dumps' for type:{}:'d':[{}]".format(type(data), data))
      }
  
  try:
    try:
      gcCipher = GcCipher(cipherKey=cipherKey)
    except:
      logExceptionWithValueError(f"failed to create GcCipher with cipherKey:[{cipherKey}]")

    encrypted_data = gcCipher.encrypt(data)
    sizeOfEncryptedData = len(encrypted_data)
    #logDebug("#type:{}:encrypted_data:[{}]".format(type(encrypted_data), binascii.hexlify(encrypted_data)))
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("unable to encrypt data:[{}]".format(data))
      }
    
  try:
    del data
  except:
    logException("failed to delete 'data' after it's encrypted")
  
  #compressed_data = zlib.compress(encrypted_data, 2)
  
  try:
    compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, +15)
    compressed_data = compress.compress(encrypted_data)
    compressed_data += compress.flush()
    sizeOfCompressedData = len(compressed_data)
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("unable to compress encrypted_data:[{}]".format(encrypted_data))
      }
  
  try:
    del encrypted_data
  except:
    logException("failed to delete 'encrypted_data' after it's compressed")
  
  #logDebug("#type:{}:compressed_data:[{}]".format(type(compressed_data), binascii.hexlify(compressed_data)))
  
  return {
    "itemSize": sizeOfData,
    "encryptedSize": sizeOfEncryptedData,
    "compressedSize": sizeOfCompressedData,
    "cipherKey": cipherKey,
    "data": compressed_data
    }
                       
def putData(table, key, data):

  gcItemDB = GcItemDB()
  
  try:
    return {
      "status_code": 200,
      "response": gcItemDB.put(
        table=table, 
        key=key,
        value=data,
        mode="wb"
        )
      }
    
  except:
    logExceptionWithValueError("failed to store {}:{}/{}:[{}]".format(type(data).__name__, table, key, data))

