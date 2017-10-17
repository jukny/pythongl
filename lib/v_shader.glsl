#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec4 inColor;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 TexCoord;
out vec4 vColor;

void main() {
    gl_Position = view * model * vec4(position, 1.0f);
    //gl_Position = projection * vec4(position, 1.0f);
    vColor = inColor;
    TexCoord = aTexCoord;
}