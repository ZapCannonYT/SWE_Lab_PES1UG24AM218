"""Smart home device controller.

Adds devices to rooms, switches them on and off, sets the thermostat within
a safe range, lists devices by room, reports power use and saves the home
state to a JSON file.
"""
import json
import os
import subprocess  # nosec B404 - fixed argv list only, see run_scene

# Bind to loopback only; expose on the LAN deliberately via HUB_HOST if needed.
HUB_HOST = os.environ.get("HUB_HOST", "127.0.0.1")
HUB_PORT = 8080
POWER_USAGE = {"light" : 10, "fan": 60, "thermostat": 1500, "tv": 120}
# Secret comes from the environment, never from source control.
HUB_PASSWORD = os.environ.get("HUB_PASSWORD", "")
SCENES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
MIN_TEMP = 16
MAX_TEMP = 30
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device. Each device gets its own settings dict."""
    devices[device_name] = {"kind": kind, "room": room, "on": False,
                            "settings": {} if settings is None else settings}


def toggle_device(device_name):
    """Flip a device on/off and return its new state, or None if unknown."""
    if device_name not in devices:
        print("Device not found:", device_name)
        return None
    devices[device_name]["on"] = not devices[device_name]["on"]
    return devices[device_name]["on"]


def set_temperature(device_name, value):
    """Set a thermostat's target, clamped to the safe range.

    Returns True on success, False if the device is unknown or is not a
    thermostat.
    """
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, MIN_TEMP), MAX_TEMP)
    return True


def devices_in_room(room):
    """Return the names of all devices in the given room."""
    return [name for name, info in devices.items() if info["room"] == room]


def power_usage():
    """Return the total power draw (W) of all devices that are on."""
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)

def save_state(file_name="home_state.json"):
    """Write the current device state to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as state_file:
        json.dump(devices, state_file, indent=2)


def hub_address():
    """Return the hub address as host:port."""
    return HUB_HOST + ":" + str(HUB_PORT)


def run_scene(scene_script):
    """Run a scene script from SCENES_DIR and return its exit code.

    Helper kept for the lab: not called by the demo. Only a bare file name
    inside SCENES_DIR is accepted (no paths, no "..").
    """
    script_path = os.path.join(SCENES_DIR, scene_script)
    if os.path.basename(scene_script) != scene_script or \
            not os.path.isfile(script_path):
        raise ValueError("Unknown scene script: " + scene_script)
    # Fixed argv list, no shell: user input can't inject extra commands.
    return subprocess.call(["/bin/bash", script_path])  # nosec B603


def main():
    """Run a short demonstration of the controller."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())# for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    print("Devices on:", [name for name, info in devices.items() if info["on"]])
    save_state()


if __name__ == "__main__":
    main()
