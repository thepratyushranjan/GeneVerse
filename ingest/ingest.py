from langchain.document_loaders import PyPDFLoader, TextLoader,  UnstructuredWordDocumentLoader, Docx2txtLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import os



from docx import Document

class Docx2txtLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        doc = Document(self.file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    


def document_loader(uploaded_file):
    if uploaded_file:
        file_extension = uploaded_file.filename.split('.')[-1].lower()

        if file_extension in ['pdf', 'txt']:
            save_path = os.path.join('media/data', uploaded_file.filename)
            uploaded_file.save(save_path)
            loader = PyPDFLoader(save_path) if file_extension == 'pdf' else TextLoader(save_path)
            return loader
        elif file_extension in ['doc', 'docx']:
            save_path = os.path.join('media/data', uploaded_file.filename)
            uploaded_file.save(save_path)
            loader = Docx2txtLoader(save_path) if file_extension == 'doc' else UnstructuredWordDocumentLoader(save_path)
        else:
            return "Unsupported file format. Please upload a .pdf or .txt file."
        






# Commented code is write in the Flask .

# def document_loader(uploaded_file):
#     if uploaded_file:
#         file_extension = uploaded_file.filename.split('.')[-1].lower()
#         if file_extension in ['pdf']:
#             uploaded_file.save(os.path.join('media/data', uploaded_file.filename))
#             loader = PyPDFLoader(os.path.join('media/data', uploaded_file.filename))
#             return loader
#         elif file_extension in ['txt']:
#             uploaded_file.save(os.path.join('static/data', uploaded_file.filename))
#             loader = TextLoader(os.path.join('static/data', uploaded_file.filename))
#             return loader
#         elif file_extension in ['doc', 'docx']:
#             uploaded_file.save(os.path.join('static/data', uploaded_file.filename))
#             # loader = Docx2txtLoader(os.path.join('static/data', uploaded_file.filename))
#             # loader = UnstructuredWordDocumentLoader(os.path.join('static/data', uploaded_file.filename))
#             return loader
#         else:
#             return "Unsupported file format. Please upload a .pdf, .txt, or .docx file."
        
        
def create_embeddings(loader):
    chunks = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    return chunks, embeddings
