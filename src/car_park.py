import math
from sensor import Sensor
from display import Display

DEFAULT_LOCATION = "unknown"
DEFAULT_CAPACITY = 0
DEFAULT_TEMPERATURE = 25


class CarPark:
    def __init__(self, location, capacity, temperature,disabled_capacity=None, plates=None, sensors=None, displays=None):
        self.location = location
        self.capacity = capacity
        self.temperature = temperature
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []

        self.disabled_capacity = self.total_disabled_bays() or 0

    def __str__(self):
        # return string containing car parks location and capacity
        return f'Car park at {self.location}, with {str(self.capacity)} bays total. {str(self.disabled_capacity)} of which are disability bays.'

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
        data = {"total available bays": self.available_bays, "available disabled bays": self.available_disability_bays} # , "temperature": self.temperature

        for display in self.displays:
            display.update(data)

    @property
    def available_bays(self):
            return max(0, self.capacity - len(self.plates))

    @property
    def available_disability_bays(self):
            return max(0, self.disabled_capacity - len(self.plates))

    def total_disabled_bays(self):
        """Assigns capacity of disabled parking bays based on the Australian Disability Network guidelines for accessible parking."""
        ### Source: https://australiandisabilitynetwork.org.au/DFD/dfd-06-05-car-parking.html ###

        if self.capacity < 1000: # add 1 disability park bay for 50 standard bays.
            self.disabled_capacity = math.ceil(self.capacity / 50)
            return self.disabled_capacity
        elif self.capacity >= 1000: # adds 1 additional bay for every 100 bays beyond the first 1000.
            self.disabled_capacity = math.ceil(10 + (100 / (self.capacity - 1000)))
            return self.disabled_capacity


print(CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY, DEFAULT_TEMPERATURE).displays) # test #
#CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY).
#print(f"Disabled parking capacity: {CarPark(DEFAULT_LOCATION, DEFAULT_CAPACITY, DEFAULT_TEMPERATURE).disabled_capacity}")# test 2