#version 330 core

in vec2 vert;
in vec2 texCoord;
uniform vec2 position;
uniform vec2 scale;
uniform vec2 screen_size;

out vec2 uvs;

void main() {
    // Transform vertex position to bullet's world position
    vec2 world_pos = vert * scale + position;

    // Convert to normalized device coordinates
    vec2 ndc = (world_pos / screen_size) * 2.0 - 1.0;
    ndc.y = -ndc.y; // Flip Y coordinate for pygame coordinate system

    uvs = texCoord;
    gl_Position = vec4(ndc, 0.0, 1.0);
}
