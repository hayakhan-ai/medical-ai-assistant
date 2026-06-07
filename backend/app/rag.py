from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import json
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient(":memory:")

COLLECTION_NAME = "medical_data"

try:
    client.get_collection(COLLECTION_NAME)
except:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../datasets/cleaned_dataset.json")

def load_data():
    if not os.path.exists(DATASET_PATH):
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    points = []

    for idx, item in enumerate(data):
        text = f"{item['treatment']} {item['speciality']}"
        embedding = model.encode(text).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload=item
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

load_data()

def search_medical_data(query):

    embedding = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=3
    )

    return [point.payload for point in results.points]