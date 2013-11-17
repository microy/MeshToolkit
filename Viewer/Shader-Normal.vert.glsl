#version 330 core

layout (location = 0) in vec3 in_Position;
layout (location = 1) in vec3 in_Normal;
layout (location = 2) in vec3 in_Color;

// Output data ; will be interpolated for each fragment.
out vec3 frag_Color;
out vec3 Position_worldspace;
out vec3 Normal_cameraspace;
out vec3 EyeDirection_cameraspace;
out vec3 LightDirection_cameraspace;

// Values that stay constant for the whole mesh.
uniform mat4 MVP_Matrix;
uniform mat4 View_Matrix;
uniform mat4 Model_Matrix;
uniform vec3 LightPosition_worldspace;


void main(void)
{
	// Output position of the vertex, in clip space : MVP * position
	gl_Position = MVP_Matrix * vec4( in_Position, 1.0 );

	// Position of the vertex, in worldspace : M * position
	Position_worldspace = (Model_Matrix * vec4(in_Position,1)).xyz;

	// Vector that goes from the vertex to the camera, in camera space.
	// In camera space, the camera is at the origin (0,0,0).
	vec3 vertexPosition_cameraspace = ( View_Matrix * Model_Matrix * vec4(in_Position,1)).xyz;
	EyeDirection_cameraspace = vec3(0,0,0) - vertexPosition_cameraspace;

	// Vector that goes from the vertex to the light, in camera space. M is ommited because it's identity.
	vec3 LightPosition_cameraspace = ( View_Matrix * vec4(LightPosition_worldspace,1)).xyz;
	LightDirection_cameraspace = LightPosition_cameraspace + EyeDirection_cameraspace;

	// Normal of the the vertex, in camera space
	// Only correct if ModelMatrix does not scale the model ! Use its inverse transpose if not.
	Normal_cameraspace = ( View_Matrix * Model_Matrix * vec4(in_Normal,0)).xyz;

	// Send the color
	frag_Color = in_Color;
}

