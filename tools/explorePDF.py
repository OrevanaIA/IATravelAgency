import fitz  # PyMuPDF
import tiktoken


def text_formatter(text: str) -> str:
    cleaned_text = text.replace("\n", " ").strip()

    return cleaned_text

def open_and_read_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    pages_and_texts = []

    tokenizer = tiktoken.encoding_for_model("gpt-4o")

    for page_number, page in enumerate(doc):
        text = page.get_text()
        text = text_formatter(text)

        tokens = tokenizer.encode(text)
        word_count = len(text.split())

        pages_and_texts.append({
            "file_name": pdf_path,
            "page_number": page_number,
            "page_word_count": word_count,
            "page_token_cont": len(tokens),
            "text": text
        })

    return pages_and_texts

def get_pages_and_texts(pages_and_texts_sublist):
    pages_and_texts = [page for page in pages_and_texts_sublist if page["page_word_count"] > 0]

    return pages_and_texts

def concatenate_documents(docs, max_tokens):
    concatenated_docs = []
    current_group = {"file_name": "", "text": "", "token_size": 0}

    for doc in docs:
        if current_group["file_name"] != doc["file_name"]:
            if current_group["token_size"] > 0:
                concatenated_docs.append(current_group)
            current_group = {"file_name": doc["file_name"], "text": doc["text"], "token_size": doc["token_size"]}
        elif current_group["token_size"] + doc["token_size"] <= max_tokens:
            current_group["text"] += (" " + doc["text"]).strip()
            current_group["token_size"] += doc["token_size"]
        else:
            concatenated_docs.append(current_group)
            current_group = {"file_name": doc["file_name"], "text": doc["text"], "token_size": doc["token_size"]}

    if current_group["token_size"] > 0:
        concatenated_docs.append(current_group)
    
    return concatenated_docs