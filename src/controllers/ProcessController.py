from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ProcessEnum
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class ProcessController(BaseController):
    def __init__(self, project_id: int):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)
        
    def get_file_extension(self, file_id : str):
        file_extension = os.path.splitext(file_id)[-1]
        return file_extension
    
    def get_file_loader(self, file_id:str):
        file_extension = self.get_file_extension(file_id= file_id)
        file_path = os.path.join(self.project_path, file_id)
        
        if file_extension == ProcessEnum.TXT.value:
            return TextLoader(file_path= file_path, encoding='utf-8')
        
        if file_extension == ProcessEnum.PDF.value:
            return PyMuPDFLoader(file_path= file_path)
        
        return None
    
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def split_file_content(self, file_content: list, chunk_size: int = 100, overlap:int =20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=overlap)
        
        text_chunks = text_splitter.split_documents(file_content)
        
        return text_chunks
        
        
        