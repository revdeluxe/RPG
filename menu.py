from direct.gui.DirectGui import (
    DirectFrame, DirectScrolledFrame,
    DirectLabel, DirectCheckButton,
    DirectSlider, DirectEntry, DirectButton
)
from panda3d.core import TextNode

class SettingsMenu:
    def __init__(self, base, settings_framework):
        self.base    = base
        self.sf      = settings_framework
        self.active  = False
        self.widgets = {}
        self.row_h   = 0.07

        # 1) Create the full-screen semi-opaque overlay
        self.frame = DirectFrame(
            parent    = base.aspect2dp,
            frameColor=(0, 0, 0, 0.85),
            frameSize = (-1,1,-1,1),
            pos       = (0,0,0)
        )
        self.frame.hide()

        # 2) Create a scrollable region inside that frame
        self.scroll = DirectScrolledFrame(
            parent      = self.frame,
            frameSize   = (-0.95, 0.95, -0.95, 0.95),
            canvasSize  = (-0.95, 0.95, -2.0, 0.95),
            autoHideScrollBars = True
        )
        # Convenience pointer to the “content” node
        self.canvas = self.scroll.getCanvas()

        # 3) Build all controls once, into self.canvas
        self._build_menu(
            cfg        = self.sf.settings,
            parent     = self.canvas,
            parent_key = "",
            x0         = -0.9,
            y0         =  0.9,
            indent     =  0.0
        )

        # 4) “Save & Close” at the bottom of the overlay
        DirectButton(
            parent  = self.frame,
            text    = "Save & Close",
            scale   = 0.06,
            pos     = (0, 0, -0.95),
            command = self._on_save_close
        )

        # 5) Bind your toggle key
        base.accept("f1", self.toggle)

        # Debug: show what got registered
        print("🌳 SettingsMenu widgets:", list(self.widgets.keys()))

    def _build_menu(self, cfg, parent, parent_key, x0, y0, indent):
        y = y0
        for key, val in cfg.items():
            dotted = f"{parent_key}.{key}" if parent_key else key

            # Label
            DirectLabel(
                parent     = parent,
                text       = key,
                scale      = 0.055,
                pos        = (x0 + indent, 0, y),
                text_align = TextNode.ALeft
            )
            y -= self.row_h

            # Boolean
            if isinstance(val, bool):
                cb = DirectCheckButton(
                    parent = parent,
                    scale  = 0.05,
                    pos    = (x0 + 0.5 + indent, 0, y)
                )
                cb["indicatorValue"] = int(val)
                cb["extraArgs"]      = [dotted]
                cb["command"]        = self._on_bool_change
                self.widgets[dotted] = cb
                y -= self.row_h

            # Number
            elif isinstance(val, (int, float)):
                sl = DirectSlider(
                    parent   = parent,
                    scale    = 0.5,
                    range    = (0.0, 2.0),
                    value    = val,
                    pageSize = 0.01,
                    pos      = (x0 + 0.5 + indent, 0, y)
                )
                sl["extraArgs"] = [dotted]
                sl["command"]   = self._on_number_change
                self.widgets[dotted] = sl
                y -= self.row_h

            # String
            elif isinstance(val, str):
                entry = DirectEntry(
                    parent      = parent,
                    scale       = 0.045,
                    initialText = val,
                    pos         = (x0 + 0.5 + indent, 0, y),
                    command     = lambda txt, k=dotted: self._on_string_change(k, txt)
                )
                self.widgets[dotted] = entry
                y -= self.row_h

            # Nested dict
            elif isinstance(val, dict):
                y = self._build_menu(
                    cfg        = val,
                    parent     = parent,
                    parent_key = dotted,
                    x0         = x0,
                    y0         = y,
                    indent     = indent + 0.1
                )

            else:
                y -= self.row_h

        return y

    # —— Callback handlers ——  
    def _on_bool_change(self, key):
        w = self.widgets[key]
        self._set_setting(key, bool(w["indicatorValue"]))

    def _on_number_change(self, key):
        w      = self.widgets[key]
        cur    = w["value"]
        target = type(self._get_setting(key))
        self._set_setting(key, target(cur))

    def _on_string_change(self, key, value):
        self._set_setting(key, value)

    # —— Helpers for accessing nested dict ——  
    def _get_setting(self, dotted):
        obj = self.sf.settings
        for part in dotted.split("."):
            obj = obj[part]
        return obj

    def _set_setting(self, dotted, value):
        parts = dotted.split(".")
        obj   = self.sf.settings
        for p in parts[:-1]:
            obj = obj[p]
        obj[parts[-1]] = value

    def _on_save_close(self):
        import json
        with open(self.sf.config_path, "w") as f:
            json.dump(self.sf.settings, f, indent=4)
        self.toggle()

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.frame.show()
            self.sf.camera.set_enabled(False)
        else:
            self.frame.hide()
            self.sf.camera.set_enabled(True)
