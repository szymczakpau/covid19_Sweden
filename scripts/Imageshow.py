#!/usr/bin/env python
# coding: utf-8

# In[1]:


# """
# import pandas as pd
# import matplotlib.image as mpimg
# import plotly.graph_objects as go

# #img=mpimg.imread('../images/image_{}.jpg'.format(0))
# fig = go.Figure()

# #img_width = 1000
# #img_height = 1000
# #scale_factor = 1

# #fig.add_trace(go.Image(z = img))

# # Configure axes
# fig.update_xaxes(
#     visible=False,
#     #range=[0, img_width * scale_factor]
# )

# fig.update_yaxes(
#     visible=False,
#     #range=[0, img_height * scale_factor],
#     # the scaleanchor attribute ensures that the aspect ratio stays constant
#     #scaleanchor="x",
#     autorange = 'reversed'
# )              
              

# def plot_images():
              
#     for j in range(3):
#         img=mpimg.imread('../images/image_{}.jpg'.format(j))

#         fig.add_trace(
#                 go.Image(
#                     visible = False,
#                     z = img))
            
# plot_images()

# # Create and add slider

# def generate_story():
#     steps = []
#     for i in range(3):
#         step = dict(
#             method="update",
#             args=[{"visible": [False] * len(fig.data)}],
#         )
#         step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
#         steps.append(step)

#     sliders = [dict(
#         active=0,
#         currentvalue={"prefix": "Slide: "},
#         pad={"t": 20},
#         steps=steps
#     )]

#     fig.update_layout(
#         autosize=False,
#         width=500,
#         height=500,
#         sliders=sliders,
#         template ="plotly_white"
#     )

#     fig.write_html('../figures_html/story.html')

# generate_story()
# """


# In[6]:


import pandas as pd
import matplotlib.image as mpimg
import matplotlib.animation 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'


# In[7]:


def show_image(i):
    img = mpimg.imread('../images/image_{}.jpg'.format(i))
    #plt.figure(figsize = (20,2))
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    plt.figsize = (10,6)
    plt.tight_layout()


# In[8]:


fig, ax = plt.subplots(figsize=(10,8))
animator = FuncAnimation(fig, show_image, frames=range(0,23))

# animator.save(filename = '../figures_html/story.gif', writer='imagemagick', fps=0.5)
FFwriter = matplotlib.animation.FFMpegWriter(fps=0.5)
animator.save('../figures_html/story.mp4', writer = FFwriter, dpi=100)

animator.to_jshtml(fps=0.5)
plt.close()


# In[5]:


ts = animator.to_jshtml(fps=0.5)


# In[ ]:




