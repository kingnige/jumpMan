#!/usr/bin/python

import sys, pygame, pygame.mixer, time, math
import csv

#add in the option to read key presses
from pygame.locals import *

#setup a clock variable
clock = pygame.time.Clock()

#initalise PyGame
pygame.init()

#setup game variables (load sounds and images, define colours and other information)
sound = pygame.mixer.Sound("coin_flip.wav")
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
                self.Image = pygame.image.load('grass.png')
                self.rect = pygame.Rect(self.Image.get_rect()) #rectangle wrapper for collision detention
                self.update()

        def update(self):
                self.rect.topleft = self.X, self.Y
                screen.blit(self.Image,(self.X, self.Y))

class wall(pygame.sprite.Sprite):
    def __init__(self,X,Y,W,H):
        pygame.sprite.Sprite.__init__(self)
        self.X = X
        self.Y = Y
        self.rect = pygame.Rect(self.X,self.Y,W,H)
        self.update()

    def update(self):
        self.rect.topleft = self.X,self.Y

#create a platform group to hold all of the static platform collision objects
platforms = pygame.sprite.Group()
items = pygame.sprite.Group()

#add in the platforms for the level
with open('level1.csv','rb') as csvFile:
    grassItem = []
    currentRow = 0
    csvInput = csv.reader(csvFile, delimiter=',')
    for row in csvInput:
        value1 = int(row[1])
        value2 = int(row[2])
        grassItem.append(grass(value1,value2))
        platforms.add(grassItem[currentRow])
        currentRow += 1

#add in the platforms to stop the player leaving the level
with open('screenBlock.csv','rb') as csvFile:
    wallItem = []
    currentRow = 0
    csvInput = csv.reader(csvFile, delimiter=',')
    for row in csvInput:
        value1 = int(row[1])
        value2 = int(row[2])
        value3 = int(row[3])
        value4 = int(row[4])
        wallItem.append(wall(value1,value2,value3,value4))
        platforms.add(wallItem[currentRow])
        currentRow += 1

#setup a class to create collectable cherrys
class cherry(pygame.sprite.Sprite):
	def __init__(self,X,Y):
        	pygame.sprite.Sprite.__init__(self)
                self.X = X
                self.Y = Y
                self.Image = pygame.image.load('cherry.png')
                self.rect = pygame.Rect(self.Image.get_rect()) #rectangle wrapper for collision detention
                self.update()

        def update(self):
                self.rect.topleft = self.X, self.Y
                screen.blit(self.Image,(self.X, self.Y))

#create cherries to place in the level to be collected
cherry1 = cherry(300,480)
cherry2 = cherry(700,280)
cherry3 = cherry(200,80)
items.add(cherry1)
items.add(cherry2)
items.add(cherry3)

#setup the initial settings for jumper (and create the JUMPER class)
class jumper(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.X = 0
                self.Y = 450
                self.Move = 0
                self.Speed = 4
                self.Image = pygame.image.load('baddie.png')
                self.AllowJump = 0
                self.JumpHeight = 50
                self.Spring = -5
                self.Gravity = -5
                self.Status = 'falling'
                self.rect = pygame.Rect(self.Image.get_rect()) #rectangle wrapper for collision detention
                self.update()

        def collision(self):    
                platformCollision = pygame.sprite.spritecollide(self, platforms, False)
                if len(platformCollision) > 0:
                        return True #this means that a collision has happened
                else:
                        return False #this means that there is no collision
        
        def jump(self):
                if self.Status == 'onfloor':                            #if the player is on the ground
                        self.AllowJump = self.JumpHeight                #allow to jump to current allowed height
                        self.Status = 'jumping'                         #change the status to jumping

        def update(self):
                if self.Move != 0:
                        self.X += self.Move                             #move the player
                        self.rect.topleft = self.X, self.Y              #update the collision rectangle
                        if self.collision() == True:                    #see if there has been a collision
                                self.X -= self.Move                     #if collision move player back
                                self.AllowJump = 0                      #if character was jumping kill jump
                                self.Status = 'falling'                 #prevent character from jumping (as falling)
                                self.rect.topleft = self.X, self.Y      #update the collision rectangle to original position
                

                #try to move the character, and see if there is a collision. Allow drop if no collision
                #(first test if jumping before applying gravity)
                if self.AllowJump == 0:
                        self.Y -= self.Gravity
                        self.rect.topleft = self.X, self.Y              #update collision rectangle to new position
                        if self.collision() == True:                    #if there is a collision
                                self.Y += self.Gravity                  #move the character back upwards
                                self.rect.topleft = self.X, self.Y      #update collision rectangle to original position
                                self.Status = 'onfloor'                 #allow the character to jump if needed

                #see if the character has collected a cherry, and if so remove the item
		itemList = len(items)
		pygame.sprite.spritecollide(self, items, True)
		itemList2 = len(items)
		if itemList2 < itemList:
			sound.play()

                if self.AllowJump > 0:
                        self.Y += self.Spring
                        self.rect.topleft = self.X, self.Y              #update collision rectangle to new position
                        self.AllowJump -= 1
                        if self.collision() == True:
                                self.Y -= self.Spring
                                self.rect.topleft = self.X, self.Y      #update collision rectangle to original position
                                self.Status = 'falling'                 #reset the character to be falling (and not able to jump)
                                self.AllowJump = 0

                #update the player position rectangle
                self.rect.topleft = self.X, self.Y
                screen.blit(self.Image,(self.X, self.Y))

#add code to hide the mouse cursor (1 would be TRUE)
pygame.mouse.set_visible(0)

#use a version of the class JUMPER to create our player JUMPMAN
jumpMan = jumper()

def terminate():
    pygame.quit()
    sys.exit()

#main game loop (move key pressed to new FUNCTION at a later date)
while 1:
        #looks for anything that pygame recognises as an input
        for event in pygame.event.get():
                #if you click the X at the top this will send the quit command
                if event.type == pygame.QUIT:
                    terminate()
                #if key is pressed, and key is ESCAPE then exit
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        terminate()
                elif event.type == KEYDOWN and event.key == K_q:
                        terminate()

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
        platforms.update()
	items.update()
        jumpMan.update()

        #force the game to run at 60 frames per second (no faster)
        clock.tick(60)

        #update the screen so the image is shown
        pygame.display.flip()
