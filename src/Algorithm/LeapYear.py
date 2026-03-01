# -*- coding: utf-8 -*-
# # 求闰年
# © 2025~2026 wilber-20130410

def RunYear(y):
    if y % 4 == 0 and y % 100 != 0:
        return 1
    elif y % 400 == 0:
        return 1
    else:
        return 0
    
try:
    year = int(input("请输入一个年份："))
    if year >= 0:
        r1 = RunYear(year)
        if r1:
            print("%d是闰年" % (year))
        else:
            print("%d不是闰年" % (year))
    else:
        print("输入的年份错误！")
except:
    print("输入的年份错误！")