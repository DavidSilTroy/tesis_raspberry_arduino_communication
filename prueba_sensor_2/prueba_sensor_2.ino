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

int value_sensor  =0;
int count_value   =0;



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
      delay(200);
      for(int i=0; i<=5; i++){
          value_sensor=value_sensor+analogRead(1);
          count_value++;
          delay(100);
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
  }else{
    //no msg.. so what to do?
    digitalWrite(led_working,LOW);
    waiting_signal(1000);
  }
}

void all_stop(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,LOW);
  }
void go_up(){
  digitalWrite(down_signal,LOW);
  digitalWrite(up_signal,HIGH);
  delay(1200);
  all_stop();
  }
void go_down(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,HIGH);
  delay(1000);
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