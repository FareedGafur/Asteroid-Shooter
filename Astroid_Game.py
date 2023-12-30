import pygame, sys
from random import randint, uniform


class Ship(pygame.sprite.Sprite):

	def __init__(self, groups):

		# we have to init the parent class
		super().__init__(groups) 

		#2 We need a surface
		self.image = pygame.image.load('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/ship.png').convert_alpha()

		# We need a rect
		self.rect = self.image.get_rect(center = (Window_Width / 2, Window_Height / 2))

		# Add a Mask
		self.mask = pygame.mask.from_surface(self.image)

		# Timer
		self.can_shoot = True
		self.shoot_time = None

		# Sound
		self.laser_sound = pygame.mixer.Sound('C:/Users/faree/Downloads/asteroid_shooter_files (1)/asteroid_shooter_files/project_15 - Sound/sounds/laser.ogg')

	
	def laser_timer(self):
		# Method that checks if the space ship can shoot. If not, subtracts the time of the last laser shot from the current time to see if it can shoot
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > 500:
				self.can_shoot = True

	def input_position(self): 
		# Gets the mouse position for the spaceship to follow
		pos = pygame.mouse.get_pos()
		self.rect.center = pos


	def laser_shoot(self):
		# If mouse is clicked, and self.can_shoot is true, set it to false, get the shoot time, and shoots laser from space ship
		if pygame.mouse.get_pressed()[0] and self.can_shoot:

			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()

			Laser(self.rect.midtop,laser_group)
			self.laser_sound.play()

	def meteor_collision(self):
		# If there is a colision between the space ship and the meteoroid, end the game and close the window
		if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
			pygame.quit()
			sys.exit()
	
	def update(self):
		self.laser_timer()
		self.input_position()
		self.laser_shoot()
		self.meteor_collision()

class Laser(pygame.sprite.Sprite):

	def __init__(self, pos, groups):

		super().__init__(groups)

		# Gets laser image, creates a rect and mask for the image

		self.image = pygame.image.load('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/laser.png').convert_alpha()

		self.rect = self.image.get_rect(midbottom = pos)
		self.mask = pygame.mask.from_surface(self.image)
		


		# Float based position
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(0,-1)
		self.speed = 600

		# Sound
		self.explosion_sound = pygame.mixer.Sound('C:/Users/faree/Downloads/asteroid_shooter_files (1)/asteroid_shooter_files/project_15 - Sound/sounds/explosion.wav')

	def meteor_collision(self):
		# When laser collides with a meteor, kills both entities and plays explosion sound
		if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):

			self.kill()
			self.explosion_sound.play()



	def update(self):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))

		if self.rect.bottom < 0: # Laser sprite is killed when moved off the screen
			self.kill()
		self.meteor_collision()

class Meteor(pygame.sprite.Sprite):

	def __init__(self, pos, groups):

		# Basic setup
		super().__init__(groups)

		# Gets meteor image, and sizes it at a random scale from 0.5 - 1.5
		meteor_surf = pygame.image.load('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/meteor.png').convert_alpha()
		meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)

		# gets the scaled surface, iamge, rect, and mask
		self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
		self.image = self.scaled_surf
		self.rect = self.image.get_rect(center = pos)
		self.mask = pygame.mask.from_surface(self.image)

		# Float based position
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(uniform(-0.5, 0.5),uniform(0.5, 2))
		self.speed = randint(400,600)

		# Rotation Logic
		self.rotation = 0
		self.rotation_speed = randint(20,50)

	def rotate(self):

		# Meteorioid rotates as its falling; each frame shows the meteoroid rotate, little by little
		self.rotation += self.rotation_speed * dt
		rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
		self.image = rotated_surf
		self.rect = self.image.get_rect(center = self.rect.center)
		self.mask = pygame.mask.from_surface(self.image)	

	def update(self):

		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))
		self.rotate()

		if self.rect.top > Window_Height:
			self.kill()

class Score:

	def __init__(self):

		# Gets font from files
		self.font = pygame.font.Font('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/subatomic.ttf', 50)
		self.points = 0

	def display(self):

		# Sets up scoreboard
		score_text = f'Score: {self.points}' # Text format
		text_surf = self.font.render(score_text, True, (255,255,255))
		text_rect = text_surf.get_rect(midbottom = (Window_Width/2, Window_Height - 80))
		display_surface.blit(text_surf, text_rect) 
		pygame.draw.rect(display_surface, 'white', text_rect.inflate(30,30), width = 8, border_radius = 5)

	def update(self):

		# Adds 1 point for every meteor blown up
		if pygame.sprite.groupcollide(laser_group, meteor_group, True, True):
			self.points += 1

		if pygame.sprite.groupcollide(spaceship_group, meteor_group, True, True):
			print('\n\n\n\n\n\n\n=============== COLLISION ===============\n')
			print('===============   Score:  ===============\n')
			print(f'===============     {self.points}     ===============\n\n\n\n\n\n')
			pygame.quit()
			sys.exit()




# Game setup
pygame.init()
Window_Width, Window_Height = 1280,720
display_surface = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption('Astroid Shooter')
clock = pygame.time.Clock()

# Background
bg_surf = pygame.image.load('C:/Users/faree/Downloads/Images_for_pygame/asteroid_shooter_files/project_4 - Image Text/graphics/background.png').convert()

# Sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# Sprite creation
ship = Ship(spaceship_group)
scoreboard = Score()


# Timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400) #controls how fast meteors spawn in the game


# Sound
Background_music = pygame.mixer.Sound('C:/Users/faree/Downloads/asteroid_shooter_files (1)/asteroid_shooter_files/project_15 - Sound/sounds/music.wav')
Background_music.play(loops = -1)


while True:

	# Event Loop
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == meteor_timer:
			meteor_y_pos = randint(-150, -50)
			meteor_x_pos = randint(-100, Window_Width + 100)
			Meteor((meteor_x_pos, meteor_y_pos), groups = meteor_group)


	#delta time
	dt = clock.tick() / 1000

	# background
	display_surface.blit(bg_surf, (0,0))

	# Updates
	spaceship_group.update()
	laser_group.update()
	meteor_group.update()

	# Score
	scoreboard.update()
	scoreboard.display()

	# Graphics
	spaceship_group.draw(display_surface)
	laser_group.draw(display_surface)
	meteor_group.draw(display_surface)

	# draw the frame
	pygame.display.update()