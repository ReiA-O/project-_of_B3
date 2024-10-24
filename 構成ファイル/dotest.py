# -*- coding:utf-8 -*-
#!/usr/bin/python3
import mariadb
import sys
from bluepy import btle
from omron_env_broadcast import ScanDelegate
import time
import schedule
import slackweb
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
float_SW_GPIO = 4

GPIO.setup(float_SW_GPIO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

scanner = btle.Scanner().withDelegate(ScanDelegate())
scanner.scan(5.0)
IotTemperature = scanner.delegate.sensorValue['Temperature']
IotHumidity = scanner.delegate.sensorValue['Humidity']
IotVoltage = scanner.delegate.sensorValue['BatteryVoltage']

print("data connect")

slack_DB_tuuti = "温度：" + str(IotTemperature) + "\n湿度：" + str(IotHumidity) + "\n電池残量" + str(IotVoltage)

slack_SW_tuuti = "水が減っています"
slack_SW_tuuti_1 = "水はあります"

def DBjob():
    slack = slackweb.Slack(url ="https://hooks.slack.com/services/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")
    print("start")
    try:
        # Python Style
        DBConnector = mariadb.connect(
        user="ipsa",
        password="ipsa2221",
        host="157.13.24.163",
        port=3306,
        database="23project_test"
        )
        print(f"CONNECT SUCCESSED")
    except mariadb.Error as e:
        print(f"CONNECT ERROR: {e}")
        sys.exit(1)

    # Create DB Object
    DBobj = DBConnector.cursor()

    # IoT Data
    scanner = btle.Scanner().withDelegate(ScanDelegate())
    #スキャンしてセンサ値取得（タイムアウト5秒）
    scanner.scan(5.0)

    IotTemperature = scanner.delegate.sensorValue['Temperature']
    IotHumidity = scanner.delegate.sensorValue['Humidity']
    IotVoltage = scanner.delegate.sensorValue['BatteryVoltage']

    # Iot Data to SQL
    nowTemp = str(IotTemperature)
    nowHumit = str(IotHumidity)
    nowVol = str(IotVoltage)

    # SQL Execute
    try:
        DBobj.execute("INSERT INTO test(collecttime,temperature,humidity,BatteryVoltage) VALUES (NOW(),?,?,?)",
        (nowTemp, nowHumit, nowVol) )
        print("温度")
        print(scanner.delegate.sensorValue['Temperature'])
        print("湿度")
        print(scanner.delegate.sensorValue['Humidity'])
        print("電池残量")
        print(scanner.delegate.sensorValue['BatteryVoltage'])
        print("-------------------")
    except mariadb.Error as e:
        print(f"SQL execute error: {e}")
    # Commit DB
    DBConnector.commit()

    # Close DB Connection
    DBConnector.close()
    slack_DB_tuuti = "DBに値送信しました\n温度：" + str(IotTemperature) + "\n湿度：" + str(IotHumidity) + "\n電池残量" + str(IotVoltage)
    slack.notify(text = slack_DB_tuuti)

def SWjob():
    slack = slackweb.Slack(url ="https://hooks.slack.com/services/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")
    time.sleep(1)   
    float_switch_status = GPIO.input(float_SW_GPIO)

    if float_switch_status == 0:
        print("水ない")
        slack.notify(text = slack_SW_tuuti)
        print("水不足通知送信")
    else:
        print("水ある")
        slack.notify(text = slack_SW_tuuti_1)
        print("水存在通知送信")

try:
    while True:
        print("hello")
        schedule.every().day.at("09:00").do(DBjob)
        schedule.every().day.at("12:00").do(DBjob)
        schedule.every().day.at("16:00").do(DBjob)

        schedule.every().day.at("16:52").do(DBjob)
        schedule.every().day.at("16:52").do(SWjob)

        schedule.every().day.at("09:10").do(SWjob)
        schedule.every().day.at("12:10").do(DBjob)
        schedule.every().day.at("16:10").do(DBjob)

        while True:
            schedule.run_pending()
            time.sleep(5)

except Exception as err_txt:
    print("----- Error! -----")
    pass