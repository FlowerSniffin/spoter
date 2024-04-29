#There are two types of connecting to TPlink device based on plugp100 library
#As you can see there are these two functions "example_connect_by_guessing" which is the one i have been able to utilize
#Need to find out what is wrong with the other one "example_discovery" 
#When you run this app flask hosts site reacheable on your localhost under port :5000
#/127.0.0.1/testing has button which is meant for testing functions, in this version of the program it is specifically set to call "tryauthorize" function for test purp 
#Finally status of the device is recheable, so far tested only with smartplug p100, but we can clearly see authentification works
#We are currently testing the plugp100 library to not only get the status of the device but to actually control it 
import cv2
import numpy as np
import configparser
from flask import Flask, Response, render_template
from requests import Session
import asyncio
import logging
import os
# Imports plugp100 library
from plugp100.common.credentials import AuthCredential
from plugp100.common.credentials import AuthCredential
from plugp100.discovery.tapo_discovery import TapoDiscovery
from plugp100.common.credentials import AuthCredential
from plugp100.new.device_factory import connect, DeviceConnectConfiguration



async def example_connect_by_guessing(credentials: AuthCredential, host: str):
    device_configuration = DeviceConnectConfiguration(
        host=host,
        credentials=credentials
    )
    device = await connect(device_configuration)
    await device.update()
    print({
        'type': type(device),
        'protocol': device.protocol_version,
        'raw_state': device.raw_state,
        'components': device.get_device_components
    })


async def example_discovery(credentials: AuthCredential):
    discovered = await TapoDiscovery.scan(timeout=5)
    for discovered_device in discovered:
        try:
            device = await discovered_device.get_tapo_device(credentials)
            await device.update()
            print({
                'type': type(device),
                'protocol': device.protocol_version,
                'raw_state': device.raw_state
            })
            await device.client.close()
        except Exception as e:
            logging.error(f"Failed to update {discovered_device.ip} {discovered_device.device_type}", exc_info=e)

async def disc():
    credentials = AuthCredential("davidnovak.cze@gmail.com", "Nasrat666.")
    #await example_discovery(credentials)
    await example_connect_by_guessing(credentials, "192.168.0.60")

def loopfunction():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(disc())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()

# Initialize Flask app
app = Flask(__name__)

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.cfg')
video_device_index = int(config['video']['cap'])

# Load the pre-trained YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Access the video camera based on the configured index
cap = cv2.VideoCapture(video_device_index)

# Placeholder function to turn off the TP-Link smart switch
def tryauthorize():
    # Implement code to turn off the TP-Link smart switch
    print("Trying to connect to ipadress set in function disc(dis as discover)")
    loopfunction()
    #p100.turnOff()

#just testing something
def send_sms():
    print("SMS received")
    
    
    
    # Placeholder function to send a notification via Signal messenger
def send_signal_message():
    # Implement code to send a message via Signal messenger
    print("Sending notification via Signal...")

# Define a function to perform object detection
def detect_objects():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Process the detections
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == 'person':
                    send_signal_message()
                    # Draw a bounding box around the detected person
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    turn_off_switch()
                    send_sms()
                    

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        
        # Yield the frame in the response for video streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route for video feed streaming
@app.route('/videofeed')
def videofeed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Define a route for the Flask web server
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testing')
def testing():
    return render_template('testing.html')

@app.route('/turn_off_switch', methods=['GET'])
def trigger_turn_off_switch():
    tryauthorize()  # Call the turn_off_switch function
    return 'Switch turned off'  # Return a response

# Start the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
