import math
import pygame
from pygame.locals import *
import numpy as np
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Montacargas:
    
    def __init__(self, dim, vel, scale, color, cubos):
        self.scale = scale
        self.radius = math.sqrt(3) 
        self.collision = False
        self.color = color
        self.vel = vel
        self.Cubos = cubos
        self.collided_cube = None
        
        #vertices del cubo
        self.points = np.array([[-1.0,-1.0, 1.0], [1.0,-1.0, 1.0], [1.0,-1.0,-1.0], [-1.0,-1.0,-1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0,-1.0], [-1.0, 1.0,-1.0]])
        
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la magnitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel

    def update(self):
        self.collisionDetection() # updates collision attribute
        
        if self.collision == False:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]
            
            # detecc de que el objeto no se salga del area de navegacion
            if(abs(new_x) <= self.DimBoard):
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]
            
            if(abs(new_z) <= self.DimBoard):
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2] 
        
        elif self.collision == True:
            if self.collided_cube is not None:
                new_x = 0 - self.Position[0]
                new_z = 0 - self.Position[2]

                # para asegurar una velocidad constante
                magnitude = math.sqrt(new_x ** 2 + new_z ** 2)
                
                if magnitude != 0:
                    # normalizamos el vector dirección
                    new_x /= magnitude
                    new_z /= magnitude

                    # actualizamos velocidad
                    self.Direction[0] = new_x * self.vel
                    self.Direction[2] = new_z * self.vel

                    # movemos al montacargas en la nueva dirección al centro
                    self.Position[0] += self.Direction[0]
                    self.Position[2] += self.Direction[2]
                    
                    # movemos al cubo colisionado igualmente al centro
                    self.collided_cube.Position[0] += self.Direction[0]
                    self.collided_cube.Position[2] += self.Direction[2]

                    # checamos si hemos llegado al centor
                    if abs(self.Position[0]) < self.radius and abs(self.Position[2]) < self.radius:
                        
                        # eliminamos el collided_cube de la lista Cubos
                        if self.collided_cube in self.Cubos:
                            self.Cubos.remove(self.collided_cube)

                        # restauramos la dirección del montacargas a aleatoria
                        self.Direction[0] = random.random()
                        self.Direction[2] = random.random()

                        # normalizamos
                        m = math.sqrt(self.Direction[0] * self.Direction[0] + self.Direction[2] * self.Direction[2])
                        self.Direction[0] /= m
                        self.Direction[2] /= m
                        # actualizamos la vel
                        self.Direction[0] *= self.vel
                        self.Direction[2] *= self.vel

                        # reseteamos estado collision y la referencia al collided_cube
                        self.collision = False
                        self.collided_cube = None
                        
                        new_x = self.Position[0] + self.Direction[0]
                        new_z = self.Position[2] + self.Direction[2]

                        self.Position[0] = new_x
                        self.Position[2] = new_z

    def collisionDetection(self):            
        for cube in self.Cubos:
            if self != cube and self.collided_cube == None and self.collision == False:
                d_x = self.Position[0] - cube.Position[0]
                d_z = self.Position[2] - cube.Position[2]
                d_c = math.sqrt(d_x * d_x + d_z * d_z)
                
                if d_c - (self.radius + cube.radius) < 0.0:
                    self.collision = True
                    self.collided_cube = cube  # guardamos la referencia al cubo colisionado

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
    
    def draw(self):
        glPushMatrix() # guardamos el estado de transformacion actual
        glTranslatef(self.Position[0], self.Position[1], self.Position[2]) # trasladamos
        glScaled(self.scale[0], self.scale[1], self.scale[2]) # escalamos el objeto
        glColor3f(self.color[0], self.color[1], self.color[2]) # fijamos el color
        self.drawFaces() # dibujamos las caras
        glPopMatrix() # quitamos del pila