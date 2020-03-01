#include <SimpleDHT.h>
#include <SoftwareSerial.h>

// for DHT11,
//      VCC: 5V or 3V
//      GND: GND
//      DATA: 16
#define RxNodePin 13
#define TxNodePin 15
#define pinDHT11 16

SimpleDHT11 dht11(pinDHT11);

// Setup UART Communication with
SoftwareSerial Sigfox = SoftwareSerial(RxNodePin, TxNodePin);

// 12 bytes message buffer
uint8_t sigfoxMsg[12];

void setup()
{
  Serial.begin(115200);
  pinMode(RxNodePin, INPUT);
  pinMode(TxNodePin, OUTPUT);
  Sigfox.begin(9600);
  delay(100);

  //Serial.print("Device ID: " + getID());
  //Serial.print("Device PAC Number: " + getPAC());
  //delay(100);
}

void loop()
{
  // start working...
  Serial.println("=================================");
  Serial.println("Sample DHT11...");

  // read the sensors.
  byte temperature = 0;
  byte humidity = 0;
  byte luminosite = analogRead(A0);
  luminosite = map(luminosite, 0, 255, 0, 100);

  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess)
  {
    Serial.print("Read DHT11 failed, err=");
    Serial.println(err);
    delay(1000);
    return;
  }

  Serial.print("Sample OK: ");
  Serial.print((int)temperature);
  Serial.print(" °C, ");
  Serial.print((int)humidity);
  Serial.println(" %");

  // prepare the message
  sigfoxMsg[0] = (int)temperature;
  sigfoxMsg[1] = (int)humidity;
  sigfoxMsg[2] = (int)luminosite;

  // transmit the message
  sendMessage(sigfoxMsg, 3);

  // wait 10min
  delay(600000);
}

// Get device ID
String getID()
{
  String deviceId = "";
  char sigfoxBuffer;

  // Send AT$I=10 to WISOL to GET ID number
  Sigfox.print("AT$I=10\r");

  while (!Sigfox.available())
  {
    delay(10);
  }

  while (Sigfox.available())
  {
    sigfoxBuffer = Sigfox.read();
    deviceId += sigfoxBuffer;
    delay(10);
  }
  return deviceId;
}

// Get PAC number
String getPAC()
{
  String pacNumber = "";
  char sigfoxBuffer;

  // Send AT$I=11 to WISOL to GET PAC number
  Sigfox.print("AT$I=11\r");
  while (!Sigfox.available())
  {
    delay(10);
  }
  while (Sigfox.available())
  {
    sigfoxBuffer = Sigfox.read();
    pacNumber += sigfoxBuffer;
    delay(10);
  }
  return pacNumber;
}

String sendMessage(uint8_t sigfoxMsg[], int bufferSize)
{
  String status = "";
  char sigfoxBuffer;

  // Send AT$SF=xx to WISOL to send XX (payload data of size 1 to 12 bytes)
  Sigfox.print("AT$SF=");
  for (int i = 0; i < bufferSize; i++)
  {
    if (sigfoxMsg[i] < 0x10)
    {
      Sigfox.print("0");
    }
    Sigfox.print(String(sigfoxMsg[i], HEX));
  }

  Sigfox.print("\r");

  while (!Sigfox.available())
  {
    delay(10);
  }

  while (Sigfox.available())
  {
    sigfoxBuffer = (char)Sigfox.read();
    status += sigfoxBuffer;
    delay(10);
  }
  Serial.println("message envoyé !");

  return status;
}
