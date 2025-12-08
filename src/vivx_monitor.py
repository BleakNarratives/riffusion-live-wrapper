#!/usr/bin/env python3
# src/vivx_monitor.py - Real-Time Viewer Interaction & AIX Monitor via EquiNex Bridge

import os
import time
import random
from datetime import datetime
from src.equinex_bridge import EquiNexBridge

# ANSI Color Codes
BLUE = '\033[34m'; CYAN = '\033[36m'; ORANGE = '\033[33m'
GREEN = '\033[32m'; BOLD = '\033[1m'; RESET = '\033[0m'

# --- CONFIGURATION & BRIDGE INITIALIZATION ---
TEMP_LOG_FILE = "/tmp/lyria_steering_log.txt"
BRIDGE = EquiNexBridge()

def fetch_lyria_status():
    """Reads the last command sent to Riffusion Music Engine via the Bridge log file."""
    try:
        with open(TEMP_LOG_FILE, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                if "Riffusion Music EngineSteer" in last_line:
                    prompt = last_line.split("Riffusion Music EngineSteer: ")[-1]
                    return f"Steering: {prompt}"
    except FileNotFoundError:
        return "AIX: Riffusion Music Engine Standby (Log Missing)"
    return "AIX: Ready"

def display_live_monitor():
    start_time = time.time()
    
    while True: 
        os.system('clear')

        # --- HEADER ---
        elapsed = int(time.time() - start_time)
        print(f"{BOLD}{CYAN}------------------------------------------------------{RESET}")
        print(f"{BOLD}{CYAN}  LIVE PERFORMANCE CONSOLE | TIME: {elapsed}s | EQUINEX {RESET}")
        print(f"{BOLD}{CYAN}------------------------------------------------------{RESET}")
        
        # --- AII/AIX (Riffusion's Internal State) ---
        print(f"{BOLD}{BLUE}--- AIX: LYRIA MUSIC ENGINE STATUS (AII) ---{RESET}")
        lyria_status = fetch_lyria_status()
        print(f"{CYAN}  > {lyria_status}{RESET}")
        
        # --- VIVX (Viewer Interaction) ---
        print(f"\n{BOLD}{ORANGE}--- VI/VX: VIEWER SYNTAX CHALLENGE ---{RESET}")
        vivx_data = BRIDGE.get_live_viewer_data()
        
        print(f"{BOLD}{GREEN}  > RHYME GOAL (VI): {vivx_data['syntax_challenge']}{RESET}")
        print(f"{ORANGE}  > Active Vote: [Beat Fade] ({vivx_data['vote_result']}){RESET}")
        
        # --- UI/UX CUES ---
        print(f"\n{BOLD}{CYAN}--- USER CUES (UI/UX) ---{RESET}")
        # Note: Vocal energy is now generated locally since the monitor needs to be fast
        print(f"{CYAN}  > Vocal Energy: {random.randint(40, 99)}% | Mic Gain: 0dB{RESET}")
        print(f"{CYAN}  > Current Set Item: The Kick-Out Freestyle{RESET}")
        
        # --- FOOTER ---
        print(f"\n{BOLD}{CYAN}------------------------------------------------------{RESET}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    # Ensure log file exists before starting the monitor
    try:
        open(TEMP_LOG_FILE, 'w').close()
    except:
        pass
        
    display_live_monitor()
