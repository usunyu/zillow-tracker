import firebase_admin
from datetime import datetime
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


def save_new_listings_and_views_count(area: str, data: dict):
    today = datetime.today()
    collection_name = f"{area}-new_listings_and_views_count"
    date_str = today.strftime("%Y-%m-%d")
    data["date"] = date_str
    utc_time = datetime(today.year, today.month, today.day, 0, 0, 0)
    data["time"] = utc_time
    firestore.client().collection(collection_name).document(date_str).set(data)


def get_new_listings_and_views_count(area: str) -> list:
    collection_name = f"{area}-new_listings_and_views_count"
    collection_ref = firestore.client().collection(collection_name)
    collection_docs = collection_ref.order_by("time").get()
    collection_list = [doc.to_dict() for doc in collection_docs]
    return collection_list


""" TEST """
if __name__ == "__main__":
    # save_new_listings_and_views_count(
    #     "bay_area", {"new_listings_count": 27, "total_views_count": 31259}
    # )

    docs_list = get_new_listings_and_views_count("bay_area")
    for doc_data in docs_list:
        print(doc_data)
