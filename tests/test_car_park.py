import unittest
import json
from pathlib import Path
from car_park import CarPark

class TestCarPark(unittest.TestCase):
      def setUp(self):
         self.car_park = CarPark("123 Example Street", 100, 30)
         self.path = Path("new_log.txt")

      def test_car_park_initialized_with_all_attributes(self):
         self.assertIsInstance(self.car_park, CarPark)
         self.assertEqual(self.car_park.location, "123 Example Street")
         self.assertEqual(self.car_park.capacity, 100)
         self.assertEqual(self.car_park.temperature, 30)
         self.assertEqual(self.car_park.plates, [])
         self.assertEqual(self.car_park.displays, [])
         self.assertEqual(self.car_park.available_bays, 100)
         self.assertEqual(self.car_park.log_file, Path("log.txt"))

      def test_add_car(self):
         self.car_park.add_car("FAKE-001")
         self.assertEqual(self.car_park.plates, ["FAKE-001"])
         self.assertEqual(self.car_park.available_bays, 99)

      def test_remove_car(self):
         self.car_park.add_car("FAKE-001")
         self.car_park.remove_car("FAKE-001")
         self.assertEqual(self.car_park.plates, [])
         self.assertEqual(self.car_park.available_bays, 100)

      def test_overfill_the_car_park(self):
         for i in range(100):
            self.car_park.add_car(f"FAKE-{i}")
         self.assertEqual(self.car_park.available_bays, 0)
         self.car_park.add_car("FAKE-100")

         # Overfilling the car park should not change the number of available bays
         self.assertEqual(self.car_park.available_bays, 0)

         # Removing a car from an overfilled car park should not change the number of available bays
         self.car_park.remove_car("FAKE-100")
         self.assertEqual(self.car_park.available_bays, 0)

      def test_removing_a_car_that_does_not_exist(self):
         with self.assertRaises(ValueError):
            self.car_park.remove_car("NO-1")

      def test_register_raises_type_error(self):
         with self.assertRaises(TypeError):
            self.car_park.register("Not a Sensor or Display")

      def test_log_file_created(self):
         new_carpark = CarPark("123 Example Street", 100, 30, log_file = "new_log.txt")
         self.assertTrue(self.path.exists())

      def tearDown(self):
         self.path.unlink(missing_ok=True)

      def test_car_logged_when_entering(self):
         new_carpark = CarPark("123 Example Street", 100, 30, log_file = "new_log.txt") # TODO: change this to use a class attribute or new instance variable
         self.car_park.add_car("NEW-001")
         with self.car_park.log_file.open() as f:
            last_line = f.readlines()[+1]
         self.assertIn("NEW-001", last_line) # check plate entered
         self.assertIn("entered", last_line) # check description
         self.assertIn("\n", last_line) # check entry has a new line

      def test_car_logged_when_exiting(self):
         new_carpark = CarPark("123 Example Street", 100, 30, log_file = "new_log.txt") # TODO: change this to use a class attribute or new instance variable
         self.car_park.add_car("NEW-001")
         self.car_park.remove_car("NEW-001")
         with self.car_park.log_file.open() as f:
            last_line = f.readlines()[-1]
         self.assertIn("NEW-001", last_line) # check plate exited
         self.assertIn("exited", last_line) # check description
         self.assertIn("\n", last_line) # check entry has a new line

      def test_car_park_write_to_config_file(self):
         config_path = Path("config.json")
         self.car_park.write_config(config_path)

         with config_path.open() as f:
            config_data = json.load(f)

         self.assertEqual(self.car_park.location, config_data["location"])
         self.assertEqual(self.car_park.capacity, config_data["capacity"])
         self.assertEqual(self.car_park.temperature, config_data["temperature"])
         self.assertEqual(f'{self.car_park.log_file}', config_data["log_file"])

         config_path.unlink()  # Clean up

      def test_car_park_initialized_from_config_file(self):
         config_data = {
            "location": "456 Main Street",
            "capacity": 200,
            "temperature": 25,
            "log_file": "test_log.txt"
         }

         config_path = Path("config.json")
         with config_path.open("w") as f:
            json.dump(config_data, f)

         car_park = CarPark.from_config(config_path)

         self.assertEqual(car_park.location, config_data["location"])
         self.assertEqual(car_park.capacity, config_data["capacity"])
         self.assertEqual(car_park.temperature, config_data["temperature"])
         self.assertEqual(car_park.log_file.name, f'{config_data["log_file"]}')

         config_path.unlink()  # Clean up

if __name__ == "__main__":
   unittest.main()