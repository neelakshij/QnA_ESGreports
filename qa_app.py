import streamlit as st
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import vertexai
import langchain
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import VertexAI
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate

st.set_page_config(page_title='ESG-Report-Q-n-A', page_icon='♻️')
st.markdown('## Q-n-A with Environmental, Social, and Governance Reports 🌱')
placeholder_text="choose from options"

llm=VertexAI(model_name="text-bison@001", max_output_tokens=500, temperature=0, top_p=0.8, top_k=40, verbose=True)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def main():
           
    fpath=None
    pagelist = []
    df = pd.read_csv('./gcs-bucket/ESG_Report_files.csv')
    
    fpath = get_report_input(df)
  
    if fpath:
        pages = fileloader(fpath)

        if 'vectordb' not in st.session_state:
            vectordb = None
            persist_directory = "vectordb"
            st.session_state.vectordb = Chroma.from_documents(documents=pages,
                                                              embedding=embeddings,
                                                              persist_directory=persist_directory)
            st.session_state.vectordb.persist()
    
    query = get_user_query()

    #if (query and vectordb):
    if query and ('vectordb' in st.session_state):
        print(fpath)
        prompt_template = """Use the following pieces of context to answer the question at the end.\ 
         If you don't know the answer, just say that information is not available, don't try to make up an answer.\
         Keep the answer as concise as possible and present as a bullet points.\ 
         Always say "thanks for asking!" at the end of the answer, in new line. 
         {context}
         Question: {question}
         Answer:"""
        
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"] )
        chain_type_kwargs = {"prompt": PROMPT}
        
        qa_retriever = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",
                                                   retriever=st.session_state.vectordb.as_retriever(), 
                                                   chain_type_kwargs=chain_type_kwargs, 
                                                   return_source_documents=True, verbose=False )
        result = qa_retriever({"query": query})
        for i in range(len(result["source_documents"])): 
            pagelist.append((result["source_documents"][i].metadata.get('page')))
        
       
        st.header('Response:', divider='rainbow')
        st.write(result["result"])
        
        st.subheader('Sources', divider='green')
        st.write("reference page numbers: ",pagelist)
        
    #if 'vectordb' in st.session_state:
     #   vectordb = None
        
# End of main function

def get_report_input(df):
    '''
    Take user input: first year
    for selected year, filter the dataframe to collect company names of which reports are available in bucket.
    For selected year and company, get filepath to retrieve the report.
    '''
    df1 = None
    file_path=''
    st.sidebar.header("First select year and then company.", divider='blue')
    
    chosen_year = st.sidebar.selectbox("Select a year", df['year'].unique(), index=None, 
                                       placeholder=placeholder_text)
    if chosen_year:
        company_options = df[df['year'] == chosen_year]['company_name'].unique()
        chosen_company = st.sidebar.selectbox("Choose a company", company_options,
                                              index=None, placeholder=placeholder_text)
    if st.sidebar.button('Retrieve'):
        st.sidebar.write("Retrieving the report for : ", chosen_company, "for year ",chosen_year)
        df1 = df[(df['year'] == chosen_year) & (df['company_name'] == chosen_company)]
        file_path = df1['filepath'].item() # pass to llm-pdfloader
    return file_path


def fileloader(pdffile):
    loader = PyPDFLoader(pdffile)
    pages = loader.load_and_split()
    return pages


def get_user_query():
    '''
    Get user query: user can choose from sample queries or can write their own.
    After query submit button is pressed, identify the query.
    '''
    user_query =""
    # Create the selectbox for sample queries
    sample_queries = sampleQueries()
    
    #with col1:
    selected_query = st.selectbox("Choose a sample query", sample_queries, 
                                  index=None,
                                  placeholder=placeholder_text)
    # Create the text input for user-written query
    given_query = st.text_input("Or write your own query")
    submit=st.button('Submit')

    # Create the submit button
    if submit:
        # Check if the user has written their own query
        if given_query:
            user_query = given_query
        elif selected_query:
            user_query = selected_query
        
        st.write("Looking into the report .... ")
    return(user_query)
  

def sampleQueries():
    # sample queries
    sample_queries = ["What are the company's views on climate change?",
                      "What are the company' plans to become more energy efficient?",
                      "Which are the highlights of this report?",
                      "How the company is going to achieve carbon neutrality?",
                      "How the company manages its water consumption?",
                      "How the company manages its energy consumption?",
                      "How is waste handled by the company?",
                      "Which future targets are mentioned in the report?",
                      "What are the company's plan to achive their targets?"
                      "How many targets the company have achieved? Which are those?",
                      "Which targets the company could not meet?"
                      "How did the company support their employes during the Covid Pandemic?"]
    return sample_queries
    
                        
if __name__ == '__main__':
    main()
