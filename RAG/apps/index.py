from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).parent.parent / "data" / "sample.pdf"

#PDF loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

#Text Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#embedd chunks into openai embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Create a Qdrant vector store
vector_store = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="sample_collection"
    url="http://localhost:6333"
)
