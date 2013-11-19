#version 330 core

layout (location = 0) in vec4 Vertex;
layout (location = 1) in vec3 Normal;

uniform mat4 MVP_Matrix;
uniform mat3 Normal_Matrix;

out vec4 FragColor;

void main( void ) {

	vec3 Norm = normalize( Normal_Matrix * Normal );
	vec3 LightDir = vec3( 0.0, 0.0, 1.0 );

	float Dot = max( 0.0, dot(Norm, LightDir) ); 

	FragColor.xyz = vec3( 0.6, 0.6, 0.6 ) * Dot;
	FragColor.a = 1.0;

	gl_Position = MVP_Matrix * Vertex;
}

