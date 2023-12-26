"""
Packaging for mandelviews
"""
from .version import __version__

from .core import mandelbrot_py
from .core import create_mandelimage_py

from .vis import display_mandelimage_mpl
from .vis import draw_rect
