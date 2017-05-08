import plotly.plotly as py
import plotly.graph_objs as go
import random
import squarify
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv


data = pd.read_csv("C:\Users\Shubham\Desktop\Stack API\userData.csv")
#print data.shape
repu=np.array(data['Reputation'])
loc=np.array(data['Location'])

x = 0.
y = 0.
width = 700.
height = 700.

normed = squarify.normalize_sizes(repu, width, height)
rects = squarify.squarify(normed, x, y, width, height)

color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
                'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)',
                'rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)',
                'rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']
shapes = []
annotations = []
counter = 0

for r in rects:
    shapes.append( 
        dict(
            type = 'rect', 
            x0 = r['x'], 
            y0 = r['y'], 
            x1 = r['x']+r['dx'], 
            y1 = r['y']+r['dy'],
            line = dict( width = 2 ),
            fillcolor = color_brewer[counter]
        ) 
    )
    annotations.append(
        dict(
            x = r['x']+(r['dx']/2),
            y = r['y']+(r['dy']/2),
            text = loc[counter],
            showarrow = False
        )
    )
    counter = counter + 1
    if counter >= len(color_brewer):
        counter = 0

# For hover text
trace0 = go.Scatter(
    x = [ r['x']+(r['dx']/2) for r in rects ], 
    y = [ r['y']+(r['dy']/2) for r in rects ],
    text = [ str(v) for v in loc ], 
    mode = 'text',
)
        
layout = dict(
    height=700, 
    width=700,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    shapes=shapes,
    annotations=annotations,
    hovermode='closest'
)

# With hovertext
figure = dict(data=[trace0], layout=layout)
py.iplot(figure, filename='squarify-treemap')
