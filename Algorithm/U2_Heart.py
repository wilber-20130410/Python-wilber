#笛卡尔心形

import matplotlib.pyplot as plt #pip install matplotlib
import numpy as np #pip install numpy

x = np.linspace(0, 2 * np.pi, 500)
a = 6
rho = a * (1 - np.sin(x))
plt.subplot(polar = True)
plt.plot(x, rho, c = 'r')
plt.text(0, 0, 'Love You!',color = 'm')
plt.show()