from pyglet.gl import *

from ctypes import *
import yaml
from array import array
import pyglet.image as pyi
import Matrixop as mo


class Mesh:
    def __init__(self, source, camera, shader):
        """

        :rtype: object
        """
        try:
            with open(source, 'r') as m:
                data = yaml.load(m)
                self.vertices = array('f', data['vertices'])
                self.material = data['material']
                self.texture_id = self.__setup_texture(data['material']['diffuse'])
        except IOError as ie:
            print(ie)
            exit(1)
        except yaml.YAMLError as ye:
            print(ye)
            exit(1)
        self.VAO = GLuint(0)
        self.VBO = GLuint(0)
        self.rotation =  mo.rotate(0, mo.vec([0,0,0]))
        self.translation = mo.translate([0, 0, 0])
        self.scale = mo.scale([1, 1, 1])


    def draw(self, shader, camera):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        view = self.translation * self.rotation * self.scale
        shader.uniform_matrix('model', self.translation * self.rotation * self.scale)
        shader.uniform_matrix('view', camera.viewMatrix())
        shader.uniform_matrix('projection', camera.projection())
        glDrawArrays(GL_TRIANGLES, 0, GLint(int(len(self.vertices)/8)))

    def to_string(self):
        return self.vertices.tostring()

    def vertice_byte_size(self):
        return len(self.vertices) * sizeof(GLfloat)

    def transform(self, da, v, type):
        pass


    def __setup_texture(self, texture_file):
        self.texture_image = pyi.load(texture_file).get_texture()

        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return self.texture_image.id

