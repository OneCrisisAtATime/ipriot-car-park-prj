

class Sensor:
    def __init__(self, id_, is_active, car_park=None):
        self.id_ = id_
        self.is_active = is_active
        self.car_park = car_park

    def __str__(self):
        return f'Sensor {str(self.id_)}: {str(self.is_active)}'

class EntrySensor(Sensor):
    pass

class ExitSensor(Sensor):
    pass

print(Sensor(5, True).__str__()) # test