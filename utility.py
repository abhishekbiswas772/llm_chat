import re
from dataclass_utility import ChatResponse
from langchain.schema import HumanMessage, SystemMessage
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
import PyPDF2
import os
import tempfile
import time
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

embedding  = OpenAIEmbeddings(
    show_progress_bar=True,
    model="text-embedding-3-large"
)

def create_db() -> PineconeVectorStore:
    try:
        index_name = os.getenv("INDEX_NAME")
        pc = Pinecone()
        index = pc.Index(index_name)
        vector_store = PineconeVectorStore(index=index, embedding=embedding, pinecone_api_key=os.getenv("PINECONE_API_KEY"))
        return vector_store
    except Exception as e:
        print(e)
        return None

def handle_image_response(res : str, user_question: str) -> ChatResponse:
    from llm_calls import llm
    pattern = r'FILE_PATH:\s*"([^"]+)"'
    match = re.search(pattern, res)
    file_path = match.group(1) if match else None
    cleaned_content = llm.invoke([
        SystemMessage("Remove the file path and make respone as 'The image of .. has been generated'"),
        HumanMessage(res),
    ]).content
    return ChatResponse(question=user_question, answer=cleaned_content, document_path=file_path)

def handle_pdf_ingestion_tempfile(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        # Explicitly check if file exists and is readable
        if not os.path.exists(temp_path):
            print(f"Temporary file {temp_path} does not exist.")
            return False

        file_ext = Path(temp_path).suffix.lower()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
        )
        vector_store = create_db()
        
        if vector_store is None:
            print("Vector DB setup failed")
            return False

        print("Vector DB is successfully setup")

        try:
            if file_ext == ".txt":
                # Add error handling for TextLoader
                try:
                    loader = TextLoader(temp_path, encoding='utf-8')  # Specify encoding
                    documents = loader.load_and_split(text_splitter)
                    vector_store.add_documents(documents)
                    print("Text file successfully processed and indexed.")
                    return True
                except Exception as txt_error:
                    print(f"Error loading text file: {txt_error}")
                    return False

            elif file_ext == ".pdf":
                pdfReader = PyPDF2.PdfReader(temp_path)
                totalPages = len(pdfReader.pages)
                if totalPages < 5:
                    loader = PyMuPDFLoader(temp_path)
                    documents = loader.load_and_split(text_splitter)
                    vector_store.add_documents(documents)
                    print("PDF file successfully processed and indexed.")
                    return True
                else:
                    print("PDF has 5 or more pages, skipping processing.")
                    return False
            else:
                print("Unsupported file format.")
                return False
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            return False
        finally:
            # Ensure temporary file is deleted
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    except Exception as overall_error:
        print(f"Overall error in file processing: {overall_error}")
        return False


def get_retriver():
    db = create_db()
    retriver = db.as_retriever()
    return retriver

