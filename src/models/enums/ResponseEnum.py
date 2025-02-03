from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "File uploaded successfully"
    FILE_IS_VALID = "File is valid"
    FILE_UPLOADED_FAIL = "File upload fail"