##import libraries
import time
from typing import Collection
import serial
import threading
import re  
from tesis_firestore import DB_sensors
from data_analitics import KnwingTheError
# from wincha_control import Wincha

##Global variables
print('Starting..')
t1 = 1.2 #time to wait in seconds
t2 = 1 #time to stop in seconds
data_sent=False #to not send all the time the same to the Arduino

"""Here the code start"""

def read_db_status():
    docs=db_s.doc_status.get()
    while docs.exists == False: pass
    return docs.to_dict()



if __name__ == '__main__':

    count = 1000000
    print('Hi! and welcome, this program is for a Thesis to measure presure sensors..')
    time.sleep(0.5)
    print("Lest's start!")
    time.sleep(0.2)
    print("Use your phone since now! :3")
    db_s= DB_sensors()
    kte=KnwingTheError()

    with serial.Serial('/dev/ttyACM0', 9600, timeout=5) as arduinoMega:
        time.sleep(0.2) #waiting for serial to open
        if arduinoMega.isOpen():
            print(f'{arduinoMega.port} connected!, Arduino is working!')
            try:
                last_action=""
                while True:
                    
                    answer = ""
                    
                    status_data = read_db_status()
                    collection_name = status_data[u'collection_is']
                    current_action = status_data[u'current']

                    #print(f'{collection_name} y la action es {current_action}') #getting the current collection
                    
                    if last_action != current_action:
                        last_action=current_action
                        if current_action == "new":
                            count = 1000000
                            current_action="stop"

                        """Sending message to Arduino"""
                        arduinoMega.write(current_action.encode())
                        print(f'The action is: {current_action}') #getting the current collection
                    
                    if arduinoMega.inWaiting()>0:
                            count+=1
                            answer=str(arduinoMega.readline())
                            answer= re.search("[^(')][A-Za-z0-9 ]+",answer).group() #To take only the data we need
                            print(f'The answer is: {answer}')
                            arduinoMega.flushInput() #remove data after reading

                    if re.compile("[0-9]+").match(answer) is not None:
                        print(f'tenemos numerous: {answer}')
                        """Saving the data in the database"""
                        db_s.add_data(f'measure_{count}',answer)
                        """Analazing the data and printing result"""
                        print(kte.adding_value(answer))

                    elif re.compile("[A-Za-z]+").match(answer) is not None:
                        print(f'tenemos palabraus: {answer}')

                    else:
                        #nothing here
                        pass

                    
                    time.sleep(1)

            except KeyboardInterrupt:
                cmd="stop"
                arduinoMega.write(cmd.encode())
                print("KeyboardInterrupt has been caught.")
                print('Closing the program')
