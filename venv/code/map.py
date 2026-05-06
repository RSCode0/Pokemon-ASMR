import pyscroll
import pytmx
import pygame

from player import Player

class Map:
  def __init__(self, display_surface):
    self.display_surface: pygame.Surface = display_surface
    self.dt: int | float = 0
    self.tmx_data: pytmx.TiledMap = None
    self.map_data: pyscroll.TiledMapData = None
    self.map_layer: pyscroll.BufferedRenderer = None
    self.group: pyscroll.PyscrollGroup = None
    
    self.collisions: list[pygame.Rect] = []
    self.player_spawn: list[int | None, int | None] = []
    
    self.load_map("map_0")
    
    self.player: Player | None = None
  
  def update(self):
    self.group.center(self.player.rect.center)
    self.group.update()
    self.group.draw(self.display_surface)
    self.player.dt = self.dt
      
  def load_map(self, map: str):
    self.tmx_data = pytmx.load_pygame(f"venv/assets/map/{map}.tmx")
    self.get_collisions()
    self.get_spawn()
    self.map_data = pyscroll.TiledMapData(self.tmx_data)
    self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.display_surface.get_size())
    self.zoom_map()
    self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
  
  def zoom_map(self):
    self.map_layer.zoom = 3
  
  def add_player(self, player: Player):
    self.player = player
    self.group.add(self.player)
    self.player.collisions = self.collisions
    self.player.rect.center = self.player_spawn
  
  def get_collisions(self):
    for obj in self.tmx_data.objects:
      if obj.name == "collision":
        self.collisions.append(pygame.rect.Rect((obj.x, obj.y, obj.width, obj.height)))
    
  def get_spawn(self):
    for obj in self.tmx_data.objects:
      if obj.name == "player_spawn":
        self.player_spawn = [obj.x, obj.y]