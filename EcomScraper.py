"""Created with ❤ by Jishwuh, a Python enthusiast.
This script finds e-commerce sites based on keywords using Google search.

Cleaned up and optimized by Jishwuh + ChatGPT"""

import time
from urllib.parse import urlparse
import json
import os
import re
from datetime import datetime
import random

RESULTS_PER_KEYWORD = 100
SEARCH_PAUSE = 2.0
REQUEST_TIMEOUT = 5

os.system("cls" if os.name == "nt" else "clear")

print("Installing Required Packages...")

try:
    from colorama import Fore, Style, init
    print(Fore.GREEN + "colorama is already installed.")
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama")
    print(Fore.GREEN + "Installed colorama successfully.")
    init(autoreset=True)
try:
    from googlesearch import search
    print(Fore.GREEN + "googlesearch-python is already installed.")
except ImportError:
    os.system("pip install googlesearch-python")
    print(Fore.GREEN + "Installed googlesearch-python successfully.")
try:
    import requests
    print(Fore.GREEN + "requests is already installed.")
except ImportError:
    os.system("pip install requests")
    print(Fore.GREEN + "Installed requests successfully.")
try:
    from bs4 import BeautifulSoup
    print(Fore.GREEN + "beautifulsoup4 is already installed.")
except ImportError:
    os.system("pip install beautifulsoup4")
    print(Fore.GREEN + "Installed beautifulsoup4 successfully.")

from GoogleKeywordDumper import GoogleKeywordDumper

print(Fore.GREEN + Style.BRIGHT +
      r" _____                      ____                                 ")
print(Fore.GREEN + Style.BRIGHT +
      r"| ____|___ ___  _ __ ___   / ___|  ___ _ __ __ _ _ __   ___ _ __ ")
print(Fore.GREEN + Style.BRIGHT +
      r"|  _| / __/ _ \| '_ ` _ \  \___ \ / __| '__/ _` | '_ \ / _ \ '__|")
print(Fore.GREEN + Style.BRIGHT +
      r"| |__| (_| (_) | | | | | |  ___) | (__| | | (_| | |_) |  __/ |   ")
print(Fore.GREEN + Style.BRIGHT +
      r"|_____\___\___/|_| |_| |_| |____/ \___|_|  \__,_| .__/ \___|_|   ")
print(Fore.GREEN + Style.BRIGHT +
      r"                                                |_|              ")
print(Fore.CYAN + Style.BRIGHT + "EcomScraper - E-commerce Site Finder\n")
print(Fore.YELLOW + "Welcome to EcomScraper! This tool finds e-commerce sites based on keywords.\n")

def update_cmd_title(current_keyword: str, finished: int, total: int):
    safe_keyword = re.sub(r'[&|><^"]', '', current_keyword[:50])
    title = f"Checking: {safe_keyword} - {finished}/{total}"
    try:
        os.system(f"title {title}")
    except Exception as e:
        print(f"Failed to update title: {e}")

def ensure_required_files():
    if not os.path.exists("blacklist.txt"):
        with open("blacklist.txt", "w", encoding="utf-8") as f:
            f.write(
                "amazon.com\n"
                "ebay.com\n"
                "walmart.com\n"
                "# One domain per line\n"
                "# Lines starting with # are ignored as comments\n"
            )
        print(Fore.GREEN + "[Created] blacklist.txt")
        print(Fore.YELLOW + "→ Add one domain per line.\n")
        input(Fore.CYAN + "Press Enter to continue after editing blacklist.txt...")

def generate_keywords_interactively():
    print(Fore.MAGENTA + "\nWould you like to generate keywords using Google Autocomplete?")
    choice = input(Fore.CYAN + "Enter Y to generate from one seed keyword, or N to use your own list: ").strip().lower()
    
    if choice != 'y':
        return

    seed = input(Fore.CYAN + "Enter your seed keyword (e.g., 'wireless earbuds'): ").strip()
    while not seed:
        seed = input(Fore.RED + "Seed keyword cannot be empty. Please enter a valid keyword: ").strip()

    limit = input(Fore.CYAN + "How many keywords would you like to generate? (max 500): ").strip()
    try:
        limit = int(limit)
        if limit > 500:
            print(Fore.YELLOW + "Limiting to 500 keywords.")
            limit = 500
    except ValueError:
        print(Fore.YELLOW + "Invalid number entered. Defaulting to 100 keywords.")
        limit = 100

    dumper = GoogleKeywordDumper()
    keywords = dumper.dump_keywords(seed_keyword=seed, limit=limit)

    with open("keywords.txt", "w", encoding="utf-8") as f:
        for kw in keywords:
            f.write(kw + "\n")

    print(Fore.GREEN + f"\n✅ {len(keywords)} keywords saved to keywords.txt")
    print(Fore.YELLOW + "You can review or edit this list before continuing.\n")
    input(Fore.CYAN + "Press Enter to continue...")

    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w", encoding="utf-8") as f:
            f.write(
                "wireless earbuds\n"
                "gaming monitor\n"
                "# One keyword or phrase per line\n"
                "# Lines starting with # are ignored as comments\n"
            )
        print(Fore.GREEN + "[Created] keywords.txt")
        print(Fore.YELLOW + "→ Add one keyword per line.\n")
        input(Fore.CYAN + "Press Enter to continue after editing keywords.txt...")

def load_blacklist(filename="blacklist.txt"):
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                if "# One domain per line" in content:
                    print(
                        Fore.YELLOW + "Detected initial blacklist format. Please edit blacklist.txt to add domains.")
                    input(
                        Fore.CYAN + "Press Enter to continue after editing blacklist.txt...")
                else:
                    return [line.strip().lower() for line in content.splitlines() if line.strip()]
        except FileNotFoundError:
            print(
                Fore.RED + f"[?] Blacklist file '{filename}' not found. Proceeding with empty blacklist.")
            return []

def load_keywords(filename="keywords.txt"):
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                if "# One keyword or phrase per line" in content:
                    print(
                        Fore.YELLOW + "Detected initial keywords format. Please edit keywords.txt to add keywords.")
                    input(
                        Fore.CYAN + "Press Enter to continue after editing keywords.txt...")
                else:
                    return [line.strip() for line in content.splitlines() if line.strip()]
        except FileNotFoundError:
            print(
                Fore.RED + f"[?] Keywords file '{filename}' not found. Proceeding with empty keywords.")
            return []

def get_results_filename():
    raw_input = input(Fore.CYAN + "\nWhat keyword(s) are you targeting? (used for naming result file): ").strip()
    if not raw_input:
        raw_input = "unnamed"
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", raw_input).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{safe_name}_{timestamp}.txt"
    folder = "results"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)

def appendToValidFile(url: str, filename: str) -> None:
    with open(filename, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def is_ecommerce_site(url: str, proxy: str) -> bool:
    """
      - "add to cart", "shopping cart", "checkout", "cart", "buy now"
      - JSONLD script with "@type": "Product" - indicates product pages when indexing
    """
    try:
        if proxy:
            if "http" not in proxy:
                proxy = f"http://{proxy}"
        proxies = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers={
            "User-Agent": "Mozilla/5.0 (compatible; EcomScraper/1.0)"
        }, proxies=proxies)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print(Fore.RED + f"[Timeout] Took too long to respond.")
        return False
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        if code == 403:
            print(Fore.MAGENTA + f"[403 Forbidden] Access denied.")
        elif code == 404:
            print(Fore.RED + f"[404 Not Found] Does not exist.")
        else:
            print(Fore.RED + f"[HTTP {code}] Error accessing.")
        return False
    except requests.exceptions.ProxyError:
        print(Fore.RED + f"[Proxy Error] Could not connect to proxy.")
        return False
    except requests.exceptions.ConnectionError:
        print(Fore.RED + f"[Connection Error] Failed to connect.")
        return False
    except Exception as e:
        print(Fore.RED + f"[Unknown Error] - {str(e)}")
        return False
    
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ").lower()

    if any(kw in text for kw in ("add to cart", "shopping cart", "checkout", "cart",
                                 "buy now", "shop now", "order now", "purchase",
                                 "product page", "complete purchase", "continue shopping",
                                 "proceed to checkout", "view cart", "add to bag", "add to basket",
                                 "buy today", "grab it today", "treat yourself today",
                                 "shop the sale", "get free shipping", "redeem voucher",
                                 "claim offer", "get discount", "finalize order",
                                 "secure checkout", "place order", "confirm purchase", "buy today")):
        return True

    for script in soup.find_all("script", type="application/ld+json"):
        if script.string and '"@type": "Product"' in script.string:
            return True

    return False


def load_or_create_config(config_file="config.json"):
    def prompt(prompt_text, current_val, default_val, cast_type):
        while True:
            try:
                inp = input(
                    f"{prompt_text} (default: {default_val}) (Current: {current_val}): ").strip()
                return cast_type(inp) if inp else current_val
            except ValueError:
                print(Fore.RED + "Invalid input. Please try again.")

    config = {}

    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(Fore.YELLOW + f"Loaded configuration from {config_file}")

        change = input(Fore.CYAN + "Do you want to update your config settings? (Y/N): ").strip().lower()
        if change != 'y':
            return config

    print(Fore.MAGENTA + "\nUpdating configuration settings...\n")

    config['keywords_file'] = input(
        f"Enter path to keywords file (default: keywords.txt) (Current: {config.get('keywords_file', 'keywords.txt')}): ").strip() or config.get('keywords_file', 'keywords.txt')

    config['results_per_keyword'] = prompt(
        "Number of Google results to check per keyword",
        config.get('results_per_keyword', 100),
        100,
        int
    )

    config['request_timeout'] = prompt(
        "HTTP request timeout (seconds)",
        config.get('request_timeout', 5),
        5,
        int
    )

    config['search_pause'] = prompt(
        "Pause between searches (seconds)",
        config.get('search_pause', 2.0),
        2.0,
        float
    )

    config['max_keywords'] = prompt(
        "Max number of keywords to process (blank = no limit)",
        config.get('max_keywords', None),
        '',
        lambda x: int(x) if x else None
    )

    config['proxy'] = input(
        f"Enter proxy (user:pass@host:port or ip:port, leave blank for none) (Current: {config.get('proxy', 'None')}): ").strip() or config.get('proxy', None)

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    print(Fore.GREEN + f"\nConfiguration updated and saved to {config_file} !\n")

    return config


def safe_google_search(query, num_results, proxy=None, max_retries=5, cooldown=60):
    attempt = 0
    while attempt < max_retries:
        try:
            return list(search(query, num_results=num_results, proxy=proxy))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = cooldown + random.randint(10, 30)
                print(Fore.RED + f"[429 Too Many Requests] Rate limited. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                attempt += 1
            else:
                raise
        except Exception as e:
            print(Fore.RED + f"[Search Error] {e}")
            break
    print(Fore.RED + "[Failed] Max retries reached.")
    return []

def main():
    ensure_required_files()
    blacklist = load_blacklist()
    generate_keywords_interactively()
    keywords = load_keywords()
    print(Fore.YELLOW + f"Loaded {len(blacklist)} blacklisted domains.")
    print(Fore.YELLOW + f"Loaded {len(keywords)} keywords.")
    args = load_or_create_config()
    output_file = get_results_filename()

    global RESULTS_PER_KEYWORD, REQUEST_TIMEOUT, SEARCH_PAUSE
    RESULTS_PER_KEYWORD = args['results_per_keyword']
    REQUEST_TIMEOUT = args['request_timeout']
    SEARCH_PAUSE = args['search_pause']

    if args['max_keywords']:
        keywords = keywords[:args['max_keywords']]

    found_urls = set()

    for i, kw in enumerate(keywords, start=1):
        update_cmd_title(kw, i - 1, len(keywords))
        print(Fore.BLUE + f"\nSearching for e-commerce sites related to: {kw}")
        for url in safe_google_search(kw, num_results=RESULTS_PER_KEYWORD, proxy=args['proxy']):
            domain = urlparse(url).netloc.lower()
            if url in found_urls:
                continue
            if any(black in domain for black in blacklist):
                continue
            print(Fore.CYAN + f"{domain} ", end="", flush=True)
            result = is_ecommerce_site(url, args['proxy'])
            if result:
                print(Fore.GREEN + "[OK]")
                if not str(domain).startswith("http"):
                    domain = "https://" + domain if url.startswith("https") else "http://" + domain
                found_urls.add(domain)
                appendToValidFile(domain + " | " + url, filename=output_file)
            else:
                print(Fore.RED + "[X]", flush=True)

    with open(output_file, "w", encoding="utf-8") as out:
        for url in sorted(found_urls):
            out.write(url + "\n")

    print(Fore.GREEN + f"\n✅ Done! {len(found_urls)} site(s) saved to {output_file}")


if __name__ == "__main__":
    main()
