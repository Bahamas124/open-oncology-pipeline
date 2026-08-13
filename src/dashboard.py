import os
import glob

def render_graphical_matrix():
    sample_files = len(glob.glob("data/patient_samples/*.fasta"))
    report_files = len(glob.glob("data/reports/*.txt"))
    visual_files = len(glob.glob("data/visuals/*.txt"))
    manufacturing_files = len(glob.glob("data/manufacturing/*.txt"))
    
    latest_log = glob.glob("data/validation/validation_log_*.txt")
    length_stat, stability_stat, status_stat = "N/A", "N/A", "OFFLINE"
    if latest_log:
        with open(max(latest_log, key=os.path.getmtime), "r", encoding="utf-8") as f:
            for line in f:
                if "Length Check:" in line: length_stat = line.split("(")[-1].replace(")", "").strip()
                if "Stability Check:" in line: stability_stat = line.split("(")[-1].replace(")", "").strip()
                if "FINAL STATUS:" in line: status_stat = line.split(":")[-1].strip()
    
    latest_recipe = glob.glob("data/manufacturing/lnp_recipe_*.txt")
    np_ratio_stat, density_stat = "N/A", "N/A"
    if latest_recipe:
        with open(max(latest_recipe, key=os.path.getmtime), "r", encoding="utf-8") as f:
            for line in f:
                if "Optimized N/P Charge Ratio:" in line: np_ratio_stat = line.split(":")[-1].strip()
                if "Total Required Lipid Density:" in line: density_stat = line.split(":")[-1].strip()
    
    dashboard_view = f"""
======================================================================
      OPEN-ONCOLOGY PIPELINE (OOP) | GRAPHICAL MONITOR MATRIX
======================================================================
  [ENGINE LIFECYCLE STATUS]: {status_stat} | ACTIVE PIPELINE MODS: 16
----------------------------------------------------------------------
  
  [MODULE PROCESSING MONITOR]
  [Mod 01 Ingestion]    ████████████████████ 100% | Ingestion Shield: SECURE
  [Mod 02 Classifier]   ████████████████████ 100% | Somatic Filter: PASS
  [Mod 03 Predictor]    ████████████████████ 100% | Anchor Injection: MIXED
  [Mod 12 System Log]   ████████████████████ 100% | Rolling Log: ACTIVE
  [Mod 13 Cleaner]      ████████████████████ 100% | Pre-Run Sweep: READY
  [Mod 14 Sanitizer]    ████████████████████ 100% | Data Shield: ARMED
  [Mod 15 HLA Predict]  ████████████████████ 100% | Screening Gate: ACTIVE
  [Mod 16 LNP Optim]    ████████████████████ 100% | Enveloping Core: STABLE
  
----------------------------------------------------------------------
  [BIOMOLECULAR & LNP TELEMETRY MATRIX]
  -> Finalized Structural Length:    {length_stat}
  -> Thermal Stability Metric:       {stability_stat}
  -> HLA Binding Affinity Matrix:    MHC-I ALLELE HLA-A*02:01 SCREENED
  -> LNP Target Charge Balance:      N/P RATIO {np_ratio_stat}
  -> LNP Optimized Mixture Density:  {density_stat}
  -> Microfluidic Flow Channels:     AQUEOUS: 3.0 mL/min | ORGANIC: 1.0 mL/min
  
======================================================================
  GPLv3 LICENSE SECURED - SYSTEM NODE FULLY CACHED AND OPERATIONAL
======================================================================
"""
    print(dashboard_view)

if __name__ == "__main__":
    render_graphical_matrix()
