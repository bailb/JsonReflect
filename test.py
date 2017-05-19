import jsonUtils
import json
import JsonReflect
encodejson = json.load(open("json.data",'r'))
eList = jsonUtils.ElementList()
JsonReflect.conToClassDesc(encodejson,eList)

print("----------------------------------")
def tab(num):
    space='    '
    while(num):
        num=num-1
        space+='    '
    return space

print("class requestData {")
for i in range(eList.count()):
    aEl=eList.getIndex(i)
    if (aEl._eleType == 'objlistbegin'):
        print(tab(aEl._level)+"class "+aEl._name+"Element {")
    elif(aEl._eleType == 'objlistend'):
        print(tab(aEl._level)+"};")
        print(tab(aEl._level)+"List<"+aEl._name+"Element>"+aEl._name+'\n')
    elif(aEl._eleType == 'objbegin'):
        print(tab(aEl._level)+"class "+aEl._name+"Element {")
    elif(aEl._eleType == 'objend'):
        print(tab(aEl._level)+"};")
        print(tab(aEl._level)+aEl._name+"Element "+aEl._name+";\n")
    elif(aEl._eleType == 'var'):
        print(tab(aEl._level)+aEl._name+";")
    elif(aEl._eleType == 'varlist'):
        print(tab(aEl._level)+aEl._name+"[];")
print("};")
# print("i[%s] desc[%s] type[%s] name[%s] [%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i))
