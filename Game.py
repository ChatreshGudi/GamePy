import pygame
from pygame.locals import *
import copy
from colors import *

class Window():
    def __init__(self, width, height, title):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.widgets = []
        self.mouse = pygame.mouse
        self.main = pygame
        self.events = pygame.event.get()
        self.fill = 'color'
        self.bg = white
        self.setBGColor(self.bg)

    def setBGColor(self, color):
        self.display.fill(color)

    def addWidget(self):
        pass

    def run(self, main = None):
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
        if self.fill == 'color':
            self.setBGColor(self.bg)
        for i in self.widgets:
            i.render()

    def addChild(self, widget):
        self.widgets.append(widget)


class Button:
    def __init__(self, parent: Window, posx:int, posy:int, width:int, height:int, bg:tuple = (0, 0, 0), border_width:int = 0, border_color:tuple = (0, 0, 0), border_radius:int = 0) -> None:
        self.parent = parent
        self.parent.addChild(self)
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
        self.parent.main.draw.rect(self.parent.display, config['border-color'], pygame.Rect(config['x']-config['border-width'], config['y']-config['border-width'], 2*config['border-width']+config['width'], 2*config['border-width']+config['height']), border_radius=config['border-radius'])
        self.parent.main.draw.rect(self.parent.display, config['bg'], self.innerRect, border_radius=config['border-radius']-config['border-width'])
        
    def isHover(self):
        pos = self.parent.mouse.get_pos()
        if pos[0]>self.config['x']-self.config['border-width'] and pos[0]<self.config['x']+self.config['border-width']+self.config['width'] and pos[1]> self.config['y']-self.config['border-width'] and pos[1]<self.config['y']-self.config['border-width']+2*self.config['border-width']+self.config['height']:
            return True
        return False
    
    def isClick(self, btn = 'l'):
        if self.parent.mouse.get_pressed()[['l', 'm', 'r'].index(btn)] and self.isHover():
            return True
        return False
    def onHover(self, func):
        pos = self.parent.mouse.get_pos()
        if self.isHover():
            func()

    def onClick(self, func , btn = 'l'):
        if self.isClick(btn):
            func()

class InputBox:
    def __init__(self, parent:Window, x:int, y:int, width:int, height:int, bg:tuple = black, color:tuple = white, border_width:int = 0, border_color:int = black, border_radius:int = 0) -> None:
        self.text = ''
        self.parent = parent
        self.parent.addChild(self)
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
        
