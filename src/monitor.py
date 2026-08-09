import time
import os
from src.dashboard import render_graphical_matrix

def launch_live_monitor_loop(refresh_rate_sec=3):
    """
    Optional Runtime Module: Interactive System Monitor Loop.
    Clears the screen and re-renders the graphical matrix at a regular interval.
    """
    try:
        while True:
            # Clear the terminal window based on operating system constraints
            os.system("cls" if os.name == "nt" else "clear")
            
            # Render the updated statistics overview tracking frame
            render_graphical_matrix()
            
            print(">>> [MONITOR LOOP] Press Ctrl+C at any time to exit the dashboard node safely... <<<")
            time.sleep(refresh_rate_sec)
    except KeyboardInterrupt:
        print("\n>>> [MONITOR LOOP] Interactive Tracker Stopped Safely. <<<")

if __name__ == "__main__":
    launch_live_monitor_loop()
