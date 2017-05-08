import csv
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import random
G=nx.Graph()
data=pd.read_csv("C:\Users\Shubham\Desktop\Stack API\Graphdata.csv")


#ar=[]
for line in data['Tags']:
    ar2=[]
    for value in line.split(','):
        ar2.append(value)
        
        for i in ar2:
            G.add_node(i)
            G.add_edge(value,i)
    #ar.append(ar2)

for node in G.nodes():
    n=G.degree(node)
    
    if n<6:
        G.remove_node(node)
    
d=nx.degree(G) 
colors = [(random(), random(), random()) for i in range(10)]
nx.draw_circular(G,nodelist=d.keys(),node_size=[v*200 for v in d.values()],with_labels=True,node_color=colors)
plt.show()
