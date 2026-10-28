"""Smart home device controller.

Adds devices to rooms, switches them on and off, sets the thermostat within
a safe range, lists devices by room, reports power use and saves the home
state to a JSON file.
"""
import json
import subprocess

HUB_HOST = "0.0.0.0"
HUB_PORT = 8080
POWER_USAGE = {"light" : 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = "smarthome-demo"
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
    """Run a scene script from the scenes folder and return its exit code.

    Helper kept for the lab: not called by the demo.
    """
    return subprocess.call("bash scenes/" + scene_script, shell=True)


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
