from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
class DataController(BaseController):
    def __init__(self):
        super().__init__()
    
    def validate_file_uploaded(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * 1045876 : #size scalling 
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_IS_VALID.value
        
        