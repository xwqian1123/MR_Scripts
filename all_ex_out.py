import csv
import sys
from typing import List, Dict

def merge_files_based_on_key(file_a: str, file_b: str, output_file: str) -> None:
    """
    Merge the content of two files based on a key value and write the result to an output file.
    
    Parameters:
    file_a: Path to the first file containing key values and data.
    file_b: Path to the second file containing key values and data.
    output_file: Path to the output file where the merged result will be saved.
    """
    try:
        # Read file A and build a dictionary mapping keys to rows
        key_to_row_map: Dict[str, List[str]] = {}  # Initialize key-row mapping dictionary    
        with open(file_a, "r", encoding="utf-8") as fa:  # Open file A for reading
            reader_a = csv.reader(fa, delimiter="\t")    # Create CSV reader with tab delimiter
            for row in reader_a:
                if len(row) >= 3:  # Skip rows with fewer than 3 columns
                    key = row[2]   # Use 3rd column as key
                    key_to_row_map[key] = row  # Store full row in dictionary

        # Read file B and merge data based on matching keys
        with open(file_b, "r", encoding="utf-8") as fb, \
             open(output_file, "w", encoding="utf-8", newline="") as fc:  # Create output file
            reader_b = csv.reader(fb, delimiter="\t")  # Create CSV reader for file B
            writer = csv.writer(fc, delimiter="\t")    # Create CSV writer for output
            for row in reader_b:
                if len(row) >= 5:  # Skip rows with fewer than 5 columns
                    key = row[4]   # Get key from 5th column
                    if key in key_to_row_map:  # Check key existence
                        merged_row = key_to_row_map[key] + row  # Merge rows
                        writer.writerow(merged_row)  # Write merged data

        print(f"Merge completed, result saved to {output_file}")
    # Handle the exception when the file is not found
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(1)
    # Handle other types of exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main() -> None:
    """
    Main function to parse command-line arguments and call the merge function.
    """
    if len(sys.argv) < 4:
        # Prompt the user for the correct usage and exit the program
        print("Usage: python all_ex_out.py <file_a> <file_b> <output_prefix>")
        sys.exit(1)

    # Parse the file names and output file name prefix from the command-line arguments
    file_a: str = sys.argv[1]
    file_b: str = sys.argv[2]
    output_prefix: str = sys.argv[3]
    # Construct the output file name
    output_file: str = f"{output_prefix}_all_{file_a}"

    # Call the merge function to merge the contents of two files based on a key
    merge_files_based_on_key(file_a, file_b, output_file)

# If this script is executed as the main program, invoke the main function.
if __name__ == "__main__":
    main()