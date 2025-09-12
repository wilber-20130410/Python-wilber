#抽纸牌
import random

#传统算法
Poker = ['黑A','黑2','黑3','黑4','黑5','黑6','黑7','黑8','黑9','黑10',
         '黑J','黑Q','黑K','红A','红2','红3','红4','红5','红6','红7',
         '红8','红9','红10','红J','红Q','红K','梅A','梅2','梅3','梅4',
         '梅5','梅6','梅7','梅8','梅9','梅10','梅J','梅Q','梅K','方A',
         '方2','方3','方4','方5','方6','方7','方8','方9','方10','方J',
         '方Q','方K','大王','小王']
print('一副牌有%d张'% (len(Poker)))
Show = random.sample(Poker, 5)
print(Show)

#高效空间利用率算法
'''
规则:1-13:黑A-黑K,14-26:红A-红K,27-39:梅A-梅K,40-52:方A-方K,小王53,大王54
'''
shape = ['J','Q','K','大王','小王']
Show1 = []
Show2 = []

def getCards(name, r, Show2, shape):
    if r == 1:
        Show2.append(name + 'A')
    elif r <= 10:
        Show2.append(name + str(r))
    else:
        Show2.append(name + shape[r - 11])

for x in range(5):
    y = random.randint(1, 54)
    Show1.append(y)
for r in Show1:
    if r <= 13:
        getCards('黑', r, Show2, shape)
    elif r > 13 and r <= 26:
        getCards('红', r - 13, Show2, shape)
    elif r > 27 and r <= 39:
        getCards('梅', r - 26, Show2, shape)
    elif r > 40 and r <= 52:
        getCards('方', r - 39, Show2, shape)
    else:
        Show2.append(shape[r % 50])
print(Show2)