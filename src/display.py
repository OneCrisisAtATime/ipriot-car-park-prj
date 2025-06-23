DEFAULT_MESSAGE = ""
DEFAULT_IS_ON = False

class Display:

    def __init__(self, id_=None, message="", is_on=False, car_park=None):
        self.id_ = id_
        self.message = message
        self.is_on = is_on
        self.car_park = car_park

    def __str__(self):
        return f'Display {str(self.id_)}: {self.message}'

print(Display(2,"Welcome stranger!")) # test