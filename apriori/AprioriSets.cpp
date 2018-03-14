/*----------------------------------------------------------------------
 File     : AprioriSets.cpp
 Contents : apriori algorithm for finding frequent sets
 ----------------------------------------------------------------------*/

#include "AprioriSets.h"

#include <ctime>
#include <algorithm>
#include <iostream>

using namespace std;

AprioriSets::AprioriSets()
{
    data = 0;
    minsup = 0;
    remap = 0;
    relist = 0;
    trie = new Item(0);
    verbose = false;
    countType = 1;
}

AprioriSets::~AprioriSets()
{
    if (data) delete data;
    if (trie)
    {
        trie->deleteChildren();
        delete trie;
    }
    if (remap) delete remap;
    if (relist) delete relist;
}

void AprioriSets::setData(char *fn, int type)
{
    data = new Data(fn, type);
}

int AprioriSets::setOutputSets(char *fn)
{
    setsout.open(fn);
    if (!setsout.is_open())
    {
        cerr << "error: could not open " << fn << endl;
        return -1;
    }
    return 0;
}

int AprioriSets::generateSets()
{
    int total = 0, pass = 0;
    bool running = true;

    while (running)
    {
        clock_t start;
        int generated = 0, nodes = 0, tnr = 0, pruned;

        pass++;
        cout << pass << " " << flush;

        if (pass > 2)
        {
            start = clock();
            generated = generateCandidates(pass);
            nodes = pruneNodes(pass);
            if (verbose) cout << generated << " [" << (clock() - start) / double(CLOCKS_PER_SEC) << "s] " << flush;
        }

        start = clock();
        tnr = countCandidates(pass);
        if (verbose)
        {
            if (pass == 1) cout << trie->getChildren()->size() << " ";
            cout << tnr << " [" << (clock() - start) / double(CLOCKS_PER_SEC) << "s] " << flush;
        }

        if (pass == 1 && setsout.is_open()) printSet(*trie, 0, 0);

        start = clock();
        pruned = pruneCandidates(pass);
        if (verbose) cout << pruned << " [" << (clock() - start) / double(CLOCKS_PER_SEC) << "s]\n" << flush;

        if (pass == 1) ReOrder(); // Reorder all items

        total += pruned;
        if (pruned <= pass) running = false;
    }

    cout << endl;

    return total;
}

int AprioriSets::generateCandidates(int level)
{
    int *tmp = new int[level];
    int generated = generateCandidates(level, trie->getChildren(), 1, tmp);
    delete[] tmp;

    return generated;
}

int AprioriSets::generateCandidates(int level, set<Item> *items, int depth, int *current)
{
    if (items == 0) return 0;

    int generated = 0;
    set<Item>::reverse_iterator runner;

    if (depth == level - 1)
    {
        for (runner = items->rbegin(); runner != items->rend(); runner++)
        {
            current[depth - 1] = runner->getId();
            set<Item> *children = runner->makeChildren();

            for (set<Item>::reverse_iterator it = items->rbegin(); it != runner; it++)
            {
                current[depth] = it->getId();
                if (level <= 2 || checkSubsets(level, current, trie->getChildren(), 0, 1))
                {
                    children->insert(Item(it->getId()));
                    generated++;
                }
            }
        }
    }
    else
    {
        for (runner = items->rbegin(); runner != items->rend(); runner++)
        {
            current[depth - 1] = runner->getId();
            generated += generateCandidates(level, runner->getChildren(), depth + 1, current);
        }
    }
    return generated;
}

bool AprioriSets::checkSubsets(int sl, int *iset, set<Item> *items, int spos, int depth)
{
    if (items == 0) return 0;

    bool ok = true;
    set<Item>::iterator runner;
    int loper = spos;
    spos = depth + 1;

    while (ok && (--spos >= loper))
    {
        runner = items->find(Item(iset[spos]));
        if (runner != items->end())
        {
            if (depth < sl - 1) ok = checkSubsets(sl, iset, runner->getChildren(), spos + 1, depth + 1);
        }
        else ok = false;
    }

    return ok;
}

int AprioriSets::pruneNodes(int level)
{
    return pruneNodes(level, trie->getChildren(), 1);
}

int AprioriSets::pruneNodes(int level, set<Item> *items, int depth)
{
    if (items == 0) return 0;

    int nodes = 0;

    if (depth == level) nodes = items->size();
    else
    {
        for (set<Item>::iterator runner = items->begin(); runner != items->end();)
        {
            int now = pruneNodes(level, runner->getChildren(), depth + 1);
            if (now)
            {
                nodes += now;
                nodes++;
                runner++;
            }
            else
            {
                runner->deleteChildren();
                set<Item>::iterator tmp = runner++;
                items->erase(tmp);
            }
        }
    }

    return nodes;
}

int AprioriSets::countCandidates(int level)
{
    int trans = 0;

    // count all single items
    if (level == 1)
    {
        while (Transaction *t = data->getNext())
        {
            trie->Increment();

            int *iset = t->t, sl = t->length;
            set<Item> *items = trie->makeChildren();
            for (int i = 0; i < sl; i++)
            {
                Item item(iset[i]);
                set<Item>::iterator runner = items->find(item);
                if (runner == items->end()) runner = (items->insert(item)).first;
                runner->Increment();
            }
            trans++;
            delete t;
        }
    }
    else
    {
        while (Transaction *t = data->getNext())
        {
            if (t->length >= level)
            {
                // Reorder transaction
                int i;
                vector<int> list;
                for (i = 0; i < t->length; i++)
                {
                    set<Element>::iterator it = relist->find(Element(t->t[i]));
                    if (it != relist->end()) list.push_back(it->id);
                }
                int size = list.size();
                sort(list.begin(), list.end());
                delete t;
                t = new Transaction(size);
                for (i = 0; i < size; i++)
                    t->t[i] = list[i];

                if (countType == 1 || level <= 2)
                {
                    if (processTransaction(level, t, trie->getChildren(), 0, 1)) trans++;
                }
                else
                {
                    if (processTransaction2(level, t, trie->getChildren(), 0, 1)) trans++;
                }

                delete t;
            }
        }
    }
    return trans;
}

int AprioriSets::processTransaction2(int level, Transaction *t, set<Item> *items, int spos, int depth)
{
    if (items == 0) return 0;
    int used = 0, max = t->length - level + depth;

    for (set<Item>::iterator it = items->begin(); spos < max && it != items->end(); it++)
    {
        while (spos < max && t->t[spos] < it->getId())
            spos++;
        if (spos < max && (t->t[spos] == it->getId()))
        {
            if (depth == level)
            {
                it->Increment();
                used++;
            }
            else used += processTransaction2(level, t, it->getChildren(), spos + 1, depth + 1);
        }
    }

    return used;
}

int AprioriSets::processTransaction(int level, Transaction *t, set<Item> *items, int spos, int depth)
{
    if (items == 0) return 0;

    int used = 0, *iset = t->t, sl = t->length, loper = spos;
    set<Item>::iterator runner;

    spos = sl - (level - depth);
    while (--spos >= loper)
    {
        runner = items->find(Item(iset[spos]));
        if (runner != items->end())
        {
            if (depth == level)
            {
                runner->Increment();
                used++;
            }
            else
            {
                if (depth == 1 && level == 2) runner->makeChildren();
                used += processTransaction(level, t, runner->getChildren(), spos + 1, depth + 1);
            }
        }
        else if (depth == 2 && level == 2)
        {
            set<Item> *singles = trie->getChildren();
            if (singles->find(Item(iset[spos])) != singles->end())
            {
                runner = items->insert(Item(iset[spos])).first;
                runner->Increment();
                used++;
            }
        }
    }

    return used;
}

int AprioriSets::pruneCandidates(int level)
{
    int pruned;
    int *tmp = new int[level];
    pruned = pruneCandidates(level, trie->getChildren(), 1, tmp);
    delete[] tmp;
    return pruned;
}

int AprioriSets::pruneCandidates(int level, set<Item> *items, int depth, int *itemset)
{
    if (items == 0) return 0;
    int left = 0;

    for (set<Item>::iterator runner = items->begin(); runner != items->end();)
    {
        itemset[depth - 1] = runner->getId();

        if (depth == level)
        {
            if (runner->getSupport() < minsup)
            {
                runner->deleteChildren();
                set<Item>::iterator tmp = runner++;
                items->erase(tmp);
            }
            else
            {
                if (setsout.is_open()) printSet(*runner, itemset, depth);
                left++;
                runner++;
            }
        }
        else
        {
            int now = pruneCandidates(level, runner->getChildren(), depth + 1, itemset);
            if (now)
            {
                left += now;
                runner++;
            }
            else
            {
                runner->deleteChildren();
                set<Item>::iterator tmp = runner++;
                items->erase(tmp);
            }
        }
    }

    return left;
}

void AprioriSets::printSet(const Item& item, int *itemset, int length)
{
    set<int> outset;

    for (int j = 0; j < length; j++)
        if (remap) outset.insert(remap[itemset[j]]);
        else outset.insert(itemset[j]);
    for (set<int>::iterator k = outset.begin(); k != outset.end(); k++)
        setsout << *k << " ";
    setsout << "(" << item.getSupport() << ")" << endl;
}

void AprioriSets::ReOrder()
{
    set<Item> *src = trie->getChildren();
    set<Item>::iterator itI;
    multiset<Element>::iterator itE;
    multiset<Element> list;

    for (itI = src->begin(); itI != src->end(); itI++)
        list.insert(Element(itI->getSupport(), itI->getId()));

    remap = new int[list.size() + 1];
    relist = new set<Element> ;
    src->clear();
    int i = 1;
    for (itE = list.begin(); itE != list.end(); itE++)
    {
        if (itE->oldid >= minsup)
        {
            remap[i] = itE->id;
            relist->insert(Element(itE->id, i));
            Item a(i);
            a.Increment(itE->oldid);
            src->insert(a);
            i++;
        }
    }
}

