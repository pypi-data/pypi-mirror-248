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
import platform

import os
from os import scandir
from os.path import expanduser, exists

import shutil

def getOSDIrPath(dirPath):
    return dirPath.replace("/", "\\") if platform.system().startswith("Win") else dirPath.replace("\\", "/")

def getOSTempDirPath():
    return expanduser("~\\AppData\\Local\\Temp") if platform.system().startswith("Win") else expanduser("~/tmp")

def createDir(dirPath):
    dirPath = expanduser(getOSDIrPath(dirPath))
    
    if exists(dirPath):
        print(f"Directory {dirPath} already exists.")
        return dirPath
    
    os.makedirs(dirPath)
    print(f"Directory {dirPath} is created.")
    return dirPath

def cloneDir(sourceDir, targetDir):
    sourceDir = expanduser(sourceDir)
    targetDir = expanduser(targetDir)
    print("Cloning directory tree from [{}] to [{}]".format(sourceDir, targetDir))

    if not os.path.exists(sourceDir):
        print("Source directory does not exist.")
        return

    def ignore_files(directory, files):
        return [f for f in files if os.path.isfile(os.path.join(directory, f))]

    shutil.copytree(sourceDir, targetDir, ignore=ignore_files)
    print("Directory tree cloned successfully.")

def listDir(dirPath, type=None):
    dirPath = os.path.expanduser(dirPath)
    
    if not os.path.exists(dirPath):
        print("The specified directory does not exist.")
        return []
    
    if not os.path.isdir(dirPath):
        print("The specified path is not a directory.")
        return []
    
    filename_list = []
    for file in scandir(dirPath):
        if type is None:
            filename_list.append(file.name)
        elif type == "dir" and file.is_dir():
            filename_list.append(file.name)
        elif type == "file" and file.is_file():
            filename_list.append(file.name)
    
    return filename_list