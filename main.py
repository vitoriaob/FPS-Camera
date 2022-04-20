import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

width, height = 1020, 720
lastX, lastY = width / 2, height / 2
xoffset = 0
yoffset = 0
first_mouse = True
command_V = False
glCamAngx = 3
glCamAngy = 3
gCamZoom = 1
call = ''
move = False
left = 0
top = 0

def Panning():
    m = (GLfloat * 16)()
    mtx = glGetFloatv(GL_MODELVIEW_MATRIX, m)
    glTranslatef(-left*m[0],-left*m[4],-left*m[8])
    glTranslatef(top*m[1],top*m[5],top*m[9])
  
def Orbit():
    m = (GLfloat * 16)()
    mtx = glGetFloatv(GL_MODELVIEW_MATRIX, m)
    glRotatef(glCamAngx,0,1,0)    
    glRotatef(glCamAngy,m[0],m[4],m[8])
  
def Zoom():
    global gCamZoom
    m = (GLfloat * 16)()
    mvm = glGetFloatv(GL_MODELVIEW_MATRIX, m)
    glTranslate(gCamZoom*m[2],gCamZoom*m[6],gCamZoom*m[10])
    

def render():
    global command_V, glCamAngx, glCamAngy, left, top
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLoadIdentity()   
    gluPerspective(90,1,1,25)
    glMatrixMode(GL_MODELVIEW)   
    
    gluLookAt(1,1,1, 0,0,0, 0,1,0)
      
    if(command_V):
        glCamAngx = 3
        glCamAngy = 3
        left = 0
        top = 0
        gCamZoom = 1
        command_V = False
    
    Orbit()
    Zoom()
    Panning()
    
    glColor3ub(255,255,255) 
    drawUnitCube()
    drawFrame()
    drawPlane()
       


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([10.,0.,0.]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,10.,0.]))
    glColor3ub(0,0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0,0.,10.]))
    glEnd()

def drawPlane():
    glBegin(GL_LINES)
    glColor3ub(255,0, 255)
    for i in np.arange(-100, 100, 0.5):
        glVertex3fv(np.array([i,0.,0.]))
        glVertex3fv(np.array([i,0.,100.]))
    for i in np.arange(-100, 100, 0.5):
        glVertex3fv(np.array([i,0.,0.]))
        glVertex3fv(np.array([i,0.,-100.]))
    for i in np.arange(-100, 100, 0.5):
        glVertex3fv(np.array([0.,0.,i]))
        glVertex3fv(np.array([100,0.,i]))
    for i in np.arange(-100, 100, 0.5):
        glVertex3fv(np.array([0.,0.,i]))
        glVertex3fv(np.array([-100,0.,i]))
    glEnd()
    
def drawUnitCube():
    glBegin(GL_LINES)
    vertices= ((0.5, 0., -0.5),(0.5, 1., -0.5),(-0.5, 1., -0.5),(-0.5, 0., -0.5),(0.5, 0., 0.5),(0.5, 1., 0.5),(-0.5,0., 0.5),(-0.5, 1., 0.5))
    edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
    for e in edges:
        for vertex in e:
            glVertex3fv(vertices[vertex])
    glEnd()

def mouse_look_callback(window, xpos, ypos):
    global glCamAngx, glCamAngy, xoffset, yoffset, left, right, bottom, top, lastY, lastX

    if call == 'left' and move == True :       
        xoffset = xpos - lastX
        yoffset = lastY - ypos
        
        glCamAngx += xoffset*0.4
        glCamAngy += yoffset*0.4    
                                 
    elif call == 'right' and move == True :
        xoffset = xpos - lastX
        yoffset = lastY - ypos

        left -= xoffset*0.006
        top += yoffset*0.006
        
    lastX = xpos
    lastY = ypos
    

def mouse_enter_callback(window, enter):
    global first_mouse

    if enter:
        first_mouse = False
    else:
        first_mouse = True

def scroll_callback(window, xoffsett, yoffsett):

    global gCamZoom
    
    gCamZoom+= yoffsett*0.3

 
def key_callback(window, key, scancode, action, mods):
    global command_V
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_V:
            command_V = True
        

           
def button_callback(window, button, action, mod):
    global call, move, orbit_flag, pan_flag
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            call = 'left'
            move = True
        elif action==glfw.RELEASE:
            move = False


    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            call = 'right'
            move = True
        elif action==glfw.RELEASE:
            move = False
  
def main():
    if not glfw.init():
        return
    window = glfw.create_window(1020,720,"3D Viewer", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    glfw.set_cursor_enter_callback(window, mouse_enter_callback)
    glfw.set_cursor_pos_callback(window, mouse_look_callback)
    glfw.make_context_current(window)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
         
        glfw.poll_events() 
        render()    
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
