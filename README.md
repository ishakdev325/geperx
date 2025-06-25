# 🌐 **GeperX - Elite Path Scanner**

**GeperX** is a next-generation cybersecurity tool designed for lightning-fast and intelligent path enumeration. Built with precision, it empowers security researchers to uncover hidden endpoints with unmatched efficiency. Featuring smart proxy rotation, advanced content analysis, and seamless fallback modes, GeperX is your ultimate weapon for penetration testing and bug bounty hunting.

---

## 🚀 **Features**

- **Blazing Fast Scanning**: Multi-threaded architecture with up to 20 concurrent threads for rapid path enumeration.  
- **Smart Proxy Management**: Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies loaded from a file, with intelligent rotation and fallback to direct mode.  
- **Dynamic Header Spoofing**: Randomized User-Agent, Referer, and other headers to evade detection.  
- **Content Analysis**: Detects sensitive endpoints (e.g., admin panels, login pages) and analyzes JSON/HTML responses.  
- **Customizable Delays**: Fine-tune request delays to bypass rate limits and optimize performance.  
- **JSON Output**: Structured results saved in JSON format for easy integration and analysis.  
- **Cross-Platform**: Fully compatible with Windows and Linux, with vibrant CLI output using colorama.  
- **Robust Error Handling**: Automatic retries, rate limit detection, and fallback mode ensure uninterrupted scans.

---

## 🛠 **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ishakdev325/geperx.git
   cd geperx
   ```

2. **Install Dependencies**:
   ```bash
   pip install requests PySocks colorama
   ```

3. **Prepare Files**:
   - Create a `wordlist.txt` with paths to scan (e.g., `admin`, `login`, `api`).
   - (Optional) Create a `proxies.txt` with proxies in the format:
     ```
     http://127.0.0.1:8080
     https://192.168.1.100:3128
     socks4://45.76.43.21:1080
     socks5://198.12.34.56:9050
     ```

---

## ⚙️ **Usage**

```bash
python geperx.py -u <target_url> -w <wordlist_file> [options]
```

### Options:

| Flag               | Description                            | Example              |
| ------------------ | -------------------------------------- | -------------------- |
| `-u, --url`        | Target URL (required)                  | `http://example.com` |
| `-w, --wordlist`   | Path to wordlist file (required)       | `wordlist.txt`       |
| `-t, --threads`    | Number of concurrent threads           | `25`                 |
| `-e, --exclude`    | Status codes to exclude                | `404,500`            |
| `-p, --proxy-file` | Path to proxy list file                | `proxies.txt`        |
| `--time`           | Delay between requests (in seconds)    | `0.2`                |
| `--fallback`       | Fallback to direct mode if proxy fails | `--fallback`         |

---

## 💡 **Example Commands**

**Basic scan without proxies**:
```bash
python geperx.py -u http://example.com -w wordlist.txt -t 20 -e 404,403 --time 0.2
```

**Scan with proxies and fallback**:
```bash
python geperx.py -u http://example.com -w wordlist.txt -p proxies.txt --time 0.1 --fallback
```

---

## 📁 **File Formats**

**wordlist.txt**:
```
admin
login
dashboard
api/v1
config
```

**proxies.txt**:
```
http://127.0.0.1:8080
https://192.168.1.100:3128
socks4://45.76.43.21:1080
socks5://198.12.34.56:9050
```

---

## 📊 **Output**

- **Console**: Real-time results with color-coded status (✅ green = success, ❌ red = errors, ⚠️ magenta = sensitive).
- **File**: Results saved as `geperx_results_YYYYMMDD_HHMMSS.json`.

```json
[
  {
    "status": 200,
    "details": "[200] http://example.com/admin [Content-Type: text/html | 5123 bytes] [Potential sensitive endpoint]"
  }
]
```

---

## ⚠️ **Legal Disclaimer**

GeperX is intended for authorized security testing and bug bounty programs. Unauthorized use against systems you do not have explicit permission to test is illegal. The developer is not responsible for misuse of this tool.

---

## 🌟 **Contributing**

- Fork the repository.
- Create a feature branch:
  ```bash
  git checkout -b feature/awesome-feature
  ```
- Commit your changes:
  ```bash
  git commit -m 'Add awesome feature'
  ```
- Push to the branch:
  ```bash
  git push origin feature/awesome-feature
  ```
- Open a Pull Request.

---

## 📬 **Contact**

- GitHub: [ishakdev325](https://github.com/ishakdev325)
- Twitter: [@ishakxdev](https://x.com/ishakxdev)
- Instagram: [@ishakdev](https://www.instagram.com/ishakdev/)
- X: [@ishakxdev](https://x.com/ishakxdev)

---

## 💪 **Built with Power**

GeperX is crafted with ❤️ for the cybersecurity community.
⭐ Star the repo if you find it useful!
