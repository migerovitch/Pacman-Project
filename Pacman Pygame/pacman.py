import pygame, sys 
from pygame.locals import *
import random
import csv

#pygame.init()

width = 600 #This can change
height = 600 #This can change
playersize = 20 #This can change
ghostsize = 20
fps = 15 #This can change
clock = pygame.time.Clock()

#Create display
DISPLAY = pygame.display.set_mode((width,height))
pygame.display.set_caption("A E I O U and sometimes Y")

#define colors with rgb values
white = (255,255,255)
yellow = (255,255,0)
black = (0,0,0)
grey = (128,128,128)
darkBlue = (0,20,121)

blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
orange = (255,165,0)
pink = (255,192,203)


#load sprites
pacmanLeft = [pygame.image.load('pacmanSprites/pacmanLeft.png'), pygame.image.load('pacmanSprites/pacmanLeftD.png')]
pacmanRight = [pygame.image.load('pacmanSprites/pacmanRight.png'), pygame.image.load('pacmanSprites/pacmanRightD.png')]
pacmanUp = [pygame.image.load('pacmanSprites/pacmanUp.png'), pygame.image.load('pacmanSprites/pacmanUpD.png')]
pacmanDown = [pygame.image.load('pacmanSprites/pacmanDown.png'), pygame.image.load('pacmanSprites/pacmanDownD.png')]

pinkGhost = [pygame.image.load('pacmanSprites/pinkLeft.png'),pygame.image.load('pacmanSprites/pinkRight.png'),pygame.image.load('pacmanSprites/pinkUp.png'),pygame.image.load('pacmanSprites/pinkDown.png')] 
orangeGhost = [pygame.image.load('pacmanSprites/orangeLeft.png'),pygame.image.load('pacmanSprites/orangeRight.png'),pygame.image.load('pacmanSprites/orangeUp.png'),pygame.image.load('pacmanSprites/orangeDown.png')] 
redGhost = [pygame.image.load('pacmanSprites/redLeft.png'),pygame.image.load('pacmanSprites/redRight.png'),pygame.image.load('pacmanSprites/redUp.png'),pygame.image.load('pacmanSprites/redDown.png')] 
blueGhost = [pygame.image.load('pacmanSprites/blueLeft.png'),pygame.image.load('pacmanSprites/blueRight.png'),pygame.image.load('pacmanSprites/blueUp.png'),pygame.image.load('pacmanSprites/blueDown.png')] 


steps = 0
left = False
right = False
up = False
down = False


#starting coords of player
pacX = width/2
pacY = height/2

yChange = 0
xChange = 0

ghostCoords = {"blue":[width/2-50,height/2-50,blueGhost,0], "orange":[width/2-50,height/2-50,orangeGhost,0], "red":[width/2-50,height/2-50,redGhost,0], "pink":[width/2-50,height/2-50,pinkGhost,0] }

score = 0


xy = []
blocks = []
barriers = []
food = []
levelname = (input("Levelname (omit file extension):"))

#if true then no entry
touching = False

#if true then system exit
gameExit = False

csvfile =open(levelname +".csv",'r')
obj=csv.reader(csvfile)
for row in obj:
	blocks.append((row))

blocks[0][0] = pacX
blocks[0][1] = pacY 

for block in blocks:
	if block[0] == "barrier":
		barriers.append(block)
	elif block[0] == "food":
		food.append(block)
print(barriers)
print(food)

def buildlevel(xy,screen,bcolor,fcolor):
	global ghostCoords
	for coord in barriers:
		pygame.draw.rect(screen,bcolor,[float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4])])
	for coord in food:
		pygame.draw.rect(screen,fcolor,[float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4])])

def drawSprites():
	DISPLAY.fill(grey)
	global steps
	if left:
		if steps + 1 <= 1:
			steps += 1
		else:
			steps = 0
		DISPLAY.blit(pacmanLeft[steps],(pacX,pacY))
	if right:
		
		if steps + 1 <= 1:
			steps += 1
		else:
			steps = 0
		DISPLAY.blit(pacmanRight[steps],(pacX,pacY))
	if up:
		if steps + 1 <= 1:
			steps += 1
		else:
			steps = 0
		DISPLAY.blit(pacmanUp[steps],(pacX,pacY))

	if down:
		if steps + 1 <= 1:
			steps += 1
		else:
			steps = 0
		DISPLAY.blit(pacmanDown[steps],(pacX,pacY))
	
	for ghost in ghostCoords:
		ghostDirection = None

		randGhostX = random.randrange(-2,2)
		randGhostY = random.randrange(-2,2)

		if random.randrange(0,2) == 1:	
			for i in range(randGhostX):
				ghostCoords[ghost][0] += (1*randGhostX) 
		else:
			for i in range(randGhostY):
				ghostCoords[ghost][1] += (1*randGhostY)
		
		if randGhostX <= 0:
			ghostDirection = 0
		elif randGhostX >= 0:
			ghostDirection = 1
		elif randGhostY >= 0:
			ghostDirection = 2
		elif randGhostY <= 0:
			ghostDirection = 3


		print(f"X of {ghost}:{ghostCoords[ghost][0]}")
		print(f"Y of {ghost}:{ghostCoords[ghost][1]}")

		DISPLAY.blit(ghostCoords[ghost][2][ghostDirection], (ghostCoords[ghost][0], ghostCoords[ghost][1]))
		
	
	buildlevel(xy,DISPLAY,darkBlue,white)
	pygame.display.update()
	
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
				left = True
				right = False
				up = False
				down = False
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_RIGHT:
				xChange = playersize/2
				yChange = 0
				left = False
				right = True
				up = False
				down = False
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_UP:
				yChange = -playersize/2
				xChange = 0
				left = False
				right = False
				up = True
				down = False
				#print(str(x)+", "+str(y))
			elif event.key == pygame.K_DOWN:
				yChange = playersize/2
				xChange = 0
				left = False
				right = False
				up = False
				down = True		
			if event.key == pygame.K_r:
				pacX = width/2
				pacY = height/2	
		
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

	#is the movement selected going to intersect with a boundary or a ghost?
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
	
#is player touching a ghost?
	for ghost in ghostCoords:
		x = ghostCoords[ghost][0]
		y = ghostCoords[ghost][1]
		rectwidth = ghostsize
		rectheight = ghostsize
		if pacX+xChange > round(x-playersize) and pacX+xChange < round(x+rectwidth) and pacY+yChange > round(y-playersize) and pacY+yChange < round(y+rectheight):
			gameExit = True
		
		
	"""
	if score == maxscore:
		print("You Win!")
		#gameExit = True
	"""

	
	
	#draw everything on the display
	drawSprites()
	clock.tick(fps)
	pygame.display.update()
pygame.quit()
sys.exit()
