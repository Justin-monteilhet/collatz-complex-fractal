# Collatz Fractal Generator

This is a python script that allows you to draw the [Collatz Fractal](https://en.wikipedia.org/wiki/Collatz_conjecture) at the scale that you want, around any complex, and with varying precision depending on the time you want the fractal to complete.

## Installation

Download `collatz.py`, `plot.py`, and `requirements.txt`in the same folder. 
In your terminal, run :
```
pip install -r requirements.txt
```
If you know the basics of python, you are good to go. All you have to do is import the functions you want from `plot.py` and read the doc strings.

New to python ? Simply create a `.py` file in the same directory as the files you just installed, and import the functions. Then declare variables to customize your fractal, and pass them to the function. You will get an image back, and you can show/save it.
```py
from plot import make_collatz

# The center of your plot, (0, 0) if you wan it centered at the origin.
center = (-1.5, 0)

# The width of the fractal, i.e. the real values range.
# Note that the imaginary range is by default half of the real range.
rng = 2		# So here the real range will be (-2.5, -0.5)

fractal = make_collatz(center, rng)

# Show the image
fractal.show()

# Save the image
# assuming that you created a "images" folder inside of the installation directory
path = 'images/fractal.png'
fractal.save(path)
``` 

And here you are !

If you want to pass other parameters, like the number of iterations on each pixel, the divergence limit, or the image's dimension, you can pass to `make_collatz` the exact same parameters as you would with `collatz_plot`, except `im`and `re`.

## How does it work ?

The script computes the real and imaginary range of values, as well as the width and height of the image. It creates a NumPy zeros matrix of width x height, and iterates over each pixel.

For each pixel, the corresponding complex value is computed. This complex is then passed to the Collatz function extended to complex, until the number exceeds the `div_limit`, or until `iter` iterations have passed, in which case we consider that the Collatz sequence of this number is convergent. Depending on how fast the number diverges, it gets assigned a number between 0 and 1 that will represent the intensity of the pixel's color.

I implemented two features to make the image better at the end. First, every pixel's intensity is passed to an activation function so that numbers that diverge fairly quickly still stand out on the final rendering, and numbers that take a long time to diverge have the same color overall.

The second is "scaling" all the pixels so that the highest intensity is always 1, and the others are scaled depending on this. For example, when you zoom in quite far, you will only get values in a divergence range of, let's say [0 ; 0.3]. Without scaling, if the brightest pixels are 0.3, i.e. 30% of the normal color, you won't be able to see anything on the picture. To avoid this, we would multiply each value by 3.33 to get a range of [0 ; 1], which is way better.

Once the NumPy matrix is all good, we convert it to a Pillow image that is returned to you.

## Reach me on discord if any questions, ӄ.ʀǟռɖօʍ_ce#2808
