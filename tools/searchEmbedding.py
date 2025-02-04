import numpy as np

from config.env_loader import (
    azure_openai_endpoint,
    azure_openai_deployment_name,
    azure_openai_api_key,
    azure_openai_endpoint_embeding,
    bing_search_api_key,
    azure_openai_embeding_api_key,
    azure_openai_embeding_deployment_name
)

pass

def calculate_embeddings(text):
    from openai import AzureOpenAI
    client = AzureOpenAI(
                        azure_endpoint=azure_openai_endpoint_embeding,
                        api_key=azure_openai_embeding_api_key,
                        api_version="2024-05-01-preview")
    
    embeddings = client.embeddings.create(input=text, model=azure_openai_embeding_deployment_name)

    return embeddings.data[0].embedding


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def find_most_similar(input_text, data, desired_doc_count=1):
    input_text_embeding = calculate_embeddings(input_text)
    similarities = []
    for entry in data:
        similarity = cosine_similarity(input_text_embeding, np.array(entry["embeddings"]))
        similarities.append((entry["text"], similarity))

    sorted_documents =sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_documents[:desired_doc_count]


def create_contextual_texts_per_pdf(filtered_pages_and_texts, overlap_ratio=0.2):
    all_output_texts = []

    for pdf_texts in filtered_pages_and_texts:
        output_texts = []
        input_texts = [page['text'] for page in pdf_texts]
        file_name = pdf_texts[0]['file_name'] if pdf_texts else ""

        for i in range(len(input_texts)):
            previous_context = input_texts[i - 1][-int(len(input_texts[i - 1]) * overlap_ratio/2):] if i > 0 else ""
            next_context = input_texts[i + 1][:int(len(input_texts[i + 1]) * overlap_ratio/2)] if i < len(input_texts) - 1 else ""

            combined_text = f"{previous_context} {input_texts[i]} {next_context}".strip()

            output_texts.append(combined_text)

        all_output_texts.append({
            "file_name": file_name,
            "texts": output_texts
        })

    return all_output_texts
# function implementation
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def find_most_similar(input_text, data, desired_doc_count=0):
    input_text_embeding = calculate_embeddings(input_text)
    similarities = []
    
    for entry in data:
        similarity = cosine_similarity(input_text_embeding, np.array(entry["embeddings"]))
        similarities.append((entry["text"], similarity))

    sorted_documents = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Si no hay resultados, devolver None
    return sorted_documents[:desired_doc_count] if sorted_documents else None

comparision_data = None

def search_for_info(input_text,desired_doc_count=1):   
    if comparision_data == None:
        return None
    most_similar = find_most_similar(input_text, comparision_data, desired_doc_count)
    if not most_similar:  # Si la lista está vacía
        return None
    most_similar_text = " ".join([entry[0] for entry in most_similar])
    return most_similar_text

def update_comparision_data(new_data):
    global comparision_data  # Permite modificar la variable global
    comparision_data = new_data