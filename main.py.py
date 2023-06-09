import machine
import time
from Lights import Light
from Buzzer import *
from Displays import *
from Button import *

# Define GPIO pins for the traffic light
GREEN_PIN = machine.Pin(12, machine.Pin.OUT)
YELLOW_PIN = machine.Pin(13, machine.Pin.OUT)
RED_PIN = machine.Pin(14, machine.Pin.OUT)

# Define GPIO pins for the pedestrian display
WALK_PIN = machine.Pin(21, machine.Pin.OUT)
DONT_WALK_PIN = machine.Pin(20, machine.Pin.OUT)

# Define GPIO pin for the buzzer
BUZZER_PIN = machine.Pin(15, machine.Pin.OUT)

# Define TrafficLight class
class TrafficLight:
    def __init__(self):
        self.green_pin = GREEN_PIN
        self.yellow_pin = YELLOW_PIN
        self.red_pin = RED_PIN

    def controlState(self):
        # Green light
        self.green_pin.on()
        self.yellow_pin.off()
        self.red_pin.off()
        time.sleep(7)

        # Yellow light
        self.green_pin.off()
        self.yellow_pin.on()
        self.red_pin.off()
        time.sleep(3)

        # Red light
        self.green_pin.off()
        self.yellow_pin.off()
        self.red_pin.on()
        time.sleep(7)

# Define TrafficLightController class
class TrafficLightController:
    def __init__(self):
        self.button = machine.Pin(17, machine.Pin.IN)
        self.display = Display()
        self.buzzer = Buzzer()

    def coordinateSystem(self):
        while True:
            if self.button.value() == 1:
                # Display "Walk" and make sound
                self.display.printWords("Walk")
                self.buzzer.makeSound()

                # Control traffic light state
                traffic_light = TrafficLight()
                traffic_light.controlState()

                # Display "Don't Walk" and make sound
                self.display.printWords("Don't Walk")
                self.buzzer.makeSound()

                # Countdown timer for 30 seconds
                self.display.printWords("Countdown: 30")
                self.buzzer.makeSound()

                for i in range(29, -1, -1):
                    self.display.printWords("Countdown: " + str(i))
                    self.buzzer.makeSound()
                    time.sleep(1)

# Define Display class
class Display:
    def __init__(self):
        self.display = LCDDisplay(sda=20, scl = 21, i2cid = 0)
        self.display.showText("Dont Walk")
        self.screen = machine.Pin(20, machine.Pin.OUT)
        self.walk_pin = WALK_PIN
        self.dont_walk_pin = DONT_WALK_PIN

    def printWords(self, text):
        self.screen.on()
        self.walk_pin.off()
        self.dont_walk_pin.off()

        if text == "Walk":
            self.walk_pin.on()
        elif text == "Don't Walk":
            self.dont_walk_pin.on()
        elif text.startswith("Countdown"):
            self.walk_pin.off()
            self.dont_walk_pin.off()
            self.screen.off()
            time.sleep(0.1)
            self.screen.on()
            time.sleep(0.1)
            self.screen.off()
            time.sleep(0.1)
            self.screen.on()
            time.sleep(0.1)

# Define Buzzer class
class Buzzer:
    def __init__(self):
        self.beep = BUZZER_PIN

    def makeSound(self):
        self.beep.on()
        time.sleep(3)
        self.beep.off()
        time.sleep(3)



# Instantiate TrafficLightController
traffic_light_controller = TrafficLightController()

# Start coordinating the traffic light system
traffic_light_controller.coordinateSystem()