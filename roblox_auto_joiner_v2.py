"""
Roblox Launcher - Session Reuse Method
First launch: Manual login required
Subsequent launches: Reuses saved session
"""

import os
import sys
import time
import subprocess
from typing import Dict, List, Optional


def launch_chrome_with_session(username: str, vip_link: str, first_time: bool = False) -> Optional[subprocess.Popen]:
    """Launch Chrome with persistent session"""
    try:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if not chrome_path:
            print("      ❌ Chrome not found")
            return None
        
        # Each account gets its own Chrome profile
        profile_dir = os.path.join(os.getcwd(), "chrome_sessions", username)
        os.makedirs(profile_dir, exist_ok=True)
        
        if first_time:
            print(f"      🔐 FIRST TIME - Please login manually in the Chrome window")
            print(f"      After logging in, Chrome will stay open")
            print(f"      Close this terminal to stop, or wait for Roblox to close")
        
        # Launch Chrome with persistent profile
        proc = subprocess.Popen([
            chrome_path,
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            vip_link
        ])
        
        return proc
        
    except Exception as e:
        print(f"      ❌ Launch failed: {e}")
        return None


def wait_for_roblox_close():
    """Wait for Roblox to close"""
    try:
        import psutil
    except:
        print("Installing psutil...")
        subprocess.run([sys.executable, "-m", "pip", "install", "psutil", "--break-system-packages"])
        import psutil
    
    print("   ⏳ Waiting for Roblox to close...", end="", flush=True)
    
    while True:
        found = False
        for proc in psutil.process_iter(['name']):
            try:
                if 'RobloxPlayerBeta.exe' in proc.info['name']:
                    found = True
                    break
            except:
                pass
        
        if not found:
            print(" ✅\n")
            return
        
        time.sleep(2)


def check_if_logged_in(username: str) -> bool:
    """Check if this account already has a saved session"""
    profile_dir = os.path.join(os.getcwd(), "chrome_sessions", username)
    # Check if profile exists and has cookies
    cookies_file = os.path.join(profile_dir, "Default", "Network", "Cookies")
    return os.path.exists(cookies_file)


def main():
    print("\n🎮 ROBLOX SESSION LAUNCHER\n")
    print("⚠️  IMPORTANT:")
    print("   First time per account: You must login manually")
    print("   After that: Session is saved and reused\n")
    
    print("DEBUG: Loading files...")
    
    # Load files
    def load_txt(f):
        print(f"DEBUG: Loading {f}...")
        if not os.path.exists(f):
            print(f"DEBUG: {f} does not exist!")
            return []
        with open(f) as file:
            lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            print(f"DEBUG: Loaded {len(lines)} lines from {f}")
            return lines
    
    def load_kv(f):
        print(f"DEBUG: Loading {f}...")
        if not os.path.exists(f):
            print(f"DEBUG: {f} does not exist!")
            return {}
        data = {}
        with open(f) as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip()] = v.strip()
        print(f"DEBUG: Loaded {len(data)} entries from {f}")
        return data
    
    targets = load_txt('targets.txt')
    vips = load_kv('vipserver.txt')
    collectors = load_kv('collectors.txt')
    
    print(f"\nDEBUG: targets={len(targets)}, vips={len(vips)}, collectors={len(collectors)}")
    
    if not targets:
        print("❌ No targets loaded!")
        input()
        return
        
    if not collectors:
        print("❌ No collectors loaded!")
        input()
        return
    
    targets_with_vip = [t for t in targets if t in vips]
    print(f"DEBUG: {len(targets_with_vip)} targets have VIP servers")
    
    if not targets_with_vip:
        print("❌ No targets have VIP servers")
        input()
        return
    
    total = len(targets_with_vip) * len(collectors)
    print(f"✅ {total} launches\n")
    
    print("DEBUG: Starting launch loop...")
    
    # Launch
    current = 0
    for target in targets:
        if target not in vips:
            continue
        
        print(f"🎯 {target}\n")
        vip_link = vips[target]
        
        for username in collectors.keys():
            current += 1
            print(f"[{current}/{total}] 🚀 {username}")
            
            # Check if first time
            first_time = not check_if_logged_in(username)
            
            if first_time:
                print("   ⚠️  FIRST TIME - Manual login required")
            else:
                print("   ✅ Session exists - Should auto-login")
            
            # Launch Chrome
            print("   🌐 Launching Chrome...")
            proc = launch_chrome_with_session(username, vip_link, first_time)
            
            if not proc:
                print("   ❌ FAILED\n")
                continue
            
            print(f"   ✅ Chrome launched (PID: {proc.pid})")
            
            # Wait for Roblox to start
            print("   ⏳ Waiting 15s for you to login/Roblox to start...")
            time.sleep(15)
            
            # Wait for Roblox to close
            wait_for_roblox_close()
            
            # Kill Chrome
            print("   ❌ Closing Chrome...")
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except:
                try:
                    proc.kill()
                except:
                    pass
            
            print("=" * 60)
    
    print("\n✅ DONE\n")
    input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input()