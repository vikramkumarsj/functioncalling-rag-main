# AI Agent with RAG and Tool Calling

## Description
• Retrieval-Augmented Generation (RAG) on faiss database using publicly available USGS unstructured data.
• Structured tool/API calling using a public API to download dataset and also for additional context.
• A simple chat interface for user interaction using steamlit.

## Dependency 
Python: 
    https://www.python.org/downloads/release/python-3137/
Microsoft Visual C++ Redistributable: 
    https://aka.ms/vs/16/release/vc_redist.x64.exe
Collect the API for USGS requesting through below
    https://api.waterdata.usgs.gov/signup

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Ollama (required for the chatbot to function). Follow the instructions for your operating system on the [Ollama website](https://ollama.ai/).

3. Pull the required models for Ollama:
   ```bash
   ollama pull llama3.2
   ```

4.  
4.1 Collect the API for USGS requesting through below
    https://api.waterdata.usgs.gov/signup
4.2 replace the api_url referenced in the code streamlit_function_calling.py with your api_key.
4.3 Download USGS Research report on Water from below link and place it in research_reports folder.
    circular1217.pdf https://share.google/rRuLZviW5UChSGloL


## Running Instructions

python -m streamlit run streamlit_function_calling.py

Please make sure that 'vector_data_manager.py' to store data in RAG & 
RAG data retriever 'RAG_with_RetrievalQA.py' is running in the background 
to be used in above streamlit_function_calling.py'

### You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501


### Step 1: Embed the Documents in FAISS DataStore
If You need to embed the additional documents into the faiss vector store.

1. Run the embedding script:
   ```bash
   python vector_data_manager.py
   ```

### Step 2: Start and Test the RAG Chat on FAISS data store
Once the documents are embedded and available in faiss_index_USGS folder, you can start the chatbot.

1. Run the chat script:
   ```bash
   python RAG_with_RetrievalQA.py
   ```
2. Interact with the chatbot through the terminal.

## Examples
Below two example questions and corresponding answers are shown.

1. **Question: what is the approval status for monitoring location USGS-01482100'**

    Based on the provided context, I can extract the following information about monitoring locations with an "approval_status" of "Provisional"

## Extract New data from USGS and store in Datastore as JSON Files

 run function calling program function_calling_new_dataset.py with edits for new datasets from USGS

