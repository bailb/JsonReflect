#coding=utf-8
import json

class Element(object):
        def __init__(self,level,name,desc,eleType):
                self._level=level
                self._name=name
                self._desc=desc
                self._eleType=eleType

class ElementList(object):
        def __init__(self):
            self._eleList=[]

        def push_back(self,aElement):
            self._eleList.append(aElement)
            return self._eleList;
        def push(self,aElement):
            self._eleList.append(aElement)
        def pushParam(self,level,name,desc,eleType):
            aElem=Element(level,name,desc,eleType)
            self.push(aElem)
        def pop(self):
            if (len(self._eleList) > 0):
                return self._eleList.pop()
            else:
                return None
        def count(self):
            return len(self._eleList)

        def getIndex(self,index):
            if (len(self._eleList) > index):
                return self._eleList[index]
            else:
                return None

def getType(value):
    if(isinstance(value,dict)):
        return 'obj'
    elif(isinstance(value,list)):
        if(isinstance(value[0],str) or isinstance(value[0],unicode)):
            return 'varlist'
        else:
            return 'objlist'
    elif(isinstance(value,str) or isinstance(value,unicode)):
        return 'var'

def getDesc(string):
    if(isinstance(string,str) or isinstance(string,unicode)):
        return string
    else:
        return ""

def isListLegal(value):
    if(len(value) > 1):
        return False
    if(isinstance(value[0],list) or isinstance(value[0],dict) or isinstance(value[0],str) or isinstance(value[0],unicode)):
        return True
    else:
        return False

def decodeJson(jsonStr,elementList,i):
    if(isinstance(jsonStr,dict)):
        for item in jsonStr:
#            print("item  : ["+item + "] getType[ "+ getType(jsonStr[item]) + "] type %s %s"%(type(jsonStr[item]),i))
            desc=getDesc(jsonStr[item])
            valueType=getType(jsonStr[item])
            aElem=Element(i,item,desc,valueType)
            elementList.push_back(aElem)

            if(isinstance(jsonStr[item],dict)):
                decodeJson(jsonStr[item],elementList,i=i+1)
            elif(isinstance(jsonStr[item],list)):
                if(False == isListLegal(jsonStr[item])):
                    print("This json wasn't right["+item+"]")
                    return False
                decodeJson(jsonStr[item],elementList,i=i+1)
            elif(isinstance(jsonStr[item],str) or isinstance(jsonStr[item],unicode)):
#                print("****%s"%jsonStr[item])
                 pass
            else:
#                print("ERROR type:%s" % type(jsonStr[item]))
                pass
    elif(isinstance(jsonStr,list)):
        length=len(jsonStr)
        for j in range(0, length):
            if(isinstance(jsonStr[j],dict)):
                decodeJson(jsonStr[j],elementList,i=i+1)
            else:
                pass
#                print("type [%s]"%type(jsonStr[j]))
    else:
        print("jsonStr is not json object!")
    return True
