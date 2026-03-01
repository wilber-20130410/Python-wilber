# -*- coding: utf-8 -*-
# 求三维空间内任意三点连接而成的图形的面积
# © 2025~2026 wilber-20130410

import numpy as np

A = np.array([1, 1, 1])
B = np.array([3, 1.5, 1.5])
C = np.array([4, 2, 2])
Dab = np.sqrt(np.sum((A -B) ** 2))
Dac = np.sqrt(np.sum((A -C) ** 2))
Dbc = np.sqrt(np.sum((B -C) ** 2))
print("AB的长度为：" , Dab)
print("AC的长度为：" , Dac)
print("BC的长度为：" , Dbc)
s = (Dab + Dac + Dbc) / 2
area = np.sqrt(s * (s - Dab) * (s - Dac) * (s - Dbc))
print("该任意图形的面积为：%.2f" % (area))