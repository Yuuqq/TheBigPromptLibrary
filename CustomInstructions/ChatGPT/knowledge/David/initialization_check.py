import json
import os
from pathlib import Path


SESSION_DATA_FILE = Path(__file__).with_name("session_data.json")

class InitializationCheck:
    def __init__(self, session_data_file):
        self.session_data_file = Path(session_data_file)
        self.default_mode = "Standard"
        self.trusted_mode_token = "Omicron-Omicron-Alpha-Yellow-Francis-3-7"

    def read_last_session_mode(self):
        if not self.session_data_file.exists():
            return self.default_mode

        try:
            with self.session_data_file.open("r", encoding="utf-8") as file:
                session_data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return self.default_mode

        return session_data.get("last_mode", self.default_mode)

    def check_for_trusted_mode_continuation(self, last_mode):
        if last_mode == "Trusted":
            # Placeholder for any additional checks, e.g., user authentication
            return True
        return False

    def determine_initial_mode(self):
        last_mode = self.read_last_session_mode()
        if self.check_for_trusted_mode_continuation(last_mode):
            return "Trusted"
        else:
            return self.default_mode

    def set_initial_mode(self):
        initial_mode = self.determine_initial_mode()
        # Log the initial mode for auditing
        print(f"Initialization Check: Setting mode to {initial_mode}")
        return initial_mode

def main():
    init_check = InitializationCheck(SESSION_DATA_FILE)
    return init_check.set_initial_mode()


if __name__ == "__main__":
    main()
