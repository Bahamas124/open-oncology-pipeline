from Bio.Seq import Seq

def isolate_live_somatic_mutations(tumor_sequence_id, raw_tumor_seq):
    print(f"--- Launching Stage 2: Filtering Live Record [{tumor_sequence_id}] ---")
    healthy_prostate_reference = "ATGGTTTACAAGTAG" 
    tumor_dna = str(raw_tumor_seq).upper()
    tumor_codons = [tumor_dna[i:i+3] for i in range(0, len(tumor_dna), 3) if len(tumor_dna[i:i+3]) == 3]
    healthy_codons = set([healthy_prostate_reference[i:i+3] for i in range(0, len(healthy_prostate_reference), 3)])
    isolated_mutations = []
    for index, codon in enumerate(tumor_codons):
        if codon in healthy_codons:
            continue
        else:
            try:
                amino_acid = str(Seq(codon).translate())
                mutation_entry = {
                    "id": f"MUT-{tumor_sequence_id}-POS-{(index * 3) + 1}",
                    "position": (index * 3) + 1,
                    "mutated_codon": codon,
                    "amino_acid": amino_acid,
                    "target_type": "Personalized Cancer Clone"
                }
                isolated_mutations.append(mutation_entry)
                print(f"[Classifier] Anomaly found at base {mutation_entry['position']}: Codon {codon} -> Amino Acid {amino_acid}")
            except Exception:
                continue
    print(f"[Classifier] Analysis complete. Isolated {len(isolated_mutations)} target variations.")
    return isolated_mutations
