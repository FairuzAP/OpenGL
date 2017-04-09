from glumpy import app, gloo, gl
from math import cos, sin, radians
import triangle
import numpy as np

vertex = """
  
  uniform mat4 u_trans;         // Translation/Scaling/Rotate matrix
  uniform vec4 v_color;
  attribute vec2 position;
  
  void main()
  {
    gl_Position = u_trans * vec4(position, 0.0, 1.0);
  } """

fragment = """
  uniform vec4 v_color;
  void main()
  {
      gl_FragColor = v_color;
  } """

def transMatrix(scale, dx, dy, rot):
	cosr = cos(radians(rot))
	sinr = sin(radians(rot))
	mScale = np.matrix([[scale,0,0,0],[0,scale,0,0],[0,0,scale,0],[0,0,0,1]])
	mTrans = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[dx,dy,0,1]])
	mRotat = np.matrix([[cosr,-sinr,0,0],[sinr,cosr,0,0],[0,0,1,0],[0,0,0,1]])
	return mTrans * mRotat * mScale

# Build the program and corresponding buffers (with 4 vertices)
head = gloo.Program(vertex, fragment, count=29)

# Upload data into GPU
list = [[-1.015,36.871], [3.979,37.855], [5.539,34.606], [10.711,31.199], [12.241,30.883], [13.337,32.007], [11.813,33.732], [9.101,39.207], [8.528,42.404], [8.809,45.242],
		[9.445,48.649], [7.747,53.191], [8.141,55.137], [8.268,57.48], [7.611,56.837], [7.561,49.884], [8.467,47.643], [7.784,46.787], [6.189,43.444], [5.284,46.047],
		[5.539,49.162], [3.437,50.96], [0.068,57.598], [-0.959,58.65], [-0.176,55.794], [0.686,53.017], [3.46,48.382], [3.07,43.963], [-5.286,41.142]]
triangles = triangle.triangulate({'vertices' : list})
print(triangles)

head['v_color'] = (1,1,1,1)
head['position'] = list
head['u_trans'] = transMatrix(1/17,0,-45,0)

# Create a window with a valid GL context
window = app.Window()

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    head.draw(gl.GL_LINE_LOOP)

# Run the app
app.run()
