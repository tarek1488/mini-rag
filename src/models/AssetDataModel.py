from .db_schemes.asset import Asset
from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
class AssetDataModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def initialize_asset_model(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection_with_index()
        return instance
        
    async def init_collection_with_index(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )
                
    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset
    
    async def get_asset_by_project_id_file_name(self, asset_file_name: str, asset_project_id: str):
        record = await self.collection.find_one({
            "asset_name": asset_file_name,
            "asset_project_id": ObjectId(asset_project_id)
        })
        if not record or record is None:
            return None
        
        return Asset(**record)
    
    async def get_assets_by_project_id(self, project_id: str):
        cursor = await self.collection.find({
            "asset_project_id": ObjectId(project_id) if isinstance(project_id,str) else project_id
        })
        return list(cursor)