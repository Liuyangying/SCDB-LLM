# Supreme Court Case Variable Encoding with LLM

## Overview

This project involves the use of a Large Language Model (LLM) to encode variables based on text extracted from Supreme Court cases. The LLM is trained to understand and process the language used in legal documents, specifically focusing on decisions and opinions from the United States Supreme Court. The encoded variables can be used for various legal research and analysis purposes.

The variables are modeled after those found in the [Supreme Court Database](http://scdb.wustl.edu/)

## Features

- **Text Extraction**: The LLM is capable of extracting and processing text from Supreme Court cases, including decisions, opinions, and related documents.

- **Variable Encoding**: The extracted text is processed by the LLM to encode relevant variables, which can include legal principles, key arguments, case details, and more.

- **Data Export**: Encoded variables can be exported in a structured csv for further analysis, data visualization, and integration with other tools. Along with the encodings, the LLM will export explanations for the decision to encode a variable.

## Getting Started

Follow these steps to start using the Supreme Court Case Variable Encoding LLM:

1. **Obtain OpenAI API Key**:

    1. Visit the [OpenAI website](https://openai.com/) and sign in to your account. If you don't have an account, you'll need to create one.

    2. Once you're logged in, click on API from the 3 options that show up. Then, click on your user profile in the top right corner of the screen and navigate to View Api Keys

    3. Once you have reached the <strong>API keys</strong> page, click on <strong>Create new api key</strong>. You may need to provide some additional information or agree to certain terms and conditions.

    4. After you've successfully created the API key, make sure to copy it and keep it secure. You'll need this API key to authenticate your requests to the OpenAI API.

    Remember to handle your API key securely and avoid sharing it in publicly accessible code repositories or online platforms.

    For more detailed information on how to manage your OpenAI API key and use it effectively, refer to the official [OpenAI API documentation](https://platform.openai.com/docs/introduction).

2. **Installation**:

    First, clone the repository to your local machine using the command line prompt:

    ```bash
    git clone https://github.com/yourusername/SCDB-LLM.git
    ```

    Then, you will need to install the necessary packages for this project to run. Navigate to the repository using the command line and install the dependencies using the following commands:

    ```console
    cd [your_directory]
    
    python install.py 
    ```

    Once the dependencies have been succesfully installed, you should get the message:

    ```bash
    All required packages have been installed.
    ```

    Next, navigate to the .env file and add your api key to the enviornmental variables so that the LLM can access GPT's internal modules.

    ```python
    OPENAI_API_KEY="your_api_key"
    ```

    If you would like to install the packages individually instead of using install.py, you can use the following commands from your command line. Otherwise, skip to the next section.

    [pdfplumber](https://pypi.org/project/pdfplumber/)

    ```console
    pip install pdfplumber
    ```

    This package will be used to extract text from pds and turn them into strings than can be fed into the LLM.

    [xlsxwriter](https://pypi.org/project/pdfplumber/)

    ```console
    pip install xlsxwriter
    ```

    This package will be used to open, read from, and write to excel files.

    [pandas](https://pandas.pydata.org/)

    ```console
    pip install pandas
    ```

    Pandas is a Python library that provides high-performance, easy-to-use data structures and data analysis tools for working with structured (tabular, multidimensional, potentially heterogeneous) and time series data.

    [openai](https://github.com/openai/openai-python)

    ```console
    pip install openai
    ```

    This will be used to access openai's api and internal models.



3. **Data Collection**: [Information on how to gather Supreme Court case text data for input.]

4. **Encoding Process**: [Details on how to use the LLM to encode variables from the collected text data.]

5. **Exporting Data**: [Instructions on how to export encoded variables for analysis.]

## Example Usage

```python
# Sample Python code demonstrating how to use the LLM for variable encoding
import supreme_llm

# Initialize the LLM model
model = supreme_llm.SupremeLLM()

# Load and preprocess Supreme Court case text
case_text = supreme_llm.load_case_text('path_to_case.txt')

# Encode variables from the case text
encoded_variables = model.encode_variables(case_text)

# Print the encoded variables
print(encoded_variables)
