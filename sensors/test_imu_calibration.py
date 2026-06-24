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
 # LSB/°/s  — matches datasheet language
# ── STEP 3: connect safely ────────────────────────────
try:                                      # try this, if fails go to except
    with TCPDriver(HOST, PORT) as driver: # open connection, auto-closes after
        with Handler(Framer(driver.read, driver.write)) as handler:
            print("initate connection")
            # print("bias for 200 counts")

            start_time = time()           # start stopwatch
            count=0
            x_bias=0    
            y_bias=0
            z_bias=0
            x_g_bias=0
            y_g_bias=0
            z_g_bias=0
            for msg, metadata in handler:
                if isinstance(msg, MsgImuRaw):  # if you have the class imported
                    # print(msg.acc_x, msg.acc_y, msg.acc_z)   # Accelerometer data
                    x_bias=msg.acc_x+x_bias
                    y_bias=msg.acc_y+y_bias
                    z_bias=msg.acc_z+z_bias
                    x_g_bias=msg.gyr_x+x_g_bias
                    y_g_bias=msg.gyr_y+y_g_bias
                    z_g_bias=msg.gyr_z+z_g_bias

                    count+=1
                    if count >=1000:
                        break
            print(count)
            x_bias=(x_bias/(count*raw_count))
            y_bias=(y_bias/(count*raw_count))
            z_bias=(z_bias/(count*raw_count))
            x_g_bias=(x_g_bias/(count*GYRO_SENSITIVITY))
            y_g_bias=(y_g_bias/(count*GYRO_SENSITIVITY))
            z_g_bias=(z_g_bias/(count*GYRO_SENSITIVITY))
            print(x_bias,y_bias,z_bias,x_g_bias,y_g_bias,z_g_bias)
            with open("imu_calibration.json", "w") as f:
                json.dump({
                    "x_bias":   x_bias,
                    "y_bias":   y_bias,
                    "z_bias":   z_bias,
                    "x_g_bias": x_g_bias,
                    "y_g_bias": y_g_bias,
                    "z_g_bias": z_g_bias
                }, f, indent=4)

            # read back
            with open("imu_calibration.json", "r") as f:
                calib = json.load(f)

            print(calib["x_bias"], calib["y_bias"], calib["z_bias"])
            print(calib["x_g_bias"], calib["y_g_bias"], calib["z_g_bias"])

            # for msg,metadata in handler:
            #     if isinstance(msg,MsgImuRaw):
            #         print("linear acceleration")
            #         print(((msg.acc_x/raw_count)-x_bias)*g)
            #         print(((msg.acc_y/raw_count)-y_bias)*g)
            #         print(((msg.acc_z/raw_count)-z_bias)*g)
            #         print("angular velocity")
            #         print(((msg.gyr_x/GYRO_SENSITIVITY)-x_g_bias)*(math.pi/180))
            #         print(((msg.gyr_y/GYRO_SENSITIVITY)-y_g_bias)*(math.pi/180))
            #         print(((msg.gyr_z/GYRO_SENSITIVITY)-z_g_bias)*(math.pi/180))
            #         # # print(metadata)
            #         # print(msg)
            #         if time() - start_time >= 0.5:  # stop after 3 seconds
            #             break   

except KeyboardInterrupt:
    print("Stopped by user.")