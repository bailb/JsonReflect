import jsonUtils
import json
import JsonReflect
import sys;
import os;
sys.path.append("./pyutils")
import cppUtils as langUtils 


def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    fileList = [];
    for allDir in pathDir:
        filePath = os.path.join('%s/%s' % (filepath, allDir))
        fileList.append(filePath);
        print filePath 
    return fileList 

fileList = eachFile("./proto");
langUtils.genCode(fileList);
