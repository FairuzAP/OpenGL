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


# Upload data into GPU
listHead = [[-1.015,36.871], [3.979,37.855], [5.539,34.606], [10.711,31.199], [12.241,30.883], [13.337,32.007], [11.813,33.732], [9.101,39.207], [8.528,42.404], [8.809,45.242],
			[9.445,48.649], [7.747,53.191], [8.141,55.137], [8.268,57.48], [7.611,56.837], [7.561,49.884], [8.467,47.643], [7.784,46.787], [6.189,43.444], [5.284,46.047],
			[5.539,49.162], [3.437,50.96], [0.068,57.598], [-0.959,58.65], [-0.176,55.794], [0.686,53.017], [3.46,48.382], [3.07,43.963], [-5.286,41.142]]

listBody = [[-5.286,41.142], [-11.16,35.709], [-12.444,32.444], [-13.436,24.339], [-9.244,-2.792], [-5.077,-9.932], [1.213,-18.718], [3.608,-21.781], [7.646,-27.231], 
			[11.907,-38.046], [10.351,-45.197], [4.812,-51.485], [2.335,-52.907], [-3.949,-54.551], [-11.409,-52.394], [-12.234,-51.789], [-13.696,-50.393], [-15.43,-47.837], 
			[-16.685,-42.984], [-12.485,-36.397], [-10.187,-34.276], [-16.389,-37.302], [-18.765,-44.934], [-13.938,-54.534], [-9.316,-57.06], [-3.299,-58.32], [-0.671,-58.32], 
			[3.156,-57.627], [15.053,-48.6], [17.513,-43.132], [18.796,-35.056], [11.829,-16.029], [7.61,-9.851], [6.319,-5.944], [8.268,22.519], [7.13,23.98], [-0.849,29.388], 
			[-3.039,32.656], [-1.015,36.871]]

# Build the program and corresponding buffers
head = gloo.Program(vertex, fragment, count=len(listHead))
body = gloo.Program(vertex, fragment, count=len(listBody))

head['v_color'] = (1,1,1,1)
head['position'] = listHead
head['u_trans'] = transMatrix(1/100,0,0,0)

body['v_color'] = (1,1,1,1)
body['position'] = listBody
body['u_trans'] = transMatrix(1/100,0,0,0)

# Create a window with a valid GL context
window = app.Window()

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    head.draw(gl.GL_LINE_LOOP)
    body.draw(gl.GL_LINE_LOOP)

# Run the app
app.run()
