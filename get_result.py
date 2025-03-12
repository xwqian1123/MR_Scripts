import pandas as pd
import sys
from pathlib import Path
from typing import Union, List


# Define column names for exposure and outcome data
EXPOSURE_DATA_COLUMNS = [
    "chr.exposure", "pos.exposure", "beta.exposure", "se.exposure", 
    "pval.exposure", "SNP", "effect_allele.exposure", "other_allele.exposure"
]

OUTCOME_DATA_COLUMNS = [
    "chr.outcome", "pos.outcome", "beta.outcome", "se.outcome", 
    "pval.outcome", "SNP", "effect_allele.outcome", "other_allele.outcome", "eaf.outcome"
]


def process_exposure_outcome_data(input_file: Union[str, Path], output_prefix: Union[str, Path]) -> None:
    """
    Process the input file and generate exposure and outcome data files.

    Args:
        input_file: Path to the input file.
        output_prefix: Prefix for the output files.
    """
    # Convert input and output paths to Path objects for better handling
    input_path = Path(input_file)
    output_prefix = Path(output_prefix)
    
    # Define output file paths
    outcome_file = f"{output_prefix}.outcome.txt"
    exposure_file = f"{output_prefix}.exposure.txt"
    
    # Read input data
    df = pd.read_csv(input_path, sep='\t')
    
    # Process outcome data
    process_outcome_data(df, outcome_file)
    
    # Process exposure data
    process_exposure_data(df, exposure_file)


def process_outcome_data(df: pd.DataFrame, output_file: Union[str, Path]) -> None:
    """
    Process and save the outcome data.

    Args:
        df: DataFrame containing the input data.
        output_file: Path to the output file.
    """
    # Select relevant columns
    outcome_columns = [24, 25, 32, 33, 30, 28, 27, 26, 34]
    outcome_data = df.iloc[:, outcome_columns].copy()
    
    # Set column names and add additional information
    outcome_data.columns = OUTCOME_DATA_COLUMNS
    #outcome_data["samplesize"] = 118291
    outcome_data["outcome"] = "PE"
    outcome_data["id.outcome"] = "finngen_R11_O15_PREECLAMPS"
    outcome_data["mr_keep.outcome"] = "TRUE"
    
    # Save to file
    outcome_data.to_csv(output_file, header=True, sep='\t', index=False)


def process_exposure_data(df: pd.DataFrame, output_file: Union[str, Path]) -> None:
    """
    Process and save the exposure data.

    Args:
        df: DataFrame containing the input data.
        output_file: Path to the output file.
    """
    # Select relevant columns
    exposure_columns = [0, 3, 18, 19, 21, 2, 17, 16]
    exposure_data = df.iloc[:, exposure_columns].copy()
    
    # Set column names and add additional information
    exposure_data.columns = EXPOSURE_DATA_COLUMNS
    #exposure_data.insert(5, 'samplesize.exposure', '18340')
    exposure_data['id.exposure'] = "MiBioGen"
    exposure_data['exposure'] = df.iloc[:, 12]
    exposure_data['eaf.exposure'] = "NA"
    exposure_data["mr_keep.exposure"] = "TRUE"
    exposure_data["pval_origin.exposure"] = "inferred"
    exposure_data["data_source.exposure"] = "MiBioGen"
    
    # Save to file
    exposure_data.to_csv(output_file, header=True, sep='\t', index=False)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_prefix>")
        sys.exit(1)

    # Assign command-line arguments to variables
    input_file = sys.argv[1]
    output_prefix = sys.argv[2]

    # Call the main processing function
    process_exposure_outcome_data(input_file, output_prefix)