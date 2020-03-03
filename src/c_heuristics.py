#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:38:45 2018

@author: marco
"""

from data import *
import itertools
import collections
import functools

from solutions import *

def double_ended_nn_tsp(cities, start=None):
    if start is None:
        start = first(cities)
    tour = collections.deque([start])
    unvisited = set(cities - {start})
    while unvisited:
        closest_head = nearest_neighbor(tour[0], unvisited)
        closest_tail = nearest_neighbor(tour[-1], unvisited)
        if distance(tour[0], closest_head) < distance(tour[-1], closest_tail):
            tour.appendleft(closest_head)
            unvisited.remove(closest_head)
        else:
            tour.append(closest_tail)
            unvisited.remove(closest_tail)
    return tour

def nearset_insertion_tsp(cities, start = None):
    if start is None:
        random.seed(len(cities) * 42)
        start = random.choice(list(cities))
    tour = [start, nearest_neighbor(start, cities - {start})]
    unvisited = set(cities - {tour[0], tour[1]})
    while unvisited:
        (addition, cost) = min(
            [
                nearest_neighbor_with_dist(city, unvisited)
                for city in tour
            ],
            key=lambda t: t[1]
        )
        unvisited.remove(addition)
        tour.insert(tour.index(get_best_insert_after(addition, tour))+1, addition)
    return tour

def farthest_insertion_tsp(cities, start = None):
    if start is None:
        random.seed(len(cities) * 42)
        start = random.choice(list(cities))
    tour = [start, farthest_neighbor(start, cities - {start})]
    unvisited = set(cities - {tour[0], tour[1]})
    while unvisited:
        # Select farthest edge
        (addition, (nn, cost)) = max(
            [
                (
                    city,
                    nearest_neighbor_with_dist(city, tour)
                ) for city in unvisited
            ],
            key=lambda t: t[1][1]
        )
        # Insert into tour such that cost is minimized
        unvisited.remove(addition)
        tour.insert(tour.index(get_best_insert_after(addition, tour))+1, addition)
    return tour

def random_insertion_tsp(cities, start = None):
    if start is None:
        random.seed(len(cities) * 42)
        start = random.choice(list(cities))
    tour = [start, farthest_neighbor(start, cities - {start})]
    unvisited = set(cities - {tour[0], tour[1]})
    while unvisited:
        addition = random.choice(c for c in unvisited)
        # Insert into tour such that cost is minimized
        unvisited.remove(addition)
        tour.insert(tour.index(get_best_insert_after(addition, tour))+1, addition)
    return tour

def get_best_insert_after(city, tour):
    safe = tour.copy()
    safe.append(tour[0])
    insert_after = None
    best_insertion = float("inf")
    for fr, to in zip(safe, safe[1:]):
        diff = distance(fr, city) + distance(city, to) - distance(fr, to)
        if diff < best_insertion:
            best_insertion = diff
            insert_after = fr
    return insert_after

def nn_tsp(cities, start=None):
    """Start the tour at the first city; at each step extend the tour 
    by moving from the previous city to its nearest neighbor 
    that has not yet been visited."""
    if start is None: start = first(cities)
    tour = [start]
    unvisited = set(cities - {start})
    while unvisited:
        C = nearest_neighbor(tour[-1], unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour

# @functools.lru_cache(None)
def nearest_neighbor(A, cities):
    """Find the city in cities that is nearest to city A."""
    return min(cities, key=lambda c: distance(c, A))

def nearest_neighbor_with_dist(A, cities):
    return min([(city, distance(A, city)) for city in cities], key=lambda t: t[1])

def farthest_neighbor(A, cities):
    return max(cities, key=lambda c: distance(c, A))

def farthest_neighbor_with_dist(A, cities):
    return max([(city, distance(A, city)) for city in cities], key=lambda t: t[1])

def greedy_tsp(cities):
    """Go through edges, shortest first. Use edge to join segments if possible."""
    endpoints = {c: [c] for c in cities} # A dict of {endpoint: segment}
    for (A, B) in shortest_edges_first(cities):
        if A in endpoints and B in endpoints and endpoints[A] != endpoints[B]:
            new_segment = join_endpoints(endpoints, A, B)
            if len(new_segment) == len(cities):
                return new_segment
            
            
def shortest_edges_first(cities):
    """Return all edges between distinct cities, sorted shortest first."""
    edges = [(A, B) for A in cities for B in cities if id(A) < id(B)]
    return sorted(edges, key=lambda edge: distance(*edge))


def join_endpoints(endpoints, A, B):
    """Join B's segment onto the end of A's and return the segment. Maintain endpoints dict."""
    a_segment, b_segment = endpoints[A], endpoints[B]
    if a_segment[-1] is not A: a_segment.reverse()
    if b_segment[0] is not B: b_segment.reverse()
    a_segment.extend(b_segment)
    del endpoints[A], endpoints[B] # A and B are no longer endpoints
    endpoints[a_segment[0]] = endpoints[a_segment[-1]] = a_segment
    return a_segment



