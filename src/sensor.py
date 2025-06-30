import random
from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, id_, is_active, car_park=None):
        self.id_ = id_
        self.is_active = is_active
        self.car_park = car_park

    def __str__(self):
        return f'Sensor {str(self.id_)}: {str(self.is_active)}'

    @abstractmethod
    def update_car_park(self, plate):
        pass

    def detect_vehicle(self):
        plate = self._scan_plate()
        self.update_car_park(plate)

    def _scan_plate(self):
        return 'FAKE-' + format(random.randint(0, 999), "03d")

class EntrySensor(Sensor):
    def update_car_park(self, plate):
        self.car_park.add_car(plate)
        print(f"Incoming vehicle detected. Plate: {plate}")

class ExitSensor(Sensor):
    def update_car_park(self, plate):
        self.car_park.remove_car(plate)
        print(f"Outgoing vehicle detected. Plate: {plate}")

    def _scan_plate(self):
        """Uses 'random.choice' instead of 'random.randint' to prevent bugs caused by the absence of a real plate sensor."""
        return random.choice(self.car_park.plates)
