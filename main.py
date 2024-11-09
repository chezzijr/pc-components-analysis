import asyncio
import numpy as np
import pandas as pd
import argparse as ap
import logging
import sys
from populate import insert_data, insert_prices
from parts import CPU
from parts import VGA
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from os.path import exists

# stdout as the default logging handler
logfile = "log.txt"
logging.basicConfig(filename=logfile,
                    filemode='a',
                    format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

parser = ap.ArgumentParser()
parser.add_argument("task", help="The task to be performed which is either insert_data|query_prices|chat")
args = parser.parse_args()

match args.task:
    case "insert_data":
        insert_data()
        print("Data inserted")
    case "query_prices":
        asyncio.run(insert_prices())
        print("Prices inserted")
    case "chat":
        print("Starting the chatbot")
    case _:
        print("Invalid task")

exit(0)
# csv_to_constructor_map = {
#     "cpu.csv": CPU,
#     "video-card.csv": VGA,
# }

# documents = []
# for csv_file, constructor in csv_to_constructor_map.items():
#     parts = (
#         pd.read_csv(f"./datasets/csv/{csv_file}")
#         .drop("price", axis=1)
#         .replace(np.nan, None)
#     )
#     # print(parts.isnull().sum())
#     documents.extend(
#         Document(page_content=str(part))
#         for part in parts.apply(lambda row: constructor(*row), axis=1)
#     )

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(documents)

# if exists("./chroma_langchain_db"):
#     vectorstore = Chroma(
#         collection_name="pc_parts",
#         persist_directory="./chroma_langchain_db",
#         embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
#     )
# else:
#     vectorstore = Chroma.from_documents(
#         documents=splits,
#         embedding=OllamaEmbeddings(model="nomic-embed-text"),
#         persist_directory="./chroma_langchain_db",
#         collection_name="pc_parts",
#     )

# retriever = vectorstore.as_retriever()
# prompt = PromptTemplate.from_template(
#     (
#         "You are an assistant for question-answering tasks. "
#         "Use the following pieces of retrieved context to answer the question. "
#         "If you don't know the answer, just say that you don't know. "
#         "Use three sentences maximum and keep the answer concise.\n"
#         "Question: {question} \n"
#         "Context: {context} \n"
#         "Answer:"
#     )
# )
# llm = OllamaLLM(model="llama3.2:1b", temperature=0.1)


# def format_docs(documents):
#     return "\n\n".join(doc.page_content for doc in documents)


# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# result = rag_chain.invoke(input())
# print(result)
