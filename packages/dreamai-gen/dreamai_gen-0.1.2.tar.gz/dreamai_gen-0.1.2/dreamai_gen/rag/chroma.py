from .imports import *
from ..utils import *
from ..parsing.pdf import *
from ..prompting.prompts import *


def chroma_collection(name: str, persistent_dir: str = "chroma_dir") -> chromadb.Collection:
    embedding_function = OpenCLIPEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path=persistent_dir)
    collection = chroma_client.get_or_create_collection(
        name, embedding_function=embedding_function, data_loader=ImageLoader()
    )
    collection.modify(metadata={"retrieved_ids": ""})
    return collection


def pdf_to_chroma_input(
    pdf_file: str | Path,
    max_characters: int = 5000,
    all_data: bool = False,
    data_keys: list = ["text", "page_number", "file_directory", "filename"],
) -> dict:
    data = pdf_to_chunks(
        pdf_file, max_characters=max_characters, all_data=all_data, data_keys=data_keys
    )
    book_ids = []
    book_documents = []
    book_metadatas = []
    for i, chunk in enumerate(data):
        book_ids.append(f"{chunk['filename']}_{i+1}")
        book_documents.append(chunk["text"])
        book_metadatas.append({k: v for k, v in chunk.items() if k != "text"})
    return {"ids": book_ids, "documents": book_documents, "metadatas": book_metadatas}


def pdf_to_chroma_collection(
    pdf_file: str | Path,
    collection_name: str,
    max_characters: int = 5000,
    all_data: bool = False,
    data_keys: list = ["text", "page_number", "file_directory", "filename"],
    persistent_dir: str = "chroma_dir",
) -> chromadb.Collection:
    collection = chroma_collection(collection_name, persistent_dir=persistent_dir)
    collection.upsert(
        **pdf_to_chroma_input(
            pdf_file,
            max_characters=max_characters,
            all_data=all_data,
            data_keys=data_keys,
        )
    )
    return collection
