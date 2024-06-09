
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.prompt import *
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY=os.getenv("openai_api_key")
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

def file_processing(filepath):
    loader=PyPDFLoader(filepath)
    data=loader.load()

    question_gen = ""
    for page in data:
        question_gen+=page.page_content

    splitter_question_gen=TokenTextSplitter(
        model_name = "gpt-3.5-turbo",
        chunk_size = 10000,
        chunk_overlap = 200
    )

    chunk_queue_gen=splitter_question_gen.split_text(question_gen)

    document_que_gen=[Document(page_content = t) for t in chunk_queue_gen]

    splitter_answer_gen=TokenTextSplitter(
        model_name = "gpt-3.5-turbo",
        chunk_size = 1000,
        chunk_overlap = 100
    )

    document_ans_gen=splitter_answer_gen.split_documents(document_que_gen)
    
    return document_que_gen, document_ans_gen


def llm_pipeline(filepath):
    
    document_que_gen, document_ans_gen=file_processing(filepath)

    PROMPT_QUESTIONS=PromptTemplate(
        template=prompt_template,
        input_variables=["text"]
    )
    REFINE_PROMPT_QUESTIONS=PromptTemplate(
        template=refined_template,
        input_variables=["existing_answer","text"]
    )

    llm_ques_gen_pipeline=ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.3
        )

    chain_ques_gen=load_summarize_chain(
        llm=llm_ques_gen_pipeline,
        chain_type="refine",
        verbose=True,
        question_prompt=PROMPT_QUESTIONS,
        refine_prompt=REFINE_PROMPT_QUESTIONS)

    ques=chain_ques_gen.run(document_que_gen)

    question_list=ques.split("\n")

    embeddings=OpenAIEmbeddings()


    vector_store=FAISS.from_documents(
        document_ans_gen,
        embeddings
    )

    llm_answer_gen=ChatOpenAI(
        temperature=0.1,
        model_name="gpt-3.5-turbo"
        )

    answer_generation_chain=RetrievalQA.from_chain_type(
        llm=llm_answer_gen,
        retriever=vector_store.as_retriever(),
        chain_type="stuff"
    )

    return question_list, answer_generation_chain

