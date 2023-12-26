from .element import Element

class Manager(object):
  def __init__(self):
    self._internal_lookup = []
    self._limit = 140
  
  def add(self, managable: Element):
    if len(self._internal_lookup) == 140:
      raise Exception("Too many scenes are in this story. The limit is 140")
    self._internal_lookup.append(managable)
    return True

  def reorder(self, element_list):
    if len(element_list) > 140:
      raise Exception("Too many scenes are in this story. The limit is 140")
    self._internal_lookup = element_list
    return True

  def list(self):
    return self._internal_lookup
  
  def export(self):
    returned_list = []
    for obj in self._internal_lookup:
      returned_list.append(obj.export())
    return returned_list

  