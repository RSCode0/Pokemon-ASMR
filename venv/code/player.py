import pygame

from entities import Entity

class Player(Entity):
  def __init__(self, spritesheet: str, cols: int, rows: int, keys: list[int]):
    super().__init__(spritesheet, cols, rows)
    self.keys: list[int] = keys
    
  def update(self):
    self.check_move()
  
  def check_move(self):
    if pygame.K_q in self.keys:
      self.move_left()
    elif pygame.K_d in self.keys:
      self.move_right()
    elif pygame.K_z in self.keys:
      self.move_up()
    elif pygame.K_s in self.keys:
      self.move_down()