# main.py
from direct.showbase.ShowBase import ShowBase
from settings import SettingsFramework
from camera import CameraController
from menu import SettingsMenu
from panda3d.core import load_prc_file_data
import random, math

# 1) Read your JSON early (without ShowBase)
import json, os
cfg = json.load(open(os.path.join("settings.json")))
w = cfg["renderingSettings"]["resolution"]["width"]
h = cfg["renderingSettings"]["resolution"]["height"]
fullscreen = cfg["renderingSettings"].get("fullscreen", False)

# 2) Inject PRC
prc = f"""
win-size     {w} {h}
fullscreen   {1 if fullscreen else 0}
aspect-ratio {w / h:.6f}
"""
load_prc_file_data("", prc)

class GameApp(ShowBase):
    def __init__(self):
        super().__init__()

        # 1) Bootstrap settings + subsystems
        self.settings = SettingsFramework(self)
        print("🎮 Subsystems:")
        print("- Input:", self.settings.input)
        print("- Render:", self.settings.render)
        print("- UI:", self.settings.ui)

        # 2) Camera
        self.camera = CameraController(self, self.settings.settings)
        # make it available to your menu
        self.settings.camera = self.camera

        # 3) Load & position your main scene
        #    (use loader.loadModel, not load_model)
        self.scene = self.loader.loadModel("scene/glb/wall-truck-w2e-3[3].glb")
        self.scene.reparentTo(self.render)
        self.scene.setPos(0, 0, 0)
        self.scene.setHpr(0, 90, 0)
        self.scene.setScale(2.0)

        # 4) Settings menu + a UI test label
        self.menu = SettingsMenu(self, self.settings)
        self.settings.ui.create_label(
            "test", "Scene loaded successfully", pos=(0, -0.9)
        )
        


# 6) Run the app
app = GameApp()
app.run()