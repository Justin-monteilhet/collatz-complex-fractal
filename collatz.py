from typing import Union
from decimal import Decimal
from cmath import sin, cos
from math import pi, exp


def activation(x:float) -> float:
    """Takes a 0-1 input and returns a 0-1 output so that values near 0 are now more spread, and higer values are closer."""
    return 1-exp(-5*x)

def cltz(z:complex) -> complex | None:
    """Complex function to iterate in order to get Collatz sequence complex extension."""
    
    try : 
        return (sin(z*pi/2)**2)*(3*z+1) + (cos(z*pi/2)**2)*(z/2)
    except OverflowError : 
        return None

def divergence(z:complex, n_iter, div_limit):
    """Number from 0 to 1 caracterizing the complex's collatz sequence divergence. 0 means it directly diverges, 1 means it converges."""
    i = 0
    while i < n_iter:
        i += 1
        
        try : 
            abs_ = abs(z)
            z = cltz(z)
        except OverflowError : break
        if abs_ > div_limit : break
        if not z : break
        
    return i/n_iter

