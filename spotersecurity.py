import cv2
import numpy as np
import configparser
from flask import Flask, Response, render_template
from requests import Session
import asyncio

# Initialize PyP100 details
#import asyncio
import os




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
def turn_off_switch():
    # Implement code to turn off the TP-Link smart switch
    print("Turning off the TP-Link smart switch...")
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
    turn_off_switch()  # Call the turn_off_switch function
    return 'Switch turned off'  # Return a response

# Start the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
