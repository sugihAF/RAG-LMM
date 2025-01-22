import os
import base64
import gc
import tempfile
from dotenv import load_dotenv

from llama_index.core import Settings, PromptTemplate
from llama_index.core import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Global variables from .env
LANGSMITH_TRACING = True
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = "https://api.deepseek.com"

def load_llm():
    """
    Instantiates and returns the ChatOpenAI LLM.
    """
    llm = ChatOpenAI(
        model='deepseek-chat', 
        openai_api_key=OPENAI_API_KEY, 
        openai_api_base=OPENAI_API_BASE,
        max_tokens=1024
    )
    return llm

def create_embed_model():
    """
    Instantiates and returns the HuggingFace embedding model.
    """
    model_name = "BAAI/bge-large-en-v1.5"
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embed_model

def build_query_engine(uploaded_file, session_id):
    """
    Given an uploaded PDF file (as a file-like object) and a session id,
    this function writes the file to a temporary directory, processes it,
    builds a query engine, updates the prompt template, and returns the query engine.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Ensure the file is present in the directory by using the directory reader
        loader = SimpleDirectoryReader(
            input_dir=temp_dir,
            required_exts=[".pdf"],
            recursive=True
        )
        docs = loader.load_data()

        # Setup llm & embedding model
        llm = load_llm()
        embed_model = create_embed_model()

        # Set the global embed model
        Settings.embed_model = embed_model
        # Create an index over loaded docs
        index = VectorStoreIndex.from_documents(docs, show_progress=True)

        # Setup service context with the llm if needed (you can customize this further)
        Settings.llm = llm
        query_engine = index.as_query_engine(streaming=True)

        # Customize the prompt template
        qa_prompt_tmpl_str = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information above I want you to think step by step to answer the query in a crisp manner, "
            "in case you don't know the answer say 'I don't know!'.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

        query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
        )

        return query_engine
