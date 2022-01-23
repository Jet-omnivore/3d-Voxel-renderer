import math
import constants as CONSTANTS

from pygame import Vector3


class Mat4:
    __slots__ = ['rows', 'cols', 'mat']

    def __init__(self, mat):
        self.mat = mat 
        self.cols = [
                 (Vector3((mat[0][0], mat[1][0], mat[2][0])), mat[3][0]),
                 (Vector3((mat[0][1], mat[1][1], mat[2][1])), mat[3][1]),
                 (Vector3((mat[0][2], mat[1][2], mat[2][2])), mat[3][2]),
                 (Vector3((mat[0][3], mat[1][3], mat[2][3])), mat[3][3])
             ]

    def vec_dot(self, vec):
        return  (
                Vector3(
                    vec.dot(self.cols[0][0]) + self.cols[0][1],
                    vec.dot(self.cols[1][0]) + self.cols[1][1],
                    vec.dot(self.cols[2][0]) + self.cols[2][1],
                        ),
                    vec.dot(self.cols[3][0]) + self.cols[3][1]
                )

    def vec_dot2(self, vec):
        v = vec[0]
        w = vec[1]
        return (
                Vector3(
                    v.dot(self.cols[0][0]) + w * self.cols[0][1],
                    v.dot(self.cols[1][0]) + w * self.cols[1][1],
                    v.dot(self.cols[2][0]) + w * self.cols[2][1],
                        ),
                    v.dot(self.cols[3][0]) + w * self.cols[3][1]
                )

    def mat4_dot(self, mat):
        new_mat = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    new_mat[i][j] += self.mat[i][k] * mat.mat[k][j]
        return Mat4(new_mat)



def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = list(transposeMatrix(cofactors))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
