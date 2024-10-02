from langchain_community.document_loaders import PyPDFLoader

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain.chains import (ConversationalRetrievalChain,create_retrieval_chain,create_history_aware_retriever)
from langchain.chains.combine_documents import create_stuff_documents_chain
import tempfile
import os

# def load_file(file_path):




    # sys.modules['sqlite3'] = sys.modules["pysqlite3"]




    # llm = ChatGroq(model="llama3-8b-8192")

    # llm = ChatGroq(
    # temperature=0, 
    # groq_api_key='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', 
    # model_name="llama-3.1-70b-versatile"
    # )
    # response = llm.invoke("The first person to land on moon was ...")

    # # loader = WebBaseLoader("https://jobs.nike.com/job/R-35349")
    # # page_data = loader.load().pop().page_content

    # prompt_extract = PromptTemplate.from_template(
    #         """
    #         ### SCRAPED TEXT FROM WEBSITE:
    #         {page_data}
    #         ### INSTRUCTION:
    #         The scraped text is from the career's page of a website.
    #         Your job is to extract the job postings and return them in JSON format containing the 
    #         following keys: `role`, `experience`, `skills` and `description`.
    #         Only return the valid JSON.
    #         ### VALID JSON (NO PREAMBLE):    
    #         """
    # )

    # chain_extract = prompt_extract | llm 
    # res = chain_extract.invoke(input={'page_data':page_data})


def get_pdf_text(pdf_docs):
    docs=[]
    # for pdf in pdf_docs:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, pdf_docs.name)
    with open(path, "wb") as f:
            f.write(pdf_docs.getvalue())
    loader = PyPDFLoader(path)
    docs=loader.load_and_split()
    # print(docs)
    return  docs


def process_pdf(pdf_doc):
    # loader = PyPDFLoader(file_path)
    # docs = uploaded_file.getvalue().decode("utf-8")
    # print(pdf_doc)
    # print(pdf_doc.getvalue())


    docs = get_pdf_text(pdf_doc)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                        model_kwargs={'device':'cpu'})
    # Create vectors

    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

    # print(index)
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # vectorstore = faiss.FAISS.from_documents(docs, embeddings)

    uuids = [str(uuid4()) for _ in range(len(docs))]

    vector_store.add_documents(documents=docs, ids=uuids)

    retriever = vector_store.as_retriever()
    return  retriever

    ### version 1
    # system_prompt = (
    #     "You are an assistant for question-answering tasks. "
    #     "Use the following pieces of retrieved context to answer "
    #     "the question. If you don't know the answer, say that you "
    #     "don't know. Use three sentences maximum and keep the "
    #     "answer concise."
    #     "\n\n"
    #     "{context}"
    # )
    # # print(input_system_prompt == "")
    # final_system_prompt = input_system_prompt if input_system_prompt != "" else system_prompt
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", final_system_prompt),
    #         ("human", "{input}"),
    #     ]
    # )
    # question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    # results = rag_chain.invoke({"input": question})

    ## version2

def get_rag_chain(llm,retriever):



    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


    # template = """Answer the question in your own words as truthfully as possible from the context given to you.
    #     If you do not know the answer to the question, simply respond with "I don't know. Can you ask another question".
    #     If questions are asked where there is no relevant context available, simply respond with "I don't know. Please ask a question relevant to the documents"
    #     Context: {context}

    #     {chat_history}
    #     user: {question}
    #     assistant: """

    # prompt = PromptTemplate(
    #     input_variables=["context", "chat_history", "question"], template=template
    # )

    # # Create the custom chain
    # chain = ConversationalRetrievalChain.from_llm(
    #     llm=llm, retriever=retriever,
    #     get_chat_history=get_chat_history, return_source_documents=True,
    #     combine_docs_chain_kwargs={'prompt': prompt})
    # results = chain.invoke()
    return rag_chain
