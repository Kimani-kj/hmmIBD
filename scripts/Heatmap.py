#!/usr/bin/env python3

#load libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import igraph as ig
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors

#load the data
path=
result=
df = pd.read_csv("$path/kilifi_hap.hmm_fract.txt", delim_whitespace=True,)

#heatmap
ibd_matrix = df.pivot(index="sample1", columns="sample2", values="fract_sites_IBD").fillna(0)
plt.figure(figsize=(10, 8))
sns.heatmap(ibd_matrix, cmap="coolwarm", annot=False)
plt.title("IBD Fraction Heatmap")
plt.savefig("$result/ibd_heatmap.png")
