from typing import Union
from cmath import sin, cos
from math import pi

def cltz(z:complex) -> complex:
    """Complex function to iterate in order to get Collatz sequence complex extension."""
    
    try : 
        return (sin(z*pi/2)**2)*(3*z+1) + (cos(z*pi/2)**2)*(z/2)
    except OverflowError : 
        return None


def cltz_seq(z:complex, n:int, div_limit=1e20):
    for _ in range(n):
        yield z
        z = cltz(z)
        try : 
            if not z or abs(z) > div_limit: break
        except OverflowError : break

def divergence(z:complex, n_iter, div_limit):
    """Number from 0 to 1 caracterizing the complex's collatz sequence divergence. 0 means it directly diverges, 1 means it converges."""
    i = 0
    for _ in cltz_seq(z, n_iter, div_limit) : i += 1
    return i/500

#for i in cltz_seq(20.1, 800) : print(i)
#print([divergence(i) for i in [20, 80, 20+1j, 20.1]])
