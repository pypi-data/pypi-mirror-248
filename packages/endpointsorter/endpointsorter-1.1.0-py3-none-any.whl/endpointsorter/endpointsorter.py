import re
import argparse
import sys


def main():
    try:
        parser = argparse.ArgumentParser(description="Url Endpoint Sorter")
        parser.add_argument(
            "-i", "--input", required=True, help="Specify the input file."
        )
        parser.add_argument(
            "-o", "--output", required=True, help="Specify the output file."
        )
        args = parser.parse_args()
        input_file = args.input.strip().lower()
        output_file = args.output.strip().lower()
        sortUrls(input_file, output_file)
    except KeyboardInterrupt:
        print("\nExecution interrupted by the user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def sortUrls(input_file, output_file):
    with open(input_file, "r") as file:
        datas = file.read()

    pattern = re.compile(r"(https?://[^\s/$.?#].[^\s]*)")

    matches = pattern.findall(datas)

    prefixes = set()
    for match in matches:
        url_parts = match.split("/")
        for i in range(3, len(url_parts) + 1):
            prefix = "/".join(url_parts[:i])
            prefixes.add(prefix)
    sorted_prefixes = sorted(prefixes)
    with open(output_file, "w") as f:
        for url in sorted_prefixes:
            f.write(url + "\n")


if __name__ == "__main__":
    main()
