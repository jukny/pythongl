from pyglet.gl import *
from ctypes import *


class Shader:
    def __init__(self, vert=[], frag=[], geom=[]):
        self.handle = glCreateProgram()
        self.linked = False
        self.createShader(vert, GL_VERTEX_SHADER)
        self.createShader(frag, GL_FRAGMENT_SHADER)
        #self.createShader(geom, GL_GEOMETRY_SHADER)

        self.link()

    def createShader(self, strings, type):
        count = len(strings)
        if count < 1:
            return
        shader = glCreateShader(type)
        src = (c_char_p * count)(*strings)
        glShaderSource(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
        glCompileShader(shader)

        temp = c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(temp))
        if not temp:
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(temp))
            buffer = create_string_buffer(temp.value)
            glGetShaderInfoLog(shader, temp, None, buffer)
            print(buffer.value)
        else:
            glAttachShader(self.handle, shader)

    def link(self):
        glLinkProgram(self.handle)
        temp = c_int(0)
        glGetProgramiv(self.handle, GL_LINK_STATUS, byref(temp))
        if not temp:
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH,  byref(temp))
            buffer = create_string_buffer(temp.value)
            glGetProgramInfoLog(self.handle, temp, None, buffer)
            print (buffer.value)
        else:
            self.linked = True

    def bind(self):
        glUseProgram(self.handle)

    def unbind(self):
        glUseProgram(0)

    def vcl(self, name):
        return glGetUniformLocation(self.handle, name)

    def uniformf(self, name, *values):
        if len(values) in range(1,5):
            {
                1: glUniform1f,
                2: glUniform2f,
                3: glUniform3f,
                4: glUniform4f
            }[len(values)](glGetUniformLocation(self.handle, create_string_buffer(name.encode('utf-8'))), *values)

    def uniformi(self, name, *values):
        if len(values) in range(1,5):
            {
                1: glUniform1i,
                2: glUniform2i,
                3: glUniform3i,
                4: glUniform4i
            }[len(values)](glGetUniformLocation(self.handle, name), *values)

    def uniform_matrix(self, name, mat):
        loc = glGetUniformLocation(self.handle, name.encode('utf-8'))
        glUniformMatrix4fv(loc, 1, False, (c_float * 16)(*mat))