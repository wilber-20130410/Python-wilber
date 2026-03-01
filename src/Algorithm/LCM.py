# -*- coding: utf-8 -*-
# 求两个整数的最小公倍数
# © 2025~2026 wilber-20130410

def T1(x, y):
    increat = 0
    if x > y:
        increat = x
    elif x < y:
        increat = y
    else:
        return x
    while increat:
        if increat % x == 0 and increat % y == 0:
            return increat
        else:
            increat += 1

try:
    n1 = int(input("请输入第一个整数："))
    n2 = int(input("请输入第二个整数："))
    if n1 <= 0 or n2 <= 0:
        print("输入的整数应该大于0")
    else:
        print("%d和%d的最小公倍数是%d" % (n1, n2, T1(n1, n2)))
except:
    print("输入的整数错误！")