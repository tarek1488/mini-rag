from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemes import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne
class ChunkDataModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        
    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id:str):
        record  = await self.collection.find_one({
            "_id" : ObjectId(chunk_id)
        })

        if not record or record is None:
            return None
        
        return DataChunk(**record)
    
    async def insert_chunks_batch(self, batch: list):
        operations = [
            InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
            for chunk in batch
        ]
        await self.collection.bulk_write(operations) 
    
    async def insert_many_batches(self, chunks:list, batch_size:int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            await self.insert_chunks_batch(batch=batch)
            
        return len(chunks)
    
    async def delete_chunks_py_project_id(self, project_id:ObjectId):
        response =await self.collection.delete_many({
            "chunk_project_id" : project_id
        })
        return response.deleted_count
        
        
    