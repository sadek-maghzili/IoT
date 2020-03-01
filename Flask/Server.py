from flask import Flask, Markup, render_template, request, jsonify
from ast import literal_eval
import time
import requests
import json
import datetime

app = Flask(__name__)

heures = [
]

temperatures = [
]

humidites = [
]

luminosites = [

]

heure = 0


def formatHeure(h, heur):
    if h.tm_hour < 10:
        heur = time.strftime("0" + str(h.tm_hour) + ":" + str(h.tm_min))
    else:
        heur = time.strftime(str(h.tm_hour) + ":" + str(h.tm_min))

    if h.tm_min < 10:
        heur = time.strftime(str(h.tm_hour) + ":0" + str(h.tm_min))
    else:
        heur = time.strftime(str(h.tm_hour) + ":" + str(h.tm_min))
    return(heur)


def jours(jour):
    if(int(jour) == 1):
        jour = "Lundi"
    elif(int(jour) == 2):
        jour = "Mardi"
    elif(int(jour) == 3):
        jour = "Mercredi"
    elif(int(jour) == 4):
        jour = "Jeudi"
    elif(int(jour) == 5):
        jour = "Vendredi"
    elif(int(jour) == 6):
        jour = "Samedi"
    elif(int(jour) == 7):
        jour = "Dimanche"
    print(jour)
    return(jour)


@app.route("/", methods=['POST'])
def data():
    body = request.json
    if body == None:
        return("Not a json !")
    if 'data' in body.keys():
        data = str(body['data'])

        temperature = "0x" + data[0:2]
        temperature = literal_eval(temperature)
        temperatures.append(temperature)

        humidite = "0x" + data[2:4]
        humidite = literal_eval(humidite)
        humidites.append(humidite)

        luminosite = "0x" + data[4:6]
        luminosite = literal_eval(luminosite)
        luminosites.append(luminosite)

        heureCapteur = body['time']
        date = time.localtime(int(heureCapteur))
        heureCapteur = formatHeure(date, heureCapteur)
        heures.append(heureCapteur)

        if len(temperatures) > 10:
            del temperatures[0]
            del humidites[0]
            del heures[0]

        if len(luminosites) >= 2:
            del luminosites[0]

        print(str(temperature) + " °C")
        print(str(humidite) + " %")
        print(str(luminosite) + " %")
        print(heures)

    return (jsonify(body))


@app.route('/IoT')
def line():
    api = ('http://api.openweathermap.org/data/2.5/weather?q=Lille&lang=fr&units=metric&appid=1ce145d5c94f1ce3502497ae86aa2c7c')
    jsonMeteo = requests.get(api).json()
    jsonMeteo = json.dumps(jsonMeteo)
    jsonMeteo = json.loads(jsonMeteo)

    ville = jsonMeteo.get("name")

    jour = str(datetime.date.today().weekday())
    jour = jours(jour)
    heure = jsonMeteo.get("dt")
    now = time.localtime(int(heure))
    heure = formatHeure(now, heure)

    description = jsonMeteo.get("weather")[0].get("description")
    icon = jsonMeteo.get("weather")[0].get("icon")
    meteoTemperature = jsonMeteo.get("main").get("temp")
    meteoSunRise = jsonMeteo.get("sys").get("sunrise")
    SunRise = time.localtime(int(meteoSunRise))
    meteoSunRise = formatHeure(SunRise, meteoSunRise)
    meteoSunSet = jsonMeteo.get("sys").get("sunset")
    SunSet = time.localtime(int(meteoSunSet))
    meteoSunSet = formatHeure(SunSet, meteoSunSet)
    meteoPression = jsonMeteo.get("main").get("pressure")
    meteoHumidite = jsonMeteo.get("main").get("humidity")
    meteoVent = jsonMeteo.get("wind").get("speed")
    return render_template('Iot.html', ville=ville, description=description, jour=jour, heure=heure, icon=icon, meteoTemperature=meteoTemperature, meteoSunRise=meteoSunRise, meteoSunSet=meteoSunSet, meteoPression=meteoPression, meteoHumidite=meteoHumidite, meteoVent=meteoVent, title='Plant de tomate', max=50, heures=heures, temperatures=temperatures, humidites=humidites, luminosite=luminosites)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
