DEFAULT_LOCATION = "unknown"
DEFAULT_CAPACITY = 0


class CarPark:
    def __init__(self, locations=DEFAULT_LOCATION, capacity=DEFAULT_CAPACITY, plates=None, sensors=None, displays=None):
        self.locations = locations
        self.capacity = capacity
        self.plates = plates
        self.sensors = sensors or []
        self.displays = displays or []



    def __str__(self):
        # return string containing car parks location and capacity
        return "Car park at " + self.locations + ", with " + str(self.capacity) + " bays."


print(CarPark())