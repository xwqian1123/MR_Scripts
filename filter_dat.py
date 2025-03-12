import logging
from pathlib import Path
from typing import List

# Configure logging settings
# Logs will display timestamps, severity level, and messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_input_path(path: str) -> Path:
    """
    Validate whether the given input file path exists.
    
    Args:
        path (str): The file path to validate.

    Returns:
        Path: The resolved absolute path of the input file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Input file path {path} does not exist.")
    return path_obj.resolve()

def validate_output_path(path: str) -> Path:
    """
    Validate whether the parent directory of the output file exists.
    
    Args:
        path (str): The output file path.

    Returns:
        Path: The resolved absolute path of the output file.

    Raises:
        FileNotFoundError: If the parent directory does not exist.
    """
    path_obj = Path(path)
    if not path_obj.parent.exists():
        raise FileNotFoundError(f"Output directory {path_obj.parent} does not exist.")
    return path_obj.resolve()

def log_skipped_line(line_number: int, filepath: Path, reason: str) -> None:
    """
    Log a warning message when a line is skipped due to an issue.

    Args:
        line_number (int): The line number in the input file.
        filepath (Path): The path of the file being processed.
        reason (str): The reason why the line was skipped.
    """
    logging.warning(f"Skipping line {line_number} in {filepath}: {reason}")

def filter_file(input_filepath: str, output_filepath: str) -> None:
    """
    Process the input file, filter lines based on a specific condition,
    and write valid lines to the output file.

    Filtering Condition:
    - The file must have at least 10 columns.
    - The 10th column (index 9) should be convertible to a float.
    - The p-value (10th column) should be less than 1e-5.

    Args:
        input_filepath (str): The path to the input file.
        output_filepath (str): The path to the output file.

    Exceptions:
        Logs any errors that occur during file processing.
    """
    rows_written = 0
    try:
        input_path = validate_input_path(input_filepath)

        # Ensure the output file's parent directory exists
        output_path = Path(output_filepath)
        if not output_path.parent.exists():
            raise FileNotFoundError(f"Output directory {output_path.parent} does not exist.")

        with input_path.open('r') as infile, output_path.open('w') as outfile:
            # Read the header line from the input file and remove any leading/trailing whitespace
            header = infile.readline().strip()
            # If a header exists, write it to the output file and increment the rows_written counter
            if header:
                outfile.write(header + "\n")
                rows_written += 1

            # Process the remaining lines
            for line_number, line in enumerate(infile, start=2):
                line = line.strip()  # Strip leading and trailing whitespace from the line
                if not line:  # Skip empty lines
                    continue

                # Split the line into parts based on whitespace (default delimiter)
                # Modify the delimiter if necessary
                parts = line.split()
                if len(parts) < 10:  # Check if the line has at least 10 columns
                    log_skipped_line(line_number, input_path, "less than 10 columns")
                    continue

                try:
                    p_value = float(parts[9])  # Attempt to convert the 10th column to a float
                except ValueError:
                    log_skipped_line(line_number, input_path, f"cannot convert '{parts[9]}' to float")
                    continue

                # Check if the p-value is less than 1e-05
                if p_value < 1e-05:
                    outfile.write(line + "\n")
                    rows_written += 1

        logging.info(f"Finished processing {input_path}: {rows_written} rows written to {output_path}.")
    
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
    except IOError as io_error:
        logging.error(f"IO error processing file {input_filepath}: {io_error}")
    except Exception as e:
        logging.error(f"Unexpected error processing file {input_filepath}: {e}")

def process_file_paths(file_paths_filepath: str) -> None:
    """
    Read a list of file paths from a text file, filter each file, and merge the filtered results.

    Each line in the input file should contain a valid file path.

    Args:
        file_paths_filepath (str): The path to the text file containing a list of file paths.
    """
    file_paths_path = Path(file_paths_filepath)
    if not file_paths_path.exists():
        logging.error(f"File paths list {file_paths_filepath} does not exist.")
        return

    filtered_files: List[Path] = []

    with file_paths_path.open('r') as paths_file:  # Open the file containing the list of file paths
        for file_path_str in paths_file:  # Iterate through each line in the file
            file_path_str = file_path_str.strip()  
            if not file_path_str:  # Skip empty lines
                continue

            file_path = Path(file_path_str)  # Convert the file path string to a Path object
            if not file_path.exists():  # Check if the file exists
                logging.error(f"Input file {file_path} not found, skipping.")
                continue

            # Generate output file path by appending '_filtered' before the extension
            base = file_path.stem   # Get the base name of the file (without extension)
            ext = file_path.suffix  # Get the file extension
            output_file = file_path.parent / f"{base}_filtered{ext if ext else '.txt'}"

            logging.info(f"Processing {file_path} -> {output_file}")  # Log the processing information
            filter_file(str(file_path), str(output_file))
            filtered_files.append(output_file)
    
    merge_filtered_files(filtered_files, Path("merged_filtered_results.txt"))

def merge_filtered_files(filtered_files: List[Path], merged_output_file: Path) -> None:
    """
    Merge multiple filtered files into a single output file.
    
    - The first file's header is kept.
    - Subsequent files have their headers removed to avoid duplicates.

    Args:
        filtered_files (List[Path]): A list of filtered file paths.
        merged_output_file (Path): The path for the merged output file.

    Exceptions:
        Logs any errors encountered during file merging.
    """
    try:
        with merged_output_file.open('w') as outfile:
            header_written = False  # Track whether the header has been written
            for file in filtered_files:
                if file.exists():
                    with file.open('r') as infile:
                        lines = infile.readlines()
                        if not lines:
                            continue
                        if not header_written:
                            outfile.write(lines[0])  # Write header from the first file
                            header_written = True
                            remaining_lines = lines[1:]  # Exclude header from subsequent files
                        else:
                            remaining_lines = lines[1:]

                        for line in remaining_lines:
                            outfile.write(line)

        logging.info(f"Merged {len(filtered_files)} filtered files into {merged_output_file}.")
    except Exception as e:
        logging.error(f"Error merging files: {e}")

if __name__ == "__main__":
    # Specify the text file containing the list of file paths
    file_paths_list = 'list_path.txt'
    process_file_paths(file_paths_list)

