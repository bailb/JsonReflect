#include<iostream>
#include<string>
#include "MetaDesc.h"

using namespace std;
class $META_NAME$ : public TransBaseObj 
{
public: //request
$META_STRUCT$
private:
    DEFINE_METAINFO($META_STRUCT_ROOT$); 
public:
    $META_NAME$();
    ~$META_NAME$();
    void dump() {dumpMeta(METAINFO($META_STRUCT_ROOT$));};
};
