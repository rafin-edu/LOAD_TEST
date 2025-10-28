"""
Direct Firebase REST API Visitor Incrementer
This directly hits Firebase API - SUPER FAST, no browser needed!
"""

import requests
import time
from datetime import datetime
import signal
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
FIREBASE_URL = "https://boardrankctg-default-rtdb.asia-southeast1.firebasedatabase.app"
FIREBASE_PATH = "/siteStats/totalVisits.json"
DELAY = 0.01  # 0.01 seconds = 100 visits per second!
MAX_WORKERS = 50  # Number of concurrent threads

# Global variables
visit_count = 0
success_count = 0
running = True
start_time = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n\n🛑 Stopping... Please wait...")
    running = False

def increment_firebase():
    """Directly increment Firebase counter via REST API"""
    global visit_count, success_count
    
    try:
        # Firebase REST API transaction endpoint
        url = f"{FIREBASE_URL}{FIREBASE_PATH}"
        
        # Method 1: Read current value
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            current = response.json() or 0
            new_value = current + 1
            
            # Method 2: Write new value
            put_response = requests.put(url, json=new_value, timeout=5)
            
            if put_response.status_code == 200:
                visit_count += 1
                success_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{timestamp}] ✅ Visit #{visit_count} - New total: {new_value}")
                return True
        
        visit_count += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Visit #{visit_count} - Failed (status: {response.status_code})")
        return False
        
    except Exception as e:
        visit_count += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Visit #{visit_count} - Error: {str(e)[:40]}")
        return False

def increment_firebase_fast():
    """Ultra-fast method - just increment without reading"""
    global visit_count, success_count
    
    try:
        # Direct transaction using Firebase REST API
        url = f"{FIREBASE_URL}{FIREBASE_PATH}"
        
        # Just add 1 to whatever is there
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            current = response.json() or 0
            requests.put(url, json=current + 1, timeout=5)
            
            visit_count += 1
            success_count += 1
            return True
        
        visit_count += 1
        return False
        
    except:
        visit_count += 1
        return False

def print_stats():
    """Print statistics"""
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    rate = visit_count / elapsed if elapsed > 0 else 0
    success_rate = (success_count / visit_count * 100) if visit_count > 0 else 0
    
    print("\n" + "="*70)
    print(f"📊 STATISTICS")
    print("="*70)
    print(f"Total Requests Sent: {visit_count}")
    print(f"Successful: {success_count} ({success_rate:.1f}%)")
    print(f"Running Time: {minutes}m {seconds}s")
    print(f"Average Rate: {rate:.2f} requests/second")
    print(f"Target Rate: {1/DELAY:.1f} requests/second")
    print("="*70 + "\n")

def main_sequential():
    """Sequential method - one at a time"""
    global running, start_time
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*70)
    print("🚀 DIRECT FIREBASE VISITOR INCREMENT - Sequential Mode")
    print("="*70)
    print(f"Firebase URL: {FIREBASE_URL}")
    print(f"Target Path: {FIREBASE_PATH}")
    print(f"Delay: {DELAY} seconds ({1/DELAY:.1f} requests/second)")
    print("="*70)
    print("\nPress Ctrl+C to stop\n")
    
    start_time = time.time()
    
    try:
        while running:
            increment_firebase()
            if running:
                time.sleep(DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        print("\n\n⏹  Stopped!")
        print_stats()

def main_concurrent():
    """Concurrent method - SUPER FAST with multiple threads"""
    global running, start_time
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*70)
    print("🚀 DIRECT FIREBASE VISITOR INCREMENT - Concurrent Mode (FASTEST!)")
    print("="*70)
    print(f"Firebase URL: {FIREBASE_URL}")
    print(f"Target Path: {FIREBASE_PATH}")
    print(f"Concurrent Workers: {MAX_WORKERS}")
    print(f"Delay: {DELAY} seconds")
    print("="*70)
    print("\n⚡ WARNING: This is VERY FAST and may trigger rate limits!")
    print("Press Ctrl+C to stop\n")
    
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            
            while running:
                # Submit multiple requests
                for _ in range(10):  # Batch of 10
                    if not running:
                        break
                    future = executor.submit(increment_firebase_fast)
                    futures.append(future)
                
                # Small delay between batches
                time.sleep(DELAY)
                
                # Print progress occasionally
                if len(futures) % 100 == 0:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 📈 Sent {visit_count} requests...")
            
            # Wait for remaining futures
            for future in as_completed(futures):
                future.result()
                
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        print("\n\n⏹  Stopped!")
        print_stats()

if __name__ == "__main__":
    print("\n🎯 Choose mode:\n")
    print("1. Sequential (Safer, ~100 visits/sec)")
    print("2. Concurrent (FASTEST, ~1000+ visits/sec)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        print("\n⚡ Starting CONCURRENT mode...")
        time.sleep(1)
        main_concurrent()
    else:
        print("\n✅ Starting SEQUENTIAL mode...")
        time.sleep(1)
        main_sequential()