import os
import sys
import pygame
import random
import math

pygame.init()
##setup

screen_width, screen_height = 500,500
window = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
fps = 60

dropdown = pygame.USEREVENT + 1
pygame.time.set_timer(dropdown,1000)

blocksize = 50

white = (255,255,255)
black = (0,0,0)
gold = (252, 194, 3)


saved_blocks = []
free_spaces = []

def update_free_spaces(saved_blocks):
	temp_free_spaces = []
	for x in range(0,screen_width,blocksize):
		for y in range(0,screen_height,blocksize):
			if (x,y) not in saved_blocks:
				temp_free_spaces.append((x,y))
	return temp_free_spaces

free_spaces =  update_free_spaces(saved_blocks)

def background():
	window.fill(white)
	for x in range(0,screen_width,blocksize):
		for y in range(0,screen_height,blocksize):
			rect = pygame.Rect(x,y,blocksize,blocksize)
			pygame.draw.rect(window,black,rect,1)


t_image = [[
	1,1,1,0,
	0,1,0,0,
	0,0,0,0,
	0,0,0,0],[

	0,1,0,0,
	1,1,0,0,
	0,1,0,0,
	0,0,0,0],[

	0,1,0,0,
	1,1,1,0,
	0,0,0,0,
	0,0,0,0],[

	0,1,0,0,
	0,1,1,0,
	0,1,0,0,
	0,0,0,0]]

i_image = [[
	1,1,1,1,
	0,0,0,0,
	0,0,0,0,
	0,0,0,0],[

	0,1,0,0,
	0,1,0,0,
	0,1,0,0,
	0,1,0,0]]

l_image = [[
	0,1,0,0,
	0,1,0,0,
	0,1,1,0,
	0,0,0,0],[

	0,0,0,0,
	1,1,1,0,
	1,0,0,0,
	0,0,0,0],[

	1,1,0,0,
	0,1,0,0,
	0,1,0,0,
	0,0,0,0],[

	0,0,1,0,
	1,1,1,0,
	0,0,0,0,
	0,0,0,0]]

j_image = [[
	0,1,0,0,
	0,1,0,0,
	1,1,0,0,
	0,0,0,0],[

	1,0,0,0,
	1,1,1,0,
	0,0,0,0,
	0,0,0,0],[

	0,1,1,0,
	0,1,0,0,
	0,1,0,0,
	0,0,0,0],[

	0,0,0,0,
	1,1,1,0,
	0,0,1,0,
	0,0,0,0]]

o_image = [[
	1,1,0,0,
	1,1,0,0,
	0,0,0,0,
	0,0,0,0]]

s_image = [[
	0,1,1,0,
	1,1,0,0,
	0,0,0,0,
	0,0,0,0],[

	1,0,0,0,
	1,1,0,0,
	0,1,0,0,
	0,0,0,0]]

z_image = [[
	1,1,0,0,
	0,1,1,0,
	0,0,0,0,
	0,0,0,0],[

	0,1,0,0,
	1,1,0,0,
	1,0,0,0,
	0,0,0,0]]

def build_shape(shape):
	rotations = []
	x = 0 - blocksize
	y = 0
	r = math.sqrt(len(shape[0])) * blocksize - blocksize
	for rotation in shape:
		templst = []
		for i in shape[shape.index(rotation)]:
			x += blocksize
			if i == 1:
				templst.append((x,y))
				if x == r:
					y += blocksize
					x = -blocksize
			elif x == r:
				y += blocksize
				x = -blocksize
		rotations.append(templst)
		y = 0

	return rotations

class Shape():
	def __init__(self,rotations):
		self.rotations = rotations
		self.shape = self.rotations[0]

	def rotate(self):
		if len(self.rotations)>0:
			point = self.shape[0]
			shape_holder = []
			self.rotations.append(self.rotations.pop(0))
			for tup in self.rotations[0]:
				shape_holder.append((tup[0]+point[0],tup[1]+point[1]))
			self.shape = shape_holder

	def direction(self,movement):
		templst = []
		for tup in self.shape:
			templst.append((tup[0]+movement[0],tup[1]+movement[1]))
		self.shape = templst

	def dropdown():
		pass

t = Shape(build_shape(t_image))
i = Shape(build_shape(i_image))
l = Shape(build_shape(l_image))
j = Shape(build_shape(j_image))
o = Shape(build_shape(o_image))
s = Shape(build_shape(s_image))
z = Shape(build_shape(z_image))
shape_list = [t,i,l,j,o,s,z]

class Player(): #take key input, give updated coordinates for shape,saved blocks,freespaces
	def __init__(self,shape_list):
		self.saved_blocks = []
		self.free_spaces = []
		self.current_piece = random.choice(shape_list)

		for y in range(0,screen_height,blocksize):
			for x in range(0,screen_width, blocksize):
				self.free_spaces.append((x,y))

	def input(self):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.current_piece.direction((blocksize,0))
			elif event.key == pygame.K_LEFT:
				self.current_piece.direction((-blocksize,0))
			elif event.key == pygame.K_SPACE:
				self.current_piece.rotate()
			elif event.key == pygame.K_DOWN:
				pass #drop to bottom

		elif event.type == dropdown:
			self.current_piece.direction((0,blocksize))

	def new_piece(self):
		movement = self.current_piece.shape[0]
		self.current_piece.direction((-movement[0],-movement[1]))
		self.current_piece = random.choice(shape_list)
		
player = Player(shape_list)

def keep_shape_in(current_piece):
	for tup in current_piece.shape:
		if tup[0] < 0:
			current_piece.direction((blocksize,0))
			break
		elif tup[0] > screen_width - blocksize:
			current_piece.direction((-blocksize,0))
			break

def check_matches(saved_blocks): #returns list to remove from saved blocks
	templst = []
	for tup in saved_blocks:
		templst.append(tup[1])

	kill_guide = {i:templst.count(i) for i in templst}
	matches = []

	for tup in saved_blocks:
		if kill_guide.get(tup[1]) == screen_width/blocksize:
			matches.append(tup)
			
	return matches

def row_delete(saved_blocks):
	matches = check_matches(saved_blocks)
	templst = []
	number_of_rows = (len(matches)) / (screen_width/blocksize) 
	if len(matches) > 0:
		for tup in matches:
			saved_blocks.remove(tup)

		templst = []
		for tup in saved_blocks:
			for dedtup in matches:
				if tup[0] == dedtup[0] and tup[1] < dedtup[1]:
					templst.append((tup[0],tup[1]+blocksize))

				elif tup[0] == dedtup[0] and tup[1] > dedtup[1]:
					templst.append(tup)

	return templst

def stack(free_spaces,saved_blocks,player):
	stack = False
	shape_holder = player.current_piece.shape
	for tup in shape_holder:
		if tup not in free_spaces:
			stack = True
			break
	if stack:
		for tup in shape_holder:
			saved_blocks.append((tup[0],tup[1]-blocksize))
		player.new_piece()
	
def draw(shape,saved_blocks):
	for tup in shape:
		pygame.draw.rect(window,black,(tup[0],tup[1],blocksize,blocksize))
	for tup in saved_blocks:
		pygame.draw.rect(window,gold,(tup[0],tup[1],blocksize,blocksize))

#main loop
playing = True
while playing:
	clock.tick(fps)

	background()

	keep_shape_in(player.current_piece)
	stack(free_spaces,saved_blocks,player)

	updated_saved_blocks = row_delete(saved_blocks)
	if len(updated_saved_blocks):
		saved_blocks = updated_saved_blocks

	free_spaces = update_free_spaces(saved_blocks)

	draw(player.current_piece.shape,saved_blocks)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		else:
			player.input()

	pygame.display.update()

pygame.quit()