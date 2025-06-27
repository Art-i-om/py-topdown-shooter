#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    // CRT curvature
    vec2 uv = uvs;
    uv = uv * 2.0 - 1.0; // [-1,1] range
    float curve = 0.1;
    uv.x *= 1.0 + curve * pow(uv.y, 2.0);
    uv.y *= 1.0 + curve * pow(uv.x, 2.0);
    uv = (uv + 1.0) * 0.5; // back to [0,1]

    // RGB color offset (chromatic aberration)
    float offset = 0.002;
    float r = texture(tex, uv + vec2(offset, 0.0)).r;
    float g = texture(tex, uv).g;
    float b = texture(tex, uv - vec2(offset, 0.0)).b;
    vec3 color = vec3(r, g, b);

    // Add some scanlines effect using time
    float scanline = sin(uv.y * 800.0) * 0.04;
    color -= scanline;

    // Add some noise using time
    float noise = (fract(sin(dot(uv + time * 0.001, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) * 0.05;
    color += noise;

    // Vignette effect
    float vignette = distance(uv, vec2(0.5));
    vignette = 1.0 - vignette * 0.5;
    color *= vignette;

    f_color = vec4(color, 1.0);
}
