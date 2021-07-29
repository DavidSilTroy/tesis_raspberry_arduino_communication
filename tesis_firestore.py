import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time

cred = credentials.Certificate("../tesis_davidsiltroy.json")
firebase_admin.initialize_app(cred)


#db.collection("persons").add({"name":"JHon","age":26})

class DB_sensors_fs:
    db = firestore.client()
    db_collection=db.collection("main_data")
    doc_status = db_collection.document("status_data")
    
    def __init__(self):
        pass

    def add_data(self,db_document,db_data):
        current_date = int(time.time())
        self.db_collection.document(str(db_document)).update({
            f'v{current_date}' : str(db_data)
            })
    def add_data_with_id(self,db_document,id ,db_data):
        self.db_collection.document(str(db_document)).update({
            f'v{id}' : str(db_data)
            })
    def add_data_with_dict(self,db_document,db_data):
        self.db_collection.document(str(db_document)).update({
            db_data
            })
    
    def add_new_action(self, action):
        self.doc_status.update({
            u'action': str(action)
            })
        

    
        
