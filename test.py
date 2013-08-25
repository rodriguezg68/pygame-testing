#This is a test with pygame to create an object that moves and shoots
#by Gilberto Rodriguez

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

def mod_mouse_pos(mouse_x, mouse_y):
	return mouse_x % PI, mouse_y % PI

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
    return [math.cos(ang[0]), math.sin(ang[1])]

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
        
class Circle:
	def __init__(self, color, position, velocity, raidus, filled_in, life = 0, animate = False):
		self.color = color
		self.pos = position
		self.vel = velocity 
		self.rad = raidus
		self.fill = filled_in
		self.life = life
		self.angle = []
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
		test = angle_to_vector(self.angle)
		bullet_pos = [self.pos[0] + self.rad[0] * test[0], self.pos[1] + self.rad[1] * test[1]]
        	bullet_vel = [self.vel[0] + 6, self.vel[1] + 6]
		bullet_array.append(Circle(WHITE, bullet_pos, bullet_vel, 5, 0, 150))
	
	def collide(self, other_object):
		distance = dist(self.get_pos(), other_object.get_pos())
		if distance <= self.get_radius() + other_object.get_radius():
			return True
		else:
			return False

test = Circle(WHITE, [LENGTH/2, WIDTH/2], [0, 0], 20, 0)
bullet_array = []
enemy_array = []
explosion_array = []

while True:
	WINDOW.fill(BLACK)

	test.draw(WINDOW)
	test.update()
	process_group(bullet_array, WINDOW)
	process_group(enemy_array, WINDOW)
	process_group(explosion_array, WINDOW)

	group_collide(enemy_array, test)
	group_group_collide(enemy_array, bullet_array)
	test.change_angle(mod_mouse_pos(mousex, mousey))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos
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
