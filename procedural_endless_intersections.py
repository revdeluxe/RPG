from templates.city_block import INTERSECTION_TYPES
from direct.showbase.Loader import Loader

from direct.showbase.ShowBase import ShowBase

from settings import SettingsFramework
from camera import CameraController
from menu import SettingsMenu

def load_model(model_path, position):
    model = loader.loadModel(model_path)
    model.reparentTo(base.render)
    model.setPos(*position)
    return model

def generate_grid(rows, cols, intersection_type="city"):
    tile = INTERSECTION_TYPES[intersection_type]
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
        self.settings = SettingsFramework(self)
        self.setBackgroundColor(0.1, 0.1, 0.1)
        self.generate_city()
        self.camera = CameraController(self, self.settings.settings)
        
        self.settings.camera = self.camera
        self.menu = SettingsMenu(self, self.settings)
        self.settings.ui.create_label("test", "Scene loaded successfully", pos=(0, -0.9))

    def generate_city(self):
        # Generate a 10x10 grid of city blocks
        generate_grid(10, 10, intersection_type="city")

app = ProceduralCityGenerationApp()
app.run()
