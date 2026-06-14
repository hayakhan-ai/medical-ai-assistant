from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.mongodb_service import fetch_treatments
import os

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent Qdrant storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

QDRANT_PATH = os.path.join(BASE_DIR, "..", "qdrant_db")

print("Qdrant path:", QDRANT_PATH)

client = QdrantClient(path=QDRANT_PATH)

COLLECTION_NAME = "medical_data"


# Create collection if it doesn't exist
try:
    client.get_collection(COLLECTION_NAME)

except Exception:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


def load_data():

    data = fetch_treatments()
    print("Categories:", len(data))

    if not data:
        print("No treatments found in MongoDB.")
        return

    count = client.count(collection_name=COLLECTION_NAME).count

    if count > 0:
        print("Embeddings already exist.")
        return

    points = []
    idx = 0

    for category in data:

        category_name = category.get("categoryName", "")

        for treatment in category.get("treatments", []):

            text = f"""
Category: {category_name}

Treatment: {treatment.get('subCategory', '')}

Description:
{treatment.get('description', '')}
"""

            embedding = model.encode(text).tolist()

            points.append(
                PointStruct(
                    id=idx,
                    vector=embedding,
                    payload={
                        "category": category_name,
                        "treatment": treatment.get("subCategory", ""),
                        "description": treatment.get("description", "")
                    }
                )
            )

            idx += 1

    print("Total points:", len(points))        

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(
    "Count after upsert:",
    client.count(collection_name=COLLECTION_NAME).count
)



def search_medical_data(query, limit=5):
    query_embedding = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
     )

    payloads = [p.payload for p in results.points]

    print("\nQUERY:", query)
    print("RESULTS:")
    for p in payloads:
        print(p)

    return payloads

print(client.count(collection_name=COLLECTION_NAME).count)