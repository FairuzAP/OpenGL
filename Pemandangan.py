from glumpy import app, gloo, gl
from math import cos, sin, radians
from random import randint
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

# The Rainbow Model
listRainbow = []
colorRainbow = []

degreeIncrement = 5;
currentDegree = 0;
radius = 400;
radiusDecrement = 15;
collorPallete = [[201,23,11,255],[201,118,11,200],[189,201,11,255],[11,201,23,200],[11,189,201,255],[23,11,201,200],[118,11,201,255],[255,255,255,0]]
i = 0

while (i<7):
	colhi = collorPallete[i]
	collow = collorPallete[i+1]
	nextx = cos(radians(currentDegree))
	nexty = sin(radians(currentDegree))
	listRainbow.append([nextx*radius,nexty*radius,-2])
	colorRainbow.append(colhi)
	if (currentDegree==0):
		while (currentDegree < 180):
			nextx = cos(radians(currentDegree))
			nexty = sin(radians(currentDegree))
			listRainbow.append([nextx*(radius-radiusDecrement),nexty*(radius-radiusDecrement),-2])

			currentDegree += degreeIncrement
			nextx = cos(radians(currentDegree))
			nexty = sin(radians(currentDegree))		
			listRainbow.append([nextx*radius,nexty*radius,-2])

			colorRainbow.extend([collow,colhi])
	else:	
		while (currentDegree > 0):
			nextx = cos(radians(currentDegree))
			nexty = sin(radians(currentDegree))
			listRainbow.append([nextx*(radius-radiusDecrement),nexty*(radius-radiusDecrement),-2])

			currentDegree -= degreeIncrement
			nextx = cos(radians(currentDegree))
			nexty = sin(radians(currentDegree))
			listRainbow.append([nextx*radius,nexty*radius,-1])

			colorRainbow.extend([collow,colhi])

	listRainbow.append([nextx*(radius-radiusDecrement),nexty*(radius-radiusDecrement),-2])
	colorRainbow.append(collow)
	radius = radius-radiusDecrement
	i += 1
	
rainbow = gloo.Program(vertex, fragment, count=len(listRainbow))
rainbow["color"] = colorRainbow
rainbow["position"] = listRainbow
rainbow["u_trans"] = transMatrix(1,0,-1,0)

# The Circle Model
def drawCircle(posX,posY,radius):
        triangleAmount=20
        listCircle=[[posX,posY,-2]]
        colorCircle=[[240,240,240,255]]
        twicePi = 6.28318530718
        for i in range (0,triangleAmount+1):
                listCircle.append([posX + (radius * cos(i * twicePi / 20)), posY + (radius * sin(i * twicePi / triangleAmount)),-2])
                colorCircle.append([240,240,240,255])
        Circle = gloo.Program(vertex, fragment, count=len(listCircle))
        Circle['color'] = colorCircle
        Circle['position'] = listCircle
        Circle['u_trans'] = transMatrix(3/4,-1,-1/3,0)
        Circle.draw(gl.GL_TRIANGLE_FAN)

# The Tree Model
listTrunk = [[-325,-300,-1],[-400,-300,-1],[-333,-233,-1],[-400,84,-1],[-340,84,-1],[-375,175,-1],[-325,200,-1],[-300,300,-1]]
colorTrunk = []
for i in range (0, len(listTrunk)):
	colorTrunk.append([152,101,50,255])
trunk = gloo.Program(vertex, fragment, count=len(listTrunk))
trunk['color'] = colorTrunk
trunk['position'] = listTrunk
trunk['u_trans'] = transMatrix(1,0,0,0)
def drawBush(posX,posY,radius):
        triangleAmount=40
        listBush=[[posX,posY,-2]]
        colorBush=[[255,183,187,255]]
        twicePi = 6.28318530718
        for i in range (0,triangleAmount+1):
                listBush.append([posX + (radius * cos(i * twicePi / triangleAmount)), posY + (radius * sin(i * twicePi / triangleAmount)),-2])
                colorBush.append([255,183,187,255])
        Bush = gloo.Program(vertex, fragment, count=len(listBush))
        Bush['color'] = colorBush
        Bush['position'] = listBush
        Bush['u_trans'] = transMatrix(1,0,0,0)
        Bush.draw(gl.GL_TRIANGLE_FAN)

# The Leaf Model
def drawLeaf(posX,posY,rot):
	listLeaf = [[posX+10,posY+20,-1],[posX+10,posY+10,-1],[posX,posY+10,-1],[posX,posY,-1]]
	colorLeaf = []
	for i in range (0, len(listLeaf)):
		colorLeaf.append([255,183,187,255])
	leaf = gloo.Program(vertex, fragment, count=len(listLeaf))
	leaf['color'] = colorLeaf
	leaf['position'] = listLeaf
	leaf['u_trans'] = transMatrix(1,0,0,rot)
	leaf.draw(gl.GL_TRIANGLE_STRIP)
	

# Create a window with a valid GL context
window = app.Window(800,600)

leafPos = []
for i in range (1,75):
	leafPos.append([randint(-400,400),randint(-300,300),randint(0,360)])
	
# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
	window.clear()
	sky.draw(gl.GL_POLYGON)
	rainbow.draw(gl.GL_TRIANGLE_STRIP)
	sun.draw(gl.GL_POLYGON)
	hill.draw(gl.GL_TRIANGLE_STRIP)
	hill2.draw(gl.GL_TRIANGLE_STRIP)
	
	#Mickey Mouse Cloudy thing
	#drawCircle(100,300,40)
	#drawCircle(140,370,40)
	#drawCircle(80,360,45)
	drawCircle(100,380,45)
	drawCircle(50,350,45)
	drawCircle(140,320,45)
	drawCircle(90,330,40)
	drawCircle(160,380,35)
	drawCircle(180,350,35)


	#Some Other Cloud
	drawCircle(400,350,45)
	drawCircle(440,395,40)
	drawCircle(450,315,50)
	drawCircle(500,330,35)
	drawCircle(500,380,47)
	drawCircle(550,320,42)
	drawCircle(550,410,33)
	drawCircle(580,370,37)
	
	#A Random Tree
	trunk.draw(gl.GL_TRIANGLE_STRIP)
	drawBush(-300,300,90)
	drawBush(-320,250,80)
	drawBush(-320,250,80)
	drawBush(-400,300,100)
	drawBush(-400,200,50)
	drawBush(-360,190,50)
	drawBush(-400,160,50)
	
	for i in range (0,74):
		drawLeaf(leafPos[i][0],leafPos[i][1],leafPos[i][2])



# Run the app
app.run()

