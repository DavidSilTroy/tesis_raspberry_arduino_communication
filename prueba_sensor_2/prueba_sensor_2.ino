//Global Variables
String msg = "";
String serial_msg = "";

bool led_waiting_on= true;

int up_signal     =6;
int down_signal   =7;

int led_waiting   =8;
int led_working   =9;

int process_op    =0;
int ss_count      =0;

long value_sensor  =0;
int count_value   =0;


int timeToUp      =1000;             //time in ms
int timeToDown    =900;             //time in ms
int timeToReadS   =10;              //time in ms
int theReads      =600/timeToReadS; //The number of repetitions in 600 ms


void setup() {
  pinMode(up_signal,OUTPUT);    // output signal
  pinMode(down_signal,OUTPUT);  // output signal
  pinMode(led_waiting,OUTPUT);  // output signal
  pinMode(led_working,OUTPUT);  // output signal
    
  Serial.begin(9600); //to print the values
  
}

void loop() {
  //Here start the program
  readSerialPort();
  if(msg != ""){
    if(msg =="play"){
      digitalWrite(led_working,HIGH);
      go_up();
      go_down();
      value_sensor=0;
      count_value=0;
      delay(10);
      for(int i=0; i<=theReads; i++){
          value_sensor=value_sensor+analogRead(1);
          count_value++;
      }
      value_sensor=value_sensor/count_value;
      sendData(String(value_sensor));
    }
    if(msg =="stop"){
      go_up();
      msg="stop1";
      waiting_signal(300);
    }
    if(msg =="stop1"){
      all_stop();
      waiting_signal(500);
    }
  }
  else{
    //no msg.. so what to do?
    digitalWrite(led_working,LOW);
    waiting_signal(1000);
  }
}

void all_stop(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,LOW);
  delay(100);
  }
void go_up(){
  digitalWrite(down_signal,LOW);
  digitalWrite(up_signal,HIGH);
  delay(timeToUp);
  all_stop();
  }
void go_down(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,HIGH);
  delay(timeToDown);
  all_stop();
  }

// Reading data from the serial port and writing it in the msg
void readSerialPort(){
  serial_msg="";
  if(Serial.available()){
    delay(10);
    while(Serial.available()>0){
      serial_msg += (char)Serial.read();
    }
   Serial.flush();
   if(serial_msg.length()>1){
    msg=serial_msg;
   }
  }
}
//Send the data is just print it
void sendData(String msg_to_send){
  Serial.println(msg_to_send);
}
//led to say is waiting 
void waiting_signal(int time_to_stay){
  if (led_waiting_on){
    digitalWrite(led_waiting,HIGH);
    led_waiting_on=false;
  }else{
    digitalWrite(led_waiting,LOW);
    led_waiting_on=true;
  }
  delay(time_to_stay);
  
}