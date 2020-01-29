# 字典 应用
# from pprint import pprint

# 井字棋
theBoard = {'top_L': 'X', 'top_M': ' ', 'top_R': 'O',
            'mid_L': ' ', 'mid_M': 'X', 'mid_R': ' ',
            'low_L': ' ', 'low_M': 'O', 'low_R': ' '}


def printBoard(board):
    print(board['top_L']+'|'+board['top_M']+'|'+board['top_R'])
    print('-+-+-')
    print(board['mid_L']+'|'+board['mid_M']+'|'+board['mid_R'])
    print('-+-+-')
    print(board['low_L']+'|'+board['low_M']+'|'+board['low_R'])


# printBoard(theBoard)
# pprint(theBoard)

# 字典嵌套
allGuests = {'Alice': {'apples': 5, 'pretzels': 12},
             'Bob': {'ham sandwiches': 3, 'apples': 2},
             'Carol': {'cups': 3, 'apple pies': 1}}
# pprint(allGuests)
# print('--------------------------------------')
# for i, j in allGuests.items():
#     print(j)
# print('i:', type(i))
# print('j:', type(j))


def broCnt(guests):
    cnt = {}
    for i in allGuests.values():
        for k, v in i.items():
            cnt.setdefault(k, 0)
            cnt[k] += v
    return cnt


def broChk(allItem, item):
    cnt = allItem.get(item, 0)
    return cnt


cnt = broCnt(allGuests)

print('Number of things being brought:')
print(' - Apples '+str(broChk(cnt, 'apples')))
print(' - Cups '+str(broChk(cnt, 'cups')))
print(' - Cakes '+str(broChk(cnt, 'cakes')))
print(' - Ham Sandwiches '+str(broChk(cnt, 'ham sandwiches')))
print(' - Apple Pies '+str(broChk(cnt, 'apple pies')))
