from typing import Tuple
from time import time
from pathlib import Path
import numpy as np
import json
from PIL import Image

from progress.bar import Bar

from collatz import divergence, activation

YELLOW = (255, 180, 20)

def get_current_path():
    return Path(__file__).parent.resolve()


def make_color(base: Tuple[int, int, int], level: float):
    """Changes the intensity of the base color"""
    return tuple([int(level*i) for i in base])


def collatz_plot(real: Tuple[float, float] = (-2.5, 1),
                im: Tuple[float, float] = (-1, 1),
                iter: int = 100,
                div_limit: int = int(1e10),
                dim: Tuple[int, int] = (1000, 400),
                adapt_height: bool = True,
                log: bool = False):
    """Creates an image of the complex plan, with brighter zones being the one where the collatz sequecne of the numbers converges.

    Args:
        real (Tuple[float, float], optional): Starting and ending of the real axis. Defaults to (-2.5, 1).
        im (Tuple[float, float], optional): Starting and ending of the imaginary line. Defaults to (-1, 1).
        iter (int, optional): Number of iterations to check divergence. Higher is more precise. Defaults to 100.
        div_limit (int, optional): Limit above which the sequence is considered diverging. Defaults to 1e10.
        dim (Tuple[int, int], optional): Width and height of the image. Higher means better quality. Defaults to (1000, 400).
        log (bool, optional): Logs every divergence value in a json file. Defaults to False.
    """

    width, height = dim
    im_range = im[1] - im[0]
    re_range = real[1] - real[0]

    if adapt_height:
            height = int(width * im_range / re_range)
            dim = width, height

    total_steps = width * height

    print(
        f"Computing {total_steps} pixels ({width}x{height}) with {iter} iterations and divergence limit of {div_limit:.1E}.")

    prog_bar = Bar('Computing pixels', fill='█', max=total_steps,
                   suffix="%(percent).1f%% - %(elapsed)ds")

    if log:
        data = []

    lowest_itensity = 1
    
    intensities = np.zeros((height, width))
    
    for y in range(height):
        if log:
            data.append([])     # adds a row for the new Y-line
        for x in range(width):

            # scales the complex to the screen and the real/im interval
            z = complex(real[0] + (x / width) * (real[1] - real[0]),
                        im[0] + (y / height) * (im[1] - im[0]))

            div = divergence(z, iter, div_limit)
            # scales the pixel color to how much the number diverges
            clr_lvl = activation(div)
            lowest_itensity = min(lowest_itensity, clr_lvl)

            if log:
                data[-1].append((z.real, z.imag, div))

            intensities[y][x] = clr_lvl

            prog_bar.next()

    prog_bar.finish()
    
    # Scales all the intensities so that the highest one is now 1 (useful for huge zooms)
    scaled = (intensities - lowest_itensity) / (1 - lowest_itensity)
    
    rgb = scaled.tolist()
    for i, row in enumerate(rgb) :
        for j, pixel in enumerate(row):
            rgb[i][j] = make_color(YELLOW, pixel)
    
    rgb = np.asarray(rgb)
    
    img = Image.fromarray(rgb.astype('uint8'), 'RGB')

    if log:
        with open("points.json", "w") as f:
            json.dump(data, f)

    return img


def make_collatz(center: Tuple[float, float], range_: float, *args, **kwargs):
    """Creates the collatz fractal around a center in a given range

    Args:
        center (Tuple[float, float]): Real and imaginary part of the center.
        range (Tuple[int, int]): Range of real numbers. Imaginary range is by default half of this.
    """
    
    re_range = range_   
    im_range = re_range/2
    reals = (center[0] - re_range/2, center[0] + re_range/2)
    imaginaries = (center[1] - im_range/2, center[1] + im_range/2)

    print(f"Drawing the set centered around {center} with a range of {range_} real values.")
    plot = collatz_plot(real=reals, im=imaginaries, *args, **kwargs)
    return plot
