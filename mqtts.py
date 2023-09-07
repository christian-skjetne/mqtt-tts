import pyttsx3 # pip install pyttsx3
import paho.mqtt.client as mqtt #pip install paho-mqtt
import json
import os
import random

text = "6.1.4 Test: 0.1 µW to 20 W, 2 dB increments PRN: L1, G1, L2, L5"
class _TTS:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate",180)
    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

def speak(text):
    text = text.replace("µW","microwatts")
    text = text.replace("W","watts")
    text = text.replace("µ","micro")
    tts = _TTS()
    tts.start(text)
    del(tts)

MQTT = True

if MQTT:
    print('Connecting to mqtt: '+os.getenv("MQTTUSER")+"@"+os.getenv("MQTTHOST"))
    mqttc = mqtt.Client(client_id='mqtt-tts-'+str(random.randint(0, 999)), userdata=None, protocol=mqtt.MQTTv5, transport='tcp')
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
    if( 'siteid' in jmsg and jmsg['siteid'] == 1 and 'status' in jmsg and jmsg['status'] == "start" ):
        print("got start msg")
        txt = "starting test now!: "+jmsg['name']+":-, "+jmsg['name']+":-, "+jmsg['name']+","
        if('description' in jmsg):
            rt1 = jmsg['description']
            if('comment' in jmsg):
                rt1 = jmsg['description']+' - '+jmsg['comment']
                txt = txt+" "+rt1
            else:
                txt = txt+" "+jmsg['description']
        print("saying: "+txt)
        speak(txt)
    elif( 'siteid' in jmsg and jmsg['siteid'] == 1 and 'status' in jmsg and jmsg['status'] == "stop" ):
        print("got stop msg")
        speak("Test "+jmsg['name']+" over.")

if MQTT:
    mqttc.on_message=on_message         #attach function to callback
    mqttc.loop_start()                  #start the loop

while(True):
    cmd = input("Choose command (EXIT): ")
    if(cmd == "EXIT" or cmd == "e"):
        print("exiting..")
        if MQTT:    
            mqttc.loop_stop()
            mqttc.disconnect()
        exit()
    elif(cmd == 't'):
        print("connected: "+str(mqttc.is_connected()))
    else:
        print("Unknown command: "+cmd)
        continue