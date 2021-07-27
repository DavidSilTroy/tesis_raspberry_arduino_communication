##import libraries
import time
from typing import Collection
import serial
import threading
import re  
from tesis_firestore import DB_sensors
from data_analitics import KnwingTheError

#Global variables
print('Starting..')
current_doc_name = ""
the_loops=0

#just a welcome message!
def welcome_here():
    print('Hi! and welcome, this program is for a Thesis to measure presure sensors..')
    time.sleep(0.5)
    print("Lest's start!")
    time.sleep(0.2)
    print("Use your phone since now! :3")

#here comes the fun part!
if __name__ == '__main__':

    #displaying messages from welcome
    welcome_here()

    #conectiong with database
    db_s= DB_sensors()

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

            while True:

                answer = ""

                try:
                    #getting data from data base
                    docs=db_s.doc_status.get()

                    #checking if the data exists
                    if docs.exists:
                        status_data = docs.to_dict()
                        doc_name = status_data[u'id_sensor']
                        current_action = status_data[u'action']
                        
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
                            if stop_count >= 90:
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
                            db_s.add_data(doc_name,answer)
                            the_loops+=1

                            """Analazing the data and printing result"""
                            print(kte.adding_value(answer))
                            print("----------------------------------------------------------\n")
                            if(kte.error_from_highest>50 or the_loops>=500):
                                db_s.add_new_action("stop")
                                print("Machine stop!")
                                print(f'error is {kte.error_from_highest} and loops in {the_loops}\n\n\n')
                                the_loops=0
                                time.sleep(2)
                        elif re.compile("[A-Za-z]+").match(answer) is not None:
                            # print(f'tenemos palabraus: {answer}')
                            pass
                        else:
                            #nothing here yet
                            pass
                    else:
                        print("can't conect to firestore..")
                        print("What do you want to do?")
                        print("[1] try again \n [2] Continiu with sqlite only \n Or just Enter to close the program")
                        cmd = input('write the number:')
                        if(cmd=="1"):
                            pass
                        elif(cmd=="2"):
                            print("Using Sqlite only..")
                            print("kidding! hahah")
                            break
                        else:
                            cmd="stop"
                            arduinoMega.write(cmd.encode())
                            break

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

        #closing message
        print("Closing the program.. bye! :)")
