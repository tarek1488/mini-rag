from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "File uploaded successfully"
    FILE_IS_VALID = "File is valid"
    FILE_UPLOADED_FAIL = "File upload fail"
    FILE_PROCESSING_FALIED = "File processing failed"
    FILE_PROCESSING_SUCCEED = "File processing succeed"
    CHUNKS_DELETE_SUCCEED = "Chunks delete succeed"
    PROJECT_IS_EMPYT = "There is no files tp process in this project"
    FILE_NOT_FOUND = "File not found in this project with this file id"
    PROJECT_NOT_FOUND = "Project not found in mongo DB"
    DATA_INSERTION_IN_VECTORDB_ERROR = "Error while inserting data to vector db"
    DATA_INSERTION_IN_VECTORDB_SUCCEED= "Data inserted successfully in vector db"
    RETRIEVING_COLLECTION_INFO_VECTORDB_ERROR= "Error while retrieving collection info from vector db"
    RETRIEVING_COLLECTION_INFO_VECTORDB_SUCCEED= "retrieving collection info from vector db succeed"
    SEARCH_BY_VECTOR_ERROR = "Error while searching by vector"
    SEARCH_BY_VECTOR_SUCCEED = "searching by vector succeed"
    