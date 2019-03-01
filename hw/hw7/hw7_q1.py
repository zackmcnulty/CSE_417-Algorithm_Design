'''
Zachary McNulty
zmcnulty (1636402)

hw7_q1.py
'''
RUN_RANDOM_TEST_CASES = False

import numpy as np
import time

next_seq = input("Next sequence (Q to quit): ")
while 'Q' not in next_seq:
    print(next_seq)

    start = time.time()
    [pairings, OPT] = Nussinov(seq)
    
    runtime = time.time() - start
    n = len(seq)
    num_pairs = pairings.count(')')

    print(pairings)
    print("Length = ", n, ", Pairs = ", num_pairs, " Time = ", runtime, " sec")
    
    if n < 25:
        print_opt(OPT)

    print("")

def Nussinov(seq):
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
    n = len(seq)
    OPT = np.zeros((n,n), dtype=int)

    
    # let k be the length of our subsequence
    # let i be the start of the subsequence
    # note by the "no sharp turns" condition, k > 4
    # NOTE: since we start with the shorter subintervals first, we are
    # guarenteed to have all subproblems complete by the time they are needed.
    for k in range(5, n):
        for i in range(1, n-k+1):
            j = i + k
            
            no_pair = OPT[i, j-1]
            pair_at_tj = 1 + max([OPT[i, t-1] + OPT[t+1, j-1] for t in range(i, j-4) if can_pair(seq[j], seq[t])])

            OPT[i,j] = max(no_pair, pair_at_tj)
    
    # NOTE: run traceback algorithm and set pairs[t] = '(' and pairs[j] = ')' when necessary
    pairings = traceback(OPT, n, n)
    return [pairings, OPT]


def can_pair(base1, base2):
    return set([base1, base2]) == set(['A', 'U']) or set([base1, base2]) == set(['G', 'C'])

def print_opt(OPT):
    for row in OPT:
        for num in row:
            print('{:>5}'.format(str(num)), end='')

        print('\n')


def random_seq(n):
    return "".join(np.random.choice(['A', 'G', 'C', 'U'], size=n))

def traceback(OPT, i, j):
    if i < 0 or j < i:
        return ""
    elif OPT[i, j] == OPT[i, j-1]:
        return traceback(OPT, i, j-1) + '.'
    else:
        for t in range(i, j-4):
            if OPT[i, j] == 1 + OPT[i, t-1] + OPT[t + 1, j-1]:
                return traceback(OPT, i, t-1) + "(" + traceback(OPT,t+1, j-1) + ")"

