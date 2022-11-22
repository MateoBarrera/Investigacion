import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class PrimaryResource():
  """Definition for primary resource class
  Include info description and historical data.
  """  
  name: str = None
  station: str = None
  type_source: str = None
  time_start: str = None
  time_end: str = None
  frequency: str = None
  unit: str = None
  source: str = None
  data_list: list = None

  def __init__(self, name=None, type_source=None, source=None) -> None:
    """Constructor for PrimaryResource

    Args:
        name (str, optional): Name resource. Defaults to None.
        type_source (str, optional): Type of resource (Solar, Hydro, Wind, Biomas, etc). Defaults to None.
        source (str, optional): Information source. Defaults to None.
    """    
    self.name = name
    self.type_source = type_source
    self.source = source
  
  def __str__(self) -> str:
    """Return description info for primary resource.

    Returns:
        str: Info object primary resource.
    """    
    return "Name: {}, Type: {}, Source: {} ".format(self.name, self.type_source, self.source)
  
  @property
  def data(self):
    return self.data_list

  @property
  def data_info(self) -> str:
    return "Name: {}, time start: {}, time end: {}, frequency: {}, unit: {}".format(self.name, self.time_start, self.time_end, self.frequency, self.unit)
   
  def from_json(self, json=None):
    """Set info PrimaryResource from a JSON object.

    Args:
        json (JSON, optional): Data resource object: Include Name, times, _source and data. Defaults to None.
    """    
    if json is None: pass  

  def to_json(self):
    """Convert instance to JSON object.
    """    
    pass    
  
  @staticmethod
  def _open_excel(self, path):
    return pd.read_csv(path)

  def from_excel(self, path=None) -> bool:
    """Set info PrimaryResource from a excel file.

    Args:
        path (str, optional): Path excel file with info primary resource. Defaults to None.
    
    Returns:
        bool: True for successfully information extraction. 
    """
    if path is None:
      return False
    file = self._open_excel(path=path)
    

  def to_excel(self):
    """Write current instance info in excel file.
    """
    pass

  
  
class Sources():
  def __init__(self) -> None:
    self.name = None
    self.description = None


class GraphSource(Sources):
  pass
