# Connect to ble_bluefruit_color_picker service over BLE UART.

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

if uart_connection and uart_connection.connected:
    uart_service = uart_connection[UARTService]
    color_packet = ColorPacket((0,0,0))
    button_packet = ButtonPacket(b'1', True)
    # uart_service.write(color_packet.to_bytes())
    print("button_packet bytes", button_packet.to_bytes())
    uart_service.write(button_packet.to_bytes())
