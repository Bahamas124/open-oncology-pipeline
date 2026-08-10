import os
import glob
from src.logger import log_pipeline_event

def purge_temporary_pipeline_caches():
    """
    Stage 13: Automation Maintenance Cleaner.
    Cleans out intermediate data track files, temporary simulation logs,
    and older generated files to keep the local workspace pristine.
    """
    log_pipeline_event("cleaner", "info", "Initializing system workspace garbage collection...")
    
    # Define the cleanup target directory paths
    target_paths = [
        "data/patient_samples/ncbi_prostate_variant_*.fasta",
        "data/validation/validation_log_*.txt",
        "data/manufacturing/simulation_manifest_*.txt"
    ]
    
    purged_count = 0
    for path_pattern in target_paths:
        matching_files = glob.glob(path_pattern)
        for target_file in matching_files:
            try:
                os.remove(target_file)
                purged_count += 1
            except Exception as e:
                log_pipeline_event("cleaner", "error", f"Failed to remove cache asset {target_file}: {str(e)}")
                
    log_pipeline_event("cleaner", "success", f"Workspace clean complete. Total obsolete files purged: {purged_count}")
    return purged_count

if __name__ == "__main__":
    purge_temporary_pipeline_caches()
