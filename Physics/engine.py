#!/usr/bin/env python
"""engine.py: A simple 2d physics simulation"""

import random
import math

import pygame
import pygame.gfxdraw

#----------------------------------------#
__author__ = "Lawrence Foley"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Peter Collingridge", "Lawrence Foley"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = "emwav333@gamil.com"
__status__ = "Prototype"
#----------------------------------------#

background_color = (255, 255, 255)
(width, height) = (400, 400)

# Universe Constants
gravity = (math.pi, 0.00005)
drag = 0.99999999
elasticity = 0.7


def add_vectors(angle1_length1, angle2_length2):
    ((angle1, length1), (angle2, length2)) = angle1_length1, angle2_length2
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length


class Particle():
    def __init__(self, x_y, size):
        (x, y) = x_y
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 0)
        self.thickness = 5
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.gfxdraw.aacircle(screen, (int(self.x)), (int(self.y)), self.size, self.color)
        #pygame.gfxdraw.filled_circle(screen, (int(self.x)), (int(self.y)), self.size, self.color)
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)  # gravity affecting particle
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        elif (self.x < self.size):
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        if (self.y > height - self.size):
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif (self.y < self.size):
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics")

number_of_particles = (3)
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10, 40)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)

    particle = Particle((x, y), size)
    particle.speed = 20
    particle.angle = random.uniform(0, math.pi * 2)

    my_particles.append(particle)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(background_color)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()
    pygame.display.flip()

pygame.quit()