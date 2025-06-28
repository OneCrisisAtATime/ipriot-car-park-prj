import math
from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime
import json
import random
import string

DEFAULT_LOCATION = "unknown"
DEFAULT_CAPACITY = 1200
DEFAULT_TEMPERATURE = 25

class CarPark:
    def __init__(self, location, capacity, temperature, plates=None, sensors=None, displays=None, log_file=Path('log_file.txt'), config_file=Path("config.json")):
        self.location = location
        self.capacity = capacity
        self.temperature = temperature
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.disabled_capacity = self.calculate_disabled_bays or 0

        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        # create the file if it doesn't exist:
        self.log_file.touch(exist_ok=True)

        self.config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        self.log_file.touch(exist_ok=True)

    def __str__(self):
        # return string containing car parks location and capacity
        return f'Car park at {self.location}, with {str(self.capacity)} bays total. Including {str(self.disabled_capacity)} disability bays. And has a internal temperature of {str(self.temperature)} Celsius.'

    def register(self, component):
        """Registers components of a car park"""
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")

        if component is Sensor:
            self.sensors.append(component)
        elif component is Display:
            self.displays.append(component)

    def _log_car_activity(self, plate, action):
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now()}\n")

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    def remove_car(self, plate):
        self.plates.remove(plate)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def update_displays(self):
        data = {"total available bays": self.available_bays, "available disabled bays": self.available_disability_bays, "temperature": self.temperature}

        for display in self.displays:
            display.update(data)

    def generate_plate(self):
        """Randomly generates a 6-character number plate."""
        chars = string.ascii_uppercase + string.digits  # creates a pool of uppercase letters and numbers
        first_part = ''.join(random.choices(chars, k=3))
        second_part = ''.join(random.choices(chars, k=3))
        return f"{first_part}-{second_part}"

    @property
    def available_bays(self):
            return max(0, self.capacity - len(self.plates))

    @property
    def available_disability_bays(self):
            return max(0, self.disabled_capacity - len(self.plates))

    @property
    def calculate_disabled_bays(self):
        """Assigns capacity of disabled parking bays based on the Australian Disability Network guidelines for accessible parking."""
        ### Source: https://australiandisabilitynetwork.org.au/DFD/dfd-06-05-car-parking.html ###

        if self.capacity < 1000:
            return math.ceil(self.capacity / 50)
        return math.ceil(10 + (100 / (self.capacity - 1000)))

    def write_config(self, config_file):
        with open(config_file, "w") as f:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "temperature": self.temperature,
                       "log_file": str(self.log_file)}, f)

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], config["temperature"], log_file=config["log_file"])

#print(CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY, DEFAULT_TEMPERATURE).displays) # test #
#CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY).
#print(f"Disabled parking capacity: {CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY, DEFAULT_TEMPERATURE).disabled_capacity}")# test 2