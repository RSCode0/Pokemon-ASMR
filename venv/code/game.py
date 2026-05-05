import pygame

from map import Map
from player import Player

pygame.init()

class Game:
  def __init__(self):
    self.display_surface: pygame.Surface = pygame.display.set_mode((1280, 780))
    self.clock: pygame.time.Clock = pygame.time.Clock()
    self.dt = 0
    self.framerate: int = 60
    self.running: bool = True
    self.keys = []
    
    self.player = Player("ash_walk", 4, 4, self.keys)
    
    self.map: Map = Map(self.display_surface)
    self.map.add_player(self.player)
  
  def run(self):
    while self.running:
      self.get_input()
      self.map.update()
      pygame.display.update()
      self.dt = self.clock.tick(self.framerate) / 1000
      self.map.dt = self.dt
  
  def get_input(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        self.keys.append(event.key)
      elif event.type == pygame.KEYUP:
        self.keys.remove(event.key)