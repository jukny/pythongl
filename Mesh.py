from pyglet.gl import *
from ctypes import *

class Mesh:

    def __init__(self, vertices=[], indices=[], textcoords=[]):
        """

        :rtype: object
        """
        self.vertices = vertices
        self.indices = indices
        self.textcoords = textcoords
        self._VAO = GLuint(0)
        self._VBO = GLuint(0)
        self._EBO = GLuint(0)
        self._setupMesh()



    def draw(self, shader):
        pass

    def _setupMesh(self):
        glGenVertexArrays(1, self._VAO)
        glBindVertexArray(self._VAO)
        glGenBuffers(1, self._VBO)
        glBindBuffer(GL_ARRAY_BUFFER, self._VBO)
        glGenBuffers(1, self._EBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._EBO)

if __name__ == '__main__':
    m = Mesh()
