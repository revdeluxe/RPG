# ui.py
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode, TransparencyAttrib, ClockObject

class UIManager:
    def __init__(self, base, settings):
        self.base = base
        self.settings = settings
        self.elements = {}

        if settings.get("miscSettings", {}).get("showFPS", True):
            self.create_fps_counter()
        print("UIManager initialized with settings:", self.settings)

    def create_fps_counter(self):
        from panda3d.core import ClockObject

        self.fps_text = OnscreenText(
            text="FPS: 0.0",
            pos=(-1.3, 0.9),
            scale=0.05,
            fg=(1, 1, 0, 1),
            align=TextNode.ALeft,
            mayChange=True
        )
        self.base.task_mgr.add(self.update_fps, "update_fps_task")

    def update_fps(self, task):
        fps = ClockObject.get_global_clock().get_average_frame_rate()
        self.fps_text.setText(f"FPS: {fps:.1f}")
        return task.cont

    def create_label(self, key, text, pos, color=(1,1,1,1), scale=0.05):
        label = OnscreenText(
            text=text,
            pos=pos,
            scale=scale,
            fg=color,
            align=TextNode.ACenter,
            mayChange=True
        )
        self.elements[key] = label

    def set_text(self, key, new_text):
        if key in self.elements:
            self.elements[key].setText(new_text)

    def remove(self, key):
        if key in self.elements:
            self.elements[key].destroy()
            del self.elements[key]
