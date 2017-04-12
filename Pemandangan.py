from glumpy import app, gloo, gl
from math import cos, sin, radians
import triangle
import numpy as np

vertex = """  
  uniform mat4 u_trans;         // Translation/Scaling/Rotate matrix
  attribute vec4 color;
  attribute vec3 position;
  varying vec4 v_color;
  void main()
  {
	gl_Position = u_trans * vec4(position.x/400, position.y/300, position.z/10, 1.0);
	v_color = vec4(color/255);
  } """

fragment = """
  varying vec4 v_color;
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

	
# The Sky Model
listSky = [[400,300,-10],[-400,300,-10],[-400,-300,-10],[400,-300,-10]]
colorSky = [[25,25,112,255], [25,25,112,255], [135,206,235,255], [135,206,235,255]]

sky = gloo.Program(vertex, fragment, count=len(listSky))
sky['color'] = colorSky
sky['position'] = listSky
sky['u_trans'] = transMatrix(1,0,0,0)


# The Sun Model
listSun = [[0,0,-9], [400,0,-9]]
colorSun = [[255,255,0,255], [255,255,0,16]]

segment = 72
cosr = cos(radians(360/segment))
sinr = sin(radians(360/segment))
i = 1
while i <= segment:
	nextx = (listSun[i][0] * cosr) - (listSun[i][1] * sinr)
	nexty = (listSun[i][0] * sinr) + (listSun[i][1] * cosr)
	listSun.append([nextx, nexty, 0])
	colorSun.append(colorSun[1])
	i += 1

sun = gloo.Program(vertex, fragment, count=len(listSun))
sun['color'] = colorSun
sun['position'] = listSun
sun['u_trans'] = transMatrix(1/5,3.75,3,0)


# Create a window with a valid GL context
window = app.Window(800,600)

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
	window.clear()
	sky.draw(gl.GL_POLYGON)
	sun.draw(gl.GL_POLYGON)

# Run the app
app.run()

