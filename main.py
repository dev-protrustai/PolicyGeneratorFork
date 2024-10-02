__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_util import process_pdf,get_rag_chain
from typing import Generator


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
def get_chat_history():
    messages=[
            {
                "role": m["role"],
                "content": m["content"]
            }
            for m in st.session_state.messages
        ]
    return messages
def create_streamlit_app(llm, portfolio, clean_text):
    #st.title("Email Generator")
    #url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    #url_input = st.text_input("Paste your link here:",value = "https://jobs.nike.com/job/R-35349" )
    # location_input = st.text_input("customer location: for example EU")
    # data_collection_input = st.multiselect('what data users collect', ["Log and Usage Data","Device Data","Location Data"])
    # user_control_right_input = st.text_input("enter your user control right here")
    # company_sharing_level_input = st.selectbox('how the company uses those data ', ["All parties","Limited third parties"])
    # default_link = None
    #submit_button = st.button("Email Generator Submit")

    # st.title("Check sidebar and upload template for Policy Generator")

    with st.sidebar:
        st.title("Upload your PDF files here:")
        pdf_docs = st.file_uploader("You may upload multiple files. Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            st.session_state.retriever = process_pdf(pdf_docs)

            with st.spinner("Processing..."):
                # docs = get_pdf_text(pdf_docs)
                # text_chunks = get_text_chunks(docs)
                # get_vector_store(text_chunks,GOOGLEPALM_API_KEY)
                st.success("Done")

    # version1
    # Ask the user for a question via `st.text_area`.
    # question = st.text_area(
    #     "Now ask a question about the document!",
    #     placeholder="Can you give me a short summary?",
    #     disabled=not pdf_doc,
    # )
    # 
    # system_prompt = st.text_area(
    #     "(Optional) Input your experiment system prompt",
    #     value = "You are an assistant for question-answering tasks. "
    #     "Use the following pieces of retrieved context to answer "
    #     "the question. If you don't know the answer, say that you "
    #     "don't know. Use three sentences maximum and keep the "
    #     "answer concise."
    #     "\n\n"
    #     "{context}",
    #     disabled=not pdf_doc,
    # )



    # version2


    if prompt := st.chat_input("Ask the question about the doc..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar='😃'):
            st.markdown(prompt)

        # Fetch response from Groq API
        try:

            rag_chain = get_rag_chain(llm.llm, st.session_state.retriever)
            result = rag_chain.invoke({"input": prompt, "chat_history": get_chat_history()})
            chat_completion = result["answer"]
            # Use the generator function with st.write_stream
            with st.chat_message("assistant", avatar="📖"):
                # chat_responses_generator = generate_chat_responses(chat_completion)
                # full_response = st.write_stream(chat_responses_generator)
                st.write(chat_completion)
                full_response = chat_completion
                # print("full_response",full_response)

        except Exception as e:
            st.error(e, icon="🚨")

        # Append the full response to session_state.messages
        if isinstance(full_response, str):
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})

        else:
            # Handle the case where full_response is not a string
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": combined_response})






    # if pdf_doc and question:
    #     ans = process_pdf(llm.llm,pdf_doc,question,system_prompt)
    #     st.write(ans)

        # Process the uploaded file and question.
        # document = uploaded_file.read().decode()
        # messages = [
        #     {
        #         "role": "user",
        #         "content": f"Here's a document: {document} \n\n---\n\n {question}",
        #     }
        # ]

        # # Generate an answer using the OpenAI API.
        # stream = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=messages,
        #     stream=True,
        # )

        # Stream the response to the app using `st.write_stream`.
        # print(ans)
    # if submit_button:
    #     try:
    #         loader = WebBaseLoader([url_input])
    #         data = clean_text(loader.load().pop().page_content)
    #         portfolio.load_portfolio()
    #         jobs = llm.extract_jobs(data)
    #         for job in jobs:
    #             skills = job.get('skills', [])
    #             links = portfolio.query_links(skills)
    #             email = llm.write_mail(job, links)
    #             st.code(email, language='markdown')
    #     except Exception as e:
    #         st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Policy Generator", page_icon="📧")

    ## version2
    # Initialize chat history and selected model
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.retriever = None
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = '🧽️' if message["role"] == "assistant" else '😃'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    create_streamlit_app(chain, portfolio, clean_text)


