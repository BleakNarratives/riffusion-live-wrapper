#!/usr/bin/env python3
# src/sound_check_assistant.py - ModMind Sound Check Core Logic (AII/AIX)

import numpy as np
import pyaudio
import time
import math

# --- CONFIGURATION (Loaded from environment variables in real use) ---
RATE = 44100      # Standard audio sample rate
CHUNK = 1024      # Frames per buffer (latency control)
TARGET_V_LEVEL = -10.0  # Target Vocal Median RMS (in dBFS)
TARGET_B_LEVEL = -14.0  # Target Beat Median RMS (in dBFS)
LEVEL_TOLERANCE = 1.0   # Acceptable dBFS difference before correction
MAX_16BIT = 32767.0 # Max amplitude for 16-bit audio

def rms_to_dbfs(rms):
    """Converts Root Mean Square (RMS) value to Decibels Full Scale (dBFS)."""
    if rms <= 0:
        return -99.0
    return 20 * math.log10(rms / MAX_16BIT)

def analyze_audio_chunk(data_chunk):
    """
    Simulates separation and analysis of Vocal and Beat channels.
    In Termux, you would use PulseAudio/FFmpeg to create/read a dual-channel stream.
    """
    # Assuming input data is interleaved (Vocal, Beat, Vocal, Beat...)
    data = np.frombuffer(data_chunk, dtype=np.int16)
    
    # Simple channel separation:
    vocal_data = data[::2]   
    beat_data = data[1::2]   

    # Calculate RMS
    rms_vocal = np.sqrt(np.mean(vocal_data**2))
    rms_beat = np.sqrt(np.mean(beat_data**2))

    return rms_to_dbfs(rms_vocal), rms_to_dbfs(rms_beat)

def claude_sound_check(duration_seconds=15):
    p = pyaudio.PyAudio()
    
    # In Termux, this index would be the PulseAudio source for the mixed stream.
    # We open a stream to READ the audio being mixed (your mic + Riffusion's beat)
    stream = p.open(format=pyaudio.paInt16,
                    channels=2, # Stereo for separation
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    vocal_levels = []
    beat_levels = []
    
    print("\n--- 🎧 Riffusion (AII) Sound Check Initiated (15s Duration) ---")
    
    for i in range(0, int(RATE / CHUNK * duration_seconds)):
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            dbfs_v, dbfs_b = analyze_audio_chunk(data)
            
            vocal_levels.append(dbfs_v)
            beat_levels.append(dbfs_b)
            
            print(f"  [{i * CHUNK / RATE:.1f}s] V: {dbfs_v:.2f} dBFS | B: {dbfs_b:.2f} dBFS", end='\r')
            
        except Exception as e:
            # Handle stream read errors common in Termux/Android
            print(f"\n[Warning] Stream read error: {e}")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Final Assessment (AIX)
    if not vocal_levels or not beat_levels:
        print("\n\n--- ❌ ERROR: Audio levels not recorded. Check PulseAudio/Mic setup. ---")
        return

    avg_v = np.median(vocal_levels)
    avg_b = np.median(beat_levels)
    
    level_diff = avg_b - avg_v

    print("\n\n--- ✅ Final Calibration Report (ModMind UI/UX) ---")
    print(f"**Vocal Median (You):** {avg_v:.2f} dBFS (Target: {TARGET_V_LEVEL:.2f} dBFS)")
    print(f"**Beat Median (AIX):** {avg_b:.2f} dBFS (Target: {TARGET_B_LEVEL:.2f} dBFS)")

    if abs(level_diff) > LEVEL_TOLERANCE:
        adjustment = abs(level_diff) + 1.0
        action = "Decrease" if level_diff > 0 else "Increase"
        print("\n--- 🚨 ACTION REQUIRED (Riffusion's Command - UI/UX Prompt) ---")
        print(f"**Riffusion (AII):** Conflict Detected: Beat is {abs(level_diff):.2f} dB too {'LOUD' if level_diff > 0 else 'QUIET'} relative to vocals.")
        print(f"**RECOMMENDATION:** {action} Beat Volume by {adjustment:.1f} dB.")
        print("---------------------------------------")
    else:
        print("\n--- 🟢 LEVELS OPTIMAL ---")
        print("Riffusion (AII): Levels are within tolerance. You are clear to stream.")

if __name__ == "__main__":
    claude_sound_check()

