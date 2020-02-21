#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:53:02 2018

@author: marco
"""

from data import *

from solutions import *
from c_heuristics import *
from metaheuristics import *
# from benchmarking import *

import matplotlib.pyplot as plt

# @functools.lru_cache(None)
def benchmark(function, inputs):
    """Run function on all the inputs; return pair of (average_time_taken, results)."""
    t0           = time.clock()
    results      = [(function(x), time.clock() - t0) for x in inputs]
    t1           = time.clock()
    average_time = (t1 - t0) / len(inputs)
    return average_time, results


def benchmarks(tsp_algorithms, maps=Maps(30, 60)):
    """Print benchmark statistics for each of the algorithms."""
    all_lengths = []
    for tsp in tsp_algorithms:
        average_time, results = benchmark(tsp, maps)
        lengths, times = [], []
        for (r, t) in results:
            lengths.append(tour_length(r))
            times.append(t)
        print("{:>25} |{:7.0f} ±{:4.0f} ({:5.0f} to {:5.0f}) |{:7.3f} secs/map | {} x {}-city maps"
              .format(tsp.__name__, mean(lengths), stdev(lengths), min(lengths), max(lengths),
                      average_time, len(maps), len(maps[0])))
        all_lengths.append(lengths)
    fig, axs = plt.subplots()
    axs.boxplot(all_lengths, 0, 'ro', 0)
    axs.set_title("Benchmarks")
    axs.set_yticklabels(map(lambda x: x.__name__, tsp_algorithms))
    plt.show()
