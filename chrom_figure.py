# -*- coding: utf-8 -*-
#!/usr/bin/env python
import matplotlib.pyplot as plt



def draw_a_figure(chrom_data,tg,sample):
    for fragment in chrom_data[tg][sample]:
        if sample == fragment:     #this is ms1
            continue
        plt.plot(chrom_data[tg][sample][fragment].rt_list,
                 chrom_data[tg][sample][fragment].i_list,label = fragment)
    plt.xlabel("retation time")
    plt.ylabel("intensity")
    plt.show()
