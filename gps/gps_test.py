from gps import validate_record, get_records, log_write
import unittest

test_data_file = "log_input.json"
test_valid_record = {
        "truck_id": "TRK-001",
        "latitude": 59.437,
        "longitude": 24.7536,
        "timestamp": "2025-04-16T10:05:00Z"
        }
test_invalid_record = {
        "truck_id": "TRK-001",
        "latitude": 59.437,
        "timestamp": "2025-04-16T10:05:00Z"
}

class TestGps(unittest.TestCase):
    
    def test_records(self):
        records = get_records(test_data_file)
        self.assertIn(test_valid_record, records)

        self.assertIn({
        "truck_id": "TRK-008",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timestamp": "2025-04-16T06:15:00Z"
        }, records)

    def test_record_validation(self):
        valid, _, _ = validate_record(test_valid_record)
        self.assertTrue(valid)
        valid, _, _ = validate_record(test_invalid_record)
        self.assertFalse(valid)

    def test_log_writer(self):
        message = "Valid gg wwssdtg123"
        
        timestamp = "223:42:23"
        log_write(True, message, timestamp)
        with open("success.log", "r") as f:
            lines = f.readlines()
            if message not in lines[len(lines )- 3].rstrip():
                self.fail("not found")
            if timestamp not in lines[len(lines )- 4].rstrip():
                self.fail("not found")

        log_write(False, message, timestamp)
        with open("error.log", "r") as f:
            lines = f.readlines()
            if message not in lines[len(lines )- 3].rstrip():
                self.fail("not found")
            if timestamp not in lines[len(lines )- 4].rstrip():
                self.fail("not found")


if __name__ == "__main__":
    unittest.main()