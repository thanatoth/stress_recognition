// 1秒ごとにカウントアップしたデータをSoracom Harvestに送信し、送受信内容をシリアルモニタにプリントします
// Soracom管理画面、 「Sim 管理」 -> Sim選択 ->「SORACOM Harvest 設定」より設定後
// Soracom管理画面、 「Sim 管理」 -> Sim選択 -> 「操作」-> 「データを確認」より送信データを確認することができます
#include <WioCellLibforArduino.h>

#define INTERVAL 50
//#define INTERVAL 0
#define RECEIVE_TIMEOUT 10000

#define LIGHT WIO_A4
#define PIN WIO_D38

#define MEASUREMENT 10
#define MEASUREMENT_PLUS_ONE 11

WioCellular Wio;

//heart rate sensor用変数================================================================
unsigned char counter = 0;
unsigned int heart_rate = 80;
unsigned long temp[MEASUREMENT_PLUS_ONE];
unsigned long sub = 0;
volatile unsigned char state = LOW;
bool data_effect = true;
const int max_heartpluse_duty = 20000;
//END heart rate senser用変数============================================================

//setup===============================================================================
void setup() {

  //Serial print設定
  SerialUSB.begin(115200);
  SerialUSB.println("");
  SerialUSB.println("--- START ---");

  SerialUSB.println("--- I/O Initialize. ---");
  Wio.Init();

  SerialUSB.println("--- Power supply ON. ---");
  Wio.PowerSupplyCellular(true);
  delay(500);

  Wio.PowerSupplyGrove(true);
  delay(500);

  pinMode(LIGHT, INPUT_ANALOG);

  SerialUSB.println("--- Turn on or reset. ---");
  if (!Wio.TurnOnOrReset()) {
    SerialUSB.println("### ERROR!5435 ###");
    return;
  }

  SerialUSB.println("--- Connecting to \"soracom.io\". ---");
#ifdef ARDUINO_WIO_LTE_M1NB1_BG96
  Wio.SetSelectNetwork(WioCellular::SELECT_NETWORK_MODE_MANUAL_IMSI);
  Wio.SetAccessTechnology(WioCellular::ACCESS_TECHNOLOGY_LTE_M1);
#endif
  if (!Wio.Activate("soracom.io", "sora", "sora")) {
    SerialUSB.println("### ERROR!4575 ###");
    return;
  }

  array_init();
  attachInterrupt(PIN, interrupt, RISING);

  //SerialUSB.println("--- Setup completed. ---");
}
//END setup==============================================================================


//loop ==================================================================================
void loop() {
  char data[100];

  //light senser取得===================================
  unsigned int sensorValue = analogRead(LIGHT);
  //SerialUSB.println(sensorValue);
  //===================================================

  //heart rate 取得=====================================
  digitalWrite(PIN, state);
  //===================================================

  // create payload
  sprintf(data, "{\"lightSener\": %d, \"heartRate\": %d}", sensorValue, heart_rate);

  //SerialUSB.println("--- Open socket. ---");

  // Open harvest connection
  int connectId;
  connectId = Wio.SocketOpen("harvest.soracom.io", 8514, WIO_UDP);
  if (connectId < 0) {
    SerialUSB.println("### ERROR!1 ###");
    //goto err;
  }

  // Send data.
  //SerialUSB.println("--- Send data. ---");
  //SerialUSB.print("Send:");
  //SerialUSB.println(data);
  if (!Wio.SocketSend(connectId, data)) {
    SerialUSB.println("### ERROR!2 ###");
    goto err_close;
  }

  
    // Receive data.
    //SerialUSB.println("-- Receive data. ---");
    int length;
    length = Wio.SocketReceive(connectId, data, sizeof (data), RECEIVE_TIMEOUT);
    if (length < 0) {
    SerialUSB.println("### ERROR! ###");
    goto err_close;
    }

    if (length == 0) {
    SerialUSB.println("### RECEIVE TIMEOUT! ###");
    goto err_close;
    }


    //SerialUSB.print("Receive:");
    //SerialUSB.print(data);
    //SerialUSB.println("");
  
err_close:
  //SerialUSB.println("### Close.");
  if (!Wio.SocketClose(connectId)) {
    SerialUSB.println("### ERROR!3 ###");
    goto err;
  }

err:
  delay(INTERVAL);
  //counter++;
}

//END loop============================================================================

void sum()//calculate the heart rate
{
  if (data_effect)
  {
    heart_rate = MEASUREMENT * 60000 / (temp[MEASUREMENT] - temp[0]); //60*20*1000/20_total_time
    if(heart_rate > 150 || heart_rate < 30){
      heart_rate = 85;
    }
    //SerialUSB.print("Heart_rate_is:\t");
    //SerialUSB.println(heart_rate);
  }
  data_effect = 1; //sign bit
}
void interrupt()
{
  temp[counter] = millis(); //get sys time
  state = !state;    //change LED status
  //SerialUSB.println(counter,DEC);
  //SerialUSB.println(temp[counter]);
  switch (counter)
  {
    case (0):
      sub = temp[counter] - temp[MEASUREMENT];
      SerialUSB.print("sub1:");
      SerialUSB.println(sub);
      break;
    default:
      sub = temp[counter] - temp[counter - 1];
      SerialUSB.print("sub2:");
      SerialUSB.println(sub);
      break;
  }
  if (sub > max_heartpluse_duty) //set 2 seconds as max heart pluse duty
  {
    data_effect = 0; //sign bit
    counter = 0;
    SerialUSB.println("Heart rate measure error,test will restart!" );
    array_init();
  }
  if (counter == MEASUREMENT & data_effect)
  {
    counter = 0;
    sum();
  }
  else if (counter != MEASUREMENT && data_effect)
    counter++;
  else
  {
    counter = 0;
    data_effect = 1;
  }
}


void array_init()
{
  for (unsigned char i = 0; i != MEASUREMENT; ++i)
  {
    temp[i] = 0;
  }
  temp[MEASUREMENT] = millis();
}
