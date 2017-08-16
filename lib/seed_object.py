#!/usr/bin/python3

import os

from OpenGL.GL import *
import pygame
from pygame.locals import *


class Material(object):

	def __init__(self, name):
		self.name = name
		self.map_kd = None
		self.texture_id = None
		self.map_bump = ''
		self.ns = 0
		self.ka = []
		self.kd = []
		self.ks = []
		self.ke = []
		self.ni = 0
		self.d = 0
		illum = 0


class Face_Group(object):

	def __init__(self, usemtl):
		self.usemtl = usemtl
		self.smooth = None
		self.lines = []
		self.tri_faces = []
		self.quad_faces = []


class Game_Object(object):

	def __init__(self, name):
		self.name = name
		self.face_groups = []


class Obj_Reader(object):

	def __init__(self, filepath, filename):
		self.obj_filename = filename
		self.obj_filepath = filepath
		self.mtllib = None
		self.obj_list = []
		self.vertices = []
		self.normals = []
		self.texuals = []
		self.materials = {}

	def read(self):
		obj_file = open(self.obj_filepath + self.obj_filename, 'r')
		for line in obj_file:
			line = line.rstrip()
			if line == '': continue  #Empty Line
			line_elements = line.split()
			command, data = line_elements[0], line_elements[1:]
			if command == '#':
				continue  #Comment
			elif command == 'mtllib':
				self.mtllib = data[0]
			elif command == 'usemtl':
				face_group = Face_Group(usemtl=data[0])
				self.obj_list[-1].face_groups.append(face_group)
			elif command == 'o':
				self.obj_list.append(Game_Object(name=data[0]))
			elif command == 'v':
				vertex = (float(data[0]), float(data[1]), float(data[2]))
				self.vertices.append(vertex)
			elif command == 'vn':
				normal = (float(data[0]), float(data[1]), float(data[2]))
				self.normals.append(normal)
			elif command == 'f':
				if len(data) == 2:
					line = []
					for element in data:
						indexes = element.split('/')
						line.append(self.proc_indexes(indexes))
					self.obj_list[-1].face_groups[-1].lines.append(line)
				elif len(data) == 3:
					tri_face = []
					for element in data:
						indexes = element.split('/')
						tri_face.append(self.proc_indexes(indexes))
					self.obj_list[-1].face_groups[-1].tri_faces.append(tri_face)
				elif len(data) == 4:
					quad_face = []
					for element in data:
						indexes = element.split('/')
						quad_face.append(self.proc_indexes(indexes))
					self.obj_list[-1].face_groups[-1].quad_faces.append(quad_face)
			elif command == 's':
				self.obj_list[-1].face_groups[-1].smooth = data[0]		
			elif command == 'vt':
				texual = (float(data[0]), float(data[1]))
				self.texuals.append(texual)
			else:
				raise RuntimeError('OBJ file line not recognized: ',
								   line_elements)
		obj_file.close()
		for obj in self.obj_list:
			mtl_file = open(self.obj_filepath + self.mtllib, 'r')
			for line in mtl_file:
				line = line.rstrip()
				if line == '': continue  #Empty line
				line_elements = line.split()
				command, data = line_elements[0], line_elements[1:]
				if command == '#':
					continue  #Comment
				elif command == 'newmtl':
					mtl = Material(name=data[0])
					self.materials[mtl.name] = mtl
				elif command == 'map_Kd':
					tex_filename = data[0]
					mtl.map_kd = tex_filename
					tex_surface = pygame.image.load(self.obj_filepath
													+ tex_filename)
					tex_data = pygame.image.tostring(tex_surface,
													 'RGB',
													 True)
					texture_id = glGenTextures(1)
					glBindTexture(GL_TEXTURE_2D, texture_id)
					mtl.texture_id = texture_id
					self.materials[mtl.name] = mtl
					glTexParameteri(GL_TEXTURE_2D,
									GL_TEXTURE_MAG_FILTER,
									GL_LINEAR)
					glTexParameteri(GL_TEXTURE_2D,
									GL_TEXTURE_MIN_FILTER,
									GL_LINEAR)
					glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
					tex_width, tex_height = tex_surface.get_rect().size
					glTexImage2D(GL_TEXTURE_2D,
								 0,
								 3,
								 tex_width,
								 tex_height,
								 0,
								 GL_RGB, GL_UNSIGNED_BYTE,
								 tex_data)
					glBindTexture(GL_TEXTURE_2D, 0)
				elif command == 'map_Bump':
					mtl.map_bump = data[0]
					self.materials[mtl.name] = mtl
				elif command == 'Ns':
					mtl.ns = float(data[0])
					self.materials[mtl.name] = mtl
				elif command == 'Ka':
					mtl.ka = [float(data[0]), float(data[1]), float(data[2])]
					self.materials[mtl.name] = mtl							
				elif command == 'Kd':
					mtl.kd = [float(data[0]), float(data[1]), float(data[2])]		
					self.materials[mtl.name] = mtl
				elif command == 'Ks':
					mtl.ks = [float(data[0]), float(data[1]), float(data[2])]
					self.materials[mtl.name] = mtl
				elif command == 'Ke':
					mtl.ke = [float(data[0]), float(data[1]), float(data[2])]
					self.materials[mtl.name] = mtl
				elif command == 'Ni':
					mtl.ni = float(data[0])
					self.materials[mtl.name] = mtl
				elif command == 'd':
					mtl.d = float(data[0])
					self.materials[mtl.name] = mtl
				elif command == 'illum':
					mtl.illum = float(data[0])
					self.materials[mtl.name] = mtl
				else:
					raise RuntimeError('MTL file line not recognized: ',
									   line_elements)
			mtl_file.close()

	def load(self):
		self.display_list = glGenLists(1)
		glNewList(self.display_list, GL_COMPILE)
		for obj in self.obj_list:
			for group in obj.face_groups: 
				usemtl = group.usemtl
				mtl = self.materials[usemtl]
				texture_id = mtl.texture_id
				glColor3fv(mtl.kd)
				glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mtl.ka)
				glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mtl.kd)
				#glMaterialfv(GL_FRONT, GL_SPECULAR, mtl.ks)  #Looks bad
				glMaterialfv(GL_FRONT, GL_EMISSION, mtl.ke)
				#glMaterialf(GL_FRONT, GL_SHININESS, mtl.ns)  #Looks bad
				if texture_id != None:
					glBindTexture(GL_TEXTURE_2D, texture_id)
				glBegin(GL_LINES)
				for line in group.lines:
					for element in line:
						if element[2] != 0:
							glNormal3fv(self.normals[element[2]-1])
						if element[1] != 0:
							glTexCoord2fv(self.texuals[element[1]-1])
						glVertex3fv(self.vertices[element[0]-1])
				glEnd()
				glBegin(GL_TRIANGLES)
				for face in group.tri_faces:
					for element in face:
						if element[2] != 0:
							glNormal3fv(self.normals[element[2]-1])
						if element[1] != 0:
							glTexCoord2fv(self.texuals[element[1]-1])
						glVertex3fv(self.vertices[element[0]-1])
				glEnd()
				glBegin(GL_QUADS)
				for face in group.quad_faces:
					for element in face:
						if element[2] != 0:
							glNormal3fv(self.normals[element[2]-1])
						if element[1] != 0:
							glTexCoord2fv(self.texuals[element[1]-1])
						glVertex3fv(self.vertices[element[0]-1])
				glEnd()
		glEndList()
		print('Loaded...')

	def proc_indexes(self, index):
		if index[1] == '': index[1] = 0 
		if index[2] == '': index[2] = 0
		return (int(index[0]), int(index[1]), int(index[2]))


def test():
	print('No detectable errors. ^_^')

if __name__ == '__main__':
	test()
