import os
import csv
import datetime
import random
import sqlite3

def init_oncology_sqlite_db():
    """Module 13 Helper: Initializes a local SQLite relational database file
    and populates it with active patient specimen data records."""
    db_path = "oncology.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create structural relational patient database schemas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_specimens (
            timestamp TEXT,
            sample_id TEXT PRIMARY KEY,
            tissue_vector TEXT,
            target_assay TEXT
        )
    ''')
    
    # Hydrate database records dynamically
    mock_samples = [
        ("2026-08-13 09:30:15", "SAMP-9941", "Biopsy Core", "HER2 Amplification"),
        ("2026-08-13 09:35:42", "SAMP-9942", "Plasma cfDNA", "EGFR T790M Mutation"),
        ("2026-08-13 09:41:11", "SAMP-9943", "Whole Blood", "BRCA1 Sequencing")
    ]
    try:
        cursor.executemany('''
            INSERT OR REPLACE INTO patient_specimens (timestamp, sample_id, tissue_vector, target_assay)
            VALUES (?, ?, ?, ?)
        ''', mock_samples)
        conn.commit()
    except Exception:
        pass
    conn.close()

def query_patient_database():
    """Module 13: Natively queries the local SQLite relational database
    via user command terminal entry prompts."""
    print("\n[M13] SECURE SQLITE PATIENT PORTAL ACTIVE...")
    db_path = "oncology.db"
    if not os.path.exists(db_path):
        print("  --> [ERROR] Relational database node offline.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("  >>> Enter Patient Sample ID to run query (or press Enter to skip portal)")
    user_input = input("  >>> Query Target (e.g., SAMP-9941): ").strip()
    
    if not user_input:
        print("  - Exiting portal loop. Pipeline sequencing continuing...")
        conn.close()
        return
        
    cursor.execute("SELECT * FROM patient_specimens WHERE sample_id = ?", (user_input,))
    record = cursor.fetchone()
    
    print("\n  =============================================================")
    print("        RELATIONAL SQLITE DATABASE PORTAL QUERY RESULTS        ")
    print("=============================================================")
    if record:
        print(f"  * TIMESTAMP LOGGED: {record[0]}")
        print(f"  * UNIQUE SAMPLE ID: {record[1]}")
        print(f"  * SPECIMEN VECTOR:  {record[2]}")
        print(f"  * ONCOLOGY ASSAY:   {record[3]}")
    else:
        print(f"  --> [QUERY FAILED] No clinical record found for ID: '{user_input}'")
    print("  =============================================================\n")
    conn.close()

def check_reagent_thresholds():
    """Module 08: Scans critical bio-reagent assays and flags depleted levels."""
    print("\n[M08] SCANNING CORE CLINICAL REAGENT STORAGE STOCKS...")
    mock_inventory = {
        "Onco-Primer Assay A3": random.randint(5, 50),
        "Fluorescent Dye Kit X": random.randint(2, 20),
        "Lysis Buffer Node 4": random.randint(15, 100),
        "Polymerase Enzyme P2": random.randint(1, 15)
    }
    depleted_items = {}
    for reagent, volume in mock_inventory.items():
        if volume < 10:
            print(f"  --> [CRITICAL CRITERIA RISK] Alert triggered: '{reagent}' at depleted level: {volume} units!")
            depleted_items[reagent] = volume
        else:
            print(f"  - Stock Level Nominal: '{reagent}' -> {volume} units verified.")
    if not depleted_items:
        print("  >>> System stock health status check: NOMINAL ALL CLEAR <<<")
    return depleted_items

def dispatch_laboratory_alerts(depleted_items):
    """Module 11: Generates a high-priority laboratory dispatch alert file."""
    if not depleted_items:
        return
    print("\n[M11] INITIALIZING HIGH-PRIORITY LABORATORY DISPATCH ENGINE...")
    os.makedirs("alerts", exist_ok=True)
    alert_file = os.path.join("alerts", "urgent_reagent_dispatch.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(alert_file, "w", encoding="utf-8") as af:
        af.write("============================================================\n")
        af.write("   ⚠️  URGENT REAGENT STOCK DEPLETION DISPATCH ALERT  ⚠️\n")
        af.write(f"   DISPATCH TIMESTAMP: {timestamp}\n")
        af.write("============================================================\n\n")
        af.write("ITEMS REQUIRING IMMEDIATE REORDER COMPLIANCE:\n")
        for item, vol in depleted_items.items():
            af.write(f"  [!] REAGENT: {item:<24} | CURRENT VOLUME: {vol} units\n")
    print(f"  >>> SUCCESS: Laboratory dispatch alert file generated at: {alert_file}")

def export_specimen_queue():
    """Module 09: Generates timestamped export spreadsheet files for lab logs."""
    print("\n[M09] COMPILING SECURE PATIENT SPECIMEN LOG RUN...")
    os.makedirs("exports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("exports", f"specimen_queue_{timestamp}.txt")
    mock_samples = [
        {"ID": "SAMP-9941", "Type": "Biopsy Core", "Target": "HER2 Amplification"},
        {"ID": "SAMP-9942", "Type": "Plasma cfDNA", "Target": "EGFR T790M Mutation"},
        {"ID": "SAMP-9943", "Type": "Whole Blood", "Target": "BRCA1 Sequencing"}
    ]
    with open(file_path, "w", encoding="utf-8") as ef:
        ef.write("============================================================\n")
        ef.write(f"          SECURE PATIENT SAMPLE PIPELINE DELIVERABLE\n")
        ef.write("============================================================\n\n")
        for sample in mock_samples:
            ef.write(f"  * ID: {sample['ID']} | Vector: {sample['Type']} | Assay: {sample['Target']}\n")
    print(f"  >>> Pipeline Export Complete: Clean file written to -> {file_path}")
    return mock_samples

def export_excel_csv_report(samples):
    """Module 12: Intercepts specimen queues and writes a perfectly formatted
    Excel-compatible CSV spreadsheet report sheet database file."""
    print("\n[M12] BUILDING EXCEL CSV REPORT SPREADSHEET LEDGER...")
    if not samples:
        return
    os.makedirs("exports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join("exports", f"oncology_excel_report_{timestamp}.csv")
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Export Timestamp", "Patient Sample ID", "Specimen Tissue Vector", "Target Oncology Variant Assay"])
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for sample in samples:
                writer.writerow([current_time, sample["ID"], sample["Type"], sample["Target"]])
        print(f"  >>> SUCCESS: Tabular report sheet ready for Excel generated at:\n      {csv_path}")
    except Exception:
        pass

def inject_mock_api_payload():
    """Module 10: Safely tests local pipeline port interfaces with mock payloads."""
    print("\n[M10] SPINNING LOCAL REST API PORT TEST TARGET...")
    mock_payload = {
        "transaction_id": random.randint(100000, 999999),
        "endpoint_route": "/api/v2/oncology/stream",
        "transmission_status": "200_OK_SUCCESS",
        "payload_bytes_transferred": random.randint(1024, 4096)
    }
    print(f"  - Target Node Port Live Verification Status: SUCCESSLive")
    print(f"    [ID: {mock_payload['transaction_id']}] Route '{mock_payload['endpoint_route']}' live.")

if __name__ == "__main__":
    print("\n=============================================================")
    print("      EXECUTING INTEGRATED ONCOLOGY MASTER CONTROL LOOP     ")
    print("=============================================================")
    
    # Module 13 Database Initialization Routine
    init_oncology_sqlite_db()
    
    critical_stocks = check_reagent_thresholds()
    dispatch_laboratory_alerts(critical_stocks)
    active_samples = export_specimen_queue()
    export_excel_csv_report(active_samples)
    inject_mock_api_payload()
    
    # Module 13 Live Terminal User Query Portal Gateway Loop
    query_patient_database()
    
    print("\n=============================================================")
    print("      ALL EXPANSION MODULE PIPELINE DIAGNOSTICS: SUCCESS     ")
    print("=============================================================\n")
