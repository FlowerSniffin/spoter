import cv2
import numpy as np
import configparser
from flask import Flask, Response

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

# Placeholder function to turn off the TP-Link smart switch
def turn_off_switch():
    # Implement code to turn off the TP-Link smart switch
    print("Turning off the TP-Link smart switch...")

# Placeholder function to send a notification via Signal messenger
def send_signal_message():
    # Implement code to send a message via Signal messenger
    print("Sending notification via Signal...")

# Access the video camera based on the configured index
cap = cv2.VideoCapture(video_device_index)

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
                    # Person detected, trigger actions
                    turn_off_switch()  # Turn off the TP-Link smart switch
                    send_signal_message()  # Send a notification via Signal

        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Define a route for the Flask web server
@app.route('/')
def index():
    return "Welcome to Object Detection with Flask!"

# Define a function to generate video frames for the Flask app
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define a route for streaming video on the Flask web server
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the object detection loop and start the Flask web server
if __name__ == '__main__':
    from threading import Thread
    detection_thread = Thread(target=detect_objects)
    detection_thread.start()
    app.run(host='0.0.0.0', port=5000)
