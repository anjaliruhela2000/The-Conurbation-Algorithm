# -*- coding: utf-8 -*-
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
# import numpy.linalg as la

from procedural_city_generation.additional_stuff.Singleton import Singleton
from procedural_city_generation.building_generation.building_tools import *
from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.Polygon3D import Polygon3D

singleton = Singleton("building_generation")


def roof(walls, roofwalls, currentheight, housebool, texture, texture2=None):
    roofheight = np.random.uniform(
        singleton.roofheight_min, singleton.roofheight_max)

    if roofwalls.l == 4 and housebool:
        return houseroof(roofwalls, currentheight, roofheight, texture)
    else:
        return kastenroof(walls, roofwalls, currentheight, roofheight, texture, texture2)


def houseroof(walls, currentheight, roofheight, texture):
    # Differentiation: the shorter of the first two walls is to be cut in half
    if not np.linalg.norm(np.diff(walls.getWalls()[0], axis=0)) < np.linalg.norm(np.diff(walls.getWalls()[1], axis=0)):
        walls = Walls(np.roll(walls.vertices, 1, axis=0), walls.l)

    h_low = np.array([0, 0, currentheight])
    h_high = h_low+np.array([0, 0, roofheight])

    # The gable coordinates
    c1, c2 = sum(walls.getWalls()[0]/2), sum(walls.getWalls()[2]/2)

    # Verts are the vertices of the wall and the vertices of the gable
    verts = [x+h_low for x in walls.vertices]+[c1+h_high, c2+h_high]

    # Faces are two rectangles and two triangles
    faces = [(0, 1, 5, 4), (3, 2, 5, 4), (0, 3, 4), (1, 2, 5)]
    return [Polygon3D(verts, faces, texture)]


def kastenroof(walls, roofwalls, currentheight, roofheight, texture, texture2=None):
    # Texture2 is optional: if not given it will be texture1
    texture2 = texture2 if texture2 else texture

    # TODO: Move numeric values to conf.
    # Box is a scaled down version of the roofwalls
    box = scaletransform(roofwalls, random.uniform(0.07, 0.14))

    if not roofwalls.l == 4:
        # Constructs a box with 4 sides if the box did not have 4 sides
        a, b = box.vertices[0], box.vertices[1]
        n = (b-a)
        n = np.array([-n[1], n[0], 0])
        box = Walls(np.array([a, b, b+n, a+n]), 4)

    # Checks if every vertex of the box is "inside" the roof polygon so that the box does not float.
    # If this is not the case for every vertex, then just a flat roof is built
    for vert in box.vertices:
        if not p_in_poly(walls, vert):
            return [Polygon3D(walls.vertices+np.array([0, 0, currentheight]), [range(walls.l)], texture)]

    # List of the walls and the top of the box and the flat roof
    return [buildwalls(box, currentheight, currentheight+roofheight, texture2),
            Polygon3D(
                box.vertices+np.array([0, 0, currentheight+roofheight]), [range(4)], texture2),
            Polygon3D(walls.vertices+np.array([0, 0, currentheight]), [range(walls.l)], texture)]


def isleft(wall, point):
    return ((wall[1][0]-wall[0][0])*(point[1]-wall[0][1]) - (point[0]-wall[0][0]) * (wall[1][1]-wall[0][1]))


def p_in_poly(walls, point):
    counter = 0

    for wall in walls.getWalls():
        if wall[0][1] <= point[1]:
            if wall[1][1] > point[1]:
                if isleft(wall, point) > 0:
                    counter += 1
            else:
                if isleft(wall, point) < 0:
                    counter -= 1
    if counter != 0:
        return True
    return False
