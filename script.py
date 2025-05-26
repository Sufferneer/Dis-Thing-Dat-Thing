# ! DISCLAIMER !
# ! In many instances of the code, instances of someone in the name of 'Suff' can be found.
# ! Before you scream plagiarism, please note that 'Suff' is a pseudonym.
# ! I am usually called 'Suff' within my peers, so although it may sound weird,
# ! This algorithm is 100% self-made made only with the assist of PyGame documentations and tutorials.

import json
import os
import sys
import pygame
import math
import random
clock = pygame.time.Clock()
music = pygame.mixer.music
curTime = pygame.time.get_ticks()
FPS = 60 # ! I won't recommend on touching this one.
SCREENSIZE = (1280, 720)
FONT_WIDTH_RATIO = 0.5625 # Because the font size does not equal to a character's width, this value is multiplied by the
                          # font size of a text to get its character width

pygame.init()
pygame.display.set_caption('Dis Sheet Dat Sheet - With CCC')
screen = pygame.display.set_mode(SCREENSIZE)
mousePos = pygame.mouse.get_pos() # Mouse position variable that updates every tick.
DIALOGUE_SILENT_CHARS = [' ', ',', "'", '"', '.', '!', '?', '(', ')'] # These characters do NOT play the dialogue sound
DIALOGUE_PAUSE_CHARS = [',', ';', ':', '.', '!', '?'] # These characters delay the dialogue
pygame.mixer.music.set_volume(0)

def get_asset_path(path):
    # Simple function that returns the relative path of the assets.
    # I just don't want to type that a hundred times every time I want to get assets.
    return os.path.abspath(f'assets/{path}')
def suff_lerp(a, b, t, e = 1):
    # This function interpolates a numeric value to another numeric value based on the "percentage" given.
    # e = exponent of the function, so the interp won't be linear.
    # You will often see this in assigning position values of sprites for a smooth transition effect.
    return a + (b - a) * math.pow(t, e)
def separate_string(text, max_char = 16):
    # Makes a string into a list of strings that finds within a set width of characters.
    # "German love, festival. I am quite skeptical" with `max_char = 10` turns to ["German", "love,", "festival.",
    #                                                                              "I am quite", "skeptical"]
    # When rendered, it will be rendered like this:
    #  ____________
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
    return list(dict.fromkeys(leList))

pygame.display.set_icon(pygame.image.load(get_asset_path('images/icon.png')))
# CONSTANTS FOR SOUNDS
buttonHoverSound = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
buttonPressSound = pygame.mixer.Sound(get_asset_path('sounds/ui/click.ogg'))
textTypeSound = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
textEraseSound = pygame.mixer.Sound(get_asset_path('sounds/ui/release.ogg'))
menuExitSound = pygame.mixer.Sound(get_asset_path('sounds/ui/toggle_off.ogg'))

dialogueSound = pygame.mixer.Sound(get_asset_path('sounds/ui/dialogue.ogg'))
invalidSound = pygame.mixer.Sound(get_asset_path('sounds/ui/invalid.ogg'))

# CUSTOM OBJECTS THAT MAKE SPRITE/TEXT CREATION MORE CONVENIENT #
class SuffSprite(pygame.sprite.Sprite): # Parent class. Custom sprites with its surface and rectangle being stored as sub-variables.
    """
    Creates a configurable PyGame sprite.

    :param tuple pos: Position of the sprite.
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
        self.surface = pygame.image.load(get_asset_path(imagePath)).convert_alpha()
        self.rect = self.surface.get_rect()
    def draw(self):
        screen.blit(self.surface, (self.x, self.y), self.rect)

class SuffText(list): # Parent class. Yes, I know. It's actually a list, but it needs to be for multi-line support
    """
    Creates a configurable PyGame text sprite with multi-line support.

    :param tuple pos: Position of the text
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
        return len(self) * self.size
    def get_width(self):
        return max(len(item[2]) for item in self) * self.size * FONT_WIDTH_RATIO
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
    :param int text_hover_size: The size of the button text when button is hovered.
    :param tuple text_color: The color of the button text.
    """
    def __init__(self, pos, size, function, base_texture = '', text = '', hover_function = None, text_size = 32, text_hover_size = None, text_color = (255, 255, 255)):
        pygame.sprite.Group.__init__(self)
        self.pos = pos
        self.hovered = False
        self.clicked = False
        self.size = size
        self.text = text
        self.hover_function = hover_function
        self.function = function
        self.base_texture = base_texture
        self.text_color = text_color
        self.text_size = text_size
        if text_hover_size is not None:
            self.text_hover_size = text_hover_size
        else:
            self.text_hover_size = self.text_size
        self.base = SuffSprite(pos[0], pos[1], f'images/buttons/{base_texture}.png')
        self.base.surface.set_alpha(128)
        self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))
        self.button_text = SuffText(pos[0] + text_size / 2, pos[1] + size[1] / 4, size[0] // (text_hover_size // 2), self.text, text_size, (255, 255, 255))
    def draw(self):
        self.base.draw()
        self.button_text.draw()
        if self.pos[0] + self.size[0] >= mousePos[0] >= self.pos[0] and self.pos[1] + self.size[1] >= mousePos[1] >= \
                self.pos[1]:
            if not self.hovered:
                if self.hover_function is not None: self.hover_function()
                self.hovered = True
            self.button_text.set_size(int(suff_lerp(self.button_text.size, self.text_hover_size, 1 / FPS * 6)))
            if os.path.exists(get_asset_path(f'images/buttons/{self.base_texture}_highlighted.png')):
                self.base.surface = pygame.image.load(
                    get_asset_path(f'images/buttons/{self.base_texture}_highlighted.png')).convert_alpha()
                self.base.surface.set_alpha(128)
                self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.function()
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
        else:
            self.button_text.set_size(int(suff_lerp(self.button_text.size, self.text_size, 1 / FPS * 6)))
            if self.hovered:
                self.hovered = False
                if os.path.exists(get_asset_path(f'images/buttons/{self.base_texture}_highlighted.png')):
                    self.base.surface = pygame.image.load(
                        get_asset_path(f'images/buttons/{self.base_texture}.png')).convert_alpha()
                    self.base.surface.set_alpha(128)
                    self.base.surface = pygame.transform.scale(self.base.surface, (self.size[0], self.size[1]))

# OBJECTS THAT ARE BUILT ON THE ABOVE CUSTOM OBJECTS #
# They contain special code that is personalized for them #
class Dust(SuffSprite): # Ambient dust particles
    def __init__(self, x, y):
        SuffSprite.__init__(self, x, y, '')
        self.x = x
        self.y = y
        self.size = random.randint(4, 8)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        pygame.draw.rect(self.surface, (255, 255, 255), self.rect)
        self.surface.set_alpha(int(random.random() * 255))
        self.flitter_torque = random.random() * 5 + self.size
        self.flitter_speed = (random.random() * 0.5 - 0.5) * 2 / self.flitter_torque
        self.real_x = x
        self.real_y = y
    def draw(self):
        self.real_x, self.real_y = suff_lerp(self.real_x, self.x, 1 / FPS * 6), suff_lerp(self.real_y, self.y, 1 / FPS * 6)
        offsetX, offsetY = math.sin(curTime * (60 / FPS) * self.flitter_speed) * self.flitter_torque, math.cos(curTime * (60 / FPS) * self.flitter_speed) * self.flitter_torque
        screen.blit(self.surface, (self.real_x + offsetX * self.size, self.real_y + offsetY * self.size), self.rect)
class CCCSprite(pygame.sprite.Group): # The sprite of the game master capable of speech
    """
    Summon the almighty biology teacher Mr. Triple C into the algorithm.

    :param tuple pos: The position of Mr. Triple C.
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
        self.head = SuffSprite(self.x, self.y, 'images/ccc/neutral_head.png')
        self.mouth = SuffSprite(self.x, self.y, 'images/ccc/neutral_mouth.png')
    def change_expression(self, expression):
        self.head.load_graphic(f'images/ccc/{expression}_head.png')
        self.mouth.load_graphic(f'images/ccc/{expression}_mouth.png')
    def draw(self):
        if self.talk_tick < math.pi * 3:
            self.talk_tick += 1 / FPS * 30
        talk_coef = math.sin(self.talk_tick) / self.talk_tick
        w, h = self.head.surface.get_size()
        head_surface2 = pygame.transform.rotate(self.head.surface, self.angle + self.talk_offset * talk_coef)
        mouth_surface2 = pygame.transform.rotate(self.mouth.surface, self.angle + self.talk_offset * talk_coef)
        img2 = head_surface2.get_rect()
        screen.blit(head_surface2, (self.x - (img2.width - self.head.rect.width) / 2,
                                    self.y - (img2.height - self.head.rect.height) / 2 - talk_coef * 0.75 * 48 * self.talk_force), img2)
        screen.blit(mouth_surface2, (self.x - (img2.width - self.mouth.rect.width) / 2,
                                    self.y - (img2.height - self.mouth.rect.height) / 2 + talk_coef * 0.25 * 48 * self.talk_force), img2)
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
        self.tick:float = 0
        self.fade_time:float = fade_time
        self.fade_function = fade_function
        self.fade_function_called = False
        self.tip = SuffSprite(pos[0], pos[1], f'images/dialogue/dialogue_box_tip_{style}.png')
        width, height = max_char * 32 * FONT_WIDTH_RATIO + self.padding * 2, 32 * len(separate_string(self.text, self.max_char)) + self.padding * 2
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
        self.box_text = SuffText(self.box.x + self.padding, self.box.y + self.padding, max_char, '', 32, (0, 0, 0), font)
    def draw(self):
        if (self.fade_time != -1 and self.tick < self.fade_time + 1) or (self.fade_time == -1 and self.tick < 2):
            self.tick += 1 / FPS
        if self.displayed_text != self.text:
            if self.tick >= (self.delay if self.text[self.cur_letter - 1] not in DIALOGUE_PAUSE_CHARS else self.delay * 4):
                if self.text[self.cur_letter] not in DIALOGUE_SILENT_CHARS:
                    pygame.mixer.Sound.play(dialogueSound)
                    if self.cur_letter % 3 == 0 or self.delay >= 0.05:
                        CCC.talk_tick = 0
                        CCC.talk_force = random.random() * 0.5 + 0.5
                        CCC.talk_offset = random.randint(-10, 10)
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
class JeffreyWong(SuffSprite):
    def __init__(self, x, y):
        super().__init__(x, y, f'images/jeff/{random.randint(1, 3)}.png')
        self.surface.set_alpha(random.randint(128, 192))
        self.rect = self.surface.get_rect()
        self.flip_tick = random.random() * 30
        self.flipped = False
    def draw(self):
        self.flip_tick -= 1 / FPS * 4
        if self.flip_tick <= 0:
            self.flipped = False
            self.flip_tick = math.pi * 2 + random.random() * 30
        self.surface2 = pygame.transform.scale(self.surface, (160, 160))
        self.rect2 = self.surface2.get_rect()
        if self.flip_tick <= math.pi:
            if self.flip_tick <= math.pi / 2 and not self.flipped:
                self.load_graphic(f'images/jeff/{random.randint(1, 3)}.png')
                self.surface.set_alpha(random.randint(128, 192))
                self.flipped = True
            self.surface = pygame.transform.scale(self.surface, (160, 160))
            self.surface2 = pygame.transform.scale(self.surface, (abs(math.cos(self.flip_tick)) * 160, 160))
            self.rect2 = self.surface2.get_rect()
        screen.blit(self.surface2, (self.x - abs(math.cos(min(math.pi, self.flip_tick))) * 80 + 80, self.y), self.rect2)
fpsCounter = SuffText(0, 0, 16, '0 FPS', 16, (255, 255, 255))
background = SuffSprite(0, 0, 'images/background_1.png')
background.rect.size = (int(SCREENSIZE[0] * 1.5), int(SCREENSIZE[1] * 1.5))
background.surface = pygame.transform.scale(background.surface, (background.rect.width, background.rect.height))
infoText = SuffText(0, 0, 64, 'Dis Sheet Dat Sheet With CCC', 16,(255, 255, 255))
infoText.y = SCREENSIZE[1] - infoText.get_height()
dustGroup = []
for i in range(50):
    randomPos = (random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
    dustGroup.append(Dust(randomPos[0], randomPos[1]))
# the master of the dictionary application
CCC = CCCSprite(0, 0)
random_dialogue = [
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
    'You WILL be a fatso one day.',
    "Having a son is God's divine punishment of my sins."
]
# todo: tidy this button code
dialogueBox = DialogueBox((CCC.x + CCC.head.surface.get_width() * 1.1, 300), '', 20, 'right')
bgMode = 1
changeBG = True
def state_pre_functions(): # This function is called every time a menu initializes
    global dustGroup
    global CCC
    global dialogueBox
    for dust in dustGroup: # Dust scattering
        randomPos = (random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
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
    background.x = (SCREENSIZE[0] - background.surface.get_width()) / 2 + math.sin(curTime / 120) * 64
    background.y = (SCREENSIZE[1] - background.surface.get_height()) / 2 + math.cos(curTime / 120) * 36
    if round(math.pow(math.cos(curTime / 30), 2)) == 0 and changeBG == True:
        changeBG = False
        bgMode += 1
        if bgMode > 2: bgMode = 1
        background.load_graphic(f'images/background_{bgMode}.png')
        background.rect.size = (int(SCREENSIZE[0] * 1.5), int(SCREENSIZE[1] * 1.5))
        background.surface = pygame.transform.scale(background.surface, (background.rect.width, background.rect.height))
    if round(math.pow(math.cos(curTime / 30), 2)) == 1 and changeBG == False:
        changeBG = True
    background.surface.set_alpha(int((math.pow(math.cos(curTime / 30), 2)) * 255))
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
    def __init__(self, draw_bg = True): # This is called when the state starts to be loaded. Used to load/fetch data from the `words/` folder
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

class MainMenuState(SuffState):
    def __init__(self):
        super().__init__()
        pygame.mixer.music.stop()
    def post_load(self):
        super().post_load()
        def dict_hover():
            global CCC
            CCC.change_expression('happy')
            buttonHoverSound.play()
            global dialogueBox
            dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + 100, SCREENSIZE[1] / 2),
                                      'Learn some vocabulary for your brain library.', 20, 'right')
        def dict():
            buttonPressSound.play()
            change_state('dictionary_search')
        def quiz_hover():
            global CCC
            CCC.change_expression('smug')
            buttonHoverSound.play()
            global dialogueBox
            dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2), 'Get mentally tortured while I test your knowledge.', 20, 'left')
        def quiz():
            buttonPressSound.play()
            if os.path.exists('save.txt'):
                change_state('quiz')
            else:
                change_state('quiz_start')
        def flashcards_hover():
            global CCC
            CCC.change_expression('neutral')
            buttonHoverSound.play()
            global dialogueBox
            dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + 100, SCREENSIZE[1] / 2),
                              'Quickly memorize some words using a traditional Asian method.', 20, 'right')
        def flashcards():
            CCC.x += 5
        def credits_hover():
            global CCC
            CCC.change_expression('furious')
            buttonHoverSound.play()
            global dialogueBox
            dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2), 'Check out the sole idiot that made this garbage possible.', 20, 'left')
        def credits():
            CCC.x += 5
        self.dictionaryButton = SuffButton((10, 10), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15), dict,
                                           'dictionary',
                                           'Dictionary Mode', dict_hover, 48, 112)
        self.quizButton = SuffButton((SCREENSIZE[0] / 2 + 5, 10), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15),
                                     quiz,
                                     'quiz', 'Quiz Mode', quiz_hover, 48, 112)
        self.flashcardsButton = SuffButton((10, SCREENSIZE[1] / 2 + 5),
                                           (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15),
                                           flashcards, 'flashcards', 'Flashcards', flashcards_hover, 48, 112)
        self.creditsButton = SuffButton((SCREENSIZE[0] / 2 + 5, SCREENSIZE[1] / 2 + 5),
                                        (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15), credits, 'credits', 'Credits',
                                        credits_hover, 48, 112)
    def update(self):
        super().update()
        CCC.x = suff_lerp(CCC.x, (SCREENSIZE[0] - CCC.head.surface.get_width()) / 2, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.surface.get_height()) / 2, 1 / FPS * 6)
        distances = (CCC.x + CCC.head.surface.get_width() / 2 - mousePos[0],
                     CCC.y + CCC.head.surface.get_height() / 2 - mousePos[1])
        CCC.angle = distances[0] / SCREENSIZE[0] * 8 * -45 * distances[1] / SCREENSIZE[1] / 2

        self.dictionaryButton.draw()
        self.quizButton.draw()
        self.flashcardsButton.draw()
        self.creditsButton.draw()
        CCC.draw()
        dialogueBox.draw()
    def handle_event(self, event):
        super().handle_event(event)
        global dialogueBox
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                CCC.change_expression(random.choice(['angry', 'furious', 'smug', 'evil', 'house', 'horror']))
                dialogueBox = DialogueBox((CCC.x + CCC.head.surface.get_width() + 32, 300),
                                          random.choice(random_dialogue), 20, 'right')

curState = None

def change_state(state):
    global curState
    curState = states[state]
    states[state].__init__()

curWordData = {
    "word": [
        "excretion",
        "excrete"
    ],
    "alt_spellings": [],
    "word_class": "noun",
    "forms": {},
    "plural": [],
    "definition": "An process of which an organism removes metabolic wastes",
    "translation": [
        "\u6392\u6cc4\u4f5c\u7528"
    ]
}

class DictionarySearchState(SuffState):
    def post_load(self):
        super().post_load()
        global dialogueBox
        dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
                                  'Type a word in the field and press [ENTER].', 20, 'down', -1)
        self.searchTitle = SuffText(128, 32 - 64, 16, 'Search For Word', 80, (255, 255, 255))
        self.searchTitle.set_alpha(0)
        self.searchQuery = SuffText(128, 192 + 80 + 64, 25, '', 48, (255, 255, 255))
        self.searchIBeam = SuffText(128, 192 + 80 + 64, 1, '|', 48, (255, 255, 255))
        self.wordList = []

    def bubble_sort_word(self, letter):
        arrFile = open(f'words/{letter}.json', 'r')
        arr = json.load(arrFile)
        arrFile.close()
        for i in range(len(arr)):
            for j in range(len(arr) - 1):
                if arr[j]['word'][0] > arr[j + 1]['word'][0]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        arrFileWrite = open(f'words/{letter}.json', 'w')
        arrFileWrite.write(json.dumps(arr, indent=4))
        arrFileWrite.close()

    def binary_search_word(self, x):
        global wordList
        low = 0
        high = len(wordList) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if x in wordList[mid]['word']:
                return wordList[mid]
            elif (wordList[mid]['word'][0] < x):
                low = mid + 1
            else:
                high = mid - 1
        return None

    def search_for_word(self, word):
        global wordList
        if not os.path.exists(f'words/{word[0]}.json'):
            return None
        self.bubble_sort_word(word[0])
        wordFile = open(f'words/{word[0]}.json', 'r')
        wordList = json.load(wordFile)
        wordFile.close()
        wordData = self.binary_search_word(word)
        return wordData

    def update(self):
        super().update()
        global dialogueBox

        CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] / 2 + (SCREENSIZE[0] / 2 - CCC.head.rect.width) / 2, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.rect.height) / 2, 1 / FPS * 6)
        CCC.angle = suff_lerp(CCC.angle, 0, 1 / FPS * 6)
        self.searchIBeam.x = self.searchQuery.x + (
                    len(self.searchQuery.text) % self.searchQuery.width) * self.searchQuery.size * FONT_WIDTH_RATIO
        self.searchTitle.y = suff_lerp(self.searchTitle.y, 192, 1 / FPS * 6)
        self.searchTitle.set_alpha(suff_lerp(self.searchTitle.alpha, 255, 1 / FPS * 6))  # smooth fade-in animation

        CCC.draw()
        dialogueBox.draw()
        self.searchTitle.draw()
        self.searchQuery.draw()
        if len(
                self.searchQuery.text) < self.searchQuery.width: self.searchIBeam.draw()  # Prevent I-Beam from rendering when search field is full.

    def handle_event(self, event):
        super().handle_event(event)
        global dialogueBox
        global curState

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.searchQuery.text.isalpha():
                    w = self.search_for_word(
                        self.searchQuery.text.lower().strip())  # get word data from word folder (also
                    # removes leading/ending whitespaces and
                    # makes it lowercase)
                    if w:
                        buttonPressSound.play()
                        global curState
                        global curWordData
                        curWordData = w
                        curState = DictionaryWordState()
                    else:
                        invalidSound.play()
                        CCC.change_expression('angry')
                        dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
                                                  'I don\'t think that word exists in the biology curriculum.', 20,
                                                  'down', -1)
                else:
                    invalidSound.play()
                    CCC.change_expression('angry')
                    dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
                                              'I don\'t believe a human speaks like that.', 20, 'down', -1)
            elif event.key == pygame.K_BACKSPACE:
                self.searchQuery.set_text(self.searchQuery.text[0:len(self.searchQuery.text) - 1])
                textEraseSound.play()
            elif len(self.searchQuery.text) < self.searchQuery.width:
                self.searchQuery.set_text(self.searchQuery.text + event.unicode)
                textTypeSound.play()
            if event.key == pygame.K_ESCAPE:
                menuExitSound.play()
                curState = MainMenuState()

class DictionaryWordState(SuffState):
    def __init__(self):
        super().__init__()
    def post_load(self):
        global curWordData
        super().post_load()
        self.textGroup = []

        wordTitle = SuffText(32, 32, 32, curWordData['word'][0].upper(), 96,
                             (255, 255, 255))
        self.textGroup.append(wordTitle)
        wordClassTxtString = curWordData['word_class'] # part of speech
        if len(curWordData['plural']) > 0:
            wordClassTxtString += ', plural \'' + ', '.join(curWordData['plural']) + '\'' # plural form
        wordClassTxt = SuffText(32, wordTitle.y + wordTitle.get_height(), 32, wordClassTxtString, 32, (255, 255, 255))
        self.textGroup.append(wordClassTxt)
        wordAltTxt = SuffText(32, wordClassTxt.y + 32, 32, '', 32, (255, 255, 255))
        if len(curWordData['alt_spellings']) > 0:
            wordAltTxt.set_text('alt. ' + ', '.join(curWordData['alt_spellings']))
        self.textGroup.append(wordAltTxt)
        wordDefTxt = SuffText(32, wordAltTxt.y + 64, 48, curWordData['definition'], 32, (255, 255, 255))
        self.textGroup.append(wordDefTxt)
        wordTransDescTxt = SuffText(32, wordDefTxt.y + 32 + wordDefTxt.get_height(), 48,
                                    curWordData['word'][0][0].upper() + curWordData['word'][0][1:] + ' means ', 32,
                                    (255, 255, 255))
        self.textGroup.append(wordTransDescTxt)
        wordTransTxt = SuffText(wordTransDescTxt.x + wordTransDescTxt.get_width(), wordTransDescTxt.y, 48,
                                '；'.join(curWordData['translation']), 32, (255, 255, 255), 'zh')
        self.textGroup.append(wordTransTxt)
        tenses = ['present', 'continuous', 'past', 'perfect']
        prevHeight = 0
        for key in curWordData['forms'].keys():
            wordFormTitleTxt = SuffText(32, wordTransTxt.y + 64 + prevHeight, 48, key.upper(), 48, (255, 255, 255))
            self.textGroup.append(wordFormTitleTxt)
            prevHeight += 48
            for w in range(len(curWordData['forms'][key])):
                if key == 'verb':
                    wordTenseTxt = SuffText(32, wordFormTitleTxt.y + 58 + 32 * w, 48, tenses[w], 16, (255, 255, 255))
                wordFormTxt = SuffText(32 + (wordTenseTxt.get_width() + 16 if key == 'verb' else 0),
                                       wordFormTitleTxt.y + 48 + 32 * w, 48, curWordData['forms'][key][w], 32, (255, 255, 255))
                prevHeight += 32
                if key == 'verb': self.textGroup.append(wordTenseTxt)
                self.textGroup.append(wordFormTxt)
            prevHeight += 48

        self.scrollAmount = 0
        self.txtYOrigin = []
        self.txtYOriginalOrigin = []
        self.txtText = []
        for i in range(len(self.textGroup)):
            self.txtText.append(self.textGroup[i].text)
            self.textGroup[i].set_text('')
            self.txtYOriginalOrigin.append(self.textGroup[i].y)
            self.txtYOrigin.append(self.textGroup[i].y)
        self.maxScroll = min(-math.ceil((max(self.txtYOriginalOrigin) + 48 - SCREENSIZE[1]) / 64), 0)
        self.txtTypeTick = 0
        self.playAnim = 3
    def update(self):
        state_functions()

        CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
        CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
        CCC.draw()
        self.txtTypeTick += 1 / FPS
        playSound = False
        for i in range(len(self.textGroup)):
            if len(self.textGroup[i].text) < len(self.txtText[i]) and self.txtTypeTick > 0.025:
                if self.txtText[i][len(self.textGroup[i].text)] not in DIALOGUE_SILENT_CHARS: playSound = True
                self.textGroup[i].set_text(self.textGroup[i].text + self.txtText[i][len(self.textGroup[i].text)])
            self.textGroup[i].draw()
        if playSound:
            dialogueSound.play()
            self.playAnim += 1
            if self.playAnim > 3:
                CCC.talk_force = random.random() * 0.5 + 0.5
                CCC.talk_tick = 0
                CCC.talk_offset = random.randint(-10, 10)
                self.playAnim = 0
            self.txtTypeTick = 0
        for i in range(len(self.textGroup)):
            self.textGroup[i].y = suff_lerp(self.textGroup[i].y, self.txtYOrigin[i], 1 / FPS * 6)
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menuExitSound.play()
                global curState
                curState = DictionarySearchState()
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
        self.leQuizState = QuizState()  # preload the quiz state
        super().__init__(False)

    def post_load(self):
        self.index = 0
        # Dialogue, Expression, Beat Number, Dialogue Speed
        self.dialogue = [
            ["They don\'t call me Chief Executive Chow for nothin', kid.", 'neutral', 0, 0.03],
            ['I have ruined the futures of countless candidates.', 'happy', 8, 0.03],
            ["I'll give you a definition and three chances to answer my questions.", 'smug', 16, 0.03],
            ["And if you use all my chances...", 'evil', 24, 0.03],
            ["YOU DIE.", 'horror', 28, 0.05],
            ["", 'horror', 31, 0],
            ["", '', 32, 0]
        ]
        self.black = SuffSprite(0, 0)
        self.black.rect = pygame.draw.rect(self.black.surface, (0, 0, 0), (0, 0, SCREENSIZE[0], SCREENSIZE[1]))
        self.black.surface.set_alpha(0)
        pygame.mixer.music.load(get_asset_path('music/pre_quiz.ogg'))
        pygame.mixer.music.play()
        self.curBeat = 0
        super().post_load()

    def update(self):
        global dialogueBox
        self.curBeat = int((pygame.mixer.music.get_pos() + 50) / (60 / 144 * 1000)) # Current beat of the music. BPM is 144
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
                print(len(self.dialogue))
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                change_state('quiz')

class QuizState(SuffState):
    def __init__(self):
        self.leWordData = dict()
        self.allowInput = False
        self.derList = []
        for alp in [chr(i) for i in range(ord('a'), ord('z'))]:
            if os.path.exists(f'words/{alp}.json'):
                file = open(f'words/{alp}.json', 'r')
                leJson = json.load(file)
                file.close()
                for item in leJson:
                    self.derList.append(item)

        self.lives = 3
        self.cccExpressions = ['horror', 'demon', 'evil', 'smug', 'neutral'] # life based
        self.cccHappyExpressions = ['smug', 'happy', 'house']
        self.cccAngryExpressions = ['angry', 'furious']
        self.cccHappyLines = [
            'Very good.',
            'Quite good.',
            'Acceptable.'
        ]
        self.cccAngryLines = [
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
        self.searchQuery = SuffText(SCREENSIZE[0] / 2, 600, 25, '', 64, (255, 255, 255))
        self.searchIBeam = SuffText(SCREENSIZE[0] / 2, 600, 25, '|', 64, (255, 255, 255))
        self.reset()
        self.curBeat = 0
        self.jeffs = []
        self.jeff_width = math.ceil(SCREENSIZE[0] / 160)
        self.jeff_height = math.ceil(SCREENSIZE[1] / 160)
        for x in range(0, self.jeff_width + 1):  # Every Jeffrey Wong sprite is 80 x 80.
            for y in range(0, self.jeff_height):
                jeff = JeffreyWong(x * 160, y * 160 - 40)
                self.jeffs.append(jeff)
        self.bg = SuffSprite(0, 0, 'images/vibrio_cholerae.png')
        self.bg.surface = pygame.transform.scale(self.bg.surface, (SCREENSIZE[0], SCREENSIZE[1]))
        self.bg.rect = self.bg.surface.get_rect()
        self.dust = []
        for i in range(0, 50):
            red = Dust(random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
            self.dust.append(red)
        self.reds = []
        for i in range(1, 9):
            red = SuffSprite(0, SCREENSIZE[1] - SCREENSIZE[1] / 3 / 8 * i)
            red.rect = pygame.draw.rect(red.surface, (255, 0, 0), (0, 0, SCREENSIZE[0], SCREENSIZE[1] / 3 / 8 * i))
            red.surface.set_alpha(32)
            self.reds.append(red)
        self.flash = SuffSprite(0, 0)
        self.flash.rect = pygame.draw.rect(self.flash.surface, (255, 255, 255), (0, 0, SCREENSIZE[0], SCREENSIZE[1]))
        self.flash.surface.set_alpha(255)
        pygame.mixer.music.load(get_asset_path('music/quiz_loop.ogg'))
        pygame.mixer.music.play(-1)
    def reset(self):
        CCC.change_expression(self.cccExpressions[self.lives])
        global dialogueBox
        self.allowInput = True
        self.leWordData = random.choice(self.derList)
        ogDef = self.leWordData['definition']
        senDef = ogDef[0].lower() + ogDef[1:len(ogDef) - 1] + ogDef[len(ogDef) - 1].replace('.', '')
        leFont = 'default'
        if random.choice([True, False]):
            senDef = ' / '.join(self.leWordData['translation']) # 50% chance that it shows up the Chinese version
            leFont = 'zh'
        leDialogue = f'What is the {self.leWordData['word_class']} for {senDef}?'
        print(self.leWordData['word'])
        dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2),
                                  leDialogue, min(len(leDialogue), 50), 'down', -1, None, leFont) # Limits dialogue width by 50 chars

    def update(self):
        super().update()
        self.bg.draw()
        for i in range(len(self.jeffs)):
            self.jeffs[i].x -= 1 / FPS * 640
            if self.jeffs[i].x < -160:
                self.jeffs[i].x = SCREENSIZE[0] + 160 + self.jeffs[i].x
            self.jeffs[i].y = math.sin(self.curBeat * math.pi / 2 + (i // self.jeff_height) * math.pi / self.jeff_height) * 40 + i % self.jeff_height * 160 - 40
            self.jeffs[i].draw()
        for dust in self.dust:
            dust.x += math.sin(self.curBeat * math.pi / 2 * dust.flitter_speed * dust.flitter_torque) * dust.flitter_torque / 5
            dust.y -= 1 / FPS * 320
            if dust.real_y < -160:
                dust.y = SCREENSIZE[1]
                dust.real_y = SCREENSIZE[1]
            dust.draw()
        self.curBeat = (pygame.mixer.music.get_pos() + 10) / (60 / 144 * 1000) # BPM of music is 144
        CCC.angle = math.sin(self.curBeat * math.pi / 2) * -60 / (self.lives + 1)
        CCC.x = (SCREENSIZE[0] - CCC.head.rect.width) / 2 + math.sin(self.curBeat * math.pi / 2) * 500 / (self.lives + 1)
        CCC.y = 50 + math.sin(self.curBeat * math.pi) * 200 / (self.lives + 1)
        # Makes CCC shift around like a maniac
        CCC.draw()
        dialogueBox.draw()
        for i in range(len(self.reds)):
            self.reds[i].y = SCREENSIZE[1] - math.pow(math.sin(self.curBeat / 4 * math.pi + math.pi / 4), 2) * SCREENSIZE[1] / 3 / 8 * i
            self.reds[i].draw()
        self.searchQuery.draw()
        self.searchIBeam.draw()

        self.flash.surface.set_alpha(suff_lerp(self.flash.surface.get_alpha(), 0, 1 / FPS * 6))
        self.flash.draw()

    def look_for_chars_in_word(self, chars:str, words:list):
        containingLetters = []
        for word in range(len(words)):
            for char in chars:
                if char in words[word]:
                    containingLetters.append(char)
        return remove_duplicates(containingLetters)
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                change_state('main_menu')
                menuExitSound.play()
            elif event.key == pygame.K_BACKSPACE:
                self.searchQuery.set_text(self.searchQuery.text[:-1])
                textEraseSound.play()
            elif event.key == pygame.K_RETURN:
                global dialogueBox
                if self.allowInput:
                    containingChars = self.look_for_chars_in_word(self.searchQuery.text.lower().strip(), self.leWordData['word'])
                    if dialogueBox.displayed_text != dialogueBox.text:
                        dialogueBox.displayed_text = dialogueBox.text
                        dialogueBox.box_text.set_text(dialogueBox.displayed_text)
                        return
                    self.allowInput = False
                    if self.searchQuery.text.lower().strip() in self.leWordData['word']:
                        dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 - 200),
                                  random.choice(self.cccHappyLines), 16, 'up', 1, self.reset)
                        self.lives = clamp(self.lives + 1, 0, 4) # Limit tries
                        CCC.change_expression(random.choice(self.cccHappyExpressions))
                    elif len(containingChars) > 0:
                        CCC.change_expression('smug')
                        self.allowInput = True
                    else:
                        dialogueBox = DialogueBox((SCREENSIZE[0] / 2, SCREENSIZE[1] / 2 - 200),
                                                                random.choice(self.cccAngryLines), 16, 'up', 1, self.reset)
                        self.lives = clamp(self.lives - 1, 0, 4)
                        CCC.change_expression(random.choice(self.cccAngryExpressions))
                        invalidSound.play()
                    self.searchQuery.set_text('')
            else:
                self.searchQuery.set_text(self.searchQuery.text + event.unicode)
                textTypeSound.play()
            self.searchQuery.x = (SCREENSIZE[0] - self.searchQuery.get_width()) / 2
            self.searchIBeam.x = self.searchQuery.x + self.searchQuery.get_width()

states = {
    'main_menu': MainMenuState(),
    'quiz': QuizState(),
    'quiz_start': QuizStartState(),
    'dictionary_search': DictionarySearchState(),
    'dictionary_word': DictionaryWordState()
}
change_state('main_menu')
pygame.mixer.music.set_volume(1)

while True:
    for event in pygame.event.get():
        curState.handle_event(event)
    curState.update()
    curState.update_post()