import os
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

def weld_live_dual_action_mrna(blended_manifest, patient_record_id):
    print(f"--- Launching Stage 4: Compiling Final mRNA Blueprint for {patient_record_id} ---")
    codon_opt_map = {
        'Q': 'CAG', 'F': 'UUC', 'E': 'GAG', 'A': 'GCC', 'G': 'GGC', 'L': 'CUG',
        'V': 'GUG', 'I': 'AUC', 'S': 'AGC', 'T': 'ACC', 'K': 'AAG', 'R': 'AGG',
        'Prostate-Specific Antigen': 'AUGCCAGCACUG', 
        'Prostate-Specific Membrane Antigen': 'AUGAAUGCA',
        'Prostatic Acid Phosphatase': 'AUGCGGCA'
    }
    full_mrna_string = ""
    for target in blended_manifest:
        amino_acid = target["amino_acid"]
        if amino_acid in codon_opt_map:
            optimized_sequence = codon_opt_map[amino_acid]
        else:
            optimized_sequence = "AUG"
        full_mrna_string += optimized_sequence + "AAA"
    vaccine_record = SeqRecord(
        Seq(full_mrna_string),
        id=f"OOP-DUAL-{patient_record_id}",
        description="Personalized Prostate Cancer and BPH Therapeutic Blueprint - OPEN SOURCE"
    )
    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"vaccine_blueprint_{patient_record_id}.fasta")
    with open(output_path, "w") as out_file:
        SeqIO.write(vaccine_record, out_file, "fasta")
    return output_path
