import pandas as pd
import re

def clean_numeric_data(row):
    # Define a regular expression pattern to match numerical values
    num_pattern = r"[-+]?\d*\.?\d+"

    # Loop through all columns (except "case_id")
    for column in row.index:
        if (column != "case_id") and (column != 'chief'):
            cell_value = str(row[column])
            numerical_value = re.findall(num_pattern, cell_value)
            if numerical_value:
                row[column] = pd.to_numeric(numerical_value[0])
            else:
                row[column] = pd.NA

    return row

def replace_case_ids(gpt_output_file, matchup_file):
    # Read the CSV files
    gpt_output_data = pd.read_csv(gpt_output_file)
    matchup_data = pd.read_csv(matchup_file)

    # Remove duplicates from the matchup_data based on "CAP ID"
    matchup_data.drop_duplicates(subset="CAP ID", keep="first", inplace=True)

    # Create a dictionary mapping CAP ID to SCDB ID
    cap_id_to_scdb_id = dict(zip(matchup_data["CAP ID"], matchup_data["SCDB ID"]))

    # Update the "case_id" in GPT_output_data using the mapping
    gpt_output_data["caseId"] = gpt_output_data["caseId"].map(cap_id_to_scdb_id)

    # Clean numerical data row by row (keeping only numerical data)
    gpt_output_data = gpt_output_data.apply(clean_numeric_data, axis=1)

    # Save the updated data to a new CSV file (you can change the file name as desired)
    updated_output_file = "GPT_output_updated.csv"
    gpt_output_data.to_csv(updated_output_file, index=False)

    print(f"Updated data saved to '{updated_output_file}'.")

# Replace the file names with your actual file paths
gpt_output_file_path = "GPT_output.csv"
matchup_file_path = "matchup.csv"

replace_case_ids(gpt_output_file_path, matchup_file_path)
