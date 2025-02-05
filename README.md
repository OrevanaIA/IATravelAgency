
# Travel Agency Project

This project is a Streamlit application that acts as a travel agency assistant, helping users plan their trips.


## Interaction Flow
*PDF Upload: The user uploads PDF files via the Streamlit interface.

*PDF Processing:
    - Extracts text from each page.  
    - Generates embeddings using Azure OpenAI.

*Agent Creation: An OpenAI agent is set up to use embeddings and Bing searches.
*User Query:
    The user asks a question, and the agent searches the embeddings to return the best answer.

## Project Structure

- `env_loader.py`: Loads environment variables.
- `bing_search.py`: Performs Bing searches.
- `explore_pdf.py`: Processes PDFs and extracts their content.
- `search_embedding.py`: Generates embeddings and searches for similarities.
- `search_with_azure.py`: Coordinates searches with embeddings and Bing.
- `nuevo_agente.py`: Configures and runs the agent.
- `requirements.txt`: Necessary dependencies.
- `travelAgency.py`: Main Streamlit application file.

## Installation and Execution

### 1️⃣ Prerequisites

- Python 3.8 or higher
- API keys for Azure OpenAI and Bing Search

### 2️⃣ Installing Dependencies

Run the following command in the terminal:

pip install -r requirements.txt

### 3️⃣ Environment Variable Setup:

Create a .env file with the following content and fill in your credentials:

```
AZURE_OPENAI_ENDPOINT=...  # URL of the Azure OpenAI endpoint
AZURE_OPENAI_API_KEY=...  # Azure OpenAI API key
AZURE_OPENAI_DEPLOYMENT_NAME=...  # OpenAI deployment name
AZURE_OPENAI_ENDPOINT_EMBEDINGS=...  # URL of the OpenAI embeddings endpoint
AZURE_OPENAI_EMBEDINGS_API_KEY=...  # OpenAI embeddings API key
BING_API_KEY=...  # Bing Search API key
```

### 4️⃣ Running the Application

Run the following command in the terminal to start the application:

```sh
streamlit run travelAgency.py
```

##  Using the Application

Upload PDF files containing relevant information for your trip.
Interact with the travel assistant through the Streamlit user interface.
Receive recommendations and assistance in planning your trip.

