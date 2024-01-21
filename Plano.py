import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

import sys
sys.path.append('..')
from Cubo import Cubo
from Montacargas import Montacargas

screen_width = 1000
screen_height = 700
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200

pygame.init()

montacargas = []
nMontacargas = 5

# cybertroca = Montacargas()

cubos = []
nCubos = 15

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)
    
def drawMainCube():
    glPushMatrix()
    glTranslatef(0, 15, 0)
    glScaled(15, 15, 15)
    glColor3f(1.0, 1.0, 1.0)
    
    points = np.array([[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]])
    
    glBegin(GL_QUADS)
    glVertex3fv(points[0])
    glVertex3fv(points[1])
    glVertex3fv(points[2])
    glVertex3fv(points[3])
    glEnd()
    glBegin(GL_QUADS)
    glVertex3fv(points[4])
    glVertex3fv(points[5])
    glVertex3fv(points[6])
    glVertex3fv(points[7])
    glEnd()
    glBegin(GL_QUADS)
    glVertex3fv(points[0])
    glVertex3fv(points[1])
    glVertex3fv(points[5])
    glVertex3fv(points[4])
    glEnd()
    glBegin(GL_QUADS)
    glVertex3fv(points[1])
    glVertex3fv(points[2])
    glVertex3fv(points[6])
    glVertex3fv(points[5])
    glEnd()
    glBegin(GL_QUADS)
    glVertex3fv(points[2])
    glVertex3fv(points[3])
    glVertex3fv(points[7])
    glVertex3fv(points[6])
    glEnd()
    glBegin(GL_QUADS)
    glVertex3fv(points[3])
    glVertex3fv(points[0])
    glVertex3fv(points[4])
    glVertex3fv(points[7])
    glEnd()
    glPopMatrix()
    
def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    
    loadImage()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for i in range(nCubos):
        cubos.append(Cubo(DimBoard, [5,5,5], [0.34, 0.19, 0.1], False))

    for i in range(nMontacargas):
        montacargas.append(Montacargas(dim=DimBoard, 
                                       vel=1.0,
                                       scale=5,
                                       cubos=cubos))
    
def loadImage():
    img = pygame.image.load("./Texturas/asfalto.jpg").convert()
    textureData = pygame.image.tostring(img, "RGB", 1)
    image_width, image_height = img.get_rect().size
    bgImgGL = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bgImgGL)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width, image_height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    glGenerateMipmap(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, bgImgGL)

def drawFloor():
    glEnable(GL_TEXTURE_2D)
    glColor3f(0.65, 0.65, 0.65)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glTexCoord2f(0, 1)
    glVertex3d(-DimBoard, 0, DimBoard)
    glTexCoord2f(1, 1)
    glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(1, 0)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    
def display():  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    
    drawFloor()
    drawMainCube()
    
    for obj in cubos:
        obj.draw()

    for cybertroca in montacargas:
        cybertroca.drawTruck()
        cybertroca.update()
    
done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()