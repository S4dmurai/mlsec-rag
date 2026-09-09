import os
import collections
import chunker
import embedder
import loader
import parser
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=qdrant_url)


def new_collection(name="documents", size=384):
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(
            size=size,
            distance=Distance.COSINE
        )
    )


def implement_documents(directory: str):

    documents = loader.load_all_pdfs(directory)

    points = []
    point_id = 0

    for name, doc in documents:

        parsed_doc = parser.pars_doc(doc)

        chunks = chunker.chunk_doc(parsed_doc)

        embedded_docs = embedder.embed_chunks(chunks)

        for text, embedding, page_nr in embedded_docs:

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload={
                        "text": text,
                        "page": page_nr,
                        "document": name
                    }
                )
            )

            point_id += 1

    client.upsert(
        collection_name="documents",
        points=points
    )

def search_documents(query_vector: list, limit: int):
    search_results = client.query_points(
        collection_name="documents",
        query=query_vector,
        limit=limit
        )
    return search_results.points