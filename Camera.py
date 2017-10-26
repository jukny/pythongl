import Matrixop as mo

class CameraMovement:
    FORWARD  = 0
    BACKWARD = 1
    LEFT     = 2
    RIGHT    = 3


class Camera:

    def __init__(self, conf):
        self.position =    conf['eye']
        self.target =      conf['target']
        self.up =          conf['up']
        self.front = [0,0,-1]
        #self.right =
        #self.world_up
        #self.yaw
        #self.pitch
        self.keyboard_speed = conf['keyboard_speed']
        self.mouse_speed =       conf['mouse_speed']
        self.sensitivity = conf['mouse_sensitivity']
        #self.zoom
        self.fow =         conf['fow']
        self.aspect_ratio = conf['aspect_ratio']['width']/conf['aspect_ratio']['height']
        self.near_plane =  conf['near_plane']
        self.far_plane =   conf['far_plane']
        try:
            self.projection = getattr(locals()['self'], conf['projection'])
        except AttributeError:
            print('Projection: {}, not available'.format(conf['projection']))
            self.projection = self.perspective


    def perspective(self):
        return mo.perspective(self.fow, self.aspect_ratio, self.near_plane, self.far_plane)


    def orthographic(self):
        return mo.orthographic(-1, 1, -1, 1, self.near_plane, self.far_plane)

    def viewMatrix(self):
        la = [a + b for a, b in zip(self.target, self.front)]
        return mo.lookat(self.position, la, self.up)

    def move_z(self, dz):
        x,y,z = self.position
        xf,yf,zf = self.front
        xn = x+dz*self.keyboard_speed*xf
        yn = y+dz*self.keyboard_speed*yf
        zn = z+dz*self.keyboard_speed*zf
        self.position = [xn,yn,zn]

    def move_x(self, dx):
        x,y,z = self.position
        xn,yn,zn = mo.x_axis(self.front, self.up, self.keyboard_speed)
        self.position = [x+dx*xn, y+dx*yn, z+dx*zn]
        print(self.position)


    def resize_viewport(self, w, h):
        self.aspect_ratio = w/h
