import pyglet
import yaml

from Shader import *
from Mesh import Mesh
from pyglet.clock import schedule_interval, get_fps
from Camera import Camera

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
        self.set_mouse_cursor()
        self.shader = Shader(self.configuration['Shaders'])
        self.camera = Camera(self.configuration['Camera'])
        self.mesh = Mesh('shapes/triangle.yml', self.camera, self.shader)
        schedule_interval(self.update, get_fps())

    def on_key_press(self, symbol, mods):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.shader.bind()
        self.mesh.draw(self.shader)
        self.shader.unbind()

    def update(self, dt):
       self.mesh.transform(dt, get_fps())

if __name__ == '__main__':
    win = GWindow()
    pyglet.app.run()
