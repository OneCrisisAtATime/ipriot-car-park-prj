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
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")

        if component is Sensor:
            self.sensors.append(component)
        elif component is Display:
            self.displays.append(component)


    def add_car(self):
        pass

    def remove_car(self):
        pass

    def update_displays(self):
        pass

print(CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY).__str__()) # test