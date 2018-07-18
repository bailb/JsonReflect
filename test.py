import jsonUtils
import json
import JsonReflect
encodejson = json.load(open("./proto/json.data",'r'))
eList = jsonUtils.ElementList()
JsonReflect.conToClassDesc(encodejson,eList)

def getValueType(desc):
    if not (desc.startswith("[")):
        return "string";
    elif (desc.startswith("[int]")):
        return "int";
    elif (desc.startswith("[long]")):
        return "long";
    elif (desc.startswith("[bool]")):
        return "bool";
    elif (desc.startswith("[float]")):
        return "float"
    else:
        return desc.split("[")[1].split("]")[0];

def eleToCode(element):
    valueType = getValueType(element._desc);
    if (element._eleType == "var" or element._eleType == "obj"):
        return ("\t"+valueType+" "+element._name+";");
    elif (element._eleType == "objlist" or element._eleType == "varlist"):
        return ("\tstd::list<"+valueType+"> "+element._name+";"); 

def conToClassEx(eList):
    classStack = jsonUtils.ElementList();
    listCount = eList.count();
    if(listCount <= 0):
        print("eListCount shouldn't be lt 0");
        return None;
    statckTopLevel=-1;
    codeString="";
    for i in range(0,listCount):
        aEl=eList.getIndex(i);
        if (aEl._level >= statckTopLevel):
            classStack.push(aEl);
            statckTopLevel = aEl._level;
            #print("level[%s] desc[%s] type[%s] name[%s] index[%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i));
        elif(aEl._level < statckTopLevel):
            keyFlag=aEl._name;
            objLevel=aEl._level;
            print("struct "+aEl._name+"_Element {");
            codeString +=("struct "+aEl._name+"_Element { \n");
            while(True):
                topEl=classStack.pop();
                if (topEl._level == objLevel):
                    print("};\n");
                    codeString += "};\n";
                    break;
                if (topEl._level >= statckTopLevel):
                    statckTopLevel = topEl._level;
                    print(eleToCode(topEl));
                    codeString += (eleToCode(topEl)+"\n");
                   # print("\tlevel[%s] desc[%s] type[%s] name[%s] index[%s]"%(topEl._level,topEl._desc,topEl._eleType,topEl._name,i));                    
                elif(topEl._level < statckTopLevel):
                    statckTopLevel = topEl._level;
                    print(tab(aEl._level)+ "sfasdfdsf level[%s] desc[%s] \
                     type[%s] name[%s] index[%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i));
                    break;

            objElement=jsonUtils.Element(objLevel,aEl._name,"["+aEl._name+"_Element] list","obj");
            statckTopLevel-=1;
            if (aEl._eleType == "objend"):
                objElement=jsonUtils.Element(objLevel,aEl._name,"["+aEl._name+"_Element] list","obj");                
            elif (aEl._eleType == "objlistend"):
                objElement=jsonUtils.Element(objLevel,aEl._name,"["+aEl._name+"_Element] list","objlist");
            classStack.push(objElement);
    return codeString;

def getCPPValueType(desc):
    if not (desc.startswith("[")):
        return "FIELD_TYPE_STRING";
    elif (desc.startswith("[int]")):
        return "FIELD_TYPE_INT";
    elif (desc.startswith("[long]")):
        return "FIELD_TYPE_INT";
    elif (desc.startswith("[bool]")):
        return "FIELD_TYPE_BOOL";
    elif (desc.startswith("[float]")):
        return "FIELD_TYPE_FLOAT"
    else:
        return desc.split("[")[1].split("]")[0];

def conJstrToMetaInfo(eList):
    classStack = jsonUtils.ElementList();
    listCount = eList.count();
    if(listCount <= 0):
        print("eListCount shouldn't be lt 0");
        return None;
    codeString = "";
    stackTopLevel=0;
    for i in range(0,listCount):
        aEl=eList.getIndex(i);
        #print("==============type:"+aEl._eleType+ " name:"+aEl._name+" level %s"%aEl._level);
        if (i == 0 or (aEl._level ==0 and (aEl._eleType.startswith("objbegin") or aEl._eleType.startswith("objlistbegin")))):
            classStack.push(aEl);
            stackTopLevel = aEl._level;
            print(tab(aEl._level)+"METAINFO_CREATE("+aEl._name+"_Element);");
            codeString += (tab(aEl._level)+"METAINFO_CREATE("+aEl._name+"_Element);\n");
        else:
           # print("type:"+aEl._eleType);
            stackTopEl=classStack.getIndex(classStack.count()-1); #just look, don't pop
            if (aEl._eleType.startswith("objlistbegin") or aEl._eleType.startswith("objbegin")):
                if (aEl._eleType.startswith("objbegin")):
                    print(tab(aEl._level)+ "METAINFO_CHILD_BEGIN("+stackTopEl._name+"_Element,"+aEl._name+"_Element,"+aEl._name+");"); 
                    codeString += (tab(aEl._level)+ "METAINFO_CHILD_BEGIN("+stackTopEl._name+"_Element,"+aEl._name+"_Element,"+aEl._name+");\n");
                else:
                    print(tab(aEl._level)+ "METAINFO_CHILD_LIST_BEGIN("+stackTopEl._name+"_Element,"+aEl._name+"_Element,"+aEl._name+");");
                    codeString += (tab(aEl._level)+ "METAINFO_CHILD_LIST_BEGIN("+stackTopEl._name+"_Element,"+aEl._name+"_Element,"+aEl._name+");\n");

                classStack.push(aEl)
                stackTopLevel = aEl._level;
            elif (aEl._eleType.startswith("varlist")):
                print(tab(aEl._level)+ "METAINFO_ADD_MEMBER_LIST("+stackTopEl._name+"_Element,"+getCPPValueType(aEl._desc)+","+aEl._name+");");
                codeString += (tab(aEl._level)+ "METAINFO_ADD_MEMBER_LIST("+stackTopEl._name+"_Element,"+getCPPValueType(aEl._desc)+","+aEl._name+");\n");

            elif ((aEl._eleType.startswith("objlistend") or aEl._eleType.startswith("objend")) and i < listCount-1):
                print(tab(aEl._level)+  "METAINFO_CHILD_END();\n");
                codeString += (tab(aEl._level)+  "METAINFO_CHILD_END();\n\n");
                classStack.pop();#just pop
            elif (aEl._eleType.startswith("var")):
                print(tab(aEl._level)+ "METAINFO_ADD_MEMBER("+stackTopEl._name+"_Element,"+getCPPValueType(aEl._desc)+","+aEl._name+");");
                codeString += (tab(aEl._level)+ "METAINFO_ADD_MEMBER("+stackTopEl._name+"_Element,"+getCPPValueType(aEl._desc)+","+aEl._name+");\n");

    return codeString;



def tab(num):
    space='    '
    while(num):
        num=num-1
        space+='    '
    return space

def getEndLine(elementList,level,start):
    for i in range(start,elementList.count()):
        aEl=elementList.getIndex(i)
        if (aEl._level == level and aEl._eleType.endswith("end")):
            return i

def generateClass(elementList,start,end):
    LoopLine=start
    while(LoopLine <= end):
        aEl=elementList.getIndex(LoopLine)
        if (aEl._eleType.endswith("begin")):
            line=getEndLine(elementList, aEl._level,LoopLine)
            LoopLine=line+1
            if (aEl._eleType.startswith("objlist")):
                print("    list<"+aEl._name+"Element>"+aEl._name+";")
            else:
                print("    "+aEl._name+"Element "+aEl._name+";")
        else:
             LoopLine = LoopLine + 1
             print("    "+aEl._name)

def dumpClass(elementList):
    level=0
    for i in range(elementList.count()):
        aEl=elementList.getIndex(i)
        print("name:"+aEl._name+"    level %s"%aEl._level+ "type:"+aEl._eleType)
        if (aEl._eleType.startswith("objlistbegin") or aEl._eleType.startswith("objbegin") ):
            level=aEl._level
            endline=getEndLine(elementList,level,i);
            print("struct "+elementList.getIndex(i)._name+"Element {");
            generateClass(elementList,i+1,endline-1)
            print("}")

def genRequestClass(elementList):
    print("struct requestData {")
    end=eList.count()-1
    generateClass(elementList,0,end);
    print("};")

#for i in range(eList.count()):
#    print("name["+eList.getIndex(i)._name+"]\t\ttype["\
#    +eList.getIndex(i)._eleType+"]"+"\t\t level[%s]"%+eList.getIndex(i)._level);




print("=======================================1111111111=")
#dumpClass(eList)
print("=======================================2222222222=")
#genRequestClass(eList)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
structCode=conToClassEx(eList)
print("lllllllllllllllllllllllllllllllllllllllllllllllllllll")
metaCode=conJstrToMetaInfo(eList)
#generateClass(eList,0,15)
#print("i[%s] desc[%s] type[%s] name[%s] [%s]"%(aEl._level,aEl._desc,aEl._eleType,aEl._name,i))
f = open('./template/CppSource.cpp','r')
contents = f.read()
print(contents);
f.close();

contents1= contents.replace("$META_STRUCT$",structCode);
contents1= contents1.replace("$META_NAME$","json");
f = open('xxxxxxx.cpp','w')
f.write(contents1.replace("$META_INFO_DESC$",metaCode));
f.close();

###########################################################
f = open('./template/CppHeader.h','r')
contents = f.read()
print(contents);
f.close();

contents1= contents.replace("$META_STRUCT$",structCode);
contents1= contents1.replace("$META_NAME$","json");
f = open('./templatexxxxxxx.h','w')
f.write(contents1.replace("$META_INFO_DESC$",metaCode));
f.close();

