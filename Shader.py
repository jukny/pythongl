from pyglet.gl import *
from ctypes import *
import numpy as np


class Shader:
    def __init__(self, shaders):
        with open(shaders['vertex_shader']) as glsl:
            try:
                self.vertex_shader_code = [glsl.read().encode('utf-8')]
            except IOError as ie:
                print(ie)
                exit(1)
        with open(shaders['fragment_shader']) as glsl:
            try:
                self.fragment_shader_code = [glsl.read().encode('utf-8')]
            except IOError as ie:
                print(ie)
        self.handle = glCreateProgram()
        self.linked = False
        self.createShader(self.vertex_shader_code, GL_VERTEX_SHADER)
        self.createShader(self.fragment_shader_code, GL_FRAGMENT_SHADER)
        # self.createShader(geom, GL_GEOMETRY_SHADER)

        self.link()

    def init_shader(self, s, v):
        VAO = GLuint()
        VBO = GLuint()
        # VAO
        glGenVertexArrays(1, VAO)

        # VBO
        glGenBuffers(1, VBO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     s,
                     v,
                     GL_STATIC_DRAW)

        glBindVertexArray(VAO)
        # Position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 0)
        glEnableVertexAttribArray(0)
        # Normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 3 * sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        # Texture coordinates
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), 6 * sizeof(GLfloat))
        glEnableVertexAttribArray(2)


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
            self.link()

    def link(self):
        glLinkProgram(self.handle)
        temp = c_int(0)
        glGetProgramiv(self.handle, GL_LINK_STATUS, byref(temp))
        if not temp:
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH, byref(temp))
            buffer = create_string_buffer(temp.value)
            glGetProgramInfoLog(self.handle, temp, None, buffer)
            print(buffer.value)
        else:
            self.linked = True

    def bind(self):
        glUseProgram(self.handle)

    def unbind(self):
        glUseProgram(0)

    def vcl(self, name):
        return glGetUniformLocation(self.handle, name)

    def uniformf(self, name, *values):
        if len(values) in range(1, 5):
            {
                1: glUniform1f,
                2: glUniform2f,
                3: glUniform3f,
                4: glUniform4f
            }[len(values)](glGetUniformLocation(self.handle, create_string_buffer(name.encode('utf-8'))), *values)

    def uniformi(self, name, *values):
        if len(values) in range(1, 5):
            {
                1: glUniform1i,
                2: glUniform2i,
                3: glUniform3i,
                4: glUniform4i
            }[len(values)](glGetUniformLocation(self.handle, name.encode('utf-8')), *values)

    def uniform_matrix(self, name, mat):
        loc = glGetUniformLocation(self.handle, name.encode('utf-8'))
        data_p = mat.flatten().tolist()
        if isinstance(data_p[0], list):
            data_p = data_p[0]
        data_p = (c_float * len(data_p))(*data_p)
        print(name, *data_p)
        glUniformMatrix4fv(loc, 1, False, data_p)
