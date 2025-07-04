# inputs.py
from panda3d.core import InputDevice, KeyboardButton, MouseButton

class InputManager:
    def __init__(self, base, bindings_config):
        self.base = base
        self.bindings = bindings_config  # from settings.json
        self.action_state = {}
        self.devices = []
        self._setup_devices()
        self._setup_action_state()
        print("InputManager initialized with bindings:", self.bindings)

    def _setup_devices(self):
        # Detect gamepads and other input devices
        for device in base.devices.get_devices():
            if device.device_class in [InputDevice.DeviceClass.gamepad]:
                self.base.attach_input_device(device)
                self.devices.append(device)

    def _setup_action_state(self):
        for action in self.bindings:
            self.action_state[action] = False

    def update(self):
        # Called every frame to refresh action states
        for action, bindings in self.bindings.items():
            self.action_state[action] = any(
                self._is_binding_pressed(binding) for binding in bindings
            )

    def _is_binding_pressed(self, binding):
        if binding.startswith("gamepad:"):
            return self._read_gamepad(binding)
        elif binding.startswith("mouse"):
            return self.base.mouseWatcherNode.is_button_down(getattr(MouseButton, binding))
        else:
            return self.base.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key(binding.lower()))

    def _read_gamepad(self, binding):
        axis_map = {
            "left_stick_up": ("left_y", lambda v: v < -0.5),
            "left_stick_down": ("left_y", lambda v: v > 0.5),
            "left_stick_left": ("left_x", lambda v: v < -0.5),
            "left_stick_right": ("left_x", lambda v: v > 0.5),
        }
        if "stick" in binding:
            axis_name, condition = axis_map.get(binding[8:], (None, None))
            for dev in self.devices:
                axis = dev.find_axis(axis_name)
                if axis and condition(axis.value):
                    return True
        else:
            button_id = binding.split(":")[1].replace("button_", "")
            for dev in self.devices:
                if dev.find_button(button_id) and dev.find_button(button_id).pressed:
                    return True
        return False

    def is_action_pressed(self, action):
        return self.action_state.get(action, False)
