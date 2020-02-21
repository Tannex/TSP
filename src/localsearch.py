#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:55:34 2018

@author: marco
"""

import sys
from data import *

from solutions import *
from c_heuristics import *


def compute_delta(tour, i, j):  # TODO: verify indices
    A, B, C, D = tour[i], tour[i+1], tour[j], tour[(j+1) % len(tour)] # Reversed segment is i+1 -> j
    current_cost = distance(A, B) + distance(C, D)
    reverse_cost = distance(A, C) + distance(B, D)
    return reverse_cost - current_cost

def commit_2_opt_change(tour, i, j):
    tour[i+1:j+1] = reversed(tour[i+1:j+1])  # Left inclusive right exclusive; A = i;B = i+1; C = j; D = j+1 reverse segment BC inclusive

def two_opt_first_improvement(tour):
    """Try to alter tour for the better by reversing segments. First improvement"""
    improvement = True
    while improvement:
        improvement = False
        for (start, end) in all_segments(len(tour)):
            delta = compute_delta(tour, start, end)
            if delta < 0:
                commit_2_opt_change(tour, start, end)
                improvement = True
                # plot_tour(tour)
                # print(start,end,delta)
    return tour

def two_opt_best_improvement(tour):
    """Try to alter tour for the better by reversing segments. Best improvement"""
    improvement = True
    while improvement:
        improvement = False
        best_delta = 0  # Only accept delta < 0.
        best_segment = None
        # Get best segment if any immediate 2-exchange improvement exists
        for (i, j) in all_segments(len(tour)):
            delta = compute_delta(tour, i, j)
            if delta < best_delta:
                best_delta = delta
                best_segment = (i, j)
        if best_delta < 0:
            start, end = best_segment
            commit_2_opt_change(tour, start, end)
            # print(start,end,delta)
            improvement = True
    return tour


def all_segments(N):
    """Return (start, end) pairs of indexes that form segments of tour of length N."""
    return (
        (start, end) 
        for (start, end) in itertools.combinations(range(N), 2)
        if end > start+1
        )

def altered_nn_tsp(cities):
    """Run nearest neighbor TSP algorithm, and alter the results by reversing segments."""
    return two_opt_first_improvement(nn_tsp(cities))

def altered_greedy_tsp(cities):
    """Run greedy TSP algorithm, and alter the results by reversing segments."""
    return two_opt_first_improvement(greedy_tsp(cities))

def altered_canonical(cities):
    """Construct a canonical solution and alter the result by reversing segments."""
    tour=[c for c in cities]
    return two_opt_first_improvement(tour)

def altered_best_nn_tsp(cities):
    return two_opt_best_improvement(nn_tsp(cities))

def altered_best_greedy_tsp(cities):
    return two_opt_best_improvement(greedy_tsp(cities))

def altered_best_canonical(cities):
    tour = [c for c in cities]
    return two_opt_best_improvement(tour)

def altered_farthest_insertion(cities):
    return two_opt_first_improvement(farthest_insertion_tsp(cities))

def altered_best_farthest_insertion(cities):
    return two_opt_best_improvement(farthest_insertion_tsp(cities))
