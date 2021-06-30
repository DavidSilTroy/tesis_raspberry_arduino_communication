##import libraries
import time
import serial
from tesis_firestore import DB_sensors
# from wincha_control import Wincha

##Global variables
print('Starting..')
t1 = 1.2 #time to wait in seconds
t2 = 1 #time to stop in seconds

value_current=1
value_last = 1
value_highest = 1

error_from_highest = 0
error_from_last = 0
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
#input_str= ser.readline()

"""Here the code start"""


if __name__ == '__main__':

    count = 1000000
    print('Hi! and welcome, this program is for a Thesis to measure presure sensors..')
    time.sleep(0.5)
    print("Lest's start!")
    time.sleep(0.2)
    collection_name=input("Collection name to firestore: ")
    db_s= DB_sensors(collection_name)



    # while False:
    #     wincha.down()
    #     time.sleep(t1)
    #     count+=1
    #     wincha.stop()
    #     time.sleep(t2)
    #     input_str = ser.readline().decode("utf-8").strip()
    #     db_s.add_data(f'measure_{count}',input_str)
    #     print(f'Agregando dato sensor: {input_str}' )
    #     time.sleep(t1*1.2)
    #     if count>=1000010:
    #         break

    with serial.Serial('/dev/ttyACM0', 9600, timeout=5) as arduinoMega:
        time.sleep(0.1) #waiting for serial to open
        if arduinoMega.isOpen():
            print(f'{arduinoMega.port} connected!, Arduino is working!')
            print('You can play, reset, stop')
            try:
                cmd=input("What to do: ")
                """Sending message to Arduino"""
                arduinoMega.write(cmd.encode())
                answer = ""
                
                while True:
                    """Waiting for the answerd"""
                    while arduinoMega.inWaiting()==0: pass
                    """Getting the answer"""
                    if arduinoMega.inWaiting()>0:
                        count+=1
                        answer=str(arduinoMega.readline())
                        answer = answer.replace("'","")
                        answer = answer.replace("\\r\\n","")
                        answer = answer.replace("bArduino send: ","")
                        # print(answer)
                        arduinoMega.flushInput() #remove data after reading

                    if answer == "reseted" or answer == "stoped":
                        print(answer)
                        print('You can play, reset, stop')
                        cmd=input("What to do: ")
                        """Sending message to Arduino"""
                        arduinoMega.write(cmd.encode())
                    elif answer != "":
                        db_s.add_data(f'measure_{count}',answer)
                        value_current = int(answer)
                        if value_current >= value_highest:
                            value_highest = value_current
                            error_from_highest = 0
                        else:
                            error_from_highest = 100 - (value_current*100/value_highest)
                        if value_current >= value_last:
                            error_from_last = 0
                        else:
                            error_from_last = 100 - (value_current*100/value_last)
                        print(f'Sensor values:')
                        print(f'highest->{value_highest} ; last->{value_last} ; current->{value_current} ')
                        print(f'error from highest->{error_from_highest}')
                        print(f'error from last->{error_from_last}')
                        value_last = value_current


            except KeyboardInterrupt:
                cmd="stop"
                arduinoMega.write(cmd.encode())
                print("KeyboardInterrupt has been caught.")
                print('Closing the program')
