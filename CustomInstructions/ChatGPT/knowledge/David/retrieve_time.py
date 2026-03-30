
from pathlib import Path


TIME_TRACKER_FILE = Path(__file__).with_name("time_tracker.txt")


def retrieve_time():
    if not TIME_TRACKER_FILE.exists():
        return ""

    with TIME_TRACKER_FILE.open('r', encoding='utf-8') as file:
        last_updated_time = file.read().strip()
    return last_updated_time


if __name__ == "__main__":
    print(retrieve_time())
