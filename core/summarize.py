# # from langchain_mistralai import ChatMistralAI
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_core.output_parsers import StrOutputParser
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# # import os

# # def get_llm():
# #     return ChatMistralAI(model = "mistral-small-latest", mistral_api_key = os.getenv("MISTRAL_API_KEY"), temperature = 0.4)

# # #When we encounter big text after transcription, we need to split it before sending this to the AI

# # def split_transcript(transcript:str)->list:
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size = 3000,
# #         chunk_overlap = 200
# #     )

# #     return splitter.split_text(transcript)

# # #After getting the chunk from the transcribed video, we generate the summary

# # def summarize(transcript:str)->str:
# #     llm = get_llm()

# #     #Generates a short summary of each chunk that is sent, seperately
# #     map_prompt = ChatPromptTemplate.from_messages(
# #         [
# #             ("system", "Summarize this portion of a meeting transcript concisely."),
# #             ("human", "{text}"),
# #         ]
# #     )

# #     map_chain = map_prompt | llm | StrOutputParser()

# #     chunks = split_transcript(transcript)

# #     chunk_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

# #     combined = "\n\n".join(chunk_summaries)

# #     combined_prompt = ChatPromptTemplate.from_messages(
# #         [
# #             (
# #                 "system",
# #                 "You are an expert meeting summarizer. Combine these partial summaries "
# #                 "into one final professional meeting summary in bullet points.",
# #             ),
# #             ("human", "{text}"),
# #         ]
# #     )

# #     combined_chain = (
# #         RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
# #     )

# #     return combined_chain.invoke(combined)


# # #Generate a suitable title for the summary
# # def generate_title(transcipt : str) -> str:
# #     llm = get_llm()

    

# #     title_chain = (
# #         RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
# #         ChatPromptTemplate.from_messages([
# #              (
# #                 "system",
# #                 "Based on the meeting transcript, generate a short professional meeting title "
# #                 "(max 8 words). Only return the title, nothing else.",
# #             ),
# #             ("human", "{text}"),
# #         ])
# #         | llm
# #         |StrOutputParser()
# #     )

# #     return title_chain.invoke(transcipt[:2000])

# import os
# from langchain_mistralai import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough, RunnableLambda
# from core.vector_store import build_vector_store, load_vector_store, get_retriever

# def get_llm():
#     return ChatMistralAI(
#         model="mistral-small-latest",
#         mistral_api_key=os.getenv("MISTRAL_API_KEY"),
#         temperature=0.3,
#     )

# def format_docs(docs):
#     return "\n\n".join([doc.page_content for doc in docs])

# def build_rag_chain(transcript:str):

#     vector_store = build_vector_store(transcript)

#     retriever = get_retriever(vector_store, k = 4)

#     llm = get_llm()

#     prompt = ChatPromptTemplate.from_messages(

#         [(
#             "system",
#             """You are an expert meeting assistant. Answer the user's question 
# based ONLY on the meeting transcript context provided below.

# If the answer is not found in the context, say: 
# "I could not find this information in the meeting transcript."

# Always be concise and precise. If quoting someone, mention it clearly.

# Context from meeting transcript:
# {context}""",
#         ),
#         ("human", "{question}"),
#     ]
#     )

#     #full LCEL Rag pipeline 

#     rag_chain = (

#         {"context" : retriever | RunnableLambda(format_docs),
#          "question": RunnablePassthrough()
#          }
#          |prompt|llm|StrOutputParser()
#     )

#     return rag_chain


# def load_rag_chain():
#     vector_store = load_vector_store()
#     retriver = get_retriever()

#     llm = get_llm()
#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """You are an expert meeting assistant. Answer the user's question 
# based ONLY on the meeting transcript context provided below.

# If the answer is not found in the context, say: 
# "I could not find this information in the meeting transcript."

# Always be concise and precise. If quoting someone, mention it clearly.

# Context from meeting transcript:
# {context}""",
#         ),
#         ("human", "{question}"),
#     ])

#     rag_chain = (
#         {
#             "context":  retriver| RunnableLambda(format_docs),
#             "question": RunnablePassthrough(),
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return rag_chain


# def ask_question(rag_chain, question:str) -> str:
#     print(f"Question : {question}")
#     answer = rag_chain.invoke(question)
#     print(f"answer :{answer}")
#     return answer

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os 

def get_llm():
    return ChatMistralAI(model = "mistral-small-latest", mistral_api_key = os.getenv("MISTRAL_API_KEY"),temperature=0.3)


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)

def summarize(transcript : str) -> str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "Summarize this portion of a meeting transcript concisely."),
        ("human", "{text}"),
    ]
    )

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",
        ),
        ("human", "{text}"),
    ]
    )

    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
    )

    return combined_chain.invoke(combined)

def generate_title(transcipt : str) -> str:
    llm = get_llm()

    

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    return title_chain.invoke(transcipt[:2000])