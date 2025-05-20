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

# CONSTANTS FOR SOUNDS
buttonHoverSound = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
buttonPressSound = pygame.mixer.Sound(get_asset_path('sounds/ui/click.ogg'))
textTypeSound = pygame.mixer.Sound(get_asset_path('sounds/ui/hover.ogg'))
textEraseSound = pygame.mixer.Sound(get_asset_path('sounds/ui/release.ogg'))
menuExitSound = pygame.mixer.Sound(get_asset_path('sounds/ui/toggle_off.ogg'))

dialogueSound = pygame.mixer.Sound(get_asset_path('sounds/ui/dialogue.ogg'))
invalidSound = pygame.mixer.Sound(get_asset_path('sounds/ui/invalid.ogg'))

# CUSTOM OBJECTS THAT MAKE SPRITE/TEXT CREATION MORE CONVENIENT #
class SuffSprite(pygame.sprite.Sprite): # Custom sprites with its surface and rectangle being stored as sub-variables.
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

class SuffText(list): # Yes, I know. It's actually a list, but it needs to be for multi-line support
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
class SuffButton(pygame.sprite.Group):
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
    def __init__(self, pos, text, max_char = 10, style = 'up', fade_time = 1.5):
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
        self.tip = SuffSprite(pos[0], pos[1], f'images/dialogue/dialogue_box_tip_{style}.png')
        width, height = max_char * 32 * FONT_WIDTH_RATIO + self.padding * 2, 32 * len(separate_string(self.text, self.max_char)) + self.padding * 2
        if style == 'up':
            box_pos = (self.pos[0] - (width - self.tip.rect.width) / 2 - 20, self.pos[1] - height + 4)
            tip_pos = (self.pos[0] - 20, self.pos[1] - self.tip.rect.height)
        elif style == 'down':
            box_pos = (self.pos[0] - (width - self.tip.rect.width) / 2 - 20, self.pos[1] + self.tip.rect.height - 4)
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
        self.box_text = SuffText(self.box.x + self.padding, self.box.y + self.padding, max_char, '', 32)
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
    for dust in dustGroup: # Dust scattering
        randomPos = (random.randint(0, SCREENSIZE[0]), random.randint(0, SCREENSIZE[1]))
        dust.x = randomPos[0]
        dust.y = randomPos[1]
    CCC.change_expression('neutral') # Make CCC neutral every time he switches to menu
def state_functions(): # This function is called before every tick function in a menu
    global curTime
    global mousePos
    global background
    global dustGroup
    global bgMode
    global changeBG
    curTime = pygame.time.get_ticks() / FPS
    clock.tick(FPS)
    mousePos = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
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
    fpsCounter.set_text(str(int(clock.get_fps())) + ' FPS')
    fpsCounter.draw()
    infoText.draw()
    pygame.display.update()

def dictionary_word_menu(wordData):
    state_pre_functions()
    textGroup = []

    wordTitle = SuffText(len(wordData['word'][0]) * -96 * FONT_WIDTH_RATIO, 32, 32, wordData['word'][0].upper(), 96,
                         (255, 255, 255))
    wordTitle.set_alpha(0)
    textGroup.append(wordTitle)
    wordClassTxtString = wordData['word_class'] # part of speech
    if len(wordData['plural']) > 0:
        wordClassTxtString += ', plural \'' + ', '.join(wordData['plural']) + '\'' # plural form
    wordClassTxt = SuffText(32, wordTitle.y + wordTitle.get_height(), 32, wordClassTxtString, 32, (255, 255, 255))
    textGroup.append(wordClassTxt)
    wordAltTxt = SuffText(32, wordClassTxt.y + 32, 32, '', 32, (255, 255, 255))
    if len(wordData['alt_spellings']) > 0:
        wordAltTxt.set_text('alt. ' + ', '.join(wordData['alt_spellings']))
    textGroup.append(wordAltTxt)
    wordDefTxt = SuffText(32, wordAltTxt.y + 64, 48, wordData['definition'], 32, (255, 255, 255))
    textGroup.append(wordDefTxt)
    wordTransDescTxt = SuffText(32, wordDefTxt.y + 32 + wordDefTxt.get_height(), 48,
                                wordData['word'][0][0].upper() + wordData['word'][0][1:] + ' means ', 32,
                                (255, 255, 255))
    textGroup.append(wordTransDescTxt)
    wordTransTxt = SuffText(wordTransDescTxt.x + wordTransDescTxt.get_width(), wordTransDescTxt.y, 48,
                            '；'.join(wordData['translation']), 32, (255, 255, 255), 'zh')
    textGroup.append(wordTransTxt)
    tenses = ['present', 'continuous', 'past', 'perfect']
    prevHeight = 0
    for key in wordData['forms'].keys():
        wordFormTitleTxt = SuffText(32, wordTransTxt.y + 64 + prevHeight, 48, key.upper(), 48, (255, 255, 255))
        textGroup.append(wordFormTitleTxt)
        prevHeight += 48
        for w in range(len(wordData['forms'][key])):
            if key == 'verb':
                wordTenseTxt = SuffText(32, wordFormTitleTxt.y + 58 + 32 * w, 48, tenses[w], 16, (255, 255, 255))
            wordFormTxt = SuffText(32 + (wordTenseTxt.get_width() + 16 if key == 'verb' else 0),
                                   wordFormTitleTxt.y + 48 + 32 * w, 48, wordData['forms'][key][w], 32, (255, 255, 255))
            prevHeight += 32
            if key == 'verb': textGroup.append(wordTenseTxt)
            textGroup.append(wordFormTxt)
        prevHeight += 48

    scrollAmount = 0
    txtYOrigin = []
    txtYOriginalOrigin = []
    txtText = []
    for i in range(len(textGroup)):
        txtText.append(textGroup[i].text)
        textGroup[i].set_text('')
        txtYOriginalOrigin.append(textGroup[i].y)
        txtYOrigin.append(textGroup[i].y)
    maxScroll = min(-math.ceil((max(txtYOriginalOrigin) + 48 - SCREENSIZE[1]) / 64), 0)
    print(maxScroll)
    txtTypeTick = 0
    playAnim = 3
    while True:
        state_functions()
        wordTitle.x = suff_lerp(wordTitle.x, 32, 1 / FPS * 6)
        wordTitle.set_alpha(suff_lerp(wordTitle.alpha, 255, 1 / FPS * 6))

        CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] - (CCC.head.rect.width / 4) * 3, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, SCREENSIZE[1] - (CCC.head.rect.height / 4) * 3, 1 / FPS * 6)
        CCC.angle = suff_lerp(CCC.angle, 30, 1 / FPS * 6)
        CCC.draw()
        txtTypeTick += 1 / FPS
        playSound = False
        for i in range(len(textGroup)):
            if len(textGroup[i].text) < len(txtText[i]) and txtTypeTick > 0.025:
                if txtText[i][len(textGroup[i].text)] not in DIALOGUE_SILENT_CHARS: playSound = True
                textGroup[i].set_text(textGroup[i].text + txtText[i][len(textGroup[i].text)])
            textGroup[i].draw()
        if playSound:
            dialogueSound.play()
            playAnim += 1
            if playAnim > 3:
                CCC.talk_force = random.random() * 0.5 + 0.5
                CCC.talk_tick = 0
                CCC.talk_offset = random.randint(-10, 10)
                playAnim = 0
            txtTypeTick = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menuExitSound.play()
                    dictionary_menu()
            if event.type == pygame.MOUSEWHEEL:
                scrollAmount += event.y
                if scrollAmount > 0:
                    scrollAmount = 0
                if scrollAmount < maxScroll:
                    scrollAmount = maxScroll
                for i in range(len(textGroup)):
                    txtYOrigin[i] = txtYOriginalOrigin[i] + scrollAmount * 64
        for i in range(len(textGroup)):
            textGroup[i].y = suff_lerp(textGroup[i].y, txtYOrigin[i], 1 / FPS * 6)
        state_post_functions()
def bubble_sort_word(letter):
    arrFile = open(f'words/{letter}.json', 'r')
    arr = json.load(arrFile)
    arrFile.close()
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j]['word'][0] > arr[j + 1]['word'][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    arrFileWrite = open(f'words/{letter}.json', 'w')
    arrFileWrite.write(json.dumps(arr, indent = 4))
    arrFileWrite.close()
def dictionary_menu():
    state_pre_functions()
    global CCC
    global dialogueBox
    dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + SCREENSIZE[0] / 4, SCREENSIZE[1] / 2 + 180),
                              'Type a word in the field and press [ENTER].', 20, 'down', -1)
    searchTitle = SuffText(128, 32 - 64, 16, 'Search For Word', 80, (255, 255, 255))
    searchTitle.set_alpha(0)
    searchQuery = SuffText(128, 192 + 80 + 64, 25, '', 48, (255, 255, 255))
    searchIBeam = SuffText(128, 192 + 80 + 64, 1, '|', 48, (255, 255, 255))
    wordList = []

    def search_for_word(word):
        global wordList
        if not os.path.exists(f'words/{word[0]}.json'):
            return None
        bubble_sort_word(word[0])
        wordFile = open(f'words/{word[0]}.json', 'r')
        wordList = json.load(wordFile)
        wordFile.close()
        wordData = binary_search_word(word)
        return wordData
    def binary_search_word(x):
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
    while True:
        state_functions()

        CCC.x = suff_lerp(CCC.x, SCREENSIZE[0] / 2 + (SCREENSIZE[0] / 2 - CCC.head.rect.width) / 2, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.rect.height) / 2, 1 / FPS * 6)
        CCC.angle = suff_lerp(CCC.angle, 0, 1 / FPS * 6)
        CCC.draw()
        searchIBeam.x = searchQuery.x + (len(searchQuery.text) % searchQuery.width) * searchQuery.size * FONT_WIDTH_RATIO
        searchTitle.y = suff_lerp(searchTitle.y, 192, 1 / FPS * 6)
        searchTitle.set_alpha(suff_lerp(searchTitle.alpha, 255, 1 / FPS * 6)) # smooth fade-in animation
        dialogueBox.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if searchQuery.text.replace(' ', '').isalpha():
                        w = search_for_word(searchQuery.text.lower().strip()) # get word data from word folder (also
                                                                              # removes leading/ending whitespaces and
                                                                              # makes it lowercase)
                        if w:
                            buttonPressSound.play()
                            dictionary_word_menu(w)
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
                    searchQuery.set_text(searchQuery.text[0:len(searchQuery.text)-1])
                    textEraseSound.play()
                elif len(searchQuery.text) < searchQuery.width:
                    searchQuery.set_text(searchQuery.text + event.unicode)
                    textTypeSound.play()
                if event.key == pygame.K_ESCAPE:
                    menuExitSound.play()
                    main_menu()

        searchTitle.draw()
        searchQuery.draw()
        if len(searchQuery.text) < searchQuery.width: searchIBeam.draw() # Prevent I-Beam from rendering when search field is full.

        state_post_functions()
def main_menu():
    state_pre_functions()
    def dict_hover():
        global CCC
        CCC.change_expression('happy')
        buttonHoverSound.play()
        global dialogueBox
        dialogueBox = DialogueBox((SCREENSIZE[0] / 2 + 100, SCREENSIZE[1] / 2),
                          'Learn some vocabulary for your brain library.', 20, 'right')

    def dict():
        buttonPressSound.play()
        dictionary_menu()

    def quiz_hover():
        global CCC
        CCC.change_expression('smug')
        buttonHoverSound.play()
        global dialogueBox
        dialogueBox = DialogueBox((SCREENSIZE[0] / 2 - 100, SCREENSIZE[1] / 2), 'Get mentally tortured while I test your knowledge.', 20, 'left')

    def quiz():
        CCC.x += 5

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

    dictionaryButton = SuffButton((10, 10), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15), dict, 'dictionary',
                                   'Dictionary Mode', dict_hover, 48, 112)
    quizButton = SuffButton((SCREENSIZE[0] / 2 + 5, 10), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15), quiz,
                             'quiz', 'Quiz Mode', quiz_hover, 48, 112)
    flashcardsButton = SuffButton((10, SCREENSIZE[1] / 2 + 5), (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15),
                                   flashcards, 'flashcards', 'Flashcards', flashcards_hover, 48, 112)
    creditsButton = SuffButton((SCREENSIZE[0] / 2 + 5, SCREENSIZE[1] / 2 + 5),
                                (SCREENSIZE[0] / 2 - 15, SCREENSIZE[1] / 2 - 15), credits, 'credits', 'Credits',
                                credits_hover, 48, 112)
    while True:
        global dialogueBox
        state_functions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    CCC.change_expression(random.choice(['angry', 'furious', 'smug', 'evil', 'house', 'horror']))
                    dialogueBox = DialogueBox((CCC.x + CCC.head.surface.get_width() + 32, 300),
                                              random.choice(random_dialogue), 20, 'right')
        # button rendering
        dictionaryButton.draw()
        quizButton.draw()
        flashcardsButton.draw()
        creditsButton.draw()
        CCC.x = suff_lerp(CCC.x, (SCREENSIZE[0] - CCC.head.surface.get_width()) / 2, 1 / FPS * 6)
        CCC.y = suff_lerp(CCC.y, (SCREENSIZE[1] - CCC.head.surface.get_height()) / 2, 1 / FPS * 6)
        distances = (CCC.x + CCC.head.surface.get_width() / 2 - mousePos[0],
                     CCC.y + CCC.head.surface.get_height() / 2 - mousePos[1])
        CCC.angle = distances[0] / SCREENSIZE[0] * 8 * -45 * distances[1] / SCREENSIZE[1] / 2
        CCC.draw()
        if dialogueBox.text != '': dialogueBox.draw()

        state_post_functions()
main_menu()