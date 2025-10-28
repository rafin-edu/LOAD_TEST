import requests
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import signal
import sys

# Configuration
WEBSITE_URL = "https://yaeko-pajamaed-contrapuntally.ngrok-free.dev/"  # Change this to your website URL
DELAY = 0.1  # 0.1 seconds between requests
MAX_WORKERS = 5  # Number of concurrent threads

# Global variables
visit_count = 0
running = True
start_time = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n\n🛑 Stopping... Please wait...")
    running = False

def visit_website():
    """Send a single visit request to the website"""
    global visit_count
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(WEBSITE_URL, headers=headers, timeout=10)
        visit_count += 1
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        if response.status_code == 200:
            print(f"[{timestamp}] ✅ Visit #{visit_count} - Status: {response.status_code}")
            return True
        else:
            print(f"[{timestamp}] ⚠️  Visit #{visit_count} - Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏱️  Visit #{visit_count + 1} - Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Visit #{visit_count + 1} - Connection Error")
        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Visit #{visit_count + 1} - Error: {str(e)}")
        return False

def print_stats():
    """Print statistics"""
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    rate = visit_count / elapsed if elapsed > 0 else 0
    
    print("\n" + "="*60)
    print(f"📊 STATISTICS")
    print("="*60)
    print(f"Total Visits Sent: {visit_count}")
    print(f"Running Time: {minutes}m {seconds}s")
    print(f"Average Rate: {rate:.2f} visits/second")
    print(f"Target Rate: {1/DELAY:.1f} visits/second")
    print("="*60 + "\n")

def main():
    """Main function"""
    global running, start_time
    
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("="*60)
    print("🚀 AUTO VISITOR - Python Edition")
    print("="*60)
    print(f"Target URL: {WEBSITE_URL}")
    print(f"Delay: {DELAY} seconds ({1/DELAY:.1f} visits/second)")
    print(f"Concurrent Workers: {MAX_WORKERS}")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    if not WEBSITE_URL.startswith(('http://', 'https://')):
        print("❌ Error: URL must start with http:// or https://")
        return
    
    start_time = time.time()
    
    try:
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while running:
                executor.submit(visit_website)
                time.sleep(DELAY)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        running = False
        print("\n\n⏹  Stopped!")
        print_stats()

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found!")
        print("\nInstall it with: pip install requests")
        sys.exit(1)
    
    main()