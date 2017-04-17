from glumpy import app, gloo, gl, glm
import numpy as np

vertex = """
    uniform mat4 u_model;       // Model matrix (local to world space)
    uniform mat4 u_view;        // View matrix (world to camera space)
    uniform mat4 u_projection;  // Projection matrix (camera to screen)

    attribute vec3 a_position;  // Vertex Position

    void main()
    {
        gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    } """

fragment = """
    void main()
    {
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    } """


cube = gloo.Program(vertex, fragment)
cube["a_position"] = [[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1],
                      [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
                      [1, 1, 1], [1, 1, -1], [1, -1, -1], [1, -1, 1],
                      [-1, 1, 1], [-1, 1, -1], [-1, -1, -1], [-1, -1, 1],
                      [1, 1, 1], [1, 1, -1], [-1, 1, -1], [-1, 1, 1],
                      [1, -1, 1], [1, -1, -1], [-1, -1, -1], [-1, -1, 1],]


# Initiate all three matrix
view = np.eye(4,dtype=np.float32)
model = np.eye(4,dtype=np.float32)
projection = glm.perspective(45.0, 1, 2.0, 100.0)

# Minimize the model, and move the camera-view back
glm.scale(model,0.5,0.5,0.5)
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

