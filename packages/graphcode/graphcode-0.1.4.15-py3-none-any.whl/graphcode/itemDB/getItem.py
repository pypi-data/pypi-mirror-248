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

import time
import json

import zlib

def getItem(table, key, paginatingRange=None, cipherKey='DEFAULT-CIPHER-KEY'):
  getDataResponse_dict = getData(
    table=table, 
    key=key
    )
  
  #for thisKey in getDataResponse_dict.keys():
  #  logDebug("getDataResponse_dict[{}]:[{}]".format(thisKey, getDataResponse_dict[thisKey]))
  
  manifest_dict_data = decryptThenDecompressData(data=getDataResponse_dict["data"], cipherKey=cipherKey)
  #for thisKey in manifest_dict_data.keys():
  #  logDebug("manifest_dict_data[{}]:[{}]".format(thisKey, manifest_dict_data[thisKey]))
  
  try:
    manifest_dict = manifest_dict_data["data"]
    #for thisKey in manifest_dict.keys():
    #  logDebug("manifest_dict_data[{}]:[{}]".format(thisKey, manifest_dict[thisKey]))
  except:
    logExceptionWithValueError("unexpected manifest_dict_data:{}/{}:[{}]".format(table, key, manifest_dict_data))
    
  if manifest_dict["isCacheData"]:
    if time.time() > manifest_dict["__expirationTime__"]:
      raiseValueError("expired data {:,.3f}s({:,.3f}h) ago".format(time.time()-manifest_dict["__expirationTime__"], (time.time()-manifest_dict["__expirationTime__"])/3600 ))
    #else:
    #  logDebug("alive data for [{:,.3f}s]".format(manifest_dict["__expirationTime__"] - time.time()))
  #else:
  #  logDebug("ttl_s is not set")
    
  if manifest_dict["isPaginatedData"]:
    decryptedDecompressedData_list = []

    if isinstance(paginatingRange, list):
      if len(paginatingRange) == 2:
        if abs(paginatingRange[0]) > manifest_dict["paginatingLength"]:
          if paginatingRange[0] < 0:
            paginatingRange[0] = -1 * manifest_dict["paginatingLength"]
          else:
            paginatingRange[0] = manifest_dict["paginatingLength"]
        
        if paginatingRange[1] > 0:
          paginatingRange[1] += 1
        elif paginatingRange[1] < 0:
          paginatingRange[1] -= 1
          
        if abs(paginatingRange[1]) > manifest_dict["paginatingLength"]:
          if paginatingRange[1] < 0:
            paginatingRange[1] = -1 * manifest_dict["paginatingLength"]
          else:
            paginatingRange[1] = manifest_dict["paginatingLength"]
        
            
        paginatingId = paginatingRange[0]
        for cipherKey in manifest_dict["cipherKeys"][paginatingRange[0]: paginatingRange[1]]:
          
          getDataResponse_dict = getData(
            table=table, 
            key="__{}_paginatingId_{}__".format(key, paginatingId + len(decryptedDecompressedData_list)),
            )
          
          #logDebug("#{:,}:[{}]".format(len(decryptedDecompressedData_list), cipherKey))
          decryptedDecompressedData_list.append(
            decryptThenDecompressData(data=getDataResponse_dict["data"], cipherKey=cipherKey)
            )
        
          #logDebug("(#{:,})\tdecryptedDecompressedData_list[-1]:[{}]".format(len(decryptedDecompressedData_list), decryptedDecompressedData_list[-1]))
      else:
        processedPaginatingId_list = []
        for paginatingId in paginatingRange:
          if paginatingId in processedPaginatingId_list:
            logWarn("processed paginatingId:[{}]".format(paginatingId))
            continue
          
          if paginatingId > manifest_dict["paginatingLength"]:
            if manifest_dict["paginatingLength"] in processedPaginatingId_list:
              logWarn("processed paginatingId:[{}] exceeds paginatingLength:[{}]".format(paginatingId, manifest_dict["paginatingLength"]))
              continue
            else:
              logWarn("paginatingId:[{}] exceeds paginatingLength:[{}]".format(paginatingId, manifest_dict["paginatingLength"]))
              paginatingId = manifest_dict["paginatingLength"]
            
          cipherKey = manifest_dict["cipherKeys"][paginatingId]
          
          getDataResponse_dict = getData(
            table=table, 
            key="__{}_paginatingId_{}__".format(key, paginatingId),
            )
          
          #logDebug("#{:,}:[{}]".format(len(decryptedDecompressedData_list), cipherKey))
          decryptedDecompressedData_list.append(
            decryptThenDecompressData(data=getDataResponse_dict["data"], cipherKey=cipherKey)
            )
        
          #logDebug("(#{:,})\tdecryptedDecompressedData_list[-1]:[{}]".format(len(decryptedDecompressedData_list), decryptedDecompressedData_list[-1]))

    else:
      for cipherKey in manifest_dict["cipherKeys"]:
        
        getDataResponse_dict = getData(
          table=table, 
          key="__{}_paginatingId_{}__".format(key, len(decryptedDecompressedData_list)),
          )
        
        #logDebug("#{:,}:[{}]".format(len(decryptedDecompressedData_list), cipherKey))
        decryptedDecompressedData_list.append(
          decryptThenDecompressData(data=getDataResponse_dict["data"], cipherKey=cipherKey)
          )
      
        #logDebug("(#{:,})\tdecryptedDecompressedData_list[-1]:[{}]".format(len(decryptedDecompressedData_list), decryptedDecompressedData_list[-1]))
        
        if isinstance(paginatingRange, int) and len(decryptedDecompressedData_list) >= paginatingRange:
          #logDebug("paginatingCount:[{}] exceeded paginatingRange:[{}]".format(len(decryptedDecompressedData_list) , paginatingRange))
          break
        
    if manifest_dict["dataType"] in ["list"]:
      slieceData_list = []
      for decryptedDecompressedDataItem_dict in decryptedDecompressedData_list:
        for dataItem_dict in decryptedDecompressedDataItem_dict["data"]:
          slieceData_list.append(dataItem_dict)
      return slieceData_list
    else:
      raiseValueError("unexpected type:[{}]".format(manifest_dict["dataType"], decryptedDecompressedData_list))
  
  else:
    data = manifest_dict["__data__"]
    #logDebug("{}:data:[{}]".format(type(data).__name__, data))
    
    if manifest_dict["isTTL"]:
      try:
        del data["__expirationTime__"]
      except:
        pass#logException("unable to delete '__expirationTime__' from {}:data:[{}]".format(type(data).__name__, data))
        
      return data
    
    else:
      return data
    

def decryptThenDecompressData(data, cipherKey=None):
  sizeOfCompressedData = len(data)
  
  try:
    #decompressed_data = zlib.decompress(data)
    decompress = zlib.decompressobj()
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    sizeOfDecompressedData = len(decompressed_data)
    #logDebug("#type:{}:decompressed_data:[{}]".format(type(decompressed_data), decompressed_data))
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("failed to decompress type:{}:data:[{}]".format(type(data), data))
      }
  
  try:
    gcCipher = GcCipher(cipherKey)
    decrypted_data = gcCipher.decrypt(decompressed_data)
    sizeOfDecryptedData = len(decrypted_data)
    #logDebug("#type:{}:decrypted_data:[{}]".format(type(decrypted_data), decrypted_data))
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("failed to decrypt type:{}:data:[{}]".format(type(decompressed_data), decompressed_data))
      }
  
  try:
    #logDebug("{}:decrypted_data:[{}]".format(type(decrypted_data).__name__, decrypted_data))
    item_dict = json.loads(decrypted_data)
    #logDebug("{}:item_dict:[{}]".format(type(item_dict).__name__, item_dict))
    if type(item_dict).__name__ not in ["str", "bytes", "bytearray"]:
      return {
        "itemSize":sizeOfDecryptedData,
        "encryptedSize": sizeOfDecompressedData,
        "compressedData":sizeOfCompressedData,
        "data": item_dict
        }
    else:
      try:
        item_dict = json.loads(item_dict)
        #for key in item_dict.keys():
        #  logDebug("#type:{}:{}:[{}]".format(type(item_dict[key]), key, item_dict[key]))
      except:
        logException("unable to load json with item_dict:[{}]".format(item_dict))
      
      return {
        "itemSize":sizeOfDecryptedData,
        "encryptedSize": sizeOfDecompressedData,
        "compressedData":sizeOfCompressedData,
        "data": item_dict["__data__"]
        }
      
  except:
    return {
      "status_code": 500,
      "errorCode":"Not Applicable",
      "errorReason": logException("failed to load json with type:{}:decrypted_data:[{}]".format(type(decrypted_data), decrypted_data))
      }
    
def getData(table, key):
  gcItemDB = GcItemDB()

  try:
    return {
      "status_code": 200,
      "data": gcItemDB.get(
        table = table, 
        key=key,
        mode="rb"
        )
      }
  except:
    logExceptionWithValueError("failed to load {}/{}".format(table, key))
    
  