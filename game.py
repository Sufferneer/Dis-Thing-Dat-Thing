# Dis Thing Dat Thing with CCC
# Nick T. (Sufferneer), 2025
import os.path
# ! DISCLAIMER
# ! In many instances of the code, instances of someone in the name of 'Suff' can be found.
# ! Before you scream plagiarism, please note that 'Suff' is a pseudonym.
# ! I am usually called 'Suff' within my peers, so although it may sound weird,
# ! This algorithm is 100% self-made made only with the assist of PyGame documentations and tutorials.

from json import load as json_load, dumps as json_dumps
from os.path import exists as path_exists
import string
import sys
import pygame
from math import sin, cos, ceil, pow, pi
from random import random, randint, choice

if __name__ == '__main__':
	clock = pygame.time.Clock()
	curTime = pygame.time.get_ticks()
	FPS:int = 60 # ! I won't recommend on touching this one.
	SCREENSIZE:tuple = (1280, 720)
	FONT_WIDTH_RATIO:float = 0.5625 # Because the font size does not equal to a character's width, this value is multiplied by the
	# font size of a text to get its character width

	pygame.init()
	pygame.display.set_caption('Dis Thing Dat Thing with CCC')
	screen = pygame.display.set_mode(SCREENSIZE)
	mousePos = pygame.mouse.get_pos() # Mouse position variable that updates every tick.
	DIALOGUE_SILENT_CHARS:list = [' ', ',', "'", '"', '.', '!', '?', '(', ')'] # These characters do NOT play the dialogue sound
	DIALOGUE_PAUSE_CHARS:list = [',', ';', ':', '.', '!', '?'] # These characters delay the dialogue
	pygame.mixer.music.set_volume(0)

def get_asset_path(path):
	# Simple function that returns the relative path of the assets.
	# I just don't want to type that a hundred times every time I want to get assets.
	basePath = ''
	try:
		basePath = sys._MEIPASS
	except:
		basePath = os.path.abspath('.')
	return os.path.join(basePath, f'assets/{path}')
def suff_lerp(a, b, t, e = 1):
	# This function interpolates a numeric value to another numeric value based on the "percentage" given.
	# e = exponent of the function, so the interp won't be linear.
	# You will often see this in assigning position values of sprites for a smooth transition effect.
	return a + (b - a) * pow(t, e)
def separate_string(text, max_char = 16):
	# Makes a string into a list of strings that finds within a set width of characters.
	# "German love, festival. I am quite skeptical" with `max_char = 10` turns to ["German", "love,", "festival.",
	#                                                                              "I am quite", "skeptical"]
	# When rendered, it will be rendered like this:
	#  ------------
	# | German     |
	# | love,      |
	# | festival;  |
	# | I am quite |
	# | skeptical  |
	#  ------------
	wordlist = text.split(' ') # Separate each word
	textlist = []
	tally = ''
	for word in wordlist:
		if len(tally + word) > max_char or word == '\n': # If the string does not fit `max_char` or the word contains a line skip
			textlist.append(tally[0:len(tally) - 1].replace('\n ', '')) # Exclude ending space of string and put into list
			tally = word + ' '
		else:
			tally += word + ' '
	textlist.append(tally[0:len(tally) - 1].replace('\n ', '')) # Exclude ending space of string and put into list
	return textlist
def clamp(val, minimum, maximum): # Bounds a value within a range of numbers (int or float)
	return min(max(val, minimum), maximum)
def remove_duplicates(leList): # Merge duplicate items from a list into one
	print(dict.fromkeys(leList))
	return list(dict.fromkeys(leList))
def get_used_spelling(word:str, word_alt:str = '', reverse:bool = False):
	american = curSave.fetch_options('american_spelling')
	if not american or word_alt == '':
		return word if not reverse else word_alt
	else:
		return word_alt if not reverse else word
def remove_hyphens_by_setting(word:str):
	if curSave.fetch_options('spare_missing_hyphens'):
		return word.replace('-', ' ')
	else:
		return word

if __name__ == '__main__':
	pygame.display.set_icon(pygame.image.load(get_asset_path('images/icon.png')))
	# CONSTANTS FOR SOUNDS
	UI_BUTTON_HOVER_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
	UI_BUTTON_PRESS_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/click.ogg'))
	UI_TEXT_TYPE_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
	UI_TEXT_ERASE_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/release.ogg'))
	UI_MENU_EXIT_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/toggle_off.ogg'))

	UI_DIALOGUE_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/dialogue.ogg'))
	UI_INVALID_SOUND = pygame.mixer.Sound(get_asset_path('sounds/ui/invalid.ogg'))

# CUSTOM OBJECTS THAT MAKE SPRITE/TEXT CREATION MORE CONVENIENT #
class SuffSprite(pygame.sprite.Sprite): # Custom sprite.
	"""
	Creates a configurable PyGame sprite.

	:param int x: X position of the sprite.
	:param int x: Y position of the sprite.
	:param str imagePath: Path of the sprite's image.
	"""
	def __init__(self, x, y, imagePath = ''):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.angle:float = 0
		self.angle_offset:pygame.Vector2 = pygame.Vector2(0, 0)
		self.surface:pygame.Surface = pygame.Surface(screen.get_size())
		self.rect:pygame.Rect = pygame.Rect(0, 0, SCREENSIZE[0], SCREENSIZE[1])
		if imagePath != '': # So that sprite allows invisible sprites
			self.load_graphic(imagePath)
	def load_graphic(self, imagePath):
		self.surface = pygame.image.load(get_asset_path(f'images/{imagePath}.png')).convert_alpha()
		self.rect = self.surface.get_rect()
	def draw(self, surface = None, rect = None):
		if surface is None:
			usedSurf = self.surface
		else:
			usedSurf = surface
		if rect is None: usedRect = self.rect
		else: usedRect = rect
		screen.blit(usedSurf, (self.x, self.y), usedRect)

class SuffText(list): # Parent class. Yes, I know. It's actually a list, but it needs to be for multi-line support
	"""
	Creates a configurable PyGame text sprite with multi-line support.

	:param int x: X position of the text
	:param int y: Y position of the text
	:param int width: Width in characters of the text
	:param str text: The string to be displayed
	:param int size: The size in pixels of the text
	:param tuple color: The color of the text
	"""
	def __init__(self, x, y, width, text, size=16, color=(0, 0, 0), font = 'default'): # Width in characters
		super().__init__()
		self.x, self.y, self.width, self.text, self.size, self.color = x, y, width, text, size, color
		self.text_font = pygame.font.Font(get_asset_path(f'fonts/{font}.ttf'), self.size)
		self.set_text(self.text)
		self.alpha = 255
	def set_text(self, text):
		self.text = text
		self.clear()
		textlist = separate_string(text, self.width) #
		for text in textlist:
			text_sprite = self.text_font.render(text, False, self.color)
			text_sprite_rect = text_sprite.get_rect()
			self.append([text_sprite, text_sprite_rect, text])
	def set_size(self, size):
		self.size = size
		self.text_font = pygame.font.Font(get_asset_path('fonts/default.ttf'), self.size)
		for text in self:
			text[0] = self.text_font.render(text[2], False, self.color)
			text[1] = text[0].get_rect()

	def set_alpha(self, alpha):
		self.alpha = alpha
		for text in self:
			text[0].set_alpha(alpha)
	def draw(self):
		for i in range(len(self)):
			screen.blit(self[i][0], (self.x, self.y + i * self.size), self[i][1])
	def get_height(self):
		return int(len(self) * self.size) if len(self[0]) > 0 else 0
	def get_width(self):
		return int(max(len(item[2]) for item in self) * self.size * FONT_WIDTH_RATIO)
	def is_colliding(self):
		return self.x + self.get_width() >= mousePos[0] >= self.x and self.y + self.get_height() >= mousePos[1] >= self.y
class SuffButton(pygame.sprite.Group): # Parent class. Buttons
	"""
	Creates a custom button that runs a function when clicked.

	:param tuple pos: Position of the button.
	:param tuple size: Size of the button.
	:param function function: Function run when button is clicked.
	:param str base_texture: Texture of the button.
	:param str text: The text to be displayed on the button.
	:param function hover_function: Function run when button is hovered (touched but not clicked).
	:param int text_size: The size of the button text.
	:param tuple text_color: The color of the button text.
	"""
	def __init__(self, pos, size, function, base_texture = '', text = '', hover_function = None, text_size = 32, text_color = None, text_hover_size_increase = 16):
		pygame.sprite.Group.__init__(self)
		self.disabled = False
		self.x = pos[0]
		self.y = pos[1]
		self.hovered = False
		self.clicked = False
		self.size = size
		self.text = text
		self.hover_function = hover_function
		self.function = function
		self.base_texture = base_texture
		self.text_color = text_color
		if self.text_color is None:
			self.text_color = (255, 255, 255)
		self.text_size = text_size
		self.text_hover_size_increase = text_hover_size_increase
		self.base = SuffSprite(self.x, self.y, f'{base_texture}')
		self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))
		self.base.surface.set_alpha(128)
		self.button_text = SuffText(self.x + text_size / 2, self.y + size[1] / 4, size[0] // (self.text_size // 2) if self.text_size > 0 else 0, self.text, text_size, self.text_color)
	def draw(self):
		self.base.x = self.x
		self.base.y = self.y
		self.button_text.x = self.x + self.text_size / 2
		self.button_text.y = self.y + self.size[1] / 4
		if self.x + self.size[0] >= mousePos[0] >= self.x and self.y + self.size[1] >= mousePos[1] >= \
				self.y and not self.disabled:
			if not self.hovered:
				UI_BUTTON_HOVER_SOUND.play()
				self.button_text.set_size(self.text_size + self.text_hover_size_increase)
				if self.hover_function is not None: self.hover_function()
				self.hovered = True
				if path_exists(get_asset_path(f'images/{self.base_texture}_hovered.png')):
					self.base.surface = pygame.image.load(
						get_asset_path(f'images/{self.base_texture}_hovered.png')).convert_alpha()
					self.base.surface.set_alpha(128)
					self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				UI_BUTTON_PRESS_SOUND.play()
				self.clicked = True
			elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				self.clicked = False
				self.function()
		else:
			if self.hovered:
				self.button_text.set_size(self.text_size)
				self.hovered = False
				if path_exists(get_asset_path(f'images/{self.base_texture}_hovered.png')):
					self.base.surface = pygame.image.load(
						get_asset_path(f'images/{self.base_texture}.png')).convert_alpha()
					self.base.surface.set_alpha(128)
					self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))
		self.base.draw()
		if self.text_size > 0:
			self.button_text.draw()
	def change_base_texture(self, image):
		self.base_texture = image
		self.base.surface = pygame.image.load(
			get_asset_path(f'images/{self.base_texture}.png')).convert_alpha()
		self.base.surface.set_alpha(128)
class SuffSave(dict):
	DEFAULT_OPTIONS = {
		"american_spelling": False,
		"quiz_easy_mode": False,
		"spare_missing_hyphens": True
	}
	def load(self, directory = 'save'): # load save file from disk to memory
		if not path_exists(directory + '.json'):
			saveFile = open(directory + '.json', 'w') # create new json file if file does not exist
			saveFile.write(json_dumps(dict(), indent = 4))
			saveFile.close()
			return
		saveFile = open(directory + '.json', 'r')
		saveJson = json_load(saveFile)
		saveFile.close()
		for key in list(saveJson.keys()):
			self[key] = saveJson[key]
		return
	def flush(self, directory = 'save'): # overrides save file from memory to disk
		saveFile = open(directory + '.json', 'w')
		saveContents = json_dumps(self, indent = 4)
		saveFile.write(saveContents)
		saveFile.close()
	def fetch(self, variable): # returns value of save variable
		if variable in list(self.keys()):
			return self[variable]
		return None
	def fetch_options(self, variable):
		if 'options' not in list(self.keys()):
			self['options'] = self.DEFAULT_OPTIONS
		if variable not in list(self['options'].keys()):
			self['options'][variable] = self.DEFAULT_OPTIONS[variable]
		self.flush()
		return self['options'][variable]

# OBJECTS THAT ARE BUILT ON THE ABOVE CUSTOM OBJECTS #
# They contain special code that is personalized for them #
class Dust(SuffSprite): # Ambient dust particles
	def __init__(self, x, y):
		SuffSprite.__init__(self, x, y, '')
		self.x = x
		self.y = y
		self.size = randint(4, 8)
		self.rect = pygame.Rect(0, 0, self.size, self.size)
		pygame.draw.rect(self.surface, (255, 255, 255), self.rect)
		self.surface.set_alpha(int(random() * 255))
		self.flitter_torque = random() * 5 + self.size
		self.flitter_speed = (random() * 0.5 - 0.5) * 2 / self.flitter_torque
		self.real_x = x
		self.real_y = y
	def draw(self):
		self.real_x, self.real_y = suff_lerp(self.real_x, self.x, 1 / FPS * 6), suff_lerp(self.real_y, self.y, 1 / FPS * 6)
		offsetX, offsetY = sin(curTime * (60 / FPS) * self.flitter_speed) * self.flitter_torque, cos(curTime * (60 / FPS) * self.flitter_speed) * self.flitter_torque
		screen.blit(self.surface, (self.real_x + offsetX * self.size, self.real_y + offsetY * self.size), self.rect)
class CCCSprite(pygame.sprite.Group): # The sprite of the game master capable of speech
	"""
	Summon the almighty biology teacher Mr. Triple C into the algorithm.

	:param int x: The X position of Mr. Triple C.
	:param int y: The Y position of Mr. Triple C.
	"""
	def __init__(self, x, y):
		pygame.sprite.Group.__init__(self)
		self.x = x
		self.y = y
		self.angle = 0
		self.offset = pygame.Vector2(128, 0)
		self.talk_tick = 1
		self.talk_force = 1
		self.talk_offset = 0
		self.head = SuffSprite(self.x, self.y, 'ccc/neutral_head')
		self.mouth = SuffSprite(self.x, self.y, 'ccc/neutral_mouth')
	def change_expression(self, expression):
		self.head.load_graphic(f'ccc/{expression}_head')
		self.mouth.load_graphic(f'ccc/{expression}_mouth')
	def draw(self):
		if self.talk_tick < pi * 3:
			self.talk_tick += 1 / FPS * 30
		talk_coef = sin(self.talk_tick) / self.talk_tick
		w, h = self.head.surface.get_size()
		head_surface2 = pygame.transform.rotate(self.head.surface, self.angle + self.talk_offset * talk_coef)
		mouth_surface2 = pygame.transform.rotate(self.mouth.surface, self.angle + self.talk_offset * talk_coef)
		img2 = head_surface2.get_rect()
		screen.blit(head_surface2, (self.x - (img2.width - self.head.rect.width) / 2,
									self.y - (img2.height - self.head.rect.height) / 2 - talk_coef * 48 * self.talk_force), img2)
		screen.blit(mouth_surface2, (self.x - (img2.width - self.mouth.rect.width) / 2,
									 self.y - (img2.height - self.mouth.rect.height) / 2 + talk_coef * 48 * self.talk_force), img2)
class DialogueBox(pygame.sprite.Group): # RPG styled text boxes used for dialogue.
	"""
	Creates a RPG-styled dialogue box.

	:param tuple pos: The position of the dialogue box.
	:param str text: The text to be displayed of the dialogue box.
	:param int max_char: The maximum number of characters per line.
	:param str style: The orientation of the dialogue box. 'up' or 'down' or 'left' or 'right'.
	:param float fade_time: The seconds it takes for the dialogue box to disappear after the text finishes.
	"""
	padding = 20
	def __init__(self, pos, text, max_char = 10, style = 'up', fade_time = 1.5, fade_function = None, font = 'default'):
		pygame.sprite.Group.__init__(self)
		self.pos:tuple = pos
		self.text:str = text
		self.cur_letter:int = 0
		self.delay:float = 0.025
		self.displayed_text:str = ''
		self.style:str = style
		self.max_char:int = max_char
		self.true_max_char:int = min(len(self.text), self.max_char)
		self.tick:float = 0
		self.fade_time:float = fade_time
		self.fade_function = fade_function
		self.fade_function_called = False
		self.tip = SuffSprite(pos[0], pos[1], f'dialogue/dialogue_box_tip_{style}')
		width, height = self.true_max_char * 32 * FONT_WIDTH_RATIO + self.padding * 2, 32 * len(separate_string(self.text, self.true_max_char)) + self.padding * 2
		if style == 'up':
			box_pos = (self.pos[0] - (width - self.tip.rect.width) / 2 - 20, self.pos[1] - height + 6 - self.tip.rect.height)
			tip_pos = (self.pos[0] - 20, self.pos[1] - self.tip.rect.height)
		elif style == 'down':
			box_pos = (self.pos[0] - (width - self.tip.rect.width) / 2 - 20, self.pos[1] + self.tip.rect.height - 3)
			tip_pos = (self.pos[0] - 20, self.pos[1])
		elif style == 'left':
			box_pos = (self.pos[0] - self.tip.rect.width - width + 4, self.pos[1])
			tip_pos = (self.pos[0] - self.tip.rect.width, self.pos[1])
		else:
			box_pos = (self.pos[0] + self.tip.rect.width - 4, self.pos[1])
			tip_pos = (self.pos[0], self.pos[1])
		self.box = SuffSprite(box_pos[0], box_pos[1])
		self.tip.x, self.tip.y = tip_pos[0], tip_pos[1]

		self.box.surface.fill((255, 255, 255), (0, 0, width, height))
		self.box.rect = pygame.draw.rect(self.box.surface, (0, 0, 0), (0, 0, width, height), 3)
		self.box_text = SuffText(self.box.x + self.padding, self.box.y + self.padding, self.max_char, '', 32, (0, 0, 0), font)
	def draw(self):
		if (self.fade_time != -1 and self.tick < self.fade_time + 1) or (self.fade_time == -1 and self.tick < 2):
			self.tick += 1 / FPS
		if self.displayed_text != self.text:
			if self.tick >= (self.delay if self.text[self.cur_letter - 1] not in DIALOGUE_PAUSE_CHARS else self.delay * 4):
				if self.text[self.cur_letter] not in DIALOGUE_SILENT_CHARS:
					pygame.mixer.Sound.play(UI_DIALOGUE_SOUND)
					if self.cur_letter % 3 == 0 or self.delay >= 0.05:
						CCC.talk_tick = 0
						CCC.talk_force = random() * 0.5 + 0.5
						CCC.talk_offset = randint(-10, 10)
				self.displayed_text += self.text[self.cur_letter]
				self.box_text.set_text(self.displayed_text)
				self.tick = 0
				self.cur_letter += 1
		if self.tick <= self.fade_time or self.fade_time == -1:
			self.box.draw()
			self.tip.draw()
			self.box_text.draw()
		if self.tick > self.fade_time and not self.fade_function_called:
			self.fade_function_called = True
			if self.fade_function: self.fade_function()
class QuizBGTile(SuffSprite):
	def __init__(self, x, y):
		super().__init__(x, y, f'quiz/tile/{randint(1, 3)}')
		self.surface.set_alpha(randint(128, 192))
		self.rect = self.surface.get_rect()
		self.flip_tick = random() * 60
		self.flipped = False
	def draw(self):
		self.flip_tick -= 1 / FPS * 4
		if self.flip_tick <= 0:
			self.flipped = False
			self.flip_tick = pi * 2 + random() * 60
		self.surface2 = pygame.transform.scale(self.surface, (160, 160))
		self.rect2 = self.surface2.get_rect()
		if self.flip_tick <= pi:
			if self.flip_tick <= pi / 2 and not self.flipped:
				self.load_graphic(f'quiz/tile/{randint(1, 3)}')
				self.surface.set_alpha(randint(128, 192))
				self.flipped = True
			self.surface = pygame.transform.scale(self.surface, (160, 160))
			self.surface2 = pygame.transform.scale(self.surface, (abs(cos(self.flip_tick)) * 160, 160))
			self.rect2 = self.surface2.get_rect()
		screen.blit(self.surface2, (self.x - abs(cos(min(pi, self.flip_tick))) * 80 + 80, self.y), self.rect2)
if __name__ == '__main__':
	curSave = SuffSave()
	curSave.load('save')
	fpsCounter = SuffText(0, 0, 16, '0 FPS', 16, (255, 255, 255))
	background = SuffSprite(0, 0, 'background_1')
	background.rect.size = (int(SCREENSIZE[0] * 1.5), int(SCREENSIZE[1] * 1.5))
	background.surface = pygame.transform.scale(background.surface, (background.rect.width, background.rect.height))
	infoText = SuffText(0, 0, 64, 'Dis Thing Dat Thing with CCC', 16,(255, 255, 255))
	infoText.y = SCREENSIZE[1] - infoText.get_height()
	dustGroup = []
	for i in range(20):
		randomPos = (randint(0, SCREENSIZE[0]), randint(0, SCREENSIZE[1]))
		dustGroup.append(Dust(randomPos[0], randomPos[1]))
	# the master of the dictionary application
	CCC = CCCSprite(0, 0)
	RANDOM_DIALOGUE = [
		'Go eat a banana.',
		'Go home and eat a banana.',
		'Your mom? Your dad? Who is it?',
		'12 o\' clock; 3 o\' clock; 6 o\' clock.',
		'Beijing cerebrum.',
		'You know Nanjing\'s friend?',
		'First warning.',
		'Way too weak.',
		'Your concept is not clear.',
		'Dropping is your only option.',
		'Explain. Describe. Compare.',
		'I asked you \'cause I KNOW you can\'t hear it.',
		'Low level.',
		'Zero marks.',
		'Correct direction, still zero marks.',
		'High marks, low intelligence.',
		'OUT.',
		'I bet you didn\'t hear that.',
		'No shame, no pain.',
		'Shamelessness is the most important way of life.',
		"Having a son is God's divine punishment of my sins."
	]
	dialogueBox = DialogueBox((CCC.x + CCC.head.surface.get_width() * 1.1, 300), '', 20, 'right')
	bgMode = 1
	changeBG = True
def state_pre_functions(): # This function is called every time a menu initializes
	global dustGroup
	global CCC
	global dialogueBox
	for dust in dustGroup: # Dust scattering
		randomPos = (randint(0, SCREENSIZE[0]), randint(0, SCREENSIZE[1]))
		dust.x = randomPos[0]
		dust.y = randomPos[1]
	dialogueBox = DialogueBox((0, 0), '', 10)
	CCC.change_expression('neutral') # Make CCC neutral every time he switches to menu
def state_functions(draw_bg = True): # This function is called before every tick function in a menu
	global CCC
	global curTime
	global mousePos
	curTime = pygame.time.get_ticks() / FPS
	clock.tick(FPS)
	mousePos = pygame.mouse.get_pos()
	screen.fill((0, 0, 0))
	if draw_bg: draw_default_bg()
def draw_default_bg():
	global background
	global dustGroup
	global bgMode
	global changeBG
	background.x = (SCREENSIZE[0] - background.surface.get_width()) / 2 + sin(curTime / 120) * 64
	background.y = (SCREENSIZE[1] - background.surface.get_height()) / 2 + cos(curTime / 120) * 36
	if round(pow(cos(curTime / 30), 2)) == 0 and changeBG == True:
		changeBG = False
		bgMode += 1
		if bgMode > 2: bgMode = 1
		background.load_graphic(f'background_{bgMode}')
		background.rect.size = (int(SCREENSIZE[0] * 1.5), int(SCREENSIZE[1] * 1.5))
		background.surface = pygame.transform.scale(background.surface, (background.rect.width, background.rect.height))
	if round(pow(cos(curTime / 30), 2)) == 1 and changeBG == False:
		changeBG = True
	background.surface.set_alpha(int((pow(cos(curTime / 30), 2)) * 255))
	background.draw()
	for dust in dustGroup:
		dust.draw()
def state_post_functions(): # This function is called after every tick function in a menu
	global CCC
	fpsCounter.set_text(str(int(clock.get_fps())) + ' FPS')
	fpsCounter.draw()
	infoText.draw()
	pygame.display.update()

class SuffState(): # Parent class. Used for individual menus.
	def __init__(self, draw_bg = True): # This is called when the state starts to be loaded. Used to load/fetch words from the `words_beta/` folder
		super().__init__()
		self.post_load()
		self.draw_bg = draw_bg
	def post_load(self): # This is called when the state finishes loading. Used for initializing menu elements.
		state_pre_functions()
	def update(self): # This is called every tick.
		state_functions(self.draw_bg)
	def update_post(self): # This is called every tick after the `update` function. Not used yet.
		state_post_functions()
	def handle_event(self, event): # Used to handle events like keyboard presses or mouse presses.
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

class TitleState(SuffState):
	TITLE_SOUND = pygame.mixer.Sound(get_asset_path('music/intro.ogg'))
	TITLE_SOUND.set_volume(0.0)
	def __init__(self):
		super().__init__()
	def post_load(self):
		super().post_load()
		self.banner = SuffSprite(0, 0, 'banner')
		self.banner.surface.set_alpha(255)

		self.text = SuffText(0, 0, 32, 'Press Any Mouse Key', 64)
		self.text.x = (SCREENSIZE[0] - self.text.get_width()) / 2
		self.text.y = (SCREENSIZE[1] - self.text.get_height()) - 64

		self.TITLE_SOUND.stop()
		self.TITLE_SOUND.play()
	def update(self):
		super().update()
		self.banner.draw()
		self.text.set_alpha(pow(sin(curTime / pi), 2) * 255)
		self.text.draw()
	def handle_event(self, event):
		super().handle_event(event)
		if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)):
			self.TITLE_SOUND.stop()
			pygame.mixer.music.load(get_asset_path('music/main_loop.ogg'))
			pygame.mixer.music.play(-1, 0, randint(4000, 8000))
			change_state('main_menu')

class MainMenuState(SuffState):
	def __init__(self):
		super().__init__()
	def post_load(self):
		super().post_load()
		self.renderButtons = False
		def dict_hover():
			global CCC
			CCC.change_expression('happy')
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 + 100),
									  'Learn some vocabulary for your brain library.', 20, 'down')
		def dict():
			change_state('dictionary_search')
		def quiz_hover():
			global CCC
			CCC.change_expression('smug')
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + 100, SCREENSIZE[1] / 2), 'Get mentally tortured while I test your knowledge.', 20, 'right')
		def quiz():
			global dialogueBox
			change_state('quiz_selection')

		def credits_hover():
			global CCC
			CCC.change_expression('furious')
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2),
									  'Check out the people who made this garbage possible.', 20, 'left')

		def credits():
			change_state('credits')

		def options_hover():
			global CCC
			CCC.change_expression('neutral')
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2),
									  "Change my teaching style. Can't change me though.", 20, 'left')

		def options():
			change_state('options')

		def info_hover():
			global CCC
			CCC.change_expression('house')
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2), "You're new here? See how this game works!", 20, 'left')
		def info():
			change_state('info')
		self.dictionaryButton = SuffButton((10, 10), (SCREENSIZE[0] - 20, SCREENSIZE[1] / 2 - 15), dict,
										   'main_menu/dictionary_button',
										   'Dictionary Mode', dict_hover, 96)
		self.dictionaryButton.disabled = True
		self.quizButton = SuffButton((10, SCREENSIZE[1] / 2 + 5), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15),
									 quiz, 'main_menu/quiz_button', 'Quiz Mode', quiz_hover, 64)
		self.quizButton.disabled = True
		self.creditsButton = SuffButton((SCREENSIZE[0] / 2 + 5, SCREENSIZE[1] / 2 + 5),
										(SCREENSIZE[0] / 2 - 25 - 165, SCREENSIZE[1] / 2 - 15), credits,
										'main_menu/credits_button', 'Credits',
										credits_hover, 64)
		self.creditsButton.disabled = True
		self.optionsButton = SuffButton((SCREENSIZE[0] - 10 - 165, self.creditsButton.y),
										(165, 165), options,
										'main_menu/options_button', 'Settings',
										options_hover, 28, None, 4)
		self.optionsButton.disabled = True

		self.infoButton = SuffButton((self.optionsButton.x, SCREENSIZE[1] - 165 - 10),
									 (165, 165), info,
									 'main_menu/info_button', 'Manual',
									 info_hover, 32, None, 8)
		self.infoButton.disabled = True
		infoText.set_text('Dis Thing Dat Thing with CCC')
	def update(self):
		super().update()
		CCC.x = suff_lerp(CCC.x, (SCREENSIZE[0] - CCC.head.surface.get_width()) / 2, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.surface.get_height()) / 2, 1 / FPS * 6)
		distances = (CCC.x + CCC.head.surface.get_width() / 2 - mousePos[0],
					 CCC.y + CCC.head.surface.get_height() / 2 - mousePos[1])
		CCC.angle = distances[0] / SCREENSIZE[0] * 8 * -45 * distances[1] / SCREENSIZE[1] / 2

		# Prevent user from pressing buttons after going out of menus
		if not (pygame.mouse.get_pressed(3)[0] or pygame.mouse.get_pressed(3)[1] or pygame.mouse.get_pressed(3)[2]):
			if not self.renderButtons:
				self.dictionaryButton.disabled = False
				self.quizButton.disabled = False
				self.creditsButton.disabled = False
				self.optionsButton.disabled = False
				self.infoButton.disabled = False
		self.dictionaryButton.draw()
		self.quizButton.draw()
		self.creditsButton.draw()
		self.optionsButton.draw()
		self.infoButton.draw()
		CCC.draw()
		dialogueBox.draw()
	def handle_event(self, event):
		super().handle_event(event)
		global dialogueBox
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				CCC.change_expression(choice(['angry', 'furious', 'smug', 'evil', 'house', 'horror']))
				dialogueBox = DialogueBox((CCC.x + CCC.head.surface.get_width() + 32, 300),
										  choice(RANDOM_DIALOGUE), 20, 'right')

class QuizSelectionState(SuffState):
	def __init__(self):
		super().__init__()
	def post_load(self):
		super().post_load()
		global CCC
		CCC.change_expression('evil')
		CCC.x = (SCREENSIZE[0] - CCC.head.surface.get_width()) / 2
		CCC.y = (SCREENSIZE[1] - CCC.head.surface.get_height()) / 2
		CCC.angle = 0
		def quiz_dictionary():
			QuizState.usesBookmarkWords = False
			change_state('quiz_start')
		def quiz_bookmark():
			global dialogueBox
			if curSave.fetch('bookmarked_words') is None or len(curSave.fetch('bookmarked_words')) < 4:
				CCC.change_expression('neutral')
				dialogueBox = DialogueBox((SCREENSIZE[0] / 2, 540),
										  'You must bookmark at least four words in the dictionary.', 32, 'down')
				return
			QuizState.usesBookmarkWords = True
			change_state('quiz_start')

		self.quizBookmarkButton = SuffButton((0, 0), (360, 360), quiz_bookmark, 'main_menu/quiz/bookmarks', '')
		self.quizBookmarkButton.x = (SCREENSIZE[0] - self.quizBookmarkButton.size[0] * 2) / 2 - 10
		self.quizBookmarkButton.y = (SCREENSIZE[1] - self.quizBookmarkButton.size[1]) / 2
		self.quizBookmarkButtonTxt = SuffText(0, 540, 64, 'Bookmarked Words', 32, (255, 255, 255))
		self.quizBookmarkButtonTxt.x = self.quizBookmarkButton.x + (
				self.quizBookmarkButton.size[0] - self.quizBookmarkButtonTxt.get_width()) / 2
		self.quizDictionaryButton = SuffButton((0, 0), (360, 360), quiz_dictionary, 'main_menu/quiz/dictionary', '')
		self.quizDictionaryButton.x = (SCREENSIZE[0] - self.quizDictionaryButton.size[0] * 2) / 2 + \
									  self.quizDictionaryButton.size[0] + 10
		self.quizDictionaryButton.y = (SCREENSIZE[1] - self.quizDictionaryButton.size[1]) / 2
		self.quizDictionaryButtonTxt = SuffText(0, 540, 64, 'Entire Dictionary', 32, (255, 255, 255))
		self.quizDictionaryButtonTxt.x = self.quizDictionaryButton.x + (
				self.quizDictionaryButton.size[0] - self.quizDictionaryButtonTxt.get_width()) / 2

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')
	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('main_menu')
	def update(self):
		super().update()
		CCC.draw()
		self.quizBookmarkButtonTxt.draw()
		self.quizBookmarkButton.draw()
		self.quizDictionaryButtonTxt.draw()
		self.quizDictionaryButton.draw()
		self.exitButton.draw()
		dialogueBox.draw()
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()

class OptionsState(SuffState):
	class Option():
		def __init__(self, name, variable_type, choices, display_name, description):
			self.name = name
			self.variable_type = variable_type
			self.choices = choices
			self.display_name = display_name
			self.description = description

	AVAILABLE_OPTIONS = [
		Option('american_spelling', 'bool', [True, False], 'American Spelling',
			   "You're really special, aren't you? Well then, I'll use the American spellings instead."),
		Option('quiz_easy_mode', 'bool', [True, False], 'Pity Mode',
			   "You get more time to answer my questions. And I'm gonna donate more lives to you... For a price."),
		Option('spare_missing_hyphens', 'bool', [True, False], 'Lenient Hyphens',
			   "If enabled, missing hyphens will not be counted as a mistake.")
	]
	curChoices = []
	selectedOption:int = 0
	def __init__(self):
		super().__init__()
	def post_load(self):
		super().post_load()
		global CCC
		CCC.change_expression('neutral')

		self.curChoices = [option.choices.index(curSave.fetch_options(option.name)) for option in self.AVAILABLE_OPTIONS]
		self.optionsTxtGroup = []
		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')
		self.playedDialogue = False
		optionTxt:SuffText = SuffText(64, 32, 256, 'SETTINGS', 96, (255, 255, 255))
		self.optionsTxtGroup.append(optionTxt)
		for i in range(len(self.AVAILABLE_OPTIONS)):
			entry = self.AVAILABLE_OPTIONS[i]
			optionButtonSprite = entry.variable_type
			if optionButtonSprite == 'bool':
				optionButtonSprite += '_' + str(curSave.fetch_options(entry.name)).lower()

			optionButton = SuffButton((64, optionTxt.y + optionTxt.get_height() + 32), (72, 72),
									  self.change_option, f'options/' + optionButtonSprite, str(i), None, 0)
			optionTxt = SuffText(optionButton.x + optionButton.size[0] + 16, optionButton.y, 256, entry.display_name, 64, (255, 255, 255))
			self.optionsTxtGroup.append(optionButton)
			self.optionsTxtGroup.append(optionTxt)

	def change_option(self):
		name = self.AVAILABLE_OPTIONS[self.selectedOption].name
		choices = self.AVAILABLE_OPTIONS[self.selectedOption].choices

		self.curChoices[self.selectedOption] += 1
		if self.curChoices[self.selectedOption] >= len(choices):
			self.curChoices[self.selectedOption] = 0
		curSave['options'][name] = choices[self.curChoices[self.selectedOption]]
		for sprite in self.optionsTxtGroup:
			if type(sprite) == SuffButton and sprite.hovered:
				entry = self.AVAILABLE_OPTIONS[int(sprite.text)]
				optionButtonSprite = entry.variable_type
				if optionButtonSprite == 'bool':
					optionButtonSprite += '_' + str(curSave.fetch_options(entry.name)).lower()
				sprite.change_base_texture('options/' + optionButtonSprite)
		# print(curSave['options'])

	def play_dialogue(self, index):
		global dialogueBox
		dialogueBox = DialogueBox((CCC.x, CCC.y + CCC.head.surface.get_width() // 2),
								  self.AVAILABLE_OPTIONS[index].description, 54, 'left', -1)
	def reset_dialogue(self):
		global dialogueBox
		dialogueBox.fade_time = 2
	def back_to_main_menu(self):
		curSave.flush()
		UI_MENU_EXIT_SOUND.play()
		change_state('main_menu')
	def update(self):
		super().update()
		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
		CCC.draw()
		buttonsHovered = 0
		for sprite in self.optionsTxtGroup:
			sprite.draw()
			if type(sprite) == SuffButton and sprite.hovered:
				self.selectedOption = int(sprite.text)
				buttonsHovered += 1
		if buttonsHovered > 0:
			if not self.playedDialogue:
				self.playedDialogue = True
				self.play_dialogue(self.selectedOption)
		else:
			self.playedDialogue = False

		self.exitButton.draw()
		dialogueBox.draw()
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()

curState:SuffState = None

def change_state(state):
	global curState
	curState = states[state]
	states[state].__init__()

class DictionarySearchState(SuffState):
	autoQueryTick = 0
	autoSearched = False
	def post_load(self):
		super().post_load()
		global dialogueBox
		dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
								  'Type a word in the field and press [ENTER].', 20, 'down', -1)
		self.searchTitle = SuffText(128, 64, 16, 'Search For Word', 80, (255, 255, 255))
		self.searchTitle.set_alpha(0)
		self.searchQuery = SuffText(128, self.searchTitle.y + 64 + 16, 25, '', 48, (255, 255, 255))
		self.searchIBeam = SuffText(128, self.searchQuery.y, 1, '_', 48, (255, 255, 255))
		self.wordList = []
		self.autoQueries = []
		self.hoveredAutoQuery = ''
		self.searchTitle.y = 0
		def go_to_bookmarks():
			if curSave.fetch('bookmarked_words') is None:
				CCC.change_expression('angry')
				global dialogueBox
				dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
										  "Dude, you haven't even bookmarked a single word.", 20, 'down', -1)
				return
			change_state('dictionary_bookmarks')
		self.bookmarkButton = SuffButton((128, self.searchQuery.y + 64), (72, 104), go_to_bookmarks, 'dictionary/bookmark')
		self.bookmarkText = SuffText(self.bookmarkButton.x + 72 + 16, self.bookmarkButton.y + 24, 32, 'Bookmarked Words', 32, (255, 255, 255))

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')

	def bubble_sort_word(self, letter):
		arrFile = open(get_asset_path(f'data/words/{letter}.json'), 'r', encoding = 'utf-8')
		arr = json_load(arrFile)
		arrFile.close()
		for i in range(len(arr)):
			for j in range(len(arr) - 1):
				if arr[j]['word'].lower() > arr[j + 1]['word'].lower():
					arr[j], arr[j + 1] = arr[j + 1], arr[j]
		arrFileWrite = open(get_asset_path(f'data/words/{letter}.json'), 'w')
		arrFileWrite.write(json_dumps(arr, indent = 4, ensure_ascii = False))
		arrFileWrite.close()

	def binary_search_word(self, x):
		global wordList
		low = 0
		high = len(wordList) - 1
		while low <= high:
			mid = low + (high - low) // 2
			if x.lower() == wordList[mid]['word'].lower() or \
					x.lower() == wordList[mid]['plural'].lower() or \
					x.lower() in wordList[mid]['redirects'] or \
					x.lower() == wordList[mid]['word_alt'] or \
					x.lower() == wordList[mid]['plural_alt']:
				return wordList[mid]
			elif (wordList[mid]['word'].lower() < x.lower()):
				low = mid + 1
			else:
				high = mid - 1
		return None

	def search_for_word(self, word):
		global wordList
		if len(word) < 1 or not path_exists(get_asset_path(f'data/words/{word[0]}.json')):
			return None
		self.bubble_sort_word(word[0])
		wordFile = open(get_asset_path(f'data/words/{word[0]}.json'), 'r', encoding='utf-8')
		wordList = json_load(wordFile)
		# print(wordList)
		wordFile.close()
		wordData = self.binary_search_word(word)
		return wordData

	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('main_menu')

	def update(self):
		super().update()
		global dialogueBox

		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] / 2 + (SCREENSIZE[0] / 2 - CCC.head.rect.width) / 2, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.rect.height) / 2, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 0, 1 / FPS * 6)
		self.searchIBeam.x = self.searchQuery.x + (
				len(self.searchQuery.text) % self.searchQuery.width) * self.searchQuery.size * FONT_WIDTH_RATIO
		self.searchTitle.y = suff_lerp(self.searchTitle.y, 64, 1 / FPS * 6)
		self.searchTitle.set_alpha(suff_lerp(self.searchTitle.alpha, 255, 1 / FPS * 6))  # smooth fade-in animation

		CCC.draw()
		dialogueBox.draw()
		self.searchTitle.draw()
		self.searchQuery.draw()
		self.bookmarkButton.draw()
		self.bookmarkText.draw()
		self.exitButton.draw()
		for word in self.autoQueries:
			word.draw()
			if word.hovered:
				self.hoveredAutoQuery = word.text
		if not self.autoSearched:
			self.autoQueryTick += 1 / FPS
			if self.autoQueryTick >= 0: # rate limited to prevent lag
				self.autoSearched = True
				self.auto_search()

		if len(self.searchQuery.text) < self.searchQuery.width: self.searchIBeam.draw()  # Prevent I-Beam from rendering when search field is full.
	def auto_search(self):
		query = self.searchQuery.text
		containingWords = []
		if len(query) >= 1 and path_exists(get_asset_path(f'data/words/{query[0]}.json')):
			wordFile = open(get_asset_path(f'data/words/{query[0]}.json'), 'r', encoding='utf-8')
			leWordList = json_load(wordFile)
			wordFile.close()
			for word in leWordList:
				defaultSpelling = get_used_spelling(word['word'], word['word_alt'])
				if ((word['word'].lower().startswith(query.lower()) and word['word'] != query) or \
					(word['word_alt'].lower().startswith(query.lower()) and word['word_alt'] != query)) and \
						word['class'] != 'easter egg':
					containingWords.append(defaultSpelling)
		# print(containingWords)
		self.render_auto_search_words(containingWords)

	def render_auto_search_words(self, array):
		self.autoQueries.clear()
		wordButton = SuffButton((self.bookmarkButton.x, self.bookmarkButton.y + self.bookmarkButton.size[1] - 48),
								(0, 32), self.binary_search_word)
		for word in array:
			wordButton = SuffButton((self.bookmarkButton.x, wordButton.y + 48), (32 * len(word), 32), self.copy_auto_query_to_search_bar, '', word, None,
									32,
									(128, 128, 128))  # Visually, it is not a button, but it still calls functions when clicked
			wordButton.base.surface.set_alpha(0)
			self.autoQueries.append(wordButton)

	def copy_auto_query_to_search_bar(self):
		self.searchQuery.set_text(self.hoveredAutoQuery)
		self.autoQueryTick = 0
		self.autoSearched = False

	def handle_event(self, event):
		super().handle_event(event)
		global dialogueBox
		global curState

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if all(x.isalpha() or x.isspace() for x in self.searchQuery.text): # iterates all characters, if it's a letter + has a space
					w = self.search_for_word(
						self.searchQuery.text.lower().strip())  # get word words from word folder (also
					# removes leading/ending whitespaces and
					# makes it lowercase)
					if w: # if word data exists
						DictionaryWordState.curWordData = w
						change_state('dictionary_word')
					else:
						UI_INVALID_SOUND.play()
						CCC.change_expression('angry')
						dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
												  'I don\'t think that word exists in my library.', 20,
												  'down', -1)
				else:
					UI_INVALID_SOUND.play()
					CCC.change_expression('angry')
					dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
											  'I don\'t believe a human speaks like that.', 20, 'down', -1)
			elif event.key == pygame.K_BACKSPACE:
				self.searchQuery.set_text(self.searchQuery.text[0:len(self.searchQuery.text) - 1])
				self.autoSearched = False
				self.autoQueryTick = 0
				UI_TEXT_ERASE_SOUND.play()
			elif len(self.searchQuery.text) < self.searchQuery.width:
				self.searchQuery.set_text(self.searchQuery.text + event.unicode)
				self.autoSearched = False
				self.autoQueryTick = 0
				UI_TEXT_TYPE_SOUND.play()
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()

class DictionaryWordState(SuffState):
	curWordData = {
		"word": "asexual reproduction",
		"class": "noun phrase",
		"redirects": [],
		"full": "",
		"word_alt": "",
		"plural_alt": "",
		"forms": {},
		"plural": "",
		"definition": "A form of reproduction that involves a single parent by mitotic cell division.",
		"translation": "\u7121\u6027\u751f\u6b96"
	}
	def __init__(self):
		super().__init__()
	def save_word(self):
		global dialogueBox
		if curSave.fetch('bookmarked_words') is None:
			curSave['bookmarked_words'] = []
		if self.curWordData['word'] in curSave['bookmarked_words']:
			curSave['bookmarked_words'].remove(self.curWordData['word'])
			dialogueBox = DialogueBox((CCC.x, CCC.y), 'Word unbookmarked.', 16, 'left')
			self.bookmarkButton.change_base_texture('dictionary/bookmark')
		else:
			for i in range(len(curSave['bookmarked_words'])):
				if curSave['bookmarked_words'][i] > self.curWordData['word']:
					curSave['bookmarked_words'].insert(i, self.curWordData['word'])
					break
			if self.curWordData['word'] not in curSave['bookmarked_words']:
				curSave['bookmarked_words'].append(self.curWordData['word'])
			dialogueBox = DialogueBox((CCC.x, CCC.y), 'Word bookmarked.', 16, 'left')
			self.bookmarkButton.change_base_texture('dictionary/unbookmark')
		curSave.flush('save')
	def post_load(self):
		super().post_load()
		defaultSpelling = get_used_spelling(self.curWordData['word'], self.curWordData['word_alt'])
		altSpelling = get_used_spelling(self.curWordData['word'], self.curWordData['word_alt'], True)
		defaultPluralSpelling = get_used_spelling(self.curWordData['plural'], self.curWordData['plural_alt'])
		altPluralSpelling = get_used_spelling(self.curWordData['plural'], self.curWordData['plural_alt'], True)
		self.textGroup = []
		self.isEasterEgg = self.curWordData['class'] == 'easter egg'
		wordTitle = SuffText(32, 32, 32, defaultSpelling, 96,
							 (255, 255, 255))
		self.textGroup.append(wordTitle)
		wordClassTxtString = self.curWordData['class'] # part of speech
		if len(self.curWordData['plural']) > 0:
			wordClassTxtString += ', plural \'' + defaultPluralSpelling + '\'' # plural form
		if len(self.curWordData['full']) > 0:
			wordClassTxtString += ', full form \'' + self.curWordData['full'] + '\'' # plural form
		wordClassTxt = SuffText(32, wordTitle.y + wordTitle.get_height() + 8, 32, wordClassTxtString, 32, (255, 255, 255))
		self.textGroup.append(wordClassTxt)
		wordDefTxt = SuffText(32, wordClassTxt.y + wordClassTxt.get_height() + 32, 48, self.curWordData['definition'], 32, (255, 255, 255))
		self.textGroup.append(wordDefTxt)
		wordTransDescTxt = SuffText(32, wordDefTxt.y + 32 + wordDefTxt.get_height(), 48, '', 32, (255, 255, 255))
		if not self.isEasterEgg:
			if self.curWordData['translation'] != self.curWordData['word']:
				wordTransDescTxt.set_text(defaultSpelling[0].upper() + defaultSpelling[1:] + ' means ')
				self.textGroup.append(wordTransDescTxt)
				wordTransTxt = SuffText(wordTransDescTxt.x + wordTransDescTxt.get_width(), wordTransDescTxt.y, 48,
										self.curWordData['translation'], 32, (255, 255, 255), 'zh')
				self.textGroup.append(wordTransTxt)
		else:
			pygame.mixer.Sound(get_asset_path('sounds/a_carinha_dele.ogg')).play()
			global dialogueBox
			dialogueBox = DialogueBox((SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3), self.curWordData['translation'], 16, 'left', -1)

		wordDescTxt = SuffText(32, wordTransDescTxt.y + wordTransDescTxt.get_height() + 32, 48, '', 48, (128, 128, 128))
		if len(altSpelling) > 0:
			wordDescTxt.set_text('{ ALTERNATIVE SPELLING }')
			self.textGroup.append(wordDescTxt)
			altSpellingString = altSpelling
			if altPluralSpelling != '':
				altSpellingString += ', plural \'' + altPluralSpelling + '\''
			wordDescTxt = SuffText(32, wordDescTxt.y + wordDescTxt.get_height(), 48, altSpellingString, 32,
								   (255, 255, 255))
			self.textGroup.append(wordDescTxt)
		if len(self.curWordData['forms']) > 0:
			wordDescTxt = SuffText(32, wordDescTxt.y + wordDescTxt.get_height() + 32, 48, '{ FORMS }', 64,
								   (128, 128, 128))
			self.textGroup.append(wordDescTxt)
			for key in self.curWordData['forms'].keys():
				wordDescTxt = SuffText(32, wordDescTxt.y + wordDescTxt.get_height() + 32, 48, key, 48,
									   (192, 192, 192))
				self.textGroup.append(wordDescTxt)
				formContent = self.curWordData['forms'][key]
				tenses = [
					'simple present',
					'3rd person present',
					'present participle',
					'simple past',
					'past participle'
				]
				for i in range(len(formContent)):
					wordDescTxt = SuffText(32, wordDescTxt.y + wordDescTxt.get_height() + 8,
										   48, '', 16,
										   (128, 128, 128))
					if key.startswith('verb') == True:
						wordDescTxt.set_text(tenses[i] + ' ')
						self.textGroup.append(wordDescTxt)
					wordDescTxt = SuffText(32 + wordDescTxt.get_width(), wordDescTxt.y - 8, 48,
										   formContent[i], 32,
										   (255, 255, 255))
					self.textGroup.append(wordDescTxt)

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')
		if not self.isEasterEgg:
			self.bookmarkButton = SuffButton((self.exitButton.x - 10 - self.exitButton.size[0], self.exitButton.y), (72, 104), self.save_word, 'dictionary/bookmark')
			if curSave.fetch('bookmarked_words') is not None and self.curWordData['word'] in curSave['bookmarked_words']:
				self.bookmarkButton.change_base_texture('dictionary/unbookmark')

		self.scrollAmount = 0
		self.txtYOrigin = []
		self.txtYOriginalOrigin = []
		self.txtText = []
		for i in range(len(self.textGroup)):
			self.txtText.append(self.textGroup[i].text)
			self.textGroup[i].set_text('')
			self.txtYOriginalOrigin.append(self.textGroup[i].y)
			self.txtYOrigin.append(self.textGroup[i].y)
		self.maxScroll = min(-ceil((max(self.txtYOriginalOrigin) + 48 - SCREENSIZE[1]) / 64), 0)
		self.txtTypeTick = 0
		self.playAnim = 3

	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('dictionary_search')
	def update(self):
		state_functions()

		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
		CCC.draw()
		dialogueBox.draw()
		if not self.isEasterEgg: self.bookmarkButton.draw()
		self.exitButton.draw()
		self.txtTypeTick += 1 / FPS
		playSound = False
		for i in range(len(self.textGroup)):
			if len(self.textGroup[i].text) < len(self.txtText[i]) and self.txtTypeTick > 0.025:
				if self.txtText[i][len(self.textGroup[i].text)] not in DIALOGUE_SILENT_CHARS: playSound = True
				self.textGroup[i].set_text(self.textGroup[i].text + self.txtText[i][len(self.textGroup[i].text)])
			self.textGroup[i].draw()
		if playSound:
			UI_DIALOGUE_SOUND.play()
			self.playAnim += 1
			if self.playAnim > 3:
				CCC.talk_force = random() * 0.5 + 0.5
				CCC.talk_tick = 0
				CCC.talk_offset = randint(-10, 10)
				self.playAnim = 0
			self.txtTypeTick = 0
		for i in range(len(self.textGroup)):
			self.textGroup[i].y = suff_lerp(self.textGroup[i].y, self.txtYOrigin[i], 1 / FPS * 6)
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()
		if event.type == pygame.MOUSEWHEEL:
			self.scrollAmount += event.y
			if self.scrollAmount > 0:
				self.scrollAmount = 0
			if self.scrollAmount < self.maxScroll:
				self.scrollAmount = self.maxScroll
			for i in range(len(self.textGroup)):
				self.txtYOrigin[i] = self.txtYOriginalOrigin[i] + self.scrollAmount * 64
class DictionaryBookmarkState(SuffState):
	def __init__(self):
		super().__init__()
	def binary_search_word(self):
		x = self.curWord
		# print(x)
		if len(x) <= 0: return
		f = open(get_asset_path(f'data/words/{x[0]}.json'), 'r', encoding = 'utf-8')
		wordList = json_load(f)
		f.close()
		low = 0
		high = len(wordList) - 1
		while low <= high:
			mid = low + (high - low) // 2
			if x.lower() == wordList[mid]['word'].lower():
				DictionaryWordState.curWordData = wordList[mid]
				change_state('dictionary_word')
				break
			elif (wordList[mid]['word'].lower() < x.lower()):
				low = mid + 1
			else:
				high = mid - 1
		return None
	def post_load(self):
		savedWords = curSave.fetch('bookmarked_words')
		super().post_load()
		if savedWords is None:
			return
		pointer = string.ascii_lowercase.index(savedWords[0][0].lower())
		leEntryList = []
		DictWithWords = dict()
		for word in savedWords: # Group words by alphabetical order
			if word.lower()[0] == string.ascii_lowercase[pointer]:
				leEntryList.append(word)
			else:
				DictWithWords[string.ascii_lowercase[pointer]] = leEntryList
				pointer += ord(word.lower()[0]) - ord(string.ascii_lowercase[pointer])
				leEntryList = []
				leEntryList.append(word)
		DictWithWords[string.ascii_lowercase[pointer]] = leEntryList
		self.textGroup = []

		self.curWord = ''

		prevHeight = 32
		for alpha in DictWithWords.keys():
			alphaText = SuffText(32, prevHeight, 32, alpha.upper(), 128,
								 (192, 192, 192))
			self.textGroup.append(alphaText)
			prevHeight += alphaText.get_height()
			for word in DictWithWords[alpha]:
				wordButton = SuffButton((32, prevHeight), (32 * len(word), 32), self.binary_search_word, '', word, None,
										32)  # Visually, it is not a button, but it still calls functions when clicked
				wordButton.base.surface.set_alpha(0)
				self.textGroup.append(wordButton)
				prevHeight += wordButton.size[1] * 1.5

		self.scrollAmount = 0
		self.txtYOrigin = []
		self.txtYOriginalOrigin = []
		for i in range(len(self.textGroup)):
			self.txtYOriginalOrigin.append(self.textGroup[i].y)
			self.txtYOrigin.append(self.textGroup[i].y)
		self.maxScroll = min(-ceil((max(self.txtYOriginalOrigin) + 128 - SCREENSIZE[1]) / 64), 0)

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')

	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('dictionary_search')
	def update(self):
		state_functions()

		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
		CCC.draw()
		self.exitButton.draw()
		for i in range(len(self.textGroup)):
			self.textGroup[i].draw()
			self.textGroup[i].y = suff_lerp(self.textGroup[i].y, self.txtYOrigin[i], 1 / FPS * 6)
			if type(self.textGroup[i]) == SuffButton and self.textGroup[i].hovered:
				self.curWord = self.textGroup[i].text
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()
		if event.type == pygame.MOUSEWHEEL:
			self.scrollAmount += event.y
			if self.scrollAmount > 0:
				self.scrollAmount = 0
			if self.scrollAmount < self.maxScroll:
				self.scrollAmount = self.maxScroll
			for i in range(len(self.textGroup)):
				self.txtYOrigin[i] = self.txtYOriginalOrigin[i] + self.scrollAmount * 64

class QuizStartState(SuffState):
	def __init__(self):
		super().__init__(False)

	def post_load(self):
		self.index = 0
		# Dialogue, Expression, Beat Number, Dialogue Speed
		self.dialogue = [
			["They don\'t call me Chief Executive Chow for nothin', kid.", 'neutral', 0, 0.03],
			["I have ruined the futures of countless candidates.", 'happy', 8, 0.03],
			["I'll give you a definition and three chances to answer my questions.", 'smug', 16, 0.03],
			["And if you use all my chances...", 'evil', 24, 0.03],
			["YOU DIE.", 'horror', 28, 0.06],
			["", 'horror', 31, 0],
			["", '', 32, 0]
		]
		self.black = SuffSprite(0, 0)
		self.black.rect = pygame.draw.rect(self.black.surface, (0, 0, 0), (0, 0, SCREENSIZE[0], SCREENSIZE[1]))
		self.black.surface.set_alpha(0)
		pygame.mixer.music.load(get_asset_path('music/pre_quiz.ogg'))
		pygame.mixer.music.play()
		self.curBeat = 0
		infoText.set_text('Click Anywhere to Skip' if curSave.fetch('quiz_highscore') else '')
		super().post_load()
		self.BPM = 144

	def update(self):
		global dialogueBox
		self.curBeat = int((pygame.mixer.music.get_pos() + 50) / (60 / self.BPM * 1000)) # Current beat of the music.
		super().update()
		for event in self.dialogue: # This causes dialogue to sync with the music.
			if event[2] == self.curBeat:
				if event[0] != '':
					dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 - 100),
											  event[0], min(20, len(event[0])), 'up', -1)
					dialogueBox.delay = event[3]
				else:
					self.black.surface.set_alpha(255)
				if event[1] != '':
					CCC.change_expression(event[1])
				self.dialogue.pop(0)
				if len(self.dialogue) <= 0:
					change_state('quiz')
				self.index += 1
		CCC.x = suff_lerp(CCC.x, (SCREENSIZE[0] - CCC.head.rect.width) / 2, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.rect.height) / 2 + 100, 1 / FPS * 6)
		CCC.angle = 0
		CCC.draw()
		dialogueBox.draw()
		self.black.draw()

	def handle_event(self, event):
		# (Intentional) Without the super() function, quitting is disabled
		if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)) and curSave.fetch('quiz_highscore') is not None:
			change_state('quiz')

class QuizState(SuffState):
	usesBookmarkWords = False
	def __init__(self):
		self.leWordData = dict()
		self.defaultSpelling = ''
		self.allowInput = False
		self.derList = []
		for alp in string.ascii_lowercase: # From a to z
			if path_exists(get_asset_path(f'data/words/{alp}.json')):
				file = open(get_asset_path(f'data/words/{alp}.json'), 'r', encoding = 'utf-8')
				leJson = json_load(file)
				file.close()
				for item in leJson:
					if item['class'] != 'easter egg':
						if (self.usesBookmarkWords and item['word'] in curSave.fetch('bookmarked_words')) or not self.usesBookmarkWords:
							self.derList.append(item)

		self.lives = 3
		self.maxLives = 4
		self.timePenalty = 0.25
		self.scorePenalty = 0
		if curSave.fetch_options('quiz_easy_mode'):
			self.lives = 4
			self.maxLives = 6
			self.timePenalty = 0.2
			self.scorePenalty = 0.5
		self.cccExpressions = ['horror', 'demon', 'evil', 'smug', 'neutral'] # life based
		self.CCC_HAPPY_EXPRESSIONS = ['smug', 'happy', 'house']
		self.CCC_ANGRY_EXPRESSIONS = ['angry', 'furious']
		self.actualInput = ''
		self.CCC_HAPPY_LINES = [
			'Very good.',
			'Quite good.',
			'Acceptable.'
		]
		self.baseTimeLimit = 30
		self.timeLeft = 30
		self.countdown = False
		self.CCC_ANGRY_LINES = [
			'Go eat a banana.',
			'Go home and eat a banana.',
			'6 o\' clock.',
			'Beijing cerebrum.',
			'Way too weak.',
			'Your concept is not clear.',
			'Dropping is your only option.',
			'Low level.',
			'Zero marks.'
		]
		super().__init__(False)

	def post_load(self):
		super().post_load()
		self.jeffs = [] # Group for background tiles that "rotate"
		self.dust = [] # Group for dust particles
		self.reds = [] # Group for translucent red overlay
		self.hearts = [] # Group for heart sprites (indicator for num. of lives)
		self.brokenHearts = [] # Group for broken heart sprites
		self.correctLettersTxt = [] # Group for correct letters (as text)

		self.searchQuery = SuffText(SCREENSIZE[0] / 2, 600, 25, '', 64, (255, 255, 255)) # Actual player input
		self.searchIBeam = SuffText(SCREENSIZE[0] / 2, 600 + 64, 25, '^', 64, (255, 255, 255)) # That I-Beam you see when you usually type something
		self.curBeat = 0 # Current beat of the background music
		# BG Stuff
		self.jeff_velocity = 640
		self.BPM = 144
		self.jeff_width = ceil(SCREENSIZE[0] / 160)
		self.jeff_height = ceil(SCREENSIZE[1] / 160)
		for x in range(0, self.jeff_width + 1):  # Every Quiz BG Tile sprite is 80 x 80.
			for y in range(0, self.jeff_height):
				jeff = QuizBGTile(x * 160, y * 160 - 40)
				self.jeffs.append(jeff)
		self.bg = SuffSprite(0, 0, 'quiz/bg')
		self.bg.surface = pygame.transform.scale(self.bg.surface, (SCREENSIZE[0], SCREENSIZE[1]))
		self.bg.rect = self.bg.surface.get_rect()
		for i in range(0, 50):
			red = Dust(randint(0, SCREENSIZE[0]), randint(0, SCREENSIZE[1]))
			self.dust.append(red)
		for i in range(1, 9):
			red = SuffSprite(0, SCREENSIZE[1] - SCREENSIZE[1] / 3 / 4 * i)
			red.rect = pygame.draw.rect(red.surface, (255, 0, 0), (0, 0, SCREENSIZE[0], SCREENSIZE[1] / 3 / 4 * i))
			red.surface.set_alpha(32)
			self.reds.append(red)
		self.flash = SuffSprite(0, 0)
		self.flash.rect = pygame.draw.rect(self.flash.surface, (255, 255, 255), (0, 0, SCREENSIZE[0], SCREENSIZE[1]))
		self.flash.surface.set_alpha(255)
		pygame.mixer.music.load(get_asset_path('music/quiz_loop.ogg'))
		pygame.mixer.music.play(-1)
		infoText.set_text('Death By CCC')
		self.cccVelocityX = SCREENSIZE[0] / ceil((random() + 0.01) * 2) * choice([1, -1])
		self.cccVelocityY = SCREENSIZE[1] / ceil((random() + 0.01) * 2) * choice([1, -1])

		self.timeTxt = SuffText(0, 0, 4, '', 16 * 32, (255, 255, 255))
		for i in range(self.lives):
			self.add_heart()

		self.curScore = 0
		self.reset()
	def reset(self):
		CCC.change_expression(self.cccExpressions[clamp(self.lives, 0, 4)])
		global dialogueBox
		self.attempts = 0
		self.allowInput = True
		self.leWordData = choice(self.derList) # current word, answer
		self.defaultSpelling = get_used_spelling(self.leWordData['word'], self.leWordData['word_alt'])
		self.actualInput = ''
		self.searchQuery.set_text(self.string_padding(self.actualInput))
		self.searchQuery.x = (SCREENSIZE[0] - self.searchQuery.get_width()) / 2
		self.searchIBeam.x = self.searchQuery.x + len(
			self.actualInput) * self.searchIBeam.get_width()  # Adjust I-Beam position
		self.baseTimeLimit = int(clamp(35 - pow(30, 0.05 * self.curScore), 3, 30))
		# With each correct answer, CCC's patience decreases. When you play really well, you only get 4 seconds to guess.
		# Maximum of 31 seconds are given.
		if curSave.fetch_options('quiz_easy_mode'):
			self.baseTimeLimit = int(self.baseTimeLimit * 1.5)
		self.baseTimeLimit += 1
		self.timeLeft = self.baseTimeLimit # Actual timer
		self.misplacedLetters = []  # List of characters that exist in the word but wrong position
		self.correctLetters = []  # List of characters that exist in the word and correct position
		self.wrongLetters = []  # List of characters that does not satisfy both requirements

		self.correctLettersTxt = []
		self.misplacedLettersTxt = []
		self.wrongLettersTxt = []
		ogDef = self.leWordData['definition']
		leFont = 'default'
		if choice([True, False]) and ogDef == self.leWordData['word']: # 50% chance to display the Chinese definition instead
			ogDef = self.leWordData['translation']
			leFont = 'zh' # Uses Chinese font instead
		senDef = ogDef[0].lower() + ogDef[1:len(ogDef) - 1] + ogDef[len(ogDef) - 1].replace('.', '')
		partOfSpeech = self.leWordData['class']
		leDialogue = f'What is the {partOfSpeech} for {senDef}?'
		# print(self.leWordData['word'])
		dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2),
								  leDialogue, 50, 'down', -1, None, leFont) # Limits dialogue width by 50 chars
	def add_heart(self):
		heart = SuffSprite(0, SCREENSIZE[1], 'quiz/heart')
		heart.surface = pygame.transform.scale(heart.surface, (50, 50))
		heart.rect = heart.surface.get_rect()
		self.hearts.append(heart)
	def remove_heart(self):
		leLittleHeart:SuffSprite = self.hearts.pop()
		leLittleHeart.load_graphic('quiz/heart_broken')
		leLittleHeart.surface = pygame.transform.scale(leLittleHeart.surface, (50, 50))
		leLittleHeart.rect = leLittleHeart.surface.get_rect()
		self.brokenHearts.append(leLittleHeart)

	def update(self):
		super().update()
		self.bg.draw()
		global dialogueBox

		self.jeff_velocity = suff_lerp(self.jeff_velocity, max(0, 240 + (3 - self.lives) * 120), 1 / FPS * 4) # Tiles scroll faster with each life lost
		self.cccVelocityX = suff_lerp(self.cccVelocityX, max(0, 150 + (3 - self.lives) * 80), 1 / FPS * 2)
		self.cccVelocityY = suff_lerp(self.cccVelocityY, 50 + max(0, 3 - self.lives) * 50, 1 / FPS * 2)
		for i in range(len(self.jeffs)):
			self.jeffs[i].x -= 1 / FPS * self.jeff_velocity
			if self.jeffs[i].x < -160:
				self.jeffs[i].x = SCREENSIZE[0] + 160 + self.jeffs[i].x # Put tiles back to their starting position (off-screen)
			self.jeffs[i].y = sin(self.curBeat * pi / 2 + (
					i // self.jeff_height) * pi / self.jeff_height) * 40 + i % self.jeff_height * 160 - 40
			# Make tiles fluctuate in a wave pattern.
			self.jeffs[i].draw()
		for dust in self.dust:
			dust.x += sin(self.curBeat * pi / 2 * dust.flitter_speed * dust.flitter_torque) * dust.flitter_torque / 5
			# Make dust particles move left and right to stimulate sparks/smoke produced from burning.
			dust.y -= 1 / FPS * 320 * abs(dust.flitter_speed * dust.flitter_torque * 2 + 1) # Make le dust go up
			if dust.real_y < -160:
				dust.y = SCREENSIZE[1] + SCREENSIZE[1] * random() / 2 # Put dust back to their starting position, along with a random offset (off-screen)
				dust.real_y = dust.y
			dust.draw()
		if not self.countdown and dialogueBox.text == dialogueBox.displayed_text and self.allowInput:
			self.countdown = True
		self.curBeat = (pygame.mixer.music.get_pos() + 10) / (60 / self.BPM * 1000) # Current beat of the BGM
		CCC.angle = sin(self.curBeat * pi / 2) * -45 / max(1, self.lives)
		CCC.x = (SCREENSIZE[0] - CCC.head.rect.width) / 2 + sin(self.curBeat * pi / 2) * self.cccVelocityX
		CCC.y = 50 + sin(self.curBeat * pi) * self.cccVelocityY
		# Makes CCC shift around like a maniac
		CCC.draw()
		if self.countdown:
			self.timeLeft -= 1 / FPS
			self.timeTxt.set_text(str(int(self.timeLeft)))
			self.timeTxt.x = (SCREENSIZE[0] - self.timeTxt.get_width()) / 2
			self.timeTxt.y = 0
			self.timeTxt.set_alpha(64)
			self.timeTxt.draw()
			if self.timeLeft < 0:
				self.allowInput = False
				if not self.check_answer():
					UI_INVALID_SOUND.play()
					self.correctLettersTxt = []
					self.misplacedLettersTxt = []
					self.wrongLettersTxt = []
					CCC.change_expression(choice(self.CCC_ANGRY_EXPRESSIONS))
					leLine = 'The word is ' + self.defaultSpelling + '. ' + choice(self.CCC_ANGRY_LINES)
					dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 - 200),
											  leLine, min(32, len(leLine)), 'up', 1, self.reset)
					self.lives = clamp(self.lives - 1, 0, self.maxLives)
					self.remove_heart()
					if self.lives <= 0:
						self.just_die()
						return
					self.countdown = False
		for i in range(len(self.reds)):
			self.reds[i].y = SCREENSIZE[1] - pow(sin(self.curBeat / 4 * pi + pi / 4), 2) * SCREENSIZE[1] / 3 / 4 * i
			# Makes red overlay fluctuate with rhythm
			self.reds[i].draw()
		dialogueBox.draw()
		for heart in self.hearts:
			leIndex = self.hearts.index(heart)
			if self.allowInput:
				heartBasePos = (dialogueBox.pos[0] - dialogueBox.box.rect.width / 2,
								dialogueBox.pos[1] + 40 + dialogueBox.box.rect.height)
			else:
				heartBasePos = (dialogueBox.pos[0] - dialogueBox.box.rect.width / 2,
								SCREENSIZE[1] * 1.5)
			heart.x = suff_lerp(heart.x, heartBasePos[0] + leIndex * 50 + sin(
				self.curBeat * pi / 4 + leIndex) * 10, 1 / FPS * 4)
			heart.y = suff_lerp(heart.y, heartBasePos[1] + sin(
				self.curBeat * pi / 2 + leIndex) * 10, 1 / FPS * 4)
			heart.draw()
		for broken_heart in self.brokenHearts:
			broken_heart.y += 1 / FPS * 720
			broken_heart.draw()
		for letter in self.correctLettersTxt:
			letter.y = self.searchQuery.y + sin(letter.x + curTime / 5) * 4
			letter.draw()
		for l in range(len(self.misplacedLettersTxt)):
			self.misplacedLettersTxt[l].x = (SCREENSIZE[0] - self.misplacedLettersTxt[l].size) / 2 + sin(l + curTime / len(self.defaultSpelling)) * self.searchQuery.get_width() / 2
			self.misplacedLettersTxt[l].y = self.searchQuery.y - 64 + cos(l + curTime / len(self.defaultSpelling)) * 16
			self.misplacedLettersTxt[l].draw()
		for l in range(len(self.wrongLettersTxt)):
			self.wrongLettersTxt[l].x = (SCREENSIZE[0] - self.wrongLettersTxt[l].size) / 2 + sin(l + curTime / len(self.defaultSpelling)) * SCREENSIZE[0] / 4
			self.wrongLettersTxt[l].draw()

		if self.allowInput:
			self.searchQuery.draw()
			if len(self.actualInput) < len(self.defaultSpelling):
				self.searchIBeam.draw()

		self.flash.surface.set_alpha(suff_lerp(self.flash.surface.get_alpha(), 0, 1 / FPS * 6))
		self.flash.draw()

	def string_padding(self, strin):
		leString = strin
		for i in range(max(0, len(self.defaultSpelling) - len(strin))):
			if self.defaultSpelling[i + len(strin)].isalpha():
				leString += '_'
			else:
				leString += self.defaultSpelling[i + len(strin)]
		return leString


	def update_letter_list(self, chars:str, word:str):
		self.correctLetters = []
		tempCorrLetters = []
		for i in range(min(len(chars), len(word))):
			if chars[i] == word[i]:
				if [word[i], i] not in self.correctLetters: # Runs this first
					self.correctLetters.append([word[i], i])
					tempCorrLetters.append(word[i])
			elif chars[i] in word: # So that this won't run if word is correct
				if tempCorrLetters.count(chars[i]) < word.count(chars[i]):
					if chars[i] not in self.misplacedLetters:
						self.misplacedLetters.append(chars[i])
			else:
				if chars[i] not in self.wrongLetters:
					self.wrongLetters.append(chars[i])
		self.correctLettersTxt.clear()
		self.misplacedLettersTxt.clear()
		self.wrongLettersTxt.clear()
		for letter in self.correctLetters:
			leTxt = SuffText(self.searchQuery.x + letter[1] * self.searchQuery.size * FONT_WIDTH_RATIO,
							 self.searchQuery.y, 1, letter[0], self.searchQuery.size, (0, 192, 0))
			leTxt.set_alpha(64)
			self.correctLettersTxt.append(leTxt)
		for letter in self.misplacedLetters:
			leTxt = SuffText(0, self.searchQuery.y, 1, letter, self.searchQuery.size, (192, 192, 0))
			leTxt.set_alpha(128)
			self.misplacedLettersTxt.append(leTxt)
		for letter in self.wrongLetters:
			leTxt = SuffText(0, SCREENSIZE[1] - self.searchQuery.size, 1, letter, self.searchQuery.size, (128, 0, 0))
			self.wrongLettersTxt.append(leTxt)
	def just_die(self):
		self.curScore = int(self.curScore * (1 - self.scorePenalty))
		if curSave.fetch('quiz_highscore') is None:
			curSave['quiz_highscore'] = self.curScore
		elif self.curScore > curSave.fetch('quiz_highscore'):
			curSave['quiz_highscore'] = self.curScore
			QuizGameOverState.highscore = True
		else:
			QuizGameOverState.highscore = False
		curSave.flush('save')

		QuizGameOverState.curScore = self.curScore
		change_state('quiz_game_over')
		pygame.mixer.Sound(get_asset_path('sounds/quiz_die.ogg')).play()
	def check_answer(self):
		global dialogueBox
		if dialogueBox.displayed_text != dialogueBox.text:
			dialogueBox.displayed_text = dialogueBox.text
			dialogueBox.box_text.set_text(dialogueBox.displayed_text)
			return False
		self.attempts += 1
		if remove_hyphens_by_setting(self.actualInput.lower()) == remove_hyphens_by_setting(self.defaultSpelling.lower()):
			self.correctLettersTxt = []
			self.misplacedLettersTxt = []
			self.wrongLettersTxt = []
			dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 - 200),
									  choice(self.CCC_HAPPY_LINES), 16, 'up', 1, self.reset)
			if self.lives < self.maxLives and self.attempts <= 1:  # Limit tries
				self.lives += 1  # Extra life for first-guesses
				self.add_heart()
			self.curScore += 1
			CCC.change_expression(choice(self.CCC_HAPPY_EXPRESSIONS))
			self.countdown = False
			self.allowInput = False
			return True
		else:
			prevCorrectLetters = self.correctLetters
			prevMisplacedLetters = self.misplacedLetters
			self.update_letter_list(self.actualInput.lower().strip(), self.defaultSpelling)
			UI_INVALID_SOUND.play()
			self.timeLeft -= (self.baseTimeLimit - 1) * self.timePenalty
		self.actualInput = ''
		self.searchQuery.set_text(self.string_padding(self.actualInput))
		return False
	def handle_event(self, event):
		if event.type == pygame.QUIT:
			self.just_die()
			return # If you try to quit, CCC will smite you immediately.
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.just_die()
				return # If you try to press escape, CCC will smite you immediately.
			elif event.key == pygame.K_BACKSPACE:
				self.actualInput = self.actualInput[:-1]
				self.searchQuery.set_text(self.string_padding(self.actualInput))
				UI_TEXT_ERASE_SOUND.play()
			elif event.key == pygame.K_RETURN:
				if self.allowInput:
					self.check_answer()
			elif len(self.actualInput) < len(self.defaultSpelling):
				self.actualInput += event.unicode
				self.searchQuery.set_text(self.string_padding(self.actualInput))
				UI_TEXT_TYPE_SOUND.play()
			self.searchQuery.x = (SCREENSIZE[0] - self.searchQuery.get_width()) / 2
			self.searchIBeam.x = self.searchQuery.x + len(self.actualInput) * self.searchIBeam.get_width() # Adjust I-Beam position

class QuizGameOverState(SuffState):
	curScore = 0
	highscore = True

	def __init__(self):
		pygame.mixer.music.stop()
		super().__init__(False)
	def post_load(self):
		CCC.angle = 0
		CCC.x, CCC.y = (SCREENSIZE[0] - CCC.head.surface.get_width()) / 2, 100
		self.flash = SuffSprite(0, 0)
		self.flash.rect = pygame.draw.rect(self.flash.surface, (255, 0, 0), (0, 0, SCREENSIZE[0], SCREENSIZE[1]))
		self.flash.rect = self.flash.surface.get_rect()
		self.flash.surface.set_alpha(255)

		self.hand = SuffSprite(540, 0, 'quiz/hand')
		self.hand.surface.set_alpha(255)
		super().post_load()
		CCC.change_expression('horror')
		infoText.set_text('')

		self.tick = 0
		self.grabbing = True
		self.allowQuit = False
	def update(self):
		super().update()
		if self.grabbing:
			self.tick += 1 / FPS
			self.hand.surface2 = pygame.transform.scale(self.hand.surface,
														(600 * pow(self.tick, 4), 530 * pow(self.tick, 4)))
			CCC.draw()
			if self.tick > 1.6 and self.grabbing:
				self.grabbing = False
		else:
			if not self.allowQuit:
				self.allowQuit = True
				self.curScoreTxt = SuffText(0, 100, 16, f'Your Score: {self.curScore}', 64, (255, 255, 255))
				self.curScoreTxt.x = (SCREENSIZE[0] - self.curScoreTxt.get_width()) / 2

				highscore = curSave.fetch('quiz_highscore')
				self.highscoreTxt = SuffText(0, self.curScoreTxt.y + 300, 16, f'Highscore: {highscore}', 64,
											 (255, 255, 128))
				self.highscoreTxt.x = (SCREENSIZE[0] - self.highscoreTxt.get_width()) / 2

				self.newHighscoreTxt = SuffText(0, self.highscoreTxt.y - 32, 16, 'NEW HIGHSCORE!', 32,
												(255, 255, 0))
				self.newHighscoreTxt.x = (SCREENSIZE[0] - self.newHighscoreTxt.get_width()) / 2
				self.newHighscoreTxt.set_alpha(128 if self.highscore else 0)

				self.exitTxt = SuffText(0, 0, 64, 'Click anywhere to exit', 32,
										(255, 255, 255))
				self.exitTxt.x = (SCREENSIZE[0] - self.exitTxt.get_width()) / 2
				self.exitTxt.y = SCREENSIZE[1] - self.exitTxt.get_height() - 16
			self.curScoreTxt.draw()
			self.highscoreTxt.draw()
			self.newHighscoreTxt.y = self.highscoreTxt.y - 32 + abs(sin(curTime / 2)) * -20
			self.newHighscoreTxt.draw()
			self.exitTxt.draw()
		self.flash.surface.set_alpha(suff_lerp(self.flash.surface.get_alpha(), 0, 1 / FPS))
		self.flash.draw()

		self.hand.rect2 = self.hand.surface2.get_rect()
		self.hand.x = 800 - self.hand.rect2.width / 1.6
		self.hand.y = 300 - self.hand.rect2.height / 1.8
		if self.allowQuit:
			self.hand.surface2.set_alpha(suff_lerp(self.hand.surface2.get_alpha(), 0, 1 / FPS))
		self.hand.draw(self.hand.surface2, self.hand.rect2)
	def handle_event(self, event):
		# No quitting
		if self.allowQuit:
			if (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)):
				pygame.mixer.music.load(get_asset_path('music/main_loop.ogg'))
				pygame.mixer.music.play(-1, 0, randint(4000, 8000))
				change_state('main_menu')
			super().handle_event(event)
class CreditsState(SuffState):
	def __init__(self):
		super().__init__()
	def post_load(self):
		CREDITS = [ # Credits are hard-coded to ensure no one maliciously changes anything
			["PROGRAMMING", "default", 96], # Text, Font, Font Size
			["Nick T. (Sufferneer)", "default", 48],
			["", "default", 32],
			["DICTIONARY", "default", 96],
			["Definitions (Most) - New Senior Secondary Mastering Biology (Third Edition) - Oxford University Press", "default", 32],
			["Word CSV - Deepseek", "default", 48],
			["Chinese Translations - An English-Chinese Glossary of Terms Commonly Used in the Teaching of Biology in Secondary Schools - Education Bureau", "default", 32],
			["Dictionary information may not be 100% compliant with Biology DSE.", "default", 16],
			["", "default", 32],
			["GRAPHICS", "default", 96],
			["Credits Button Background - Ministry of Health (Brazil)", "default", 32],
			["Nick T. (Sufferneer)", "default", 48],
			["All sprites, drawings and art are either self-made or used under the Creative Commons Attribution 4.0 International License. No copyright infringement is intentionally made.",
			 "default", 16],
			["", "default", 32],
			["MUSIC", "default", 96],
			["That's CCC! - Nick T. (Sufferneer)", "default", 48],
			["Artistic Expression - Kawai Sprite", "default", 48],
			["Megalo Strikes Back - Toby Fox", "default", 48],
			["All music is either self-made or used under the Creative Commons Attribution-ShareAlike 4.0 License. No copyright infringement is intentionally made.", "default", 16],
			["", "default", 32],
			["TYPEFACES", "default", 96],
			["Suffirat Mono - Nick T. (Sufferneer)", "default", 48],
			["JasonHandwriting1 清松手寫體1 - Jason Yu Ching Sung 游清松", "zh", 32],
			["All typefaces are either self-made or used under the SIL Open Font License.", "default", 16],
			["", "default", 32],
			["SPECIAL THANKS", "default", 96],
			["YellowAfterlife", "default", 32],
			["Miss Chan", "default", 32],
			["My Biology Teacher", "default", 32],
			["Jerry", "default", 32],
			["Dis Thing Dat Thing is made by Nick T. (Sufferneer).", "default", 16],
			["All characters and other entities appearing in this work are fictitious. Any resemblance to real persons, dead or alive, or other real-life entities, past or present, is purely coincidental.", "default", 16],
			["AI Disclaimer: Although AI assistance is used for data organization, this program does NOT contain any media created by generative artificial intelligence.", "default", 16]
		]
		super().post_load()
		self.textGroup = []

		prevHeight = 32
		for str in CREDITS:
			wordTitle = SuffText(32, prevHeight, int(SCREENSIZE[0] / str[2]), str[0], str[2],
								 (255, 255, 255), str[1])
			self.textGroup.append(wordTitle)
			prevHeight += wordTitle.get_height() + 16

		self.scrollAmount = 0
		self.txtYOrigin = []
		self.txtYOriginalOrigin = []
		for i in range(len(self.textGroup)):
			self.txtYOriginalOrigin.append(self.textGroup[i].y)
			self.txtYOrigin.append(self.textGroup[i].y)
		self.maxScroll = min(-ceil((max(self.txtYOriginalOrigin) + 64 - SCREENSIZE[1]) / 64), 0)

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')
	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('main_menu')
	def update(self):
		state_functions()

		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
		CCC.draw()
		self.exitButton.draw()
		for i in range(len(self.textGroup)):
			self.textGroup[i].draw()
		for i in range(len(self.textGroup)):
			self.textGroup[i].y = suff_lerp(self.textGroup[i].y, self.txtYOrigin[i], 1 / FPS * 6)
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()
		if event.type == pygame.MOUSEWHEEL:
			self.scrollAmount += event.y
			if self.scrollAmount > 0:
				self.scrollAmount = 0
			if self.scrollAmount < self.maxScroll:
				self.scrollAmount = self.maxScroll
			for i in range(len(self.textGroup)):
				self.txtYOrigin[i] = self.txtYOriginalOrigin[i] + self.scrollAmount * 64

class InfoState(SuffState):
	def __init__(self):
		super().__init__()
	def post_load(self):
		CREDITS_FILE = open('manual.txt')
		CREDITS = CREDITS_FILE.read().split('\n')
		CREDITS_FILE.close()
		super().post_load()
		self.textGroup = []

		prevHeight = 32
		for str in CREDITS:
			wordSize = 96 if str.isupper() else 32
			wordTitle = SuffText(32, prevHeight, int(SCREENSIZE[0] / wordSize), str, wordSize,
								 (255, 255, 255))
			self.textGroup.append(wordTitle)
			prevHeight += wordTitle.get_height() + wordTitle.size // 2

		self.scrollAmount = 0
		self.txtYOrigin = []
		self.txtYOriginalOrigin = []
		for i in range(len(self.textGroup)):
			self.txtYOriginalOrigin.append(self.textGroup[i].y)
			self.txtYOrigin.append(self.textGroup[i].y)
		self.maxScroll = min(-ceil((max(self.txtYOriginalOrigin) + 128 - SCREENSIZE[1]) / 64), 0)

		self.exitButton = SuffButton((SCREENSIZE[0] - 80, 8), (72, 72), self.back_to_main_menu,
									 'exit')
	def back_to_main_menu(self):
		UI_MENU_EXIT_SOUND.play()
		change_state('main_menu')
	def update(self):
		state_functions()

		CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
		CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
		CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
		CCC.draw()
		self.exitButton.draw()
		for i in range(len(self.textGroup)):
			self.textGroup[i].draw()
		for i in range(len(self.textGroup)):
			self.textGroup[i].y = suff_lerp(self.textGroup[i].y, self.txtYOrigin[i], 1 / FPS * 6)
	def handle_event(self, event):
		super().handle_event(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.back_to_main_menu()
		if event.type == pygame.MOUSEWHEEL:
			self.scrollAmount += event.y
			if self.scrollAmount > 0:
				self.scrollAmount = 0
			if self.scrollAmount < self.maxScroll:
				self.scrollAmount = self.maxScroll
			for i in range(len(self.textGroup)):
				self.txtYOrigin[i] = self.txtYOriginalOrigin[i] + self.scrollAmount * 64
states = { # Attempt to preload all screens by calling these classes
	'title': TitleState(),
	'main_menu': MainMenuState(),
	'quiz_selection': QuizSelectionState(),
	'quiz': QuizState(),
	'quiz_start': QuizStartState(),
	'quiz_game_over': QuizGameOverState(),
	'dictionary_search': DictionarySearchState(),
	'dictionary_bookmarks': DictionaryBookmarkState(),
	'dictionary_word': DictionaryWordState(),
	'credits': CreditsState(),
	'options': OptionsState(),
	'info': InfoState()
}

if __name__ == '__main__':
	pygame.mixer.music.set_volume(1)
	change_state('title')
	TitleState.TITLE_SOUND.set_volume(0.75)

	while True:
		for event in pygame.event.get():
			curState.handle_event(event)
		curState.update()
		curState.update_post()