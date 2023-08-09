import subprocess

def install_packages(package_list):
    for package in package_list:
        print(f"Installing {package}...")
        subprocess.run(["pip", "install", package])

if __name__ == "__main__":
    required_packages = [
        "pdfplumber",
        "xlsxwriter",
        "openai",
        "pandas",
        "python-dotenv"
    ]
    
    install_packages(required_packages)
    
    print("All required packages have been installed.")
