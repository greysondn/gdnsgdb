from PIL import Image
from ruamel.yaml import YAML

from typing import (
    Any,
)

class GDNSGDBColor:
    """Just a simple color class to convert between RGB tuples and html strings"""
    def __init__(self, red:int=0, green:int=0, blue:int=0):
        """Init.
        <br><br>
        WARNING: This does not validate its inputs. You will see errors down
        the line somewhere if you screw up.
        
        Args:
            red: channel value 0-255. Defaults to 0.
            green: channel value 0-255. Defaults to 0.
            blue: channel value 0-255. Defaults to 0.
        """
        self.red:int = red
        self.green:int = green
        self.blue:int = blue
        
    @classmethod
    def from_html(cls, html_color:str) -> "GDNSGDBColor":
        ret:GDNSGDBColor = GDNSGDBColor()
        
        # there are probably better algorithms, "but"
        col_src:str = html_color.lstrip("#")
        
        col_src_red:str   = col_src[0:2]
        col_src_green:str = col_src[2:4]
        col_src_blue:str  = col_src[4:6]
        
        ret.red   = int(col_src_red,   16)
        ret.green = int(col_src_green, 16)
        ret.blue  = int(col_src_blue,  16)
        
        return ret
    
    @classmethod
    def from_tuple(cls, pil_color:tuple[int, ...]) -> "GDNSGDBColor":
        ret:GDNSGDBColor = GDNSGDBColor()
        
        # this one should be straightforward
        ret.red   = pil_color[0]
        ret.green = pil_color[1]
        ret.blue  = pil_color[2]
        
        return ret
    
    def to_html(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
    
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)
        
class GDNSGDB:
    def __init__(self):
        self.conf:Any = None
        """
        Config for this instance
        """
    
        self.palettes:dict[str, dict[int, GDNSGDBColor]]= {}
        """Palette cache.
        """
    def load_yaml(self, yaml:str) -> None:
        """
        decodes given yaml src data into self.conf and sets related fields.

        Args:
            yaml: a yaml src str of some sort
        """
        # just the barebones load part
        loader:YAML = YAML(typ="safe")
        self.conf = loader.load(yaml)
        
        # load the palettes in
        for flat_color, palette_entries in self.conf["colors"].items():
            # we can get our key for storage and start a value dict
            swp_k:str = flat_color
            swp_v:dict[int, GDNSGDBColor] = {}
            
            # and then the other part
            for index, palette_color in palette_entries.items():
                swp_v[index] = GDNSGDBColor.from_html(palette_color)
            
            # throw it in our dict
            self.palettes[swp_k] = swp_v
    
    def run(self):
        pass