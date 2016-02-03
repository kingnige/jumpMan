#!/usr/bin/python

import sys, pygame, pygame.mixer, time, math

#add in the option to read key presses
from pygame.locals import *

#setup a clock variable
clock = pygame.time.Clock()

#initalise PyGame
pygame.init()

#setup game variables (load sounds and images, define colours and other information)
sound = pygame.mixer.Sound("sound.wav")
black = (0,0,0)
yellow = (255,215,0)

#setup the game screen
screen = pygame.display.set_mode((800,600))

#setup a class to create a PLATFORM sprite
class grass(pygame.sprite.Sprite):
	def __init__(self,X,Y):
		pygame.sprite.Sprite.__init__(self)
		self.X = X
		self.Y = Y
		self.Image = pygame.image.load("grass.png")
		self.rect = pygame.Rect(self.Image.get_rect()) #rectangle wrapper for collision detention
		self.update()

	def update(self):
		self.rect.topleft = self.X, self.Y
		screen.blit(self.Image,(self.X, self.Y))

#create platforms for the game
grass1 = grass(0,500)
grass2 = grass(400,300)

#create a platform group to hold all of the different platforms
platforms = pygame.sprite.Group()

#add the GRASS platforms to a group for drawing, updating and collision detection
platforms.add(grass1)
platforms.add(grass2)

#setup the initial settings for jumper (and create the JUMPER class)
class jumper(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.X = 0
		self.Y = 0
		self.Move = 0
		self.Speed = 4
		self.Image = pygame.image.load("baddie.png")
		self.AllowJump = 0
		self.JumpHeight = 50
		self.Spring = -5
		self.Gravity = -5

		self.rect = pygame.Rect(self.Image.get_rect()) #rectangle wrapper for collision detention
		self.update()

	def collision(self):    
		platformCollision = pygame.sprite.spritecollide(self, platforms, False)
		if len(platformCollision) > 0:
			return True #this means that a collision has happened
		else:
			return False #this means that there is no collision


	def onFloor(self):
		if self.rect.bottom >= grass1.rect.top: #check if rectangles are touching
			self.Status = "jumping"
	
	def jump(self):
		self.onFloor() #check if the character is on the floor
		if self.Status == "jumping":
			self.AllowJump = self.JumpHeight

	def update(self):
		if self.Move != 0:
			self.X += self.Move
		

		#try to move the character, and see if there is a collision. Allow drop if no collision
		#(first test if jumping before applying gravity
		if self.AllowJump == 0:
			self.Y -= self.Gravity
			self.rect.topleft = self.X, self.Y		#update collision rectangle to new position
			if self.collision() == True:			#if there is a collision
				self.Y += self.Gravity			#move the character back upwards
				self.rect.topleft = self.X, self.Y	#update collision rectangle to original position

		#if self.rect.colliderect(grass1.rect) == False and self.AllowJump == 0:
		#	self.Y -= self.Gravity



		if self.AllowJump > 0:
			self.Y += self.Spring
			self.rect.topleft = self.X, self.Y		#update collision rectangle to new position
			self.AllowJump -= 1
			if self.collision() == True:
				self.Y -= self.Spring
				self.rect.topleft = self.X, self.Y	#update collision rectangle to original position
				self.AllowJump = 0

		#update the player position rectangle
		self.rect.topleft = self.X, self.Y
		screen.blit(self.Image,(self.X, self.Y))

#add code to hide the mouse cursor (1 would be TRUE)
pygame.mouse.set_visible(0)

#use a version of the class JUMPER to create our player JUMPMAN
jumpMan = jumper()


#main game loop (move key pressed to new FUNCTION at a later date)
while 1:
	#looks for anything that pygame recognises as an input
	for event in pygame.event.get():
		#if you click the X at the top this will send the quit command
		if event.type == pygame.QUIT:
			sys.exit()
		#if key is pressed, and key is ESCAPE then exit
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			sys.exit()
		elif event.type == KEYDOWN and event.key == K_q:
			sys.exit()

		#add in code to move JUMPER
		if  event.type == KEYDOWN and event.key == K_RIGHT:
			jumpMan.Move = jumpMan.Speed
		elif event.type == KEYUP and event.key == K_RIGHT:
			jumpMan.Move = 0
		if event.type == KEYDOWN and event.key == K_LEFT:
			jumpMan.Move = -jumpMan.Speed
		elif event.type == KEYUP and event.key == K_LEFT:
			jumpMan.Move = 0 

		#make JUMPER faster and slower (in sets of 10)
		if event.type == KEYDOWN and event.key == K_e:
			jumpMan.Speed += 4
		elif event.type == KEYDOWN and event.key == K_w:
			if (jumpMan.Speed > 4):
				jumpMan.Speed -= 4
		
		#give JUMPMAN the permission to JUMP
		if event.type == KEYDOWN and event.key == K_UP:
			jumpMan.jump()
	
	#clear the screen (fill with a colour)
	screen.fill(black)

	#check for a collision (and change colour if generated list is longer than 0
	if jumpMan.collision() == True:
        	screen.fill(yellow)

	#call the player function to move and generate image, and display the platforms
	grass1.update()
	grass2.update()
	jumpMan.update()

	#force the game to run at 60 frames per second
	clock.tick(60)

	#update the screen so the image is shown
	pygame.display.flip()
