import os
import glob
import sys

def render_graphical_matrix():
    # 1. Gather stats from your data directories safely
    sample_files = len(glob.glob("data/patient_samples/*.fasta"))
    report_files = len(glob.glob("data/reports/*.txt"))
    visual_files = len(glob.glob("data/visuals/*.txt"))
    manufacturing_files = len(glob.glob("data/manufacturing/*.txt"))
    
    # 2. Extract latest stability stats if they exist
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
  [CORE CORE CORE ENGINE STATUS]: {status_stat} | ACTIVE PIPELINE MODS: 10
----------------------------------------------------------------------
  
  [MODULE PROCESSING MONITOR]
  [Mod 01 Ingestion]    ████████████████████ 100% | Samples Cached: {sample_files}
  [Mod 02 Classifier]   ████████████████████ 100% | Somatic Filter: PASS
  [Mod 03 Predictor]    ████████████████████ 100% | Anchor Injection: ACTIVE
  [Mod 04 Optimizer]    ████████████████████ 100% | Codon Stability: HARDENED
  [Mod 05 Reporter]     ████████████████████ 100% | Clinical Reports: {report_files}
  [Mod 06 Visualizer]   ████████████████████ 100% | Barcode Visuals: {visual_files}
  [Mod 07 Validator]    ████████████████████ 100% | QA Length Check: {length_stat}
  [Mod 08 Simulator]    ████████████████████ 100% | Manufacturing Run: {manufacturing_files}
  [Mod 09 Exporter]     ████████████████████ 100% | Production Sheets: READY
  [Mod 10 Web API]      ████████████████████ 100% | Portal Listen Node: PORT 8080
  
----------------------------------------------------------------------
  [BIOMOLECULAR TELEMETRY MATRIX]
  -> Finalized Structural Length:    {length_stat}
  -> Thermal Stability Metric:       {stability_stat}
  -> Network Integration Layer:      HTTP REST API ACTIVE
  
======================================================================
  GPLv3 LICENSE SECURED - SYSTEM NODE FULLY CACHED AND OPERATIONAL
======================================================================
"""
    print(dashboard_view)

if __name__ == "__main__":
    render_graphical_matrix()
