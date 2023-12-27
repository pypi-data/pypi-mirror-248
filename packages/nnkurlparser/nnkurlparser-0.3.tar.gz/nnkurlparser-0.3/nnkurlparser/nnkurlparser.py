import argparse
import urllib.parse
import os

def read_urls(input_filename, output_filename):
    url_parts = set()

    input_path = os.path.join(input_filename)
    output_path = os.path.join(output_filename)

    with open(input_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            url_string = line.strip()
            parsed_url = urllib.parse.urlparse(url_string)

            if parsed_url.path is not None:
                path_array = parsed_url.path.split('/')
                path_array = [part for part in path_array if part]  
                parts = [
                    f"{parsed_url.scheme}://{parsed_url.hostname}/{'/'.join(path_array[:index + 1])}/"
                    for index in range(len(path_array))
                ]
                url_parts.update(parts)

    urls = sorted(url_parts, key=len)
    print("\n".join(urls))

    with open(output_path, 'a') as save_file:
        for element in urls:
            save_file.write(f"{element}\n")

    return list(url_parts)

def main():
    parser = argparse.ArgumentParser(description="URL Parser")
    parser.add_argument("input_filename", help="Name of the input file")
    parser.add_argument("output_filename", help="Name of the output file")

    args = parser.parse_args()

    read_urls(args.input_filename, args.output_filename)

if __name__ == "__main__":
    main()
