"""
Author: Muhammad Umar Riaz
"""
import os
import glob

def folder2files(dataDir, format='.png'):
    """
    Function: It creates a list of all the files present in all the
              subfolders of dataDir.
    Input:
        dataDir: folder path containing the subfolders where the
                 files of interest are present.
    Output:
        dataList: list of files in the subfolders of dataDir.
    """
    dataList = []
    for dirName, subdirList, fileList in os.walk(dataDir):
      dataList = dataList + sorted(glob.glob(dirName + '/*' + format))
    return dataList
