import uuid



class Element(object):

  def __init__(self):
    self.model_id = str(uuid.uuid1())
    self._internal_order_key = None

