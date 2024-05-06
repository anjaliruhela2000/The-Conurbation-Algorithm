from procedural_city_generation.additional_stuff.Singleton import Singleton
try:
    from procedural_city_generation.roadmap.main import gui as plt
    if plt is None:
        import matplotlib.pyplot as plt
except:
    import matplotlib.pyplot as plt

plotbool = False

singleton = Singleton("roadmap")


class Vertex(object):
    def __init__(self, coords):
        self.coords = coords
        self.neighbours = []
        self.minor_road = False
        self.seed = False

    def __cmp__(self, other):
        if isinstance(other, Vertex):
            if self.coords[0] > other.coords[0]:
                return 1
            elif self.coords[0] < other.coords[0]:
                return -1
            else:
                if self.coords[1] > other.coords[1]:
                    return 1
                elif self.coords[1] < other.coords[1]:
                    return -1
            return 0

    def connection(self, other):
        if other not in self.neighbours:
            self.neighbours.append(other)
        if self not in other.neighbours:
            other.neighbours.append(self)

        if plotbool:
            col = 'black'
            width = 3
            if self.minor_road or other.minor_road:
                col = 'blue'
                width = 1
            plt.plot([self.coords[0], other.coords[0]], [
                     self.coords[1], other.coords[1]], color=col, linewidth=width)

    def __repr__(self):
        return "Vertex"+str(self.coords)+"\n"


def set_plotbool(singletonbool):
    global plotbool
    plotbool = singletonbool
