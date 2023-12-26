"""
mandelviews_core.py

Implement core back-end functions in mandelviews package

Calculate whether a complex number is in the mandelbrot set, and 
calculate the same for an entire array generating an image.

Code adapted from multiple sources: 
https://github.com/NIH-HPC/python-in-hpc
https://holoviews.org/gallery/apps/bokeh/mandelbrot.html
https://numba.pydata.org/numba-doc/0.21.0/user/examples.html
"""

#%% imports and function definitions  

import numpy as np
import time


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
    generate the 2d image showing which regions are in the Mandelbrot set. Uses the
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




#%%
if __name__ == '__main__':
    #%% CALCULATE using core functions
    print("Pure python extraction no zoom")
    start_time_py0 = time.time()
         
    run_time_py0 = time.time() - start_time_py0
    print(f"\tRun time {run_time_py0} seconds: {run_time_py0/60:0.2f} minutes")