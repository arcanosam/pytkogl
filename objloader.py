""" obj file loader and MTL helper
"""

from PIL import Image

from tko.ogl_hdr import GLfloat, GLuint, \
                        GL_CCW, GL_COMPILE, GL_LINEAR, GL_POLYGON, GL_RGBA, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, \
                        GL_TEXTURE_MIN_FILTER, GL_UNSIGNED_BYTE, \
                        glBegin, glBindTexture, glColor3f, glDisable, glEnable, glEnd, glEndList, glFrontFace, \
                        glGenLists, glGenTextures, glNewList, glNormal3f, glTexImage2D, glTexCoord2f, \
                        glTexParameteri, glVertex3f



def mtl_loader(filename):
    """loads mtl texture helper"""

    contents = {}
    mtl = None

    for line in open('rsc/'+filename, "r"):

        if line.startswith('#'):
            continue

        values = line.split()

        if not values:
            continue

        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}

        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")

        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]

            tga_tex = Image.open('rsc/'+mtl['map_Kd']).transpose( Image.FLIP_TOP_BOTTOM )
            tga_img = tga_tex.tobytes()

            ix, iy = tga_tex.size

            mtl['texture_Kd'] = GLuint(1)

            glGenTextures(1, mtl['texture_Kd'])

            texid = mtl['texture_Kd']

            glBindTexture(GL_TEXTURE_2D, texid)

            glTexParameteri(
                GL_TEXTURE_2D,
                GL_TEXTURE_MIN_FILTER,
                GL_LINEAR
            )

            glTexParameteri(
                GL_TEXTURE_2D,
                GL_TEXTURE_MAG_FILTER,
                GL_LINEAR
            )

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                ix,
                iy,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                tga_img
            )

        else:
            try:
                mtl[values[0]] = list(
                    map(
                        GLfloat,
                        list(
                            map(float, values[1:])
                        )
                    )
                )

            except ValueError as e:
                print(e)

    return contents


class ObjLoader:

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None

        for line in open(filename, "r"):

            if line.startswith('#'):
                continue

            values = line.split()

            if not values:
                continue

            if values[0] == 'v':
                v = list(
                    map(
                        GLfloat,
                        list(
                            map(float, values[1:4])
                        )
                    )
                )

                if swapyz:
                    v = v[0], v[2], v[1]

                self.vertices.append(v)

            elif values[0] == 'vn':
                v = list(
                    map(
                        GLfloat,
                        list(
                            map(float, values[1:4])
                        )
                    )
                )

                if swapyz:
                    v = v[0], v[2], v[1]

                self.normals.append(v)

            elif values[0] == 'vt':
                self.texcoords.append(
                    list(
                        map(
                            GLfloat,
                            list(
                                map(float, values[1:3])
                            )
                        )
                    )
                )

            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'mtllib':
                self.mtl = mtl_loader(values[1])

             # continue
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []

                for v in values[1:]:

                    w = v.split('/')

                    face.append(
                        int(w[0])
                    )

                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(
                            int(w[1])
                        )

                    else:
                        texcoords.append(0)

                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(
                            int(w[2])
                        )

                    else:
                        norms.append(0)

                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)

        glNewList(self.gl_list, GL_COMPILE)

        glEnable(GL_TEXTURE_2D)

        glFrontFace(GL_CCW)

        for face in self.faces:
            vertices, normals, texture_coords, material = face

            try:
                mtl = self.mtl[material]
            except AttributeError as e:
                mtl = None

            if mtl:
                if 'texture_Kd' in mtl:
                    # use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])

                else:
                    # just use diffuse colour
                    glColor3f(
                        mtl['Kd'][0],
                        mtl['Kd'][1],
                        mtl['Kd'][2]
                    )

            glBegin(GL_POLYGON)

            for i in range(len(vertices)):

                if normals[i] > 0:
                    normal_vl = self.normals[normals[i] - 1]
                    glNormal3f(normal_vl[0], normal_vl[1], normal_vl[2])

                if texture_coords[i] > 0:
                    tex_coord_vl = self.texcoords[texture_coords[i] - 1]
                    glTexCoord2f(tex_coord_vl[0],tex_coord_vl[1])

                # glColor3f(1, 0, 1)
                vertex_vl = self.vertices[vertices[i] - 1]
                glVertex3f(vertex_vl[0],vertex_vl[1], vertex_vl[2])

            glEnd()

        glDisable(GL_TEXTURE_2D)

        glEndList()
