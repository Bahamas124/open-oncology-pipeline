import os
import json
import glob
from http.server import HTTPServer, BaseHTTPRequestHandler
from run_pipeline import execute_live_data_pipeline

class OpenOncologyAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_payload = {"system": "OPEN-ONCOLOGY PIPELINE (OOP)", "status": "ONLINE", "active_modules": 10, "license": "GPLv3 Copyleft Enforced"}
            self.wfile.write(json.dumps(status_payload).encode("utf-8"))
            return
        elif self.path == "/api/latest-manifest":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            log_files = glob.glob("data/validation/validation_log_*.txt")
            if not log_files:
                self.wfile.write(json.dumps({"error": "No assets compiled yet."}).encode("utf-8"))
                return
            latest_log = max(log_files, key=os.path.getmtime)
            with open(latest_log, "r", encoding="utf-8") as lf:
                log_lines = lf.readlines()
            manifest_payload = {"source_log": os.path.basename(latest_log), "metrics": [line.strip() for line in log_lines]}
            self.wfile.write(json.dumps(manifest_payload).encode("utf-8"))
            return
        else:
            self.send_error(404, "Endpoint Not Found")
    def do_POST(self):
        if self.path == "/api/trigger-run":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            print("\n>>> [API PORTAL] Remote Trigger Active! <<<")
            execute_live_data_pipeline()
            reply = {"status": "SUCCESS", "message": "9-Stage Loop Completed Natively"}
            self.wfile.write(json.dumps(reply).encode("utf-8"))
            return
        else:
            self.send_error(404, "Endpoint Not Found")

def launch_api_portal(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, OpenOncologyAPIHandler)
    print(f"============================================================")
    print(f"       OOP WEB API PORTAL INITIALIZED ON PORT {port}         ")
    print(f"============================================================")
    print(f"-> Status Gateway:    http://localhost:{port}/api/status")
    print(f"-> Manifest Gateway:  http://localhost:{port}/api/latest-manifest")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n>>> [API PORTAL] Server Node Shut Down Safely. <<<")

if __name__ == "__main__":
    launch_api_portal()
