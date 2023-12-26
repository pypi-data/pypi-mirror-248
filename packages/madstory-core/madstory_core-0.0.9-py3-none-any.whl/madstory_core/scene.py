from .element import Element
from .manager import Manager
from enum import Enum
class Transition(Enum):
  NO_TRAN = 'None'
  FADE_IN = 'FADE_IN'
  FADE_OUT = 'FADE_OUT'
  SLIDE_RIGHT = 'SLIDE_RIGHT'
  SLIDE_LEFT = 'SLIDE_LEFT'

class StoryPart(Enum):
  START = "START"
  MIDDLE = "MID"
  END = "END"

class Art(Element):
  def __init__(self, scene_id, seed):
    super().__init__()
    self.seed = seed
    self._scene_id = scene_id
    self.photo_data = None

  @classmethod
  def load_from_data(cls, data):
    new_art = cls(data['scene_id'], data['seed'])
    new_art.photo_data = data['data']
    return new_art
  
  def export(self):
    return {
      'seed': self.seed,
      'scene_id': self._scene_id,
      'data': self.photo_data
    }

class Scene(Element):
  def __init__(self, parent_uuid, title):
    super().__init__()
    self._story_uuid = parent_uuid
    self.title = title
    self.text = None
    self.art = None
    self.voice = None
    self.transition = Transition.NO_TRAN
    self.story_part = StoryPart.START
    self.story_part_index = 0
    
  
  @classmethod
  def load_from_data(cls, data):
    new_scene = cls(data['story_id'], data['title'])
    new_scene.model_id = data['model_id']
    new_scene.text = data['text']
    new_scene.voice = data['voice']
    new_scene.transition = Transition(data['transition'])
    new_scene.art = Art.load_from_data(data['art'])
   
    return new_scene
  
  def export(self):
    art_data = {
      'seed': None,
      'data': None,
      'scene_id': None
    }
    if self.art is not None:
      art_data = self.art.export()

    return {
      'title': self.title, 
      'model_id': self.model_id,
      'text': self.text,
      'art': art_data,
      'transition': self.transition.value,
      'voice': self.voice,
      'story_id': self._story_uuid,
      'story_part': self.story_part.value,
      'story_part_index': self.story_part_index
    }
