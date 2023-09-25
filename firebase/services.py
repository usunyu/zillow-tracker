import firebase_admin
from datetime import datetime
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


def save_new_listing_and_views_count(area: str, data: dict):
    collection_name = f"{area}-new_listing_and_views_count"
    date_str = datetime.today().strftime("%Y-%m-%d")
    data["date"] = date_str
    firestore.client().collection(collection_name).document(date_str).set(data)


def get_new_listing_and_views_count(area: str) -> list:
    collection_name = f"{area}-new_listing_and_views_count"
    collection_ref = firestore.client().collection(collection_name)
    collection_docs = collection_ref.get()
    collection_list = [doc.to_dict() for doc in collection_docs]
    return collection_list


""" TEST """
if __name__ == "__main__":
    save_new_listing_and_views_count(
        "bay_area", {"new_listing_count": 27, "total_views_count": 31259}
    )

    docs = get_new_listing_and_views_count("bay_area")
    for doc in docs:
        print(doc)
