import math
import numpy as np
from array import array

def vec(vec):
    return np.matrix(vec)

def identity():
    return np.matrix([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

def transform(m,v):
    return np.asarray(m * np.asmatrix(v).T)[:,0]

def magnitude(v):
    return math.sqrt(np.sum(np.asarray(v) ** 2))

def normalize(v):
    m = magnitude(v)
    if m == 0:
        return v
    return np.divide(np.matrix(v), m)

def orthographic(l, r, b, t, n, f):
    dx = r - l
    dy = t - b
    dz = f - n
    rx = -(r + l) / (r - l)
    ry = -(t + b) / (t - b)
    rz = -(f + n) / (f - n)
    return np.matrix([[2.0/dx, 0,      0,       rx],
                      [0,      2.0/dy, 0,       ry],
                      [0,      0,      -2.0/dz, rz],
                      [0,       0,     0,        1]])

def perspective(fow, aspect, near, far):
    f = 1.0/math.tan(math.radians(fow)/2.0)
    zz = (far + near)/ (far - near)
    zw = -(2*far*near)/(far - near)
    return np.matrix([[f/aspect,  0,   0,  0],
                      [       0,  f,   0,  0],
                      [       0,  0,  zz, zw],
                      [       0,  0,  -1,  0]])


def frustrum(x0, x1, y0, y1, z0, z1):
    a = (x1+x0)/(x1-x0)
    b = (y1+y0)/(y1-y0)
    c = -(z1+z0)/(z1-z0)
    d = -2*z1*z0/(z1-z0)
    sx = 2*z0/(x1-x0)
    sy = 2*z0/(y1-y0)
    return np.matrix([[sx, 0, a, 0],
                      [0, sy, b, 0],
                      [0, 0, c,  d],
                      [0, 0, -1, 0]])

def translate(xyz):
    x,y,z = xyz
    return np.matrix([[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]])

def scale(xyz):
    x,y,z = xyz
    return np.matrix([[x,0,0,0],
                      [0,y,0,0],
                      [0,0,z,0],
                      [0,0,0,1]])

def sincos(a):
    a = math.radians(a)
    return math.sin(a), math.cos(a)

def rotate(a, xyz):
    x,y,z = normalize(xyz).tolist()[0]
    s,c = sincos(a)
    nc = 1 - c
    return np.matrix([[   x*x*nc + c, x*y*nc -  z*s, x*z*nc + y*s, 0],
                      [ y*x*nc + z*s,    y*y*nc + c, y*z*nc - x*s, 0],
                      [ x*z*nc - y*s, y*z*nc +  x*s, z*z*nc +   c, 0],
                      [            0,             0,            0, 1]])

def rotx(a):
    s, c = sincos(a)
    return np.matrix([[ 1, 0,  0, 0],
                      [ 0, c, -s, 0],
                      [ 0, s,  c, 0],
                      [ 0,  0,  0, 1 ]])


def roty(a):
    s, c = sincos(a)
    return np.matrix([[c, 0, s, 0],
                      [0, 1, 0, 0],
                      [-s, 0, c, 0],
                      [0, 0, 0, 1]])


def rotz(a):
    s, c = sincos(a)
    return np.matrix([[c, -s, 0, 0],
                      [s, c, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])


def lookat(eye, target, up):
    F = np.matrix(target) - np.matrix(eye)
    f = normalize(F)
    U = normalize(np.matrix(up))
    s = np.cross(f, U)
    u = np.cross(s, f)
    M = np.matrix(np.identity(4))
    M[:3, :3] = np.vstack([s,u,-f])
    T = translate(-eye)
    return M * T

def viewport(x, y, w, h):
    x, y, w, h = map(float, (x, y, w, h))
    return np.matrix([[w/2,   0, 0, x+w/2],
                      [  0, h/2, 0, y+h/2],
                      [  0,   0, 1,     0],
                      [  0,   0, 0,     1]])

