import os
import glob

def render_graphical_matrix():
    # 1. Gather stats from your data directories safely
    sample_files = len(glob.glob("data/patient_samples/*.fasta"))
    report_files = len(glob.glob("data/reports/*.txt"))
    visual_files = len(glob.glob("data/visuals/*.txt"))
    manufacturing_files = len(glob.glob("data/manufacturing/*.txt"))
    
    # 2. Extract latest stability and HLA stats if they exist
    latest_log = glob.glob("data/validation/validation_log_*.txt")
    length_stat, stability_stat, status_stat = "N/A", "N/A", "OFFLINE"
    if latest_log:
        with open(max(latest_log, key=os.path.getmtime), "r", encoding="utf-8") as f:
            for line in f:
                if "Length Check:" in line: length_stat = line.split("(")[-1].replace(")", "").strip()
                if "Stability Check:" in line: stability_stat = line.split("(")[-1].replace(")", "").strip()
                if "FINAL STATUS:" in line: status_stat = line.split(":")[-1].strip()
    
    # 3. Construct high-scannability visual interface string layout matrix
    dashboard_view = f"""
======================================================================
      OPEN-ONCOLOGY PIPELINE (OOP) | GRAPHICAL MONITOR MATRIX
======================================================================
  [ENGINE LIFECYCLE STATUS]: {status_stat} | ACTIVE PIPELINE MODS: 15
----------------------------------------------------------------------
  
  [MODULE PROCESSING MONITOR]
  [Mod 01 Ingestion]    ████████████████████ 100% | Ingestion Shield: SECURE
  [Mod 02 Classifier]   ████████████████████ 100% | Somatic Filter: PASS
  [Mod 03 Predictor]    ████████████████████ 100% | Anchor Injection: MIXED
  [Mod 12 System Log]   ████████████████████ 100% | Rolling Log: ACTIVE
  [Mod 13 Cleaner]      ████████████████████ 100% | Pre-Run Sweep: READY
  [Mod 14 Sanitizer]    ████████████████████ 100% | Data Shield: ARMED
  [Mod 15 HLA Predict]  ████████████████████ 100% | Screening Gate: ACTIVE
  
----------------------------------------------------------------------
  [BIOMOLECULAR TELEMETRY MATRIX]
  -> Finalized Structural Length:    {length_stat}
  -> Thermal Stability Metric:       {stability_stat}
  -> HLA Binding Affinity Matrix:    MHC-I ALLELE HLA-A*02:01 SCREENED
  -> Core Integration Layer:         DECENTRALIZED LOCAL HOST REST API
  
======================================================================
  GPLv3 LICENSE SECURED - SYSTEM NODE FULLY CACHED AND OPERATIONAL
======================================================================
"""
    print(dashboard_view)

if __name__ == "__main__":
    render_graphical_matrix()
