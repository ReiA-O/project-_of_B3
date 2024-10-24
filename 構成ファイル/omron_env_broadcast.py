from bluepy import btle
import struct

class ScanDelegate(btle.DefaultDelegate):
    #コンストラクタ
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        #センサデータ保持用変数
        self.sensorValue = None

    # スキャンハンドラー
    def handleDiscovery(self, dev, isNewDev, isNewData):  
        # 新しいデバイスが見つかったら
        if isNewDev or isNewData:  
            # アドバタイズデータを取り出し
            for (adtype, desc, value) in dev.getScanData():  
                #環境センサのとき、データ取り出しを実行
                if desc == 'Manufacturer' and value[0:4] == 'd502':
                    #センサの種類（EP or IM）を取り出し
                    sensorType = dev.scanData[dev.SHORT_LOCAL_NAME].decode(encoding='utf-8')
                    #EPのときのセンサデータ取り出し
                    if sensorType == 'EP':
                        self.decodeSensorData_EP(value)
                    #IMのときのセンサデータ取り出し
                    if sensorType == 'IM':
                        self.decodeSensorData_IM(value)

    # センサデータを取り出してdict形式に変換（EPモード時）
    def decodeSensorData_EP(self, valueStr):
        #文字列からセンサデータ(6文字目以降)のみ取り出し、バイナリに変換
        valueBinary = bytes.fromhex(valueStr[6:])
        #バイナリ形式のセンサデータを整数型Tapleに変換
        (temp, humid, light, uv, press, noise, discomf, wbgt, rfu, batt) = struct.unpack('<hhhhhhhhhB', valueBinary)
        #単位変換した上でdict型に格納
        self.sensorValue = {
            'SensorType': 'EP',
            'Temperature': temp / 100,
            'Humidity': humid / 100,
            'Light': light,
            'UV': uv / 100,
            'Pressure': press / 10,
            'Noise': noise / 100,
            'Discomfort': discomf / 100,
            'WBGT': wbgt / 100,
            'BatteryVoltage': (batt + 100) / 100
        }

    # センサデータを取り出してdict形式に変換（IMモード時）
    def decodeSensorData_IM(self, valueStr):
        #文字列からセンサデータ(6文字目以降)のみ取り出し、バイナリに変換
        valueBinary = bytes.fromhex(valueStr[6:])
        #バイナリ形式のセンサデータを整数型Tapleに変換
        (temp, humid, light, uv, press, noise, accelX, accelY, accelZ, batt) = struct.unpack('<hhhhhhhhhB', valueBinary)
        #単位変換した上でdict型に格納
        self.sensorValue = {
            'SensorType': 'IM',
            'Temperature': temp / 100,
            'Humidity': humid / 100,
            'Light': light,
            'UV': uv / 100,
            'Pressure': press / 10,
            'Noise': noise / 100,
            'AccelerationX': accelX / 10,
            'AccelerationY': accelY / 10,
            'AccelerationZ': accelZ / 10,
            'BatteryVoltage': (batt + 100) / 100
        }
