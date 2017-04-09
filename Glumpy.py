from glumpy import app, gloo, gl
import numpy as np
from math import *

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
left_wing = gloo.Program(vertex, fragment, count=4)

# Upload data into GPU
left_wing['v_color'] = (1,1,1,1)
left_wing['position'] = [ (+1,0),   (0,-1),   (-1,0),   (0,+1) ]
left_wing['u_trans'] = transMatrix(1,0,0,45)

# Create a window with a valid GL context
window = app.Window()

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    left_wing.draw(gl.GL_LINE_LOOP)

# Run the app
app.run()
