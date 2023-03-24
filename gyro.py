import time
from mpu6050 import mpu6050

sensor = mpu6050(0x68)

while True:
    gyro_data = sensor.get_gyro_data()
    x = gyro_data['x']
    y = gyro_data['y']
    z = gyro_data['z']
    gyro_angle = (x + y + z) / 3 # calculate the average value
    print("Degree angle of gyroscope: " + str(gyro_angle))
    time.sleep(1) # wait for one second
