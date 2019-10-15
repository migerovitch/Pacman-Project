import pygame, sys 
from pygame.locals import *
import random
import csv

width = 600 #This can change
height = 600 #This can change
playersize = 20 #This can change
fps = 15 #This can change
clock = pygame.time.Clock()

#Create dis
DISPLAY=pygame.display.set_mode((width,height))
pygame.display.set_caption("waka waka waka")

#define colors with rgb values
white = (255,255,255)
yellow = (255,255,0)
black = (0,0,0)
grey = (128,128,128)
darkBlue = (0,20,121)

#starting coords of player
pacX = 40
pacY = 40

yChange = 0
xChange = 0

score = 0


xy = []
blocks = []
barriers = []
food = []
levelname = (input("Levelname (omit file tag):"))

#if true then no entry
touching = False

#if true then system exit
gameExit = False

csvfile =open(levelname +".csv",'r')
obj=csv.reader(csvfile)
for row in obj:
	blocks.append((row))
print(blocks)

pacX = width/2
pacY = height/2



for block in blocks:
	if block[0] == "barrier":
		barriers.append(block)
	elif block[0] == "food":
		food.append(block)
print(barriers)
print(food)

def buildlevel(xy,screen,bcolor,fcolor):
	for coord in barriers:
		pygame.draw.rect(screen,bcolor,[float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4])])
	for coord in food:
		pygame.draw.rect(screen,fcolor,[float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4])])

maxscore = len(food)


#main game loop
while gameExit == False:
	for event in pygame.event.get():
		if event.type == QUIT:
			gameExit = True
		#Gets keypresses and moves the player accordingly
		if event.type == pygame.KEYDOWN:
			#print(str(event.key))
			if event.key == pygame.K_LEFT:
				xChange = -playersize/2
				yChange = 0
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_RIGHT:
				xChange = playersize/2
				yChange = 0
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_UP:
				yChange = -playersize/2
				xChange = 0
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_DOWN:
				yChange = playersize/2
				xChange = 0
		"""
		#Make player stop moving after keyup
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or pygame.K_RIGHT:
				xChange = 0
			if event.key == pygame.K_UP or pygame.K_DOWN:
				yChange = 0
		"""
	#if player goes out of bounds then move them to the other side of the screen
	if pacX > width or pacX < 0 or pacY > height or pacY < 0: 
		if pacX > width: pacX = 0
		if pacX < 0: pacX = width - playersize
		if pacY > height: pacY = 0
		if pacY < 0: pacY = height - playersize

	#is the movement selected going to intersect with a boundary?
	for coord in barriers:
		x = float(coord[1])
		y = float(coord[2])
		rectwidth = float(coord[3])
		rectheight = float(coord[4])

		if pacX+xChange > round(x-playersize) and pacX+xChange < round(x+rectwidth) and pacY+yChange > round(y-playersize) and pacY+yChange < round(y+rectheight):
			touching = True

#if player touching barrier then dont allow move
	if not touching:
		pacX += xChange
		pacY += yChange
	touching = False

	for coord in food:
		x = float(coord[1])
		y = float(coord[2])
		rectwidth = float(coord[3])
		rectheight = float(coord[4])

		if pacX+xChange > round(x-playersize) and pacX+xChange < round(x+rectwidth) and pacY+yChange > round(y-playersize) and pacY+yChange < round(y+rectheight):
			score += 1 
			food.remove(coord)
			print(score)

	if score == maxscore:
		print("You Win!")
		gameExit = True

	
	
	#draw everything on the display
	DISPLAY.fill(grey)
	pygame.draw.rect(DISPLAY,yellow,[pacX,pacY,playersize,playersize])
	buildlevel(xy,DISPLAY,darkBlue,white)
	pygame.display.update()
	clock.tick(fps)

pygame.quit()
sys.exit()