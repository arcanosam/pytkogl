# pytkogl - A pure OpenGL window using Python with TKinter
----------------------------------------------------------

Just Python and it's standard library to build an OpenGL window.

Check my article to more details: [OpenGL in Python with TKinter]

**It's below OpenGL 3.1 programming**

License: [The Code Project Open License (CPOL) 1.02]

[OpenGL in Python with TKinter]: http://www.codeproject.com/Articles/1073475/OpenGL-in-Python-with-TKinter

[The Code Project Open License (CPOL) 1.02]: http://www.codeproject.com/info/cpol10.aspx

# Updates
---------

2017-04-02:
* Add branch: gui_objloader_branch
    * Added obj file loader
    * Added some GUI funcionality
    * Both couldn't 100% functional, probably have some bugs
        * The OBJ filer loader don't work for all OBJ files cases because some OBJ files export complex models a bit differently from low-poly models
    * Folders:
        * rsc/ - OBJ files
        * rsc/Texture - MTL files

* Remember check your path for your OpenGL Shared Object library
* Check MTL path on your OBJ files
* Thanks for Alexandr Lazov for ask to help which make do it this and sorry not complete this
    * Their links to obj loader:
        * [PyGAME ObjLoader]
        * [PyOpenGL tutorial(russian)]

[PyGAME ObjLoader]:https://www.pygame.org/wiki/OBJFileLoader
[PyOpenGL tutorial(russian)]:https://habrahabr.ru/post/246625/
