from pygame import Vector3
import math
from material import *

class Sphere ():
	def __init__ (self, center, radius, material=Material()):
		self.center: Vector3 = center
		self.radius: float = radius
		self.material = material
		self.t = 0

	def ray_intersect (self, origin: Vector3, direction: Vector3):
		L: Vector3 = self.center - origin
		tca: float = L * direction
		d2: float = L * L - tca * tca
		if d2 > self.radius * self.radius: return False
		thc: float = math.sqrt(self.radius * self.radius - d2)
		self.t = tca - thc
		t1: float = tca + thc
		if self.t < 0: self.t = t1
		if self.t < 0: return False
		return True