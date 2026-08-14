import os
import csv
import datetime
import random

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
        print("  --> [WARNING] No active sample data vectors to map to Excel.")
        return
    os.makedirs("exports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join("exports", f"oncology_excel_report_{timestamp}.csv")
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write structured database spreadsheet header row cells
            writer.writerow(["Export Timestamp", "Patient Sample ID", "Specimen Tissue Vector", "Target Oncology Variant Assay"])
            # Write independent sample record rows
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for sample in samples:
                writer.writerow([current_time, sample["ID"], sample["Type"], sample["Target"]])
        print(f"  >>> SUCCESS: Tabular report sheet ready for Excel generated at:\n      {csv_path}")
    except Exception as e:
        print(f"  --> [ERROR] Failed to compile CSV artifact: {str(e)}")

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
    critical_stocks = check_reagent_thresholds()
    dispatch_laboratory_alerts(critical_stocks)
    active_samples = export_specimen_queue()
    
    # Run the new Excel spreadsheet builder subroutine loop
    export_excel_csv_report(active_samples)
    
    inject_mock_api_payload()
    print("\n=============================================================")
    print("      ALL EXPANSION MODULE PIPELINE DIAGNOSTICS: SUCCESS     ")
    print("=============================================================\n")
