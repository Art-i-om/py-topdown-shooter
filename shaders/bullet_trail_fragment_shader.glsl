#version 330 core

uniform float time;
uniform vec3 bullet_color;
uniform float trail_index;
uniform float max_trail_length;

in vec2 uvs;
in float trail_factor;
out vec4 f_color;

void main() {
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(uvs, center);

    // Create trail opacity based on position in trail - increased base alpha
    float alpha_factor = trail_factor * 0.5; // Increased from 0.8 to 1.2

    // Create a soft circular gradient
    float glow = 1.0 - smoothstep(0.0, 0.5, dist);
    glow = pow(glow, 1.5); // Reduced power for softer falloff

    // Add some energy effect
    float energy = sin(time * 0.1 + trail_index * 0.5) * 0.2 + 0.8;

    // Combine effects
    vec3 final_color = bullet_color * energy;
    float final_alpha = glow * alpha_factor * 0.9; // Increased multiplier from default

    f_color = vec4(final_color, final_alpha);
}
