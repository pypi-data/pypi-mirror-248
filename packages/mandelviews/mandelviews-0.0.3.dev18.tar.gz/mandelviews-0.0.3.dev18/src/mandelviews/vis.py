"""
vis.py

mandelviews visualization functions 

Plot mandelbrot image in matplotlib, and overlay rectangle.
"""
#%%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import colors
from matplotlib.colors import Colormap  # for type hinting
import numpy as np
from numpy.typing import ArrayLike
import time
from typing import Any


def display_mandelimage_mpl(image: np.ndarray, 
                            x_range: ArrayLike, 
                            y_range: ArrayLike, 
                            cmap: Colormap ='magma',
                            ax: plt.Axes = None,
                            show_axis: bool = True):
    """Display image of mandelbrot set using matplotlib
    
    Parameters
    ----------
    image: np.ndarray
        2d array containing the image of the mandelbrot set
    x_range, y_range: ArrayLike
        length two lists/arrays of x and y range limits [xmin, xmax] for the mandelbrot plots 
        Used to get set axis limits for the plot.
    cmap: Colormap
        Colormap to use (default 'magma', but 'Purples' looks cool)
    ax: matplotlib axes object
        Axes object to plot on, default is None which creates a new plot
    show_axis: bool
        show or hide axis labels and ticks, default True. 
        Showing them is useful when looking for new area to zoom.

    Returns
    -------
    ax: mpl axes object

    Notes
    -----
    Code adapted from https://github.com/NIH-HPC/python-in-hpc    
    """
    norm = colors.PowerNorm(0.3)
    if ax is None:
        f, ax = plt.subplots(figsize=(6,6), dpi=72)
    ax_extent = [x_range[0], x_range[1], y_range[0], y_range[1]]
    ax.imshow(image, cmap=cmap, origin='lower', norm=norm, extent=ax_extent)
    if not show_axis:
        ax.set_axis_off()

    return ax


def draw_rect(rect_coords, 
              color: Any ='white', 
              line_width: float = 0.5, 
              ax: plt.Axes = None):
    """Draw a single unfilled rectangle on given axes object.

    Helper function to plot on mandelbrot image to find interesting regions to zoom in on.
    
    Parameters
    ----------
        rect_coords: array-like
            Standard bounding-box format: [rect_xmin, rect_ymin, rect_xmax, rect_ymax] 
        color: matplotlib color
            string or rgb for color of the line
        line_width : float
            width of the line for rectangle
        ax : pyplot.Axes object 
            axes object upon which rectangle will be drawn, default None
    
    Returns
    -------
        ax: pyplot.Axes object
        rect: matplotlib Rectangle object
    """   
    if ax is None:
        f, ax = plt.subplots()
        
    rect_origin = (rect_coords[0], rect_coords[1])
    rect_height = rect_coords[3] - rect_coords[1] 
    rect_width = rect_coords[2] - rect_coords[0]

    rect = Rectangle(rect_origin, 
                     width=rect_width, 
                     height=rect_height,
                     color=color, 
                     alpha=1,
                     fill=None,
                     linewidth=line_width)
    ax.add_patch(rect)

    return ax, rect

#%%
if __name__ == '__main__':

    #%% CALCULATE using core functions
    from mandelviews import create_mandelimage_py

    print("Pure python extraction no zoom")
    start_time_py0 = time.time()
    mandelimage_py0 = create_mandelimage_py(num_x=250, num_y=250)
    run_time_py0 = time.time() - start_time_py0
    print(f"\tRun time {run_time_py0:0.2f} seconds: {run_time_py0/60:0.2f} minutes")

    print("Pure python extraction zoom level 1")
    rect1_xmin = -0.68
    rect1_ymin = 0.46
    rect1_xmax = -0.38
    rect1_ymax = 0.76
    start_time_py1 = time.time()
    mandelimage_py1 = create_mandelimage_py(xmin=rect1_xmin, 
                                                  xmax=rect1_xmax,
                                                  ymin=rect1_ymin, 
                                                  ymax=rect1_ymax,
                                                  num_x=500,
                                                  num_y=500,
                                                  maxiters=500)
    run_time_py1 = time.time() - start_time_py1
    print(f"\tRun time {run_time_py1:0.2f} seconds: {run_time_py1/60:0.2f} minutes")
    
    print("Pure python extraction zoom level 2")
    rect2_xmin = -0.575
    rect2_xmax = -0.550
    rect2_ymin = 0.631
    rect2_ymax = 0.656
    start_time_py2 = time.time()
    mandelimage_py2 = create_mandelimage_py(xmin=rect2_xmin, 
                                            xmax=rect2_xmax,
                                            ymin=rect2_ymin, 
                                            ymax=rect2_ymax,
                                            num_x=1000,
                                            num_y=1000,
                                            maxiters=500)
    run_time_py2 = time.time() - start_time_py2
    print(f"\tRun time {run_time_py2:0.2f} seconds: {run_time_py2/60:0.2f} minutes")

    
    #%%  VISUALIZE results of pure python computations
    print("Plot using mpl")
    rect1_coords = [rect1_xmin, rect1_ymin, rect1_xmax, rect1_ymax]  
    rect2_coords = [rect2_xmin, rect2_ymin, rect2_xmax, rect2_ymax]
    cmap = 'Purples'

    f, (ax0, ax1, ax2) = plt.subplots(1,3, figsize=(16, 6), dpi=72)

    ax0 = display_mandelimage_mpl(mandelimage_py0, 
                                    x_range=[-2, 0.5], 
                                    y_range=[-1.25, 1.25], 
                                    cmap=cmap,
                                    ax=ax0,
                                    show_axis=False)
 
    ax1 = display_mandelimage_mpl(mandelimage_py1, 
                                    x_range=[rect1_xmin, rect1_xmax], 
                                    y_range=[rect1_ymin, rect1_ymax], 
                                    cmap=cmap,
                                    ax=ax1,
                                    show_axis=False)

    ax2 = display_mandelimage_mpl(mandelimage_py2, 
                                  x_range=[rect2_xmin, rect2_xmax],
                                  y_range=[rect2_ymin, rect2_ymax], 
                                  cmap=cmap, 
                                  ax=ax2,
                                  show_axis=False)

    draw_rect(rect1_coords, color='red', ax=ax0, line_width=2)
    draw_rect(rect2_coords, color='lime', ax=ax0, line_width=1)
    draw_rect(rect2_coords, color='lime', ax=ax1, line_width=2)

    ax0.set_title("Full Mandelbrot", fontsize=16)
    ax1.set_title("Red Inset", fontsize=16)
    ax2.set_title("Green Inset", fontsize=16)

    plt.tight_layout();
    plt.show();
    

# %%
