//Global Variables
String msg = "";
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
    if(msg =="play"){
      digitalWrite(led_working,HIGH);
      if (process_op==0){
        go_up();
        go_down();
      }
      sensor_check();
      waiting_signal(100);
    }
    if(msg =="stop"){
      go_up();
      msg="stop1";
      waiting_signal(400);
      waiting_signal(400);
      waiting_signal(200);
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
  delay(1500);
  all_stop();
  }
void go_down(){
  digitalWrite(up_signal,LOW);
  digitalWrite(down_signal,HIGH);
  delay(1200);
  all_stop();
  }

void work_now(){
  go_up();
  go_down();
}

void sensor_check(){
  delay(800);
  process_op=1;
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