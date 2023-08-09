import os
import pdfplumber
import xlsxwriter

def extract_text_from_pdfs(path, excel_file):
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0 

    for file in os.listdir(path):
        if file.endswith(".pdf"):
            pdf = pdfplumber.open(os.path.join(path, file))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            filename = file.split(".pdf")[0]
            worksheet.write(row, col,     filename)
            worksheet.write(row, col + 1, text)
        row += 1
    
            

    workbook.close()

if __name__ == "__main__":
    path = "Cases"
    excel_file = "Data/CAP_IDs_text.xlsx"
    extract_text_from_pdfs(path, excel_file)
