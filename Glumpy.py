from glumpy import app, gloo, gl
import numpy

# Create a window with a valid GL context
window = app.Window()

vertex = """
  uniform float scale;
  uniform float theta;
  attribute vec2 position;
  attribute vec4 color;
  varying vec4 v_color;
  void main()
  {
    float ct = cos(theta);
    float st = sin(theta);
    float x = scale* (position.x*ct - position.y*st);
    float y = scale* (position.x*st + position.y*ct);
    gl_Position = vec4(x, y, 0.0, 1.0);
    v_color = color;
  } """

fragment = """
  varying vec4 v_color;
  void main()
  {
      gl_FragColor = v_color;
  } """

# Build the program and corresponding buffers (with 4 vertices)
quad = gloo.Program(vertex, fragment, count=4)

# Upload data into GPU
quad['color'] = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
quad['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1) ]
quad['scale'] = 1
quad['theta'] = 0

# Tell glumpy what needs to be done at each redraw
time = 0.0
@window.event
def on_draw(dt):
    global time

    time += dt
    window.clear()
    quad['scale'] = numpy.cos(time)
    quad['theta'] = time
    quad.draw(gl.GL_TRIANGLE_STRIP)

# Run the app
app.run()
