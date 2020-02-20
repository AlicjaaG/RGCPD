# %load_ext autoreload
# %autoreload 2
import os, inspect, sys
import PyQt5
main_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
RGCPD_func = os.path.join(main_dir, 'RGCPD')
cluster_func = os.path.join(main_dir, 'clustering')
if RGCPD_func not in sys.path:
    sys.path.append(RGCPD_func)
    sys.path.append(cluster_func)


import clustering_spatial as cl
from RGCPD import RGCPD
import plot_maps

import matplotlib.pyplot as plt

rg = RGCPD()
plt.show()




rg.pp_precursors()




rg.list_precur_pp




var_filename = rg.list_precur_pp[0][1]
mask = [145.0, 230.0, 20.0, 50.0]
for q in [85, 95]:
    xrclustered, results = cl.dendogram_clustering(var_filename, mask=mask, q=q, kwrgs={'n_clusters':3})
    plot_maps.plot_corr_maps(xrclustered)
    plt.show()