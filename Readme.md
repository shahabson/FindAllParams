## Overview
This script extracts various components from URLs, including query parameters, paths, domains, and more. It also supports advanced features such as joining query parameter keys into a single string and ensuring unique results. The script is multithreaded for faster processing of large URL lists.

### Features
- Extract specific URL components:
  - Scheme (`http`, `https`, etc.)
  - Netloc (host and port)
  - Path (e.g., `/users`)
  - Query string components (keys, values, key-value pairs)
  - Fragment (`#fragment`)
  - Root domain and subdomains
- Join query parameter keys into a single `&`-delimited string.
- Ensure unique results.
- Multithreaded processing for large input files.
- Flexible output formats: JSON or TXT.

## Prerequisites
- Python 3.6 or higher
- Install required libraries:
  ```bash
  pip install requests
  ```

## Usage

### Command-Line Arguments
| Argument        | Description                                                                 | Default    |
|-----------------|-----------------------------------------------------------------------------|------------|
| `--input`       | Input file containing URLs.                                                 | Required   |
| `--component`   | Component to extract (see supported components below).                      | Required   |
| `--output`      | Output file to save results. If omitted, results are printed to the console.| None       |
| `--format`      | Output format (json or txt).                                                | txt        |
| `--unique`      | Ensure unique results.                                                      | False      |
| `--threads`     | Number of threads for parallel processing.                                  | 1          |

### Supported Components
- `scheme`: Extracts the URL scheme (e.g., `http`, `https`).
- `netloc`: Extracts the network location (e.g., `example.com`).
- `path`: Extracts the path segments (e.g., `/users`).
- `params`: Extracts the parameters (if any).
- `query`: Extracts the raw query string.
- `keys`: Extracts query string keys (one per line).
- `values`: Extracts query string values (one per line).
- `pairs`: Extracts key-value pairs from the query string.
- `joined-keys`: Joins all query string keys into a single `&`-delimited string.
- `root-domain`: Extracts the root domain (e.g., `example.com`).
- `subdomains`: Extracts subdomains (e.g., `sub.example.com` → `sub`).

### Examples

1. **Extract Query Keys**:
   ```bash
   python script.py --input urls.txt --component keys
   ```
   Output:
   ```
   id
   name
   action
   post_id
   ```

2. **Extract Unique Query Keys**:
   ```bash
   python script.py --input urls.txt --component keys --unique
   ```
   Output:
   ```
   action
   id
   name
   post_id
   ```

3. **Join Query Keys**:
   ```bash
   python script.py --input urls.txt --component joined-keys
   ```
   Output:
   ```
   id&name&action&post_id
   ```

4. **Extract Root Domains**:
   ```bash
   python script.py --input urls.txt --component root-domain
   ```
   Output:
   ```
   example.com
   test.net
   ```

5. **Save Results to a File**:
   ```bash
   python script.py --input urls.txt --component keys --output keys.txt
   ```

6. **Process URLs with Multiple Threads**:
   ```bash
   python script.py --input urls.txt --component keys --threads 4
   ```

## Notes
- The script assumes that the input file contains one URL per line.
- If `--unique` is specified, duplicate results are removed, and the output is sorted.

## License
This script is open-source and free to use under the MIT license.
