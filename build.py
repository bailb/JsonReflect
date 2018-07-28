import jsonUtils
import json
import JsonReflect
import sys;
import os;
sys.path.append("./langUtils")
import cppUtils as langUtils 

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    fileList = [];
    for allDir in pathDir:
        filePath = os.path.join('%s/%s' % (filepath, allDir))
        fileList.append(filePath);
        print filePath 
    return fileList 
lth=len(sys.argv) 
if (lth <= 1):
    langType="cpp";
else:
    langType=sys.argv[1];
if (langType == "cpp"):
    print("generate cpp code");
    fileList = eachFile("./proto");
    langUtils.genCode(fileList);
else:
    print(langType+" not support yet ");

