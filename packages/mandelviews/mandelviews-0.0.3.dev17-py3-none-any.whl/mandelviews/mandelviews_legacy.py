"""
mandelviews.py

Implement core functions in mandelviews package

Functions for calculating mandelbrot set.
Functions for viewing mandelbrot set.

Code adapted from multiple sources: 
https://github.com/NIH-HPC/python-in-hpc
https://holoviews.org/gallery/apps/bokeh/mandelbrot.html
https://numba.pydata.org/numba-doc/0.21.0/user/examples.html
"""

#%% imports and function definitions  
# %matplotlib qt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import colors
from matplotlib.colors import Colormap  # for type hinting
import numpy as np
import time
from typing import Callable, Any
from numpy.typing import ArrayLike

#######################
# Calculation back-end
#######################
def mandelbrot_py(creal: float, 
                  cimag: float, 
                  maxiters: int) -> int:
    """Determine if complex number is in mandelbrot set using pure python. 

    Given the real and imaginary parts of a complex number use the escape time
    algorithm to determine if it is a candidate for membership in the Mandelbrot
    Set -- go through max iterations to determine if it diverges. 

    Parameters
    ----------
    creal: float
        Real part of the complex number
    cimag: float
        Imaginary part of the complex number
    maxiter: int
        number of iterations to go check divergence: determines accuracy

    Returns
    -------
    n: int
        How many iterations to diverge (scaled from 0 to 255), if not divergent, returns 255.
    """
    real = creal
    imag = cimag
    for n in range(maxiters):
        real2 = real*real
        imag2 = imag*imag
        if real2 + imag2 >= 4.0:
            # print(f"{n} steps to diverge")
            return (255 * n) // maxiters
        imag = 2 * real*imag + cimag
        real = real2 - imag2 + creal      
    return 255  


def create_mandelimage_py(xmin: float = -2.0, 
                          xmax: float = 0.5, 
                          ymin: float = -1.25, 
                          ymax: float = 1.25, 
                          num_x: int = 1000, 
                          num_y: int = 1000, 
                          maxiters: int = 80) -> np.ndarray:
    """ Generate mandelbrot image given bounds/iterations using pure python.

    Given appropritae bounds, maxiters, and number of points between bounds, 
    generate the 2d image showing which values diverged and didn't. Uses the
    the pure python function mandelbrot_py. This will be very slow if you have lots of
    iterations. 

    Parameters
    ----------
    xmin, xmax: float
        min and max values (inclusive) for x to plot 
        these will be real values fed into mandelbrot set calculator
    ymin, ymax: float
        min/max values for y to plot (inclusive)  
        these will be imaginary values fed into mandelbrot set calculator
    num_x, num_y: int
        number of x and y values to include in the image array
        determines resolution of the mandelbrot view
    maxiters: int
        number of iterations check for convergence: determines accuracy

    Returns
    -------
    image: np.ndarray
        2d array containing the image of the mandelbrot set (num_y, num_x dims)

    """
    real_vals = np.linspace(xmin, xmax, num_x)
    imag_vals = np.linspace(ymin, ymax, num_y)
    image = np.empty((num_y, num_x), dtype=np.int32)
    for x in range(num_x):
        for y in range(num_y):
            image[y, x] = mandelbrot_py(real_vals[x], 
                                        imag_vals[y], 
                                        maxiters)
    return image


#########################
# Visualization functions
##########################
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
        show or hide axis labels and ticks. 
        Showing them is useful when looking for new area to zoom.

    Returns
    -------
    ax: mpl axes object
    
    """
    norm = colors.PowerNorm(0.3)
    if ax is None:
        fig, ax = plt.subplots(figsize=(6,6), dpi=120)
    ax_extent = [x_range[0], x_range[1], y_range[0], y_range[1]]
    ax.imshow(image, cmap=cmap, origin='lower', norm=norm, extent=ax_extent)
    if not show_axis:
        ax.set_axis_off()
    plt.show()

    return ax


def draw_rect(rect_coords, 
              color: Any ='white', 
              line_width: float = 0.5, 
              ax: plt.Axes = None):
    """Draw a single unfilled rectangle on given axes object.

    Used to plot on mandelbrot image to find interesting regions to zoom in on.
    
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


print('functions defined')


#%%
if __name__ == '__main__':
    #%% CALCULATE using core functions
    print("Pure python extraction no zoom")
    start_time_py0 = time.time()
    mandelimage_py0 = create_mandelimage_py()
    run_time_py0 = time.time() - start_time_py0
    print(f"\tRun time {run_time_py0} seconds: {run_time_py0/60:0.2f} minutes")

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
                                                  num_x=1000,
                                                  num_y=1000,
                                                  maxiters=500)
    run_time_py1 = time.time() - start_time_py1
    print(f"\tRun time {run_time_py1} seconds: {run_time_py1/60:0.2f} minutes")

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
                                            num_x=2000,
                                            num_y=2000,
                                            maxiters=1000)
    run_time_py2 = time.time() - start_time_py2
    print(f"\tRun time {run_time_py2} seconds: {run_time_py2/60:0.2f} minutes")

    
    #%%  VISUALIZE results of pure python computations
    rect1_coords = [rect1_xmin, rect1_ymin, rect1_xmax, rect1_ymax]  
    rect2_coords = [rect2_xmin, rect2_ymin, rect2_xmax, rect2_ymax]
    cmap = 'Purples'

    f, (ax0, ax1, ax2) = plt.subplots(1,3, figsize=(20, 6), dpi=72)

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


# %%
