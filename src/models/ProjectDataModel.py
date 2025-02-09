from .BaseDataModel import BaseDataModel
from .db_schemes import Project 
from .enums.DataBaseEnum import DataBaseEnum

class ProjectDataModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
    @classmethod
    async def initialize_project_model(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection_with_index()
        return instance
        
    
    async def init_collection_with_index(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )
        
    
    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        return project
    
    async def get_or_create_project(self, project_id: str):
        record = await self.collection.find_one({
            "project_id" : project_id
        })
        
        if not record or record is None:
            project = Project(project_id=project_id)
            project =  await self.create_project(project=project)
            return project
        
        return Project(**record)
    
    async def get_all_projects(self, page_num:int = 1, page_size:int = 10):
        #total number of documents in the project colllection 
        total_documents = await self.collection.count_documents({})
        
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages = total_pages + 1
        
        #mongodb motor return a curson for the retrieved documents in the collection
        cursor = self.collection.find().skip((page_num - 1)*page_size).limit(page_size)
        
        projects = []
        
        async for document in cursor:
            projects.append(Project(**document))
        
        return total_pages, projects
        
        
        
        