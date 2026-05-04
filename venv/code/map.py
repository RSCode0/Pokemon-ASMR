import pyscroll
import pytmx
import pygame

class Map:
  def __init__(self, display_surface):
    self.display_surface: pygame.Surface = display_surface
    self.tmx_data: pytmx.TiledMap = None
    self.map_data: pyscroll.TiledMapData = None
    self.map_layer: pyscroll.BufferedRenderer = None
    self.group: pyscroll.PyscrollGroup = None
    self.load_map("map_0")
  
  def update(self):
    self.group.draw(self.display_surface)
  
  def load_map(self, map):
    self.tmx_data = pytmx.load_pygame(f"venv/assets/map/{map}.tmx")
    self.map_data = pyscroll.TiledMapData(self.tmx_data)
    self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.display_surface.get_size())
    self.zoom_map()
    self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
  
  def zoom_map(self):
    self.map_layer.zoom = 5