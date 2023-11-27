from time import sleep, time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import serial

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# Initial quaternion
quaternion = [1, 0, 0, 0]

def draw_cube():

        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.5, 0.2, -0.5)
        glVertex3f(-0.5, 0.2, -0.5)
        glVertex3f(-0.5, 0.2, 0.5)
        glVertex3f(0.5, 0.2, 0.5)

        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(0.5, -0.2, 0.5)
        glVertex3f(-0.5, -0.2, 0.5)
        glVertex3f(-0.5, -0.2, -0.5)
        glVertex3f(0.5, -0.2, -0.5)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.5, 0.2, 0.5)
        glVertex3f(-0.5, 0.2, 0.5)
        glVertex3f(-0.5, -0.2, 0.5)
        glVertex3f(0.5, -0.2, 0.5)

        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.5, -0.2, -0.5)
        glVertex3f(-0.5, -0.2, -0.5)
        glVertex3f(-0.5, 0.2, -0.5)
        glVertex3f(0.5, 0.2, -0.5)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-0.5, 0.2, 0.5)
        glVertex3f(-0.5, 0.2, -0.5)
        glVertex3f(-0.5, -0.2, -0.5)
        glVertex3f(-0.5, -0.2, 0.5)

        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(0.5, 0.2, -0.5)
        glVertex3f(0.5, 0.2, 0.5)
        glVertex3f(0.5, -0.2, 0.5)
        glVertex3f(0.5, -0.2, -0.5)
        glEnd()

def update_cube_orientation_quat():
    glLoadIdentity()

    # rotation matrix represents rotation transformation
    rotation_matrix = [
        [1 - 2 * (quaternion[2]**2 + quaternion[3]**2), 2 * (quaternion[1]*quaternion[2] - quaternion[0] * quaternion[3]), 2 * (quaternion[0] * quaternion[2] + quaternion[1] * quaternion[3]), 0],
        [2 * (quaternion[1] * quaternion[2] + quaternion[0] * quaternion[3]), 1 - 2 * (quaternion[1]**2 + quaternion[3]**2), 2 * (quaternion[2] * quaternion[3] - quaternion[0] * quaternion[1]), 0],
        [2 * (quaternion[1] * quaternion[3] - quaternion[0] * quaternion[2]), 2 * (quaternion[0] * quaternion[1] + quaternion[2] * quaternion[3]), 1 - 2 * (quaternion[1]**2 + quaternion[2]**2), 0],
        [0, 0, 0, 1]
    ]

    glMultMatrixf(rotation_matrix) # Apply the rotation matrix object

def read_quaternion_data(serial_port):

    line = serial_port.readline().decode("utf-8").strip() # data being sent like "w,x,y,z\n"

    line_bytes = line.encode("utf-8") # Encode string to bytes
    line_bytes = line_bytes.replace(b'\x00', b'')  # takeout null bytes (I think it's cause i do \r in firmware)
    line = line_bytes.decode("utf-8") # Decode bytes back to string

    quaternion_data = [float(value) for value in line.split(',') if value] # split line into individual values

    #print(quaternion_data)

    return quaternion_data

def normalize(q):
    magnitude = sum(val**2 for val in q)**0.5
    return [val / magnitude for val in q]

def main():
    global quaternion_data, quaternion
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Cube")

    gluPerspective(35, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, 5.0)

    serial_port = serial.Serial('COM4', 115200, timeout=1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        quaternion_data = read_quaternion_data(serial_port)
        if len(quaternion_data) == 4:
            quaternion = normalize(quaternion_data)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        update_cube_orientation_quat()

        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
