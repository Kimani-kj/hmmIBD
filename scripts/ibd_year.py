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
merged_data = merged_data.merge(metadata, left_on="sample2", right_on="sample", how="left", suffixes=("_sample1", "_sample2"))
merged_data=merged_data.drop(columns=["sample_sample1","sample_sample2"])
merged_data.head()

#ploting  ibd graph
# Create a Graph
G = nx.Graph()

# Define a color map (using viridis, but you can change this)
cmap = plt.cm.get_cmap('viridis')  # Choose a color map (e.g., 'viridis', 'plasma', etc.)
norm_sample1 = mcolors.Normalize(vmin=merged_data['sample_year_sample1'].min(), vmax=merged_data['sample_year_sample1'].max())

# Loop through the merged data to add edges
for _, row in merged_data.iterrows():
    if row["fract_sites_IBD"] > 0.9:
        # Add edge between sample1 and sample2 with weight based on 'fract_sites_IBD'
        G.add_edge(row["sample1"], row["sample2"], weight=row["fract_sites_IBD"])

# Now, we will color the nodes based on their respective year_of_collection
node_colors = []
for node in G.nodes():
    # Find the row corresponding to this node (either sample1 or sample2)
    node_data_sample1 = merged_data[merged_data['sample1'] == node]
    node_data_sample2 = merged_data[merged_data['sample2'] == node]
    
    # Get the corresponding year for coloring the node (sample1 or sample2)
    if not node_data_sample1.empty:
        year = node_data_sample1['sample_year_sample1'].values[0]
    else:
        year = node_data_sample2['sample_year_sample2'].values[0]

    # Normalize the year and map to a color
    node_color = cmap(norm_sample1(year))
    node_colors.append(node_color)

# To visualize the graph with the colored nodes
fig, ax = plt.subplots(figsize=(12, 12))  # Create a figure and axis for plotting
pos = nx.spring_layout(G)  # Layout for the nodes

# Draw the graph with nodes colored based on the 'year_of_collection_sample1'
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', width=2, font_size=10, ax=ax)

# Add edge labels (weights)
#edge_labels = nx.get_edge_attributes(G, 'weight')  # Get the weights from the edges
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

# Create a color bar (legend) for the node colors
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_sample1)
sm.set_array([])  # Empty array for the color bar
cbar = plt.colorbar(sm, ax=ax)  # Add the colorbar to the existing axis
cbar.set_label('Year of Collection')  # Label for the color bar
cbar.set_ticks([merged_data['sample_year_sample1'].min(), merged_data['sample_year_sample1'].max()])
cbar.ax.invert_yaxis()  # Invert the color bar if necessary (optional)

# Show the plot

plt.title("IBD Network Graph, >= 0.9")
plt.savefig("$results/yearNode.png")
