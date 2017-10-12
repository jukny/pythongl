#version 330

out vec4 oTexture;

in vec4 vColor;
in vec2 TexCoord;

uniform sampler2D vTexture;

void main() {
    oTexture = texture(vTexture, TexCoord) * vColor;
}