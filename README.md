# Rapport du projet IOT « Station Météo »

__1. Choix technologiques__

__Introduction__

Dans le cadre du projet d'IoT, nous avions à réaliser une station météo connectée, nous avons 
choisi de réaliser notre station pour l'agriculture. Notre station météorologique permet donc 
de renseigner des données spécifiques à l’environnement d’un champ de tomate (plante qui a besoin 
de beacoup de soleil, d'eau et de lumière) tel que l’humidité du sol, la luminosité ou encore la 
température extérieure. Cela permettra aux professionnels de l’agro-alimentaire d’améliorer leur 
rendement, gagner du temps et donc de la productivité.

Notre technologie d’IoT (Internet Of Things) doit être capable de récolter des informations
sur son environnement à l'aide de ses capteurs et les transmettre de manière autonome et sans
fil pour pouvoir être traité et afficher. Pour cela, des choix appropriés de technologies sont 
nécessaires en fonction du système que l’on souhaite concevoir.

Dans notre cas, nous avons opté pour un module Sigfox pour faire la liaison entre les capteurs et 
le serveur. En effet, les messages Sigfox sont limités en taille (12 bytes au maximum) toutes les 
10 minutes et en nombre (140 par jour), ce qui est amplement suffisant pour des relevés de température 
et d'humidité. De plus, cela permet d'être plus efficace que le WiFi dans les zones de campagnes les 
plus reculé.

__Schéma de la solution__

![alt text][schema_sol]

[schema_sol]: https://github.com/sadek-maghzili/IoT/blob/master/Image/Schema%20solution.png "Schéma de la solution"

__Schéma électronique__

![alt text][schema_elec]

[schema_elec]: https://github.com/sadek-maghzili/IoT/blob/master/Image/Sch%C3%A9ma%20%C3%A9lectronique.png "Schéma électronique"

__2. How to...__

Après avoir récupérer le l'Id du module sigfox pour configurer le callback et avoir fait tous les branchements électriques
comme indiqué plus haut, il faut :

uploader le code suivant dans la carte Node MCU à l'aide du logiciel arduino :
```C
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
```
Ce code enverra la température, l'humidité et la luminosité toutes les 10 minutes par l'intermédiare de Sigfox.
Il faut à présent récupérer ces données sur un serveur, pour cela on utilisera ngrok. Après avoir télécharger ngrok,
on lance la commande suivante dans un terminal : ./ngrok http 5000 -region eu
Cela permettra de créer un serveur local pour récupérer les données, il suffira de configurer le
_callback_ de sigfox directement sur leur site à l'adresse : https://backend.sigfox.com/devicetype/list
en choisissant le bon module grâce à son ID : 

![alt text][callback]

[callback]: https://github.com/sadek-maghzili/IoT/blob/master/Image/callback.png "callback"

On copie l'adresse donné par ngrok. Nous allons ensuite dans le dossier Flask pour lancer le serveur qui héberge
notre "site" grâce à la commande suivante : python Server.py et en s'assurant que les dossiers templates et static 
sont bien présents.

Pour visualiser les données, il reste à ouvrir le navigateur internet et aller à l'adresse http://localhost:5000/IoT
Nous obtenons comme résultat :

![alt text][résultat]

[résultat]: https://github.com/sadek-maghzili/IoT/blob/master/Image/Result.png "résultat"


__3. Usages potentiels__

Cette technologie à de nombreux usages potentiels, à grande échelle comme à petite échelle. Tout 
d’abord à __grande échelle__ : 
Les agriculteurs de demain aurons accès un flux de donnée régulier sur l’état de leur produit en 
temps réel. L’étude des sols leur permettrons d’anticiper une mauvaise croissance ou quelconque 
anomalie et de vite réagir face à une situation de façon très localisé. De ce fait, non seulement 
ce contrôle réduit les pertes et par conséquent le gâchis mais permet de fructifier considérablement 
sa production.

A présent à __petite échelle__ :
Dans une société visant à manger mieux avec des produits de meilleure qualité, être plus éco-responsable 
et moins dépendant des produits de grande surface dont la provenance et leur surproduction sont des problèmes. 
Notre système d’alertes permettrait à des personnes sans connaissances agricoles particulières de faire pousser 
leurs propres légumes simplement. En effet, nous avons pensé à mettre différentes alertes indiquant les besoins 
en eaux ou en compléments nutritifs à la terre en mesurant le tôt d’oxygène par exemple. 

Une société auto-suffisante, plus vert, limitant considérablement notre empreinte carbone.


