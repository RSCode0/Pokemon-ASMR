import pygame

class Entity(pygame.sprite.Sprite):
  def __init__(self, spritesheet: str, cols: int, rows: int):
    super().__init__()
    self.spritesheet: pygame.Surface = pygame.image.load(f"venv/assets/sprite/{spritesheet}.png").convert_alpha()
    self.spritesheet: pygame.Surface = pygame.transform.scale_by(self.spritesheet, 0.5)
    self.width, self.height = self.spritesheet.get_size()
    self.cols: int = cols
    self.rows: int = rows
    self.frame_width: int | float = self.width // self.cols
    self.frame_height: int | float = self.height // self.rows
    self.frame_index: int | float = 0
    self.image: pygame.Surface = self.spritesheet.subsurface((0, 0, self.frame_width, self.frame_height))
    self.all_images: dict[list: pygame.Surface] = self.get_all_images()
    self.rect: pygame.Rect = self.image.get_rect()
    self.dt: int | float = 0
  
  def move_right(self):
    self.rect.x += 1
    self.animation("right")
  
  def move_left(self):
    self.rect.x -= 1
    self.animation("left")
    
  def move_up(self):
    self.rect.y -= 1
    self.animation("up")
    
  def move_down(self):
    self.rect.y += 1
    self.animation("down")
  
  def animation(self, direction: str):
    self.frame_index += 7 * self.dt
    self.image = self.all_images[direction][int(self.frame_index) % len(self.all_images[direction])]
  
  def get_all_images(self):
    frames = {
      "down": [],
      "left": [],
      "right": [],
      "up": []
    }
    
    for row, direction in enumerate(frames.keys()):
      for col in range(self.cols):
        frames[direction].append(self.spritesheet.subsurface(((self.width // self.cols) * col, (self.height // self.rows) * row, self.frame_width, self.frame_height)))
    
    return frames
  