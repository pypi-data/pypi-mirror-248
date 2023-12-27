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
from graphcode.logging import logDebug, logError, logException, raiseValueError
from collections.abc import KeysView

def getDelimiter(result_list, divider=3):
  """
  Calculate the delimiter for displaying items based on the length of the result list.

  :param result_list: The list, tuple, or KeysView object whose items are to be displayed.
  :param divider: The divider to determine the frequency of item display. Default is 3.
  :return: A tuple containing the start index, total number of items, and the calculated delimiter.
  :raises ValueError: If the input result_list is not a list, tuple, or KeysView object.
  """
  if isinstance(result_list, list) or isinstance(result_list, tuple) or isinstance(result_list, KeysView):
    totalNumber = len(result_list)
    if divider is None:
      if totalNumber <= 10:
        divider = 1
      elif totalNumber <= 100000:
        divider = 3 
      elif totalNumber <= 999999:
        divider = 10
      else:
        divider = 100

    percentageDelimiter = int(totalNumber/divider) + 1

    firstItemCount = 1

    logDebug("firstItemCount:[{:,}], totalNumber:[{:,}], percentageDelimiter:[{:,}]".format(firstItemCount, totalNumber, percentageDelimiter))
    return firstItemCount, totalNumber, percentageDelimiter

  else:
    raiseValueError("{} is yet to support".format(type(result_list).__name__))

def displayItemDetails(itemCount, totalNumber, percentageDelimiter, itemDetails, itemName="itemDetails"):
  """
  Display details of an item if the item count is a multiple of the percentage delimiter or if it's the first or last item.

  :param itemCount: The current count of the item being processed.
  :param totalNumber: The total number of items.
  :param percentageDelimiter: The calculated delimiter to determine display frequency.
  :param itemDetails: The details of the current item.
  :param itemDetails: The name of the item. Default is "itemDetails".
  :return: The updated item count.
  """
    
  try:
    if (itemCount % percentageDelimiter) == 0 or (itemCount in [1, totalNumber]):
      logDebug("(#{:,}/{:,})\t{}:{}:[{}]".format(itemCount, totalNumber, type(itemDetails).__name__, itemName, itemDetails))
    
    itemCount += 1
    
    return itemCount
  except:
    logException("unexpected error")