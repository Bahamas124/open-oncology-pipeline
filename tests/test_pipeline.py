import unittest
import os
import glob
from src.logger import log_pipeline_event
from src.cleaner import purge_temporary_pipeline_caches

class TestOpenOncologyAutomationSuite(unittest.TestCase):
    def test_module_12_logger_write_integrity(self):
        """Validates that the system logging module accurately creates persistent tracking streams on disk."""
        test_path = log_pipeline_event("test_node", "info", "Executing system validation script integrity verification check.")
        self.assertTrue(os.path.exists(test_path), "System Logger failed to generate physical audit logs on the hard drive.")
        
    def test_module_13_cleaner_directory_sweep(self):
        """Validates that the garbage collector sweeps standard tracking directories accurately."""
        test_file = "data/patient_samples/ncbi_prostate_variant_9999999999.fasta"
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(">TEST_RECORD\\nACGT")
        
        purged = purge_temporary_pipeline_caches()
        self.assertGreaterEqual(purged, 1, "Garbage collection module failed to isolate and clean target paths.")

if __name__ == "__main__":
    unittest.main()
