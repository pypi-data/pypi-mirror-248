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
from graphcode.logging import logDebug, logError, logException, getLogLevel, setLogLevel
from threading import Thread
import time

def unitTest(testCases):
    """
    Run unit tests provided in the testCases dictionary or list.
    
    :param testCases: A dictionary or list containing test case information.
    """
    unitTestCount = 0
    previousLogLevel = getLogLevel()
    setLogLevel('DEBUG')

    # Check if the input is a dictionary
    if isinstance(testCases, dict):
        for testName, testInfo in testCases.items():
            unitTestCount += 1
            runTest(testName, testInfo, unitTestCount)

    # Check if the input is a list
    elif isinstance(testCases, list):
        for testInfo in testCases:
            unitTestCount += 1
            testName = testInfo.get("target").__name__
            runTest(testName, testInfo, unitTestCount)

    # Reset the log level to its previous state
    setLogLevel(previousLogLevel)

def runTest(testName, testInfo, unitTestCount):
    """
    Run a single unit test.
    
    :param testName: Name of the test.
    :param testInfo: Dictionary containing test information.
    :param unitTestCount: The current test number.
    """
    try:
        logDebug(f"unitTestFunctionName(#{unitTestCount}):[{testName}] started")
        targetFunction = testInfo["target"]
        targetArgs = testInfo.get("args", ())
        t = Thread(target=targetFunction, args=targetArgs)
        
        __microSecondBeginTime__ = int(time.time() * 1000000)
        t.start()
        t.join()
        __microSecondEndTime__ = int(time.time() * 1000000)
        
        microsSecondProcessTime = __microSecondEndTime__ - __microSecondBeginTime__
        logDebug(f"unitTestFunctionName(#{unitTestCount}):[{testName}] finished (runTime:[{microsSecondProcessTime:,}]MicroSeconds")
    
    except Exception as e:
        logException()
        logError(f"Error:[{e}] -> unitTestFunctionName(#{unitTestCount}):[{testName}] failed")
