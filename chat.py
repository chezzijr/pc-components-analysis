import sys
from langchain.schema import AIMessage, HumanMessage, StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from os.path import exists
from parts import CPU, VGA, RAM, SSD, HDD, Mainboard
from langchain_community.document_loaders import TextLoader
from typing import Any

def chat():
    # if db exists, load it, else create it
    if exists("./chroma_langchain_db"):
        vectorstore = Chroma(
            collection_name="pc_parts",
            persist_directory="./chroma_langchain_db",
            embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
        )
    else:
        models = [CPU, VGA, RAM, SSD, HDD, Mainboard]
        documents = []
        for model in models:
            name = model.__name__.lower()
            file_path = "./documents/{}.txt".format(name)
            loader = TextLoader(file_path)
            documents.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OllamaEmbeddings(model="nomic-embed-text"),
            persist_directory="./chroma_langchain_db",
            collection_name="pc_parts",
        )

    retriever = vectorstore.as_retriever()
    llm = Ollama(model="llama3.2:1b", callbacks=CallbackManager([StreamingStdOutCallbackHandler()]))

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    chat_history = []
    while (question := input("Question: ")) != "quit":
        ai_response = rag_chain.invoke({
            "input": question,
            "chat_history": chat_history,
        })
        chat_history.extend([
            HumanMessage(content=question),
            AIMessage(content=ai_response["answer"]),
        ])
