import pyttsx3 # pip install pyttsx3
import paho.mqtt.client as mqtt #pip install paho-mqtt
import json
import os

class _TTS:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

text = "6.1.4 Test: 0.1 µW to 20 W, 2 dB increments PRN: L1, G1, L2, L5"
#engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)

def speak(text):
    text = text.replace("µW","microwatts")
    text = text.replace("W","watts")
    text = text.replace("µ","micro")
    #engine.say(text)
    #engine.runAndWait()
    tts = _TTS()
    tts.start(text)
    del(tts)

MQTT = True

if MQTT:
    print('Connecting to mqtt: '+os.getenv("MQTTUSER")+"@"+os.getenv("MQTTHOST"))
    mqttc = mqtt.Client(client_id='mqtt-rds', userdata=None, protocol=mqtt.MQTTv5, transport='tcp')
    mqttc.username_pw_set(os.getenv("MQTTUSER"), password=os.getenv("MQTTPASS"))
    mqttc.connect(os.getenv("MQTTHOST"))
    mqttc.subscribe("basic_status/testevent")
    

def on_message(client, userdata, message):
    print("msg...")
    msg = str(message.payload.decode("utf-8"))
    
    try:
        jmsg = json.loads(msg)
    except:
        print("Error decoding json: "+msg)
        return
    
    #print("message topic=",message.topic)
    #TODO: change to site topics
    print("message received " ,msg)
    #mqttc.loop_stop()
    speak("yo, mah dude!")
    #mqttc.loop_start()


if MQTT:
    mqttc.on_message=on_message         #attach function to callback
    mqttc.loop_start()                  #start the loop

while(True):
    cmd = input("Choose command (EXIT): ")
    if(cmd == "EXIT" or cmd == "e"):
        print("exiting..")
        #if MQTT:    
        #    mqttc.loop_stop()
        #    mqttc.disconnect()
        exit()
    elif(cmd == 't'):
        mqttc.loop_stop()
        mqttc.loop_start()
        print("connected: "+str(mqttc.is_connected()))
        
    else:
        print("Unknown command: "+cmd)
        continue