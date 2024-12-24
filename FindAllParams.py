import argparse
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor

def parse_url(url):
    try:
        return urllib.parse.urlparse(url)
    except Exception:
        return None

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
        return list(query_params.keys())  # Return a list of keys
    elif component == "values":
        query_params = urllib.parse.parse_qs(parsed.query)
        return [value for values in query_params.values() for value in values]
    elif component == "pairs":
        query_params = urllib.parse.parse_qsl(parsed.query)
        return [f"{k}={v}" for k, v in query_params]
    elif component == "joined-keys":
        query_params = urllib.parse.parse_qs(parsed.query)
        return "&".join(query_params.keys())  # Properly join keys
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
    try:
        with open(file_path, "r") as file:
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
                for item in results:
                    file.write(f"{item}\n")
    else:
        # Print to console if no output file is specified
        if output_format == "json":
            print(json.dumps(results, indent=4))
        elif output_format == "txt":
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
        results = sorted(set(results)) if args.unique else results
    elif args.component == "joined-keys":
        # Join all keys into a single &-delimited string
        results = "&".join(sorted(set(results))) if args.unique else "&".join(results)
    elif args.unique:
        results = sorted(set(results))

    output_results(results, args.output, args.format)

if __name__ == "__main__":
    main()
