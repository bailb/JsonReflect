#include<string>
#include<vector>
#include<list>
#include<stddef.h>
#include<stdio.h>

using namespace std;

typedef enum {

    FIELD_TYPE_INT,
    FIELD_TYPE_FLOAT,
    FIELD_TYPE_STRING,
    FIELD_TYPE_BOOL,
    FIELD_TYPE_OBJECT

}FIELD_TYPE;

class CMeta_info;

struct CField_info 
{

    int offset;
    FIELD_TYPE type;
    string name;
    bool islist;
    CMeta_info *metaInfo;

    CField_info &operator=(const CField_info &field) 
    {
        this->offset = field.offset;
        this->type   = field.type;
        this->islist = field.islist;
        this->metaInfo = field.metaInfo;
        return *this;
    }

};

class CMeta_info 
{
    private:
        vector<CField_info> mFields;

    public:

		void addField(const CField_info &field)
        {
            mFields.push_back(field);
        }
		
        const CField_info& getField(int i)
        {
            return mFields[i];
        }

        int getCount()
        {
            return mFields.size();
        }

}; 

void metainfo_add_member(CMeta_info *mi, int pos, int type, const char *name, bool islist)
{
    CField_info f;
    f.offset = pos;
    f.type = (FIELD_TYPE) type; 
    f.islist = islist;
    f.name = name;
    f.metaInfo = NULL;
	mi->addField(f);
}

CMeta_info *metainfo_add_child(CMeta_info *mi, int pos, const char *name, bool islist)
{
    CMeta_info *child = new CMeta_info();
    CField_info f;
    f.offset = pos;
    f.type = FIELD_TYPE_OBJECT;
    f.islist = islist;
    f.name = name;
    f.metaInfo = child;
   	mi->addField(f); 
	return child;
}

void dumpMeta(CMeta_info *metaInfo)
{
	int len = metaInfo->getCount();

	for(int i=0;i<len;i++)
	{
		CField_info f=metaInfo->getField(i);
		printf("name[%s] pos[%d]\n",f.name.c_str(),f.offset);
		if (f.metaInfo) 
		{
			dumpMeta(f.metaInfo);
		}
	}
}

#define METAINFO(s)                         _metainfo_##s
#define DEFINE_METAINFO(s)                  CMeta_info *METAINFO(s);

#define METAINFO_CREATE(s)                  METAINFO(s) = new CMeta_info();
#define METAINFO_DESTROY(s)                 metainfo_destroy(METAINFO(s))

#define METAINFO_ADD_MEMBER(s, t, n)        metainfo_add_member(METAINFO(s), offsetof(struct s, n), t, #n, false)
#define METAINFO_ADD_MEMBER_LIST(s, t, n)   metainfo_add_member(METAINFO(s), offsetof(struct s, n), t, #n, true)
#define METAINFO_ADD_CHILD(s, t, n)         metainfo_add_child(METAINFO(s), offsetof(struct s, n), #n, false)
#define METAINFO_ADD_CHILD_LIST(s, t, n)    metainfo_add_child(METAINFO(s), offsetof(struct s, n), #n, true)

#define METAINFO_CHILD_BEGIN(s, t, n)       { CMeta_info *METAINFO(t) = METAINFO_ADD_CHILD(s, t, n);
#define METAINFO_CHILD_LIST_BEGIN(s, t, n)  { CMeta_info *METAINFO(t) = METAINFO_ADD_CHILD_LIST(s, t, n);
#define METAINFO_CHILD_END()                }

class TransBaseObj {
public:
    TransBaseObj(){};
    virtual ~TransBaseObj(){};
public:
    virtual bool genStr(){return true;};
    virtual string getSendStr() {return mTargetStr;};
    virtual bool overrideStr(const char* str) { mTargetStr = str;};
    virtual int send(){};
    virtual void dump(){};
public:
    std::string mRequestStr;
    std::string mResponseStr;

    std::string mTargetStr; //target
    int mTargetType;        //0:json 1:xml
};

