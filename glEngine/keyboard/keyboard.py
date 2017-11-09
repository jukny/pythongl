import pyglet.clock as clock
from pyglet.window import key


class gl_keyboard(key.KeyStateHandler):

    def __init__(self, bindings):
        super(gl_keyboard, self).__init__()
        clock.schedule(self.handle_keyboard)

    def handle_keyboard(self):
        try:
            s = 60/clock.get_fps()
        except ZeroDivisionError:
            s = 1
        #MESH
        #if self.keyboard[keymap[self.keyboard_bindings['rotate_up']]]:
        #    self.glmesh.rotate_x(s)
        #if self.keyboard[keymap[self.keyboard_bindings['rotate_down']]]:
        #    self.glmesh.rotate_x(-s)
        #if self.keyboard[keymap[self.keyboard_bindings['rotate_left']]]:
        #    self.glmesh.rotate_y(s)
        #if self.keyboard[keymap[self.keyboard_bindings['rotate_right']]]:
        #    self.glmesh.rotate_y(-s)

        #CAMERA
        if self.keyboard[keymap[self.keyboard_bindings['forward']]]:
            self.camera.move(Directions.FORWARD, s)
        if self.keyboard[keymap[self.keyboard_bindings['back']]]:
            self.camera.move(Directions.BACKWARD, s)
        if self.keyboard[keymap[self.keyboard_bindings['strafe_right']]]:
            self.camera.move(Directions.RIGHT, s)
        if self.keyboard[keymap[self.keyboard_bindings['strafe_left']]]:
            self.camera.move(Directions.LEFT, s)

