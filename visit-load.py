"""
Simple Website Visitor - Just hit the URL repeatedly
NO database, NO browser, NO HTML files needed!
Just pure HTTP requests to your website
"""

import requests
import time
from datetime import datetime
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

# ========== CONFIGURATION ==========
WEBSITE_URL = "https://yaeko-pajamaed-contrapuntally.ngrok-free.dev/"  # PUT YOUR WEBSITE URL HERE
DELAY = 1  # Delay between requests (0.1 = 10 requests per second)
CONCURRENT_REQUESTS = 1  # Number of simultaneous requests
# ===================================

# Global variables
visit_count = 0
success_count = 0
running = True
start_time = None

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    global running
    print("\n\n🛑 Stopping...")
    running = False

def visit_url():
    """Send one request to the website"""
    global visit_count, success_count
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(WEBSITE_URL, headers=headers, timeout=10)
        visit_count += 1
        
        if response.status_code == 200:
            success_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ✅ Visit #{visit_count} - Success")
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Visit #{visit_count} - Status: {response.status_code}")
            return False
            
    except Exception as e:
        visit_count += 1
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Visit #{visit_count} - Error: {str(e)[:30]}")
        return False

def print_stats():
    """Print statistics"""
    if start_time is None:
        return
        
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    rate = visit_count / elapsed if elapsed > 0 else 0
    success_rate = (success_count / visit_count * 100) if visit_count > 0 else 0
    
    print("\n" + "="*60)
    print("📊 STATISTICS")
    print("="*60)
    print(f"Total Visits: {visit_count}")
    print(f"Successful: {success_count} ({success_rate:.1f}%)")
    print(f"Running Time: {minutes}m {seconds}s")
    print(f"Average Rate: {rate:.2f} visits/second")
    print("="*60)

def main():
    """Main function"""
    global running, start_time
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*60)
    print("🚀 SIMPLE URL VISITOR")
    print("="*60)
    print(f"Target: {WEBSITE_URL}")
    print(f"Delay: {DELAY}s ({1/DELAY:.0f} requests/sec)")
    print(f"Concurrent: {CONCURRENT_REQUESTS} threads")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    if WEBSITE_URL == "https://your-website-url.com":
        print("❌ Please change WEBSITE_URL in the code!")
        return
    
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
            while running:
                # Submit concurrent requests
                futures = [executor.submit(visit_url) for _ in range(CONCURRENT_REQUESTS)]
                
                # Wait for all to complete
                for future in futures:
                    if not running:
                        break
                    try:
                        future.result()
                    except:
                        pass
                
                # Delay before next batch
                if running:
                    time.sleep(DELAY)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        running = False
        print("\n⏹  Stopped!")
        print_stats()

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' not installed!")
        print("\nInstall with: pip install requests")
        sys.exit(1)
    
    main()