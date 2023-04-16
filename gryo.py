import math
import smbus2
import time

# MPU6050 Registers and Addresses
DEVICE_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

# Initialize the I2C bus
bus = smbus2.SMBus(1)

# Power on the MPU6050
bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)

# Set the sample rate
bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)

# Set the low pass filter
bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)

# Set the gyro range
bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 0)

# Enable data ready interrupt
bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)

# Define the complementary filter coefficients
alpha = 0.98
beta = 1 - alpha

# Define the initial angles
angle_x = 0
angle_y = 0

# Define the initial gyro readings
gyro_x_prev = 0
gyro_y_prev = 0
gyro_z_prev = 0

# Define the time variables
t_prev = time.time()
dt = 0

while True:
    # Read the accelerometer and gyroscope values
    accel_x = bus.read_byte_data(DEVICE_ADDRESS, ACCEL_XOUT)
    accel_y = bus.read_byte_data(DEVICE_ADDRESS, ACCEL_YOUT)
    accel_z = bus.read_byte_data(DEVICE_ADDRESS, ACCEL_ZOUT)
    gyro_x = bus.read_byte_data(DEVICE_ADDRESS, GYRO_XOUT)
    gyro_y = bus.read_byte_data(DEVICE_ADDRESS, GYRO_YOUT)
    gyro_z = bus.read_byte_data(DEVICE_ADDRESS, GYRO_ZOUT)

    # Calculate the accelerometer angles
    accel_x_angle = math.degrees(math.atan2(accel_y, accel_z))
    accel_y_angle = math.degrees(math.atan2(accel_x, accel_z))

    # Calculate the gyro angles
    t_now = time.time()
    dt = t_now - t_prev
    t_prev = t_now

    gyro_x_rate = gyro_x / 131.0
    gyro_y_rate = gyro_y / 131.0
    gyro_z_rate = gyro_z / 131.0

    gyro_x_angle = gyro_x_rate * dt + gyro_x_prev
    gyro_y_angle = gyro_y_rate * dt + gyro_y_prev
    gyro_z_angle = gyro_z_rate * dt + gyro_z_prev

    gyro_x_prev = gyro_x_angle
    gyro_y_prev = gyro_y_angle
    gyro_z_prev = gyro_z_angle

    # Calculate the complementary filter angles
    angle_x = alpha * (angle_x + gyro_x_angle) + beta * accel_x_angle
    angle_y = alpha * (angle_y + gyro_y_angle) + beta * accel_y_angle

    # Calculate the final angle
    angle = math.sqrt(angle_x**2 + angle_y**2)

    # Convert the angle to a value between 1 and 360 degrees
    angle_degrees = angle if angle >= 0 else angle + 360

    # Print the angle value
    print("Angle: ", angle_degrees)

    # Wait for a short period of time before reading again
    time.sleep(0.01)