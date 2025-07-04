# render.py
from panda3d.core import AntialiasAttrib, LODNode, NodePath, Filename, load_prc_file_data
from direct.showbase.Loader import Loader

class RenderManager:
    def __init__(self, base, settings):
        self.base = base
        self.settings = settings
        self.lod_settings = settings["lodbias"]
        self.features = settings.get("features", {})
        self.chunks = {}  # Key: chunk name, Value: NodePath

        self._apply_render_flags()
    
    def _apply_render_flags(self):
        if self.settings.get("antiAliasing", True):
            self.base.render.set_antialias(AntialiasAttrib.MAuto)
        
        if self.settings["debugSettings"].get("wireframeMode"):
            self.base.render.set_render_mode_wireframe()

        if self.features.get("testNewLighting"):
            self._inject_lighting_debug_shader()

    def _inject_lighting_debug_shader(self):
        # Placeholder for custom shader attachment
        pass

    def load_scene(self, path, flatten=False):
        model = self.base.loader.load_model(Filename.from_os_specific(path))
        model.reparent_to(self.base.render)
        if flatten:
            model.flatten_medium()
        return model

    def load_chunk(self, name, path, position):
        if name in self.chunks:
            return  # Already loaded
        chunk = self.base.loader.load_model(Filename.from_os_specific(path))
        chunk.set_pos(*position)
        chunk.reparent_to(self.base.render)
        self.chunks[name] = chunk

    def unload_chunk(self, name):
        if name in self.chunks:
            self.chunks[name].remove_node()
            del self.chunks[name]

    def update_lod(self, camera_pos):
        for name, chunk in list(self.chunks.items()):
            dist = (chunk.get_pos() - camera_pos).length()
            if dist > self.lod_settings["max"]:
                self.unload_chunk(name)
