#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:55:34 2018

@author: marco
"""

import data
import algorithms
import assessment
import benchmarking


def reverse_segment_if_better(tour, i, j):
    "If reversing tour[i:j] would make the tour shorter, then do it." 
    # Given tour [...A-B...C-D...], consider reversing B...C to get [...A-C...B-D...]
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    # Are old edges (AB + CD) longer than new ones (AC + BD)? If so, reverse segment.
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])
        
        
def alter_tour(tour):
    "Try to alter tour for the better by reversing segments."
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        reverse_segment_if_better(tour, start, end)
    # If we made an improvement, then try again; else stop and return tour.
    if tour_length(tour) < original_length:
        return alter_tour(tour)
    return tour

def all_segments(N):
    "Return (start, end) pairs of indexes that form segments of tour of length N."
    return [(start, start + length)
            for length in range(N, 2-1, -1)
            for start in range(N - length + 1)]

def altered_nn_tsp(cities):
    "Run nearest neighbor TSP algorithm, and alter the results by reversing segments."
    return alter_tour(nn_tsp(cities))


def repeated_altered_nn_tsp(cities, repetitions=20): 
    "Use alteration to improve each repetition of nearest neighbors."
    return shortest_tour(alter_tour(nn_tsp(cities, start)) 
                         for start in sample(cities, repetitions))

def repeat_5_altered_nn_tsp(cities): return repeated_altered_nn_tsp(cities, 5)



def altered_greedy_tsp(cities):
    "Run greedy TSP algorithm, and alter the results by reversing segments."
    return alter_tour(greedy_tsp(cities))