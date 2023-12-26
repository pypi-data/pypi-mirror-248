import uuid
from .scene import Scene
from .element import Element
from .manager import Manager

class MadStory(Element):

  def __init__(self, title):
    super().__init__()
    self.scene_manager = Manager()
    self.title = title
    self.credits = None

  
  def export_title_scene(self):
    return {
      'title': self.title,
      'credits': self.credits
    }
  def create_scene(self, title):
    self.scene_manager.add(Scene(self.model_id, title))
  
  def export(self):
    exported_story_obj = {'scenes':[]}
    exported_story_obj['scenes'] = self.scene_manager.export()
    exported_story_obj['model_id'] = self.model_id
    exported_story_obj['title'] = self.title
    exported_story_obj['title_card'] = self.export_title_scene()
    return exported_story_obj
  
  @classmethod
  def load_from_data(cls, data):
    new_story = cls(data['title'])
    new_story.model_id = data['model_id']
    scenes = []
    for dat in data['scenes']:
      new_scene = Scene.load_from_data(dat)
      scenes.append(new_scene)
    new_story.scene_manager.reorder(scenes)
    return new_story