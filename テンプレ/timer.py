#!/usr/bin/python3

import datetime
import RPi.GPIO as GPIO

# 変数宣言
LED_GPIO = 18
LED_active = True

#GPIOセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO , GPIO.OUT)


try:
    while True:
    # 朝6時にLEDを点灯
        if LED_active == False and datetime.datetime.now().strftime("%H:%M") == "15:44":
            print("LED_on_" + datetime.datetime.now().strftime("%H:%M"))
            GPIO.output(LED_GPIO, 1)
            LED_active = True

        # 夜21時にLEDを消灯
        if LED_active == True and datetime.datetime.now().strftime("%H:%M") == "15:45":
            print("LED_off_" + datetime.datetime.now().strftime("%H:%M"))
            GPIO.output(LED_GPIO, 0)
            LED_active = False

except Exception as err_txt:
    #print("----- Error! -----")
    pass
finally:
    #クリーンナップ#
    GPIO.cleanup()