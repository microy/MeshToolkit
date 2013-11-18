#version 330 core

layout (location = 0) in vec3 in_Position;

uniform mat4 MVP_Matrix;

void main(void)
{
	gl_Position = MVP_Matrix * vec4( in_Position, 1.0 );
}
