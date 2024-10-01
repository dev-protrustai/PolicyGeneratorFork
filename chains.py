import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the job portal's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are XYZ, a B.Tech Student from RCPIT college . 
            Your job is to write a cold email to the HR regarding the job mentioned above describing the capability of student
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase student's portfolio: {link_list}
            Remember you are XYZ, B.Tech CSE at RCPIT. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        print (job)
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    
    def write_policy_template(self, job, links):
        prompt_policy_template = PromptTemplate.from_template(
            """

                You are XYZ, a policy review writer . 
                Your job is to write a website policy to stay compliant.  
                There will be one section named policy section.
                Under this section there is one <paragraph>

                Use the following pieces of retrieved context to fill <paragraph> in bold text.
                
                If you don't know the answer, say that you
                don't know. Use three sentences maximum and keep <paragraph> in bold text concise.


                {context}


            """
        )
        chain_email = prompt_policy_template | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))