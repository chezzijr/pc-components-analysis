import sys
from langchain.schema import AIMessage, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.callbacks.manager import CallbackManager
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import create_history_aware_retriever
from os.path import exists
from parts import CPU, VGA, RAM, SSD, HDD, Mainboard
from langchain_community.document_loaders import TextLoader


def few_shot_prompt():
    examples = [
        {
            "input": "What is the cheapest price of AMD Ryzen 7 7800X3D CPU",
            "context": """
AMD Ryzen 7 7800X3D CPU (central processing unit) has these specifications:
- Cores: 8
- Base frequency: 4.2 GHz
- Boost frequency: 5.0 GHz
- Thermal design power (TDP): 120 W
- Integrated graphics: Radeon
- Supports simultaneous multithreading (SMT)
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
            "output": """
Let's break down the steps to find the cheapest price of AMD Ryzen 7 7800X3D CPU (central processing unit):
As from the context, prices for AMD Ryzen 7 7800X3D CPU are as follows:
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
Find the cheapest by ordering the prices in ascending order:
10890000 < 11890000 < 11990000 < 11990000 < 27680000 < 28880000 < 28980000 < 28980000 < 29680000 < 29980000 < 34680000 < 34680000 < 36680000 < 45680000 < 48860000 < 54680000
Therefore, the cheapest price of AMD Ryzen 7 7800X3D CPU is 10890000 VND at https://tinhocngoisao.com (updated at 2024-11-08).
Answer: 10890000 VND at https://tinhocngoisao.com (updated at 2024-11-08)
""",
        },
        {
            "input": "What is the price of Gigabyte WINDFORCE OC GeForce RTX 4070 VGA",
            "context": """
Gigabyte WINDFORCE OC GeForce RTX 4070 VGA (Video Graphics Adapter) has these specifications:
- Chipset: GeForce RTX 4070
- Memory: 12.0 GB
- Core clock: 1920.0 MHz
- Boost clock: 2490.0 MHz
- Length: 261 mm
Prices for Gigabyte WINDFORCE OC GeForce RTX 4070 VGA are as follows:
- 26990000 VND at https://gearvn.com (updated at 2024-11-10)
- 19490000 VND at https://gearvn.com (updated at 2024-11-10)

""",
            "output": """
Let's break down the steps to find the price of Gigabyte WINDFORCE OC GeForce RTX 4070 VGA (Video Graphics Adapter):
The information about prices is as follows:
The price of Gigabyte WINDFORCE OC GeForce RTX 4070 VGA (Video Graphics Adapter) is as follows:
- 26990000 VND at https://gearvn.com (updated at 2024-11-10)
- 19490000 VND at https://gearvn.com (updated at 2024-11-10)
Therefore, the price of Gigabyte WINDFORCE OC GeForce RTX 4070 VGA is 26990000 VND at https://gearvn.com (updated at 2024-11-10),
and 19490000 VND at https://gearvn.com (updated at 2024-11-10).
Answer: 
- 26990000 VND at https://gearvn.com (updated at 2024-11-10)
- 19490000 VND at https://gearvn.com (updated at 2024-11-10)
""",
        },
        {
            "input": "What is the price of Western Digital Black SN850X SSD",
            "context": """
Western Digital Black SN850X SSD (Solid State Drive) has these specifications:
- Capacity: 2000 GB
- Cache: Unknown
- Form factor: M.2-2280
- Interface: M.2 PCIe 4.0 X4
""",
            "output": """
Let break down the steps to find the price of Western Digital Black SN850X SSD (Solid State Drive):
As the price of Western Digital Black SN850X SSD is not provided in the context, we do not have the information to answer the question.
Therefore, we cannot provide the price of Western Digital Black SN850X SSD.
Answer: I don't know the price of Western Digital Black SN850X SSD.
            """,
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages([
        ("system", "The queried context is: {context}"),
        ("human", "Question: {input}"),
        ("ai", "Answer: {output}"),
    ])

    prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    return prompt


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

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OllamaEmbeddings(model="nomic-embed-text"),
            persist_directory="./chroma_langchain_db",
            collection_name="pc_parts",
        )

    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 6}
    )
    llm = ChatOllama(
        model="llama3.2:1b",
        num_ctx=2 * 4096,
        num_gpu=20,
        callbacks=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0,
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Your job is to explain to user about computer parts, "
        "then suggest them where to buy with reasonable price "
        "from different sources if possible, and also compare "
        "the prices so that user can choose the cheapeat option. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "Context: {context}"
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
        few_shot_prompt(),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    chat_history = []
    while (question := input("Question: ")) != "quit":
        # relevant_docs = retriever.invoke(question)
        # for doc in relevant_docs:
        #     print(doc.page_content)
        ai_response = rag_chain.invoke({
            "input": question,
            "chat_history": chat_history,
        })
        chat_history.extend([
            HumanMessage(content=question),
            AIMessage(content=ai_response["answer"]),
        ])
