"""Created with ❤ by Jishwuh, a Python enthusiast.
This script finds e-commerce sites based on keywords using Google search.

Cleaned up and optimized by Jishwuh + ChatGPT"""

import time
from urllib.parse import urlparse
import json
import os
import traceback

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


def appendToValidFile(url: str, filename: str = "valid_urls.txt") -> None:
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
    except Exception as e:
        print(traceback.format_exc())
        print(Fore.RED + f"Error fetching {url}: {e}")
        time.sleep(SEARCH_PAUSE)
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
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(Fore.YELLOW + f"Loaded configuration from {config_file}")
        return config

    print(Fore.CYAN + "No config file found. Please enter settings:\n")

    def prompt(prompt_text, default_val, cast_type):
        while True:
            try:
                inp = input(
                    f"{prompt_text} (default: {default_val}): ").strip()
                return cast_type(inp) if inp else default_val
            except ValueError:
                print(Fore.RED + "Invalid input. Please try again.")

    config = {
        "keywords_file": input("Enter path to keywords file (default: keywords.txt): ").strip() or "keywords.txt",
        "results_per_keyword": prompt("Number of Google results to check per keyword", 100, int),
        "request_timeout": prompt("HTTP request timeout (seconds)", 5, int),
        "search_pause": prompt("Pause between searches (seconds)", 2.0, float),
        "max_keywords": prompt("Max number of keywords to process (blank = no limit)", None, lambda x: int(x) if x else None),
        "proxy": input("Enter proxy (user:pass@host:port or ip:port, leave blank for none): ").strip() or None
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    print(Fore.GREEN + f"\nConfiguration saved to {config_file} ✅\n")
    return config


def main():
    ensure_required_files()
    blacklist = load_blacklist()
    keywords = load_keywords()
    print(Fore.YELLOW + f"Loaded {len(blacklist)} blacklisted domains.")
    print(Fore.YELLOW + f"Loaded {len(keywords)} keywords.")
    args = load_or_create_config()

    global RESULTS_PER_KEYWORD, REQUEST_TIMEOUT, SEARCH_PAUSE
    RESULTS_PER_KEYWORD = args['results_per_keyword']
    REQUEST_TIMEOUT = args['request_timeout']
    SEARCH_PAUSE = args['search_pause']

    if args['max_keywords']:
        keywords = keywords[:args['max_keywords']]

    found_urls = set()

    for kw in keywords:
        print(Fore.BLUE + f"\nSearching for e-commerce sites related to: {kw}")
        for url in search(kw, num_results=RESULTS_PER_KEYWORD, proxy=args['proxy']):
            domain = urlparse(url).netloc.lower()
            if url in found_urls:
                continue
            if any(black in domain for black in blacklist):
                continue
            print(Fore.CYAN + f"{domain} ", end="", flush=True)
            if is_ecommerce_site(url, args['proxy']):
                print(Fore.GREEN + " [OK]")
                if not str(domain).startswith("http"):
                    domain = "https://" + \
                        domain if url.startswith(
                            "https") else "http://" + domain
                found_urls.add(domain)
                appendToValidFile(domain + " | " + url)
            else:
                print(Fore.RED + " [X]")

    with open("ecommerce_sites.txt", "w", encoding="utf-8") as out:
        for url in sorted(found_urls):
            out.write(url + "\n")

    print(f"\n✅ Done! {len(found_urls)} site(s) saved to ecommerce_sites.txt")


if __name__ == "__main__":
    main()
