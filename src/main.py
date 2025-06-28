from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display
import random

def main():
    carpark = CarPark("Moondalup", 100, 25, log_file="moondalup.txt")

    entry_sensor = EntrySensor(1, True, carpark)
    exit_sensor = ExitSensor(2, True, carpark)

    display = Display(1, carpark,"welcome to Moondalup", True)
    print(display)

    for c in range(10):
        entry_sensor.update_car_park(carpark.generate_plate())

    for c in range(2):
        exit_sensor.update_car_park(random.choice(carpark.plates))

if __name__ == "__main__":
    main()