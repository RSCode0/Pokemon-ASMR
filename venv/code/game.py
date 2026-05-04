import pygame

from map import Map

pygame.init()

class Game:
  def __init__(self):
    self.display_surface: pygame.Surface = pygame.display.set_mode((1280, 780))
    self.clock: pygame.time.Clock = pygame.time.Clock()
    self.framerate: int = 60
    self.running: bool = True
    
    self.map: Map = Map(self.display_surface)
  
  def run(self):
    while self.running:
      self.get_input()
      self.map.update()
      pygame.display.update()
      self.clock.tick(self.framerate)
  
  def get_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False