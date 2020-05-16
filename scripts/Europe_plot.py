#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly
import plotly.offline as offline


# In[2]:


df_sweden = pd.read_csv('../data/similar_country_absolute_cases.csv', index_col=0)


# In[3]:


data_slider = []

scl = [[0.0, '#ffffff'],[0.2, '#ff9999'],[0.4, '#ff4d4d'],        [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']] # reds

for date in df_sweden["Date"].unique():
    
    region_one_date = df_sweden[df_sweden["Date"] == date].drop(["Date"], axis = 1)
    
    new_df = pd.DataFrame({"country": region_one_date["Country/Region"].tolist(),
                           "infected": region_one_date["Number of cases"].tolist()})
    
    data_one_date = dict(
                        type='choropleth',
                        colorscale = scl, 
                        locations = new_df["country"], 
                        locationmode = 'country names',
                        z=new_df["infected"],
                        text = new_df["country"],
                        zmin = 0,
                        zmax = 25000,
        
                        marker = dict(     # for the lines separating states
                        line = dict (color = 'rgb(0,0,0)', width = 0.5) ),
                        
                        colorbar = dict(title = "Number of infected people in a given day") 
                        )

    data_slider.append(data_one_date)  # I add the dictionary to the list of dictionaries for the slider


# In[4]:


steps = []

for i in range(len(data_slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)],
                label= "Date: {}".format(df_sweden["Date"].unique()[i]))
    step['args'][1][i] = True
    steps.append(step)


##  I create the 'sliders' object from the 'steps' 

sliders = [dict(active=0, pad={"t": 1}, steps=steps, ticklen = 10, len = 750, lenmode = 'pixels')]


# In[5]:


layout = dict(
    title = None,
    width = 580, 
    height = 500, 
    hovermode = "closest",
    geo=dict(
        scope='europe',
        showlakes = True, 
        lakecolor = 'rgb(73, 216, 230)',
        lataxis = {"range": [55.0, 85.0]}, 
        lonaxis = {"range": [-1, 40.0]}, 
        showland = False
    ),
    sliders=sliders,
    margin=dict(l=50, r=0, t=0, b=100)
)


# In[6]:


fig = dict(data=data_slider, layout=layout) 

# to plot in the notebook

plotly.offline.iplot(fig)


# In[7]:


offline.plot(fig, auto_open=False, image_width=580, image_height=500, 
              filename='../figures_html/scandinavia_covid.html', validate=True)


# In[ ]:





# In[ ]:




