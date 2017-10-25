import pyglet
import yaml
from Shader import *
from Mesh import Mesh
from pyglet.clock import schedule_interval, get_fps
from pyglet.window import key
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
        super(GWindow, self).__init__(resizable=True)
        self.set_size(self.configuration['window']['resolution']['width'], self.configuration['window']['resolution']['height'])
        self.set_fullscreen(self.configuration['window']['fullscreen'])
        self.set_caption(self.configuration['window']['caption'])
        self.light = self.configuration['Light']
        self.set_mouse_cursor()
        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.camera = Camera(self.configuration['Camera'])

        self.shader = Shader(self.configuration['Shaders'])
        self.mesh = Mesh('shapes/cube.yml')
        self.shader.init_shader(self.mesh.vertice_byte_size(), self.mesh.to_string())
        glEnable(GL_DEPTH_TEST)
        schedule_interval(self.update, get_fps())

    def on_key_press(self, symbol, mods):
        if symbol == key.ESCAPE:
            self.close()
        if symbol == key.LEFT:
            self.mesh.rotate_y(-1.0)
        if symbol == key.RIGHT:
            self.mesh.rotate_y(1.0)
        if symbol == key.UP:
            self.mesh.rotate_x(1.0)
        if symbol == key.DOWN:
            self.mesh.rotate_x(-1.0)
        if symbol == key.W:
            self.camera.move_z(-0.01)
        if symbol == key.S:
            self.camera.move_z(0.01)
        if symbol == key.A:
            self.camera.move_x(-0.01)
        if symbol == key.D:
            self.camera.move_x(0.01)

    def on_draw(self):
        self.handle_keyboard()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.shader.bind()
        self.shader.uniformi('material.diffuse', c_int(0))
        self.shader.uniformf('light.position', *self.light['position'])
        self.shader.uniformf('light.ambient', *self.light['ambient'])
        self.shader.uniformf('light.diffuse', *self.light['diffuse'])
        self.shader.uniformf('light.specular', *self.light['specular'])
        self.shader.uniformf('viewPos', *self.camera.position)
        self.mesh.draw(self.shader, self.camera)
        self.shader.unbind()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        return pyglet.event.EVENT_HANDLED

    def update(self, dt):
       pass
       #self.mesh.transform(dt, get_fps())

    def handle_keyboard(self):
        pass

if __name__ == '__main__':
    win = GWindow()
    pyglet.app.run()
