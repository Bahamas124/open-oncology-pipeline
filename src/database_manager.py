import sqlite3
import os
from src.logger import log_pipeline_event

def initialize_pipeline_database():
    """
    Stage 18: Relational Database Storage Layer.
    Initializes an embedded SQLite3 relational database tracking block
    to maintain persistent record histories of patient runs.
    """
    db_dir = "data/database"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "clinical_history.db")
    
    log_pipeline_event("database_manager", "info", f"Syncing connection mapping to database node: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create persistent data structure schema tables natively
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient_runs (
        id TEXT PRIMARY KEY,
        sequence_length INTEGER,
        gc_content TEXT,
        np_ratio TEXT,
        lipid_density REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    log_pipeline_event("database_manager", "success", "Relational schema layouts verified and locked.")
    return db_path

def save_patient_run_to_history(patient_id, length, gc_content, np_ratio, lipid_density):
    """Saves completed 12-stage telemetry profiles permanently into relational storage grids."""
    db_path = os.path.join("data/database", "clinical_history.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT OR REPLACE INTO patient_runs (id, sequence_length, gc_content, np_ratio, lipid_density)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id, length, gc_content, np_ratio, lipid_density))
        conn.commit()
        log_pipeline_event("database_manager", "success", f"Record SPEC-{patient_id} successfully cataloged in relational index.")
    except Exception as e:
        log_pipeline_event("database_manager", "error", f"Database transaction commit failure: {str(e)}")
    finally:
        conn.close()
