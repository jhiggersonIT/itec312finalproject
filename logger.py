# Hogwarts Logger
# --------------------------
# This script logs events and errors for the Hogwarts Management System.
# Features: Logs student, teacher, and course actions; tracks errors in JSON format.

import json
import os
from datetime import datetime

LOG_FILE = "hogwarts_log.json"

def log_event(event_type, details):
    log_entry = {
        "Timestamp": datetime.now().isoformat(),
        "Event_Type": event_type,
        "Details": details
    }
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([log_entry], f, indent=4)
    else:
        with open(LOG_FILE, 'r+') as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)


ERROR_LOG_FILE = "hogwarts_error_log.json"

def log_error(error_message, details=None):
    error_entry = {
        "Timestamp": datetime.now().isoformat(),
        "Error_Message": error_message,
        "Details": details if details else {}
    }
    try:
        if not os.path.exists(ERROR_LOG_FILE):
            with open(ERROR_LOG_FILE, 'w') as f:
                json.dump([error_entry], f, indent=4)
        else:
            with open(ERROR_LOG_FILE, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(error_entry)
                f.seek(0)
                json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Failed to log error: {e}")
