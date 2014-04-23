#version 330 core

layout (location = 0) in vec4 Vertex;
layout (location = 1) in vec4 Color;

out vec4 FragColor;

void main(void) {
        gl_Position = Vertex;
        FragColor = Color;
}
