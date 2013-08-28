#This is a test with pygame to create an object that moves and shoots
#by Gilberto Rodriguez
#!/usr/bin/python

import pygame, sys, math, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

LENGTH = 640
WIDTH = 480
DIM = [LENGTH, WIDTH]
WINDOW = pygame.display.set_mode((LENGTH, WIDTH))
PI = 3.1415926535

pygame.display.set_caption("This is a test")

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
mousex, mousey = 0, 0
timer = 0
in_play = False

def find_angle(circle, mouse_x, mouse_y):
	circle_pos = circle.get_pos()
	result = math.atan2((mouse_y - circle_pos[1]),  (mouse_x - circle_pos[0]))
	return result

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def kill_group(group):
    for item in list(group):
        group.remove(item)
    
def process_group(group, canvas):
    for item in list(group):
        item.draw(canvas)
        if item.update():
            group.remove(item)

def group_collide(group, other_object):
    collisions = 0
    for item in list(group):
        if item.collide(other_object):
            	collisions += 1
		explosion_array.append(Circle(GREEN, item.get_pos(), [0, 0], 0, 0, 100, True))
        	group.remove(item)
    return collisions

def group_group_collide(group1, group2):
    total_collisions = 0
    for item in list(group1):
        collisions = group_collide(group2, item)
        if collisions != 0:
            total_collisions += collisions
            group1.remove(item)
    return total_collisions

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def spawn_enemy():
	if len(enemy_array) < 10:
		rand_pos = [0, 0]
		rand_vel = [0, 0]
		for index in range(2):
			while True:
				rand_pos[index] = random.randrange(0, DIM[index])
				if abs(rand_pos[index] - test.get_pos()[index]) > 20:
					break 
			rand_vel[index] = random.randint(-5, 5)
		enemy_array.append(Circle(RED, rand_pos, rand_vel, 10, 0))

def title_screen(window):
	title_text.draw(window)
	if play_text.rect.collidepoint(pygame.mouse.get_pos()):
       		play_text.hovered = True
       	else:
       	    	play_text.hovered = False
	play_text.draw(window)

        
class Circle:
	def __init__(self, color, position, velocity, raidus, filled_in, life = 0, animate = False):
		self.color = color
		self.pos = position
		self.vel = velocity 
		self.rad = raidus
		self.fill = filled_in
		self.life = life
		self.angle = 0
		self.ani = animate

	def draw(self, window):
		if self.ani:
			if self.life > 50:
				self.change_radius(self.get_radius() + 3)
			else:
				self.change_radius(self.get_radius() - 3)
			pygame.draw.circle(window, self.color, self.pos, self.rad, self.fill)
		else:
			pygame.draw.circle(window, self.color, self.pos, self.rad, self.fill)

	def move_hor(self, x):
		self.vel[0] = x

	def move_vert(self, y):
		self.vel[1] = y

	def change_angle(self, new_angle):
		self.angle = new_angle

	def change_radius(self, new_radius):
		self.rad = new_radius
	
	def get_pos(self):
		return self.pos

	def get_vel(self):
		return self.vel

	def get_radius(self):
		return self.rad
	
	def get_angle(self):
		return self.angle

	def update(self):
		remove = False
		for index in range(2):
			self.pos[index] = (self.pos[index] + self.vel[index]) % DIM[index]
		if self.life:
			self.life -= 10
			if self.life <= 0:
				remove = True
		return remove

	def shoot(self):
		test = angle_to_vector(self.get_angle())
		bullet_pos = [int(self.pos[0] + self.rad * test[0]), int(self.pos[1] + self.rad* test[1])]
        	bullet_vel = [int(6 * test[0]), int(6 * test[1])]
		bullet_array.append(Circle(BLUE, bullet_pos, bullet_vel, 5, 0, 150))
	
	def collide(self, other_object):
		distance = dist(self.get_pos(), other_object.get_pos())
		if distance <= self.get_radius() + other_object.get_radius():
			return True
		else:
			return False

class Text:

	hovered = False
	
	def __init__(self, label, pos, color, string, size, number = 0):
		self.label = label
		self.pos = pos
		self.color = color
		self.string = string
		self.size = size
		self.number = number
		self.set_rect()
	
	def change_number(self, new_number):
		if self.string == False:
			self.number = new_number

	def get_number(self):
		if self.string == False:
			return self.number

	def get_color(self):
		if self.hovered:
			return RED
		else:
			return self.color

	def set_font(self):
		font = pygame.font.Font(None, self.size)
		if self.string == False:
			self.font = font.render(self.label + str(self.number), True, self.get_color())
		else:
			self.font = font.render(self.label, True, self.get_color())
	def set_rect(self):
		self.set_font()
		self.rect = self.font.get_rect()
		self.rect.topleft = self.pos

	def draw(self, window):	
		self.set_font()	
		window.blit(self.font, self.pos)
     
test = Circle(WHITE, [DIM[0] / 2, DIM[1] / 2], [0, 0], 20, 0)
#border = Circle(WHITE, [LENGTH / 2, WIDTH / 2], [0, 0], test.get_radius() + 90, 1)
bullet_array = []
enemy_array = []
explosion_array = []

life_text = Text("Life: ", [550, 450], WHITE, False, 30, 100)
score_text = Text("Score: ", [10, 450], WHITE, False, 30, 0)
title_text = Text("TEST", [250, 200], WHITE, True, 72)
play_text = Text("Play", [287, 250], WHITE, True, 40)

while True:
	WINDOW.fill(BLACK)
	pygame.event.pump()

	if in_play == False:
		title_screen(WINDOW)
	
	else:

		test.draw(WINDOW)
		#border.draw(WINDOW)
		test.update()
		life_text.draw(WINDOW)
		score_text.draw(WINDOW)
		test.change_angle(find_angle(test, mousex, mousey))
		process_group(bullet_array, WINDOW)
		process_group(enemy_array, WINDOW)
		process_group(explosion_array, WINDOW)

		collisions = life_text.get_number() - 10 * group_collide(enemy_array, test)
		if collisions <= 0:
			life_text.change_number(0)
			in_play = False
		else:
			life_text.change_number(collisions)

		score_text.change_number(score_text.get_number() + 100 * group_group_collide(enemy_array, bullet_array))	

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			if in_play:
				mousex, mousey = event.pos
		elif event.type == MOUSEBUTTONDOWN:
			if in_play:
				test.shoot()
			else:
				if play_text.rect.collidepoint(event.pos):
					in_play = True
		elif event.type == KEYDOWN:
			if event.key == K_LEFT or event.key == K_a:
				test.move_hor(-3)
			elif event.key == K_RIGHT or event.key == K_d:
				test.move_hor(3)
			elif event.key == K_UP or event.key == K_w:
				test.move_vert(-3)
			elif event.key == K_DOWN or event.key == K_s:
				test.move_vert(3)
			elif event.key == K_SPACE:
				test.shoot()
		elif event.type == KEYUP:
			if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d:
				test.move_hor(0)
			elif event.key == K_UP or event.key == K_DOWN or event.key == K_w or event.key == K_s:
				test.move_vert(0)

	if timer % 10 == 0:
		timer = 0
		spawn_enemy()
	timer += 1

	pygame.display.update()
	fpsClock.tick(30)
