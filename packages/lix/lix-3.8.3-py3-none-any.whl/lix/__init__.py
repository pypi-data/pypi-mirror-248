'''
# Caches
@lix.cache
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fibo(n-2)

@lix.fast
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fibo(n-2)

@lix.limit(5)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fibo(n-2)

# Sort
my_list = [6,2,5,7,9,7,3,1,124,6,54,1,4,47,74,43,1,12,5,7,94,223]

lix.bubblesort(my_list)
lix.insertionsort(my_list)
lix.selectionsort(my_list)
lix.mergesort(my_list)
lix.quicksort(my_list)
lix.heapsort(my_list)
lix.shellsort(my_list)

# Color
lix.Fore      # lix.Fore.BLACK
lix.Back
lix.Style
lix.Effect
lix.Decor
lix.BackEffect

lix.init()    # OPTIONAL
lix.deinit()  # OPTIONAL

lix.clear()   # clear console/terminal
lix.reset()   # reset console/terminal
lix.blend()   # blend color, style, back, etc
lix.get('black', 'Fore')     # get color, style, back, etc
lix.gradient('black', 'Fore') # get gradient color, style, back, etc
lix.code('print("Hello World")', 'text', 'friendly') # code highlight
lix.new(fore='black', back='white', style='bold') # new color
lix.color('Hello World', lix.new(fore='black', back='white', style='bold')) # color with new

# Math
lix.mean(my_list)
lix.median(my_list)
lix.mode(my_list)
lix.range(my_list)
lix.variance(my_list)
lix.standard_deviation(my_list)
lix.covariance(my_list, my_list2)
lix.correlation(my_list, my_list2)
lix.linear_regression(my_list, my_list2)

# Fibonacci
lix.fib(5)
lix.fibonacci(10000000)

# Factorial
lix.factorial(5)
lix.factorial(10000000)

# Square Root
lix.sqrt(5)
lix.square_root(5)
lix.squareroot(5)

# Copying
lix.copy(object)
lix.shallow(object)

lix.deepcopy(object)
lix.deep(object)

# Random
lix.random(start, end)
lix.randint(start, end)
lix.randrange(start, end)
lix.choice(my_list)
lix.choices(my_list, k=5)
lix.shuffle(my_list)
lix.sample(my_list, k=5)

# Time
lix.time(5)
lix.sleep(5)
lix.format(time)
'''

from .factorial import factorial
from .cache import *
from .color import *
from .math  import *
from .sort  import *
from .sqrt  import *
from .fib   import *

import copy
shallow = copy.copy
deepcopy = copy.deepcopy
deep = copy.deepcopy
copy = copy.copy

import random
randint = random.randint
randrange = random.randrange
choice = random.choice
choices = random.choices
shuffle = random.shuffle
sample = random.sample
random = random.random

import time
sleep = time.sleep
format = time.strftime
time = time.time

__version__ = '3.8.3'
__author__ = 'flowa'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 flowa'
