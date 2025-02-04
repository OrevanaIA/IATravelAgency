import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='/Users/veronica/IA_2024/ProyectoIA/ProyectoIA_Modulo02/my-python-project/.env', override=True)

azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_URL")
azure_openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint_embeding = os.getenv("AZURE_OPENAI_ENDPOINT_URL_EMBBEDDING")
bing_search_api_key = os.getenv("BING_API_KEY")
azure_openai_embeding_api_key = os.getenv("AZURE_OPENAI_API_KEY_EMB")
azure_openai_embeding_deployment_name = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")



