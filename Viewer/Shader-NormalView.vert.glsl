#version 330

layout(location = 0) in vec3 in_Position;
layout(location = 1) in vec3 in_Normal;

out vec4 geom_Position;
out vec4 geom_Normal;

uniform mat4 MVP_Matrix;
uniform float ScaleFactor;


void main()
{
    geom_Position = vec4( in_Position, 1.0 );
    geom_Normal = vec4( in_Normal, 1.0 );
}

