# 🛒 EcomScraper - E-commerce Site Finder

**EcomScraper** is a Python-based tool that scrapes Google search results for specified keywords, filters out blacklisted domains, and checks if the remaining websites are e-commerce stores based on keyword presence or structured data.

---

## 📦 Features

- Google search integration for keyword discovery  
- Optional **Google Autocomplete keyword generator** (via seed + limit)
- Automatic detection of e-commerce sites  
- Smart retry system on Google 429 errors (with cooldown + retry limit)  
- Live-updating **Command Prompt title** with progress tracking  
- Interactive config editor showing current values before changing  
- Custom blacklist to avoid known domains  
- Input-based configuration saved to `config.json`  
- Auto-generation of required files (`keywords.txt`, `blacklist.txt`)  
- Optional proxy support  
- Output results saved to **timestamped files** in the `/results` folder  
- Color-coded and clean terminal output  
- Kill switch if keyword expansion returns too few new suggestions  
- Live feedback on keyword generation progress using `colorama`  

---

## 🔧 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
````

Or let the script auto-install what's missing when run.

### `requirements.txt` includes:

```
requests
beautifulsoup4
googlesearch-python
colorama
```

---

## 🚀 How to Use

### 1. Clone or Download the Script

Place the script in a folder where you want results saved.

### 2. Run the Script

```bash
python EcomScraper.py
```

On the first run, it will:

* Ask if you'd like to generate keywords from Google autocomplete
* Create a `keywords.txt` file with sample keywords
* Create a `blacklist.txt` with default domains to exclude
* Prompt you for configuration (saved in `config.json`)

### 3. Choose Your Keywords

* You can **manually enter keywords** in `keywords.txt`, or
* **Automatically generate them** by entering a seed keyword (e.g., "gaming mouse") and a limit (up to 500). The tool will fetch autocomplete suggestions and write them to `keywords.txt`.

Lines starting with `#` are treated as comments.

### 4. Edit `blacklist.txt` (Optional)

Add domains to exclude from results (e.g., Amazon, Walmart):

```
amazon.com
ebay.com
```

### 5. Configure the Tool (First Run or On Demand)

You’ll be prompted to input:

* Path to keyword file
* Number of Google results per keyword
* HTTP request timeout
* Delay between searches
* Max number of keywords to use
* Proxy (optional)

If `config.json` already exists, you'll be asked if you want to update it.
Current values will be shown for reference.

---

## 📄 Output Files

* Results are saved in `/results` as:

  ```
  <keyword>_YYYY-MM-DD_HH-MM-SS.txt
  ```
* Each file contains deduplicated, valid e-commerce domains with their source URLs

---

## 🔐 Proxy Support

To avoid Google rate limits, you can use a proxy:

* Format: `user:pass@host:port` or `ip:port`
* Leave blank to skip

The tool also implements retry logic for Google’s 429 errors (Too Many Requests) with a cooldown and retry limit.

---

## ✅ Example Run

```
Would you like to generate keywords using Google Autocomplete? (Y/N): Y
Enter your seed keyword: wireless earbuds
How many keywords would you like to generate? (max 500): 100
✅ 100 keywords saved to keywords.txt

Do you want to update your config settings? (Y/N): N

Loaded 3 keywords.
Loaded 65 blacklisted domains.

Searching for e-commerce sites related to: wireless earbuds
→ www.brandx.com [OK]
→ www.amazon.com [X] (blacklisted)

✅ Done! 1 site(s) saved to results/wireless_earbuds_2025-07-11_22-16-02.txt
```

---

## 🧠 Tips

* Use long-tail keywords for better targeting (e.g., `best budget gaming monitor 2025`)
* Rotate proxies or increase search pauses to avoid Google blocks
* Update your blacklist regularly to clean up results
* Use the Google Autocomplete feature to get long-tail, real-world queries

---

## 📬 Support

For questions or suggestions, feel free to open an issue or request improvements.

---

**Made with ❤️ for finding hidden e-commerce gems.**
