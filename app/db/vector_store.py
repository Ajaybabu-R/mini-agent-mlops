import os
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings


def create_vector_store():

    documents = [
        "Chemical cleaning solvent",
        "Industrial lubricant oil",
        "Organic fertilizer compound",
        "Pharmaceutical raw material"
    ]

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        api_version="2024-02-01"
    )

    vector_store = FAISS.from_texts(documents, embeddings)

    return vector_store
