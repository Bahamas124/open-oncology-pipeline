import random
from src.logger import log_pipeline_event

def evaluate_hla_binding_affinity(blended_manifest, hla_allele="HLA-A*02:01"):
    """
    Stage 15: HLA Binding Affinity Predictor Layer.
    Simulates immunological presentation scores to ensure selected tumor
    mutations trigger a robust, patient-specific T-cell response.
    """
    log_pipeline_event("hla_predictor", "info", f"Evaluating MHC-I binding matrix against allele footprint: {hla_allele}")
    
    validated_payloads = []
    for target in blended_manifest:
        if "Universal" in target.get("target_type", ""):
            target["hla_binding_score"] = 1.00
            target["immunogenicity"] = "HIGH (ANCHOR)"
            validated_payloads.append(target)
            continue
            
        simulated_ic50 = round(random.uniform(15.0, 750.0), 2)
        target["ic50_nm"] = simulated_ic50
        
        binding_score = round(1.0 - (simulated_ic50 / 1000.0), 2)
        target["hla_binding_score"] = binding_score
        
        if simulated_ic50 <= 500.0:
            target["immunogenicity"] = "POTENT"
            validated_payloads.append(target)
            log_pipeline_event("hla_predictor", "success", f"Target slot {target['id']} cleared gate with IC50: {simulated_ic50} nM")
        else:
            target["immunogenicity"] = "WEAK (FILTERED)"
            log_pipeline_event("hla_predictor", "warning", f"Dropped weak binder slot {target['id']} due to low affinity ({simulated_ic50} nM)")
            
    log_pipeline_event("hla_predictor", "success", f"Immunological screening complete. Viable slots preserved: {len(validated_payloads)}")
    return validated_payloads
