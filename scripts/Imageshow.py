import matplotlib.image as mpimg
import matplotlib.animation 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

def show_image(i):
    img = mpimg.imread('../images/image_{}.jpg'.format(i))
    #plt.figure(figsize = (20,2))
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    plt.figsize = (10,6)
    plt.tight_layout()


fig, ax = plt.subplots(figsize=(10,8))
animator = FuncAnimation(fig, show_image, frames=range(0,23))

FFwriter = matplotlib.animation.FFMpegWriter(fps=0.5)
animator.save('../figures_html/story.mp4', writer = FFwriter, dpi=100)

animator.to_jshtml(fps=0.5)
plt.close()




