from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate,
)
from os.path import exists
from parts import CPU, VGA, RAM, SSD, HDD, Mainboard


def chat():
    models = [CPU, VGA, RAM, SSD, HDD, Mainboard]

    documents = []
    for model in models:
        name = model.__name__.lower()
        with open("./documents/{}.txt".format(name), "r") as f:
            content = f.read()
            document = Document(page_content=content, title=name)
            documents.append(document)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    if exists("./chroma_langchain_db"):
        vectorstore = Chroma(
            collection_name="pc_parts",
            persist_directory="./chroma_langchain_db",
            embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
        )
    else:
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OllamaEmbeddings(model="nomic-embed-text"),
            persist_directory="./chroma_langchain_db",
            collection_name="pc_parts",
        )

    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )

    few_shot_examples = [
        {
            "input": "Give me the price of the AMD Ryzen 7 7800X3D CPU",
            "output": """
Prices for AMD Ryzen 7 7800X3D CPU are as follows:
- 48860000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 11990000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 29680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 28880000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 36680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 54680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 28980000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 29980000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 28980000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 34680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 27680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 45680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 34680000 VND at https://ttgshop.vn (updated at 2024-11-08)
- 11990000 VND at https://gearvn.com (updated at 2024-11-08)
- 10890000 VND at https://tinhocngoisao.com (updated at 2024-11-08)
- 11890000 VND at https://memoryzone.com.vn (updated at 2024-11-08)
""",
        },
        {
            "input": "What is the specifications of the AMD Ryzen 5 7600X CPU?",
            "output": """
AMD Ryzen 5 7600X CPU (central processing unit) has these specifications:
- Cores: 6
- Base frequency: 4.7 GHz
- Boost frequency: 5.3 GHz
- Thermal design power (TDP): 105 W
- Integrated graphics: Radeon
- Supports simultaneous multithreading (SMT)
""",
        },
        {
            "input": "What is the price of the MSI GeForce RTX 3060 Ventus 2X 12G GeForce RTX 3060 12GB VGA?",
            "output": "Sorry I don't have the price of the MSI GeForce RTX 3060 Ventus 2X 12G GeForce RTX 3060 12GB VGA",
        },
    ]

    few_shot_template = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}"),
    ])

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=few_shot_template,
        examples=few_shot_examples,
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are an assistant for question-answering tasks. "
                "Your purpose is to provide information about computer parts and also to provide suggestion. "
                "This will help users to choose the right parts for their PC build. "
                "Information about computer parts consists of specifications and prices. "
                "Use the following pieces of retrieved context to answer the question. "
                "If you don't know the answer, just say that you don't know. "
                "Use three sentences maximum and keep the answer concise.\n"
            ),
        ),
        few_shot_prompt,
        ("user", "{question}"),
        ("user", "{context}"),
    ])

    llm = OllamaLLM(model="llama3.2:1b")

    def format_docs(documents):
        return "\n\n".join(doc.page_content for doc in documents)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    while (question := input("Question: ")) != "quit":
        result = rag_chain.invoke(question)
        print(result)
