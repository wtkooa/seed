#!/usr/bin/python3

import pygame
import os
from math import sin, cos, radians
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from lib import seed_math 
from lib import seed_object

CWD = os.getcwd()
WINDOW_CAPTION = "Game Object Viewer"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
DEFAULT_DISTANCE = -3
LIGHT_POSITION = (0, 0, 2, 0)
COLOR = (0.5,0.5,0.5) ##########This is temp.....
PYGAME_MODE = HWSURFACE|DOUBLEBUF|OPENGL|RESIZABLE
FIELD_OF_VIEW = 60
Z_NEAR = 0.1
Z_FAR = 1000.0

#degrees per second
ROTATION_SPEED = 45.0
#meters per second
TRANSFORM_SPEED = 5

def draw_object(reader):
	glCallList(reader.display_list)
	
def init():
	obj_filename = input("Enter OBJ filepath: ")
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY, PYGAME_MODE)
	pygame.display.set_caption(WINDOW_CAPTION)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.05, 0.05, 0.05))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5))
	reader = seed_object.Obj_Reader()
	reader.set_filepath(CWD)
	reader.set_obj_filename(obj_filename)
	reader.read()
	reader.load()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(FIELD_OF_VIEW, ASPECT_RATIO, Z_NEAR, Z_FAR)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION) 
	glColor(COLOR)
	#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) ################# Remember to change this....
	return screen, reader

def resize_window(display):
	aspect_ratio = display[0] / display[1]
	screen = pygame.display.set_mode(display, PYGAME_MODE)
	glViewport(0, 0, display[0], display[1])
	glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(FIELD_OF_VIEW, aspect_ratio, Z_NEAR, Z_FAR)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	return screen

def rollover_handler(angle):
	if angle > 360.0: return angle - 360.0
	if angle < 0: return angle + 360.0
	return angle

def rotate_object(rotate_event_vec, model, frame_time_seconds):
	glPushMatrix()
	glLoadIdentity()
	rotation_speed_delta = ROTATION_SPEED * frame_time_seconds
	if rotate_event_vec.x != 0:
		glRotate(rotate_event_vec.x * rotation_speed_delta, 1, 0, 0)
	if rotate_event_vec.y != 0:
		glRotate(rotate_event_vec.y * rotation_speed_delta, 0, 1, 0)
	if rotate_event_vec.z != 0:
		glRotate(rotate_event_vec.z * rotation_speed_delta, 0, 0, 1)
	glMultMatrixf(model)
	model = glGetFloatv(GL_MODELVIEW_MATRIX)  #Don't use this func for long.
	glPopMatrix()
	return model	

def transform_object(transform_event_vec, transform_object_vec, frame_time_seconds):
	transform_speed_delta = TRANSFORM_SPEED * frame_time_seconds 
	if transform_event_vec.z == 1: transform_object_vec.z += transform_speed_delta
	if transform_event_vec.z == -1: transform_object_vec.z += -transform_speed_delta
	glTranslate(0, 0, transform_object_vec.z)
	return transform_object_vec

def event_handler(events, engine_on, rotate_event_vec, transform_event_vec, screen):
	for event in events:
		if event.type == pygame.QUIT:
			engine_on = False
		elif event.type == pygame.VIDEORESIZE:
			screen = resize_window(event.size)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				engine_on = False
			elif event.key == pygame.K_w:
				rotate_event_vec.x += -1.0
			elif event.key == pygame.K_s:
				rotate_event_vec.x += 1.0
			elif event.key == pygame.K_d:
				rotate_event_vec.y += 1.0
			elif event.key == pygame.K_a:
				rotate_event_vec.y += -1.0
			elif event.key == pygame.K_q:
				rotate_event_vec.z += 1.0
			elif event.key == pygame.K_e:
				rotate_event_vec.z += -1.0
			elif event.key == pygame.K_LSHIFT:
				transform_event_vec.z = 1
			elif event.key == pygame.K_LCTRL:
				transform_event_vec.z = -1
			elif event.key == pygram.K_0:
				continue
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_w: 
				rotate_event_vec.x += 1.0
			elif event.key == pygame.K_s:
				rotate_event_vec.x += -1.0
			elif event.key == pygame.K_d:
				rotate_event_vec.y += -1.0
			elif event.key == pygame.K_a:
				rotate_event_vec.y += 1.0
			elif event.key == pygame.K_q: 
				rotate_event_vec.z += -1.0
			elif event.key == pygame.K_e:
				rotate_event_vec.z += 1.0
			elif event.key == pygame.K_LSHIFT or event.key == pygame.K_LCTRL:
				 transform_event_vec.z = 0
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed() == (0,1,0):
				continue #############Change
		elif event.type == pygame.MOUSEBUTTONUP:
			if pygame.mouse.get_pressed() == 4:
				continue #############Change
	return engine_on, rotate_event_vec, transform_event_vec, screen

def clear_screen():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

def handle_time(clock):
	frame_time_millisec = clock.tick(60)
	frame_time_seconds = frame_time_millisec / 1000.0
	return frame_time_seconds

def main():

	screen, reader = init()
	rotate_event_vec = seed_math.Vector3()
	rotate_object_vec = seed_math.Vector3()
	transform_event_vec = seed_math.Vector3()
	transform_object_vec = seed_math.Vector3(0, 0, DEFAULT_DISTANCE)
	glPushMatrix()
	glLoadIdentity()
	model = glGetFloatv(GL_MODELVIEW_MATRIX)
	glPopMatrix()
	
	clock = pygame.time.Clock()
	
	engine_on = True
	while engine_on:
	
		engine_on, rotate_event_vec, transform_event_vec, screen = event_handler(pygame.event.get(), engine_on,	rotate_event_vec, transform_event_vec, screen)
		clear_screen()
		frame_time_seconds = handle_time(clock)
		glPushMatrix()
		transform_object_vec = transform_object(transform_event_vec, transform_object_vec, frame_time_seconds)
		model = rotate_object(rotate_event_vec, model, frame_time_seconds)
		glMultMatrixf(model)
		draw_object(reader)
		glPopMatrix()
		pygame.display.flip()
			
	pygame.quit()

if __name__ == "__main__":
	main()
	quit()
