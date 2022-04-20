# FPS-Camera
Blender alike FPS camera in Python using OpenGL 

1.	Code structure and how to run
The code structure starts with the initialization of the global variables, followed by the implementation of each method to zoom, rotate and pan, then we have render method and all the drawing methods. After that we will have all the mouse/key callback functions and finally the main method.
Since the methods are all organized in the same file, to run the entire program you should run “main.py” file normally.

2.	Methods
The logic I used to implement all this methods was using the glFloatv() method to get the Modelview matrix and using this matrix position vectors I was able to do the operations of the camera properly.
The coordinates from the camera (u,v,w ) are given by:
Right – u vector m[0], m[4], m[8]
Up – v vector m[1], m[5], m[9]
Back – w vector m[2], m[6], m[10]
The 3x3 R-U-B matrix is a rotation matrix.
Now, the methods implemented were:

i)	Pan()  - For panning the object
 I used glGetFloatv() method to get the camera position matrix in space, and after that I used glTranslate() to translate the camera and object by multiplying the v, u vectors of the camera by ‘left’ and ‘top’ variables that are actualized in the mouse callback function.

ii)	Orbit() – For rotating the object
Again, I used glGetFloat() to get modelview matrix and I rotated with angles (glCamAngx, glCamAngy) modified in the mouse callback method, around the y-axis and around the vector u given by the rotation matrix. 

iii)	Zoom() – For zooming in-out
For zooming, I used a variable to modify the zoom factor in the mouse wheel callback and multiplied the ‘w’ vector of the camera coordinates inside glTranslate() method.

iv)	Callback methods:

Mouse_look_callback: get the mouse position and pass it to the parameter to modify angle for rotation and positions for panning.
Mouse_enter_callback: check if the mouse is in the window or not.
Scroll_callback: gets the camera zoom factor multiplied by the mouse wheel movement.
Key_callback: check if key V is pressed for toggling the view
Button_callback: auxiliates in the “dragging” movement of the mouse.

v)	Toggle by pressing key ‘v’
In render function I check if V command is true, and then reset the variables to their initial value


3.	References

https://3dengine.org/Right-up-back_from_modelview/
https://www.glfw.org/docs/3.3/input_guide.html
https://docs.microsoft.com/en-us/windows/win32/opengl/glgetfloatv
https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glGet.xml

