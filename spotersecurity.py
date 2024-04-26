import cv2
import numpy as np

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

# Access the USB camera
cap = cv2.VideoCapture(2)  # You may need to adjust the index based on your system

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

cap.release()
cv2.destroyAllWindows()
