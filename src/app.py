'''
from dmcview.cli import main 

if __name__ == "__main__":
   main()

   The above for docker not working as per below message. This is special for GUI app (pyside6)
   which needs native linux Graphical library to work. 

   Error:
   Attaching to server-1
server-1  | Y
server-1  | qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
server-1  | qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
server-1  | This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
server-1  | 
server-1  | Available platform plugins are: wayland-egl, vnc, linuxfb, vkkhrdisplay, eglfs, minimal, offscreen, minimalegl, xcb, wayland.

see issue: https://forum.qt.io/topic/154450/build-a-docker-for-pyside6 

'''
# disabled the docker execution put a simple print 
print('Disabled the docker start due to below error:')
print ("ERROR START:")
print("qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.")
print("qt.qpa.plugin: Could not load the Qt platform plugin \"xcb\" in \"\" even though it was found.")
print("This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.")
print("Available platform plugins are: wayland-egl, vnc, linuxfb, vkkhrdisplay, eglfs, minimal, offscreen, minimalegl, xcb, wayland.")
print("Error End:")

