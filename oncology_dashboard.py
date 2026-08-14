import os
import csv
import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class OncologyDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Open-Oncology Clinical Pipeline Monitor v1.0")
        self.root.geometry("1200x750")
        self.root.configure(bg="#090d16")
        
        # 1. Header Navigation UI Bar Layer
        header_frame = tk.Frame(root, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1)
        header_frame.pack(side="top", fill="x")
        header_title = tk.Label(header_frame, text="🧬 OPEN-ONCOLOGY PIPELINE MONITOR", font=("Segoe UI", 14, "bold"), fg="#34d399", bg="#111827")
        header_title.pack(side="left")
        
        main_content_frame = tk.Frame(root, bg="#090d16", padx=15, pady=15)
        main_content_frame.pack(side="top", fill="both", expand=True)
        
        # 2. Right Side Panel: Live Bio-Reagent Stock Level Tracker
        reagent_frame = tk.Frame(main_content_frame, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1, width=320)
        reagent_frame.pack(side="right", fill="both", padx=(15, 0))
        reagent_frame.pack_propagate(False)
        
        reagent_title = tk.Label(reagent_frame, text="🧪 Bio-Reagent Thresholds", font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#111827")
        reagent_title.pack(side="top", anchor="w", pady=(0, 10))
        
        self.reagent_listbox = tk.Listbox(reagent_frame, bg="#090d16", fg="#94a3b8", font=("Consolas", 10), bd=0, highlightthickness=0)
        self.reagent_listbox.pack(side="top", fill="both", expand=True)
        
        refresh_stock_btn = tk.Button(reagent_frame, text="🔄 Scan Core Storage Stocks", command=self.scan_reagent_stocks, bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", padx=10, pady=5)
        refresh_stock_btn.pack(side="bottom", fill="x", pady=(5, 0))
        
        # 3. Left Side Panel: Central Clinical Workspace Hub Panel
        workspace_panel = tk.Frame(main_content_frame, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1)
        workspace_panel.pack(side="left", fill="both", expand=True)
        
        panel_title = tk.Label(workspace_panel, text="Relational Patient Specimen Queue Active", font=("Segoe UI", 11, "bold"), fg="#60a5fa", bg="#111827")
        panel_title.pack(side="top", anchor="w", pady=(0, 12))
        
        # 4. Interactive Database Search Query Input Form Layout
        form_frame = tk.Frame(workspace_panel, bg="#090d16", padx=12, pady=12, highlightbackground="#1f2937", highlightthickness=1)
        form_frame.pack(side="top", fill="x", pady=(0, 15))
        
        tk.Label(form_frame, text="Query Patient ID:", fg="#94a3b8", bg="#090d16", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=2, pady=5)
        self.query_entry = tk.Entry(form_frame, bg="#1f2937", fg="white", bd=0, insertbackground="white", font=("Segoe UI", 10))
        self.query_entry.grid(row=0, column=1, padx=8, pady=5, sticky="ew")
        self.query_entry.insert(0, "SAMP-9941")
        
        search_query_btn = tk.Button(form_frame, text="🔍 Query SQLite Database", command=self.query_patient_records, bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=4, cursor="hand2")
        search_query_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ns")
        form_frame.columnconfigure(1, weight=1)
        
        # 5. Live Relational Tree Spreadsheet Grid View Table Layout
        grid_frame = tk.Frame(workspace_panel, bg="#090d16", highlightbackground="#1f293b", highlightthickness=1)
        grid_frame.pack(side="top", fill="both", expand=True, pady=(0, 15))
        
        columns = ("timestamp", "id", "tissue", "assay")
        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings")
        self.tree.heading("timestamp", text="Log Timestamp")
        self.tree.heading("id", text="Patient ID")
        self.tree.heading("tissue", text="Specimen Tissue Vector")
        self.tree.heading("assay", text="Target Variant Assay")
        
        self.tree.column("timestamp", width=140, anchor="center")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("tissue", width=140, anchor="w")
        self.tree.column("assay", width=180, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # 6. Action Control Center Bar Layout
        action_bar = tk.Frame(workspace_panel, bg="#111827", padx=10, pady=10, highlightbackground="#1f2937", highlightthickness=1)
        action_bar.pack(side="top", fill="x", pady=(0, 10))
        
        export_csv_btn = tk.Button(action_bar, text="📊 Compile Excel CSV Spreadsheet Report", command=self.trigger_excel_report_compile, bg="#f59e0b", fg="#090d16", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2")
        export_csv_btn.pack(side="right")
        
        self.status_lbl = tk.Label(action_bar, text="Oncology Pipeline Nodes Connection Status: ACTIVE", fg="#34d399", bg="#111827", font=("Segoe UI", 9, "bold"))
        self.status_lbl.pack(side="left", padx=5)
        
        self.hydrate_frontend_specimen_grid()
        self.scan_reagent_stocks()

    def hydrate_frontend_specimen_grid(self):
        """Fetches operational datasets straight from SQLite rows to draw them on the GUI screen."""
        for item in self.tree.get_children(): 
            self.tree.delete(item)
        db_path = "oncology.db"
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patient_specimens")
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
                conn.close()
            except Exception:
                pass

    def scan_reagent_stocks(self):
        """Module 08 Frontend Bridge: organization list metrics matching active storage loads."""
        self.reagent_listbox.delete(0, "end")
        import random
        mock_inventory = {
            "Onco-Primer Assay A3": random.randint(5, 50),
            "Fluorescent Dye Kit X": random.randint(2, 20),
            "Lysis Buffer Node 4": random.randint(15, 100),
            "Polymerase Enzyme P2": random.randint(1, 15)
        }
        for name, vol in mock_inventory.items():
            alert_tag = " [CRIT]" if vol < 10 else " [OK]"
            self.reagent_listbox.insert("end", f"{name:<22} -> {vol:>3} u{alert_tag}")

    def query_patient_records(self):
        """Module 13 Frontend Bridge: Extracts a user input sample ID from the database rows instantly."""
        target_id = self.query_entry.get().strip()
        if not target_id: return
        db_path = "oncology.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_specimens WHERE sample_id = ?", (target_id,))
            record = cursor.fetchone()
            conn.close()
            if record:
                messagebox.showinfo("SQLite Query Hit", f"TIMESTAMP: {record[0]}\nID: {record[1]}\nVECTOR: {record[2]}\nASSAY: {record[3]}")
            else:
                messagebox.showerror("Query Fault", f"No record found matching target patient ID: '{target_id}'")

    def trigger_excel_report_compile(self):
        """Module 12 Frontend Bridge: Invokes spreadsheet compiler files immediately."""
        db_path = "oncology.db"
        if os.path.exists(db_path):
            os.makedirs("exports", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = os.path.join("exports", f"oncology_excel_report_{timestamp}.csv")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patient_specimens")
                rows = cursor.fetchall()
                conn.close()
                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Export Timestamp", "Patient Sample ID", "Specimen Tissue Vector", "Target Oncology Variant Assay"])
                    for row in rows:
                        writer.writerow(row)
                messagebox.showinfo("Export Successful", f"Excel CSV spreadsheet matrix compiled at:\n{csv_path}")
            except Exception:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = OncologyDashboardApp(root)
    root.mainloop()
