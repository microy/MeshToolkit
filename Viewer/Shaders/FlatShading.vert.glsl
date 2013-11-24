#version 330 core

layout (location = 0) in vec4 Vertex;
layout (location = 1) in vec3 Normal;
layout (location = 2) in vec3 Color;

uniform mat4 MVP_Matrix;
uniform mat3 Normal_Matrix;
uniform int color_enabled = 0;
uniform int hidden_lines = 0;

flat out vec4 FragColor;

void main( void ) {

	vec3 Norm = normalize( Normal_Matrix * Normal );
	vec3 LightDir = vec3( 0.0, 0.0, 1.0 );

	float Dot = max( 0.0, dot(Norm, LightDir) ); 

	if( hidden_lines == 1 ) {
		FragColor.xyz = vec3( 1.0, 1.0, 1.0 );
	}	
	else if( color_enabled == 0 ) {
		FragColor.xyz = vec3( 0.7, 0.7, 0.7 ) * Dot;
	}
	else {
		FragColor.xyz = Color * Dot;
	}

	FragColor.a = 1.0;

	gl_Position = MVP_Matrix * Vertex;
}

