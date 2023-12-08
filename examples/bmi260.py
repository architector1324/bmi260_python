from time import sleep

from bmi270 import registers
from bmi270 import definitions
from bmi270.BMI270 import BMI270
from bmi270 import config_file


# init
bmi260 = BMI270(registers.I2C_SEC_ADDR) # change to `I2C_PRIM_ADDR` if does not work
bmi260.soft_reset()

bmi260.load_config_file(config_file.bmi260_config_file)

# config
bmi260.set_mode(definitions.PERFORMANCE_MODE)

bmi260.set_acc_range(definitions.ACC_RANGE_2G)
bmi260.set_acc_odr(definitions.ACC_ODR_200)
bmi260.set_acc_bwp(definitions.ACC_BWP_NORMAL)

bmi260.set_gyr_range(definitions.GYR_RANGE_2000)
bmi260.set_gyr_odr(definitions.GYR_ODR_200)
bmi260.set_gyr_bwp(definitions.GYR_BWP_NORMAL)

bmi260.disable_fifo_header()
bmi260.enable_data_streaming()
bmi260.enable_acc_filter_perf()
bmi260.enable_gyr_noise_perf()
bmi260.enable_gyr_filter_perf()


if __name__ == "__main__":
    while True:
        print(f'gyro: {bmi260.get_raw_gyr_data()} accel: {bmi260.get_raw_acc_data()}')
        sleep(0.1)
