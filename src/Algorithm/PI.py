# -*- coding: utf-8 -*-
# 蒙特卡洛法求pie
# © 2025~2026 wilber-20130410
from random import random

n = 100000 #求pie的精度值，越大越高,但不宜过高(如果你的电脑配置很好，当我没说)

def xy_rang(n):
    m = 0
    for i in range(1, n + 1):
        x = random() * 2 - 1
        y = random() * 2 - 1
        if x**2 + y**2 < 1:
            m += 1
    return m

c1 = xy_rang(n)
print('总实验次数是 %d ,计算的圆周率是 %f' % (n, 4 * c1 / n))
