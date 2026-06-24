from roboclaw_3 import Roboclaw
from time import sleep 
try:
    print("Initializing RoboClaw...")
    roboclaw = Roboclaw("/dev/ttyUSB0", 38400)
    
    print("Opening connection...")
    roboclaw.Open()
    
    
    print("Sending command to motor...")
    # roboclaw.ForwardM1(0x80, 63)
    # motor_1_count = roboclaw.ReadEncM1(0x80)
    print ("Original:")
    # print (motor_1_count)

    # sleep(1)

except FileNotFoundError:
    print("❌ Serial port not found (expected - hardware not connected)")