from PIL import Image



def mix_rgb (colors):
	r, g, b = 0, 0, 0
	for color in colors:
		r += color[0]
		g += color[1]
		b += color[2]
	return (round(r / len(colors)), round(g / len(colors)), round(b / len(colors)))

def upscale (img):
	result = Image.new('RGB', (img.width * 2, img.height * 2))
	for ix in range(img.width - 1):
		for iy in range(img.height - 1):
			x, y = ix * 2, iy * 2
			for i in range(2):
				for j in range(2):
					if i == j == 0: result.putpixel((x, y), img.getpixel((ix, iy)))
					elif i == j == 1: result.putpixel((x + i, y + j), mix_rgb([img.getpixel((ix, iy)), img.getpixel((ix + 1, iy)), img.getpixel((ix, iy + 1)), img.getpixel((ix + 1, iy + 1))]))
					else:
						if i == 1: result.putpixel((x + i, y), mix_rgb([img.getpixel((ix, iy)), img.getpixel((ix + i, iy))]))
						if j == 1: result.putpixel((x, y + j), mix_rgb([img.getpixel((ix, iy)), img.getpixel((ix, iy + j))]))
	return result
