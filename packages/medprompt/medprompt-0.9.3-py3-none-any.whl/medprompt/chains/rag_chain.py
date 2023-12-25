"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


import os
from typing import List
from kink import di
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.tools import tool
from langchain.vectorstores import Chroma, Redis, FAISS
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from ..tools.create_embedding import CreateEmbeddingFromFhirBundle


from .. import MedPrompter
# from ..tools import CreateEmbeddingFromFhirBundle

med_prompter = MedPrompter()
_TEMPLATE = """Given the following chat history and a follow up question, rephrase the
follow up question to be a standalone question, in its original language that includes context from chat history below.

Chat History:
{chat_history}
Follow Up Question: {input}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_TEMPLATE)

ANSWER_TEMPLATE = """Answer the following question based only on the available context below.

Context:
{context}

Question:
{input}

"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")
EMBED_MODEL = di["embedding_model"]
INDEX_SCHEMA = di["index_schema"]
REDIS_URL = di["redis_url"]
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
VECTORSTORE_NAME = di["vectorstore_name"]


main_llm = di["rag_chain_main_llm"]
clinical_llm = di["rag_chain_clinical_llm"]

def check_index(input_object):
    patient_id = input_object["patient_id"]
    try:
        if VECTORSTORE_NAME == "redis":
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Redis.from_existing_index(
                embedding=embedding, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
        elif VECTORSTORE_NAME == "chroma":
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Chroma(collection_name=patient_id, persist_directory=di["vectorstore_path"], embedding_function=embedding)
            vectorstore.persist()
        elif VECTORSTORE_NAME == "faiss":
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            fname = di["vectorstore_path"] + "/" + patient_id + ".index"
            vectorstore = FAISS.load_local(fname, embeddings=embedding)
        else:
            return "No vector store defined."
    except:
        return "Failed to create index for patient with id: " + patient_id
    return vectorstore.as_retriever().get_relevant_documents(input_object["input"], k=10)


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    _reply = document_separator.join(doc_strings)
    if len(_reply.strip()) < 3:
        _reply = "No information found. The vectorstore may still be indexing. Please try again later."
    return _reply


def _format_chat_history(chat_history: List[str]) -> str:
    """Format chat history into a string."""
    buffer = ""
    if not chat_history:
        return buffer
    for dialogue_turn in chat_history:
        buffer += "\n" + dialogue_turn
    return buffer

# User input
class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[str] = Field(default=[])
    input: str = Field(default="Give a summary.")
    patient_id: str = Field(default="123456")

def get_runnable(**kwargs):
    """Get the runnable chain."""
    context = RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"]),
        patient_id=lambda x: x["patient_id"],
        input=lambda x: x["input"],
    ) | check_index | _combine_documents
    input = RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"]),
        patient_id=lambda x: x["patient_id"],
        input=lambda x: x["input"],
    ) | CONDENSE_QUESTION_PROMPT | main_llm | StrOutputParser()
    _inputs = RunnableMap(
        context=context,
        input=input,
    )
    _chain = _inputs | ANSWER_PROMPT | clinical_llm | StrOutputParser()
    chain = _chain.with_types(input_type=ChatHistory)
    return chain

@tool("last attempt", args_schema=ChatHistory)
def get_rag_tool(**kwargs):
    """
    Returns a chain that can be used to finally answer a question based on a patient's medical record.
    Use this chain to answer a question as a final step if it was not found before.
    Do not use this tool again with the same input/query.
    Use the tool to create index for medical record before using this tool.

    Args:
        patient_id (str): The id of the patient to search for.
        input (str): The question to ask the model based on the available context.
        chat_history (List): The previous conversation history.
    """
    return get_runnable().invoke(kwargs)
