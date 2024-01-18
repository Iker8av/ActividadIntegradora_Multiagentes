import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Montacargas:
    def __init__(self):
        self.x = 0
        self.y = 1
        self.z = 0
        self.width = 5
        self.height = 2
        self.depth = 5

    def drawRectangle(self, x, y, z, width, height, depth):
        glColor3f(0.925, 0.19, 0.03)
        glBegin(GL_QUADS)
        # Bottom face
        glVertex3f(x, y, z)
        glVertex3f(x + width, y, z)
        glVertex3f(x + width, y + height, z)
        glVertex3f(x, y + height, z)

        # Top face
        glVertex3f(x, y, z + depth)
        glVertex3f(x + width, y, z + depth)
        glVertex3f(x + width, y + height, z + depth)
        glVertex3f(x, y + height, z + depth)

        # Front face
        glVertex3f(x, y, z)
        glVertex3f(x + width, y, z)
        glVertex3f(x + width, y, z + depth)
        glVertex3f(x, y, z + depth)

        # Back face
        glVertex3f(x, y + height, z)
        glVertex3f(x + width, y + height, z)
        glVertex3f(x + width, y + height, z + depth)
        glVertex3f(x, y + height, z + depth)

        # Left face
        glVertex3f(x, y, z)
        glVertex3f(x, y + height, z)
        glVertex3f(x, y + height, z + depth)
        glVertex3f(x, y, z + depth)

        # Right face
        glVertex3f(x + width, y, z)
        glVertex3f(x + width, y + height, z)
        glVertex3f(x + width, y + height, z + depth)
        glVertex3f(x + width, y, z + depth)
        glEnd()
        
    def drawCylinder(self, x, y, z, radius, height, orientation, slices=30):
        slices = int(slices)
        glBegin(GL_QUAD_STRIP)
        glColor3f(0.0, 0.0, 0.0)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices

            if orientation == 'x':
                dx, dy, dz = 0, radius * math.cos(angle), radius * math.sin(angle)
                glVertex3f(x + dx, y + dy, z + dz)
                glVertex3f(x + dx + height, y + dy, z + dz)
            elif orientation == 'y':
                dx, dy, dz = radius * math.cos(angle), 0, radius * math.sin(angle)
                glVertex3f(x + dx, y + dy, z + dz)
                glVertex3f(x + dx, y + dy + height, z + dz)
            elif orientation == 'z':
                dx, dy, dz = radius * math.cos(angle), radius * math.sin(angle), 0
                glVertex3f(x + dx, y + dy, z + dz)
                glVertex3f(x + dx, y + dy, z + dz + height)
            else:
                raise ValueError("Invalid orientation. Use 'x', 'y', or 'z'.")
        glEnd()            

        # Draw the top and bottom faces
        glBegin(GL_POLYGON)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices

            if orientation == 'x':
                dx, dy, dz = 0, radius * math.cos(angle), radius * math.sin(angle)
            elif orientation == 'y':
                dx, dy, dz = radius * math.cos(angle), 0, radius * math.sin(angle)
            elif orientation == 'z':
                dx, dy, dz = radius * math.cos(angle), radius * math.sin(angle), 0

            glVertex3f(x + dx, y + dy, z + dz)
        glEnd()

        glBegin(GL_POLYGON)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices

            if orientation == 'x':
                dx, dy, dz = 0, radius * math.cos(angle), radius * math.sin(angle)
                glVertex3f(x + dx + height, y + dy, z + dz)
            elif orientation == 'y':
                dx, dy, dz = radius * math.cos(angle), 0, radius * math.sin(angle)
                glVertex3f(x + dx, y + dy + height, z + dz)
            elif orientation == 'z':
                dx, dy, dz = radius * math.cos(angle), radius * math.sin(angle), 0
                glVertex3f(x + dx, y + dy, z + dz + height)
        glEnd()
        
    def drawTruck(self):
        glPushMatrix()
        glScale(10, 10, 10)
        # Base y techo
        self.drawRectangle(0.0, 1.0, 0.0, 4.0, 1.0, 2.0)
        self.drawRectangle(0.0, 4.0, 0.0, 2.2, 0.5, 2.0)
        
        # Plataforma
        self.drawRectangle(-2.0, 0.9, 0.0, 2.0, 0.3, 2.0)
        
        # Pilares
        self.drawCylinder(0.2, 2.0, 0.2, 0.2, 2.0, 'y')
        self.drawCylinder(0.4, 2.0, 1.8, 0.2, 2.0, 'y')
        self.drawCylinder(2.0, 2.0, 1.8, 0.2, 2.0, 'y')
        self.drawCylinder(2.0, 2.0, 0.2, 0.2, 2.0, 'y')
        
        # Ruedas
        self.drawCylinder(0.7, 1.0, -0.5, 0.5, 0.5, 'z')
        self.drawCylinder(3.2, 1.0, -0.5, 0.5, 0.5, 'z')
        self.drawCylinder(0.7, 1.0, 2.0, 0.5, 0.5, 'z')
        self.drawCylinder(3.2, 1.0, 2.0, 0.5, 0.5, 'z')
        
        glPopMatrix()
        
    def update(self):
        """
        Función que actualiza el ángulo de rotación del objeto.
        
        Parámetros:
        - self: La instancia actual de la clase.
        
        Retorna:
        No tiene valor de retorno.
        """
    
    def draw(self):
        """
        Función que dibuja el objeto Astro y sus lunas asociadas.
        
        Parámetros:
        - self: La instancia actual de la clase.
        
        Retorna:
        No tiene valor de retorno.
        """
        glPushMatrix()
        
        # Definir el color de la esfera
        glColor3fv(self.color)
        
        # Dibuja una esfera de radio 1.0.
        gluSphere(self.sphere, 1.0, 16, 16)
        
        for moon in self.moons:
            moon.draw()
        
        glPopMatrix()
        self.update()
        
    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()
        
    def draw(self, cubos):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale, self.scale, self.scale)
        glColor3f(1.0, 1.0, 1.0)
        self.drawFaces()
        glPopMatrix()