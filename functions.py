from math import floor
from pprint import pprint

def quad_matrix_multiply(square, mat, cache=None):
    new_quad = []
    if cache is not None:
        for vec in square:
            index = tuple(vec) #(vec.x, vec.y, vec.z)
            if index not in cache:
                cache[index] = mat.vec_dot(vec)
            new_quad.append(cache[index])
    else:
        for i in range(len(square)):
            new_quad.append(mat.vec_dot(square[i]))
    return new_quad


def quad_matrix_multiply2(square, mat, cache=None):
    new_quad = []
    if cache is not None:
        for i in range(len(square)):
            vec = square[i]
            index = (vec.x, vec.y, vec.z)
            if index not in cache:
                cache[index] = mat.vec_dot2(vec)
            new_quad.append(cache[index])
    else:
        for i in range(len(square)):
            new_quad.append(mat.vec_dot2(square[i]))
    return new_quad

def get_normal(quad):
    line1 = quad[1][0] - quad[0][0]
    line2 = quad[2][0] - quad[0][0]
    return line1.cross(line2)
    line1 = quad[1] - quad[0]
    line2 = quad[2] - quad[0]
    return cross(line1[:3], line2[:3])


def perspective_div(vec):
    new_vec = vec[0] / vec[1]
    return new_vec
    points = [(vec2.x + 1) * 240, (vec2.y + 1) * 135]
    # print(points, vec2, vec)
    return points

def np_quad_dot(quad, mat):
    new_quad = []
    for vertex in quad:
        new_quad.append(dot(list(vertex) + [1], mat))
    return new_quad

def screen_points(vec):
    # print(vec)
    # points = [(vec[0] + 1) * 240, (vec[1] + 1) * 135]
    return [(vec[0] + 1) * 240, (vec[1] + 1) * 135]

def vec4toscreen(vec):
    return screen_points(perspective_div(vec))

def vec4_dot(vec1, vec2):
    return vec1[0].dot(vec2[0]) + vec1[1] * vec2[1]

'''
def get_rotated_vector(yaw, pitch, roll):
    return dot(Matrix.Z_VEC, Matrix.get_rotation_mat(yaw, pitch, roll))
'''


def cap(value, minimum, maximum):
    return min(max(value, minimum), maximum)
