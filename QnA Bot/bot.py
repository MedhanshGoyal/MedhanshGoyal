import faiss
import json
import os
import pickle
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import Dataset
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, S3DirectoryLoader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


class QnABot:
    def __init__(
        self,
        order_index_path: str,
        item_index_path: str,
        customer_index_path: str,
        fine_tuned_model_path: str,
        model: str | None = None,
        temperature=0,
    ):
        # Initialize the QnABot by selecting a model, loading FAISS indexes, and loading the fine-tuned model
        self.select_model(model, temperature)
        self.load_indexes(order_index_path, item_index_path, customer_index_path)
        self.load_fine_tuned_model(fine_tuned_model_path)

        # Load the question-answering chain for the selected model
        self.chain = load_qa_with_sources_chain(self.llm)

    def select_model(self, model: str | None, temperature: float):
        # Select and set the appropriate model based on the provided input
        if model is None or model == "gpt-3.5-turbo":
            print("Using model: gpt-3.5-turbo")
            self.llm = ChatOpenAI(temperature=temperature)

    def load_indexes(self, order_index_path: str, item_index_path: str, customer_index_path: str):
        # Load pre-made FAISS indexes from specified paths
        if os.path.exists(order_index_path):
            print(f"Loading order index from: {order_index_path}")
            with open(order_index_path, "rb") as f:
                self.order_index = pickle.load(f)
        else:
            raise FileNotFoundError(f"Order index file not found: {order_index_path}")

        if os.path.exists(item_index_path):
            print(f"Loading item index from: {item_index_path}")
            with open(item_index_path, "rb") as f:
                self.item_index = pickle.load(f)
        else:
            raise FileNotFoundError(f"Item index file not found: {item_index_path}")

        if os.path.exists(customer_index_path):
            print(f"Loading customer index from: {customer_index_path}")
            with open(customer_index_path, "rb") as f:
                self.customer_index = pickle.load(f)
        else:
            raise FileNotFoundError(f"Customer index file not found: {customer_index_path}")

    def load_fine_tuned_model(self, fine_tuned_model_path: str):
        # Load the fine-tuned model and tokenizer from the specified path
        self.tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(fine_tuned_model_path)

    def print_answer(self, question, k=1):
        # Retrieve and print the answer to the given question
        weight_order = 0.5  # Example weight for order_docs
        weight_item = 0.3   # Example weight for item_docs
        weight_customer = 0.2

        order_docs = self.order_index.similarity_search(question, k=k)
        item_docs = self.item_index.similarity_search(question, k=k)
        customer_docs = self.customer_index.similarity_search(question, k=k)

        combined_docs = []
        combined_docs.extend([(doc[0], doc[1] * weight_order) for doc in order_docs])
        combined_docs.extend([(doc[0], doc[1] * weight_item) for doc in item_docs])
        combined_docs.extend([(doc[0], doc[1] * weight_customer) for doc in customer_docs])

        # Sort combined_docs by score in descending order
        combined_docs.sort(key=lambda x: x[1], reverse=True)

        # Optionally, limit to top k documents
        combined_docs = combined_docs[:k]

        print(
            self.chain(
                {
                    "input_documents": combined_docs,
                    "question": question,
                },
                return_only_outputs=True,
            )["output_text"]
        )

    def get_answer(self, question, k=1):
        # Retrieve the answer to the given question and return it
        order_docs = self.order_index.similarity_search(question, k=k)
        item_docs = self.item_index.similarity_search(question, k=k)
        customer_docs = self.customer_index.similarity_search(question, k=k)

        combined_docs = order_docs + item_docs + customer_docs  # Combine results if needed

        return self.chain(
            {
                "input_documents": combined_docs,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]


# Example usage:
order_index_path = "path/to/order_index.pkl"
item_index_path = "path/to/item_index.pkl"
customer_index_path = "path/to/customer_index.pkl"
fine_tuned_model_path = "./fine_tuned_qna_model"

bot = QnABot(order_index_path, item_index_path, customer_index_path, fine_tuned_model_path, model="gpt-3.5-turbo", temperature=0)

# Example query
question = "What are the recent orders placed by customer ABC?"
answer = bot.get_answer(question)
print("Answer:", answer)
