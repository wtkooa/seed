#!/usr/bin/python3

from math import sin, cos, sqrt

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

if __name__ == "__main__":
	vector2_test()
	vector3_test()
	matrix44_test()
