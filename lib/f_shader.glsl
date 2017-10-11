#version 330

in vec3 vColor;

out vec4 oColor;

void main() {
    oColor = vec4(vColor.r, vColor.g, vColor.b, 1.0f);
}