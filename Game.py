import pygame
from pygame.locals import *
class Window():
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))

    def setBGColor(self, color):
        self.display.fill(color)
