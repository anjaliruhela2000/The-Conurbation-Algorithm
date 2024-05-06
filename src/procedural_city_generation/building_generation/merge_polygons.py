# import numpy as np
# import time
# import matplotlib.pyplot as plt

def merge_polygons(polygons, textures, output_name):
    print("Merging Polygon3Ds")

    # List of Empty Lists is filled up with polygons with corresponding texture
    poly_group_by_texture = [[] for x in range(len(textures))]
    [poly_group_by_texture[poly.texture.index].append(
        poly) for poly in polygons]

    mergedpolys = []
    ind = 0
    for polys in poly_group_by_texture:
        if len(polys) > 0:
            M = Merger()
            [M.merge(poly) for poly in polys]

            # TODO: Fix Scale!
            savelist = [[x.tolist() for x in M.allverts], M.allfaces,
                        textures[ind].name, textures[ind].scale*30, textures[ind].shrinkwrap]
            mergedpolys.append(savelist)
        ind += 1

    print("Merging done, saving data structure")
    import pickle
    import os
    import procedural_city_generation
    with open(os.path.dirname(procedural_city_generation.__file__)+"/outputs/"+output_name+".txt", 'wb') as f:
        import sys
        if sys.version[0] == "2":
            s = pickle.dumps(mergedpolys)
            f.write(s)
        else:
            pickle.dump(mergedpolys, f)

    return 0


class Merger(object):
    """Merger Class used to Merge polygons together while keeping track of an index"""

    def __init__(self):
        self.n = 0
        self.allverts = []
        self.allfaces = []

    def merge(self, poly):
        self.allfaces.extend([[x+self.n for x in face] for face in poly.faces])
        self.n += len(poly.verts)
        self.allverts.extend(poly.verts)
