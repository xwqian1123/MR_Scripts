import csv
import sys
from typing import List, Dict

def merge_fun(file_a: str, file_b: str, output_file: str) -> None:
    """
    Merges two tab-delimited CSV files based on a common key and writes the result to an output file.

    Parameters:
    file_a (str): Path to the first input file.
    file_b (str): Path to the second input file.
    output_file (str): Path to the output file.
    """
    a_dict: Dict[str, List[str]] = {}  
    # Open and read the first file, storing relevant rows in a dictionary
    with open(file_a, "r", encoding="utf-8") as fa:
        reader_a = csv.reader(fa, delimiter="\t")
        for row in reader_a:
            if len(row) >= 3:
                key = row[2]
                a_dict[key] = row

    # Open the second file and the output file, merging rows based on the common key
    with open(file_b, "r", encoding="utf-8") as fb, open(output_file, "w", encoding="utf-8", newline="") as fc:
        reader_b = csv.reader(fb, delimiter="\t")
        writer = csv.writer(fc, delimiter="\t")
        for row in reader_b:
            if len(row) >= 4:
                key = row[3]
                if key in a_dict:
                    merged_row = a_dict[key] + row
                    writer.writerow(merged_row)
    print(f"Merging completed, results saved to {output_file}")


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python get_bac.py <file_a> <file_b>")
        sys.exit(1)

    # Assign command-line arguments to variables
    file_a: str = sys.argv[1]
    file_b: str = sys.argv[2]
    output_file: str = 'mer_' + file_a

    # Call the merge function with the provided file paths
    merge_fun(file_a, file_b, output_file)