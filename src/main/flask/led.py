#coding=utf-8
import time
import RPi.GPIO as GPIO

def lightLED(sleepTime,lightTime):
	GPIO.setmode(GPIO.BCM)
	time.sleep(float(sleepTime)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
   	time.sleep(float(lightTime))
    GPIO.output(27, GPIO.LOW)
	time.sleep(1)
	GPIO.cleanup()
    