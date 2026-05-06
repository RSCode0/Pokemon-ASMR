import pygame

from entities import Entity

class Player(Entity):
  def __init__(self, spritesheet: str, cols: int, rows: int, keys: list[int]):
    super().__init__(spritesheet, cols, rows)
    self.keys: list[int] = keys
    
  def update(self):
    super().update()
    self.check_move()
  
  def check_move(self):
    if pygame.K_q in self.keys:
      self.move_left()
      if not self.check_collision():
        self.rect.x -= 1
    elif pygame.K_d in self.keys:
      self.move_right()
      if not self.check_collision():
        self.rect.x += 1
    elif pygame.K_z in self.keys:
      self.move_up()
      if not self.check_collision():
        self.rect.y -= 1
    elif pygame.K_s in self.keys:
      self.move_down()
      if not self.check_collision():
        self.rect.y += 1