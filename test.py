import jsonUtils
import json
import JsonReflect
encodejson = json.load(open("json.data",'r'))
eList = jsonUtils.ElementList()
JsonReflect.conToClassDesc(encodejson,eList)

print("----------------------------------")
for i in range(eList.count()):
    aEl=eList.getIndex(i) 
    print("i[%s] desc[%s] type[%s] name[%s] [%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i))

#print("----------------------------------")
#for i in range(eStack.count()):
#    aEl=eStack.getIndex(i) 
#    print("i[%s] desc[%s] type[%s] name[%s] [%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i))


