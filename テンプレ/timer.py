#!/usr/bin/python3

import datetime
import time
import RPi.GPIO as GPIO

# 変数宣言
LED_GPIO = 18
LED_active = True

#GPIOセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO , GPIO.OUT)

def main():
    try:
        while True:
        # 朝6時にLEDを点灯
            if LED_active == False and datetime.datetime.now().strftime("%H:%M") == "06:00":
                print("LED_on_" + datetime.datetime.now().strftime("%H:%M"))
                GPIO.output(LED_GPIO, GPIO , True)
                LED_active = True

            # 夜21時にLEDを消灯
            if LED_active == True and datetime.datetime.now().strftime("%H:%M") == "21:00":
                print("LED_off_" + datetime.datetime.now().strftime("%H:%M"))
                GPIO.output(LED_GPIO, GPIO , False)
                LED_active = False

    except Exception as err_txt:
        #print("----- Error! -----")
        pass
    finally:
        #クリーンナップ#
        GPIO.cleanup()