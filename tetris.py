#This is a test with pygame to create an object that moves
#by Gilberto Rodriguez

import pygame, sys, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

LENGTH = 640
WIDTH = 640
GRID_LEN_START = LENGTH / 20
GRID_LEN_END = GRID_LEN_START * 11
PIECE_PLACE = (GRID_LEN_START + GRID_LEN_END) / 2 - 2 * GRID_LEN_START
GRID_WID = WIDTH / 22
GRID_TOP = 2 * GRID_WID
DIM = [LENGTH, WIDTH]
WINDOW = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption("Tetris Clone")

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
AQUA = pygame.Color(0, 255, 255)
PINK = pygame.Color(255, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
PURPLE = pygame.Color(128, 0, 128)

I = pygame.image.load("Images/I.png").convert()
L = pygame.image.load("Images/L.png").convert()
J = pygame.image.load("Images/J.png").convert()
O = pygame.image.load("Images/O.png").convert()
S = pygame.image.load("Images/S.png").convert()
Z = pygame.image.load("Images/Z.png").convert()
T = pygame.image.load("Images/T.png").convert()

mousex, mousey = 0, 0
inplay = False
timer = 0

class Piece:
	def __init__(self, image):
		self.image = image
		if self.image == I:
			self.image = pygame.transform.scale(self.image, 
[GRID_LEN_START * 4, GRID_WID])
		elif self.image == O:
			self.image = pygame.transform.scale(self.image, 
[GRID_LEN_START * 2, GRID_WID * 2])
		else:
			self.image = pygame.transform.scale(self.image, 
[GRID_LEN_START * 3, GRID_WID * 2])

		if self.image == S or self.image == Z:
			self.pos = [PIECE_PLACE, GRID_TOP + GRID_WID]
		else:
			self.pos = [PIECE_PLACE, GRID_TOP]

	def draw(self, window):
		if self.image == S or self.image == Z:
			window.blit(self.image, self.pos)
		else:
			window.blit(self.image, self.pos)
	
	def update(self):
		global inplay
		print self.pos
		if self.pos[1] >= WIDTH:
			print "TEST"
			inplay == False
			if self.image == I:
				self.pos[1] = WIDTH - GRID_WID
			else:
				self.pos[1] = WIDTH - 2 * GRID_WID
		else:
			self.pos[1] += GRID_WID
		print self.pos

def grid_set_up(window):
	for num in range(11):
		mult = num + 1
		pygame.draw.line(window, WHITE, [GRID_LEN_START * mult, GRID_TOP], 
[GRID_LEN_START * mult, WIDTH], 1)

	for num in range(22):
		mult = num + 1
		if num <= 20:
			pygame.draw.line(window, WHITE, 
[GRID_LEN_START, WIDTH - num * GRID_WID], [GRID_LEN_END, WIDTH - num * GRID_WID], 1)

#	pygame.draw.polygon(window, WHITE, [[400, 400], [400, 600], [600, 600], [600, 400]], 1)

def piece_select():
	global inplay
	piece = random.randrange(0, 7)
	if piece == 0:
		selected = Piece(I)
	elif piece == 1:
		selected = Piece(L)
	elif piece == 2:
		selected = Piece(J)
	elif piece == 3:
		selected = Piece(O)
	elif piece == 4:
		selected = Piece(S)
	elif piece == 5:
		selected = Piece(Z)
	elif piece == 6:
		selected = Piece(T)
	inplay = True
	return selected

while True:
	WINDOW.fill(BLACK)

	grid_set_up(WINDOW)
	
	if inplay == False:
		piece = piece_select()

	piece.draw(WINDOW)
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				pass
			elif event.key == K_RIGHT:
				pass
			elif event.key == K_UP:
				pass
			elif event.key == K_DOWN:
				pass
		elif event.type == KEYUP:
			if event.key == K_LEFT or event.key == K_RIGHT:
				pass
			elif event.key == K_UP or event.key == K_DOWN:
				pass

	if inplay == True:
		if timer % 30 == 0:
			piece.update()
			print inplay

	timer += 1	
	
	pygame.display.update()
	fpsClock.tick(30)
