import pyscroll
import pytmx
import pygame

from player import Player

class Map:
  def __init__(self, display_surface):
    self.display_surface: pygame.Surface = display_surface
    self.dt: int | float = 0
    self.map = "map_0"
    self.tmx_data: pytmx.TiledMap = None
    self.map_data: pyscroll.TiledMapData = None
    self.map_layer: pyscroll.BufferedRenderer = None
    self.group: pyscroll.PyscrollGroup = None
    
    self.collisions: list[pygame.Rect] = []
    self.player_spawn: list[int | None, int | None] = []
    self.tps = []
    
    self.player: Player | None = None
    
    self.load_map("map_0")
    
  def update(self):
    self.group.center(self.player.rect.center)
    self.group.update()
    self.group.draw(self.display_surface)
    self.player.dt = self.dt
    self.check_tp()
      
  def load_map(self, map: str):
    self.tmx_data = pytmx.load_pygame(f"venv/assets/map/{map}.tmx")
    self.get_collisions()
    self.get_spawn()
    self.get_tps()
    self.map = map
    self.map_data = pyscroll.TiledMapData(self.tmx_data)
    self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.display_surface.get_size())
    self.zoom_map()
    self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
    if self.player:
      self.add_player(self.player)
  
  def zoom_map(self):
    if self.map.startswith("house"):
      self.map_layer.zoom = 5
    else:
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
      if str(obj.name).startswith("spawn") and str(obj.name).endswith(self.map):
        self.player_spawn = [obj.x, obj.y]
        return
      if obj.name == "player_spawn":
        self.player_spawn = [obj.x, obj.y]
  
  def get_tps(self):
    tps = []
    
    for obj in self.tmx_data.objects:
      if str(obj.name).split(" ")[0] == "tp":
        tps.append({
          "rect": pygame.rect.Rect((obj.x, obj.y, obj.width, obj.height)),
          "name": str(obj.name).split(" ")[1]
        })
    
    self.tps = tps
  
  def check_tp(self):
    for tp in self.tps:
      if self.player.rect.colliderect(tp["rect"]):
        self.load_map(tp["name"])