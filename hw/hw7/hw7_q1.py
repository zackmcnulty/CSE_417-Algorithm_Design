'''
Zachary McNulty
zmcnulty (1636402)

hw7_q1.py

OPT table Conventions

Entry (i,j) in the OPT table corresponds to the optimal number of pairs
in the sequence starting at base i and ending at base j. When 
printing out the OPT table to standard input, I follow the convention
found in the slides where each i value corresponds to a row with i = 0
at the top and i = n-1 at the bottom. Similarly, each j value
corresponds to a column with j = 0 at the far left and j = n-1
at the far right. This places the optimal value of the full
sequence in the upper right corner of the OPT table.

The main method is at the bottom of this file

'''
# run random test cases or not
# must be False to run tests from standard in
RUN_RANDOM_TEST_CASES = False

# For random test cases:  number of test cases of each size to run 
NUM_TRIALS = 3

# For random test cases: sizes of test cases to run
TEST_SIZES = list(range(100, 1000, 100))

import numpy as np
import time
import sys



def Nussinov(seq, output=True):
    '''
    Returns one of the optimal secondary structures for the given RNA sequence
    (following the assumptions of the Nussinov Algorithm; note this may not
    be the actual minimum energy structure)

    seq: a string of {A, G, C, U} characters representing the primary sequence of
        a given RNA

    returns predicted optimal secondary structure in the form of a formatted string
    where parenthesis represent pairing (each open and corresponding closed parentheses
    pair)

    GCCCACCUUCGAAAAGACUGGAUGACCAUGGGCCAUGAUU
    ((((....((.....)).(((....))).)))).......
    '''

    start = time.time()
    n = len(seq)
    OPT = np.zeros((n,n), dtype=int)
    BACKLINKS = {}

    
    # let k be the length of our subsequence
    # let i be the start of the subsequence
    # note by the "no sharp turns" condition, k > 4
    # NOTE: since we start with the shorter subintervals first, we are
    # guarenteed to have all subproblems complete by the time they are needed.
    for k in range(5, n): # interval lengths (end - start): 5 to n-1
        for i in range(n-k): # start positions: 0 to n-k-1
            j = i + k # end position
            
            no_pair = OPT[i, j-1]

            pair_at_tj = -1
            tval = -1

            for t in range(i, j-4):
                next_val = 1 + OPT[i, t-1] + OPT[t+1, j-1]
                if can_pair(seq[j], seq[t]) and next_val > pair_at_tj:
                    pair_at_tj = next_val
                    tval = t

            if pair_at_tj > no_pair:
                BACKLINKS[(i,j)] = [(i, tval-1), (tval+1, j-1)]
                OPT[i, j] = pair_at_tj
            else:
                BACKLINKS[(i,j)] = [(i,j-1)]
                OPT[i,j] = no_pair

    
    # NOTE: run traceback algorithm and set pairs[t] = '(' and pairs[j] = ')' when necessary
    pattern = ['.']*n

    Nussinov_runtime = time.time() - start

    trace_start = time.time()
    traceback(OPT, BACKLINKS, (0, n-1), pattern)
    trace_runtime = time.time() - trace_start

    if output:
        print(seq)
        print(''.join(pattern))
        num_pairs = pattern.count(')')
        runtime = trace_runtime + Nussinov_runtime
        print("Length = ", n, ", Pairs = ", num_pairs, ", Time = ", runtime, " sec")
        if n <= 25:
            print_opt(OPT)
        print("")



    return [''.join(pattern), OPT, Nussinov_runtime, trace_runtime]


def can_pair(base1, base2):
    return set([base1, base2]) == set(['A', 'U']) or set([base1, base2]) == set(['G', 'C'])

def print_opt(OPT):
    for row in OPT:
        for num in row:
            print('{:>5}'.format(str(num)), end='')

        print('')


def random_seq(n):
    return "".join(np.random.choice(['A', 'G', 'C', 'U'], size=n))

def traceback(OPT, BACKLINKS, pos, pattern):
    i = pos[0]
    j = pos[1]
    if not pos in BACKLINKS:
        return ""
    elif len(BACKLINKS[pos]) == 1:
        return traceback(OPT, BACKLINKS, (i, j-1), pattern)
    else:
        t = BACKLINKS[pos][0][1] + 1
        pattern[t] = "("
        pattern[j] = ")"
        traceback(OPT, BACKLINKS, BACKLINKS[pos][0], pattern)
        traceback(OPT, BACKLINKS, BACKLINKS[pos][1], pattern)




# =============================================

# NOTE MAIN PROGRAM
if RUN_RANDOM_TEST_CASES:
#    print("N, full runtime, Nussinov runtime, traceback runtime")

    for size in TEST_SIZES:
        for _ in range(NUM_TRIALS):
            [pattern, OPT, Nussinov_runtime, trace_runtime] = Nussinov(random_seq(size), output=True)
            #print(size, ", ", Nussinov_runtime + trace_runtime, ", ", Nussinov_runtime, ", ", trace_runtime)
else:
    for line in sys.stdin:
        next_seq = line.strip()
        Nussinov(next_seq)


