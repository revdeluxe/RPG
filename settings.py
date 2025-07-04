# settings.py
import json
import os
from panda3d.core import load_prc_file_data, NodePath
from render import RenderManager
from inputs import InputManager
from ui import UIManager

CONFIG = {}

class SettingsFramework:
    def __init__(self, base, config_path="settings.json"):
        self.base = base
        self.config_path = config_path
        self.settings = {}
        self.input = None
        self.render = None
        self.ui = None

        self._load_config()
        self._apply_prc_settings()
        self._init_subsystems()

    def _load_config(self):
        global CONFIG
        with open(self.config_path, 'r') as f:
            self.settings = json.load(f)
            CONFIG = self.settings  # Make it globally available if needed

    def _apply_prc_settings(self):
        render_cfg = self.settings["renderingSettings"]
        w, h = render_cfg["resolution"]["width"], render_cfg["resolution"]["height"]
        fullscreen = int(render_cfg.get("fullscreen", False))
        vSync = int(render_cfg.get("vSync", False))
            # settings.py → _apply_prc_settings()
        bias = self.settings["renderingSettings"].get("textureLodBias", 0.0)
        load_prc_file_data("", f"texture-lodbias {bias}")

        load_prc_file_data("", f"win-size {w} {h}")
        load_prc_file_data("", f"fullscreen {fullscreen}")
        load_prc_file_data("", f"sync-video {vSync}")

    def _init_subsystems(self):
        self.input = InputManager(self.base, self.settings["inputBindings"])
        self.render = RenderManager(self.base, self.settings["renderingSettings"])
        self.ui = UIManager(self.base, self.settings)

    def reload_config(self):
        self._load_config()
        # Optional: Reapply PRC or hot-reload subsystems

    def get_setting(self, path, default=None):
        keys = path.split(".")
        ref = self.settings
        for key in keys:
            ref = ref.get(key, {})
        return ref or default
    