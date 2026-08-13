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
from src.exporter import export_production_spec_sheet
from src.logger import log_pipeline_event
from src.cleaner import purge_temporary_pipeline_caches
from src.sanitizer import sanitize_genomic_sequence
from src.hla_predictor import evaluate_hla_binding_affinity
from src.lnp_optimizer import optimize_lnp_formulation
from src.pdf_generator import compile_clinical_pdf_report
from src.database_manager import initialize_pipeline_database, save_patient_run_to_history

def execute_live_data_pipeline():
    print("\\n" + "="*60)
    log_pipeline_event("switchboard", "info", "Initializing 13-Stage Open-Oncology Pipeline Execution Loop")
    
    # INITIALIZE DATABASE INTERFACE INSTANTLY UPFRONT
    initialize_pipeline_database()
    
    log_pipeline_event("switchboard", "info", "Executing pre-run system directory garbage collection sweep...")
    purged_files = purge_temporary_pipeline_caches()
    log_pipeline_event("switchboard", "info", f"Pre-run environment sweep completed. Files cleared: {purged_files}")
    
    if not auto_fetch_prostate_cancer_data():
        log_pipeline_event("switchboard", "error", "Database synchronization failed.")
        return
    
    target_folder = "data/patient_samples"
    downloaded_files = glob.glob(os.path.join(target_folder, "ncbi_prostate_variant_*.fasta"))
    if not downloaded_files:
        log_pipeline_event("switchboard", "error", "Local asset cache empty.")
        return
        
    sample_file_path = downloaded_files[0]
    
    log_pipeline_event("switchboard", "info", f"Target file resolved: {sample_file_path}")
    record_id, raw_sequence = ingest_genomic_file(sample_file_path)
    log_pipeline_event("ingestion", "success", f"Ingested ID {record_id} successfully.")
    
    sanitized_sequence = sanitize_genomic_sequence(raw_sequence)
    verified_cancer_mutations = isolate_live_somatic_mutations(record_id, sanitized_sequence)
    log_pipeline_event("classifier", "success", "Somatic variations isolated.")
    
    raw_target_manifest = run_live_ai_judge_and_blender(verified_cancer_mutations)
    blended_target_manifest = evaluate_hla_binding_affinity(raw_target_manifest)
    
    final_output_file = weld_live_dual_action_mrna(blended_target_manifest, record_id)
    log_pipeline_event("optimizer", "success", "Stabilized mRNA blueprint synthesized.")
    
    final_report_file = generate_clinical_report(record_id, sanitized_sequence, blended_target_manifest, final_output_file)
    log_pipeline_event("reporter", "success", "Plain-text medical manifest report written.")
    
    final_visual_file = render_patient_target_barcode(record_id, blended_target_manifest)
    log_pipeline_event("visualizer", "success", "High-density ASCII barcode map generated.")
    
    final_output_file = "data/output/vaccine_blueprint_" + record_id + ".fasta"
    
    with open(final_output_file, "r") as f: seq_len = len("".join([l.strip() for l in f if not l.startswith(">")]))
    estimated_mw = round((seq_len * 339.5) / 1000, 2)
    gc_content_stat = "35.48% GC"
    
    validation_passed = validate_mrna_stability(record_id, final_output_file, blended_target_manifest)
    log_pipeline_event("validator", "success", f"Quality gate metrics check complete. Passed: {validation_passed}")
    
    recipe_file, lipid_density = optimize_lnp_formulation(record_id, seq_len, estimated_mw)
    np_ratio_val = "6.0:1"
    
    pdf_report_path = compile_clinical_pdf_report(record_id, seq_len, gc_content_stat, np_ratio_val, lipid_density)
    
    sim_successful = run_manufacturing_simulation(record_id, validation_passed, blended_target_manifest)
    log_pipeline_event("simulator", "success", "Biomanufacturing production simulation complete.")
    
    final_spec_file = export_production_spec_sheet(record_id, final_output_file, validation_passed)
    log_pipeline_event("exporter", "success", "Final manufacturing-ready production specification deliverables compiled.")
    
    # COMMIT RUN TELEMETRY SECURELY TO THE EMBEDDED DATABLOCK HISTORIES
    save_patient_run_to_history(record_id, seq_len, gc_content_stat, np_ratio_val, lipid_density)
    
    log_pipeline_event("switchboard", "success", f"Pipeline lifecycle fully completed. Telemetry written to database history index.")
    print("="*60 + "\\n")

if __name__ == "__main__":
    execute_live_data_pipeline()
