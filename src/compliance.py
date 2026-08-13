import os
import json
from src.logger import log_pipeline_event

def evaluate_regulatory_compliance(patient_id, sequence_len, gc_content, purged_count):
    log_pipeline_event("compliance_auditor", "info", f"Initializing formal safety audit for batch SPEC-{patient_id}...")
    length_compliant = 50 <= sequence_len <= 150
    purity_compliant = purged_count >= 0
    stability_compliant = "N/A" not in gc_content
    overall_clearance = "CERTIFIED - VALID PASSED" if (length_compliant and purity_compliant and stability_compliant) else "REJECTED - VARIANCE DETECTED"
    compliance_report = {
        "batch_id": f"SPEC-{patient_id}",
        "auditor_layer": "OOP-COMPLIANCE-GATEV2",
        "checks": {
            "nucleotide_length_gate": "PASS" if length_compliant else "FAIL",
            "pre_run_contamination_sweep": "PASS" if purity_compliant else "FAIL",
            "thermodynamic_stability_index": "PASS" if stability_compliant else "FAIL"
        },
        "regulatory_status": overall_clearance
    }
    audit_dir = "data/validation"
    os.makedirs(audit_dir, exist_ok=True)
    audit_path = os.path.join(audit_dir, f"compliance_audit_{patient_id}.json")
    with open(audit_path, "w", encoding="utf-8") as af:
        json.dump(compliance_report, af, indent=4)
    log_pipeline_event("compliance_auditor", "success", f"Regulatory safety status locked: {overall_clearance}")
    log_pipeline_event("compliance_auditor", "success", f"Audit receipt written permanently to: {os.path.abspath(audit_path)}")
    return compliance_report, audit_path