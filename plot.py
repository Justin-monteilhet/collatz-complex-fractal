from typing import Tuple
from PIL import Image, ImageDraw
from time import time
import json

from progress.bar import Bar

from collatz import divergence

save = False

N_ITER = 500
DIV_LIMIT = 1e20

width, height = dim = (1000, 400)

real = (-2.5, 2.5)
im = (-1, 1)

def make_color(base:float):
    """Changes 0-1 float color to 0-255 int color"""
    return (int(255*base), int(255*base*0.5), 0)  # orange

img = Image.new('RGB', dim, (0, 0, 0))
draw = ImageDraw.Draw(img)

total_steps = width * height

prog_bar = Bar('Computing pixels', fill='█', max=total_steps, suffix = "%(percent).1f%% - %(elapsed)ds")

if save : data = []

for y in range(0, height):
    if save : data.append([])
    for x in range(0, width):
        z = complex(real[0] + (x / width) * (real[1] - real[0]),
                    im[0] + (y / height) * (im[1] - im[0]))
        
        div = divergence(z, N_ITER, DIV_LIMIT)

        if save : data[-1].append((z.real, z.imag, div))
        #color = make_color(div)
        draw.point((x, y), (int((1-div)*255),)*3)
        
        prog_bar.next()

prog_bar.finish()

if save :
    with open("points.json", "w") as f:
        json.dump(data, f)

filename = f"{real} {im} {N_ITER} iter {DIV_LIMIT} limit"
img.save(f'./images/{filename}.png', 'PNG')
img.show()