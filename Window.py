import pyglet
import yaml
from Shader import *
from Mesh import Mesh
import pyglet.clock as clock
from pyglet.window import key
from Camera import Camera, Direction
from keymap import keymap


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
        self.set_size(self.configuration['window']['width'], self.configuration['window']['height'])
        self.w_fullscreen = self.configuration['window']['fullscreen']
        self.set_fullscreen(self.w_fullscreen)
        self.set_caption(self.configuration['window']['caption'])
        self.light = self.configuration['Light']

        self.set_mouse_visible(False)
        self.mouse_position = [self.configuration['window']['width']/2,
                               self.configuration['window']['height']/2]

        self.keyboard = key.KeyStateHandler()
        self.keyboard_bindings = self.configuration['Keyboard']
        self.push_handlers(self.keyboard)

        self.camera = Camera()

        self.shader = Shader(self.configuration['Shaders'])

        self.mesh = Mesh('shapes/cube.yml')

        self.shader.init_shader(self.mesh.vertice_byte_size(), self.mesh.to_string())
        glEnable(GL_DEPTH_TEST)

        clock.schedule(self.handle_keyboard)

    def on_key_press(self, symbol, mods):
        if symbol == keymap[self.keyboard_bindings['quit']]:
            self.close()
        if symbol == keymap[self.keyboard_bindings['toggle_fullscreen']]:
            self.toggle_fullscreen()

    def on_mouse_motion(self, x, y, dx, dy):
        self.camera.pitch_yaw(0,dy)
        pass

    def on_draw(self):
        #self.handle_keyboard()
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.shader.bind()
        self.shader.uniformi('material.diffuse', c_int(0))
        #self.shader.uniformi('material.specular', self.mesh.material['specular'])
        self.shader.uniformf('light.position', *self.light['position'])
        self.shader.uniformf('light.ambient', *self.light['ambient'])
        self.shader.uniformf('light.diffuse', *self.light['diffuse'])
        self.shader.uniformf('light.specular', *self.light['specular'])
        self.shader.uniformf('viewPos', *self.camera.position)
        self.mesh.draw(self.shader, self.camera)
        self.shader.unbind()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        self.camera.resize_viewport(width, height)
        return pyglet.event.EVENT_HANDLED


    def handle_keyboard(self, a):
        try:
            s = 60/clock.get_fps()
        except ZeroDivisionError:
            s = 1
        #MESH
        if self.keyboard[keymap[self.keyboard_bindings['rotate_up']]]:
            self.mesh.rotate_x(s)
        if self.keyboard[keymap[self.keyboard_bindings['rotate_down']]]:
            self.mesh.rotate_x(-s)
        if self.keyboard[keymap[self.keyboard_bindings['rotate_left']]]:
            self.mesh.rotate_y(s)
        if self.keyboard[keymap[self.keyboard_bindings['rotate_right']]]:
            self.mesh.rotate_y(-s)

        #CAMERA
        if self.keyboard[keymap[self.keyboard_bindings['forward']]]:
            self.camera.move(Direction.FORWARD, s)
        if self.keyboard[keymap[self.keyboard_bindings['back']]]:
            self.camera.move(Direction.BACKWARD, s)
        if self.keyboard[keymap[self.keyboard_bindings['strafe_right']]]:
            self.camera.move(Direction.RIGHT, s)
        if self.keyboard[keymap[self.keyboard_bindings['strafe_left']]]:
            self.camera.move(Direction.LEFT, s)

    def toggle_fullscreen(self):
        self.w_fullscreen = not self.w_fullscreen
        self.set_fullscreen(self.w_fullscreen)

if __name__ == '__main__':
    win = GWindow()
    pyglet.app.run()
