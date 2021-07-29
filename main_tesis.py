##import libraries
import time
from typing import Collection
import serial
import threading
import re  
from tesis_firestore import DB_sensors_fs
from tesis_sqlite import DB_sensors_sql
from data_analitics import KnwingTheError

#Global variables
print('Starting..')
current_action="stop"
current_doc_name = ""
the_loops=0
lets_work=False
doc_ready=False
docs={}
thread_working=True

#just a welcome message!
def welcome_here():
    print('Hi! and welcome, this program is for a Thesis to measure presure sensors..')
    time.sleep(0.5)
    print("Lest's start!")
    time.sleep(0.2)
    print("Use your phone since now! :3")

def check_firestore():
    #getting data from data base
    global docs
    global doc_ready
    global thread_working
    while thread_working:
        docs=db_fs.doc_status.get()
        if docs.exists:
            doc_ready = True
        #waiting to get the data
        time.sleep(3)

#here comes the fun part!
if __name__ == '__main__':
    #displaying messages from welcome
    welcome_here()
    #conectiong with database
    db_fs= DB_sensors_fs()
    db_sql = DB_sensors_sql()
    #to show the error in the datas
    kte=KnwingTheError()
    #working with the arduino
    with serial.Serial('/dev/ttyACM0', 9600, timeout=5) as arduinoMega:
        
        #waiting for serial to open
        time.sleep(0.2) 
        
        #checking if arduino is conected
        if arduinoMega.isOpen():
            print(f'{arduinoMega.port} connected!, Arduino is working!')
            
            last_action=""
            stop_count = 0
            thethread = threading.Thread(target=check_firestore,)
            thethread.start()
            time.sleep(2)

            while True:
                answer = ""
                try:
                    #checking if the data from firestore was gotten
                    if doc_ready:
                        status_data = docs.to_dict()
                        doc_name = status_data[u'id_sensor']
                        current_action = status_data[u'action']
                        lets_work=True
                    else:
                        print("can't conect to firestore..")
                        print("What do you want to do?")
                        print("[1] try again \n [2] Continiu with sqlite only \n Or just Enter to close the program")
                        cmd = input('write the number:')
                        if(cmd=="1"):
                            lets_work=False
                        elif(cmd=="2"):
                            print("Using Sqlite only..")
                            doc_name=input('what is the test name: ')
                            current_action = "play"
                            break
                        else:
                            cmd="stop"
                            arduinoMega.write(cmd.encode())
                            break
                    
                    if lets_work:
                        #setting the table name to sql
                        db_sql.create_table(doc_name)                    
                        #if the collection change!
                        if(doc_name != current_doc_name):
                            current_doc_name=doc_name
                        #if the action change!
                        if last_action != current_action:
                            last_action=current_action
                            """Sending message to Arduino"""
                            arduinoMega.write(current_action.encode())
                            print(f'The action is: {current_action}') #getting the current collection

                        #if program was stoped too much time
                        if current_action == "stop":
                            time.sleep(2)
                            stop_count+=1
                            if stop_count >= 100:
                                print("Program in stop too much time..")
                                break
                        
                        #if arduino is sending something
                        if arduinoMega.inWaiting()>0:
                                answer=str(arduinoMega.readline())
                                answer= re.search("[^(')][A-Za-z0-9 ]+",answer).group() #To take only the data we need
                                print("\n\nNew Data..")
                                print(f'The answer is: {answer} \n')
                                arduinoMega.flushInput() #remove data after reading            
                        #looking what is in the answer
                        if re.compile("[0-9]+").match(answer) is not None:
                            # print(f'tenemos numerous: {answer}')
                            """Saving the data in the database"""
                            print(f'database doc name is: {doc_name}')
                            print(f'value is: {answer} \n')
                            #db_fs.add_data(doc_name,answer)
                            db_sql.add_data(answer)
                            the_loops+=1
                            print(f'the loop is: {the_loops} \n')

                            """Analazing the data and printing result"""
                            print(kte.adding_value(answer))
                            print("----------------------------------------------------------\n")
                            if(kte.error_from_highest>50 or the_loops>=1000):
                                db_fs.add_new_action("stop")
                                print("Machine stop!")
                                print(f'error is {kte.error_from_highest} and loops in {the_loops}\n\n\n')
                                the_loops=0
                                time.sleep(2)
                        elif re.compile("[A-Za-z]+").match(answer) is not None:
                            print(f'Arduino says: {answer}')
                        else:
                            #nothing here yet
                            pass
                    
                #when interrupt with ctrl + c
                except KeyboardInterrupt:
                    cmd="stop"
                    arduinoMega.write(cmd.encode())
                    print("KeyboardInterrupt has been caught.")
                    break
                #when Arduino lose conection
                except OSError:
                    print("Arduino disconected!")
                    break
        else:
            print("Arduino not detected!")

        wanting = input('wanting to save the data in farestore?[Y - N]')
        
        if wanting == "Y" or wanting == "Yes" or wanting == "yes" or wanting == "y":
            print("Uploading in firestore")
            #data_to_firestore={}
            data_from_sql = db_sql.get_data_from_column(doc_name,"*")
            for data in data_from_sql:
                #data_to_firestore[str(data[0])]=str(data[1])
                db_fs.add_data_with_id(doc_name,data[0],data[1])
            #db_fs.add_data_with_dict(doc_name,data_to_firestore)
            #print(data_to_firestore)
        else:
            print("Not uploading in firestore")
        thread_working=False
        #closing message
        print("Closing the program.. bye! :)")
