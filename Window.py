import pyglet
import yaml

from Shader import *


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
        with open(self.configuration['OpenGL']['vertex_shader']) as glsl:
            try:
                self.vertex_shader_code = glsl.read().encode('utf-8')
            except IOError as ie:
                print(ie)
                exit(1)
        with open(self.configuration['OpenGL']['fragment_shader']) as glsl:
            try:
                self.fragment_shader_code = glsl.read().encode('utf-8')
            except IOError as ie:
                print(ie)
        self.shader = Shader([self.vertex_shader_code], [self.fragment_shader_code])

    def on_key_press(self, symbol, mods):
        if symbol == pyglet.window.key.ESCAPE:
            self.close()


if __name__ == '__main__':
    win = ()
    pyglet.app.run()
