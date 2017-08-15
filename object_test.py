#!/usr/bin/python3

from math import sin, cos, radians
import os

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from lib.seed_math import * 
from lib.seed_object import *

CWD = os.getcwd()
OBJ_FILEPATH = CWD + '/obj/'
WINDOW_CAPTION = 'Game Object Viewer'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
DEFAULT_DISTANCE = -3
LIGHT_POSITION = (0, 0, 2, 0)  #Update: ?
DEFAULT_AMBIENT = (0.05, 0.05, 0.05)  #Update: ?
DEFAULT_DIFFUSE = (0.5, 0.5, 0.5)  #Update: ?
DEFAULT_COLOR = (0.5,0.5,0.5)  #Update: ?
PYGAME_MODE = HWSURFACE|DOUBLEBUF|OPENGL|RESIZABLE
FIELD_OF_VIEW = 60
Z_NEAR = 0.1
Z_FAR = 1000.0
ROTATION_SPEED = 45.0  #Degrees per second
TRANSFORM_SPEED = 5  #Meters per second
WIREFRAME = False


class Object_Viewer(object):

	def __init__(self, *args):
		self.arg_handler(args)
		self.init()
		self.main()

	def arg_handler(self, args):
		if len(args) == 0:
			self.obj_filename = input('OBJ Filename: ')
			if self.obj_filename == '':
				self.obj_filename = 'cube.obj'
		elif len(args) == 1:
			self.obj_filename = args[0]
		else:
			raise ValueError('Object_Viewer(none or filename): ' + str(args))

	def init(self):
		pygame.init()
		self.screen = pygame.display.set_mode(DISPLAY, PYGAME_MODE)
		pygame.display.set_caption(WINDOW_CAPTION)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_COLOR_MATERIAL)
		glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
		glColor(DEFAULT_COLOR)
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
		glLightfv(GL_LIGHT0, GL_AMBIENT, DEFAULT_AMBIENT)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, DEFAULT_DIFFUSE)
		glShadeModel(GL_SMOOTH)
		if WIREFRAME: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) 
		self.reader = Obj_Reader(filepath=OBJ_FILEPATH,
								 filename=self.obj_filename)
		self.reader.read()
		self.reader.load()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(FIELD_OF_VIEW, ASPECT_RATIO, Z_NEAR, Z_FAR)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		self.rot_event_v3 = Vector3()
		self.rot_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
		self.tran_event_v3 = Vector3()
		self.tran_pos_v3 = Vector3(0, 0, DEFAULT_DISTANCE)
		self.clock = pygame.time.Clock()

	def resize_window(self, display):
		aspect_ratio = display[0] / display[1]
		self.screen = pygame.display.set_mode(display, PYGAME_MODE)
		glViewport(0, 0, display[0], display[1])
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(FIELD_OF_VIEW, aspect_ratio, Z_NEAR, Z_FAR)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def rotate_object(self):
		glPushMatrix()
		glLoadIdentity()
		delta = ROTATION_SPEED * self.frame_time_seconds
		if self.rot_event_v3.x != 0:
			glRotate(self.rot_event_v3.x * delta, 1, 0, 0)
		if self.rot_event_v3.y != 0:
			glRotate(self.rot_event_v3.y * delta, 0, 1, 0)
		if self.rot_event_v3.z != 0:
			glRotate(self.rot_event_v3.z * delta, 0, 0, 1)
		glMultMatrixf(self.rot_matrix)
		self.rot_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)  #Update: Too slow
		glPopMatrix()

	def transform_object(self):
		delta = TRANSFORM_SPEED * self.frame_time_seconds 
		if self.tran_event_v3.z == 1: self.tran_pos_v3.z += delta
		if self.tran_event_v3.z == -1: self.tran_pos_v3.z -= delta
		glTranslate(0, 0, self.tran_pos_v3.z)

	def event_handler(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.engine_on = False
			elif event.type == pygame.VIDEORESIZE:
				self.resize_window(event.size)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.engine_on = False
				elif event.key == pygame.K_w:
					self.rot_event_v3.x += -1.0
				elif event.key == pygame.K_s:
					self.rot_event_v3.x += 1.0
				elif event.key == pygame.K_d:
					self.rot_event_v3.y += 1.0
				elif event.key == pygame.K_a:
					self.rot_event_v3.y += -1.0
				elif event.key == pygame.K_q:
					self.rot_event_v3.z += 1.0
				elif event.key == pygame.K_e:
					self.rot_event_v3.z += -1.0
				elif event.key == pygame.K_LSHIFT:
					self.tran_event_v3.z = 1
				elif event.key == pygame.K_LCTRL:
					self.tran_event_v3.z = -1
				elif event.key == pygram.K_0:
					continue  #Update: View Reset
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					self.rot_event_v3.x += 1.0
				elif event.key == pygame.K_s:
					self.rot_event_v3.x += -1.0
				elif event.key == pygame.K_d:
					self.rot_event_v3.y += -1.0
				elif event.key == pygame.K_a:
					self.rot_event_v3.y += 1.0
				elif event.key == pygame.K_q:
					self.rot_event_v3.z += -1.0
				elif event.key == pygame.K_e:
					self.rot_event_v3.z += 1.0
				elif (event.key == pygame.K_LSHIFT or
					 event.key == pygame.K_LCTRL):
					self.tran_event_v3.z = 0
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed() == (0,1,0):
					continue  #Update: Mouse Func
			elif event.type == pygame.MOUSEBUTTONUP:
				if pygame.mouse.get_pressed() == 4:
					continue  #Update: Mouse Func

	def clear_frame_buffer(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def handle_time(self):
		self.frame_time_millisec = self.clock.tick(60)
		self.frame_time_seconds = self.frame_time_millisec / 1000.0
		self.fps = 1000.0 / self.frame_time_millisec

	def draw_object(self):
		glPushMatrix()
		self.transform_object()
		self.rotate_object()
		glMultMatrixf(self.rot_matrix)
		glCallList(self.reader.display_list)
		glPopMatrix()

	def main(self):
		self.engine_on = True
		while self.engine_on:
			self.event_handler()
			self.handle_time()
			self.clear_frame_buffer()
			self.draw_object()
			pygame.display.flip()
		self.cleanup()

	def cleanup(self):
		pygame.quit()


if __name__ == '__main__':
	viewer = Object_Viewer()
	quit()
