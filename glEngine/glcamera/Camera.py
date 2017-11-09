from  math import cos, sin, radians

import numpy as np
import yaml

from glEngine.matrix import Matrixop as mo


class Directions:
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
        self.position =       mo.vec(self.config['position']) #Startup [0,0,10]
        self.target =         mo.vec(self.config['target'])   #Startup [0,0,0]
        self.front =          mo.vec([0,0,-1])
        self.camera_up =      mo.vec([0,1,0])
        self.right =          mo.vec([1,0,0])
        self.yaw =            -90.0
        self.pitch =          0
        self.world_up =       mo.vec([0,1,0])
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
        return mo.lookat(self.position, self.target, self.camera_up)

    def move(self, direction, delta):
        velocity = self.keyboard_speed * delta
        if direction == Directions.FORWARD:
            self.position = self.position + velocity*self.front
            self.target = self.target + velocity*self.front
        if direction == Directions.BACKWARD:
            self.position = self.position - velocity*self.front
            self.target = self.target - velocity * self.front
        if direction == Directions.RIGHT:
            self.position = self.position - velocity*self.right
            self.target = self.target - velocity*self.right
        if direction == Directions.LEFT:
            self.position = self.position + velocity*self.right
            self.target = self.target + velocity * self.right

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

    def get_position(self):
        return self.position.tolist()[0]

    def __update_camera_vectors(self):
        fx = cos(radians(self.yaw)) * cos(radians(self.pitch))
        if np.isclose(fx,0):
            fx = 0
        fy = sin(radians(self.pitch))
        if np.isclose(fy,0):
            fy = 0
        fz = sin(radians(self.yaw)) * cos(radians(self.pitch))
        if np.isclose(fz, 0):
            fz = 0
        self.front = mo.normalize(mo.vec([fx,fy,fz]))
        self.right = mo.normalize(np.cross(self.front, self.world_up))
        self.camera_up = mo.normalize(np.cross(self.right, self.front))

