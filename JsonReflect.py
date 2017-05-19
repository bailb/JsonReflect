import jsonUtils
import json

def conToClassDesc(encodejson,eList):
    originElemList=jsonUtils.ElementList()
    if (jsonUtils.decodeJson(encodejson,originElemList,0) == False):
        return False
    eStack = jsonUtils.ElementList()
    listCount = originElemList.count()
    for i in range(0,listCount):
        aEl=originElemList.getIndex(i)
#        print("i[%s] desc[%s] type[%s] name[%s] [%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i))
        if (aEl._eleType == 'objlist' or aEl._eleType == 'obj'):
            if (eStack.count() == 0):
                eStack.push(aEl)
                eList.pushParam(aEl._level,aEl._name,aEl._desc,aEl._eleType+"begin")
            else:
                ele=eStack.pop()
                if(ele._level == aEl._level):
                    eList.pushParam(ele._level,ele._name,ele._desc,ele._eleType+"end")
                else:
                    eStack.push(ele)
                eList.pushParam(aEl._level,aEl._name,aEl._desc,aEl._eleType+"begin")
                eStack.push(aEl)
        elif(aEl._eleType == 'var' or aEl._eleType == 'varlist'):
            if (eStack.count() == 0):
                eStack.push(aEl)
            else:
                ele=eStack.pop()
                if(ele._level == aEl._level):
                    eList.pushParam(ele._level,ele._name,ele._desc,ele._eleType+"end")
                else:
                    eStack.push(ele)
            eList.pushParam(aEl._level,aEl._name,aEl._desc,aEl._eleType)

    while (eStack.count() > 0):
        aEl=eStack.pop()
        eList.pushParam(aEl._level,aEl._name,aEl._desc,aEl._eleType+"end")
