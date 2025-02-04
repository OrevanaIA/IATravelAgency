
import logging
import streamlit as st
from tools.explorePDF import open_and_read_pdf
from tools.explorePDF import get_pages_and_texts
from tools.explorePDF import concatenate_documents
from tools.searchEmbedding import create_contextual_texts_per_pdf, update_comparision_data
from tools.searchEmbedding import calculate_embeddings
from tools.searchAzure import custom_agent_worker
from tools.newAgent import nuevo_agente
import tiktoken
import json
import numpy as np
import tempfile

TEXT_INPUT= "What can I help with?"

st.title("Travel Agency Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.session_state.system_prompt = """
You are an assistant that helps organize trips. 
You must respond by assisting the user in planning their trip. 
Your answers should be correct, informal, and concise. You must provide information only in English.
"""

st.image("/Users/veronica/IA_2024/ProyectoIA/ProyectoIA_Modulo02/my-python-project/images/travel.webp", width=200)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("p/Users/veronica/IA_2024/ProyectoIA/ProyectoIA_Modulo02/my-python-project/images/travel.webp");
         background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100%;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.session_state.chat_history = [{"role": "system", "content": st.session_state.system_prompt}]

uploaded_files = st.file_uploader("Select PDF files, Please", type=["pdf"], accept_multiple_files=True)

pages_and_texts=[]
filtered_pages_and_texts=[]
# Verificar si se han cargado archivos
if uploaded_files is not None:
    st.write(f"They have been uploaded. {len(uploaded_files)} files:")
    
    # Iterar a través de los archivos seleccionados y mostrar sus nombres
    for uploaded_file in uploaded_files:
        st.write(f"- {uploaded_file.name}")
        temp_file_path = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())  # Guardar el archivo subido
            temp_file_path = temp_file.name
        pages_and_texts.append(open_and_read_pdf(temp_file_path))
        filtered_pages_and_texts.append(get_pages_and_texts(pages_and_texts[-1]))
    
    overlap_ratio = 0.2

    overlapped_texts_per_pdf = create_contextual_texts_per_pdf(filtered_pages_and_texts, overlap_ratio=overlap_ratio)

    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    input_texts_and_tokens = [{'file_name': text['file_name'],'text': texto, 'token_size': len(tokenizer.encode(texto))} for text in overlapped_texts_per_pdf for texto in text['texts']]

    max_tokens = 1000

    concatenated_input_texts_and_tokens = concatenate_documents(input_texts_and_tokens, max_tokens)

    text_and_embeddings = [{'block_id': block_id, 'text': text['text'], 'embeddings': calculate_embeddings(text['text'])} for block_id, text in enumerate(concatenated_input_texts_and_tokens)]

    oputput_file = "Embeddings.json"

    with open(oputput_file, "w") as file:
        json.dump(text_and_embeddings, file)

    embedings_list = json.load(open(oputput_file,'r'))

    embedings_list = [{
        "text": entry["text"],
        "embeddings": np.array(entry["embeddings"])
    } for entry in embedings_list]

    update_comparision_data(embedings_list)

else:
    st.write("Please select one or more PDF files.")


if st.button('Instantiate the system prompt.'):
    # Solicitar al usuario que ingrese un mensaje después de hacer clic en el botón
    mensaje = st.text_input("Introduce prompt:")

    # Mostrar el mensaje ingresado
    if mensaje:
        st.session_state.system_prompt = mensaje
    else:
       st.session_state.system_prompt = """
            You are an assistant that helps organize trips. 
            You must respond by assisting the user in planning their trip. 
            Your answers should be correct, informal, and concise. You must provide information only in English.
            """

    st.session_state.chat_history = [{"role": "system", "content": st.session_state.system_prompt}]
    
    st.session_state.agent = nuevo_agente(st.session_state.system_prompt)

    st.session_state.has_run = False

if "has_run" not in st.session_state or not st.session_state.has_run:
    logger = logging.getLogger("streamlit_app")

    logger.info("Creating a new Agent.")

    from llama_index.llms.azure_openai import AzureOpenAI
    
    st.session_state.agent = nuevo_agente(st.session_state.system_prompt)

    st.session_state.has_run = True
    
if "last_user_prompt" not in st.session_state:
    st.session_state.last_user_prompt = None

user_prompt = st.chat_input(TEXT_INPUT)

if user_prompt and user_prompt != st.session_state.last_user_prompt:
    st.session_state.last_user_prompt = user_prompt  # Guarda la última pregunta

    with st.chat_message("user"):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        response = st.session_state.agent.query(user_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.markdown(response)