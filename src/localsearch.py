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


def reverse_segment_if_better(tour, i, j):
    """If reversing tour[i:j] would make the tour shorter, then do it."""
    # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    # Are old edges (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    current_cost = distance(A, B) + distance(C, D)
    reverse_cost = distance(A, C) + distance(B, D)
    delta = reverse_cost - current_cost
    if current_cost > reverse_cost:
        tour[i:j] = reversed(tour[i:j])
    return delta


def two_opt_first_improvement(tour):
    """Try to alter tour for the better by reversing segments. First improvement"""
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        delta = reverse_segment_if_better(tour, start, end)
        #if delta < 0:
        #    plot_tour(tour)
        #    print(start,end,original_length+delta)

    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour) < original_length:
        return two_opt_first_improvement(tour)
    return tour


def two_opt_best_improvement(tour):
    """Try to alter tour for the better by reversing segments. Best improvement"""
    improved = True
    while improved:
        improved = False
        best_delta = 0  # Only accept delta < 0.
        best_segment = None
        # Get best segment if any immediate 2-exchange improvement exists
        for (i, j) in all_segments(len(tour)):
            A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
            current_cost = distance(A, B) + distance(C, D)
            updated_cost = distance(A, C) + distance(B, D)
            delta = updated_cost - current_cost
            if delta < best_delta:
                best_delta = delta
                best_segment = (i, j)
        if best_delta < 0:
            start, end = best_segment
            tour[start:end] = reversed(tour[start:end])
            improved = True
    return tour


def all_segments(N):
    """Return (start, end) pairs of indexes that form segments of tour of length N."""
    return [(start, start + length)
            for length in range(N, 2-1, -1)
            for start in range(N - length + 1)]


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
