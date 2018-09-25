# AutoCarBeta
A self-driving 1/24 model car.
- Perception: PiCamera, Ultrasonic Sensor (HC-SR04)
- Data Communication: Multi-thread TCP server between Raspberry Pi and computer
- Lane Following: Neural Network trained in OpenCV to decide steer direction based on streamed camera input
- Control: Serial communication between computer and Arduino, which uses digital signal for the remote control

# Gallery
![Arduino Remote Control & Original Car](images/Arduino_RC_and_original_car.JPG?raw=true "Arduino Remote Control & Original Car")
![Final Car](images/final_car.JPG?raw=true "Final car mounted with Raspberry Pi, PiCamera, ultrasonic sensor, and battery")

# Reference
- Main Reference:
https://zhengludwig.wordpress.com/projects/self-driving-rc-car/
- Raspberry Pi:
https://picamera.readthedocs.io/en/latest/recipes2.html#rapid-capture-and-streaming
https://www.raspberrypi-spy.co.uk/2013/01/ultrasonic-distance-measurement-using-python-part-2/
- RC Control:
https://medium.com/@pkletsko/how-to-create-a-self-driving-toy-car-part-1-controlling-car-with-a-keyboard-2169f6338f8d
