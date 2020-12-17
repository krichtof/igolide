from flask import Flask
from flask import request
import json
app = Flask(__name__)

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()

uart_connection = None

if not uart_connection:
    print("Trying to connect...")
    for adv in ble.start_scan(ProvideServicesAdvertisement):
        if UARTService in adv.services:
            uart_connection = ble.connect(adv)
            print("Connected")
            break
    ble.stop_scan()

@app.route('/')
def index():
    return "Notif Light anime votre salon lorsqu'un événement survient"

@app.route('/events', methods=['GET','POST'])
def handle_event():
    data = json.loads(request.form['payload'])
    print(data["commits"][0]["author"]["username"])

    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        uart_service.write("warning".encode("utf-8"))
        uart_service.write(b'\n')

    return "Ok guy"
