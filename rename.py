import os
import csv

#Reads CAP_IDs_isolated.csv, converts pdfs in Cases folder a name with CAP_ID

def rename_pdfs(path, csv_file):
    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        row_number = 0
        for row in reader:
            row_number += 1
            id = row[0]
            new_name = id + ".pdf"
            for file in os.listdir(path):
                if file.endswith(".pdf"):
                    number = file.split("_")[0].strip("pdf")
                    if number == str(row_number):
                        os.rename(os.path.join(path, file), os.path.join(path, new_name))

if __name__ == "__main__":
    path = "Cases"
    csv_file = "Data/CAP_IDs_isolated.csv"
    rename_pdfs(path, csv_file)
    print("Renamed all files succesfully")
