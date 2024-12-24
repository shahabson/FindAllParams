# README for Final Second Script

## Overview
The second script is a URL parsing tool. It extracts specific components from URLs, such as the scheme, hostname, path, query parameters, and more.

### Features:
- Extract specific URL components (e.g., scheme, path, query keys).
- Parse subdomains and root domains.
- Multithreaded processing for handling large inputs.
- Option to output unique results.
- Flexible output formats (TXT or JSON).

## Usage

### Prerequisites
- Python 3.6 or higher
- Install required libraries:
  ```bash
  pip install requests
  ```

### Command-Line Arguments

| Argument        | Description                                                                 | Default    |
|-----------------|-----------------------------------------------------------------------------|------------|
| `--input`       | Input file containing URLs.                                                 | Required   |
| `--component`   | Component to extract (e.g., scheme, path, query, keys, root-domain).         | Required   |
| `--output`      | Output file to save results. If omitted, results are printed to the console.| None       |
| `--format`      | Output format (json or txt).                                                | txt        |
| `--unique`      | Ensure unique results.                                                      | False      |
| `--threads`     | Number of threads for parallel processing.                                  | 1          |

### Supported Components
- `scheme`: Extracts the URL scheme (e.g., `http`, `https`).
- `netloc`: Extracts the network location (e.g., `example.com`).
- `path`: Extracts the path segments (e.g., `/users`).
- `query`: Extracts the raw query string.
- `keys`: Extracts query string keys.
- `values`: Extracts query string values.
- `pairs`: Extracts key-value pairs from the query string.
- `root-domain`: Extracts the root domain (e.g., `example.com`).
- `subdomains`: Extracts subdomains (e.g., `sub.example.com` → `sub`).

### Examples

1. Extract root domains from `urls.txt` and save unique results:
   ```bash
   python script.py --input urls.txt --component root-domain --unique --output root_domains.txt
   ```

2. Extract query keys into a JSON file:
   ```bash
   python script.py --input urls.txt --component keys --format json --output query_keys.json
   ```

3. Extract paths and print results to the console:
   ```bash
   python script.py --input urls.txt --component path
   ```

4. Process URLs with 4 threads:
   ```bash
   python script.py --input urls.txt --component query --threads 4
   ```

