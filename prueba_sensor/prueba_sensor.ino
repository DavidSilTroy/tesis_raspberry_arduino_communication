//Global Variables
String msg;
String serial_msg;

bool led_waiting_on= true;

int up_signal=6;
int down_signal=7;
int led_waiting=8;
int led_working=9;

int process_op=0;
int ss_count = 0;

int value_last=0;
int value_current=1;
int value_highest=1;



void setup() {
  pinMode(up_signal,OUTPUT);    // output signal
  pinMode(down_signal,OUTPUT);  // output signal
  pinMode(led_waiting,OUTPUT);  // output signal
  pinMode(led_working,OUTPUT);  // output signal
    
  Serial.begin(9600); //to print the values
  
  msg = ""; 
  serial_msg = ""; 
}

void loop() {
  //Here start the program
  readSerialPort();
  if(msg != ""){
    digitalWrite(led_working,HIGH);

    if(msg =="play"){
      digitalWrite(led_waiting,LOW);
      switch (process_op)
      {
      case 0:
        go_up();
        delay(1500);
        all_stop();
        delay(1000);
        go_down();
        delay(1200);
        all_stop();
        sensor_check();
        waiting_signal(50);
        process_op+=1;
        break;
      default:
        waiting_signal(100);
        break;
      }
      
    }
    if(msg =="reset"){
        go_up();
        waiting_signal(300);
        waiting_signal(300);
        waiting_signal(300);
        waiting_signal(100);
        waiting_signal(500);
        all_stop();
        msg="stop";
      }
    if(msg =="stop"){
          all_stop();
          waiting_signal(500);
          waiting_signal(500);
        }
  }else{
    digitalWrite(led_working,LOW);
    waiting_signal(1000);
  }
}

void go_up(){
  digitalWrite(down_signal,LOW);
  digitalWrite(up_signal,HIGH);
  }
  
void go_down(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,HIGH);
  }
void all_stop(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,LOW);
  
  }
void sensor_check(){
  delay(800);
  if(analogRead(1)>1){
    value_current = analogRead(1);
    if(value_current>value_last){
       value_last= value_current;
       value_current=0;
       ss_count=0;
     }
     else{
       ss_count+=1;
     }
  }else{
    process_op =0;
  }

  if(ss_count>2){
    sendData(String(value_last));
    Serial.println("");
    value_current=0;
    value_last=0;
    process_op =0;
    digitalWrite(led_working,LOW);
    delay(500);
  }
}


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

void sendData(String msg_to_send){
  Serial.flush();
  Serial.print(msg_to_send);
}

void actionToDo(){
    if(msg != ""){
    if(msg == "takeData"){
      int sensor_value = analogRead(1);
      delay(10);
      while(sensor_value!=analogRead(1)){
        sensor_value = analogRead(1);
      }
      msg = String(sensor_value);
    }
  sendData(msg);
  }
}

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