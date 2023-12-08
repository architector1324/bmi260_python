from time import sleep

from bmi260 import registers
from bmi260 import definitions
from bmi260.BMI270 import BMI270
from bmi260 import config_file


# init
sensor = BMI270(registers.I2C_SEC_ADDR) # change to `I2C_PRIM_ADDR` if does not work
sensor.soft_reset()

sensor.load_config_file(config_file.bmi260_config_file)

# config
sensor.set_mode(definitions.PERFORMANCE_MODE)

sensor.set_acc_range(definitions.ACC_RANGE_2G)
sensor.set_acc_odr(definitions.ACC_ODR_200)
sensor.set_acc_bwp(definitions.ACC_BWP_NORMAL)

sensor.set_gyr_range(definitions.GYR_RANGE_2000)
sensor.set_gyr_odr(definitions.GYR_ODR_200)
sensor.set_gyr_bwp(definitions.GYR_BWP_NORMAL)

sensor.disable_fifo_header()
sensor.enable_data_streaming()
sensor.enable_acc_filter_perf()
sensor.enable_gyr_noise_perf()
sensor.enable_gyr_filter_perf()


if __name__ == "__main__":
    while True:
        print(f'gyro: {sensor.get_raw_gyr_data()} accel: {sensor.get_raw_acc_data()}')
        sleep(0.1)
