import os
import shutil
import datetime
from src.logger import log_pipeline_event

def execute_database_backup():
    """
    Module 21: Cold Backup Management Core.
    Generates timestamped mirrors of the primary relational database.
    """
    source_db = os.path.join("data/database", "clinical_history.db")
    if not os.path.exists(source_db):
        log_pipeline_event("backup_manager", "error", "Source database node missing. Aborting backup copy lifecycle.")
        return None
    
    backup_dir = "data/backups_mirror"
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_db = os.path.join(backup_dir, f"clinical_history_backup_{timestamp}.db")
    
    try:
        shutil.copy2(source_db, dest_db)
        log_pipeline_event("backup_manager", "success", f"Persistent history mirror successfully backed up to: {os.path.abspath(dest_db)}")
        return dest_db
    except Exception as e:
        log_pipeline_event("backup_manager", "error", f"Mirror copy transaction failure: {str(e)}")
        return None

if __name__ == "__main__":
    execute_database_backup()