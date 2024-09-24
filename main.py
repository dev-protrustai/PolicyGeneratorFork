__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Policy Generator")
    #url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    url_input = st.text_input("Paste your link here:")
    location_input = st.text_input("customer location: for example EU")
    data_collection_input = st.multiselect('what data users collect', ["Log and Usage Data","Device Data","Location Data"])
    user_control_right_input = st.text_input("enter your user control right here")
    company_sharing_level_input = st.selectbox('how the company uses those data ', ["All parties","Limited third parties"])
    default_link = None
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Policy Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


