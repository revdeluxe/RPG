# camera.py
from panda3d.core import WindowProperties, ClockObject, Vec3

class CameraController:
    def __init__(self, base, config):
        self.base        = base
        self.config      = config
        self.sensitivity = config.get("sensitivity", 0.2)
        self.invert_y    = config.get("invertYAxis", False)
        self.speed       = config.get("movementSpeed", 10)
        self.enabled     = True   # ← add enabled flag

        # alias to avoid clobbering
        self.camera_np = base.camera
        base.disable_mouse()
        self._grab_pointer()

        base.task_mgr.add(self.update, "camera_update")
        print("CameraController initialized with settings:")
        print(f"- Sensitivity: {self.sensitivity}")
        print(f"- Invert Y: {self.invert_y}")
        print(f"- Movement Speed: {self.speed}")
        print("CameraController is enabled:", self.enabled)

    def _grab_pointer(self):
        props = WindowProperties()
        # hide the cursor
        props.setCursorHidden(True)
        # lock the pointer to the window (or use M_relative for pure delta mode)
        props.setMouseMode(WindowProperties.M_confined)
        # make sure the window is frontmost and bounds re‐registered
        props.setForeground(True)
        props.setOrigin(-2, -2)
        # *one* requestProperties call
        self.base.win.requestProperties(props)

        # debug print to verify
        m = self.base.win.getProperties().getMouseMode()
        print("🎯 Mouse mode is now:", "M_confined" if m==WindowProperties.M_confined else m)

    def _release_pointer(self):
        props = WindowProperties()
        props.set_cursor_hidden(False)
        props.set_mouse_mode(WindowProperties.M_absolute)
        self.base.win.request_properties(props)

    def set_enabled(self, flag: bool):
        self.enabled = flag
        if flag:
            self._grab_pointer()
        else:
            self._release_pointer()

    def update(self, task):
        if not self.enabled:
            return task.cont

        dt = ClockObject.get_global_clock().get_dt()
        mw = self.base.mouseWatcherNode

        # 1) Read raw input
        inp = Vec3(0, 0, 0)
        if mw.is_button_down("w"): inp.y += 1
        if mw.is_button_down("s"): inp.y -= 1
        if mw.is_button_down("a"): inp.x -= 1
        if mw.is_button_down("d"): inp.x += 1

        # 2) Transform into camera's local XY plane
        if inp.length_squared() > 0:
            # get camera's orientation in world space
            quat = self.camera_np.get_quat(self.base.render)
            # transform input vector by camera rotation
            move_vec = quat.xform(inp)
            # ignore vertical component so you stay level
            move_vec.set_z(0)
            move_vec.normalize()
            move_vec *= self.speed * dt
            # apply movement
            self.camera_np.set_pos(self.camera_np.get_pos() + move_vec)

        # in update():
        win = self.base.win
        w, h = win.getXSize(), win.getYSize()
        cx, cy = w//2, h//2

        ptr = win.get_pointer(0)
        dx = ptr.get_x() - cx
        dy = cy - ptr.get_y()

        # apply heading as before
        new_h = self.camera_np.get_h() - dx * self.sensitivity
        self.camera_np.set_h(new_h)

        # apply pitch – multiply by -1 if invert_y to swap direction
        sign = -1 if self.invert_y else 1
        new_p = self.camera_np.get_p() + dy * self.sensitivity * sign
        self.camera_np.set_p(max(-90, min(90, new_p)))

        # re‐center
        win.movePointer(0, cx, cy)

        return task.cont

def clamp(v, mn, mx): return max(mn, min(mx, v))
