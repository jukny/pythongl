#version 330

out vec4 oTexture;

in vec3 vColor;
in vec2 TexCoord;

uniform sampler2D vTexture;

void main() {
    oTexture = texture(vTexture, TexCoord) * vec4(vColor, 1.0f);
}