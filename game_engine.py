#!/usr/bin/python3

from math import sin, cos, radians
import os
import timeit

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from lib.utils import *

CWD = os.getcwd()
OBJ_FILEPATH = CWD + '/data/obj/'
WLD_FILEPATH = CWD + '/data/world/'
TEX_FILEPATH = CWD + '/data/obj/tex/'
WINDOW_CAPTION = 'Game Engine'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
DEFAULT_DISTANCE = -3
LIGHT_POSITION = (0, 0, 10, 0)  #Update: ?
DEFAULT_AMBIENT = (0.1, 0.1, 0.1)  #Update: ?
DEFAULT_DIFFUSE = (0.5, 0.5, 0.5)  #Update: ?
DEFAULT_COLOR = (0.5,0.5,0.5)  #Update: ?
PYGAME_MODE = HWSURFACE|DOUBLEBUF|OPENGL|RESIZABLE
FIELD_OF_VIEW = 60
Z_NEAR = 0.1
Z_FAR = 1000.0
TRANSLATE_SPEED = 2 
WIREFRAME = False

class World_Engine(object):

	def __init__(self, *args):
		self.handle_args(args)
		self.init()
		self.main()

	def handle_args(self, args):
		if len(args) == 0:
			self.wld_filename = input('World Filename: ')
			if self.wld_filename == '':
				self.wld_filename = 'default.wld'
		elif len(args) == 1:
			self.wld_filename = args[0]
		else:
			raise ValueError('World_Engine(none or filename): ' + str(args))

	def init(self):
		pygame.init()
		self.screen = pygame.display.set_mode(DISPLAY, PYGAME_MODE)
		pygame.display.set_caption(WINDOW_CAPTION)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_COLOR_MATERIAL)
		glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
		glColor(DEFAULT_COLOR)
		glClearColor(0, 0, 0.7, 1)  #Update: unhardcode sky
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
		glLightfv(GL_LIGHT0, GL_AMBIENT, DEFAULT_AMBIENT)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, DEFAULT_DIFFUSE)
		glShadeModel(GL_SMOOTH)
		if WIREFRAME: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) 
		self.obj_data = Obj_Data(datapath=OBJ_FILEPATH,
								 dataname='obj.data',
								 texpath=TEX_FILEPATH)
		self.obj_data.read()
		self.obj_data.load()
		self.world_data = World_Data(datapath=WLD_FILEPATH,
									 dataname=self.wld_filename)
		self.world_data.read()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(FIELD_OF_VIEW, ASPECT_RATIO, Z_NEAR, Z_FAR)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		self.mouse_event_v3 = Vector3()
		self.tran_event_v3 = Vector3()
		self.tran_pos_v3 = Vector3(0, -3, DEFAULT_DISTANCE)
		self.clock = pygame.time.Clock()
		glBindTexture(GL_TEXTURE_2D, 1) #################
		self.x_accum = 0

	def resize_window(self, display):
		self.display = display
		aspect_ratio = display[0] / display[1]
		self.screen = pygame.display.set_mode(display, PYGAME_MODE)
		glViewport(0, 0, display[0], display[1])
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(FIELD_OF_VIEW, aspect_ratio, Z_NEAR, Z_FAR)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def reset_orientation(self):
		self.tran_pos_v3 = Vector3(0, 0, DEFAULT_DISTANCE)
		
	def rotate_object(self):
		return  #Update duh!

	def translate_camera(self):
		self.tran_pos_v3.x += self.tran_event_v3.x * TRANSLATE_SPEED * self.frame_time_seconds
		self.tran_pos_v3.y += self.tran_event_v3.y * TRANSLATE_SPEED * self.frame_time_seconds
		self.tran_pos_v3.z += self.tran_event_v3.z * TRANSLATE_SPEED * self.frame_time_seconds


	def translate_object(self, glcoord):
		glTranslate(glcoord[0] + self.tran_pos_v3.x, glcoord[1] + self.tran_pos_v3.y, glcoord[2] + self.tran_pos_v3.z)

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.engine_on = False
			elif event.type == pygame.VIDEORESIZE:
				self.resize_window(event.size)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.engine_on = False
				elif event.key == pygame.K_0:
					self.reset_orientation()
				elif event.key == pygame.K_KP0:
					self.reset_orientation()
				elif event.key == pygame.K_SPACE:
					self.tran_event_v3.y += -1.0
				elif event.key == pygame.K_LSHIFT:
					self.tran_event_v3.y += 1.0
				elif event.key == pygame.K_w:
					self.tran_event_v3.z += 1.0
				elif event.key == pygame.K_s:
					self.tran_event_v3.z += -1.0
				elif event.key == pygame.K_a:
					self.tran_event_v3.x += 1.0
				elif event.key == pygame.K_d:
					self.tran_event_v3.x += -1.0
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.tran_event_v3.y += 1.0
				elif event.key == pygame.K_LSHIFT:
					self.tran_event_v3.y += -1.0
				elif event.key == pygame.K_w:
					self.tran_event_v3.z += -1.0
				elif event.key == pygame.K_s:
					self.tran_event_v3.z += 1.0
				elif event.key == pygame.K_a:
					self.tran_event_v3.x += -1.0
				elif event.key == pygame.K_d:
					self.tran_event_v3.x += 1.0
			elif (event.type == pygame.MOUSEBUTTONDOWN and
				  pygame.mouse.get_focused()):
				if event.button == 1:
					continue  #Unused
				if event.button == 2:
					continue  #Unused
				if event.button == 3:
					self.reset_orientation()
				if event.button == 4:
					continue  #Unused
				if event.button == 5:
					continue  #Unused
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					continue  #Unused
				if event.button == 2:
					continue  #Unused

	def clear_frame_buffer(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def handle_time(self):
		self.frame_time_millisec = self.clock.tick(60)
		self.frame_time_seconds = self.frame_time_millisec / 1000.0
		self.fps = 1000.0 / self.frame_time_millisec
		
	def to_glcoords(self, world_coords):
		x = 0.5 + world_coords[0]
		y = 0.5 + world_coords[1]
		z = -0.5 - world_coords[2]
		return [x, y, z]

	def draw(self):
		#self.transform_object()
		#self.rotate_object()
		#glCallList(self.reader.display_list)
		self.translate_camera()
		for obj in self.world_data.object_list:
			glPushMatrix()
			obj_id, world_coords = obj[0], obj[1:]
			obj = self.obj_data.game_objects[int(obj_id)]
			display_list = obj.display_list
			glcoords = self.to_glcoords(world_coords)
			self.translate_object(glcoords)
			glCallList(display_list)
			glPopMatrix()

	def main(self):
		self.engine_on = True
		while self.engine_on:
			self.handle_events()
			self.handle_time()
			self.clear_frame_buffer()
			self.draw()
			pygame.display.flip()
		self.cleanup()

	def cleanup(self):
		pygame.quit()


if __name__ == '__main__':
	world = World_Engine()
	quit()
