
class Display:

    def __init__(self, id_, car_park, message="", is_on=False, ):
        self.id_ = id_
        self.message = message
        self.is_on = is_on
        self.car_park = car_park

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return f'Display {str(self.id_)}: {self.message}'


#print(Display(2, "random park","Welcome to the car park.")) # test