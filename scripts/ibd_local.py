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

#create a high ibd 
df_high_ibd = df[df["fract_sites_IBD"] > 0.5]

#load metadata
metadata= pd.read_csv("")

#merge the metadata
merged_data = df_high_ibd.merge(metadata, left_on="sample1", right_on="sample", how="left")
merged_data = merged_data.merge(metadata, left_on="sample2", right_on="sample", how="left", >
merged_data=merged_data.drop(columns=["sample_sample1","sample_sample2"])
merged_data.head()

# Create a graph
G = nx.Graph()

# Define the color map (using a list of distinct colors)
cmap = plt.cm.get_cmap("tab20")  # You can choose other color maps like "tab10", "Set1", etc.

# Create a dictionary to map population names to color indices
populations = pd.concat([merged_data['location_sample1'], merged_data['location_sample2']]).unique()
population_to_color = {pop: cmap(i / len(populations)) for i, pop in enumerate(populations)}

# Add edges based on 'fract_sites_IBD'
for _, row in merged_data.iterrows():
    if row["fract_sites_IBD"] > 0.8:
        G.add_edge(row["sample1"], row["sample2"], weight=row["fract_sites_IBD"])

# Define a node color map based on Population (Population_sample1 or Population_sample2)
node_colors = []
for node in G.nodes():
    # Check if the node exists in sample1 or sample2
    population_sample1 = merged_data.loc[merged_data['sample1'] == node, 'location_sample1']
    population_sample2 = merged_data.loc[merged_data['sample2'] == node, 'location_sample2']
    
    if len(population_sample1) > 0:
        node_color = population_to_color[population_sample1.values[0]]
    elif len(population_sample2) > 0:
        node_color = population_to_color[population_sample2.values[0]]
    else:
        # In case the node is not found in either column, we can assign a default color (gray)
        node_color = (0.5, 0.5, 0.5)  # Default gray color
    
    node_colors.append(node_color)

# Draw the graph with nodes colored by population and edges kept as is
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_size=500, edge_color="grey", node_color=node_colors, font_size=10)

# Create a custom legend based on population_to_color mapping
# We create a dummy scatter plot to associate colors with the population names
import matplotlib.lines as mlines

# Create a list of legend labels and corresponding colors
legend_labels = list(population_to_color.keys())
legend_colors = list(population_to_color.values())

# Create the legend
handles = [mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_colors]
plt.legend(handles=handles, labels=legend_labels, title="Population", loc="best")

# Title and save the figure
plt.title("IBD Network Graph, >= 0.8")
plt.savefig("$result/ibd_network_location.png")
