# encoding: utf-8, division
from __future__ import print_function, division

import os
import pylab as plt
import numpy as np

# plots in y direction:
K_max = 16
K_min = 0

# plots in x direction:
L_max = 16
L_min = 0

ax = plt.subplot(111)
x_offset = 10 # tune these
y_offset = 10 # tune these
plt.setp(ax, 'frame_on', False)
ax.set_ylim([0, (K_max-K_min +1)*y_offset ])
ax.set_xlim([0, (L_max - L_min+1)*x_offset])
ax.set_xticks([])
ax.set_yticks([])
ax.grid('off')



for k in np.arange(K_min, K_max + 1):
    for l in np.arange(L_min, L_max + 1):

        x_values = np.arange(5)
        y_values = 5 + np.random.rand(5)

        # "r" is red:
        ax.plot(x_values + l*x_offset, y_values + k*y_offset, 'r-o', ms=1, mew=0, mfc='r')

        x_values = np.arange(5)
        y_values = 3 + np.random.rand(5)

        # "b" is blue:
        ax.plot(x_values + l*x_offset, y_values + k*y_offset, 'b-o', ms=1, mew=0, mfc='b')

        # put some text:
        title = "K=%d, L=%d" % (k, l)
        ax.annotate(title, (2.5 + k * x_offset, l * y_offset), size=10, ha='center')

plt.savefig(os.path.join(os.getcwd(), 'plot-average.pdf'))
print("show")
plt.show()
