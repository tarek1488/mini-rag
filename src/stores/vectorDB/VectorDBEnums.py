from enum import Enum

class VectorDBProviders(Enum):
    QDRANT = "QDRANT"
    PINECONE = "PINECONE"


class VectorDBMetricMethod(Enum):
    COSINE = "cosine"
    DOT = "dot"