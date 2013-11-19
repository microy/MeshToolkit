#version 330 core

layout (location = 0) in vec4 vVertex;
layout (location = 1) in vec3 vNormal;

uniform mat4 MVP_Matrix;
uniform mat3 Normal_Matrix;

out vec4 vFragColor;

void main(void) {

	vec3 vNorm = normalize(Normal_Matrix * vNormal);
	vec3 vLightDir = vec3(0.0, 0.0, 1.0);

	float fDot = max(0.0, dot(vNorm, vLightDir)); 

	vFragColor.xyz = vec3( 0.6, 0.6, 0.6 ) * fDot;
	vFragColor.a = 1.0;

	gl_Position = MVP_Matrix * vVertex;
}

