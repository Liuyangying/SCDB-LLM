import pandas as pd

def compute_accuracy(gpt_output_file, true_values_file):
    # Read the CSV files
    gpt_output_data = pd.read_csv(gpt_output_file)
    true_values_data = pd.read_csv(true_values_file)

    # Merge the DataFrames based on the "case_id" column to include only matching rows
    merged_data = pd.merge(gpt_output_data, true_values_data, on="caseId", how="inner")
    merged_data['petitionerState_y'] = merged_data['petitionerState_y'].fillna(0)

    print(merged_data.head(5))

    # Compute accuracy for each column (excluding "case_id")
    accuracy_results = {}
    for column in gpt_output_data.columns:
        if column != "caseId":
            true_values = merged_data[column + "_y"]  # Column from true_values_data
            predicted_values = merged_data[column + "_x"]  # Column from gpt_output_data
            accuracy = (true_values == predicted_values).mean()
            accuracy_results[column] = accuracy

    return accuracy_results

# Replace the file names with your actual file paths
gpt_output_updated_file_path = "GPT_output_updated.csv"
true_values_file_path = "true values.csv"

accuracy_results = compute_accuracy(gpt_output_updated_file_path, true_values_file_path)

print("Accuracy results:")
for column, accuracy in accuracy_results.items():
    print(f"{column}: {accuracy:.2f}")
