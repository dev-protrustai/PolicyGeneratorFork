from langchain_community.document_loaders import PyPDFLoader

from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
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

def process_pdf(llm,pdf_doc,question):
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
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    results = rag_chain.invoke({"input": question})
    return results["answer"]
