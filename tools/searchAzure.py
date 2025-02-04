from tools.searchEmbedding import search_for_info, calculate_embeddings
from tools.searchBing import search_for_data_in_bing
from tools.searchEmbedding import cosine_similarity
# from llama_index.core.agent import FunctionCallingAgentWorker
# from llama_index.core.agent import AgentRunner
# from llama_index.core.tools import FunctionTool 

def custom_agent_worker(query: str):
       
        response = search_for_info(query) 
        # Verifica si la respuesta es válida (no None, no cadena vacía)
        if response and isinstance(response, str) and response.strip():
            # Compara la similitud entre la query y la respuesta encontrada
            similarity_score = cosine_similarity(calculate_embeddings(query), calculate_embeddings(response))

            # Si la similitud es baja (por ejemplo, < 0.4), se considera irrelevante y se devuelve None
            print(similarity_score)
            if similarity_score >= 0.4:
                return response
            else:
                print(f"Respuesta irrelevante, similitud: {similarity_score}. Devolviendo None.")
                return search_for_data_in_bing(query)

        return search_for_data_in_bing(query)
