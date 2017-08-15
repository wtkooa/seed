#!/usr/bin/python3

import pygame
import os
from pygame.locals import *
from OpenGL.GL import *

class Material(object):

	def __init__(self):
		self.name = None
		self.map_kd = None
		self.texture_id = None
		self.map_bump = ""
		self.ns = 0
		self.ka = []
		self.kd = []
		self.ks = []
		self.ke = []
		self.ni = 0
		self.d = 0
		illum = 0


	def set_name(self, name):
		self.name = name 
		
	def get_name(self):
		return self.name

	def set_map_kd(self, map_kd):
		self.map_kd = map_kd

	def get_map_kd(self):
		return self.map_kd

	def set_texture_id(self, texture_id):
		self.texture_id = texture_id

	def get_texture_id(self):
		return self.texture_id

class Face_Group(object):

	def __init__(self):
		self.usemtl = None
		self.smooth = None
		self.line_edges = []
		self.triangle_faces = []
		self.quad_faces = []

	def set_usemtl(self, usemtl):
		self.usemtl = usemtl

	def get_usemtl(self):
		return self.usemtl

	def set_smooth(self, smooth):
		self.smooth = smooth

	def get_smooth(self):
		return self.smooth

	def add_line_edge(self, edge):
		self.line_edges.append(edge)
	
	def get_line_edge(self, index):
		return self.line_edges[index]

	def add_triangle_face(self, edge):
		self.triangle_faces.append(edge)

	def get_triangle_face(self, index):
		return self.triangle_faces[index]

	def add_quad_face(self, edge):
		self.quad_faces.append(edge)

	def get_quad_face(self, index):
		return self.quad_faces[index]

	def get_line_edges(self):
		return self.line_edges

	def get_triangle_faces(self):
		return self.triangle_faces

	def get_quad_faces(self):
		return self.quad_faces


class Game_Object(object):

	vertices = []
	normals = []
	texuals = []

	def set_name(self, name):
		self.name = name
		self.mtllib = None
		self.face_groups = []
		self.materials = {}

	def get_name(self):
		return self.name

	def set_mtllib(self, mtllib):
		self.mtllib = mtllib

	def get_mtllib(self):
		return self.mtllib

	def add_vertex(self, vert):
		self.vertices.append(vert)

	def get_vertex(self, index):
		return self.vertices[index-1]

	def add_normal(self, norm):
		self.normals.append(norm)

	def get_normal(self, index):
		return self.normals[index-1]

	def add_texual(self, texual):
		self.texuals.append(texual)

	def get_texual(self, index):
		return self.texuals[index-1]
	
	def add_material(self, mtl):
		self.materials[mtl.get_name()] = mtl

	def update_material(self, mtl):
		self.materials[mtl.get_name()] = mtl

	def add_face_group(self, face_group):
		self.face_groups.append(face_group)

	def get_face_group(self, index):
		return self.face_groups[index]

	def get_material(self, name):
		return self.materials[name]

	def get_vertices(self):
		return self.vertices

	def get_normals(self):
		return self.normals

	def get_texuals(self):
		return self.texuals

	def get_face_groups(self):
		return self.face_groups

	def get_materials(self):
		return self.materials

class Obj_Reader(object):

	def __init__(self, *args):
		self.obj_list = []

	def set_filepath(self, cwd):
		self.filepath = cwd + "/obj/"

	def get_filepath(self):
		return self.filepath

	def set_obj_filename(self, obj_filename):
		if obj_filename == "": obj_filename = "cube.obj"
		self.obj_filename = obj_filename

	def get_obj_filename(self):
		return self.obj_filename

	def read(self):
		obj_file = open((self.filepath + self.obj_filename), "r")
		obj_index = -1
		group_index = -1
		for line in obj_file:
			line = line.rstrip()
			line_elements = line.split(" ")
			command, data = line_elements[0], line_elements[1:]
			if command == "":
				continue
			elif command == "#":
				continue
			elif command == "mtllib":
				self.mtllib = data[0]
			elif command == "usemtl":
				group_index += 1
				usemtl = data[0]
				face_group = Face_Group()
				face_group.set_usemtl(usemtl)
				self.obj_list[obj_index].add_face_group(face_group)
			elif command == "o":
				obj_index += 1
				group_index = -1
				self.obj_list.append(Game_Object())
				name = data[0]
				self.obj_list[obj_index].set_name(name)
				self.obj_list[obj_index].set_mtllib(self.mtllib)
			elif command == "v":
				vertex = (float(data[0]), float(data[1]), float(data[2])) 
				self.obj_list[obj_index].add_vertex(vertex)
			elif command == "vn":
				normal = (float(data[0]), float(data[1]), float(data[2])) 
				self.obj_list[obj_index].add_normal(normal)
			elif command == "f":
				if len(data) == 2:
					line_edge = []
					for element in data:
						element = element.split("/")
						line_edge.append( self.face_element(element) )
					self.obj_list[obj_index].face_groups[group_index].line_edges.append(line_edge)
				elif len(data) == 3:
					triangle_face = []
					for element in data:
						element = element.split("/")
						triangle_face.append( self.face_element(element) )
					self.obj_list[obj_index].get_face_group(group_index).add_triangle_face(triangle_face)		
				elif len(data) == 4:
					quad_face = []
					for element in data:
						element = element.split("/")
						quad_face.append( self.face_element(element) )
					self.obj_list[obj_index].face_groups[group_index].quad_faces.append(quad_face)
			elif command == "s":
				self.obj_list[obj_index].face_groups[group_index].set_smooth(data[0])		
			elif command == "vt":
				texual = (float(data[0]), float(data[1]))
				self.obj_list[obj_index].add_texual(texual)
			else:
				raise RuntimeError("OBJ file line not recognized: ",  line_elements)
		obj_file.close()
		for obj in self.obj_list:
			mtl_file = open(self.filepath + obj.get_mtllib(), "r")
			for line in mtl_file:
				line = line.rstrip()
				line_elements = line.split(" ")
				command, data = line_elements[0], line_elements[1:]
				if command == "":
					continue
				elif command == "#":
					continue
				elif command == "newmtl":
					mtl = Material()
					mtl.set_name(data[0])
					obj.add_material(mtl)
				elif command == "map_Kd":
					texture_filename = data[0]
					mtl.set_map_kd(texture_filename)
					texture_surface = pygame.image.load(self.filepath + texture_filename)
					texture_data = pygame.image.tostring(texture_surface, 'RGB', True)
					texture_id = glGenTextures(1)
					glBindTexture(GL_TEXTURE_2D, texture_id)
					mtl.set_texture_id(texture_id)
					obj.update_material(mtl)
					glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
					glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
					glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
					texture_width, texture_height = texture_surface.get_rect().size
					glTexImage2D( GL_TEXTURE_2D, 0, 3, texture_width, texture_height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
					glBindTexture(GL_TEXTURE_2D, 0)
				elif command == "map_Bump":
					mtl.map_bump = data[0]
				elif command == "Ns":
					mtl.ns = float(data[0])
				elif command == "Ka":
					mtl.ka = [float(data[0]), float(data[1]), float(data[2])]
				elif command == "Kd":
					mtl.kd = [float(data[0]), float(data[1]), float(data[2])]		
				elif command == "Ks":
					mtl.ks = [float(data[0]), float(data[1]), float(data[2])]
				elif command == "Ke":
					mtl.ke = [float(data[0]), float(data[1]), float(data[2])]
				elif command == "Ni":
					mtl.ni = float(data[0])
				elif command == "d":
					mtl.d = float(data[0])
				elif command == "illum":
					mtl.illum = float(data[0])
				else:
					raise RuntimeError("MTL file line not recognized: ", line_elements)

	def load(self):
		self.display_list = glGenLists(1)
		glNewList(self.display_list, GL_COMPILE)
		for obj in self.obj_list:
			for group in obj.face_groups: 
				usemtl = group.get_usemtl()
				material = obj.materials[usemtl]
				texture_id = material.get_texture_id()
				glColor3fv(material.kd)
				glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material.ka)
				glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material.kd)
				#glMaterialfv(GL_FRONT, GL_SPECULAR, material.ks)
				glMaterialfv(GL_FRONT, GL_EMISSION, material.ke)
				#glMaterialf(GL_FRONT, GL_SHININESS, material.ns)
				if texture_id != None: glBindTexture(GL_TEXTURE_2D, texture_id)
				glBegin(GL_LINES)
				for edge in group.get_line_edges():
					for element in edge:
						if element[2] != 0: glNormal3fv(obj.get_normal(element[2]))
						if element[1] != 0: glTexCoord2fv(obj.get_texual(element[1]))
						glVertex3fv(obj.get_vertex(element[0]))
				glEnd()
				glBegin(GL_TRIANGLES)
				for face in group.get_triangle_faces():
					for element in face:
						if element[2] != 0: glNormal3fv(obj.get_normal(element[2]))
						if element[1] != 0: glTexCoord2fv(obj.get_texual(element[1]))
						glVertex3fv(obj.get_vertex(element[0]))
				glEnd()
				glBegin(GL_QUADS)
				for face in group.get_quad_faces():
					for element in face:
						if element[2] != 0: glNormal3fv(obj.get_normal(element[2]))
						if element[1] != 0: glTexCoord2fv(obj.get_texual(element[1]))
						glVertex3fv(obj.get_vertex(element[0]))
				glEnd()
		glEndList()
		print("Loaded...")

	def set_filename(self, filename):
		self.filename = filename

	def get_filename(self):
		return self.filename

	def face_element(self, element):
		if element[1] == "": element[1] = 0 
		if element[2] == "": element[2] = 0
		return ( int(element[0]), int(element[1]), int(element[2]) )

def test():
	print("No detectable errors. ^_^")
	

if __name__ == "__main__":
	CWD = os.getcwd()
	test()
