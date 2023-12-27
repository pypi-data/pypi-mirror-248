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

from pado.theme import default

class GcTheme():
  def __init__(self, themeName = "default"):
    theme_dict = {"default": default.theme_dict}
    
    if themeName in theme_dict.keys():
      self.thisTheme_dict = theme_dict[themeName]
    else:
      logWarn("theme:[{}] is not found. So, the default theme is instated.".format(themeName))
      self.thisTheme_dict = theme_dict["default"]
  
  def getFormTags(self, category, tagName):
    if category in self.thisTheme_dict["form"].keys():
      if tagName in self.thisTheme_dict["form"][category].keys():
        formTags = self.thisTheme_dict["form"][category][tagName]
      
      else:
        logError("category:[{}]->tagName:[{}] is not found".format(category, tagName))
        
        if "default" in self.thisTheme_dict["form"].keys() and tagName in self.thisTheme_dict["form"]["default"].keys():
          formTags = self.thisTheme_dict["form"]["default"][tagName]
          logWarn("category:[{}]->tagName:[{}] is used instead category:[{}]".format("default", category, tagName))
        else:
          formTags = ""
          logError("category:[{}]->tagName:[{}] is not found at 'default'".format(category, tagName))
    
    else:
      logError("category:[{}] is not found".format(category))
      
      if "default" in self.thisTheme_dict["form"].keys() and tagName in self.thisTheme_dict["form"]["default"].keys():
        formTags = self.thisTheme_dict["form"]["default"][tagName]
        logWarn("category:[{}]->tagName:[{}] is used instead category:[{}]".format("default", category, tagName))
      else:
        formTags = ""
        logError("category:[{}]->tagName:[{}] is not found at 'default'".format(category, tagName))
    
    return formTags
      
    