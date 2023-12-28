# Yt-cc-dl

🚀 Command-line program to download cleaned up closed captions (subtitles) of channels from YouTube.com in JSON format.

[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.7-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) 


## Requirements
- 🐍 [python>=3.7](https://www.python.org/downloads/)


## ⬇️ Installation

```sh
pip install -U yt-cc-dl
```


## ⌨️ Usage

```
➜ yt-cc-dl --help

usage: yt-cc-dl [-h] [-o OUTPUT_DIR] [-l LANGUAGES] [-i INDENT] [-r] [-d]
              channel [channel ...]

positional arguments:
  channel               Single or multiple YouTube channel URL(s)

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory name or path (default: channel name)
  -l LANGUAGES, --languages LANGUAGES
                        Comma-separated list of languages to download (can be
                        regex). The list may contain "all" for all available
                        languages. The language can be prefixed with a "-" to
                        exclude it from the requested languages (e.g.,
                        all,-live_chat)
  -i INDENT, --indent INDENT
                        Indentation size in the output JSON files (None by
                        default)
  -r, --rich-data       Add a unique index and include the title and thumbnail
                        in every subtitle entry (useful for Meilisearch)
  -d, --disable-multithreading
                        Disable multithreading
```

## 📝 Todo

- [ ] Enable downloading the cc of a single video.
