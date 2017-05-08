import numpy as np
import matplotlib.pyplot as pp
import csv
from sklearn.cluster import KMeans
import random
import pandas as pd
from matplotlib import pyplot as plt
val = 0. 
data = pd.read_csv("C:\Users\Shubham\Desktop\SA_Graph\userData.csv")
#print data.shape
data['repu']=data['Reputation']
data=data.repu.reshape(-1, 1) 

def initial(points):
    k_means = KMeans(n_clusters=3, init='random')
    KMEANS=k_means.fit(points)
    k=KMEANS.cluster_centers_
    return k



k=initial(data)

cluster_centers = {
    0: {
        'center': k[0],
        'pts': []
    },
    1: {
        'center': k[1],
        'pts': []
    },
    2: {
        'center': k[2],
        'pts': []
    }
}
   

def dist(x1, x2):
    
    diff = (x1 - x2)
    diff_sq = diff**2
    sum_diff = diff_sq.sum()
    return np.sqrt(sum_diff)


#print len(points)
#print data.size
comp_dist=[]
for ix in range(len(data)):
    distances=[]
    for cx in cluster_centers.keys():
        comp_dist = dist(cluster_centers[cx]['center'], data[ix, :])
        distances.append([comp_dist, cx])
    best_dist = sorted(distances)[0]
    best_center = cluster_centers[best_dist[1]]
    cluster_centers[best_dist[1]]['pts'].append(data[ix])

cols = ['red', 'green', 'blue']
plt.figure(0)
for cx in cluster_centers.keys():
    if not len(cluster_centers[cx]['pts'])==0:
        points = np.asarray(cluster_centers[cx]['pts'])
        new_center = points.mean(axis=0)
        plt.scatter(points[:, 0.5], points[:, 0], color=cols[cx])
        cluster_centers[cx]['pts'] = []
        cluster_centers[cx]['center'] = new_center
    else:
        pass

plt.show()
