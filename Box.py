from glumpy import app, gloo, gl, glm, data
import numpy as np

vertex = """
    uniform mat4 u_model;       // Model matrix (local to world space)
    uniform mat4 u_view;        // View matrix (world to camera space)
    uniform mat4 u_projection;  // Projection matrix (camera to screen)

    attribute vec3 a_position;  // Vertex Position
    attribute vec2 a_texcoord;  // Vertex texture coordinates

    varying vec2   v_texcoord;  // Interpolated fragment texture coordinates (out)

    void main()
    {
        v_texcoord  = a_texcoord;
        gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    } """

fragment = """
    uniform sampler2D u_texture;  // Texture
    varying vec2      v_texcoord; // Interpolated fragment texture coordinates (in)

    void main()
    {
        vec4 t_color = texture2D(u_texture, v_texcoord);
        gl_FragColor = t_color;
    } """


#face_normal = [[0, 0, 1], [1, 0, 0], [0, 1, 0], [-1, 0, 1], [0, -1, 0], [0, 0, -1]]
#face_normal_idx = [0, 0, 0, 0,  1, 1, 1, 1,   2, 2, 2, 2, 3, 3, 3, 3,  4, 4, 4, 4,   5, 5, 5, 5]
#cube['a_normal']   = [face_normal[i] for i in face_normal_idx]

# Initialize the array of vertex object
vertex_pos = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1], [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
texture_coord = [[0, 0], [0, 1], [1, 1], [1, 0]]
face_vertex_idx = [0, 1, 2, 3,  0, 3, 4, 5,   0, 5, 6, 1,  1, 6, 7, 2,  7, 4, 3, 2,   4, 7, 6, 5]
face_texture_idx = [0, 1, 2, 3,  0, 1, 2, 3,   0, 1, 2, 3,  3, 2, 1, 0,  0, 1, 2, 3,   0, 1, 2, 3]

# Bind the vertex object to the cube program
cube = gloo.Program(vertex, fragment)
cube["a_position"] = [vertex_pos[i] for i in face_vertex_idx]
cube['a_texcoord'] = [texture_coord[i] for i in face_texture_idx]
cube['u_texture'] = data.get("D:\ITB\Tugas\Grafika\OpenGL\Capture.jpg")


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


# Initiaze the window
phi = 1
theta = 1
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
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['u_model'] = model


@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


app.run()

