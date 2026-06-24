#!/usr/bin/env python3

# ── STEP 1: borrow the tools we need ──────────────────
from sbp.client.drivers.network_drivers import TCPDriver  # ethernet connection tool
from sbp.client import Handler, Framer                    # message reader tools
from sbp.imu import MsgImuRaw, MsgImuAux                 # IMU message blueprints
from time import time       
import math         
import json                      # stopwatch tool

# ── STEP 2: define where sensor is ────────────────────
HOST = '195.37.48.233'
PORT = 55555
raw_count=4096 # sensitivity linear
GYRO_SENSITIVITY = 131.2 
g=9.8065

try:                                      
    with TCPDriver(HOST, PORT) as driver: 
        with Handler(Framer(driver.read, driver.write)) as handler:
            print("initate connection")
            start_time = time()           

            with open("imu_calibration.json", "r") as f:
                calib = json.load(f)

            # print(calib["x_bias"], calib["y_bias"], calib["z_bias"])
            # print(calib["x_g_bias"], calib["y_g_bias"], calib["z_g_bias"])

            for msg,metadata in handler:
                if isinstance(msg,MsgImuRaw):
                    # print("linear acceleration")
                    # print(((msg.acc_x/raw_count)-calib["x_bias"])*g)
                    # print(((msg.acc_y/raw_count)-calib["y_bias"])*g)
                    # print(((msg.acc_z/raw_count)-calib["z_bias"])*g)
                    print("angular velocity")
                    print(((msg.gyr_x/GYRO_SENSITIVITY)-calib["x_g_bias"])*(math.pi/180))
                    print(((msg.gyr_y/GYRO_SENSITIVITY)-calib["y_g_bias"])*(math.pi/180))
                    print(((msg.gyr_z/GYRO_SENSITIVITY)-calib["z_g_bias"])*(math.pi/180))
                    if time() - start_time >= 2:  
                        break   

except KeyboardInterrupt:
    print("Stopped by user.")