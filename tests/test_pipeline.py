import os
import unittest
from src.predictor import run_live_ai_judge_and_blender
from src.optimizer import weld_live_dual_action_mrna

class TestOpenOncologyPipeline(unittest.TestCase):
    def setUp(self):
        self.patient_id = "TEST-RECORD"
        self.mock_mutations = [
            {"id": "MUT-01", "position": 12, "mutated_codon": "CAG", "amino_acid": "Q"},
            {"id": "MUT-02", "position": 45, "mutated_codon": "GAA", "amino_acid": "E"}
        ]
    def test_bph_anchor_integrity(self):
        blended_manifest = run_live_ai_judge_and_blender(self.mock_mutations)
        target_ids = [target["id"] for target in blended_manifest]
        self.assertIn("TAA-PSA", target_ids)
        self.assertIn("TAA-PSMA", target_ids)
        self.assertIn("TAA-PAP", target_ids)
    def test_file_generation(self):
        blended_manifest = run_live_ai_judge_and_blender(self.mock_mutations)
        output_file = weld_live_dual_action_mrna(blended_manifest, self.patient_id)
        self.assertTrue(os.path.exists(output_file))
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
