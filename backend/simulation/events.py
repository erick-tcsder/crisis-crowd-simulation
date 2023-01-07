from dataclasses import dataclass


@dataclass
class Event:
  EVENT_TYPE: str
  message: str
  data: dict | None = None
  
  def toJson(self):
    return {
      "EVENT_TYPE": self.EVENT_TYPE,
      "message": self.message,
      "data": self.data
    }
  
class LogEvent(Event):
  def __init__(self, message:str):
    super().__init__("LOG", message, None)
    
class EndEvent(Event):
  def __init__(self,message:str,data:dict):
    super().__init__('END', message,data)
    
class StartEvent(Event):
  def __init__(self, message:str, data:dict):
    super().__init__('START',message,data)
    
class ResultEvent(Event):
  def __init__(self,message:str,data:dict):
    # data should be an object like this:
    # {
    ####### This list should be ordered from best to worst place
    #   'bestPlaces': List[{
    #     'top': top,
    #     'left': left 
    #   }]
    # }
    super().__init__("RESULTS",message,data)