import RPi.GPIO as GPIO

class Wincha:
    signal_1=11
    signal_2=13
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.signal_1, GPIO.OUT)
        GPIO.setup(self.signal_2, GPIO.OUT)

    def up(self):
        GPIO.output(self.signal_1,GPIO.LOW)
        GPIO.output(self.signal_2,GPIO.HIGH)
    def down(self):
        GPIO.output(self.signal_2,GPIO.LOW)
        GPIO.output(self.signal_1,GPIO.HIGH)
    def stop(self):
        GPIO.output(self.signal_2,GPIO.LOW)
        GPIO.output(self.signal_1,GPIO.LOW)
    def end(self):
        GPIO.cleanup()
