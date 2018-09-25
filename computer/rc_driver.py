import sys
import threading
import socketserver
import numpy as np

from model import NeuralNetwork

# distance data measured by ultrasonic sensor
sensor_data = None


class SensorDataHandler(socketserver.BaseRequestHandler):

    data = " "

    def handle(self):
        global sensor_data
        while self.data:
            self.data = self.request.recv(1024)
            sensor_data = round(float(self.data), 1)
            # print "{} sent:".format(self.client_address[0])
            print(sensor_data)


class VideoStreamHandler(socketserver.StreamRequestHandler):

    # h1: stop sign, measured manually
    # h2: traffic light, measured manually
    h1 = 5.5  # cm
    h2 = 5.5

    # load trained neural network
    nn = NeuralNetwork()
    nn.load_model("saved_model/nn_model.xml")

    obj_detection = ObjectDetection()
    rc_car = RCControl("/dev/tty.usbmodem1411")

    def handle(self):

        global sensor_data
        stream_bytes = b' '
        stop_flag = False
        stop_sign_active = True

        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    cv2.imshow('image', image)
                    # cv2.imshow('mlp_image', roi)

                    # reshape image
                    image_array = roi.reshape(1, int(height/2) * width).astype(np.float32)

                    # neural network makes prediction
                    prediction = self.nn.predict(image_array)

                    # stop conditions
                    if sensor_data and int(sensor_data) < 30:
                        print("Stop, obstacle in front")
                        self.rc_car.stop()
                        sensor_data = None

                    else:
                        self.rc_car.steer(prediction)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("car stopped")
                        self.rc_car.stop()
                        break
        finally:
            cv2.destroyAllWindows()
            sys.exit()


class Server(object):
    def __init__(self, host, port1, port2):
        self.host = host
        self.port1 = port1
        self.port2 = port2

    def video_stream(self, host, port):
        s = socketserver.TCPServer((host, port), VideoStreamHandler)
        s.serve_forever()

    def sensor_stream(self, host, port):
        s = socketserver.TCPServer((host, port), SensorDataHandler)
        s.serve_forever()

    def start(self):
        sensor_thread = threading.Thread(target=self.sensor_stream, args=(self.host, self.port2))
        sensor_thread.daemon = True
        sensor_thread.start()
        self.video_stream(self.host, self.port1)

class RCControl(object):

    def __init__(self, serial_port):
        self.serial_port = serial.Serial(serial_port, 115200, timeout=1)

    def steer(self, prediction):
        if prediction == 2:
            self.serial_port.write(chr(1).encode())
            print("Forward")
        elif prediction == 0:
            self.serial_port.write(chr(7).encode())
            print("Left")
        elif prediction == 1:
            self.serial_port.write(chr(6).encode())
            print("Right")
        else:
            self.stop()

    def stop(self):
        self.serial_port.write(chr(0).encode())

if __name__ == '__main__':
    h, p1, p2 = "192.168.1.157", 8000, 8002

    ts = Server(h, p1, p2)
    ts.start()
