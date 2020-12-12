"""
Bluetooth Controlled Room Lights using a Circuit Playground Bluetooth
   Scroll between 7 modes and control brightness with your smartphone via Bluetooth
   Full tutorial: https://learn.adafruit.com/easy-no-solder-bluetooth-controlled-room-lights/overview
Code by Kattni Rembor & Erin St Blaine for Adafruit Industries
Adafruit invests time and resources to bring you this code! Please support our shop!
"""

# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-few-public-methods

import board
import neopixel
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.sequence import AnimateOnce
from adafruit_led_animation.color import (
    AMBER,
    ORANGE,
    WHITE,
    RED,
    BLACK,
    colorwheel,
)


from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

NUM_LEDS = 240                   # change to reflect your LED strip
NEOPIXEL_PIN = board.A1        # change to reflect your wiring

pixels = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_LEDS, brightness=1.0,
                           auto_write=False
                           )


ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)
advertisement.complete_name = "DingDong"



brightWhite = Solid(pixels, color=(150, 150, 150))
powerup = RainbowComet(pixels, speed=0, tail_length=50, bounce=False)
warning = Pulse(pixels, speed=0.1, color=AMBER, period=3)
off = Solid(pixels, color=BLACK)

#startup animation will play just once
startup = AnimateOnce(powerup)

fire = AnimationGroup(
    Comet(pixels, speed=0, tail_length=1, color=BLACK),
    Sparkle(pixels, speed=0.05, num_sparkles=10, color=AMBER),
    Sparkle(pixels, speed=0.05, num_sparkles=10, color=RED),
    Sparkle(pixels, speed=0.05, num_sparkles=20, color=ORANGE),
    Sparkle(pixels, speed=0.05, num_sparkles=5, color=0xFF7D13),
    Sparkle(pixels, speed=0.05, num_sparkles=10, color=BLACK),
    )

# Here is the animation playlist where you set the order of modes

animations = AnimationSequence(brightWhite, fire, warning)
times = 20
count = 0
MODE = 0

while True:
    if MODE == 0:  # If currently off...
        startup.animate()
        while startup.animate():
            pass
        MODE = 1
    # Advertise when not connected

    elif MODE >= 1:  # If not OFF MODE...
        ble.start_advertising(advertisement)
        while not ble.connected:
            if MODE == 2:
                pass
            elif MODE == 1:
                brightWhite.animate()
    # Now we're connected

    while ble.connected:
        s = uart_service.readline().decode("utf-8").strip()
        if s == 'celebrate':
            count = 0
            MODE = 1
            animations.activate(1)
            print("oh yeah ! celebrate !")
        elif s == 'warning':
            count = 0
            MODE = 1
            animations.activate(1)
        if count > times:
            MODE = 3
            count = 0
            off.animate()
        if MODE == 1:
            animations.animate()
            count += 1
