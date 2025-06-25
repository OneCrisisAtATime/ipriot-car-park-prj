from sensor import Sensor
from display import Display

DEFAULT_LOCATION = "unknown"
DEFAULT_CAPACITY = 0


class CarPark:
    def __init__(self, locations, capacity, plates=None, sensors=None, displays=None):
        self.locations = locations
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []

    def __str__(self):
        # return string containing car parks location and capacity
        return f'Car park at {self.locations}, with {str(self.capacity)} bays.'

    def register(self, component):
        """Registers components of a car park"""
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")

        if component is Sensor:
            self.sensors.append(component)
        elif component is Display:
            self.displays.append(component)


    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()

    def remove_car(self, plate):
        self.plates.remove(plate)
        self.update_displays()

    def update_displays(self):
        data = {"total available bays": self.available_bays, "temperature": 25} #, "available disabled bays": self.available_disabled_bays

        for display in self.displays:
            display.update(data)

    @property
    def available_bays(self):
        if len(self.plates) >= self.capacity:
            return 0
        elif len(self.plates) < self.capacity:
            return self.capacity - len(self.plates)

print(CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY).__str__()) # test