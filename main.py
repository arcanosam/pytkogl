"""entry point for Tkinter Window with OpenGL]
"""

from tkinter import Tk, YES, BOTH, LEFT, RIGHT, W, StringVar
from tkinter.ttk import Frame, Entry, Label, Button


from tko.tk_win import TkOglWin

from tko.ogl_hdr import PGLfloat, \
                        GL_AMBIENT, GL_COLOR_BUFFER_BIT, GL_COLOR_MATERIAL, GL_DEPTH_TEST, \
                        GL_DEPTH_BUFFER_BIT, GL_DIFFUSE, GL_LIGHT0, GL_LIGHTING, GL_MODELVIEW, \
                        GL_POSITION, GL_PROJECTION, GL_SMOOTH, glCallList, glClear, glClearColor, glEnable, \
                        glLightfv, glLoadIdentity, glMatrixMode, glRotatef, glShadeModel, glTranslatef, glViewport

from tko.glu_hdr import gluPerspective

from objloader import ObjLoader


class AppOgl(TkOglWin):

    def __init__(self, parent, *args, **kwargs):

        super(AppOgl,self).__init__(parent,*args,**kwargs)

        self.fovy = StringVar(parent, value='90.0')
        self.znear = StringVar(parent, value='1.0')
        self.zfar = StringVar(parent, value='100.0')

        self.light_pos = StringVar(parent, value='-40, 200, 100, 0.0')
        self.light_amb = StringVar(parent, value='0.2, 0.2, 0.2, 1.0')
        self.light_dif = StringVar(parent, value='0.5, 0.5, 0.5, 1.0')


    def add_gui(self):

        self.frm_gui = Frame(self.parent)

        self.frm_gui.pack(side=RIGHT)

        Label(self.frm_gui, text='Fovy:').pack(anchor=W)
        self.edt_fovy = Entry(self.frm_gui, textvariable=self.fovy)
        self.edt_fovy.pack()

        Label(self.frm_gui, text='zNear:').pack(anchor=W)
        self.edt_znear = Entry(self.frm_gui, textvariable=self.znear)
        self.edt_znear.pack()

        Label(self.frm_gui, text='zFar:').pack(anchor=W)
        self.edt_zfar = Entry(self.frm_gui, textvariable=self.zfar)
        self.edt_zfar.pack()

        Label(self.frm_gui, text='Light position:').pack(anchor=W)
        self.edt_lightpos = Entry(self.frm_gui, textvariable=self.light_pos)
        self.edt_lightpos.pack()

        Label(self.frm_gui, text='Light Ambient:').pack(anchor=W)
        self.edt_lightamb = Entry(self.frm_gui, textvariable=self.light_amb)
        self.edt_lightamb.pack()

        Label(self.frm_gui, text='Light Diffuse:').pack(anchor=W)
        self.edt_lightdif = Entry(self.frm_gui, textvariable=self.light_dif)
        self.edt_lightdif.pack()

        self.edt_lightpos.bind('<Return>', self.on_resize)
        self.edt_lightamb.bind('<Return>', self.on_resize)
        self.edt_lightdif.bind('<Return>', self.on_resize)
        self.edt_fovy.bind('<Return>', self.on_resize)
        self.edt_znear.bind('<Return>', self.on_resize)
        self.edt_zfar.bind('<Return>', self.on_resize)

    def on_resize(self, event):

        w = self.winfo_width()
        h = self.winfo_height()

        if event is not None:
            if str(event.type) == 'Configure' :
                w = event.width
                h = event.height

        self.setup_light()

        self.setup_view(w,h)

    def pre_glcommands(self):

        self.set_ortho_view()

        self.setup_light()

        self.setup_view(self.winfo_width(), float(self.winfo_height()))

        self.obj_model = ObjLoader('rsc/trader_barman.obj')

    def render_scene(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        # RENDER OBJECT
        glTranslatef(0, -1, -1.5)

        glRotatef(0, 1, 0, 0)

        glRotatef(0, 0, 1, 0)

        glCallList(self.obj_model.gl_list)

    def set_ortho_view(self):
        glClearColor(0, 0, 0, 0)

        self.on_resize(None)

    def setup_light(self):

        glLightfv(GL_LIGHT0, GL_POSITION, PGLfloat(*list(float(vlr) for vlr in self.light_pos.get().split(','))))

        glLightfv(GL_LIGHT0, GL_AMBIENT, PGLfloat(*list(float(vlr) for vlr in self.light_amb.get().split(','))))

        glLightfv(GL_LIGHT0, GL_DIFFUSE, PGLfloat())

        glEnable(GL_LIGHT0)

        glEnable(GL_LIGHTING)

    def setup_view(self, w, h):


        glEnable(GL_COLOR_MATERIAL)

        glEnable(GL_DEPTH_TEST)

        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()

        gluPerspective(float(self.fovy.get()), w / h, float(self.znear.get()), float(self.zfar.get()))

        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, w, int(h))

        glMatrixMode(GL_MODELVIEW)


if __name__ == '__main__':
    root = Tk()

    root.minsize(640,480)

    app = AppOgl(root)

    app.pack(side=LEFT, fill=BOTH, expand=YES)

    app.mainloop()