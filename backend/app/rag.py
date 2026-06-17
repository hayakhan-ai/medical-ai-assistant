from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.mongodb_service import fetch_treatments, fetch_doctors, fetch_hospitals, fetch_laboratories, fetch_specialities, fetch_tests
import numpy as np
import os

# Embedding model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

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

    treatments = fetch_treatments()
    doctors = fetch_doctors()
    hospitals = fetch_hospitals()
    laboratories = fetch_laboratories()
    specialities = fetch_specialities()
    tests = fetch_tests()
    count = client.count(collection_name=COLLECTION_NAME).count

    if count > 0:
        print("Embeddings already exist.")
        return

    points = []
    idx = 0

    for treatment in treatments:

        text = f"""
Treatment: {treatment.get('subCategory','')}

Description:
{treatment.get('description','')}
"""

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"treatment",
                    "name":treatment.get("subCategory",""),
                    "description":treatment.get("description","")
                }
            )
        )

        idx += 1
    for doctor in doctors:
        text = f"""
        Doctor: {doctor.get('name','')}

        Specialities:
            {', '.join(doctor.get('speciality', []))}

        Qualifications:
            {doctor.get('qualifications','')}

        Experience:
            {doctor.get('clinicExperience','')} years

        About:
            {doctor.get('about','')}
    """

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"doctor",
                    "name":doctor.get("name",""),
                    "speciality":doctor.get("speciality",[]),
                    "city":doctor.get("location",{}).get("city","")
                }
            )
        )

        idx += 1

    for hospital in hospitals:

        text = f"""
Hospital:
{hospital.get('name','')}

City:
{hospital.get('location',{}).get('city','')}

Address:
{hospital.get('location',{}).get('address','')}

Emergency Number:
{hospital.get('emergencyNo','')}
"""

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"hospital",
                    "name":hospital.get("name",""),
                    "city":hospital.get("location",{}).get("city","")
                }
            )
        )

        idx += 1  
    for lab in laboratories:

        text = f"""
Laboratory:
{lab.get('name','')}

Description:
{lab.get('description','')}

City:
{lab.get('location',{}).get('city','')}
"""

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"laboratory",
                    "name":lab.get("name",""),
                    "city":lab.get("location",{}).get("city","")
                }
            )
        )

        idx += 1 
    for speciality in specialities:

        text = f"""
Medical Speciality:
{speciality.get('specialityTitle','')}
"""

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"speciality",
                    "name":speciality.get("specialityTitle","")
                }
            )
        )

        idx += 1  
    for test in tests:

        text = f"""
Medical Test:
{test.get('name','')}

Category:
{test.get('categoryName','')}

Description:
{test.get('testDescription','')}

Duration:
{test.get('duration','')}

Price:
{test.get('price','')} PKR
"""

        embedding = np.array(model.encode(text)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type": "test",
                    "name": test.get("name", ""),
                    "category": test.get("categoryName", ""),
                    "description": test.get("testDescription", ""),
                    "duration": test.get("duration", ""),
                    "price": test.get("price", ""),
                    "code": test.get("testCode", "")
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
    query_embedding = np.array(model.encode(query)).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
     )

    print("\nQUERY:", query)
    print("RESULTS:")

    for point in results.points:
       print("Score:", point.score)
       print(point.payload)

    payloads = [point.payload for point in results.points]

    return payloads

print(client.count(collection_name=COLLECTION_NAME).count)