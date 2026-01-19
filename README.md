# XIMP - Twitter Impersonation Scanner

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20Ubuntu%20|%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**XIMP** is a powerful OSINT tool designed for cybersecurity professionals to detect impersonation accounts on X (formerly Twitter). It utilizes advanced fuzzing techniques, homoglyph detection, and search engine scraping to identify malicious handles targeting your brand.

## Features

- **Advanced Permutations**: Detects typosquatting, homoglyphs (e.g., `rn` vs `m`), and common keyword suffixes (`support`, `official`).
- **Dual Scanning Engines**:
  - **SERP Discovery**: Uses Google Dorking to find indexed impersonation profiles.
  - **Direct Probing**: Validates existence of potential handles directly.
- **Stealth**: Uses User-Agent rotation to minimize blocking.
- **Professional Reports**: Clean, table-based CLI output.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SanketShewale/XIMP.git
   cd XIMP
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool interactively:
```bash
python ximp.py
```
*(You will be prompted to enter an optional SerpApi Key for enhanced results)*

Or provide the target username as an argument:
```bash
python ximp.py target_username
```

## Example

Scanning for `example`:
```
[*] Phase 1: Search Engine Discovery
Found 2 indexed profiles via Google.

[*] Phase 2: Direct Username Scanning
Checking profiles... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:15

=== REPORT ===
Potential Impersonators for 'example'
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Username          ┃ URL                           ┃ Method ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ example           │ https://x.com/example         │ SERP   │
│ examplesupport    │ https://x.com/examplesupport  │ Direct │
│ example_official  │ https://x.com/example_official│ Direct │
└───────────────────┴───────────────────────────────┴────────┘
```

## Disclaimer

This tool is for educational and defensive purposes only. The author (SanketShewale) is not responsible for any misuse.

## License

MIT License. See [LICENSE](LICENSE) for details.

---
Created by **SanketShewale**
