
import sqlite3
import time
import datetime



class DB_sensors_sql:
    con = sqlite3.connect("TesisDavidSilTroy.db")
    cur = con.cursor()
    table_name = "No_named"

    main_table_name = "sensors_tests"
    main_table_date_title = f'id INTEGER PRIMARY KEY, test_name text, date text'

    def __init__(self):
         self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS {self.main_table_name} ({self.main_table_date_title})'
            )

    def create_table(self,table_name):
        self.table_name=table_name
        current_id = int(time.time())
        current_date = datetime.datetime.now()
        table_date_title = f'id INTEGER PRIMARY KEY, value real, date text'

        self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS {self.table_name} ({table_date_title})'
            )

        data_to_main_table =(current_id, 
            self.table_name, 
            current_date)

        table_already_exists= False
        dta= self.get_data_from_column(self.main_table_name,"test_name")

        for dto in dta:
            if(dto[0]==str(self.table_name)):
                table_already_exists=True

        if table_already_exists:
            pass
        else:
            self.add_data_to_table(self.main_table_name, data_to_main_table)

    def add_data_to_table(self, table_name, data):
        #cur.executemany("insert into lang values (?, ?)", lang_list)
        self.cur.execute(f'INSERT INTO {table_name} VALUES (?,?,?)',data)
        self.con.commit()

    def add_data(self,data):
        current_id = int(time.time())
        current_date = datetime.datetime.now()
        data_to_add = (current_id,data,str(current_date))
        self.cur.execute(f'INSERT INTO {self.table_name} VALUES (?,?,?)',data_to_add)
        self.con.commit()

    def get_data_from_column(self,table_name,column_name):
        dta= self.cur.execute(f'SELECT {column_name} FROM {table_name}')
        return dta.fetchall()
        
db = DB_sensors_sql()
"""db.create_table("test_400")
print("ok")
db.add_data("500")
time.sleep(1)
db.add_data("550") """
#print(db.get_data_from_column("sensors_tests","*"))
print(db.get_data_from_column("new_400_1hr","*"))
    
       