#!/usr/bin/env python3

import socket
import time

from bmi260.BMI270 import *

# from src.bmi260.BMI270 import *


# -------------------------------------------------
# INITIALIZATION
# -------------------------------------------------

try:
    BMI270_1 = BMI270(I2C_PRIM_ADDR)
    BMI270_1.load_config_file()
except Exception as e:
    print("Error: " + str(e))
    print("Could not initialize BMI270_1. Check your wiring or try again.")
    exit(1)

try:
    BMI270_2 = BMI270(I2C_SEC_ADDR)
    BMI270_2.load_config_file()
except Exception as e:
    print("Error: " + str(e))
    print("Could not initialize BMI270_2. Check your wiring or try again.")
    exit(1)


# -------------------------------------------------
# HARDWARE CONFIGURATION
# -------------------------------------------------

BMI270_1.set_mode(PERFORMANCE_MODE)
BMI270_1.set_acc_range(ACC_RANGE_2G)
BMI270_1.set_gyr_range(GYR_RANGE_1000)
BMI270_1.set_acc_odr(ACC_ODR_200)
BMI270_1.set_gyr_odr(GYR_ODR_200)
BMI270_1.set_acc_bwp(ACC_BWP_OSR4)
BMI270_1.set_gyr_bwp(GYR_BWP_OSR4)
BMI270_1.disable_fifo_header()
BMI270_1.enable_data_streaming()
BMI270_1.enable_acc_filter_perf()
BMI270_1.enable_gyr_noise_perf()
BMI270_1.enable_gyr_filter_perf()

BMI270_2.set_mode(PERFORMANCE_MODE)
BMI270_2.set_acc_range(ACC_RANGE_2G)
BMI270_2.set_gyr_range(GYR_RANGE_1000)
BMI270_2.set_acc_odr(ACC_ODR_200)
BMI270_2.set_gyr_odr(GYR_ODR_200)
BMI270_2.set_acc_bwp(ACC_BWP_OSR4)
BMI270_2.set_gyr_bwp(GYR_BWP_OSR4)
BMI270_2.disable_fifo_header()
BMI270_2.enable_data_streaming()
BMI270_2.enable_acc_filter_perf()
BMI270_2.enable_gyr_noise_perf()
BMI270_2.enable_gyr_filter_perf()


# -------------------------------------------------
# NETWORK CONFIGURATION
# -------------------------------------------------

# Change IP and port to your needs
RECEIVER_ADDRESS = ('192.168.1.2', 8000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup sender address if needed (to always use the same sport as sender)
# SENDER_ADDRESS = ('192.168.1.1', 8001)
# sock.bind(SENDER_ADDRESS)


# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------

start_time = time.time()


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_milliseconds():
    return int(round((time.time() - start_time) * 1000))

def get_and_send_data():
    data_array = np.zeros(14, dtype=np.int32)

    data_array[0] = get_milliseconds()
    data_array[1:4] = BMI270_1.get_raw_acc_data()
    data_array[4:7] = BMI270_1.get_raw_gyr_data()
    data_array[7] = get_milliseconds()
    data_array[8:11] = BMI270_2.get_raw_acc_data()
    data_array[11:14] = BMI270_2.get_raw_gyr_data()
    
    sock.sendto(data_array.tobytes(), RECEIVER_ADDRESS)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():
    current_time = 0.0
    old_time = 0.0
    update_rate = 0.005
    data_streaming = False


    while True:
        current_time = time.time() - start_time
        
        try:
            get_and_send_data()
            if not data_streaming:
                print("\nSending data to " + str(RECEIVER_ADDRESS) + " at " + str(1 / update_rate) + " Hz\n")
                data_streaming = True
        except Exception as e:
            print("Error: " + str(e))
            print("Could not send data. Check your wiring. Trying again in 5 seconds...")
            data_streaming = False
            sleep(5)

        time_delta = current_time - old_time
        old_time = current_time
        
        sleep(max(update_rate - time_delta, 0))



if __name__ == "__main__":
    main()
