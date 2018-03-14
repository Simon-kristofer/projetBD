/*----------------------------------------------------------------------
 File     : aprioritest.cpp
 Contents : apriori algorithm for finding frequent sets
 ----------------------------------------------------------------------*/

#include "AprioriSets.h"

#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;
int main(int argc, char *argv[])
{
    cout << "Apriori frequent itemset mining implementation" << endl;

    if (argc < 3)
    {
        cerr << "usage: " << argv[0] << " datafile minsup [output]" << endl;
    }
    else
    {
        AprioriSets a;
        a.setVerbose(); // print information on nr of candidate itemsets etc
        a.setData(argv[1], 3);

        a.setCountType(2);
        // 1: to check k-subsets of transaction in set of candidates
        // 2: to check all candidates in transaction (default - best performance)

        a.setMinSup(atoi(argv[2]));
        if (argc == 4) a.setOutputSets(argv[3]);

        clock_t start = clock();
        int sets = a.generateSets();
        cout << sets << "\t[" << (clock() - start) / double(CLOCKS_PER_SEC) << "s]" << endl;
        if (argc == 4) cout << "Frequent sets written to " << argv[3] << endl;
    }

    return 0;
}

