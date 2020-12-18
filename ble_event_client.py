# Connect to ble_bluefruit_color_picker service over BLE UART.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from event_packet import EventPacket

ble = BLERadio()

uart_connection = None

if not uart_connection:
    print("Trying to connect...")
    for adv in ble.start_scan(ProvideServicesAdvertisement):
        if UARTService in adv.services:
            uart_connection = ble.connect(adv)
            print("Connected to ", adv.complete_name)
            break
    ble.stop_scan()

if uart_connection and uart_connection.connected:
    uart_service = uart_connection[UARTService]
    event_packet = EventPacket(EventPacket.WARNING, 30)
    uart_service.write(event_packet.to_bytes())
