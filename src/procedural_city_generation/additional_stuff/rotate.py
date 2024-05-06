import numpy as np

def rotate(angle, vector):
    #Explicit case because it gets called very often
    if angle == 90:
        return np.array([-vector[1], vector[0]])

    angle=angle*np.pi/180
    matrix=np.array([np.cos(angle),
    np.sin(angle),
    -np.sin(angle),
    np.cos(angle)]).reshape(2, 2)

    matrix=np.dot(vector, matrix)
    return matrix
