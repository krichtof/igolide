from flask import Flask
from flask import request
app = Flask(__name__)

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

from event import Event
from event_packet import EventPacket

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

@app.route('/events', methods=['POST'])
def handle_event():
    event = Event.from_request(request)

    if event and event.packet and uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        uart_service.write(event.packet.to_bytes())
    else:
        print("Event ignored")

    return "Ok guy"

@app.route('/success', methods=['POST'])
def display_success_animation():
    duration = None
    try:
        duration = int(request.form['duration'])
    except KeyError:
        pass

    if uart_connection and uart_connection.connected:
        uart_service = uart_connection[UARTService]
        uart_service.write(EventPacket(EventPacket.SUCCESS, duration).to_bytes())
    else:
        print("No bluetooth connection")
        abort(500)

    return "Success animation displayed"
