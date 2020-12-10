import random
import matplotlib
matplotlib.use('Agg')
import numpy as np
import hickle as hkl
from matplotlib import pyplot as plt
from matplotlib import animation
from skimage import color

plt.style.use('dark_background')


def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    return patch,


def animate(t):
    global x0, x_old, v_x, y0, y_old, v_y, counter_x, counter_y
    T_x = TIMESCALE*counter_x
    T_y = TIMESCALE*counter_y
    x_old, y_old = patch.center
    x = x0 + v_x*T_x
    y = y0 + v_y*T_y - 0.5*9.81*T_y**2 
    if y - R < Y_MIN:
        v_y = bounciness*(y_old - y)/TIMESCALE
        y0 = R
        counter_y = 0
    elif y + R > Y_MAX:
        v_y = bounciness*(y_old - y)/TIMESCALE
        y0 = Y_MAX - R
        counter_y = 0
    elif x - R < X_MIN:
        v_x = bounciness*(x_old - x)/TIMESCALE
        x0 = R
        counter_x = 0
    elif x + R > X_MAX:
        v_x = bounciness*(x_old - x)/TIMESCALE
        x0 = X_MAX - R
        counter_x = 0
    else:
        counter_y += 1
        counter_x += 1

    patch.center = (x, y)

    fig.canvas.draw()
    data_rgb = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8').reshape(HEIGHT, WIDTH, 3)
    data_grey = color.rgb2gray(data_rgb).reshape(HEIGHT*WIDTH)
    data_matrix[n, t, :] = data_grey
    
    
    return patch,

NUM_TRIALS = 100
NUM_FRAMES = 60

X_MIN, X_MAX = 0, 10
Y_MIN, Y_MAX = 0, 10

WIDTH, HEIGHT = 30, 30

data_matrix = np.zeros((NUM_TRIALS, NUM_FRAMES, WIDTH*HEIGHT))

V_MAX = 10

epsilon = 0.01

for n in range(NUM_TRIALS):
    fig = plt.figure()
    fig.set_dpi(30)
    fig.set_size_inches(1, 1)



    ax = plt.axes(xlim=(X_MIN, X_MAX), ylim=(Y_MIN, Y_MAX))
    ax.set_axis_off()

    R = random.uniform(0.25, 0.75) 
    patch = plt.Circle((5, -5), R, fc='w')

    TIMESCALE = 10.0/500

    v_x = random.uniform(-V_MAX, V_MAX)
    v_y = random.uniform(-V_MAX, V_MAX)

    x0 = random.uniform(X_MIN + R + epsilon, X_MAX - R - epsilon)
    y0 = random.uniform(Y_MIN + R + epsilon, Y_MAX - R - epsilon)

    x_old = 0
    y_old = 0 

    counter_x = 0 
    counter_y = 0 

    bounciness = random.uniform(0.7, 1)
    anim = animation.FuncAnimation(fig, animate, 
                                init_func=init, 
                                frames=NUM_FRAMES, 
                                interval=20,
                                blit=True)
    anim.save(f"fball_train_{n}.mp4")

hkl.dump(data_matrix, 'fball_training.hkl', mode='w', compression='gzip')