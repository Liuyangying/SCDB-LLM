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

    ```bash
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

    ```bash
    pip install pdfplumber
    ```

    This package will be used to extract text from pds and turn them into strings than can be fed into the LLM.

    [xlsxwriter](https://pypi.org/project/pdfplumber/)

    ```bash
    pip install xlsxwriter
    ```

    This package will be used to open, read from, and write to excel files.

    [pandas](https://pandas.pydata.org/)

    ```bash
    pip install pandas
    ```

    Pandas is a Python library that provides high-performance, easy-to-use data structures and data analysis tools for working with structured (tabular, multidimensional, potentially heterogeneous) and time series data.

    [openai](https://github.com/openai/openai-python)

    ```bash
    pip install openai
    ```

    This will be used to access openai's api and internal models.

3. **Data Collection**: 
    The supreme court pdfs are downloaded from the case.law using Noah's script, and all come in the format: "pdf[x]_[CASE_NAME]" where x is an integer. Before we can extract any text from the PDFs, the files need to be renamed with their <strong>CAP_ID</strong>, which is an ID tag that can be referenced to a corresponding row in the SCDB. To do this, first run <strong>rename.py</strong> from your terminal

    ```bash
    python rename.py
    ```

    Once it completes running, you should get the following message in your terminal:

    ```bash
    Renamed all files succesfully
    ```

    <strong>rename.py</strong> works by first accessing <strong>"CAP_IDs_isolated.csv"</strong> in the <strong>Data</strong> folder, where the xth row corresponds to <strong>CAP_ID</strong> for the file named "x_[CASE_NAME]". It renames the files directly in the Cases folder.

    Next, we need to actually extract the raw text from the pdfs. Run the following command from terminal:

    ```bash
    python text_extraction.py
    ```

     Once it completes running, you should get the following message in your terminal:

    ```bash
    Succesfully saved to 'Data/CAP_IDs_text.xlsx'
    ```

    <strong>text_extraction.py</strong> works by looping through every pdf in the <strong>Cases</strong> folder and using a packaged called [pdfplumber](https://pypi.org/project/pdfplumber/), writes the raw text of the pdf to the file named <strong>CAP_IDs_text.xlsx</strong> in the Data folder. Each row contains the <strong>CAP_ID</strong> in the first column and the case text in the second column. Once this is completed, the text of every supreme court cases has been extracted.

4. **Encoding Process**:

    There is a high level of customizability for <strong>SCDB_LLM.py</strong>.  We will look at each function inside  <strong>SCDB_LLM.py</strong>

    <strong>split_text()</strong>

    ```python
    def split_text(raw_text):

        supreme_court_splits = []

        #petitioner_state
        index = raw_text.find(("petitioner"))

        if index == -1:
            petionerState_text = raw_text[:1000]
        else:
            petionerState_text = raw_text[:index + len("petitioner")]

        supreme_court_splits.append(petionerState_text)
    ```

    This function splits the raw case text into smaller chunks for each variable. In the code snippet above, the function finds the first instance of the string "petitioner" and grabs the case text up to that point.

    <strong>run_gpt_prompts()</strong>.

     ```python
     for prompt in [f"""{supreme_court_splits[0]}""",
                    f"""{supreme_court_splits[1]}"""...]
     ```

     The above array allows you to customize the prompts passed into the llm. Each item in the array consists of the text split from the previous function followed by a prompt asking the LLM to encode the variable based on the text.

    ```python
     for retry_count in range(max_retry_count + 1):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[{"role": "system", "content": prompt}],
                    )
                if prompt_count == 8:
                    encoding = justice_encoding_dict.get(response.choices[0].message.content)
                    responses.append(encoding)
                else:
                    responses.append(response.choices[0].message.content)

                prompt_count +=1
                break
     ```

5. **Exporting Data**: [Instructions on how to export encoded variables for analysis.]
