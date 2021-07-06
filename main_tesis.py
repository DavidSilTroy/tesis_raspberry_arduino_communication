##import libraries
import time
import serial
import ast
from tesis_firestore import DB_sensors
from data_analitics import KnwingTheError
# from wincha_control import Wincha

##Global variables
print('Starting..')
t1 = 1.2 #time to wait in seconds
t2 = 1 #time to stop in seconds
data_sent=False #to not send all the time the same to the Arduino

"""Here the code start"""


if __name__ == '__main__':

    count = 1000000
    print('Hi! and welcome, this program is for a Thesis to measure presure sensors..')
    time.sleep(0.5)
    print("Lest's start!")
    time.sleep(0.2)
    print("Use your phone since now! :3")
    db_s= DB_sensors()
    kte=KnwingTheError()

    docs=""
    while docs=="":
        docs=f'{db_s.doc_status.get().to_dict()}'
        time.sleep(0.1)    

    docs_dic = ast.literal_eval(docs)
    current_collection = docs_dic["collection_is"]
    db_s.collection_to_add_data(current_collection)


    with serial.Serial('/dev/ttyACM0', 9600, timeout=5) as arduinoMega:
        time.sleep(0.1) #waiting for serial to open
        if arduinoMega.isOpen():
            print(f'{arduinoMega.port} connected!, Arduino is working!')
            try:
                
                cmd=docs_dic["current"]
                
                answer = ""

                while True:
                    

                    if cmd == "play":
                        """Sending message to Arduino"""
                        if data_sent != True:
                            arduinoMega.write(cmd.encode())
                            print(f' The current state is {cmd}')
                            data_sent= True
                        """Waiting for the answerd"""
                        while arduinoMega.inWaiting()==0: pass

                        """Getting the answer and cleaning it"""
                        if arduinoMega.inWaiting()>0:
                            count+=1
                            answer=str(arduinoMega.readline())
                            #print(answer)
                            answer = answer.replace("'","")
                            answer = answer.replace("\\r\\n","")
                            answer = answer.replace("b","")
                            arduinoMega.flushInput() #remove data after reading
                            print(answer)
                    
                    elif cmd == "stop":
                        """Sending message to Arduino"""
                        if data_sent != True:
                            arduinoMega.write(cmd.encode())
                            print(f' The current state is {cmd}')
                            data_sent=True
                    
                    elif cmd == "reset":
                        """Sending message to Arduino"""
                        if data_sent != True:
                            arduinoMega.write(cmd.encode())
                            print(f' The current state is {cmd}')
                            data_sent=True
                    else:
                        pass
                        
                    # time.sleep(0.2)


                    if answer != "":
                        """Saving the data in the database"""
                        #db_s.add_data(f'measure_{count}',answer)
                        """Analazing the data and printing result"""
                        #here the new class
                        #print(kte.adding_value(answer))
                    
                    docs=f'{db_s.doc_status.get().to_dict()}' #asking for db data
                    docs_dic = ast.literal_eval(docs)
                    new_state = docs_dic["current"]

                    if new_state!=cmd:
                        cmd = new_state
                        data_sent=False

            except KeyboardInterrupt:
                cmd="stop"
                arduinoMega.write(cmd.encode())
                print("KeyboardInterrupt has been caught.")
                print('Closing the program')
