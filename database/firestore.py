import firebase_admin
from firebase_admin import firestore, credentials
from common.log import logger


# Sample document snapshot
# {
#     "associatedId": [
#         "xxxx"
#     ],
#     "birthday": "xxxx",
#     "gender": "male",
#     "name": "xxx",
#     "nickname0": {
#         "name": "xxx",
#         "priority": 100
#     },
#     "nickname1": {
#         "name": "",
#         "priority": 0
#     },
#     "nickname2": {
#         "name": "",
#         "priority": 0
#     }
# }

class Firestore:
    def __init__(self):
        cred = credentials.Certificate("./google-credential.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def query_by_associated_id(self, associated_id: str) -> firestore.firestore.DocumentSnapshot:
        try:
            docs = self.db.collection("user").where(
                filter=firestore.firestore.FieldFilter("associatedId", "array_contains", associated_id)).stream()

            results = []
            for doc in docs:
                results.append(doc)

            if len(results) == 1:
                doc = results[0]
                return doc
            else:
                return None
        except:
            logger.error(f"No information for associated id {associated_id}")
            return None
        
