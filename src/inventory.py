import sqlite3
import os
from src.logger import log_pipeline_event

def initialize_inventory_database():
    """
    Stage 19: Chemical Inventory Management Layer.
    Establishes storage schema tables to track raw laboratory reagent stocks.
    """
    db_path = os.path.join("data/database", "clinical_history.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reagent_inventory (
        reagent_name TEXT PRIMARY KEY,
        stock_level_mg REAL,
        critical_threshold_mg REAL
    )
    """)
    
    reagents = [
        ("mRNA_Nucleotide_Bases", 50000.0, 5000.0),
        ("Ionizable_Target_Lipids", 25000.0, 2500.0),
        ("T7_RNA_Polymerase_Enzyme", 10000.0, 1000.0)
    ]
    for name, stock, thresh in reagents:
        cursor.execute("""
        INSERT OR IGNORE INTO reagent_inventory (reagent_name, stock_level_mg, critical_threshold_mg)
        VALUES (?, ?, ?)
        """, (name, stock, thresh))
        
    conn.commit()
    conn.close()
    log_pipeline_event("inventory_manager", "success", "Chemical inventory databases synchronized.")

def deduct_manufacturing_materials(sequence_length, total_yield_ug, lipid_density_mg_ml):
    """Tracks real-time manufacturing resource consumption and flags low stock alerts."""
    db_path = os.path.join("data/database", "clinical_history.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Restored calculation equations to map physical reagent usage metrics safely
    base_consumed_mg = round((sequence_length * 0.00033) * (total_yield_ug / 1000.0), 3)
    lipid_consumed_mg = round(lipid_density_mg_ml * 50.0, 3)
    enzyme_consumed_mg = round(total_yield_ug * 0.001, 3)
    
    deductions = [
        ("mRNA_Nucleotide_Bases", base_consumed_mg),
        ("Ionizable_Target_Lipids", lipid_consumed_mg),
        ("T7_RNA_Polymerase_Enzyme", enzyme_consumed_mg)
    ]
    
    for name, consumed_mass in deductions:
        cursor.execute("""
        UPDATE reagent_inventory 
        SET stock_level_mg = stock_level_mg - ? 
        WHERE reagent_name = ?
        """, (consumed_mass, name))
        
        row = cursor.execute("SELECT stock_level_mg, critical_threshold_mg FROM reagent_inventory WHERE reagent_name = ?", (name,)).fetchone()
        if row and row[0] <= row[1]:
            log_pipeline_event("inventory_manager", "warning", f"CRITICAL STOCK ALERT: {name} depleted to {row[0]} mg. Reorder immediate.")
        else:
            log_pipeline_event("inventory_manager", "success", f"Deducted {consumed_mass} mg from {name} stock pool.")
            
    conn.commit()
    conn.close()
