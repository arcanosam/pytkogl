import sys

if sys.platform.startswith('win32'):

    from ctypes import WinDLL

    _libGlu = WinDLL('glu32')

elif sys.platform.startswith('linux'):

    from ctypes import cdll

    # Shared library path hardcode for Xubuntu 16.04

    _libGlu = cdll.LoadLibrary('/usr/lib/i386-linux-gnu/mesa/libGLU.so.1')

else:
    raise NotImplementedError

from tko.ogl_hdr import GLdouble

gluPerspective = _libGlu.gluPerspective
gluPerspective.restype = None
gluPerspective.argtypes = [GLdouble, GLdouble, GLdouble, GLdouble]