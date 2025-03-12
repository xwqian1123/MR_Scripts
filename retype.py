import sys
import os
from typing import List

# Define constants
ERROR_MESSAGE = "Usage: python script.py <input_file>"
OUTPUT_FILE_PREFIX = "out."

def convert_to_tab_delimited(input_file: str, output_file: str) -> None:
    """
    Convert the input file to a tab-delimited file and save it.

    Parameters:
    input_file (str): The path to the input file.
    output_file (str): The path to the output file.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                fields: List[str] = line.strip().split()  # Split the line into fields by whitespace  
                new_line: str = "\t".join(fields)   # Join fields with a tab character   
                outfile.write(new_line + "\n") # Write the new line to the output file
        print(f"Conversion complete, result saved in {output_file}")
    except IOError as e:
        print(f"File operation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if the script is run with at least one command line argument
    if len(sys.argv) < 2:
        # If not enough arguments are provided, print an error message and exit the program
        print(ERROR_MESSAGE)
        sys.exit(1)
    
    # Get the file path from the command line arguments
    input_file: str = sys.argv[1]
    # Process file path to ensure the output file path is correct
    output_file: str = OUTPUT_FILE_PREFIX + os.path.basename(input_file)
    
    # Call the function to convert the input file to tab-delimited format and save it to the output file
    convert_to_tab_delimited(input_file, output_file)