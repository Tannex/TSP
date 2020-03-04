#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:55:34 2018

@author: marco
"""


import sys
import numpy as np
from enum import Enum
from data import *


from solutions import *
from c_heuristics import *


class Move(Enum):
    REVERSE_BC = 0
    REVERSE_BC_AND_SWAP = 1
    SWAP = 2
    REVERSE_DE_AND_SWAP = 3


def three_opt_canonical(cities):
    """Construct canonical solution, and alter the results by three opt."""
    tour = [c for c in cities]
    return three_opt(tour)


def three_opt(tour):
    """Iterative improvement based on 3 exchange."""
    improved = True
    # Get best segment if any immediate 2-exchange improvement exists
    i = 0
    while improved:
        i += 1
        improved = False
        if i % 50 == 0:
            plt.show()
        for (i, j, k) in generate_ijk(len(tour), randomized=True):
            best_closure, delta = calculate_delta(tour, i, j, k)
            if delta < 0:
                improved = True
                # print(delta, (i, j, k), best_closure)
                apply_move(tour, best_closure, i, j, k)
    return tour


def three_opt_best_improvement(tour):
    """Iterative best-improvement based on 3 exchange."""
    best_delta = 0  # Only accept delta < 0.
    best_ijkm = None
    # Get best segment if any immediate 2-exchange improvement exists
    for (i, j, k) in generate_ijk(len(tour), randomized=False):
        best_move, delta = calculate_delta(tour, i, j, k)
        if delta < best_delta:
            best_delta = delta
            best_ijkm = (i, j, k, best_move)
    if best_delta < 0:
        i, j, k, m = best_ijkm
        print(best_delta, best_ijkm)
        apply_move(tour, m, i, j, k)
        return three_opt(tour)
    return tour


def get_best_closure(cost_dict):  # (argmax, max) combo
    best_cost = float('inf')
    best_move = None
    for m in Move:
        if cost_dict[m] < best_cost:
            best_cost = cost_dict[m]
            best_move = m
    return best_move, best_cost


def calculate_delta(tour, i, j, k):
    A, B, C, D, E, F = tour[i], tour[i+1], tour[j], tour[j+1], tour[k], tour[(k+1) % len(tour)]
    removed_cost = -(distance(A, B) + distance(C, D) + distance(E, F))
    costs = {}
    # Cost of reversing BC segment (doing so only has one closure)
    costs[Move.REVERSE_BC] = distance(A, C) + distance(B, E) + distance(D, F)
    # Cost of Swapping BC and DE segments
    costs[Move.SWAP] = distance(A, D) + distance(E, B) + distance(C, F)
    # Cost of swapping BC and DE segments followed by reverse of BC
    costs[Move.REVERSE_BC_AND_SWAP] = distance(A, D) + distance(E, C) + distance(B, F)
    # Cost of swapping BC and DE segments followed by reverse of DE
    costs[Move.REVERSE_DE_AND_SWAP] = distance(A, E) + distance(D, B) + distance(C, F)
    best_move, cost = get_best_closure(costs)
    delta = removed_cost + cost
    return best_move, delta


def apply_move(tour, move, i, j, k):
    # segment_a = (i+1, j)
    # segment_b = (j+1, k)
    if move == Move.SWAP:
        swap_segments(tour, i+1, j, j+1, k)
    elif move == Move.REVERSE_BC:
        reverse_segment(tour, i+1, j)
        reverse_segment(tour, j+1, k)  # We must reverse DE as well, since that is the only valid closure
    elif move == Move.REVERSE_BC_AND_SWAP:
        reverse_segment(tour, i+1, j)
        swap_segments(tour, i+1, j, j+1, k)
    elif move == Move.REVERSE_DE_AND_SWAP:
        reverse_segment(tour, j+1, k)
        swap_segments(tour, i+1, j, j+1, k)


def swap_segments(tour, start_a, end_a, start_b, end_b):
    initial, a, between, b, after = (
        tour[0:start_a],
        tour[start_a:end_a+1],
        tour[end_a+1:start_b],
        tour[start_b:end_b+1],
        tour[end_b+1:len(tour)]
    )  # A bit overkill, since between always empty when used by three-opt.
    tour[:] = initial + b + between + a + after


def reverse_segment(tour, start, end):
    tour[start:end+1] = reversed(tour[start:end+1])


def generate_ijk(length, randomized=True):  # For now, check all valid i,j,k combinations
    if not randomized:
        for i in range(0, length):
            for j in range(i + 2, length):
                for k in range(j+2, length):
                    yield i, j, k
    else:  # leads to more ijk values being checked (since the mask isn't ordered)
        mask = np.random.permutation(length)
        for (i, j, k) in itertools.permutations(mask, 3):
            if i + 1 < j < k - 1:
                print(i, j, k)
                yield i, j, k
