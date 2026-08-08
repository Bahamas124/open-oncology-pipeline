import os
import random

def run_manufacturing_simulation(patient_id, validation_passed, blended_manifest):
    """
    Stage 8: Lab Manufacturing Simulation Core.
    Calculates cell-free transcription yields, mass output metrics, 
    and chemical costing estimations before actual printer execution.
    """
    print(f"--- Launching Stage 8: Initializing Biomanufacturing Simulation for {patient_id} ---")
    
    if not validation_passed:
        print(f"[Simulation Blocked] Quality control gate failed. Aborting manufacturing run.")
        return False
        
    # Calculate simulation factors based on payload properties
    total_slots = len(blended_manifest)
    
    # Establish deterministic transcription mechanics with slight random bio-variance
    transcription_efficiency = round(random.uniform(88.5, 94.2), 2)
    purification_yield_pct = round(random.uniform(75.0, 82.5), 2)
    
    # Mathematical output projections based on target payload layout density
    base_yield_ug_per_ml = round((total_slots * 12.5) * (transcription_efficiency / 100), 2)
    final_purified_mass_ug = round(base_yield_ug_per_ml * 50 * (purification_yield_pct / 100), 2) # Assumes 50ml batch
    
    # Financial/Resource calculation (Simulated open-source enzyme/nucleotide cost tracking)
    fixed_reagent_cost = 145.00
    variable_target_cost = total_slots * 32.10
    total_simulated_cost = round(fixed_reagent_cost + variable_target_cost, 2)
    cost_per_dose_ug = round(total_simulated_cost / final_purified_mass_ug, 2) if final_purified_mass_ug > 0 else 0
    
    print(f"[Simulator] Bioreactor yield optimization model finalized.")
    print(f"    -> RNA Polymerase Efficiency: {transcription_efficiency}%")
    print(f"    -> Projected Pure Yield:      {final_purified_mass_ug} ug (per 50mL bioreactor batch)")
    print(f"    -> Estimated Production Cost: ${total_simulated_cost} USD")
    print(f"    -> Material Unit Cost:        ${cost_per_dose_ug} USD per ug")
    
    # Write simulation manifest report to disk
    sim_dir = "data/manufacturing"
    os.makedirs(sim_dir, exist_ok=True)
    sim_path = os.path.join(sim_dir, f"simulation_manifest_{patient_id}.txt")
    
    with open(sim_path, "w", encoding="utf-8") as sim_file:
        sim_file.write(f"BIOMANUFACTURING PROJECTION MANIFEST\n")
        sim_file.write(f"Patient ID:                {patient_id}\n")
        sim_file.write(f"Transcription Efficiency:  {transcription_efficiency}%\n")
        sim_file.write(f"Purification Efficiency:   {purification_yield_pct}%\n")
        sim_file.write(f"Final Purified RNA Mass:   {final_purified_mass_ug} ug\n")
        sim_file.write(f"Total Projected Batch Cost:${total_simulated_cost} USD\n")
        sim_file.write(f"Unit Material Efficiency:  ${cost_per_dose_ug} USD/ug\n")
        sim_file.write(f"MANUFACTURING RUN STATUS: READY FOR SIMULATED PRINTER EXECUTION\n")
        
    print(f"--> SUCCESS: Biomanufacturing simulation logs written to: {os.path.abspath(sim_path)}")
    return True
