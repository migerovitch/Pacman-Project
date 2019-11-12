import pygame, sys
import csv


class PacmanGame():

	WIDTH, HEIGHT = 600, 600
	PLAYER_SIZE = 20
	FPS = 15

	def __init__(self):
		self.clock = pygame.time.Clock()

		# Create display
		self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("waka waka waka")
		# define colors with rgb values
		self.white = (255, 255, 255)
		self.yellow = (255, 255, 0)
		self.black = (0, 0, 0)
		self.grey = (128, 128, 128)
		self.darkBlue = (0, 20, 121)

		# load sprites
		self.spriteLeft = [pygame.image.load('pacmanSprites/pacmanLeft.png'), pygame.image.load('pacmanSprites/pacmanLeftD.png')]
		self.spriteRight = [pygame.image.load('pacmanSprites/pacmanRight.png'), pygame.image.load('pacmanSprites/pacmanRightD.png')]
		self.spriteUp = [pygame.image.load('pacmanSprites/pacmanUp.png'), pygame.image.load('pacmanSprites/pacmanUpD.png')]
		self.spriteDown = [pygame.image.load('pacmanSprites/pacmanDown.png'), pygame.image.load('pacmanSprites/pacmanDownD.png')]
		self.steps = 0

		self.left = False
		self.right = False
		self.up = False
		self.down = False

		# starting coords of player
		self.pacX = self.WIDTH/2
		self.pacY = self.HEIGHT/2

		self.maxscore = 0

		self.yChange = 0
		self.xChange = 0

		self.ghostCoords = {"blue": (0, 0, 0), "orange": (0, 0, 0), "green": (0, 0, 0), "red": (0, 0, 0)}

		self.score = 0

		self.xy = []
		self.blocks = []
		self.barriers = []
		self.food = []

		# if true then no entry
		self.touching = False

		# if true then system exit
		self.gameExit = False

		level_name = input("Level name (omit file extension):")
		self.create_grid(level_name)

		self.main()

	def create_grid(self, level_name):
		csv_file = open(level_name + ".csv", 'r')
		obj = csv.reader(csv_file)
		for row in obj:
			self.blocks.append(row)

		self.blocks[0][0] = self.pacX
		self.blocks[0][1] = self.pacY

		for block in self.blocks:
			if block[0] == "barrier":
				self.barriers.append(block)
			elif block[0] == "food":
				self.food.append(block)

		self.maxscore = len(self.food)

		print(self.barriers)
		print(self.food)

	def build_level(self, screen, bcolor, fcolor):
		for coord in self.barriers:
			pygame.draw.rect(screen, bcolor, [float(coord[1]), float(coord[2]), float(coord[3]), float(coord[4])])
		for coord in self.food:
			pygame.draw.rect(screen, fcolor, [float(coord[1]), float(coord[2]), float(coord[3]), float(coord[4])])

	def draw_sprites(self):
		self.display.fill(self.grey)
		if self.left:
			if self.steps + 1 <= 1:
				self.steps += 1
			else:
				self.steps = 0
			self.display.blit(self.spriteLeft[self.steps], (self.pacX, self.pacY))
		if self.right:

			if self.steps + 1 <= 1:
				self.steps += 1
			else:
				self.steps = 0
			self.display.blit(self.spriteRight[self.steps], (self.pacX, self.pacY))

		if self.up:
			if self.steps + 1 <= 1:
				self.steps += 1
			else:
				self.steps = 0
			self.display.blit(self.spriteUp[self.steps], (self.pacX, self.pacY))

		if self.down:
			if self.steps + 1 <= 1:
				self.steps += 1
			else:
				self.steps = 0
			self.display.blit(self.spriteDown[self.steps], (self.pacX, self.pacY))

		self.build_level(self.display, self.darkBlue, self.white)
		pygame.display.update()

	def game(self):
		while not self.gameExit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameExit = True
				# Gets keypresses and moves the player accordingly
				if event.type == pygame.KEYDOWN:
					# print(str(event.key))
					if event.key == pygame.K_LEFT:
						self.xChange = -self.PLAYER_SIZE/2
						self.yChange = 0
						self.left = True
						self.right = False
						self.up = False
						self.down = False
						# print(str(x)+", "+str(y))
					elif event.key == pygame.K_RIGHT:
						self.xChange = self.PLAYER_SIZE/2
						self.yChange = 0
						self.left = False
						self.right = True
						self.up = False
						self.down = False
						# print(str(x)+", "+str(y))
					elif event.key == pygame.K_UP:
						self.yChange = -self.PLAYER_SIZE/2
						self.xChange = 0
						self.left = False
						self.right = False
						self.up = True
						self.down = False
						# print(str(x)+", "+str(y))
					elif event.key == pygame.K_DOWN:
						self.yChange = self.PLAYER_SIZE/2
						self.xChange = 0
						self.left = False
						self.right = False
						self.up = False
						self.down = True

				"""
				#Make player stop moving after keyup
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT or pygame.K_RIGHT:
						xChange = 0
					if event.key == pygame.K_UP or pygame.K_DOWN:
						yChange = 0
				"""

			# if player goes out of bounds then move them to the other side of the screen
			if self.pacX > self.WIDTH or self.pacX < 0 or self.pacY > self.HEIGHT or self.pacY < 0:
				if self.pacX > self.WIDTH:
					self.pacX = 0
				if self.pacX < 0:
					self.pacX = self.WIDTH - self.PLAYER_SIZE
				if self.pacY > self.HEIGHT:
					self.pacY = 0
				if self.pacY < 0:
					self.pacY = self.HEIGHT - self.PLAYER_SIZE

			# is the movement selected going to intersect with a boundary?
			for coord in self.barriers:
				x = float(coord[1])
				y = float(coord[2])
				rectwidth = float(coord[3])
				rectheight = float(coord[4])

				if (self.pacX + self.xChange) > round(x - self.PLAYER_SIZE):
					if self.pacX + self.xChange < round(x + rectwidth):
						if (self.pacY + self.yChange) > round(y - self.PLAYER_SIZE):
							if self.pacY + self.yChange < round(y + rectheight):
								self.touching = True

			# if player touching barrier then dont allow move
			if not self.touching:
				self.pacX += self.xChange
				self.pacY += self.yChange
			self.touching = False

			for coord in self.food:
				x = float(coord[1])
				y = float(coord[2])
				rectwidth = float(coord[3])
				rectheight = float(coord[4])

				if (self.pacX + self.xChange) > round(x - self.PLAYER_SIZE):
					if self.pacX + self.xChange < round(x + rectwidth):
						if (self.pacY + self.yChange) > round(y - self.PLAYER_SIZE):
							if self.pacY + self.yChange < round(y + rectheight):
								self.score += 1
								self.food.remove(coord)
								print(self.score)
			"""
			if score == maxscore:
				print("You Win!")
				#gameExit = True
			"""

			# draw everything on the display
			self.draw_sprites()
			self.clock.tick(self.FPS)

	def main(self):
		pygame.init()

		self.game()

		pygame.quit()
		sys.exit()


if __name__ == "__main__":
	game = PacmanGame()
