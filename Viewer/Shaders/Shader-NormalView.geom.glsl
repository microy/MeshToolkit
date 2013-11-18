#version 330
layout(triangles) in;
layout(line_strip, max_vertices = 6) out;

in vec4 geom_Position[3];
in vec4 geom_Normal[3];

out vec4 frag_Color;

uniform mat4 MVP_Matrix;
uniform float ScaleFactor;

void main()
{
    const vec4 green = vec4(0.0f, 1.0f, 0.0f, 1.0f);
    const vec4 blue = vec4(0.0f, 0.0f, 1.0f, 1.0f);

    for (int i = 0; i < 3; i++)
    {
        gl_Position = MVP_Matrix * geom_Position[i];
        frag_Color = green;
        EmitVertex();

        gl_Position = MVP_Matrix * (geom_Position[i] + geom_Normal[i] * ScaleFactor);
        frag_Color = blue;
        EmitVertex();

        EndPrimitive();
    }
}
