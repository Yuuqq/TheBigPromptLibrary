import datetime
from pathlib import Path


TIME_TRACKER_FILE = Path(__file__).with_name("time_tracker.txt")

def update_time():
    current_time = datetime.datetime.now().isoformat()
    with TIME_TRACKER_FILE.open('w', encoding='utf-8') as file:
        file.write(current_time)
    return current_time


if __name__ == "__main__":
    print(update_time())
