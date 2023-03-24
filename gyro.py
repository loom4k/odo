import smbus
import time

# MPU6050 Registers and Addresses
DEVICE_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

# Initialize I2C bus
bus = smbus.SMBus(1)

# Initialize MPU6050
bus.write_byte_data(DEVICE_ADDR, PWR_MGMT_1, 0)

# Read and format data from MPU6050
def read_data(addr):
    high = bus.read_byte_data(DEVICE_ADDR, addr)
    low = bus.read_byte_data(DEVICE_ADDR, addr+1)
    value = ((high << 8) | low)
    if (value > 32768):
        value = value - 65536
    return value

# Main loop to read and print data from MPU6050
while True:
    gyro_x = read_data(GYRO_XOUT_H)
    gyro_y = read_data(GYRO_YOUT_H)
    gyro_z = read_data(GYRO_ZOUT_H)
    accel_x = read_data(ACCEL_XOUT_H)
    accel_y = read_data(ACCEL_YOUT_H)
    accel_z = read_data(ACCEL_ZOUT_H)

    print(f"Gyroscope (deg/s): X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
    print(f"Accelerometer (g): X={accel_x}, Y={accel_y}, Z={accel_z}")
    print("-----------------------------")

    time.sleep(0.1)  # pause for 100ms
