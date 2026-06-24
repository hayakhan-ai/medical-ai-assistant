from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.mongodb_service import fetch_treatments, fetch_doctors, fetch_hospitals, fetch_laboratories, fetch_specialities, fetch_tests
import numpy as np
import os

os.environ["HF_HOME"] = "D:/huggingface_cache"
# Embedding model
model = SentenceTransformer("BAAI/bge-m3")

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
            size=1024,
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
Treatment: 
{treatment.get('subCategory','')}

Description:
{treatment.get('description','')}
"""

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

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

        City:
            {doctor.get('location',{}).get('city','')}

        Address:
            {doctor.get('location',{}).get('address','')}  

        Phone:
            {doctor.get('phoneNumber','')}

        Email:
            {doctor.get('email','')}            

        Country:
            {doctor.get('country','')}            

        About:
            {doctor.get('about','')[:500]}
    """

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"doctor",
                    "name":doctor.get("name",""),
                    "speciality":doctor.get("speciality",[]),
                    "qualifications":doctor.get("qualifications",""),
                    "experience":doctor.get("clinicExperience",""),
                    "about":doctor.get("about",""),
                    "phone":doctor.get("phoneNumber",""),
                    "email":doctor.get("email",""),
                    "address": doctor.get("location",{}).get("address",""),
                    "city":doctor.get("location",{}).get("city",""),
                    "country":doctor.get("country","")
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

Phone:
{hospital.get('phoneNumber','')}

Emergency Number:
{hospital.get('emergencyNo','')}

Email:
{hospital.get('email','')}

Open Time:
{hospital.get('openTime','')}

Country:
{hospital.get('country','')}
"""

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"hospital",
                    "name":hospital.get("name",""),
                    "city":hospital.get("location",{}).get("city",""),
                    "address":hospital.get("location",{}).get("address",""),
                    "phone":hospital.get("phoneNumber",""),
                    "open time":hospital.get("openTime",""),
                    "emergencyNo":hospital.get("emergencyNo",""),
                    "email":hospital.get("email",""),
                    "country":hospital.get("country","")
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

Address:
{lab.get('location',{}).get('address','')}

Phone:
{lab.get('phoneNumber','')}

Emergency Number:
{lab.get('emergencyNo','')}

Email:
{lab.get('email','')}

Open Time:
{lab.get('openTime','')}

"""

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type":"laboratory",
                    "name":lab.get("name",""),
                    "description":lab.get("description",""),
                    "city":lab.get("location",{}).get("city",""),
                    "address":lab.get("location",{}).get("address",""),
                    "phone":lab.get("phoneNumber",""),
                    "emergencyNo":lab.get("emergencyNo",""),
                    "email":lab.get("email",""),
                    "open time":lab.get("openTime","")
                }
            )
        )

        idx += 1 
    for speciality in specialities:

        text = f"""
Medical Speciality:
{speciality.get('specialityTitle','')}
"""

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

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
        Medical Test

Description:
{test.get('testDescription','')}

Duration:
{test.get('duration','')}

Discount:
{test.get('discount','')} %

"""

        embedding = np.array(model.encode(text, normalize_embeddings=True)).tolist()

        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "type": "test",
                    "description": test.get("testDescription", ""),
                    "duration": test.get("duration", ""),
                    "discount":test.get("discount","")
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


def search_medical_data(query, limit=20):
    query_embedding = np.array(model.encode(query, normalize_embeddings=True)).tolist()

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