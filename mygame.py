import os
import sys
import pygame
import random

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

################################

def background():
	window.fill(white)
	for x in range(0,screen_width,blocksize):
		for y in range(0,screen_height,blocksize):
			rect = pygame.Rect(x,y,blocksize,blocksize)
			pygame.draw.rect(window,black,rect,1)


class BuildShape():
	def __init__(self,shape):
		self.shape_rotations = []
		x_counter = 0 - blocksize
		y_counter = 0
		for rotation in shape:
			templst = []
			for i in shape[shape.index(rotation)]:
				x_counter += blocksize
				if i == 1:
					templst.append((x_counter,y_counter))
					if x_counter == 150:
						y_counter += blocksize
						x_counter = 0 - blocksize
				elif x_counter == 150:
					y_counter += blocksize
					x_counter = 0 - blocksize
			self.shape_rotations.append(templst)
			y_counter = 0

		self.shape = self.shape_rotations[0]



class MoveShape(BuildShape):
	def rotate(self,point):
		if len(self.shape_rotations)>0:
			shape_holder = []
			self.shape_rotations.append(self.shape_rotations.pop(0))
			for tup in self.shape_rotations[0]:
				shape_holder.append((tup[0]+point[0],tup[1]+point[1]))
			self.shape = shape_holder

	def direction(self,movement):
		templst = []
		for tup in self.shape:
			templst.append((tup[0]+movement[0],tup[1]+movement[1]))

		self.shape = templst

	def dropdown():
		pygame.event.post(dropdown)


class UpdateGrid(): 

	def check_place(self):
		for tup in self.current_piece.shape:
			if tup[0] < 0:
				MoveShape.direction(self.current_piece,(blocksize,0))
				break
			elif tup[0] > screen_width - blocksize:
				MoveShape.direction(self.current_piece,(-blocksize,0))
			elif tup not in self.free_spaces:
				self.stack()
				self.current_piece = random.choice(shape_list)
				print(len(self.saved_blocks)/4)
				break

	def stack(self):
		for tup in self.current_piece.shape:
			self.saved_blocks.append((tup[0],tup[1] - blocksize))
		#self.check_matches()
		#self.update_free_spaces()

	def update_free_spaces(self):
		for tup in self.saved_blocks:	
			self.free_spaces.remove(tup)
			
	def check_matches(self):
		templst = []
		for tup in self.saved_blocks:
			templst.append(tup[1])

		kill_guide = {i:templst.count(i) for i in templst}
		kill = []

		for tup in self.saved_blocks:
			if kill_guide.get(tup[1]) == 10:
				kill.append(tup)

		for tup in kill:
			self.saved_blocks.remove(tup)

		if len(kill) > 0:
			templst = []
			for tup in self.saved_blocks:
				for dedtup in kill:
					if tup[0] == dedtup[0] and tup[1] < dedtup[1]:
						templst.append((tup[0],tup[1]+blocksize))

					elif tup[0] == dedtup[0] and tup[1] > dedtup[1]:
						templst.append(tup)

			self.free_spaces = []
			for x in range(0,screen_width,blocksize):
				for y in range(0,screen_height,blocksize):
					if (x,y) not in templst:
						self.free_spaces.append((x,y))

			self.saved_blocks = templst


class Player(MoveShape,UpdateGrid):
	def __init__(self,shape_list):
		self.saved_blocks = []
		self.free_spaces = []
		self.current_piece = random.choice(shape_list)

		for y in range(0,screen_height,blocksize):
			for x in range(0,screen_width, blocksize):
				self.free_spaces.append((x,y))

	def draw(self):
		for tup in self.current_piece.shape:
			pygame.draw.rect(window,black,(tup[0],tup[1],blocksize,blocksize))
		for i in self.saved_blocks:
			pygame.draw.rect(window,gold,(i[0],i[1],blocksize,blocksize))


	def check_input(self):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				MoveShape.direction(self.current_piece,(blocksize,0))
			elif event.key == pygame.K_LEFT:
				MoveShape.direction(self.current_piece,(-blocksize,0))
			elif event.key == pygame.K_SPACE:
				MoveShape.rotate(self.current_piece,self.current_piece.shape[0])

		elif event.type == dropdown:
			MoveShape.direction(self.current_piece,(0,blocksize))

	def board_check(self):
		UpdateGrid.check_place(self)



s = BuildShape(s_image)
t = BuildShape(t_image)
l = BuildShape(l_image)
o = BuildShape(o_image)
z = BuildShape(z_image)
j = BuildShape(j_image)
shape_list = [s,t,l,o,z,j]

player = Player(shape_list)

#main loop
playing = True
while playing:
	clock.tick(fps)
	player.board_check()

	background()
	player.draw()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		else:
			player.check_input()


	pygame.display.update()

pygame.quit()


