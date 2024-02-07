import logging
import sys
import torch
import os
import streamlit as st

from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index.llms import HuggingFaceLLM
from llama_index.prompts import PromptTemplate
from llama_index import VectorStoreIndex, set_global_service_context, ServiceContext, SimpleDirectoryReader, \
    load_index_from_storage
import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
import logging
from config import Config

os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Model names (make sure you have access on HF)
LLAMA2_7B = "meta-llama/Llama-2-7b-hf"
LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
LLAMA2_13B = "meta-llama/Llama-2-13b-hf"
LLAMA2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
LLAMA2_70B = "meta-llama/Llama-2-70b-hf"
LLAMA2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"

selected_model = LLAMA2_7B_CHAT

SYSTEM_PROMPT = """You are an AI assistant that answers questions in a friendly manner, based on the given source documents. Here are some rules you always follow:
- Generate human readable output, avoid creating output with gibberish text.
- Generate only the requested output, don't include any other language before or after the requested output.
- Never say thank you, that you are happy to help, that you are an AI agent, etc. Just answer directly.
- Generate professional language typically used in business documents in North America.
- Never generate offensive or foul language.
"""

query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=2048,
    generate_kwargs={"temperature": 0.0, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=selected_model,
    model_name=selected_model,
    device_map="auto",
    # change these settings below depending on your GPU
    model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True},
)

print('created chroma client')
try:
    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("bitcoinbook")
except Exception as e:
    print('Error creating chroma_collection' + str(e))

print('loading documents')
try:
    documents = SimpleDirectoryReader("./data/bitcoinbook/").load_data()
except Exception as e:
    print('Error loading documents' + str(e))

embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
)

service_context = ServiceContext.from_defaults(
     llm=llm, embed_model=embed_model
)
set_global_service_context(service_context)

try:
    db = chromadb.PersistentClient(path="./storage/chroma")
    chroma_collection = db.get_or_create_collection("bitcoinbook")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # if index exists, load it
    if os.path.exists("./storage/chroma/bitcoinbook"):
        index = load_index_from_storage("./storage/chroma/bitcoinbook")
        print('index from storage loaded')
    else:
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context,
                                                service_context=service_context)
        print('index generated and persisted to disk')

    query_engine = index.as_query_engine(
        verbose=True,
    )


except Exception as e:
    print('Error loading index or creating new index and persisted to disk' + str(e))


config = Config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.LOG_LEVEL))
log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL_INT)

st.set_page_config(page_title=config.PAGE_TITLE, page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)


st.title(config.PAGE_TITLE)
st.info(config.PAGE_INFO, icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Frag etwas zu den Geschäftsberichten von den Schweizer Kantonalbanken TKB, SGKB, AKB und BLKB"}
    ]


if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
