# main.py
from direct.showbase.ShowBase import ShowBase
from settings import SettingsFramework
from camera import CameraController
from menu import SettingsMenu

class GameApp(ShowBase):
    def __init__(self):
        super().__init__()
        
        # 1. Bootstrap settings + subsystems
        self.settings = SettingsFramework(self)
        print("🎮 Subsystems:")
        print("- Input:", self.settings.input)
        print("- Render:", self.settings.render)
        print("- UI:", self.settings.ui)


        self.camera   = CameraController(self, self.settings.settings)
        self.scene    = self.loader.load_model("assets/models/wall-a.glb")
        self.scene.reparent_to(self.render)
        self.scene.set_pos(0, 10, 0)

        # 4. Optional: UI test label
        self.settings.camera = self.camera
        self.menu = SettingsMenu(self, self.settings)
        self.settings.ui.create_label("test", "Scene loaded successfully", pos=(0, -0.9))


app = GameApp()
app.run()
