import pygame
import sys
import time
import random
pygame.font.init()


# global variables
sw, sh = 800, 600
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("yo mama")
clock = pygame.time.Clock()
fps = 60

# fonts and colors
font = pygame.font.SysFont("comicsans", 50)

white = (250, 250, 250)
black = (0, 0, 0)
green = (0, 250, 0)
red = (200, 0, 0)
blue = (0, 0, 0)
bg_color = (94, 129, 162)


# game functions
def draw_text(txt, font, color, x, y):
	img = font.render(txt, 1, color)
	rect = img.get_rect(center=(x, y))
	screen.blit(img, rect)

def draw_img(img, x, y):
	rect = img.get_rect(center=(x, y))
	screen.blit(img, rect)



class Blob:
	def __init__(self, img, x, y):
		self.img = img 
		self.rect = self.img.get_rect(center=(x, y))

	def draw(self):
		draw_img(self.img, self.rect.x, self.rect.y)

	def goto(self, coords):
		pass



blob_img = pygame.image.load("images/blob.png").convert_alpha()
earl = Blob(blob_img, sw//2, sh//2)


run = True
while run:

	clock.tick(fps)
	screen.fill(bg_color)

	earl.draw()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			run = False





	pygame.display.update()

pygame.quit()
sys.exit()
