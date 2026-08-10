import os
import datetime

def log_pipeline_event(module_name, event_type, message):
    """
    Stage 12: Unified Core System Logger.
    Writes standardized, timestamped audit entries to both the console
    and a rolling historical log file on disk.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{module_name.upper()}] [{event_type.upper()}] {message}"
    
    # Print cleanly to the terminal screen
    print(log_entry)
    
    # Save permanently to disk
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "pipeline_audit.log")
    
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry + "\n")
    return log_path
