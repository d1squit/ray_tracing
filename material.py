class Material ():
	def __init__ (self, color=(0, 0, 0)):
		self.color = color


class Color:
	def __init__(self, r, g, b):
		self.__color = (sorted((0, r, 255))[1], sorted((0, g, 255))[1], sorted((0, b, 255))[1])

	@property
	def color (self): return self.__color
	@color.setter
	def color (self, ncolor):
		return (sorted((0, self.__color[0], 255))[1], sorted((0, self.__color[1], 255))[1], sorted((0, self.__color[2], 255))[1])