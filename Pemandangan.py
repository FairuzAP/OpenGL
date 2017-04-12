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
listSun = [[0,0,-9], [200,0,-9], [400,0,-9]]
colorSun = [[255,255,0,255], [255,255,0,192], [255,255,0,16]]

segment = 16
cosr = cos(radians(360/segment))
sinr = sin(radians(360/segment))
i = 1
while i <= segment:
	nextx = (listSun[(i*2)-1][0] * cosr) - (listSun[(i*2)-1][1] * sinr)
	nexty = (listSun[(i*2)-1][0] * sinr) + (listSun[(i*2)-1][1] * cosr)
	listSun.append([nextx, nexty, 0])
	colorSun.append(colorSun[1])
	nextx = (listSun[(i*2)][0] * cosr) - (listSun[(i*2)][1] * sinr)
	nexty = (listSun[(i*2)][0] * sinr) + (listSun[(i*2)][1] * cosr)
	listSun.append([nextx, nexty, 0])
	colorSun.append(colorSun[2])
	i += 1

sun = gloo.Program(vertex, fragment, count=len(listSun))
sun['color'] = colorSun
sun['position'] = listSun
sun['u_trans'] = transMatrix(1/5,3.75,3,0)


# The Hill Model
listHill = [[-400,-300,-8],[400,-300,-8],[-200,-175,-8],[225,-150,-8],[-25,-10,-8],[50,20,-8]]
colorHill = [[0,100,0,255], [25,100,0,255], [50,205,50,255], [154,205,50,255], [124,252,0,255], [200,255,47,255]]

hill = gloo.Program(vertex, fragment, count=len(listHill))
hill['color'] = colorHill
hill['position'] = listHill
hill['u_trans'] = transMatrix(3/4,-1,-1/3,0)
hill2 = gloo.Program(vertex, fragment, count=len(listHill))
hill2['color'] = colorHill
hill2['position'] = listHill
hill2['u_trans'] = transMatrix(1,0,0,0)


# Create a window with a valid GL context
window = app.Window(800,600)

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
	window.clear()
	sky.draw(gl.GL_POLYGON)
	sun.draw(gl.GL_POLYGON)
	hill.draw(gl.GL_TRIANGLE_STRIP)
	hill2.draw(gl.GL_TRIANGLE_STRIP)

# Run the app
app.run()

