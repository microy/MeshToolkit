#version 330 core

layout (location = 0) in vec3 in_Position;
layout (location = 1) in vec3 in_Normals;
layout (location = 2) in vec3 in_Color;

uniform mat4 MVP_Matrix;

out vec3 frag_Color;

void main(void)
{
	gl_Position = MVP_Matrix * vec4( in_Position, 1.0 );
	frag_Color = in_Color;
}
