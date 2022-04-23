import sys
from light import Light
from sphere import *
import pygame
from PIL import Image
from upscaling import *

width =	75
height = 75

fov: float = math.pi / 3

red = Material((255, 0, 0))
blue = Material((0, 0, 255))
green = Material((0, 255, 0))

res_image = Image.new('RGB', (width, height))
upscaled = Image.new('RGB', (width * 2, height * 2))

N = Vector3()
material = Material()
point = Vector3()
cx, cy, cz = 0, 0, 0
dir = Vector3()
angle = Vector3()

quality = 0.75


pygame.init()
pygame.display.set_caption("RayTracing")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
window = pygame.display.set_mode((width, height), pygame.NOFRAME)

fps_clock = pygame.time.Clock()

def scene_intersect(origin: Vector3, direction: Vector3, spheres):
	global N
	global point
	global material

	spheres_dist: float = float('inf')

	for sphere in spheres:
		if sphere.ray_intersect(origin, direction):
			if sphere.t < spheres_dist:				
				spheres_dist = sphere.t
				point = origin + direction * spheres_dist
				N = (point - sphere.center).normalize()
				material = sphere.material
				
				

	return spheres_dist < 1000


def cast_ray (origin: Vector3, direction: Vector3, spheres, lights):
	if not scene_intersect(origin, direction, spheres): return Color(0, 0, 150)

	diffuse_light_intensity = 0
	for i in lights:
		light_dir: Vector3 = (i.position - point).normalize()
		diffuse_light_intensity += i.intensity * max([0, light_dir * N])

	for sphere in spheres:
		if sphere.ray_intersect(origin, direction): return Color(int(material.color[0] * diffuse_light_intensity), int(material.color[1] * diffuse_light_intensity), int(material.color[2] * diffuse_light_intensity))
	return Color(255, 255, 255)

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

def render (spheres, lights):
	for j in range(int(height)):
		for i in range(int(width)):
			x: float =  (2 * (i + 0.5) / float(width)  - 1) * math.tan(fov / 2) * width / float(height)
			y: float = -(2 * (j + 0.5) / float(height) - 1) * math.tan(fov / 2)
			dir = Vector3(x, y, -1).normalize().rotate(angle.x, Vector3(1, 0, 0)).rotate(angle.y, Vector3(0, 1, 0))
			# window.set_at((i, j), cast_ray(Vector3(cx, cy, cz), dir, spheres, lights).color)
			res_image.putpixel((i, j), cast_ray(Vector3(cx, cy, cz), dir, spheres, lights).color)

	
lights = [Light(Vector3(-20, 20, 20), 1.5)]

spheres = [Sphere(Vector3(-3, 0, -16), 2, blue),
		  Sphere(Vector3(-1, -1.5, -12), 2, green)]
# render(spheres, lights)
# upscaled = upscale(res_image)
# upscaled.save('upscaled.png')
# res_image.save('result.png')

while (1):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_a]: cx -= 0.5
	elif keys_pressed[pygame.K_d]: cx += 0.5
	elif keys_pressed[pygame.K_w]: cz -= 0.5
	elif keys_pressed[pygame.K_s]: cz += 0.5
	elif keys_pressed[pygame.K_q]: cy -= 0.5
	elif keys_pressed[pygame.K_e]: cy += 0.5

	if keys_pressed[pygame.K_UP]: angle.x += 5
	elif keys_pressed[pygame.K_DOWN]: angle.x -= 5
	if keys_pressed[pygame.K_LEFT]: angle.y += 5
	elif keys_pressed[pygame.K_RIGHT]: angle.y -= 5

	render(spheres, lights)
	# upscaled = upscale(res_image)
	# window.blit(pilImageToSurface(upscaled), (0, 0))
	window.blit(pilImageToSurface(res_image), (0, 0))
	pygame.display.update()