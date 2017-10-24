import Matrixop as mo

class CameraMovement:
    FORWARD  = 0
    BACKWARD = 1
    LEFT     = 2
    RIGHT    = 3


class Camera:

    def __init__(self, conf):
        self.position =    conf['eye']
        self.front = [0,0,-1]
        self.up =          conf['up']
        #self.right =
        #self.world_up
        #self.yaw
        #self.pitch
        self.speed =       conf['mouse_speed']
        self.sensitivity = conf['mouse_sensitivity']
        #self.zoom
        self.fow =         conf['fow']
        self.aspect_ratio = eval(conf['aspect_ratio'])
        self.near_plane =  conf['near_plane']
        self.far_plane =   conf['far_plane']
        self.projection = self.perspective


    def perspective(self):
        return mo.perspective(self.fow, self.aspect_ratio, self.near_plane, self.far_plane)


    def orthographic(self):
        return mo.orthographic(-1, 1, -1, 1, self.near_plane, self.far_plane)

    def viewMatrix(self):
        return mo.lookat(self.position, mo.vec(self.position) + mo.vec(self.front), self.up)