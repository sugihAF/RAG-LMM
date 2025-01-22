
# RAG LLM with Streamlit

This repository demonstrates a Retrieval-Augmented Generation (RAG) application that uses a language model (LLM) to be specific it use DeepSeek AI to answer user queries based on the contents of uploaded PDF documents. The backend handles document processing, embedding creation, and query engine setup while the frontend provides an interactive chat interface built with Streamlit.

## Project Structure

The repository is split into two main scripts:

- **`ragllm.py`**  
  Contains the backend functionality for:
  - Loading the `deepseek-chat` from DeepSeek AI.
  - Loading and creating an embedding model with `BAAI/bge-large-en-v1.5`.
  - Reading and indexing PDF documents.
  - Building a query engine and updating prompt templates.

- **`app.py`**  
  Contains the Streamlit frontend code for:
  - Handling file uploads.
  - Displaying a PDF preview.
  - Maintaining the state of the conversation.
  - Interacting with the query engine for streaming responses.

## About DeepSeek AI

This project uses the DeepSeek AI language model, a cutting-edge conversational AI designed for context-aware query handling. DeepSeek AI specializes in understanding and generating responses based on provided contextual data, making it ideal for Retrieval-Augmented Generation (RAG) tasks. By integrating DeepSeek AI, this application ensures accurate, crisp, and contextually relevant answers based on the uploaded document's content.

The model, `deepseek-chat`, is accessed via OpenAI-compatible APIs, providing high performance and adaptability for various use cases. It is fine-tuned for specific domain expertise and supports streaming capabilities to deliver responses in real-time.

To use DeepSeek AI, ensure your API keys and base URLs are correctly set in the `.env` file.
## Features

- **File Upload & Indexing:**  
  Users can upload PDF documents that are then processed and indexed. The application supports reusing previously uploaded files across page reruns.

- **PDF Preview:**  
  Once a document is uploaded, its preview is displayed on the sidebar. The file data is stored in session state to persist the preview even after queries.

- **Interactive Chat:**  
  Chat messages are displayed using Streamlit's chat UI. Queries are answered by the query engine, and responses are streamed in real-time.

- **Query Engine:**  
  The engine uses a custom prompt to instruct the LLM to answer questions based on the context of the document, with the possibility of streaming responses.

## Installation

To run the application, you must install the following packages:

- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [langchain_openai](https://pypi.org/project/langchain_openai/) (or similar library for interacting with OpenAI)
- [langchain_huggingface](https://pypi.org/project/langchain-huggingface/) (or similar library for HuggingFace embeddings)
- [llama_index](https://github.com/jerryjliu/llama_index) (or similar libraries for indexing and processing documents)

You can install the required packages using `pip`. For example:

```bash
pip install streamlit python-dotenv langchain_openai langchain_huggingface llama_index
```

```bash
pip install -U sentence-transformers
```

```bash
huggingface-cli download BAAI/bge-large-en-v1.5
```

> **Note:** The package names or versions may vary. Check your libraries' documentation for the most up-to-date installation instructions.

## Environment Variables

Create a `.env` file in the project root with the following environment variables:

```env
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_ENDPOINT=your_langsmith_endpoint
LANGSMITH_API_KEY=your_langsmith_api_key
```

Make sure to replace the placeholder values with your actual API keys and endpoint URLs.

## Running the Application

Run the application using Streamlit:

```bash
streamlit run app.py
```

After launching, use the sidebar to upload a PDF document. Once the document is indexed, enter your query in the chat input box. The chatbot will provide a streaming response based on the contents of the uploaded document.

## How It Works

1. **Document Upload & Indexing (Sidebar in `app.py`):**
   - The PDF file is uploaded via Streamlit's file uploader.
   - The file is saved in session state (as bytes) to ensure persistence across reruns.
   - The `build_query_engine` function (from `ragllm.py`) processes the document, creates embeddings, indexes it, and sets up a custom prompt for the query engine.

2. **Chat Interface (Main in `app.py`):**
   - A chat interface displays previously sent messages.
   - When a new query is submitted, the application retrieves the appropriate query engine from session state.
   - The query engine processes the query and streams the response back to the user.

3. **Backend Processing (`ragllm.py`):**
   - The script manages the document processing and query engine initialization.
   - It uses the OpenAI LLM (or similar model) and HuggingFace embedding models.
   - A custom prompt template instructs the LLM on how to answer questions based on extracted context from the document.

## Customization

- **Prompt Template:**  
  You can update the prompt template in `ragllm.py` to change how the query engine interacts with the LLM.

- **Models & Providers:**  
  Adjust the model names and parameters in `load_llm()` and `create_embed_model()` according to your chosen models and hardware configuration (e.g., CPU or GPU).

## Contributing

Feel free to fork the repository and submit pull requests if you have improvements or additional features.

## License

This project is licensed under the [MIT License](LICENSE).

