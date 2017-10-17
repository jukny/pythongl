from pyglet.gl import *

from ctypes import *
import yaml
from array import array
import pyglet.image as pyi
import numpy as np
import Matrixop as mo


class Mesh:

    def __init__(self, source, camera, shader):
        """

        :rtype: object
        """
        try:
            with open(source, 'r') as m:
                data = yaml.load(m)
                if data['color_index'] == "RGBA":
                    self.color_index = 4
                else:
                    self.color_index = 3
                self.vertices = self.__convert_to_single_array(data['vertices'],
                                                               data['colors'],
                                                               data['tex_coords'])
                print(self.vertices)
                self.indices = array('I', data['indices'])
                if 'texture_file' in data:
                    self.__setup_texture(data['texture_file'])
        except IOError as ie:
            print(ie)
            exit(1)
        except yaml.YAMLError as ye:
            print(ye)
            exit(1)
        self._VAO = GLuint(0)
        self._VBO = GLuint(0)
        self._EBO = GLuint(0)
        self.camera = camera
        self.shader = shader
        self._setupMesh()
        self.total_time = 0


    def __convert_to_single_array(self, v, c, t=[]):
        result = []
        color_index, texture_index = 0,0
        for i in range(0, len(v), 3):
            result.extend(v[i:i + 3])
            if color_index >= (len(c)):
                color_index = 0
            result.extend([ float(col)/255 for col in c[color_index:color_index + self.color_index]])
            color_index += self.color_index
            if texture_index >= (len(t)):
                texture_index = 0
            result.extend(t[texture_index:texture_index + 2])
            texture_index += 2
        return array('f', result)

    def draw(self):
        self.shader.uniform_matrix('model', mo.rotx(10))
        self.shader.uniform_matrix('view', self.camera.target)
        self.shader.uniform_matrix('projection', self.camera.perspective)
        glDrawElements(GL_TRIANGLES,
                       len(self.indices),
                       GL_UNSIGNED_INT,
                       None)

    def _setupMesh(self):
        # VAO
        glGenVertexArrays(1, self._VAO)
        glBindVertexArray(self._VAO)

        #VBO
        glGenBuffers(1, self._VBO)
        glBindBuffer(GL_ARRAY_BUFFER, self._VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vertices)*sizeof(GLfloat),
                     self.vertices.tostring(),
                     GL_STATIC_DRAW)

        #EBO
        glGenBuffers(1, self._EBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.indices)*sizeof(GLfloat),
                     self.indices.tostring(),
                     GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 9 * sizeof(GLfloat), 0)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 9 * sizeof(GLfloat), 3*sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 9 * sizeof(GLfloat), (3+self.color_index) * sizeof(GLfloat))
        glEnableVertexAttribArray(2)



    def __setup_texture(self, texture_file):
        self.texture_image = pyi.load(texture_file).get_texture()
        glBindTexture(self.texture_image.target, self.texture_image.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

if __name__ == '__main__':
    m = Mesh('shapes/triangle.yml')

