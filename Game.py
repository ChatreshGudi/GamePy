import pygame
from pygame.locals import *
import copy
from colors import *

class Window():
    def __init__(self, width, height):
        '''Constructor'''
        pygame.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        self.scenes = []
        self.scene = None
        self.mouse = pygame.mouse
        self.main = pygame
        self.events = pygame.event.get()

    def run(self, main = None):
        '''Runs the application.'''
        running = True
        while running:
            self.__render()
            if main:
                main()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            pygame.display.flip()

    def __render(self):
        '''Renders the current scene.'''
        if self.scene:
            self.scene.render()

    def addScene(self, scene):
        '''Used to add a scene.'''
        self.scenes.append(scene)

    def removeScenebyIndex(self, index):
        '''Used to remove a scene using the index.'''
        self.scenes.pop(index)

    def removeScenebyScene(self, scene):
        '''Used to remove a scene using the index.'''
        self.scenes.remove(scene)

class Scene:
    def __init__(self, win:Window, bg:tuple = white, wintitle:str = ''):
        '''Constructor'''
        self.widgets = []
        self.win = win
        self.win.addScene(self)
        self.win.scene = self
        self.__bg = bg
        self.__wintitle = wintitle

    def setBG(self, bg:tuple):
        '''Used to change the background.'''
        self.__bg = bg

    def setWinTitle(self, title:str):
        '''Used to change the title.'''
        self.__wintitle = title

    def addWidget(self, widget):
        '''Used to add a widget.'''
        self.widgets.append(widget)

    def switchScene(self):
        pass

    def removeWidgets(self):
        pass

    def render(self):
        '''Used to render all the widgets.'''
        self.win.display.fill(self.__bg)
        self.win.main.display.set_caption(self.__wintitle)
        for i in self.widgets:
            i.render()

class Widget:
    def __init__(self, parent:Scene):
        '''Constructor'''
        self.parent = parent
        self.parent.addWidget(self)

class Text(Widget):
    def __init__(self, parent:Scene, text, size, font:str = None):
        '''Constructor'''
        super().__init__(parent)
        self.__text = text
        self.__size = size
        self.__fonttxt = font
        
        self.__font = pygame.font.SysFont(self.__fonttxt, self.__size) # Pygame Font


class Button(Widget):
    def __init__(self, parent: Scene, posx:int, posy:int, width:int, height:int, bg:tuple = (0, 0, 0), border_width:int = 0, border_color:tuple = (0, 0, 0), border_radius:int = 0) -> None:
        super().__init__(parent)
        # self.parent = parent
        # self.parent.addWidget(self)
        self.config = {
            'bg': bg,
            'border-color':border_color,
            'border-radius':border_radius,
            'border-width':border_width,
            'width':width,
            'height': height,
            'x': posx,
            'y': posy
        }
        self.hover_config = copy.deepcopy(self.config)

    def render(self):
        if self.isHover():
            config = self.hover_config
        else:
            config = self.config
        self.innerRect = pygame.Rect(config['x'], config['y'], config['width'], config['height'])
        self.parent.win.main.draw.rect(self.parent.win.display, config['border-color'], pygame.Rect(config['x']-config['border-width'], config['y']-config['border-width'], 2*config['border-width']+config['width'], 2*config['border-width']+config['height']), border_radius=config['border-radius'])
        self.parent.win.main.draw.rect(self.parent.win.display, config['bg'], self.innerRect, border_radius=config['border-radius']-config['border-width'])
        
    def isHover(self):
        pos = self.parent.win.mouse.get_pos()
        if pos[0]>self.config['x']-self.config['border-width'] and pos[0]<self.config['x']+self.config['border-width']+self.config['width'] and pos[1]> self.config['y']-self.config['border-width'] and pos[1]<self.config['y']-self.config['border-width']+2*self.config['border-width']+self.config['height']:
            return True
        return False
    
    def isClick(self, btn = 'l'):
        if self.parent.win.mouse.get_pressed()[['l', 'm', 'r'].index(btn)] and self.isHover():
            return True
        return False
    def onHover(self, func):
        pos = self.parent.win.mouse.get_pos()
        if self.isHover():
            func()

    def onClick(self, func , btn = 'l'):
        if self.isClick(btn):
            func()

class InputBox(Widget):
    def __init__(self, parent:Window, x:int, y:int, width:int, height:int, bg:tuple = black, color:tuple = white, border_width:int = 0, border_color:int = black, border_radius:int = 0) -> None:
        super().__int__(parent)
        # self.parent = parent
        # self.parent.addChild(self)
        self.text = ''
        self.config = {
            'x':x,
            'y':y,
            'width':width,
            'height': height,
            'bg': bg,
            'color':color,
            'border-width':border_width,
            'border-color':border_color,
            'border-radius': border_radius
        }
        self.hover_config = copy.deepcopy(self.config)

    def isHover(self):
        pos = self.parent.mouse.get_pos()
        if pos[0]>self.config['x']-self.config['border-width'] and pos[0]<self.config['x']+self.config['border-width']+self.config['width'] and pos[1]> self.config['y']-self.config['border-width'] and pos[1]<self.config['y']-self.config['border-width']+2*self.config['border-width']+self.config['height']:
            return True
        return False

    def render(self):
        if self.isHover():
            config = self.hover_config
        else:
            config = self.config
        
        self.innerRect = pygame.Rect(config['x'], config['y'], config['width'], config['height'])
        self.parent.main.draw.rect(self.parent.display, config['border-color'], pygame.Rect(config['x']-config['border-width'], config['y']-config['border-width'], 2*config['border-width']+config['width'], 2*config['border-width']+config['height']), border_radius=config['border-radius'])
        self.parent.main.draw.rect(self.parent.display, config['bg'], self.innerRect, border_radius=config['border-radius']-config['border-width'])    
        for event in self.parent.events:
            if event.type == pygame.KEYDOWN and self.isHover():
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        print(self.text)
        # self.parent.main.blit()
        
