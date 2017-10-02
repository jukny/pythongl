import yaml
from pyglet.gl import *

class Shapes:

    def __init__(self, shape):
        try:
            with open('shapes/'+shape+'.yml') as yml_shape:
                self.shape = yaml.load(yml_shape)
        except yaml.YAMLError as ye:
            print (ye)
            exit(1)
        except IOError as ie:
            print (ie)
            exit(1)
        self.name = self.shape['name']

        self.vbo = GLuint(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, )

    def draw(self):



