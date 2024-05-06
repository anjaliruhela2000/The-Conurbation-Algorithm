
import json
import os
import random


class Texture(object):
    def __init__(self, name, scale, minP, maxP, shrinkwrap=False, index=0):

        self.name = name
        self.scale = scale
        self.minP = minP
        self.maxP = maxP
        self.shrinkwrap = shrinkwrap
        self.index = index

    def __repr__(self):
        return "Tex_"+self.name


def updateTextures():
    import procedural_city_generation
    path = os.path.dirname(procedural_city_generation.__file__)
    teximages = os.listdir(path+"/visualization/Textures/")

    with open(path+"/visualization/texTable.json", 'r') as f:
        texTable = f.read()
    texTable = json.loads(texTable)

    textures = []
    i = 0
    for img in teximages:
        shrinkwrap = True if (("Road" in img) or ("Floor" in img)) else False
        scale, minP, maxP = texTable[img]
        textures.append(Texture(img, scale, minP, maxP, shrinkwrap, i))
        i += 1

    return textures


class textureGetter(object):
    def __init__(self, textures):
        self.textures = textures

    def getTexture(self, name, p):
        p = max(min(100, p*100), 0)
        tex = [x for x in self.textures if name in x.name]
        if tex != []:
            tex = [x for x in tex if x.minP <= p <= x.maxP]
            if tex != []:
                return random.choice(tex)
            else:
                print("Warning! There is no texture that matches the criterion: "+name +
                      " in texturename AND minP<"+str(p)+"<maxP. \n A random Texture was used!")
                return random.choice(self.textures)
        else:
            print("Warning! There is no texture that matches the criterion: " +
                  name+" in texturename. \n A random Texture was used!")
            return random.choice(self.textures)
