#version 330 core

in vec2 vert;
in vec2 texCoord;
uniform vec2 position;
uniform vec2 scale;
uniform vec2 screen_size;
uniform float trail_index;
uniform float max_trail_length;

out vec2 uvs;
out float trail_factor;

void main() {
    // Calculate trail size based on position in trail
    float size_factor = (max_trail_length - trail_index) / max_trail_length;
    size_factor = pow(size_factor, 1.5); // Non-linear scaling for better effect

    // Transform vertex position to bullet's world position with scaled size
    vec2 world_pos = vert * (scale * size_factor) + position;

    // Convert to normalized device coordinates
    vec2 ndc = (world_pos / screen_size) * 2.0 - 1.0;
    ndc.y = -ndc.y; // Flip Y coordinate for pygame coordinate system

    uvs = texCoord;
    trail_factor = size_factor;
    gl_Position = vec4(ndc, 0.0, 1.0);
}
