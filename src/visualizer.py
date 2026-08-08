import os

def render_patient_target_barcode(patient_id, blended_manifest):
    """
    Stage 6: Molecular Visualizer Engine.
    Generates a high-scannability ASCII barcode map of personalized cancer clone 
    mutations alongside the standard universal tissue anchors.
    """
    print(f"--- Launching Stage 6: Rendering Molecular Visuals for {patient_id} ---")
    
    # 1. Sort the incoming tracking payload data array by ranking score
    sorted_targets = sorted(blended_manifest, key=lambda x: x["ai_priority_score"], reverse=True)
    
    # 2. Build the visual text layout matrix
    visual_output = f"""======================================================================
OPEN-ONCOLOGY VISUAL TARGET BARCODE MAP
Patient Identifier: {patient_id}
======================================================================

[VISUAL IMMUNOLOGICAL MOLECULAR BARCODE]
----------------------------------------------------------------------
"""
    
    # Render structural tracking blocks representing the payload density layout
    barcode_string = "||"
    for target in sorted_targets:
        if "Universal" in target["target_type"]:
            barcode_string += " █ [BPH-ANCHOR] "
        else:
            barcode_string += f" █ [MUT-POS-{target['id'].split('-')[-1]}] "
    barcode_string += "||"
    
    visual_output += barcode_string + "\n\n"
    visual_output += "[TARGET MATRIX SPECTROGRAPHY]\n"
    visual_output += "----------------------------------------------------------------------\n"
    
    # Add scannable detail tracks for fast medical inspection
    for index, target in enumerate(sorted_targets, 1):
        indicator = "🌟 [CORE TARGET]" if target["ai_priority_score"] >= 1.0 else "🎯 [CLONAL VAR]"
        visual_output += f"Slot #{index:02d} | {indicator} Score: {target['ai_priority_score']:.2f} -> {target['amino_acid']}\n"
        
    visual_output += f"""
----------------------------------------------------------------------
[VISUAL DATA ASSURANCE]
All structural layout maps have been safely formatted under GPLv3 copyleft rules.
======================================================================
"""

    # Save directly into your data directory asset stack
    visual_dir = "data/visuals"
    os.makedirs(visual_dir, exist_ok=True)
    visual_path = os.path.join(visual_dir, f"target_map_{patient_id}.txt")
    
    with open(visual_path, "w", encoding="utf-8") as vis_file:
        vis_file.write(visual_output)
        
    print(f"--> SUCCESS: High-density visual map written to: {os.path.abspath(visual_path)}")
    return visual_path
