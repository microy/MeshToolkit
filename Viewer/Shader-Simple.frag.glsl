#version 330 core

in vec3 in_Color;
out vec4 out_Color;

void main()
{
	out_Color = vec4( in_Color, 1.0 );
}
