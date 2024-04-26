# Spoter
Spoter is python program that spots objects with neural network (edgeYOLO) and lets you automate stuff under preset conditions.Currently we are trying to integrate as many IOT switches from tplink we will be adding more manufactures

Funcionality:

-Supports any USB camera or OBS virtual camera running on the same computer this script is running.

-Lets you easily use web frontend to config many things

Example use-cases:

-You want to switch ON/OFF tplink switch that is connected to your cat/dog feeder when the camera sees the dog/cat it will send you a message (currently only Signal network supported) and it will turn ON/OFF the switch connected to your feeder thus feeds your fluffy companion

-When person is detected it will send you photo/video on signal with timestampt 

Device support list:

-Currently we support TPlink P100D for switching things but we should add many more devices

Messaging notification network support list:

-At the time only signal network is utilized to send messages about detections and actions taken



Do not forget to download:https://github.com/patrick013/Object-Detection---Yolov3/blob/master/model/yolov3.weights or else it wont run
