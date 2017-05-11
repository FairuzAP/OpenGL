from glumpy import app, gloo, gl, glm, data
import numpy as np
from os.path import abspath


vertex = """
    uniform mat4 u_model;       // Model matrix (local to world space)
    uniform mat4 u_view;        // View matrix (world to camera space)
    uniform mat4 u_projection;  // Projection matrix (camera to screen)

    attribute vec3 a_position;  // Vertex Position
    attribute vec3 a_normal;    // Vertex normal

    varying vec3   v_texcoord;  // Interpolated fragment texture coordinates (out)
    varying vec3   v_position;  // Interpolated position (out)
    varying vec3   v_normal;    // Interpolated normal (out)

    void main()
    {
        v_texcoord  = a_position;
		v_normal = a_normal;
		v_position = a_position;
        gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    } """

fragment = """
    uniform mat4      u_model;           // Model matrix
    uniform mat4      u_view;            // View matrix
    uniform mat4      u_normal;          // Normal matrix
    uniform vec3      u_light_position;  // Light position
    uniform vec3      u_light_intensity; // Light intensity
    uniform samplerCube u_texture;       // Texture

    varying vec3      v_normal;          // Interpolated normal (out)
    varying vec3      v_position;        // Interpolated position (out)
    varying vec3      v_texcoord;        // Interpolated fragment texture coordinates (out)

    void main()
    {
        // Calculate normal in world coordinates
        vec3 normal = normalize(u_normal * vec4(v_normal,1.0)).xyz;
        // Calculate the location of this fragment (pixel) in world coordinates
        vec3 position = vec3(u_view*u_model * vec4(v_position, 1));
        // Calculate the vector from this pixels surface to the light source
        vec3 surfaceToLight = u_light_position - position;
        // Calculate the cosine of the angle of incidence (brightness)
        float brightness = dot(normal, surfaceToLight) /
                          (length(surfaceToLight) * length(normal));
        brightness = max(min(brightness,1.0),0.0);
        // Calculate final color of the pixel, based on:
        // 1. The angle of incidence: brightness
        // 2. The color/intensities of the light: light.intensities
        // 3. The texture and texture coord: texture(tex, fragTexCoord)
        // Get texture color

        vec4 t_color = textureCube(u_texture, v_texcoord);
        gl_FragColor = t_color * (0.1 + 0.9*brightness * vec4(u_light_intensity, 1));
    } """

fragment_plain = """
    uniform samplerCube u_texture;  // Texture

    varying vec3      v_normal;     // Interpolated normal (in)
    varying vec3      v_position;   // Interpolated position (in)
    varying vec3      v_texcoord;   // Interpolated fragment texture coordinates (in)

    void main()
    {
        vec4 t_color = textureCube(u_texture, v_texcoord);
        gl_FragColor = t_color;
    } """


# Initialize the array of vertex, and normal faces
vertex_pos = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1], [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
face_norm = [[0, 0, 1], [1, 0, 0], [0, 1, 0],[-1, 0, 1], [0, -1, 0], [0, 0, -1]]

face_vertex_idx = [0, 1, 2, 3,  0, 3, 4, 5,   0, 5, 6, 1,  1, 6, 7, 2,  7, 4, 3, 2,   4, 7, 6, 5]
face_normal_idx = [0, 0, 0, 0,  1, 1, 1, 1,   2, 2, 2, 2, 3, 3, 3, 3,  4, 4, 4, 4,   5, 5, 5, 5]

# Upload the texture data
texture = np.zeros((6,1024,1024,3),dtype=np.float32).view(gloo.TextureCube)
texture.interpolation = gl.GL_LINEAR
texture[2] = data.get(abspath("Gauden/Top.jpg"))/255.
texture[3] = data.get(abspath("Gauden/Bottom.jpg"))/255.
texture[0] = data.get(abspath("Gauden/Right.jpg"))/255.
texture[1] = data.get(abspath("Gauden/Left.jpg"))/255.
texture[4] = data.get(abspath("Gauden/Front3.jpg"))/255.
texture[5] = data.get(abspath("Gauden/Back.jpg"))/255.

# Bind the vertex object to the cube program
cube = gloo.Program(vertex, fragment)
cube["a_position"] = [vertex_pos[i] for i in face_vertex_idx]
cube['a_normal'] = [face_norm[i] for i in face_normal_idx]
cube['u_texture'] = texture

# Initiate all three matrix
view = np.eye(4,dtype=np.float32)
model = np.eye(4,dtype=np.float32)
projection = glm.perspective(45.0, 1, 2.0, 100.0)

# Minimize the model, and move the camera-view back
glm.scale(model,0.5,1,0.1)
glm.translate(view, 0,0,-5)

# Pass all the matrix to the model
cube['u_model'] = model
cube['u_view'] = view
cube['u_projection'] = projection
cube["u_light_position"] = 0,0,-4
cube["u_light_intensity"] = 2,2,2

# Initiaze the window
phi = 0.5
theta = 0.1
kappa = 1
window = app.Window(800,600)


@window.event
def on_resize(width, height):
   global projection

   ratio = width / float(height)
   projection = glm.perspective(45.0, ratio, 2.0, 100.0)
   cube['u_projection'] = projection


@window.event
def on_draw(dt):
    global phi, theta, model

    window.clear()
    cube.draw(gl.GL_QUADS)

    # Make cube rotate
    #view = cube['u_view'].reshape(4,4)
    #model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 1, 0)
    glm.rotate(model, phi, 0.3, 0, 0)
    glm.rotate(model, kappa, 0, 0.7, 0)
    cube['u_model'] = model
    cube['u_normal'] = np.array(np.matrix(np.dot(view, model)).I.T)


@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    #gl.glDisable(gl.GL_BLEND)

app.run()

