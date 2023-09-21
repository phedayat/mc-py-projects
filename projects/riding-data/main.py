from src.drivers.imu import MPU6050

try:
    data_path = "/sd/data"

    mpu = MPU6050('0')
    mpu.accel
    mpu.gyro
    mpu.temperature
    mpu.
except:
    print("No directory /sd")