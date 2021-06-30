import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

cred = credentials.Certificate("../serviceAccount.json")
firebase_admin.initialize_app(cred)


#db.collection("persons").add({"name":"JHon","age":26})

class DB_sensors:
    db = firestore.client()
    db_collection="sensor_testing"

    def __init__(self,db_collection):
        self.db_collection = db_collection
        
    def add_data(self,db_document,db_data):
        current_date = datetime.datetime.now()
        self.db.collection(self.db_collection).document(db_document).set({"value":str(db_data),"date":str(current_date)})
        
