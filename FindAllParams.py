import argparse
import urllib.parse
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def parse_url(url):
    try:
        return urllib.parse.urlparse(url)
    except Exception:
        return None

def get_latest_commoncrawl_index():
    """
    Fetch the latest Common Crawl index dynamically.
    """
    try:
        response = requests.get("http://index.commoncrawl.org/")
        response.raise_for_status()
        # Example of fetching the latest index dynamically
        return "CC-MAIN-2023-51"  # Replace with dynamic logic if needed
    except Exception as e:
        print(f"Error fetching latest Common Crawl index: {e}")
        return None

def fetch_commoncrawl_urls(domain):
    """
    Fetch URLs from Common Crawl for the given domain.
    """
    latest_index = get_latest_commoncrawl_index()
    if not latest_index:
        print("Unable to determine the latest Common Crawl index.")
        return []

    commoncrawl_url = f"http://index.commoncrawl.org/{latest_index}-index"
    params = {
        "url": f"*.{domain}",
        "output": "json",
        "filter": "statuscode:200",
    }
    try:
        response = requests.get(commoncrawl_url, params=params)
        response.raise_for_status()
        data = response.json()
        return [entry['url'] for entry in data]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Common Crawl: {e}")
        return []

def extract_components(url, component):
    parsed = parse_url(url)
    if not parsed:
        return None

    if component == "scheme":
        return parsed.scheme
    elif component == "netloc":
        return parsed.netloc
    elif component == "path":
        return parsed.path
    elif component == "params":
        return parsed.params
    elif component == "query":
        return parsed.query
    elif component == "fragment":
        return parsed.fragment
    elif component == "keys":
        query_params = urllib.parse.parse_qs(parsed.query)
        return list(query_params.keys())
    elif component == "values":
        query_params = urllib.parse.parse_qs(parsed.query)
        return [value for values in query_params.values() for value in values]
    elif component == "pairs":
        query_params = urllib.parse.parse_qsl(parsed.query)
        return [f"{k}={v}" for k, v in query_params]
    elif component == "joined-keys":
        query_params = urllib.parse.parse_qs(parsed.query)
        return "&".join(query_params.keys())
    elif component == "root-domain":
        return extract_root_domain(parsed.netloc)
    elif component == "subdomains":
        return extract_subdomains(parsed.netloc)
    else:
        return None

def extract_root_domain(netloc):
    if not netloc:
        return None
    parts = netloc.split('.')
    if len(parts) > 1:
        return ".".join(parts[-2:])
    return netloc

def extract_subdomains(netloc):
    if not netloc:
        return None
    parts = netloc.split('.')
    if len(parts) > 2:
        return ".".join(parts[:-2])
    return None

def parse_urls_from_file(file_path):
    """
    Read URLs from a file with UTF-8 encoding.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def output_results(results, output_file, output_format):
    if output_file:
        if output_format == "json":
            with open(output_file, "w") as file:
                json.dump(results, file, indent=4)
        elif output_format == "txt":
            with open(output_file, "w") as file:
                if isinstance(results, str):
                    file.write(results)
                else:
                    for item in results:
                        file.write(f"{item}\n")
    else:
        # Print to console if no output file is specified
        if output_format == "json":
            print(json.dumps(results, indent=4))
        elif output_format == "txt":
            if isinstance(results, str):
                print(results)
            else:
                for item in results:
                    print(item)

def main():
    parser = argparse.ArgumentParser(description="Extract components from URLs.")
    parser.add_argument("--input", help="Input file containing URLs.", required=True)
    parser.add_argument(
        "--component",
        help="Component to extract (scheme, netloc, path, params, query, fragment, keys, values, pairs, joined-keys, root-domain, subdomains).",
        required=True,
    )
    parser.add_argument("--output", help="Output file to save results.", default=None)
    parser.add_argument("--format", help="Output format (json or txt).", default="txt")
    parser.add_argument("--unique", help="Ensure unique results.", action="store_true")
    parser.add_argument("--threads", type=int, help="Number of threads for processing.", default=1)
    args = parser.parse_args()

    urls = parse_urls_from_file(args.input)

    if not urls:
        print("No valid URLs found in input file.")
        return

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(extract_components, url, args.component) for url in urls]
        for future in futures:
            result = future.result()
            if result:
                if isinstance(result, list):
                    results.extend(result)
                else:
                    results.append(result)

    if args.component == "keys":
        # Flatten the list of keys and handle uniqueness
        flat_results = []
        for result in results:
            if isinstance(result, list):
                flat_results.extend(result)
            else:
                flat_results.append(result)
        results = sorted(set(flat_results)) if args.unique else flat_results

    elif args.component == "joined-keys":
        # Join all keys into a single &-delimited string
        flat_results = []
        for result in results:
            if isinstance(result, list):
                flat_results.extend(result)
            else:
                flat_results.append(result)
        results = "&".join(sorted(set(flat_results))) if args.unique else "&".join(flat_results)

    elif args.unique:
        results = sorted(set(results))

    output_results(results, args.output, args.format)

if __name__ == "__main__":
    main()
