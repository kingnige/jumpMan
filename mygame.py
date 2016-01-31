#!/usr/bin/python

import sys, pygame, pygame.mixer
pygame.init()

sound = pygame.mixer.Sound("sound.wav")

sound.play()

black = (0,0,0)

size = width, height = 600, 400

screen = pygame.display.set_mode(size)

#load the image into the program
tux = pygame.image.load("Tux.png")
badguy = pygame.image.load("baddie.png")

x = 0
y = 0

r, g, b  = 0,0,0

while 1:
	#looks for anything that pygame recognises as an input
	for event in pygame.event.get():
		#if you click the X at the top this will send the quit command
		if event.type == pygame.QUIT:sys.exit()

	#clear the screen (fill with a colour)
	screen.fill((r,g,b))

	#set where we want the top left of the image to be displayed
	screen.blit(tux,(200,200))
	screen.blit(tux,(x,y))
	screen.blit(badguy,(100,100))

	#update the screen so the image is shown
	pygame.display.flip()

	#move one of the images across the screen to the left
	x = x+1
	y = y+1

	#reset the colour variables to 0
	if r == 255:
		r1 = -1
	elif r == 0:
		r1 = 1

	r = r + r1
