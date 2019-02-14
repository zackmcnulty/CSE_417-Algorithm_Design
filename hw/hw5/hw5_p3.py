def fraud_checker(cards):
    results = fraud_checker_helper(cards)
    print(results)
    if results[1] > len(cards) // 2:
        print("I smell fraud! ", results[0], " has been found equivalent to ", results[1] - 1 , " other cards.")
    else:
        print("All clear of fraud!")


# cards =  our set of n credit cards
def fraud_checker_helper(cards):
    # base case: problem only has a single card, so it is
    # easy to check which card type is most represented in
    # this subproblem: it must be whatever type the one card is
    n = len(cards)
    if n == 1:
        return [cards[0], 1]
    else:
        sub1 = cards[:n//2] # first half-ish of cards
        sub2 = cards[n//2:] # second half-ish of cards

        # recursive steps
        [card_type1, max_sub1] = fraud_checker_helper(sub1)
        [card_type2, max_sub2] = fraud_checker_helper(sub2)

        # current level's workload
        
        # taking the card type most common in one of the subproblems,
        # find how many cards in the other subproblem match its card type
        # (i.e. are equivalent to the most common cards)
        for card in sub2:
            # Check if the two cards are equivalent
            if card == card_type1:
                max_sub1 += 1

        for card in sub1:
            # Check if the two cards are equivalent
            if card == card_type2:
                max_sub2 += 1

        if max_sub1 > max_sub2:
            return [card_type1, max_sub1]
        else:
            return [card_type2, max_sub2]


# ============================================= testing code
cards = [0,0,1,2,2,2,2,2, 1, 1,1,1,1 ]
print(len(cards))
fraud_checker(cards)


# 2 2 3 3 3 | 2 2 4 4 4
