import os
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from run_pipeline import execute_live_data_pipeline

class OpenOncologyAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_payload = {"system": "OPEN-ONCOLOGY PIPELINE (OOP)", "status": "ONLINE", "active_modules": 19, "license": "GPLv3 Copyleft Enforced"}
            self.wfile.write(json.dumps(status_payload).encode("utf-8"))
            return
        elif self.path == "/api/latest-manifest":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            db_path = "data/database/clinical_history.db"
            if not os.path.exists(db_path):
                self.wfile.write(json.dumps({"error": "No database built yet."}).encode("utf-8"))
                return
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            rows = cursor.execute("SELECT id, sequence_length, gc_content, np_ratio, lipid_density, timestamp FROM patient_runs ORDER BY timestamp DESC").fetchall()
            conn.close()
            records = [{"patient_id": r[0], "length": r[1], "gc_content": r[2], "np_ratio": r[3], "lipid_density": r[4], "processed_at": r[5]} for r in rows]
            self.wfile.write(json.dumps({"total_records": len(records), "history": records}).encode("utf-8"))
            return
        elif self.path == "/api/inventory":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            db_path = "data/database/clinical_history.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            rows = cursor.execute("SELECT reagent_name, stock_level_mg, critical_threshold_mg FROM reagent_inventory").fetchall()
            conn.close()
            inventory_payload = [{"reagent": r[0], "stock_mg": r[1], "threshold_mg": r[2], "status": "OK" if r[1] > r[2] else "CRITICAL"} for r in rows]
            self.wfile.write(json.dumps({"live_inventory": inventory_payload}).encode("utf-8"))
            return
        else:
            self.send_error(404, "Endpoint Not Found")
    def do_POST(self):
        if self.path == "/api/trigger-run":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            print("\n>>> [API PORTAL] Remote Trigger Received! Initializing Core Engine... <<<")
            execute_live_data_pipeline()
            reply = {"status": "SUCCESS", "message": "14-Stage Relational Compute Loop Completed Natively"}
            self.wfile.write(json.dumps(reply).encode("utf-8"))
            return
        else:
            self.send_error(404, "Endpoint Not Found")

def launch_api_portal(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, OpenOncologyAPIHandler)
    print(f"============================================================")
    print(f"       OOP INVENTORY-ARMED WEB API AT PORT {port}             ")
    print(f"============================================================")
    print(f"-> Status Gateway:    http://localhost:{port}/api/status")
    print(f"-> Database History:  http://localhost:{port}/api/latest-manifest")
    print(f"-> Reagent Stock:     http://localhost:{port}/api/inventory")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n>>> [API PORTAL] Relational Server Node Shut Down Safely. <<<")

if __name__ == "__main__":
    launch_api_portal()
