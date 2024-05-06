# -*- coding: utf-8 -*-
from __future__ import division
from procedural_city_generation.roadmap.Vertex import Vertex

import numpy as np
from scipy.spatial import cKDTree
from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton = Singleton("roadmap")


def check(suggested_vertex, neighbour, newfront):
    if (abs(suggested_vertex.coords[0]) > singleton.border[0]-singleton.maxLength) or (abs(suggested_vertex.coords[1]) > singleton.border[1]-singleton.maxLength):
        return newfront

    # Finds all nearby Vertex and their distances
    distances, nearvertex = singleton.global_lists.tree.query(
        suggested_vertex.coords, 10, distance_upper_bound=singleton.maxLength)
    l = len(singleton.global_lists.vertex_list)
    nearvertex = [singleton.global_lists.vertex_list[x]
                  for x in nearvertex if x < l]

    # Distances[0] is the distance to the nearest Vertex, nearve:
    if distances[0] < singleton.min_distance:

        # If the nearest Vertex is not a neighbor
        if nearvertex[0] not in neighbour.neighbours:

            # Find the best solution - as in the closest intersection
            bestsol = np.inf
            solvertex = None

            for k in nearvertex:
                for n in k.neighbours:
                    if n in nearvertex:  # and not in doneliste
                        sol = get_intersection(
                            neighbour.coords, nearvertex[0].coords-neighbour.coords, k.coords, n.coords-k.coords)
                        if sol[0] > 0.00001 and sol[0] < 0.99999 and sol[1] > 0.00001 and sol[1] < 0.99999 and sol[0] < bestsol:
                            bestsol = sol[0]
                            solvertex = [n, k]
            # If there is at least one solution, intersect that solution
            # See docstring #3 and #4
            if solvertex is not None:
                solvertex[1].neighbours.remove(solvertex[0])
                solvertex[0].neighbours.remove(solvertex[1])
                newk = Vertex(neighbour.coords+bestsol *
                              (nearvertex[0].coords-neighbour.coords))
                singleton.global_lists.vertex_list.append(newk)
                singleton.global_lists.coordsliste.append(newk.coords)
                singleton.global_lists.tree = cKDTree(
                    singleton.global_lists.coordsliste, leafsize=160)
                neighbour.connection(newk)
                solvertex[1].connection(newk)
                solvertex[0].connection(newk)
                return newfront
            else:
                # If there is no solution, the Vertex is clear
                # See docstring finish
                nearvertex[0].connection(neighbour)
        return newfront

    bestsol = np.inf
    solvertex = None

    # If there is not an existing vertex too close, do the same thing but with
    # The vector between the suggested vertex and its neighbro
    for k in nearvertex:
        for n in k.neighbours:
            if n in nearvertex:  # and not in doneliste
                sol = get_intersection(
                    neighbour.coords, suggested_vertex.coords-neighbour.coords, k.coords, n.coords-k.coords)
                if sol[0] > 0.00001 and sol[0] < 1.499999 and sol[1] > 0.00001 and sol[1] < 0.99999 and sol[0] < bestsol:
                    bestsol = sol[0]
                    solvertex = [n, k]
    if solvertex is not None:
        solvertex[1].neighbours.remove(solvertex[0])
        solvertex[0].neighbours.remove(solvertex[1])

        newk = Vertex(neighbour.coords+bestsol *
                      (suggested_vertex.coords-neighbour.coords))
        singleton.global_lists.vertex_list.append(newk)
        singleton.global_lists.coordsliste.append(newk.coords)
        singleton.global_lists.tree = cKDTree(
            singleton.global_lists.coordsliste, leafsize=160)
        neighbour.connection(newk)
        solvertex[1].connection(newk)
        solvertex[0].connection(newk)
        return newfront

    # If the Vertex is clear to go, add him and return newfront.

    suggested_vertex.connection(neighbour)
    newfront.append(suggested_vertex)
    singleton.global_lists.vertex_list.append(suggested_vertex)
    singleton.global_lists.coordsliste.append(suggested_vertex.coords)
    singleton.global_lists.tree = cKDTree(
        singleton.global_lists.coordsliste, leafsize=160)
    return newfront


def get_intersection(a, ab, c, cd):
    try:
        return np.linalg.solve(np.array([ab, -cd]).T, c-a)
    except np.linalg.linalg.LinAlgError:
        return np.array([np.inf, np.inf])
