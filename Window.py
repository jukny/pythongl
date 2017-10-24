import pyglet
import yaml

from Shader import *
from Mesh import Mesh
from pyglet.clock import schedule_interval, get_fps
from pyglet.window import key
from Camera import Camera
import Matrixop as mo

class GWindow (pyglet.window.Window):

    """Main class. Handling window creation based on config

    """

    def __init__(self):
        with open('conf/config.yml') as cstream:
            try:
                self.configuration = yaml.load(cstream)
            except yaml.YAMLError as exc:
                print (exc)
                exit(1)
            except IOError as ie:
                print(ie)
                exit(1)
        super(GWindow, self).__init__()
        self.set_size(self.configuration['window']['width'], self.configuration['window']['height'])
        self.set_fullscreen(self.configuration['window']['fullscreen'])
        self.set_caption(self.configuration['window']['caption'])
        self.light = self.configuration['Light']
        self.set_mouse_cursor()
        self.shader = Shader(self.configuration['Shaders'])
        self.camera = Camera(self.configuration['Camera'])
        self.mesh = Mesh('shapes/triangle.yml', self.camera, self.shader)
        self.__init_shader()
        glEnable(GL_DEPTH_TEST)
        schedule_interval(self.update, get_fps())

    def on_key_press(self, symbol, mods):
        if symbol == key.ESCAPE:
            self.close()

    def on_draw(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.shader.bind()
        self.shader.uniformi('material.diffuse', c_int(0))
        self.shader.uniformf('light.position', *self.light['position'])
        self.shader.uniformf('light.ambient', *self.light['ambient'])
        self.shader.uniformf('light.diffuse', *self.light['diffuse'])
        self.shader.uniformf('light.specular', *self.light['specular'])
        self.mesh.draw(self.shader, self.camera)
        self.shader.unbind()

    def update(self, dt):
       pass
       #self.mesh.transform(dt, get_fps())

    def __init_shader(self):
        #VAO
        glGenVertexArrays(1,self.mesh.VAO)
        glBindVertexArray(self.mesh.VAO)

        #VBO
        glGenBuffers(1, self.mesh.VBO)
        glBindBuffer(GL_ARRAY_BUFFER, self.mesh.VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     self.mesh.vertice_byte_size(),
                     self.mesh.to_string(),
                     GL_STATIC_DRAW)

        #Position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 0)
        glEnableVertexAttribArray(0)
        # Normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 3 * sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        # Texture coordinates
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 6 * sizeof(GLfloat))
        glEnableVertexAttribArray(2)


if __name__ == '__main__':
    win = GWindow()
    pyglet.app.run()
