import os
import csv
import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class OncologyDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Open-Oncology Clinical Pipeline Monitor v1.1")
        self.root.geometry("1300x820")
        self.root.configure(bg="#090d16")
        
        # 1. Header Navigation UI Bar Layer
        header_frame = tk.Frame(root, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1)
        header_frame.pack(side="top", fill="x")
        header_title = tk.Label(header_frame, text="🧬 OPEN-ONCOLOGY PIPELINE MONITOR", font=("Segoe UI", 14, "bold"), fg="#34d399", bg="#111827")
        header_title.pack(side="left")
        
        main_content_frame = tk.Frame(root, bg="#090d16", padx=15, pady=15)
        main_content_frame.pack(side="top", fill="both", expand=True)
        
        # 2. Right Side Master Container Panel: Reagents & Maintenance Splits
        right_panel = tk.Frame(main_content_frame, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1, width=340)
        right_panel.pack(side="right", fill="both", padx=(15, 0))
        right_panel.pack_propagate(False)
        
        # Top Half of Right Panel: Live Bio-Reagent Stock Level Tracker
        reagent_title = tk.Label(right_panel, text="🧪 Bio-Reagent Thresholds", font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#111827")
        reagent_title.pack(side="top", anchor="w", pady=(0, 5))
        self.reagent_listbox = tk.Listbox(right_panel, bg="#090d16", fg="#94a3b8", font=("Consolas", 10), bd=0, highlightthickness=0, height=8)
        self.reagent_listbox.pack(side="top", fill="x", pady=(0, 5))
        refresh_stock_btn = tk.Button(right_panel, text="🔄 Scan Core Storage Stocks", command=self.scan_reagent_stocks, bg="#059669", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", padx=10, pady=4)
        refresh_stock_btn.pack(side="top", fill="x", pady=(0, 15))
        
        # Bottom Half of Right Panel (MODULE 14): Lab Equipment Maintenance Logger
        maint_title = tk.Label(right_panel, text="🛠️ Equipment Maintenance Log", font=("Segoe UI", 11, "bold"), fg="#a78bfa", bg="#111827")
        maint_title.pack(side="top", anchor="w", pady=(5, 5))
        
        self.maint_entry = tk.Entry(right_panel, bg="#1f2937", fg="white", bd=0, insertbackground="white", font=("Segoe UI", 10))
        self.maint_entry.pack(side="top", fill="x", pady=(0, 5))
        self.maint_entry.insert(0, "Hardware Note (e.g., Sequencer Calibration)")
        
        log_maint_btn = tk.Button(right_panel, text="+ Log Hardware Calibration", command=self.catalog_maintenance_event, bg="#7c3aed", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", padx=10, pady=4)
        log_maint_btn.pack(side="top", fill="x", pady=(0, 8))
        
        self.maint_listbox = tk.Listbox(right_panel, bg="#090d16", fg="#a78bfa", selectbackground="#7c3aed", font=("Segoe UI", 9), bd=0, highlightthickness=0)
        self.maint_listbox.pack(side="top", fill="both", expand=True)
        
        # 3. Left Side Panel: Central Clinical Workspace Hub Panel
        workspace_panel = tk.Frame(main_content_frame, bg="#111827", padx=15, pady=15, highlightbackground="#1f2937", highlightthickness=1)
        workspace_panel.pack(side="left", fill="both", expand=True)
        
        panel_title = tk.Label(workspace_panel, text="Relational Patient Specimen Queue Active", font=("Segoe UI", 11, "bold"), fg="#60a5fa", bg="#111827")
        panel_title.pack(side="top", anchor="w", pady=(0, 12))
        
        # 4. Interactive Database Search Query Input Form Layout
        form_frame = tk.Frame(workspace_panel, bg="#090d16", padx=12, pady=12, highlightbackground="#1f2937", highlightthickness=1)
        form_frame.pack(side="top", fill="x", pady=(0, 15))
        
        lbl = tk.Label(form_frame, text="Query Patient ID:", fg="#94a3b8", bg="#090d16", font=("Segoe UI", 10, "bold"))
        lbl.grid(row=0, column=0, sticky="w", padx=2, pady=5)
        
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
        
        connect_db_btn = tk.Button(action_bar, text="🔌 Connect Database Channels", command=self.hydrate_frontend_specimen_grid, bg="#3b82f6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=4, cursor="hand2")
        connect_db_btn.pack(side="left", padx=5)
        
        self.status_lbl = tk.Label(action_bar, text="Oncology GUI Workspace Layer: INITIALIZED", fg="#60a5fa", bg="#111827", font=("Segoe UI", 9, "bold"))
        self.status_lbl.pack(side="left", padx=5)
        
        self.scan_reagent_stocks()
        self.load_maintenance_events()

    def catalog_maintenance_event(self):
        note = self.maint_entry.get().strip()
        if not note or note.startswith("Hardware Note"): return
        try:
            os.makedirs("logs", exist_ok=True)
            with open(os.path.join("logs", "maintenance_tracker.log"), "a", encoding="utf-8") as lf:
                lf.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d')}] {note}\n")
            self.load_maintenance_events()
            self.maint_entry.delete(0, "end")
        except Exception:
            pass

    def load_maintenance_events(self):
        self.maint_listbox.delete(0, "end")
        log_path = os.path.join("logs", "maintenance_tracker.log")
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8") as lf:
                    for line in lf:
                        if line.strip(): self.maint_listbox.insert("end", line.strip())
            except Exception:
                pass

    def hydrate_frontend_specimen_grid(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        db_path = "oncology.db"
        try:
            conn = sqlite3.connect(db_path, timeout=2)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_specimens")
            for row in cursor.fetchall(): self.tree.insert("", "end", values=row)
            conn.close()
            self.status_lbl.configure(text="Oncology Pipeline Nodes Connection Status: ACTIVE", fg="#34d399")
        except Exception:
            messagebox.showwarning("Database Locked", "Database file busy. Click Connect Database again!")

    def scan_reagent_stocks(self):
        self.reagent_listbox.delete(0, "end")
        import random
        mock_inventory = {"Onco-Primer Assay A3": random.randint(5, 50), "Fluorescent Dye Kit X": random.randint(2, 20), "Lysis Buffer Node 4": random.randint(15, 100), "Polymerase Enzyme P2": random.randint(1, 15)}
        for name, vol in mock_inventory.items():
            alert_tag = " [CRIT]" if vol < 10 else " [OK]"
            self.reagent_listbox.insert("end", f"{name:<22} -> {vol:>3} u{alert_tag}")

    def query_patient_records(self):
        target_id = self.query_entry.get().strip()
        if not target_id: return
        db_path = "oncology.db"
        try:
            conn = sqlite3.connect(db_path, timeout=2)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_specimens WHERE sample_id = ?", (target_id,))
            record = cursor.fetchone()
            conn.close()
            if record:
                messagebox.showinfo("SQLite Query Hit", f"TIMESTAMP: {record}\nID: {record}\nVECTOR: {record}\nASSAY: {record}")
            else:
                messagebox.showerror("Query Fault", f"No record found matching patient ID: '{target_id}'")
        except Exception:
            messagebox.showwarning("Lock Present", "Database channel busy. Please try query again.")

