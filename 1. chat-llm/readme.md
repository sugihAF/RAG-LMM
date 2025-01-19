
# Chat with Local LLM
This repository contains a simple Streamlit application that allows users to chat directly with a Large Language Model (LLM) using a conversational interface. The app is built with [Streamlit](https://streamlit.io/) and leverages a custom `ChatLLM` class (powered by the `OllamaLLM` engine) to process and respond to user queries.

> **Note:** This app is a simplified version and does not integrate Retrieval-Augmented Generation (RAG) or PDF ingestion. It is designed solely for chatting with the LLM.

## Features

- **Interactive Chat Interface:** A clean and simple UI for exchanging messages with the LLM.
- **Custom LLM Chat Class:** Uses a dedicated `ChatLLM` class that handles chat prompt formatting and invoking the LLM.
- **Streamlit Integration:** Utilizes [Streamlit](https://streamlit.io/) for an easy-to-deploy web application interface.
- **Configurable Debugging:** The app logs verbose output and debugging information to help with troubleshooting.

## Downloading the Ollama Model
The ChatLLM class in this project uses the Ollama LLM (`llama3.2` model) for generating responses. To use this model, follow these steps:

- **Download ollama:** Visit the [Ollama](https://ollama.com/download) website for instructions on installing Ollama on your machine. Currently, Ollama is available on macOS and may require registration or a license key depending on your usage.

- **Download/Select the Model:** Once Ollama is installed, you can download the desired model. In this example, the default model is "llama3.2". Make sure this model is available in your Ollama installation. You can often download the model via the Ollama CLI:
```bash
  ollama pull llama3.2
```
Adjust the model name if you wish to use a different version.

- **Configure Your Environment:** Ensure that your environment is set up to allow the langchain_ollama package to communicate with your local Ollama installation. Refer to the Ollama Documentation for additional configuration and troubleshooting steps.
 ```bash
streamlit
streamlit-chat
langchain-core
langchain-ollama
langchain-community
```

## Code Overview
# ChatLLM Class

The `ChatLLM` class encapsulates the functionality of an LLM-based chat system. Below is an overview of its key components:

## Initialization
- Configures the **OllamaLLM model**.
- Sets up a **chat prompt template** using `ChatPromptTemplate`.
- Integrates additional components like an **output parser** for processing responses.

## Methods
### `ask`
- Constructs and invokes a processing chain to:
  1. Accept a user question.
  2. Format it using the prompt template.
  3. Send the query to the language model.
  4. Parse and return the model's string response.

### `clear`
- Resets any internal state (if necessary).

---

## Streamlit App (`app.py`)

This file manages the user interface and interaction with the `ChatLLM` class.

## Features
### Session State Initialization
- Initializes session variables such as:
  - `messages` (chat history).
  - `chat assistant` (instance of `ChatLLM`).

### Display Functions
- Displays conversation messages.
- Shows a spinner while the model processes a query.

### User Input Processing
- Captures user input from a text field.
- Passes input to the `ChatLLM` instance.
- Updates chat history with model responses.

---

# Customization

### Changing the LLM Model
To use a different language model, modify the instantiation of `OllamaLLM` in `ChatLLM` (found in `your_chat_module.py`).

### Adjusting the Prompt Template
The chat prompt is defined within the `ChatLLM` class. Customize the system and human messages in the prompt template to achieve your desired conversational tone.

---

## Example Usage

### Running the Streamlit App

   ```bash
   streamlit run app.py
