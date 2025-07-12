import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

class GoogleKeywordDumper:
    def __init__(self, lang='en', country='us', delay=0.3, kill_threshold=5):
        self.lang = lang
        self.country = country
        self.delay = delay
        self.kill_threshold = kill_threshold
        self.base_url = "https://suggestqueries.google.com/complete/search"
        self.session = requests.Session()

    def _fetch_suggestions(self, keyword):
        params = {
            "client": "firefox",
            "q": keyword,
            "hl": self.lang,
            "gl": self.country
        }
        try:
            response = self.session.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()[1]
        except Exception as e:
            print(Fore.RED + f"[Error] Failed to fetch suggestions for '{keyword}': {e}")
            return []

    def dump_keywords(self, seed_keyword, limit=500):
        if limit > 500:
            raise ValueError("Limit cannot exceed 500.")
        
        keywords = set()
        queue = [seed_keyword]
        no_new_keyword_streak = 0

        while queue and len(keywords) < limit:
            current = queue.pop(0)
            suggestions = self._fetch_suggestions(current)

            print(Fore.YELLOW + f"[Fetching] '{current}' → {len(suggestions)} suggestions")

            new_count = 0
            for suggestion in suggestions:
                if suggestion not in keywords:
                    keywords.add(suggestion)
                    new_count += 1
                    if len(keywords) >= limit:
                        break
                    queue.append(suggestion)

            if new_count == 0:
                no_new_keyword_streak += 1
                print(Fore.RED + f"[Notice] 0 new keywords (streak {no_new_keyword_streak}/{self.kill_threshold})")
            else:
                no_new_keyword_streak = 0

            print(Fore.CYAN + f"[Progress] {len(keywords)} / {limit} keywords collected")

            if no_new_keyword_streak >= self.kill_threshold:
                print(Fore.MAGENTA + f"[Kill Switch] Too many dead-end fetches. Stopping early.")
                break

            time.sleep(self.delay)

        print(Fore.GREEN + f"[Complete] Collected {len(keywords)} keywords.")
        return sorted(keywords)
