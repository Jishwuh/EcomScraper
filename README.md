# 🛒 EcomScraper - E-commerce Site Finder

**EcomScraper** is a Python-based tool that scrapes Google search results for specified keywords, filters out blacklisted domains, and checks if the remaining websites are e-commerce stores based on keyword presence or structured data.

---

## 📦 Features

- Google search integration for keyword discovery  
- Automatic detection of e-commerce sites  
- Custom blacklist to avoid known domains  
- Input-based configuration saved to `config.json`  
- Auto-generation of required files (`keywords.txt`, `blacklist.txt`)  
- Optional proxy support  
- Output of valid e-commerce domains in `valid_urls.txt` and `ecommerce_sites.txt`  
- Color-coded and clean terminal output  

---

## 🔧 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

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
- Create a `keywords.txt` file with sample keywords
- Create a `blacklist.txt` with default domains to exclude
- Prompt you for configuration (saved in `config.json`)

### 3. Fill Out `keywords.txt`

Open the file and input one keyword or product phrase per line:

```
wireless earbuds
gaming laptop
ergonomic chair
```

Lines starting with `#` are treated as comments.

### 4. Edit `blacklist.txt` (Optional)

Add domains to exclude from results (e.g., Amazon, Walmart):

```
amazon.com
ebay.com
```

### 5. Configure the Tool (First Run)

You'll be prompted to input:
- Path to keyword file
- Number of Google results per keyword
- HTTP request timeout
- Delay between searches
- Max number of keywords to use
- Proxy (optional, format: `http://user:pass@host:port`)

All values are saved in `config.json` and reused in future runs.

---

## 📄 Output Files

- `valid_urls.txt` – raw list of valid e-commerce site matches with source URL  
- `ecommerce_sites.txt` – clean deduplicated list of valid e-commerce domains  

---

## 🖥 Terminal Compatibility

For best results, use:
- ✅ Windows Terminal or VSCode terminal (for proper symbol/emoji rendering)
- ✅ UTF-8 compatible font like Cascadia Code or Segoe UI Emoji

If emojis like `✓` or `✗` appear as `?`, switch terminals or use ASCII mode instead.

---

## 🔐 Proxy Support

To avoid Google rate limits, you can use a proxy:
- Format: `user:pass@host:port` or `ip:port`
- Leave blank to skip

---

## ✅ Example Run

```
Enter number of Google results to check per keyword (default: 100): 50
Enter HTTP request timeout in seconds (default: 5): 3
Enter proxy (leave blank for none): 127.0.0.1:8080

Loaded 65 blacklisted domains.
Loaded 3 keywords.

Searching for e-commerce sites related to: wireless earbuds
→ https://somebrand.com [OK]
→ https://amazon.com [X] (blacklisted)

✅ Done! 1 site(s) saved to ecommerce_sites.txt
```

---

## 🧠 Tips

- Use long-tail keywords for better targeting (e.g., `best outdoor camping gear`)
- Update blacklist regularly to avoid spammy results
- Rotate proxies or search pauses to avoid blocking

---

## 📬 Support

For questions or suggestions, feel free to open an issue or request improvements.

---

**Made with ❤️ for finding hidden e-commerce gems.**
