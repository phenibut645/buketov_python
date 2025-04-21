from __future__ import annotations
import json, datetime

record_keys = {
    "truck_id": str,
    "latitude": float,
    "longitude": float,
    "timestamp": str
}

error_file_path = "error.log"
success_file_path = "success.log"
min_sym = 60

def validate_record(record):
    try:
        timestamp = record.get("timestamp")
        for key, value in record_keys.items():
            x = record.get(key)
            if not x or not isinstance(x, value):
                return False, "Invalid or missing " + key, timestamp
        return True, "Valid", timestamp
    except Exception as e:
        return False, "Exeception", timestamp

def log_write(success, data, timestamp):
    with open(success_file_path if success else error_file_path, "+a") as f:
        cvnt = data
        if isinstance(data, str):
            cnvt = [{"message":data, "timestamp":timestamp}]
        for log in data:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            x = f"====  {now}  =======  timestamp: {log["timestamp"]}  "
            x += "=" * (min_sym - len(x))
            f.write(x + "\n")
            
            f.write("- " + log["message"] + "\n")
            f.write("=" * len(x) + "\n\n")

def get_records(filepath):
    records = None
    with open(filepath, "r") as file:
        records = json.load(file)
    return records

def process_log_file(filepath):
    records = get_records(filepath)
    prepared_logs = {
        success: [],
        failed: []
    }
    for record in records:
        valid, message, timestamp = validate_record(record)
        prepared_logs["success" if valid else "failed"].append({"message":message, "timestamp":timestamp})
    

def main():
    process_log_file("log_input.json")

if __name__ == "__main__":
    main()