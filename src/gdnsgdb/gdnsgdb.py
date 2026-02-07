from PIL import Image
from ruamel.yaml import YAML

from pathlib import (
    Path,
)

from typing import (
    Any,
)



class GDNSGDBColor:
    """Just a simple color class to convert between RGB tuples and html strings"""
    def __init__(self, red:int = 0, green:int = 0, blue:int = 0):
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
        
        col_src_red:str = col_src[0:2]
        col_src_green:str = col_src[2:4]
        col_src_blue:str = col_src[4:6]
        
        ret.red = int(col_src_red, 16)
        ret.green = int(col_src_green, 16)
        ret.blue = int(col_src_blue, 16)
        
        return ret
    
    @classmethod
    def from_tuple(cls, pil_color:tuple[int, ...]) -> "GDNSGDBColor":
        ret: GDNSGDBColor = GDNSGDBColor()
        
        # this one should be straightforward
        ret.red = pil_color[0]
        ret.green = pil_color[1]
        ret.blue = pil_color[2]
        
        return ret
    
    def to_html(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"
    
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)



class GDNSGDBMetaTemplate:
    def __init__(
        self,
        path:Path,
        color_map:dict[str, int],
        accept_logo:bool,
        logo_region:tuple[int, int, int, int] = (0, 0, 0, 0),
        logo_align_horizontal:str = "center",
        logo_align_vertical:str = "center"
    ):
        self.image:Image.Image = Image.open(path)
        
        self.color_map:dict[tuple[int, int, int], int] = {}
        for k, v in color_map.items():
            self.color_map[GDNSGDBColor.from_html(k).to_tuple()] = v
        
        self.accept_logo:bool = accept_logo
        self.logo_region:tuple[int, int, int, int] = logo_region
        self.logo_align_vertical:str = logo_align_vertical
        self.logo_align_horizontal:str = logo_align_horizontal



class GDNSGDB:
    def __init__(self):
        self.conf:Any = None
        """
        Config for this instance
        """
        
        self.palettes:dict[str, dict[int, GDNSGDBColor]] = {}
        """
        Palette cache.
        """
        
        self.meta_templates:dict[str, GDNSGDBMetaTemplate] = {}
        """
        Meta template cache
        """
    
    def _load_palettes(self) -> None:
        """
        Internal helper solely responsible for loading and caching palettes
        internally.
        """
        
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
    
    def _load_meta_templates(self) -> None:
        """
        Internal helper solely responsible for loading and caching meta
        templates initially.
        """
        swp_root:Path = Path(self.conf["meta"]["root_dir"])
        
        for name, data in self.conf["meta_templates"].items():
            # the name becomes a key later
            swp_k:str = name
            
            # our v is a bit more complicated, we have to gather the parts
            
            # path
            swp_path:Path = swp_root / data["path"]
            
            # region
            swp_region:tuple[int, int, int, int] = (0, 0, 0, 0)
            
            if (data["logo"]["accept"]):
                swp_region = (
                    data["logo"]["region"]["top"],
                    data["logo"]["region"]["bottom"],
                    data["logo"]["region"]["left"],
                    data["logo"]["region"]["right"]
                )
            
            # horizontal align
            swp_horizontal:str = "center"
            
            if (data["logo"]["accept"]):
                swp_horizontal = data["logo"]["align"]["horizontal"]
            
            # vertical align
            swp_vertical:str = "center"
            
            if (data["logo"]["accept"]):
                swp_vertical = data["logo"]["align"]["vertical"]
            
            # finally get value
            swp_v:GDNSGDBMetaTemplate = GDNSGDBMetaTemplate(
                swp_path,
                data["color_map"],
                data["logo"]["accept"],
                swp_region,
                swp_horizontal,
                swp_vertical
            )
            
            # assign
            self.meta_templates[swp_k] = swp_v
    
    def load_yaml(self, yaml:str) -> None:
        """
        decodes given yaml src data into self.conf and sets related fields.

        Args:
            yaml: a yaml src str of some sort
        """
        # just the barebones load part
        loader:YAML = YAML(typ="safe")
        self.conf = loader.load(yaml)
        
        # call internal helpers now that conf is set
        self._load_palettes()
        self._load_meta_templates()
    
    def run(self):
        pass
