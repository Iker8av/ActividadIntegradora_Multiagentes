from enum import Enum
import math
import pygame
from pygame.locals import *
import numpy as np
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class EstadosMontacargas(Enum):
    NAVEGACION = 0
    COLISION = 1
    REORIENTACION = 2
    AVANDESTINO = 3
    DEPOSITANDO = 4

class Montacargas:
    
    def __init__(self, dim, vel, scale, cubos):
        self.radius = 10
        self.scale = scale
        self.vel = vel
        self.Cubos = cubos
        self.collided_cube = None
        
        self.Ymin = 0.9
        self.Ymax = 10
        self.estado = EstadosMontacargas.NAVEGACION
        self.altura = self.Ymin
        
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


    def random_movement(self):
        '''
        Función para generar un movimiento aleatorio del objeto.
        '''
        self.drawTruck()

        # Movemos al montacargas a una nueva posición
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        # detectamos que el montacargas no se salga del area de navegacion
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
        
        # verificamos si el montacargas colisionó con un cubo en su nueva posición
        self.collision_detection()
    

    def platform_animation(self):
        '''
        Función para efectuar la animación de la plataforma.
            - Se ejecuta inmediatamente después de la detección de una colisión.
        '''
        if self.altura < self.Ymax:
            if self.collided_cube != None:
                self.drawTruck()
                self.altura += 0.5
                self.collided_cube.Position[1] += 0.5
                self.collided_cube.draw()
        else:
            self.estado = EstadosMontacargas.AVANDESTINO



    def advance_to_destiny(self):
        '''
        Función para avanzar hacia el destino de entrega (centro del sistema).
        '''
        if self.collided_cube is not None:

            # volteamos la dirección del montacargas
            new_x = -1 * self.Position[0]
            new_z = -1 * self.Position[2]
            
            # calculamos la norma del vector
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

                        # actualizamos la velocidad
                        self.Direction[0] *= self.vel
                        self.Direction[2] *= self.vel

                        # reseteamos estado collision y la referencia al collided_cube
                        self.estado = EstadosMontacargas.NAVEGACION
                        self.collided_cube = None
                        
                        new_x = self.Position[0] + self.Direction[0]
                        new_z = self.Position[2] + self.Direction[2]

                        self.Position[0] = new_x
                        self.Position[2] = new_z

    def update(self):
        if (self.estado == EstadosMontacargas.NAVEGACION):
            self.random_movement()
        elif (self.estado == EstadosMontacargas.COLISION):
            self.platform_animation()
        elif (self.estado == EstadosMontacargas.REORIENTACION):
            self.reorientacion()
        elif (self.estado == EstadosMontacargas.AVANDESTINO):
            self.advance_to_destiny()
        elif (self.estado == EstadosMontacargas.DEPOSITANDO):
            self.animationDown()


    def collision_detection(self):            
        for cube in self.Cubos:
            # if self != cube and self.collided_cube == None and self.collision == False:
            if self != cube and self.collided_cube == None and self.estado != EstadosMontacargas.COLISION:
                d_x = self.Position[0] - cube.Position[0]
                d_z = self.Position[2] - cube.Position[2]
                d_c = math.sqrt(d_x * d_x + d_z * d_z)
                
                if d_c - (self.radius + cube.radius) < 0.0:
                    self.estado = EstadosMontacargas.COLISION # actualizamos el estado del montacargas a COLISION
                    self.collided_cube = cube  # guardamos la referencia al cubo colisionado

                    # detenemos el vector de dirección
                    self.Direction[0] = 0
                    self.Direction[2] = 0

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
        
    def drawPlatform(self, x, platform_height, z, width, height, depth):
        glColor3f(0.925, 0.19, 0.03)
        glBegin(GL_QUADS)
        # Bottom face
        glVertex3f(x, platform_height, z)
        glVertex3f(x + width, platform_height, z)
        glVertex3f(x + width, platform_height + height, z)
        glVertex3f(x, platform_height + height, z)

        # Top face
        glVertex3f(x, platform_height, z + depth)
        glVertex3f(x + width, platform_height, z + depth)
        glVertex3f(x + width, platform_height + height, z + depth)
        glVertex3f(x, platform_height + height, z + depth)

        # Front face
        glVertex3f(x, platform_height, z)
        glVertex3f(x + width, platform_height, z)
        glVertex3f(x + width, platform_height, z + depth)
        glVertex3f(x, platform_height, z + depth)

        # Back face
        glVertex3f(x, platform_height + height, z)
        glVertex3f(x + width, platform_height + height, z)
        glVertex3f(x + width, platform_height + height, z + depth)
        glVertex3f(x, platform_height + height, z + depth)

        # Left face
        glVertex3f(x, platform_height, z)
        glVertex3f(x, platform_height + height, z)
        glVertex3f(x, platform_height + height, z + depth)
        glVertex3f(x, platform_height, z + depth)

        # Right face
        glVertex3f(x + width, platform_height, z)
        glVertex3f(x + width, platform_height + height, z)
        glVertex3f(x + width, platform_height + height, z + depth)
        glVertex3f(x + width, platform_height, z + depth)
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
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScalef(self.scale, self.scale, self.scale)

        # Base y techo
        self.drawRectangle(0.0, 1.0, 0.0, 4.0, 1.0, 2.0)
        self.drawRectangle(0.0, 4.0, 0.0, 2.2, 0.5, 2.0)
        
        # Plataforma
        self.drawPlatform(-2.0, self.altura, 0.0, 2.0, 0.3, 2.0)
        
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