#!/usr/bin/python3

import sys
import datetime
import time
import signal
import RPi.GPIO as GPIO
import logging

time.sleep(60)

# ログ設定
logging.basicConfig(filename='/data/scripts/rpi.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    datefmt=('%Y/%m/%d %H:%M:%S')
                    )

# シグナル内容
def handler(signum, frame):
    GPIO.cleanup()
    logging.info('Force halt by kill.')
    sys.exit(0)

# シグナルをシステム登録
signal.signal(signal.SIGTERM, handler)

def main():
    # 変数宣言
    LED_active = True


    # GPIO初期化
    try:
        logging.info('GPIO SETUP : START')
        # Pinをボードベースに設定
        GPIO.setmode(GPIO.BOARD)
        # Pure GPIO
        # ------------------------------------------
        #栽培用LED : (pin-37)
        # ------------------------------------------
        # LED用のGPIOを設定
        GPIO.setup(37, GPIO.OUT, initial=GPIO.HIGH)
        # GPIOのセットアップに問題なし
        logging.info('GPIO SETUP : COMPLETE')
        #GPIO.output(21, GPIO.HIGH)
        #GPIO.output(23, GPIO.HIGH)
        GPIO.output(40, GPIO.HIGH)

    except Exception as gpio_setup_e:
        logging.error('GPIO SETUP ERROR:' + str(gpio_setup_e))
        # 全リソースを強制開放
        GPIO.cleanup()
        # リターンコード8で終了
        return 8

    # メインの処理
    try:
        # メインループ
        while True:
            # 朝6時にLEDを点灯
            if LED_active == False and datetime.datetime.now().strftime("%H:%M") == "06:00":
                print("LED_on_" + datetime.datetime.now().strftime("%H:%M"))
                GPIO.output(37, GPIO.HIGH)
                LED_active = True
                logging.info('LED STATUS : ON')

            # 夜21時にLEDを消灯
            if LED_active == True and datetime.datetime.now().strftime("%H:%M") == "21:00":
                print("LED_off_" + datetime.datetime.now().strftime("%H:%M"))
                GPIO.output(37, GPIO.LOW)
                LED_active = False
                logging.info('LED STATUS : OFF')

    except Exception as main_e:
        logging.error('MAIN Operation has error ' + str(main_e))

    finally:
        logging.info('Exit...')
        GPIO.cleanup()
        return 0


if __name__ == "__main__":
    sys.exit(main())