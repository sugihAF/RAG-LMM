from langchain_core.globals import set_verbose, set_debug
from langchain_ollama.llms import OllamaLLM
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# Enable debugging and verbose logging.
set_debug(True)
set_verbose(True)


class ChatLLM:
    def __init__(self, llm_model: str = "llama3.2"):
        # Initialize the language model.
        self.model = OllamaLLM(model=llm_model)
        
        # Set up a chat prompt template.
        # The prompt includes a system message and a human message.
        # The human message will include the user's question.
        self.prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    "You are a helpful assistant ready to chat. Answer the user's questions as clearly and concisely as possible.",
                ),
                (
                    "human",
                    "Question: {question}",
                ),
            ]
        )
        
        # Prepare the chain as None until a query is invoked.
        self.chain = None

    def ask(self, query: str):
        # Construct the chat chain by piping the input through:
        # 1. A dictionary mapping containing the question.
        # 2. The prompt template.
        # 3. The language model.
        # 4. An output parser to return the response as a string.
        self.chain = (
            {"question": RunnablePassthrough()}  # Pass the user query unchanged.
            | self.prompt
            | self.model
            | StrOutputParser()
        )

        # Invoke the chain with the user's query.
        return self.chain.invoke(query)

    def clear(self):
        # Reset the chain; not strictly necessary in this simplified version,
        # but provided to remain consistent with the original code structure.
        self.chain = None


# Example usage:
if __name__ == "__main__":
    chat = ChatLLM()
    user_question = "What is task decomposition?"
    response = chat.ask(user_question)
    print("LLM Response:", response)
