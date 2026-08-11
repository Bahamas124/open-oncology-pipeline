import os
from src.logger import log_pipeline_event

def sanitize_genomic_sequence(raw_sequence):
    """
    Stage 14: Data Input Sanitizer Shield.
    Validates and cleans input sequence tracking streams to prevent
    malformed data injections from breaching core logic layers.
    """
    log_pipeline_event("sanitizer", "info", "Initializing sequence data stream integrity scan...")
    
    # Define valid upper-case nucleotide string layouts
    valid_bases = set("ACGTU\\n\\r ")
    
    # Check for invalid characters
    cleaned_sequence = ""
    invalid_characters_found = 0
    
    for char in raw_sequence:
        if char.upper() in valid_bases:
            cleaned_sequence += char
        else:
            invalid_characters_found += 1
            
    if invalid_characters_found > 0:
        log_pipeline_event("sanitizer", "warning", f"Stripped {invalid_characters_found} malformed characters from asset track.")
    else:
        log_pipeline_event("sanitizer", "success", "Genomic data stream validation secure. Zero anomalies found.")
        
    return cleaned_sequence.upper()
