from entities import Entity
import pygame
import json

class NPC(Entity):
  def __init__(self, spritesheet, cols, rows, name):
    super().__init__(spritesheet, cols, rows)
    self.get_rect()
    
    self.name = name
    
    self.screen = None
    self.keys = None
    
    self.last_dialogue_id = ""
    self.dialogue_active = False
    self.npc_turn = True
    self.dialogues = []
    self.speakers = []
    self.dialogue_index = 0
    self.current_text = ""
    self.current_speaker = ""
    self.font = pygame.font.Font(None, 30)
    
    self.typing_index = 0
    self.typing_speed = 20
    self.last_typing_time = 0
  
  def get_rect(self):
    bounding = self.image.get_bounding_rect()
    self.hitbox = pygame.rect.Rect((0, 0, bounding.width * 0.7, bounding.height))
    self.hitbox.midbottom = (self.rect.left, self.rect.y + bounding.bottom)
  
  def load_dialogues(self):
    with open("venv/assets/data/dialogues.json", encoding="utf-8") as file:
      data_dialogues = json.load(file)
      with open("venv/assets/data/save.json", encoding="utf-8") as file:
        data_save = json.load(file)
        self.last_dialogue_id = data_save["dialogues"][self.name]
        self.speakers = data_dialogues[self.name][self.last_dialogue_id][0]
        self.dialogues = data_dialogues[self.name][self.last_dialogue_id][1:]
  
  def active_dialogue(self, keys, screen):
    self.keys = keys
    self.screen = screen
    
    if self.dialogue_active:
      current_time = pygame.time.get_ticks()
      if self.typing_index < len(self.current_text):
        if current_time - self.last_typing_time > self.typing_speed:
          self.typing_index += 1
          self.last_typing_time = current_time
      
      self.draw_current_dialogue(screen)
      
      if pygame.K_SPACE in self.keys:
        if self.typing_index < len(self.current_text):
          self.typing_index = len(self.current_text)
          keys.remove(pygame.K_SPACE)
          return
        self.advance_dialogue()
        keys.remove(pygame.K_SPACE)
    else:
      if pygame.K_SPACE in self.keys:
        self.screen_fade()
        self.start_dialogue()
        self.dialogue_active = True
        keys.remove(pygame.K_SPACE)
  
  def next_section(self):
    next_section_name = self.last_dialogue_id
    next_section_index = None
    
    with open("venv/assets/data/dialogues.json", encoding="utf-8") as file:
      data_dialogues = json.load(file)
      for i, key in enumerate(data_dialogues[self.name].keys()):
        if next_section_index == i:
          next_section_name = key
          break
        if key == self.last_dialogue_id:
          if i < len(data_dialogues[self.name].keys()):
            next_section_index = i + 1
    self.save_progression(next_section_name)
  
  def save_progression(self, next_section_name):
    save_file = "venv/assets/data/save.json"
    
    with open(save_file, "r", encoding="utf-8") as file:
      data_save = json.load(file)
    
    data_save["dialogues"][self.name] = next_section_name
    
    with open(save_file, "w", encoding="utf-8") as file:
      json.dump(data_save, file, ensure_ascii=False, indent=4)
  
  def draw_current_dialogue(self, screen):
    if self.current_text:
      self.draw_speaker_name(screen)
      self.draw_text(self.current_text[:self.typing_index], screen)
  
  def draw_speaker_name(self, screen):
    if self.current_speaker:
      name_font = pygame.font.Font(None, 25)
      name_surface = name_font.render(self.current_speaker, True, (255, 255, 255))
      name_width, name_height = name_surface.get_size()
      box_width = name_width + 40
      box_height = name_height + 20
      box_x = 40
      box_y = 780 - 150
      pygame.draw.rect(screen, (58, 158, 181), (box_x, box_y, box_width, box_height), border_radius=5)
      pygame.draw.rect(screen, (58, 158, 181), (box_x, box_y, box_width, box_height), 2, border_radius=5)
      screen.blit(name_surface, (box_x + 20, box_y + 10))
  
  def advance_dialogue(self):
    if self.dialogue_index >= len(self.dialogues):
      self.next_section()
      self.dialogue_active = False
      self.screen_fade()
      return
    
    dialogue = self.dialogues[self.dialogue_index]
    self.current_speaker = dialogue["speaker"]
    self.current_text = dialogue["text"]
    self.npc_turn = self.current_speaker != "Player"
    self.dialogue_index += 1
    
    self.typing_index = 0
  
  def screen_fade(self):
    overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
    max_alpha = 160
    step = 10
    delay = 30
    
    for alpha in range(0, max_alpha + 1, step):
      overlay.fill((0, 0, 0, alpha))
      self.screen.blit(overlay, (0, 0))
      pygame.display.update()
      pygame.event.pump()
      pygame.time.delay(delay)
  
  def start_dialogue(self):
    self.load_dialogues()
    self.dialogue_index = 0
    self.npc_turn = True
    self.advance_dialogue()
  
  def draw_text(self, text, screen):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
      test_line = current_line + word + " "
      if self.font.size(current_line)[0] < 1280 - 90:
        current_line = test_line
      else:
        lines.append(current_line)
        current_line = word + " "
    
    lines.append(current_line)
    
    line_height = self.font.get_linesize()
    pygame.draw.rect(screen, (58, 158, 181), (40, 780 - 110, 1280 - 80, 100), border_radius=10)
    pygame.draw.rect(screen, (58, 158, 181), (40, 780 - 110, 1280 - 80, 100), 2, border_radius=10)
    
    for i, line in enumerate(lines):
      x_pos = 50
      for letter in line:
        if letter.strip():
          screen.blit(self.font.render(letter, True, (255, 255, 255)), (x_pos, 780 - 90 + i * line_height))
        x_pos += self.font.size(letter)[0]