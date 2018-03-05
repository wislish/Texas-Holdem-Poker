# http://pokerpython.blogspot.com/

# create main_deck
from collections import Counter

main_deck = []
deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', ]

for x in deck:
    for s in ['H', 'D', 'C', 'S']:
        main_deck.append(x + s)
# print(main_deck)
# print(len(main_deck))

# evaluate hands, return hands type
def evaluate_hand(h):
    if is_royal(h):
        return "ROYAL FLUSH", h, 10
    elif is_seq(h) and is_flush(h):
        return "STRAIGHT FLUSH", h, 9
    elif is_fourofakind(h):
        _, fourofakind = is_fourofakind(h)
        return "FOUR OF A KIND", fourofakind, 8
    elif is_fullhouse(h):
        return "FULL HOUSE", h, 7
    elif is_flush(h):
        _, flush = is_flush(h)
        return "FLUSH", h, 6
    elif is_seq(h):
        _, seq = is_seq(h)
        return "STRAIGHT", h, 5
    elif is_threeofakind(h):
        _, threeofakind = is_threeofakind(h)
        return "THREE OF A KIND", threeofakind, 4
    elif is_twopair(h):
        _, two_pair = is_twopair(h)
        return "TWO PAIR", two_pair, 3
    elif is_pair(h):
        _, pair = is_pair(h)
        return "PAIR", pair, 2
    else:
        return "HIGH CARD", h, 1


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0]
# print (main_deck)
# print (len(main_deck))


# gets card value from  a hand. converts A to 14,  is_seq function will convert the 14 to a 1 when necessary to
# evaluate A 2 3 4 5 straightsv
def convert_tonums(h, nums={'T': 10, 'J': 11, 'Q': 12, 'K': 13, "A": 14}):
    for x in range(len(h)):
        if (h[x][0]) in nums.keys():
            h[x] = str(nums[h[x][0]]) + h[x][1]
    return h




# is royal flush
# if a hand is a straight and a flush and the lowest value is a 10 then it is a royal flush
def is_royal(h):
    nh = convert_tonums(h)
    if is_seq(h):
        if is_flush(h):
            nn = [int(x[:-1]) for x in nh]
            if min(nn) == 10:
                return True

    else:
        return False


# converts hand to number valeus and then evaluates if they are sequential
def is_seq(h):
    ace = False
    r = h[:]

    # keep the digit part
    h = [x[:-1] for x in convert_tonums(h)]

    h = [int(x) for x in h]
    h = list(sorted(h))
    ref = True
    for x in range(0, len(h) - 1):
        if not h[x] + 1 == h[x + 1]:
            ref = False
            break

    if ref:
        return True, r

    # consider A,2,3,4,5 situation
    aces = [i for i in h if str(i) == "14"]
    if len(aces) == 1:
        for x in range(len(h)):
            if str(h[x]) == "14":
                h[x] = 1

    h = list(sorted(h))
    for x in range(0, len(h) - 1):
        if not h[x] + 1 == h[x + 1]:
            return False
    return True, r


# call set() on the suite values of the hand and if it is 1 then they are all the same suit
def is_flush(h):
    # keep the suits part
    suits = [x[-1] for x in h]
    if len(set(suits)) == 1:
        return True, h
    else:
        return False


# if the most common element occurs 4 times then it is a four of a kind
def is_fourofakind(h):
    h = [a[:-1] for a in h]
    i = Most_Common(h)
    if i[1] == 4:
        return True, i[0]
    else:
        return False


# if the most common element occurs 3 times then it is a three of a kind
def is_threeofakind(h):
    h = [a[:-1] for a in h]
    i = Most_Common(h)
    if i[1] == 3:
        return True, i[0]
    else:
        return False


# if the first 2 most common elements have counts of 3 and 2, then it is a full house
def is_fullhouse(h):
    h = [a[:-1] for a in h]
    data = Counter(h)
    a, b = data.most_common(1)[0], data.most_common(2)[-1]
    if str(a[1]) == '3' and str(b[1]) == '2':
        return True, (a, b)
    return False


# if the first 2 most common elements have counts of 2 and 2 then it is a two pair
def is_twopair(h):
    h = [a[:-1] for a in h]
    data = Counter(h)
    a, b = data.most_common(1)[0], data.most_common(2)[-1]
    if str(a[1]) == '2' and str(b[1]) == '2':
        return True, (a[0], b[0])
    return False


# if the first most common element is 2 then it is a pair DISCLAIMER: this will return true if the hand is a two
# pair, but this should not be a conflict because is_twopair is always evaluated and returned first
def is_pair(h):
    h = [a[:-1] for a in h]
    data = Counter(h)
    a = data.most_common(1)[0]

    if str(a[1]) == '2':
        return True, (a[0])
    else:
        return False
# evaluate hands, return hands type
def evaluate_hand(h):
    if is_royal(h):
        return "ROYAL FLUSH", h, 10
    elif is_seq(h) and is_flush(h):
        return "STRAIGHT FLUSH", h, 9
    elif is_fourofakind(h):
        _, fourofakind = is_fourofakind(h)
        return "FOUR OF A KIND", fourofakind, 8
    elif is_fullhouse(h):
        return "FULL HOUSE", h, 7
    elif is_flush(h):
        _, flush = is_flush(h)
        return "FLUSH", h, 6
    elif is_seq(h):
        _, seq = is_seq(h)
        return "STRAIGHT", h, 5
    elif is_threeofakind(h):
        _, threeofakind = is_threeofakind(h)
        return "THREE OF A KIND", threeofakind, 4
    elif is_twopair(h):
        _, two_pair = is_twopair(h)
        return "TWO PAIR", two_pair, 3
    elif is_pair(h):
        _, pair = is_pair(h)
        return "PAIR", pair, 2
    else:
        return "HIGH CARD", h, 1


def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0]





# get the high card
def get_high(h):
    return list(sorted([int(x[:-1]) for x in convert_tonums(h)], reverse=True))[0]


# FOR HIGH CARD or ties, this function compares two hands by ordering the hands from highest to lowest and comparing
# each card and returning when one is higher then the other
def compare(xs, ys):
    # print("------------------------------------------")
    # print(xs)
    xs, ys = list(sorted(xs, reverse=True)), list(sorted(ys, reverse=True))

    for i, c in enumerate(xs):
        if ys[i] > c:
            return 'RIGHT'
        elif ys[i] < c:
            return 'LEFT'

    return "TIE"


def compare_hands(h1, h2):
    # print(h1)
    # print(h2)
    one, two = evaluate_hand(h1), evaluate_hand(h2)
    # print('--------------------')
    # print(evaluate_hand(h1))
    # print(evaluate_hand(h2))

    one, two = evaluate_hand(h1), evaluate_hand(h2)
    if one[0] == two[0]:

        if one[0] == "STRAIGHT FLUSH":

            sett1, sett2 = convert_tonums(h1), convert_tonums(h2)
            # get card digit
            sett1, sett2 = [int(x[:-1]) for x in sett1], [int(x[:-1]) for x in sett2]
            com = compare(sett1, sett2)


            if com == "TIE":
                return "none", one[1], two[1]
            elif com == "RIGHT":
                return "right", two[0], two[1]
            else:
                return "left", one[0], convert_toletters(one[1])


        elif one[0] == "TWO PAIR":

            leftover1, leftover2 = is_twopair(h1), is_twopair(h2)
            twm1, twm2 = max([int(x) for x in list(leftover1[1])]), max([int(x) for x in list(leftover2[1])])
            if twm1 > twm2:
                return "left", one[0], one[1]
            elif twm1 < twm2:
                return "right", two[0], two[1]

            if compare(list(leftover1[1]), list(leftover2[1])) == "TIE":
                l1 = [x[:-1] for x in h1 if x[:-1] not in leftover1[1]]
                l2 = [x[:-1] for x in h2 if x[:-1] not in leftover2[1]]
                if int(l1[0]) == int(l2[0]):
                    return "none", one[1], two[1]
                elif int(l1[0]) > int(l2[0]):
                    return "left", one[0], one[1]
                else:
                    return "right", two[0], two[1]
            elif compare(list(leftover1[1]), list(leftover2[1])) == "RIGHT":
                return "right", two[0], two[1]
            elif compare(list(leftover1[1]), list(leftover2[1])) == "LEFT":
                return "left", one[0], one[1]

        elif one[0] == "PAIR":
            sh1, sh2 = int(is_pair(h1)[1]), int(is_pair(h2)[1])
            if sh1 == sh2:

                c1 = [int(x[:-1]) for x in convert_tonums(h1) if not int(sh1) == int(x[:-1])]
                c2 = [int(x[:-1]) for x in convert_tonums(h2) if not int(sh1) == int(x[:-1])]
                if compare(c1, c2) == "TIE":
                    return "none", one[1], two[1]
                elif compare(c1, c2) == "RIGHT":
                    return "right", two[0], two[1]
                else:
                    return "left", one[0], one[1]

            elif h1 > h2:
                return "right", two[0], two[1]
            else:
                return "left", one[0], one[1]

        elif one[0] == 'FULL HOUSE':

            fh1, fh2 = int(is_fullhouse(h1)[1][0][0]), int(is_fullhouse(h2)[1][0][0])
            if fh1 > fh2:
                return "left", one[0], one[1]
            else:
                return "right", two[0], two[1]
        elif one[0] == "HIGH CARD":
            sett1, sett2 = convert_tonums(h1), convert_tonums(h2)
            sett1, sett2 = [int(x[:-1]) for x in sett1], [int(x[:-1]) for x in sett2]
            com = compare(sett1, sett2)
            if com == "TIE":
                return "none", one[1], two[1]
            elif com == "RIGHT":
                return "right", two[0], two[1]
            else:
                return "left", one[0], one[1]



        elif len(one[1]) < 5:
            if max(one[1]) == max(two[1]):
                return "none", one[1], two[1]
            elif max(one[1]) > max(two[1]):
                return "left", one[0], one[1]
            else:
                return "right", two[0], two[1]
        else:
            n_one, n_two = convert_tonums(one[1]), convert_tonums(two[1])
            n_one, n_two = [int(x[:-1]) for x in n_one], [int(x[:-1]) for x in n_two]

            if max(n_one) == max(n_two):
                return "none", one[1], two[1]
            elif max(n_one) > max(n_two):
                return "left", one[0], one[1]
            else:
                return "right", two[0], two[1]
    elif one[2] > two[2]:
        return "left", one[0], one[1]
    else:
        return "right", two[0], two[1]

def convert_toletters(h):
    letters = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    for i in range(len(h)):
        if (h[i][:2] == '10'):
            h[i] = 'T' + h[i][2]
        if(h[i][:2] == '11'):
            h[i] = 'J' + h[i][2]
        if (h[i][:2] == '12'):
            h[i] = 'Q' + h[i][2]
        if (h[i][:2] == '13'):
            h[i] = 'K' + h[i][2]
        if (h[i][:2] == '14'):
            h[i] = 'A' + h[i][2]
    return h

a = ['TS', 'JS', 'KS', 'QS', 'AS']
b = ['QD', 'KD', '9D', 'JD', 'TD']
c = ['2H', 'JS', 'JH', 'JC', 'JD']
# print(compare_hands(a, b))
# result=(compare_hands(a, b))
# print(result[2])
# biggerone=convert_toletters(result[2])
# print(biggerone)


def getwinner(a,b):
    result=(compare_hands(a, b))
    # print(result[2])
    biggerone=convert_toletters(result[2])
    return biggerone
