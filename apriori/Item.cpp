/*----------------------------------------------------------------------
 File     : Item.cpp
 Contents : itemset management
 ----------------------------------------------------------------------*/

#include "Item.h"

using namespace std;
set<Item> *Item::makeChildren() const
{
    if (children) return children;
    return children = new set<Item> ;
}

int Item::deleteChildren() const
{
    int deleted = 0;

    if (children)
    {
        for (set<Item>::iterator it = children->begin(); it != children->end(); it++)
        {
            deleted += it->deleteChildren();
        }
        delete children;
        children = 0;
        deleted++;
    }

    return deleted;
}
