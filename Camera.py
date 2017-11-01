import Matrixop as mo
from  math import cos, sin, radians
import yaml
import numpy as np

class Direction:
    FORWARD  = 0
    BACKWARD = 1
    LEFT     = 2
    RIGHT    = 3


class Camera:

    def __init__(self):
        try:
            with open('conf/camera.yml') as cstream:
                self.config = yaml.load(cstream)
        except IOError as ie:
            print(ie)
            exit(1)
        except yaml.YAMLError as ye:
            print(ye)
            exit(1)
        self.position =       self.config['position'] #Startup [0,0,10]
        self.target =         self.config['target']   #Startup [0,0,0]
        self.front =          [1,0,0]
        self.camera_up =      [0,1,0]
        self.right =          [1,0,0]
        self.yaw =            -90.0
        self.pitch =          0
        self.world_up =       [0,1,0]
        self.__update_camera_vectors()

        self.keyboard_speed = self.config['keyboard_speed']
        self.sensitivity =    self.config['mouse_sensitivity']
        self.zoom =           45.0
        self.fow =            self.config['fow']
        self.aspect_ratio =   self.config['aspect_ratio']
        self.near_plane =     self.config['near_plane']
        self.far_plane =      self.config['far_plane']
        try:
            self.projection = getattr(locals()['self'], self.config['projection'])
        except AttributeError:
            print('Projection: {}, not available'.format(self.config['projection']))
            self.projection = self.perspective


    def perspective(self):
        return mo.perspective(self.fow, self.aspect_ratio, self.near_plane, self.far_plane)

    def orthographic(self):
        return mo.orthographic(-1, 1, -1, 1, self.near_plane, self.far_plane)

    def viewMatrix(self):
        la = mo.normalize(mo.vec(self.target) + mo.vec(self.front)).tolist()[0]
        return mo.lookat(self.position, la, self.camera_up)

    def move(self, direction, delta):
        velocity = self.keyboard_speed * delta
        if direction == Direction.FORWARD:
            self.position = (mo.vec(self.position) + (velocity*mo.vec(self.front))).tolist()[0]
        if direction == Direction.BACKWARD:
            self.position = (mo.vec(self.position) - (velocity*mo.vec(self.front))).tolist()[0]
        if direction == Direction.RIGHT:
            self.position = (mo.vec(self.position) - (velocity*mo.vec(self.right))).tolist()[0]
        if direction == Direction.LEFT:
            self.position = (mo.vec(self.position) + (velocity*mo.vec(self.right))).tolist()[0]

    def pitch_yaw(self, dx, dy, constrainPitch=True):
        self.yaw += self.sensitivity * dx
        self.pitch += self.sensitivity * dy
        if (constrainPitch):
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.__update_camera_vectors()

    def resize_viewport(self, w, h):
        self.aspect_ratio = w/h

    def set_fow(self, delta):
        self.fow += delta
        if self.fow <= 0:
            self.fow = 1
        if self.fow > 180:
            self.fow = 180

    def __update_camera_vectors(self):
        fx = cos(radians(self.yaw)) * cos(radians(self.pitch))
        fy = sin(radians(self.pitch))
        fz = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.front = mo.normalize([fx,fy,fz]).tolist()[0]
        self.right = mo.normalize(np.cross(mo.vec(self.front), mo.vec(self.world_up))).tolist()[0]
        self.camera_up = mo.normalize(np.cross(mo.vec(self.right), mo.vec(self.front))).tolist()[0]

