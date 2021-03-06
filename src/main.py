#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:50:19 2018

@author: marco
"""

import sys
from data import *
from data2 import *
from solutions import *

from enumeration import *
from dq import *
from held_karp import *

from c_heuristics import *
from localsearch import *
from three_opt import *
from metaheuristics import *

from benchmarking import *



# plot_lines(USA_map, 'bo')
# plt.show()
# altered_canonical(Cities(30,seed=1))
# altered_canonical(USA_map)
# sys.exit(0)

# algorithms = [three_opt_canonical]
# benchmarks(algorithms, tuple(USA_map for i in range(10)))


# sys.exit(0)
#print(hk_tsp(Cities(5,seed=1)))

#sys.exit(0)

def length_ratio(cities):
    """The ratio of the tour lengths for nn_tsp and alltours_tsp algorithms."""
    return tour_length(nn_tsp(cities)) / tour_length(alltours_tsp(cities))

#print(sorted(length_ratio(Cities(8, seed=i*i)) for i in range(11)))

#sys.exit(0)


def repeat_10_nn_tsp(cities): return repeated_nn_tsp(cities, 10)
def repeat_25_nn_tsp(cities): return repeated_nn_tsp(cities, 25)
def repeat_50_nn_tsp(cities): return repeated_nn_tsp(cities, 50)
def repeat_100_nn_tsp(cities): return repeated_nn_tsp(cities, 100)

def repeat_10_de_nn_tsp(cities): return repeated_double_ended_nn_tsp(cities, 10)
def repeat_25_de_nn_tsp(cities): return repeated_double_ended_nn_tsp(cities, 25)
def repeat_50_de_nn_tsp(cities): return repeated_double_ended_nn_tsp(cities, 50)
def repeat_100_de_nn_tsp(cities): return repeated_double_ended_nn_tsp(cities, 100)

def altered_mst_tsp(cities): return alter_tour(mst_tsp(cities))


# Nearest neighbor algorithms
algorithms = [
    # nn_tsp,
    # double_ended_nn_tsp,
    # repeat_10_nn_tsp,
    # repeat_10_de_nn_tsp,
    # repeat_25_nn_tsp,
    # repeat_25_de_nn_tsp,
    # # repeat_50_nn_tsp,
    # # repeat_50_de_nn_tsp,
    # # repeat_100_nn_tsp,
    # # repeat_100_de_nn_tsp,
    # nearest_addition_tsp,
    # farthest_addition_tsp,
    altered_canonical,
    three_opt_canonical
]

# Held-Karp Algorithm
# algorithms = [hk_tsp]
benchmarks(algorithms, Maps(20, 50))


# algorithms = [altered_nn_tsp, altered_greedy_tsp, repeated_altered_nn_tsp]

# benchmarks(algorithms)
# print('-' * 100)
# benchmarks(algorithms, Maps(30, 120))
