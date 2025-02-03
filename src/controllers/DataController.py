from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()
    
    def validate_file_uploaded(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * 1045876 : #size scalling 
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_IS_VALID.value
    
    def generate_unique_file_path(self, original_file_name:str, project_id: str):
        
        random_file_name = self.generate_random_string()
        
        project_diectory = ProjectController().get_project_path(project_id=project_id)
        
        clean_file_name = self.clean_file_name(file_name= original_file_name)
        
        
        
        new_unique_file_path = os.path.join(project_diectory, random_file_name + "_" + clean_file_name)
        
        
        while os.path.exists(new_unique_file_path):
            random_file_name = self.generate_unique_file_name
            new_unique_file_path = os.path.join(project_diectory, random_file_name + "_" + clean_file_name)
        
        return new_unique_file_path, random_file_name + "_" + clean_file_name
        
        
    def clean_file_name(self, file_name: str):
                    
        cleaned_name = re.sub(r'[^\w_.]', '', file_name.strip())
        
        cleaned_name = cleaned_name.replace(" ", "_") 
        
        return cleaned_name
    
        
        