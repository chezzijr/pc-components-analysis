import numpy as np
import pandas as pd
from parts import CPU
from parts import VGA
from langchain import hub
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

csv_to_constructor_map = {
    "cpu.csv": CPU,
    "video-card.csv": VGA,
}

documents = []
for csv_file, constructor in csv_to_constructor_map.items():
    parts = (
        pd.read_csv(f"./datasets/csv/{csv_file}")
        .drop("price", axis=1)
        .replace(np.nan, None)
    )
    # print(parts.isnull().sum())
    documents.extend(
        Document(page_content=str(part))
        for part in parts.apply(lambda row: constructor(*row), axis=1)
    )

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(
    documents=splits, embedding=OllamaEmbeddings(model="nomic-embed-text")
)

retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = OllamaLLM(model="llama3.2", temperature=0)


def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke("tell me the specifications of AMD Ryzen 7 7800X3D")
print(result)
