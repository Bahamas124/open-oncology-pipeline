import os
import glob
from src.fetch_clean_data import auto_fetch_prostate_cancer_data
from src.ingestion import ingest_genomic_file
from src.classifier import isolate_live_somatic_mutations
from src.predictor import run_live_ai_judge_and_blender
from src.optimizer import weld_live_dual_action_mrna
from src.reporter import generate_clinical_report
from src.visualizer import render_patient_target_barcode
from src.validator import validate_mrna_stability
from src.simulator import run_manufacturing_simulation
from src.exporter import export_production_spec_sheet # Import Module 9

def execute_live_data_pipeline():
    print("\n" + "="*60)
    print("       OPEN-ONCOLOGY PIPELINE (OOP): FULL DUAL-ACTION RUN     ")
    print("="*60)
    if not auto_fetch_prostate_cancer_data():
        print("[Pipeline Error] Database synchronization failed.")
        return
    target_folder = "data/patient_samples"
    downloaded_files = glob.glob(os.path.join(target_folder, "ncbi_prostate_variant_*.fasta"))
    if not downloaded_files:
        print("[Pipeline Error] Local asset cache empty.")
        return
        
    sample_file_path = downloaded_files
    
    record_id, raw_sequence = ingest_genomic_file(sample_file_path)
    print("-"*60)
    verified_cancer_mutations = isolate_live_somatic_mutations(record_id, raw_sequence)
    print("-"*60)
    blended_target_manifest = run_live_ai_judge_and_blender(verified_cancer_mutations)
    print("-"*60)
    final_output_file = weld_live_dual_action_mrna(blended_target_manifest, record_id)
    print("-"*60)
    final_report_file = generate_clinical_report(record_id, raw_sequence, blended_target_manifest, final_output_file)
    print("-"*60)
    final_visual_file = render_patient_target_barcode(record_id, blended_target_manifest)
    print("-"*60)
    
    validation_passed = validate_mrna_stability(record_id, final_output_file, blended_target_manifest)
    print("-"*60)
    
    sim_successful = run_manufacturing_simulation(record_id, validation_passed, blended_target_manifest)
    print("-"*60)
    
    # Trigger Module 9: Compile Final Production Specification Sheet
    final_spec_file = export_production_spec_sheet(record_id, final_output_file, validation_passed)
    
    print("="*60)
    print("               PIPELINE LIFECYCLE COMPLETION SUCCESS           ")
    print("="*60)
    print(f"-> Source Input:      Real NCBI Asset [{record_id}]")
    print(f"-> Vaccine Blueprint: {os.path.basename(final_output_file)}")
    print(f"-> Manufacturing Sim: {'SIMULATION READY - COST MODEL OPTIMIZED' if sim_successful else 'FAILED'}")
    print(f"-> Production Spec:   {os.path.basename(final_spec_file)}")
    print(f"-> Spec Sheet Loc:    {os.path.abspath(final_spec_file)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    execute_live_data_pipeline()
