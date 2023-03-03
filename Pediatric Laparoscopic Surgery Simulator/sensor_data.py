import serial
class sensor_data(object):
    def __init__(self):
        self.test_string = "Testing class in another file"
        self.running = 0    # 1 = running, 0 = stopped
        self.sensor_string = ""



def start_sensors():
    sensor_data.running = 1
    try:
        ser = serial.Serial('COM5', 9600)
    except serial.SerialException:
        serial.Serial('COM5', 9600).close()
        ser = serial.Serial('COM5', 9600)

    while (sensor_data.running == 1):
        stuff = ser.readline()
        stuff_string = stuff.decode()
        sensor_data.sensor_string = stuff_string.rstrip()

    # When running set to 0, close serial port
    serial.Serial('COM5', 9600).close()
def test_print():
    print("test print")
