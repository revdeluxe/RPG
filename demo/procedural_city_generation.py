import sys
from pathlib import Path

# Add the root folder to the system path
root_folder = Path(__file__).resolve().parent.parent.parent
sys.path.append('C:\\Users\\Admin\\Documents\\GitHub\\RPG')

from templates.city_block import INTERSECTIONS
from direct.showbase.Loader import Loader
from direct.showbase.ShowBaseGlobal import render

from direct.showbase.ShowBase import ShowBase

from settings import SettingsFramework
from camera import CameraController
from menu import SettingsMenu


base = ShowBase()
loader = Loader(base)

def load_model(model_path, position):
    """
    Load a model from the given path and set its position.
    
    :param model_path: Path to the model file.
    :param position: Tuple (x, y, z) for the model's position.
    """
    model = loader.loadModel(model_path)
    model.reparentTo(render)
    model.setPos(*position)
    return model

def generate_grid(rows, cols, intersection_type="city"):
    tile = INTERSECTIONS[intersection_type]
    model_path = tile["path"]
    tile_size = tile["tile_size"]

    for row in range(rows):
        for col in range(cols):
            position = (
                col * tile_size[0],
                row * tile_size[1],
                0
            )
            load_model(model_path, position)

class ProceduralCityGenerationApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(0.1, 0.1, 0.1)
        self.generate_city()
        self.camera = CameraController(self, self.settings.settings)
        self.settings = SettingsFramework(self)
        self.settings.camera = self.camera
        self.menu = SettingsMenu(self, self.settings)
        self.settings.ui.create_label("test", "Scene loaded successfully", pos=(0, -0.9))

    def generate_city(self):
        # Generate a 10x10 grid of city blocks
        generate_grid(10, 10, intersection_type="city")

app = ProceduralCityGenerationApp()
app.run()
