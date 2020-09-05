import math
import random
import pygame

# define width and height of window
WIDTH, HEIGHT = 1500, 550
# define circles to add each loop
circlesPerLoop = 20
# distance between circles
distanceOffset = 1
# max attempts to add circles
# if exceeded program will halt
maxAttempts = 500
# define size to use for font
fontSize = 600
# define font style
fontStyle = 'consolas'
# position to place text
textPos = (25, 25)
# text to display
text = '2020'
# define if circles should be filled
fillCircles = False
# background color
background = (0, 0, 0)
# text color
circleColor = (255, 255, 255)

# initialize pygame
pygame.init()
# define font
font = pygame.font.SysFont(fontStyle, fontSize)
# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# set window caption
pygame.display.set_caption('Circle packing')


# Circle class
class Circle:
	def __init__(self, x, y, color):
		# define circle position (x and y)
		self.x = x
		self.y = y
		# circle radius starts at 1
		self.r = 1
		# circle starts out growing
		self.growing = True
		# circle color
		self.color = color


# function to calculate euclidean distance
def dist(x1, y1, x2, y2):
	return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


# main loop function
def draw():
	# fill screen in background color
	screen.fill(background)
	count, attempts = 0, 0
	# loop to create new circles
	while count < circlesPerLoop and attempts != maxAttempts:
		# create a new circle
		if c := newC():
			# append current circle to array to draw
			circles.append(c)
			# append current circle to array to grow
			growingCircles.append(c)
			# increase count to signify a circle is created
			count += 1
		# increase attempts
		attempts += 1
	# if attempts hits maxAttempts and all circles aren't created
	# then the program has completed
	if attempts == maxAttempts:
		print('Finished')
		# halt program
		while True: inp()
	# loop to detect collisions
	# loop over every pair of circles
	for c in growingCircles:
		for other in circles:
			# check if circles are colliding with distanceOffset space between
			# and the circles are not the same
			if dist(c.x, c.y, other.x, other.y) < c.r + other.r + distanceOffset and c != other:
				# change growing state of current circle
				c.growing = False
				# remove circle from circles to check each frame (growingCircles)
				growingCircles.remove(c)
				break
	# loop over every circle
	for c in circles:
		# draw the circle
		pygame.draw.circle(screen, c.color, (c.x, c.y), c.r, not fillCircles)
		# increase the circles radius if circle.growing is True
		c.r += c.growing
	# update the display
	pygame.display.update()


# function to create a new circle
def newC():
	# choose random x, y positions from pixels ontop of the text
	x, y = white_pixels[random.randint(0, len(white_pixels) - 1)]
	# check if (x, y) is inside another circle
	for c in circles:
		# if it is return None
		if dist(x, y, c.x, c.y) < c.r + distanceOffset + 1: return
	# if (x, y) is a valid position for a circle then return a new Circle object
	return Circle(x, y, circleColor)


# function to get pixels onto which to draw circles
def get_pixels():
	# draw text (display isn't updated so the text isn't shown)
	screen.blit(font.render(text, True, (255, 255, 255)), textPos)
	# create empty pixels array to contain valid positions
	pixels = []
	# loop over every pixel
	for x in range(WIDTH):
		for y in range(HEIGHT):
			# check if pixel is colored white
			if screen.get_at((x, y)) == (255, 255, 255):
				# if it is append it to the pixels array
				pixels.append((x, y))
	# return valid pixels
	return pixels


# function to handle input
def inp():
	# loop over every input event
	for event in pygame.event.get():
		# if window is closed then quit program
		if event.type == pygame.QUIT:
			quit()


# initialize circles array
circles = []
# initialize growingCircles array
growingCircles = []
# initialize valid pixels array using the get_pixels function
white_pixels = get_pixels()

# infinite loop
while True:
	# execute function to create/update/draw circles
	draw()
	# handle user input
	inp()