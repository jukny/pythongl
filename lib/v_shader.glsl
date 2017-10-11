#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 inColor;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 transform;

out vec2 TexCoord;
out vec3 vColor;

void main() {
    gl_Position = vec4(position, 1.0f);
    vColor = vec3(inColor);
    TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}