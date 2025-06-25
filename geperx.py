import requests
from urllib.parse import urljoin
import time
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
import os
from queue import Queue
from threading import Lock
import socks
import socket
import warnings
import urllib3
from colorama import init, Fore, Style
import sys
import json

# تهيئة colorama للتوافق مع ويندوز ولينكس
init(autoreset=True)

class GeperX:
    def __init__(self, target_url, wordlist_file, exclude_codes, proxy_file, delay, fallback):
        self.target_url = target_url.rstrip('/')
        self.wordlist_file = wordlist_file
        self.exclude_codes = [int(code) for code in exclude_codes.split(',')] if exclude_codes else []
        self.proxy_file = proxy_file
        self.successful_paths = []
        self.result_lock = Lock()
        self.delay = float(delay) if delay else random.uniform(0.05, 0.3)
        self.fallback = fallback
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        self.accept_headers = [
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'application/json,text/html,*/*;q=0.9',
            'text/html,*/*;q=0.7'
        ]
        self.common_headers = {
            'Accept-Language': 'en-US,en;q=0.8,ar;q=0.6',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1'
        }
        self.session = requests.Session()
        self.session.verify = False
        self.max_retries = 6
        self.timeout = 4
        self.rate_limit_delay = Queue()
        self.rate_limit_delay.put(self.delay)
        self.proxies = self.load_proxies()
        self.current_proxy_index = 0

    def load_proxies(self):
        proxies = []
        if self.proxy_file:
            if not os.path.exists(self.proxy_file):
                if self.fallback:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}[*] Proxy file {self.proxy_file} not found. Running in direct mode.{Style.RESET_ALL}")
                    return []
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}[-] Proxy file {self.proxy_file} not found!{Style.RESET_ALL}")
                    sys.exit(1)
            with open(self.proxy_file, 'r', encoding='utf-8', errors='ignore') as file:
                proxies = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            print(f"{Fore.GREEN}{Style.BRIGHT}[*] Loaded {len(proxies)} proxies from {self.proxy_file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}{Style.BRIGHT}[*] No proxy file provided. Running in direct mode.{Style.RESET_ALL}")
        return proxies

    def setup_proxy(self):
        with self.result_lock:
            if not self.proxies:
                self.session.proxies = {}
                socket.socket = socket._socket.socket
                return True
            proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
            try:
                proxy_type, proxy_addr = proxy.split('://', 1)
                proxy_host, proxy_port = proxy_addr.split(':')
                proxy_port = int(proxy_port)

                if proxy_type.lower() in ['http', 'https']:
                    self.session.proxies = {
                        'http': f'{proxy_type}://{proxy_addr}',
                        'https': f'{proxy_type}://{proxy_addr}'
                    }
                    socket.socket = socket._socket.socket
                elif proxy_type.lower() == 'socks4':
                    socks.set_default_proxy(socks.SOCKS4, proxy_host, proxy_port)
                    socket.socket = socks.socksocket
                elif proxy_type.lower() == 'socks5':
                    socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
                    socket.socket = socks.socksocket
                print(f"{Fore.GREEN}{Style.BRIGHT}[*] Using proxy: {proxy}{Style.RESET_ALL}")
                return True
            except (ValueError, Exception) as e:
                print(f"{Fore.RED}{Style.BRIGHT}[-] Invalid proxy {proxy}: {str(e)}{Style.RESET_ALL}")
                if self.fallback:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}[*] Switching to direct mode due to proxy failure.{Style.RESET_ALL}")
                    self.session.proxies = {}
                    socket.socket = socket._socket.socket
                    return True
                return False

    def display_banner(self):
        banner = f"""
{Fore.GREEN}{Style.BRIGHT}
 $$$$$$\                                         $$\   $$\ 
$$  __$$\                                        $$ |  $$ |
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\ \$$\ $$  |
$$ |$$$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ \$$$$  / 
$$ |\_$$ |$$$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|$$  $$<  
$$ |  $$ |$$   ____|$$ |  $$ |$$   ____|$$ |     $$  /\$$\ 
\$$$$$$  |\$$$$$$$\ $$$$$$$  |\$$$$$$$\ $$ |     $$ /  $$ |
 \______/  \_______|$$  ____/  \_______|\__|     \__|  \__|
                    $$ |                                   
                    $$ |                                   
                    \__|                                   
{Style.RESET_ALL}
"""
        print(banner)

    def get_dynamic_headers(self):
        headers = self.common_headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        headers['Accept'] = random.choice(self.accept_headers)
        headers['Referer'] = f"{self.target_url}/{random.choice(['home', 'index', 'page', str(random.randint(1, 1000))])}"
        headers['X-Forwarded-For'] = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        headers['X-Requested-With'] = random.choice(['XMLHttpRequest', 'GeperX', ''])
        headers['Sec-Fetch-Site'] = random.choice(['same-origin', 'cross-site'])
        headers['Sec-Fetch-Mode'] = random.choice(['navigate', 'cors'])
        headers['Accept-Encoding'] = random.choice(['gzip, deflate', 'br', ''])
        return headers

    def analyze_response(self, response, full_url):
        content_type = response.headers.get('Content-Type', 'Unknown')
        content_length = len(response.content)
        analysis = f" [Content-Type: {content_type} | {content_length} bytes]"
        if 'text/html' in content_type.lower():
            keywords = ['login', 'admin', 'dashboard', 'api_key', 'panel', 'control']
            if any(keyword in response.text.lower() for keyword in keywords):
                analysis += f"{Fore.MAGENTA}{Style.BRIGHT} [Potential sensitive endpoint]{Style.RESET_ALL}"
        elif 'json' in content_type.lower():
            try:
                data = response.json()
                analysis += f" [JSON: {json.dumps(data)[:50]}...]"
            except:
                pass
        return analysis

    def test_path(self, path):
        full_url = urljoin(self.target_url, path.strip())
        delay = self.rate_limit_delay.get()
        time.sleep(delay)

        for attempt in range(self.max_retries):
            if not self.setup_proxy():
                self.current_proxy_index += 1
                continue
            try:
                headers = self.get_dynamic_headers()
                response = self.session.get(full_url, headers=headers, timeout=self.timeout, allow_redirects=True)

                if response.status_code not in self.exclude_codes:
                    with self.result_lock:
                        analysis = self.analyze_response(response, full_url)
                        result = f"{Fore.RED}{Style.BRIGHT}[{response.status_code}] {full_url}{Fore.GREEN}{Style.BRIGHT}{analysis}{Style.RESET_ALL}"
                        self.successful_paths.append((response.status_code, result))
                        print(result)

                if response.status_code == 429:
                    new_delay = min(delay * 2.5, 12)
                    self.rate_limit_delay.put(new_delay)
                    print(f"{Fore.YELLOW}{Style.BRIGHT}[*] Rate limit hit, delaying {new_delay:.2f}s{Style.RESET_ALL}")
                    time.sleep(new_delay)
                    self.current_proxy_index += 1
                    continue

                self.rate_limit_delay.put(max(self.delay, delay * 0.9))
                break
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(random.uniform(0.7, 2))
                    self.current_proxy_index += 1
                    continue
                with self.result_lock:
                    print(f"{Fore.RED}{Style.BRIGHT}Flavors detected: {full_url} - {str(e)}{Style.RESET_ALL}")
                self.rate_limit_delay.put(delay)
                break

        self.rate_limit_delay.put(delay)

    def load_wordlist(self):
        if not os.path.exists(self.wordlist_file):
            print(f"{Fore.RED}{Style.BRIGHT}[-] Wordlist file {self.wordlist_file} not found!{Style.RESET_ALL}")
            sys.exit(1)
        with open(self.wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
            paths = {line.strip() for line in file if line.strip() and not line.startswith('#')}
            print(f"{Fore.GREEN}{Style.BRIGHT}[*] Loaded {len(paths)} unique paths{Style.RESET_ALL}")
            return list(paths)

    def save_results(self):
        output_file = f"geperx_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
        results = [{"status": code, "details": detail.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Fore.MAGENTA, '').replace(Style.RESET_ALL, '')} 
                   for code, detail in self.successful_paths]
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Results saved to {output_file}{Style.RESET_ALL}")

    def run(self, max_workers=20):
        self.display_banner()
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Target: {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Excluding status codes: {self.exclude_codes or 'None'}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Delay between requests: {self.delay}s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Fallback mode: {'Enabled' if self.fallback else 'Disabled'}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}[*] Scanning with {max_workers} threads...{Style.RESET_ALL}")

        paths = self.load_wordlist()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.test_path, paths)
        
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}[*] Scan completed!{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}[*] Found {len(self.successful_paths)} valid paths:{Style.RESET_ALL}")
        self.successful_paths.sort()
        for _, path in self.successful_paths:
            print(path)
        
        self.save_results()

def main():
    parser = argparse.ArgumentParser(description=f"{Fore.GREEN}{Style.BRIGHT}GeperX - Elite Path Scanner{Style.RESET_ALL}", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of concurrent threads (default: 20)")
    parser.add_argument("-e", "--exclude", help="Comma-separated status codes to exclude (e.g., 404,500)")
    parser.add_argument("-p", "--proxy-file", help="Path to proxy list file (e.g., proxies.txt)")
    parser.add_argument("--time", type=float, help="Delay between requests in seconds (e.g., 0.2)")
    parser.add_argument("--fallback", action="store_true", help="Fallback to no-proxy mode if proxy fails")
    args = parser.parse_args()

    warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
    
    tester = GeperX(args.url, args.wordlist, args.exclude, args.proxy_file, args.time, args.fallback)
    tester.run(max_workers=args.threads)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}{Style.BRIGHT}[!] Scan stopped by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}[-] Critical error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
