#!/usr/bin/python3

from math import sin, cos, sqrt
import os

from OpenGL.GL import *
import pygame
from pygame.locals import *

class Vector2(object):
	
	#Takes two (int or float) or one (tuple, list, or Vector2) or no args defaults (0,0) vector
	def __init__(self, *args):
		self.x, self.y = self.parse_vector_arg(args, "Vector2")
	
	#Handles expecting one vector argument as ints, floats, tuple, list, Vector2; Returns tuple (x, y)
	@classmethod
	def parse_vector_arg(self, args, name):
		if not args:
			return (0,0)
		elif len(args) == 1:
			if isinstance(args[0], Vector2): return (args[0].x, args[0].y)
			else: return (args[0][0], args[0][1])
		elif len(args) == 2:
			return (args[0], args[1])
		else: raise TypeError(name + " takes 0, 1, or 2 arguments (" + str(len(args)) + " given)")

	#Handles expecting two vector arguments as ints, floats, tuples, lists, Vector2s; Returns tuple (x1, y1, x2, y2)
	@classmethod
	def parse_vector_args(self, args, name):
		if len(args) == 1: return (args[0][0], args[0][1], args[0][2], args[0][3])
		elif len(args) == 2:
			ivec = []
			for index in range(2):
				if isinstance(args[index], Vector2):
					ivec.append(args[index].x)
					ivec.append(args[index].y)
				else:
					ivec.append(args[index][0])
					ivec.append(args[index][1])
			return (ivec[0], ivec[1], ivec[2], ivec[3])
		elif len(args) == 4: return (args[0], args[1], args[2], args[3])
		else: raise TypeError(name + " takes 1, 2, or 4 arguments (" + str(len(args)) + " given)")

	def __repr__(self):
		return "Vector2(" + str(self.x) + ", " + str(self.y) + ")"

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

	#Returns tuple vector
	def tuple(self):
		return (self.x, self.y)

	#Returns list vector
	def list(self):
		return [self.x, self.y]

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
	
	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_xy(self, *args):
		self.x, self.y = self.parse_vector_arg(args, "set_xy")

	def get_xy(self):
		return self.x, self.y

	def magnitude(self):
		return sqrt( self.x**2 + self.y**2 ) 
	
	#Normalizes THIS vector
	def normalize(self):
		self.x = self.x / self.magnitude()
		self.y = self.y / self.magnitude() 

	#Returns new normalized Vector2 object
	def get_normal(self):
		return Vector2(self.x / self.magnitude(), self.y / self.magnitude())

	#Negates THIS vector
	def negate(self):
		self.x, self.y = -self.x, -self.y

	#Returns new negated Vector2 object
	def get_negation(self):
		return Vector2(-self.x, -self.y)
	
	#Overloads negation operator; returns new negated Vector2 object
	def __neg__(self):
		return self.get_negation()

	#Determines distance between two vector endpoints; returns magnitude	
	def distance_to(self, *args):
		ivec = self.parse_vector_arg(args, "distance_to") 
		return sqrt( (ivec[0] - self.x)**2 + (ivec[1] - self.y)**2 )
		
	#Determines vector required to get to given vector endpoint from this vector's endpoint; returns new Vector2 object
	def get_to(self, *args):
		ivec = self.parse_vector_arg(args, "get_to")
		return Vector2(ivec[0] - self.x, ivec[1] - self.y)

	#Adds given vector to this vector; returns new Vector2 object
	def add(self, *args):
		ivec = self.parse_vector_arg(args, "add")
		return Vector2(self.x + ivec[0], self.y + ivec[1])

	#Adds two given vectors; returns new Vector2 object
	@classmethod
	def add_using(self, *args):
		ivec = Vector2.parse_vector_args(args, "add_using")
		return Vector2(ivec[0], ivec[1]) + Vector2(ivec[2], ivec[3])

	#Overloads + operator; adds given vector to this vector; returns new Vector2 object
	def __add__(self, ivec):
		return self.add(ivec)

	#Subtracts given vector from this vector; returns new Vector2 object
	def subtract(self, *args):
		ivec = self.parse_vector_arg(args, "subtract")
		return Vector2(self.x - ivec[0], self.y - ivec[1])

	#Subtracts second given vector from the first given vector; returns new Vector2 object
	@classmethod
	def subtract_using(self, *args):
		ivec = Vector2.parse_vector_args(args, "subtract_using")
		return Vector2(ivec[0], ivec[1]) - Vector2(ivec[2], ivec[3])

	#overloads - operator; substracts given vector from this vector; returns vew Vector2 object
	def __sub__(self, ivec):
		return self.subtract(ivec)
	
	#Multiplies this vector by a given scalar; returns new Vector2 object
	def multiply(self, scalar):
		return Vector2(self.x * scalar, self.y * scalar)

	#Overloads the * operator; multiplies vector by a given scalar; returns new Vector2 object
	def __mul__(self, scalar):
		return self.multiply(scalar)

	#Divides this vector by a given scalar; returns new Vector2 object
	def divide(self, scalar):
		return Vector2(self.x / scalar, self.y / scalar)

	#Overloads / operator; divides vector by a given scalar; returns new Vector2 object
	def __truediv__(self, scalar):
		return self.divide(scalar)

	#Determines dot product between this vector and given vector; returns scalar
	def dot(self, *args):
		ivec = self.parse_vector_arg(args, "dot")
		return (self.x * ivec[0]) + (self.y * ivec[1])

	#Determines dot prodruct between two given vectors; returns scalar
	@classmethod
	def dot_using(self, *args):
		ivec = Vector2.parse_vector_args(args, "dot_using")
		return Vector2(ivec[0], ivec[1]).dot(Vector2(ivec[2], ivec[3]))
	
	#Determines vector between two given vectors; returns new Vector2 object
	@classmethod
	def create_using(self, *args):
		ivec = Vector2.parse_vector_args(args, "create_using")
		return Vector2(ivec[0], ivec[1]).get_to(Vector2(ivec[2], ivec[3]))

class Vector3(object):

	#Takes three (int or float) or one (tuple, list, or Vector3) or no args defaults (0,0,0) vector
	def __init__(self, *args):
		self.x, self.y, self.z = self.parse_vector_arg(args, "Vector3")

	#Handles expecting one vector argument as ints, floats, tuple, list, Vector3; Returns tuple (x, y, z)
	@classmethod
	def parse_vector_arg(self, args, name):
		if not args:
			return (0, 0, 0)
		elif len(args) == 1:
			if isinstance(args[0], Vector3): return (args[0].x, args[0].y, args[0].z)
			else: return (args[0][0], args[0][1], args[0][2])
		elif len(args) == 3:
			return (args[0], args[1], args[2])
		else: raise TypeError(name + " takes 0, 1, or 3 arguments (" + str(len(args)) + " given)")

	#Handles expecting two vector arguments as ints, floats, tuples, lists, Vector3s; Returns tuple (x1, y1, z1, x2, y2, z2)
	@classmethod
	def parse_vector_args(self, args, name):
		if len(args) == 1: return Vector3(args[0][0], args[0][1], args[0][2]), Vector3(args[0][3], args[0][4], args[0][5])
		elif len(args) == 2:
			ivec = []
			for index in range(2):
				if isinstance(args[index], Vector3):
					ivec.append(args[index].x)
					ivec.append(args[index].y)
					ivec.append(args[index].z)
				else:
					ivec.append(args[index][0])
					ivec.append(args[index][1])
					ivec.append(args[index][2])
			return Vector3(ivec[0], ivec[1], ivec[2]), Vector3(ivec[3], ivec[4], ivec[5])
		elif len(args) == 6: return Vector3(args[0], args[1], args[2]), Vector3(args[3], args[4], args[5])
		else: raise TypeError(name + " takes 1, 2, or 6 arguments (" + str(len(args)) + " given)")

	def __repr__(self):
		return "Vector3(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

	#Returns tuple vector
	def tuple(self):
		return (self.x, self.y, self.z)

	#Returns list vector
	def list(self):
		return [self.x, self.y, self.z]

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z
	
	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_z(self, z):
		self.z = z
	
	def set_xyz(self, *args):
		ivec = Vector3.parse_vector_arg(args, "set_xyz")
		self.x, self.y, self.z = ivec.x, ivec.y, ivec.z

	def get_xyz(self):
		return self.x, self.y, self.z

	def magnitude(self):
		return sqrt( self.x**2 + self.y**2 + self.z**2 ) 

	#Normalizes THIS vector
	def normalize(self):
		self.x = self.x / self.magnitude()
		self.y = self.y / self.magnitude()
		self.z = self.z / self.magnitude()

	#Returns new normalized Vector3 object
	def get_normal(self):
		return Vector3(self.x / self.magnitude(), self.y / self.magnitude(), self.z / self.magnitude())

	#Negates THIS vector
	def negate(self):
		self.x, self.y, self.z = -self.x, -self.y, -self.z

	#Returns new negated Vector3 object
	def get_negation(self):
		return Vector3(-self.x, -self.y, -self.z)

	#Overloads negation operator; returns new negated Vector3 object
	def __neg__(self):
		return self.get_negation()

	#Determines distance between two vector endpoints; returns magnitude	
	def distance_to(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "distance_to")) 
		return sqrt( (ivec.x - self.x)**2 + (ivec.y - self.y)**2 + (ivec.z - self.z)**2 )

	#Determines vector required to get to given vector endpoint from this vector's endpoint; returns new Vector3 object
	def get_to(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "get_to"))
		return Vector3(ivec.x - self.x, ivec.y - self.y, ivec.z - self.z)

	#Adds given vector to this vector; returns new Vector3 object
	def add(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "add"))
		return Vector3(self.x + ivec.x, self.y + ivec.y, self.z + ivec.z)

	#Adds two given vectors; returns new Vector3 object
	@classmethod
	def add_using(self, *args):
		ivec1, ivec2 = Vector3.parse_vector_args(args, "add_using")
		return ivec1 + ivec2

	#Overloads + operator; adds given vector to this vector; returns new Vector3 object
	def __add__(self, ivec):
		return self.add(ivec)

	#Subtracts given vector from this vector; returns new Vector3 object
	def subtract(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "subtract"))
		return Vector3(self.x - ivec.x, self.y - ivec.y, self.z - ivec.z)

	#Subtracts second given vector from the first given vector; returns new Vector3 object
	@classmethod
	def subtract_using(self, *args):
		ivec1, ivec2 = Vector3.parse_vector_args(args, "subtract_using")
		return ivec1 - ivec2

	#overloads - operator; substracts given vector from this vector; returns vew Vector3 object
	def __sub__(self, ivec):
		return self.subtract(ivec)

	#Multiplies this vector by a given scalar; returns new Vector3 object
	def multiply(self, scalar):
		return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

	#Overloads the * operator; multiplies vector by a given scalar; returns new Vector3 object
	def __mul__(self, scalar):
		return self.multiply(scalar)

	#Divides this vector by a given scalar; returns new Vector3 object
	def divide(self, scalar):
		return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

	#Overloads / operator; divides vector by a given scalar; returns new Vector3 object
	def __truediv__(self, scalar):
		return self.divide(scalar)

	#Determines dot product between this vector and given vector; returns scalar
	def dot(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "dot"))
		return (self.x * ivec.x) + (self.y * ivec.y) + (self.z * ivec.z)

	#Determines dot prodruct between two given vectors; returns scalar
	@classmethod
	def dot_using(self, *args):
		ivec1, ivec2 = Vector3.parse_vector_args(args, "dot_using")
		return ivec1.dot(ivec2)

	#Determines cross product between this vector and given vector; returns new Vector3 object
	def cross(self, *args):
		ivec = Vector3(self.parse_vector_arg(args, "cross"))
		x = (self.y * ivec.z) - (self.z * ivec.y)
		y = (self.z * ivec.x) - (self.x * ivec.z)
		z = (self.x * ivec.y) - (self.y * ivec.x)
		return Vector3(x,y,z)

	#Determines cross product between two given vectors; returns new Vector3 object
	@classmethod
	def cross_using(self, *args):
		ivec1, ivec2 = self.parse_vector_args(args, "cross_using")
		return ivec1.cross(ivec2)

	#Determines vector between two given vectors; returns new Vector3 object
	@classmethod
	def create_using(self, *args):
		ivec1, ivec2 = Vector3.parse_vector_args(args, "create_using")
		return ivec1.get_to(ivec2)

class Matrix44(object):

	def __init__(self, *args):
		self.matrix = self.parse_matrix_arg(args, "Matrix44")

	#Handles expecting one 4x4 matrix argument as ints, floats, tuples, lists, or Vector3 objects; returns list
	@classmethod
	def parse_matrix_arg(self, args, name):
		if len(args) == 0: return [ [1, 0, 0, 0],
									[0, 1, 0, 0],
									[0, 0, 1, 0],
									[0, 0, 0, 1] ]
		elif len(args) == 1:
			if isinstance(args[0], Matrix44): return args[0].list()
			else: return [ args[0][0], args[0][1], args[0][2], args[0][3] ]
		elif len(args) == 4:
			if isinstance(args[0], Vector3): return [ args[0].list().append(0),
													args[1].list().append(0),
													args[2].list().append(0),
													args[3].list().append(1) ]
			else: return [ args[0], args[1], args[2], args[3] ]
		elif len(args) == 16: return [ [args[0], args[1], args[2], args[3] ],
										[args[4], args[5], args[6], args[7] ],
										[args[8], args[9], args[10], args[11] ],
										[args[12], args[13], args[14], args[15] ] ]
		else: raise TypeError(name + " was provided an incorrect number of arguments (" + str(len(args)) + " given)")

	def __repr__(self):
		return "Matrix44(" + str(self.matrix) + ")"

	def __str__(self):
		return str(self.matrix)

	def set(self, *args):
		self.matrix = self.parse_matrix_args(args, "set")

	#Resets THIS Matrix44 object to the identity matrix
	def reset_identity(self):
		self = Matrix44()

	#Returns a list matrix
	def list(self):
		return self.matrix

	#Returns a tuple matrix
	def tuple(self):
		return (tuple(self.matrix[0]), tuple(self.matrix[1]), tuple(self.matrix[2]), tuple(self.matrix[3]))
	
	#Overloads the index [] operator; gets a single element of this Matrix44 object
	def __getitem__(self, index):
		return self.matrix[index[0]][index[1]]

	#Overloads the index [] operator; sets a single element of this Matrix44 object
	def __setitem__(self, index, value):
		self.matrix[index[0]][index[1]] = value

	def get_row(self, row):
		return self.matrix[row]

	def get_col(self, col):
		col_list = []
		for index in range(4):
			col_list.append(self.matrix[index][col])
		return col_list

	#Returns Vector3 version of row
	def get_row_v(self, row):
		return Vector3( (self.matrix[row][0], self.matrix[row][1], self.matrix[row][2]) )

	#Returns Vector3 version of column
	def get_col_v(self, col):
		col_list = []
		for index in range(3):
			col_list.append(self.matrix[index][col])
		return Vector3( (col_list[0], col_list[1], col_list[2]) )

	def set_row(self, row, ivec):
		if isinstance(ivec, Vector3): self.matrix[row] = [ ivec.x, ivec.y, ivec.z, self.matrix[row][3] ]
		else:
			if isinstance(ivec, tuple):ivec = list(ivec)
			if len(ivec) == 4: self.matrix[row] = ivec
			else:
				self.matrix[row][0] = ivec[0]
				self.matrix[row][1] = ivec[1]
				self.matrix[row][2] = ivec[2]

	def set_col(self, col, ivec):
		if isinstance(ivec, Vector3): ivec = ivec.list()
		if isinstance(ivec, tuple): ivec = list(ivec)
		for index in range(len(ivec)):
			self.matrix[index][col] = ivec[index]

	def multiply(self, *args):
		I = Matrix44(self.parse_matrix_arg(args, "multiply"))
		M = self
		return Matrix44(M[0,0]*I[0,0] + M[0,1]*I[1,0] + M[0,2]*I[2,0] + M[0,3]*I[3,0],
						M[0,0]*I[0,1] + M[0,1]*I[1,1] + M[0,2]*I[2,1] + M[0,3]*I[3,1],
						M[0,0]*I[0,2] + M[0,1]*I[1,2] + M[0,2]*I[2,2] + M[0,3]*I[3,2],
						M[0,0]*I[0,3] + M[0,1]*I[1,3] + M[0,2]*I[2,3] + M[0,3]*I[3,3],

						M[1,0]*I[0,0] + M[1,1]*I[1,0] + M[1,2]*I[2,0] + M[1,3]*I[3,0],
						M[1,0]*I[0,1] + M[1,1]*I[1,1] + M[1,2]*I[2,1] + M[1,3]*I[3,1],
						M[1,0]*I[0,2] + M[1,1]*I[1,2] + M[1,2]*I[2,2] + M[1,3]*I[3,2],
						M[1,0]*I[0,3] + M[1,1]*I[1,3] + M[1,2]*I[2,3] + M[1,3]*I[3,3],

						M[2,0]*I[0,0] + M[2,1]*I[1,0] + M[2,2]*I[2,0] + M[2,3]*I[3,0],
						M[2,0]*I[0,1] + M[2,1]*I[1,1] + M[2,2]*I[2,1] + M[2,3]*I[3,1],
						M[2,0]*I[0,2] + M[2,1]*I[1,2] + M[2,2]*I[2,2] + M[2,3]*I[3,2],
						M[2,0]*I[0,3] + M[2,1]*I[1,3] + M[2,2]*I[2,3] + M[2,3]*I[3,3],

						M[3,0]*I[0,0] + M[3,1]*I[1,0] + M[3,2]*I[2,0] + M[3,3]*I[3,0],
						M[3,0]*I[0,1] + M[3,1]*I[1,1] + M[3,2]*I[2,1] + M[3,3]*I[3,1],
						M[3,0]*I[0,2] + M[3,1]*I[1,2] + M[3,2]*I[2,2] + M[3,3]*I[3,2],
						M[3,0]*I[0,3] + M[3,1]*I[1,3] + M[3,2]*I[2,3] + M[3,3]*I[3,3])

	def __mult__(self, *args):
		return self.multiply(args)

	def set_translation(self, ivec):
		self.set_row(3, ivec)

	def get_translation(self):
		return self.get_row_v(3)

	def translate(self, *args):
		ivec = Vector3(Vector3.parse_vector_arg(args, "translate"))
		m = self.matrix
		return Vector3(ivec.x + m[3][0], ivec.y + m[3][1], ivec.z + m[3][2])

	def set_rotation(self, *args):
		ivec = Vector3(Vector3.parse_vector_arg(args, "set_rotation"))

	#def get_rotation(self):

	#def rotate(self, *args):

	#Transforms given vector; returns new Vector3 object
	def transform(self, *args):
		ivec = Vector3(Vector3.parse_vector_arg(args, "transform"))
		M = self.matrix
		return Vector3( ivec.x * M[0][0] + ivec.x * M[1][0] + ivec.x * M[2][0] + M[3][0],
						ivec.y * M[0][1] + ivec.y * M[1][1] + ivec.y * M[2][1] + M[3][1],
						ivec.z * M[0][2] + ivec.z * M[1][2] + ivec.z * M[2][2] + M[3][2] )

	def scale(self, *args):
		if len(args) == 1:
			self.matrix[0][0] *= args[0]
			self.matrix[1][1] *= args[0]
			self.matrix[2][2] *= args[0]
		else:
			ivec = Vector3.parse_vector_args(args, "scale")
			self.matrix[0][0] *= ivec[0]
			self.matrix[1][1] *= ivec[1]
			self.matrix[2][2] *= ivec[2]
	
	def set_scale(self, *args):
		ivec = Vector3.parse_vector_arg(args, "set_scale")
		self.matrix[0][0] = ivec[0]
		self.matrix[1][1] = ivec[1]
		self.matrix[2][2] = ivec[2]

	def get_scale(self):
		return Vector3(self.matrix[0][0], self.matrix[1][1], self.matrix[2][2])


def vector2_test():
	print("--- Testing Vector2 Class ---")
	vec_d = Vector2()
	vec_i = Vector2(0,2)
	vec_t = Vector2( (3,4) )
	vec_l = Vector2( [5,6] )
	if vec_d.list() == [0,0] and vec_i.list() == [0,2] and vec_t.list() == [3,4] and vec_l.list() == [5,6]:
		print("Vector Instantiation: Success")
	else:
		print("Vector Instantiation: Failure")

	if vec_i.magnitude() == 2: print("Magnitude: Success")
	else: print("Magnitude: Failure")

	if vec_i.get_normal().list() == [0,1]: print("Normal: Success")
	else: print("Normal: Failure")
 
	if (-vec_t).list() == [-3,-4]: print("Negation: Success")
	else: print("Negation: Failure")

	if vec_i.distance_to(0,0) == 2: print("Distance To: Success")
	else: print("Distance To: Failure")

	if vec_l.get_to(0,0).list() == [-5,-6]: print("Get To: Success")
	else: print("Get To: Failure")

	if Vector2.create_using(vec_d, vec_t).list() == [3,4]: print("Create Using: Success")
	else: print("Create Using: Failure")

	if Vector2.add_using(vec_d, vec_t).list() == [3,4]: print("Vector Addition: Success")
	else: print("Vector Addition: Failure")

	if Vector2.subtract_using(vec_d, vec_t).list() == [-3,-4]: print("Vector Subtraction: Success")
	else: print("vector Subtraction: Failure")

	if (vec_i * 4).list() == [0,8]: print("Vector Multiplication: Success")
	else: print("Vector Multiplication: Failure")

	if (vec_i / 2).list() == [0,1]: print("Vector Division: Success")
	else: print("Vector Division: Failure")

	if Vector2.dot_using((0,2), vec_l) == 12: print("Vector Dot Product: Success")
	else: print("Vector Dot Product: Failure")
	
def vector3_test():
	print("--- Testing Vector3 Class ---")
	vec_d = Vector3()
	vec_i = Vector3(0,2,0)
	vec_t = Vector3( (3,4,0) )
	vec_l = Vector3( [5,6,0] )
	if vec_d.list() == [0,0,0] and vec_i.list() == [0,2,0] and vec_t.list() == [3,4,0] and vec_l.list() == [5,6,0]:
		print("Vector Instantiation: Success")
	else:
		print("Vector Instantiation: Failure")

	if vec_i.magnitude() == 2: print("Magnitude: Success")
	else: print("Magnitude: Failure")

	if vec_i.get_normal().list() == [0,1,0]: print("Normal: Success")
	else: print("Normal: Failure")
 
	if (-vec_t).list() == [-3,-4,0]: print("Negation: Success")
	else: print("Negation: Failure")

	if vec_i.distance_to(0,0,0) == 2: print("Distance To: Success")
	else: print("Distance To: Failure")

	if vec_l.get_to(0,0,0).list() == [-5,-6,0]: print("Get To: Success")
	else: print("Get To: Failure")

	if Vector3.create_using(vec_d, vec_t).list() == [3,4,0]: print("Create Using: Success")
	else: print("Create Using: Failure")

	if Vector3.add_using(vec_d, vec_t).list() == [3,4,0]: print("Vector Addition: Success")
	else: print("Vector Addition: Failure")

	if Vector3.subtract_using(vec_d, vec_t).list() == [-3,-4,0]: print("Vector Subtraction: Success")
	else: print("vector Subtraction: Failure")

	if (vec_i * 4).list() == [0,8,0]: print("Vector Multiplication: Success")
	else: print("Vector Multiplication: Failure")
	
	if (vec_i / 2).list() == [0,1,0]: print("Vector Division: Success")
	else: print("Vector Division: Failure")

	if Vector3.dot_using((0,2,0), vec_l) == 12: print("Vector Dot Product: Success")
	else: print("Vector Dot Product: Failure")
	
	if Vector3.cross_using(0,0,1,1,0,0).list() == [0,1,0]: print("Vector Cross Product: Success")
	else: print("Vector Cross Product: Failure")

def matrix44_test():
	print("--- Testing Matrix44 Class ---")
	mat = Matrix44()
	mat2 = Matrix44(mat)
	mat3 = Matrix44( [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1] )
	mat4 = Matrix44(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
	if mat.list() == mat2.list() and mat3.list() == mat4.list(): print("Matrix44 Instantiation: Success")
	else: print("Matrix44 Instantiation: Failure")
	
	print(mat4.multiply(mat3))

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


class Obj_Object(object):

	def __init__(self, name):
		self.name = name
		self.face_groups = []


class Obj_Reader(object):

	def __init__(self):
		self.obj_filename = None
		self.obj_filepath = None
		self.tex_filepath = None
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
				self.obj_list.append(Obj_Object(name=data[0]))
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
					tex_surface = pygame.image.load(self.tex_filepath
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
				#if texture_id != None:
					#glBindTexture(GL_TEXTURE_2D, texture_id) ########3
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
		return self.display_list

	def proc_indexes(self, index):
		if index[1] == '': index[1] = 0 
		if index[2] == '': index[2] = 0
		return (int(index[0]), int(index[1]), int(index[2]))


class Object_Viewer(object):

	CWD = os.getcwd()
	OBJ_FILEPATH = CWD + '/obj/'
	WINDOW_CAPTION = 'Game Object Viewer'
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)
	ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
	DEFAULT_DISTANCE = -3
	LIGHT_POSITION = (0, 0, 2, 0)  #Update: ?
	DEFAULT_AMBIENT = (0.1, 0.1, 0.1)  #Update: ?
	DEFAULT_DIFFUSE = (0.5, 0.5, 0.5)  #Update: ?
	DEFAULT_COLOR = (0.5,0.5,0.5)  #Update: ?
	PYGAME_MODE = HWSURFACE|DOUBLEBUF|OPENGL|RESIZABLE
	FIELD_OF_VIEW = 60
	Z_NEAR = 0.1
	Z_FAR = 1000.0
	ROTATION_SPEED = 15.0 
	ZOOM_SPEED = 0.5  #Meters per scroll 
	TRANSLATE_SPEED = 5
	WIREFRAME = False

	def __init__(self, *args):
		self.handle_args(args)
		self.init()
		self.main()

	def handle_args(self, args):
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
		glClearColor(0, 0, 0.5, 1)  #Update: unhardcode
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
		self.mouse_event_v3 = Vector3()
		self.rot_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
		self.tran_pos_v3 = Vector3(0, 0, DEFAULT_DISTANCE)
		self.clock = pygame.time.Clock()

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
		glPushMatrix()
		glLoadIdentity()
		self.rot_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
		glPopMatrix()

	def rotate_object(self):
		if self.mouse_event_v3.y == 1.0:
			glPushMatrix()
			glLoadIdentity()
			delta_y, delta_x = pygame.mouse.get_rel()
			delta_y *= self.frame_time_seconds * ROTATION_SPEED
			delta_x *= self.frame_time_seconds * ROTATION_SPEED
			glRotate(delta_x, 1, 0, 0)
			glRotate(delta_y, 0, 1, 0)
			glMultMatrixf(self.rot_matrix)
			self.rot_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)  #Update: Too slow
			glPopMatrix()

	def transform_object(self):
		if self.mouse_event_v3.x == 1.0:
			delta_x, delta_y = pygame.mouse.get_rel()
			self.tran_pos_v3.x += delta_x * self.frame_time_seconds
			self.tran_pos_v3.y -= delta_y * self.frame_time_seconds
		glTranslate(self.tran_pos_v3.x,
					self.tran_pos_v3.y,
					self.tran_pos_v3.z)

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
			elif (event.type == pygame.MOUSEBUTTONDOWN and
				  pygame.mouse.get_focused()):
					if event.button == 1:
						self.mouse_event_v3.x = 1.0
						pygame.mouse.get_rel()  #Dumps init rel
					if event.button == 2:
						self.mouse_event_v3.y = 1.0
						pygame.mouse.get_rel()  #Dumps init rel
					if event.button == 3:
						self.reset_orientation()
					if event.button == 4:
						self.tran_pos_v3.z += ZOOM_SPEED
					if event.button == 5:
						self.tran_pos_v3.z -= ZOOM_SPEED
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.mouse_event_v3.x = 0
				if event.button == 2:
					self.mouse_event_v3.y = 0

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
			self.handle_events()
			self.handle_time()
			self.clear_frame_buffer()
			self.draw_object()
			pygame.display.flip()
		self.cleanup()

	def cleanup(self):
		pygame.quit()


class Game_Object(object):

	def __init__(self, obj_id):
		self.name = None
		self.id = obj_id
		self.model = None
		self.display_list = None


class Obj_Data(object):

	def __init__(self, datapath, dataname, texpath):
		self.data_filepath = datapath
		self.data_filename = dataname
		self.tex_filepath = texpath
		self.game_objects = {}

	def read(self):
		data_file = open(self.data_filepath + self.data_filename, 'r')
		for line in data_file:
			line = line.rstrip()
			if line == '': continue  #Empty Line
			line_elements = line.split()
			command, data = line_elements[0], line_elements[1:]
			if command == '#':
				continue
			elif command == 'o':
				obj = Game_Object(int(data[0]))
				self.game_objects[int(data[0])] = obj
			elif command == 'name':
				obj.name = data[0]
				self.game_objects[obj.id] = obj
			elif command == 'model':
				obj.model = data[0]
				self.game_objects[obj.id] = obj
		data_file.close()

	def load(self):
		self.reader = Obj_Reader()
		self.reader.obj_filepath = self.data_filepath
		self.reader.tex_filepath = self.tex_filepath
		for obj in self.game_objects:
			self.reader.obj_filename = self.game_objects[obj].model
			self.reader.read()
			self.game_objects[obj].display_list = self.reader.load()


class World_Data(object):

	def __init__(self, datapath, dataname):
		self.data_filepath = datapath
		self.data_filename = dataname
		self.name = None
		self.spawn = None
		self.object_list = []

	def read(self):
		data_file = open(self.data_filepath + self.data_filename, 'r')
		for line in data_file:
			line = line.rstrip()
			if line == '': continue  #Empty Line
			line_elements = line.split()
			command, data = line_elements[0], line_elements[1:]
			if command == '#':
				continue
			elif command == 'name':
				self.name = data[0]
			elif command == 'spawn':
				self.spawn = (int(data[0]), int(data[1]), int(data[2]))
			elif command == 'o':
				self.object_list.append([int(data[0]), int(data[1]), int(data[2]), int(data[3])])

def test():
	print('No detectable errors. ^_^')

if __name__ == '__main__':
	test()
