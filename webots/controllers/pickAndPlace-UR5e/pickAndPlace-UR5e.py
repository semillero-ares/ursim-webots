"""UR5e controller."""

import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
import logging
import sys

from controller import Robot
from numpy import pi

print("[Robot]\tInitiating the controller...")

# Webots Robot Configuration ##############################################
robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

joints = [
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint"
]

motors = []
for joint in joints:
    motor = robot.getDevice(joint)
    motor.setPosition(0.0)  # Set to infinite position control
    motors.append(motor)


def set_joint_positions(positions):
    """Set the positions of the SCARA robot joints."""
    global motors
    for motor, position in zip(motors, positions):
        motor.setPosition(position)


gripper = robot.getDevice('gripper::left finger joint')
gripper.setPosition(0.0)  # Set to infinite position control


def set_gripper_position(state):
    """Set the position of the gripper."""
    global gripper
    position = int(format(state.actual_digital_output_bits, '#020b')[3])
    gripper.setPosition(0.8*position)


# RTDE Configuration ###############################################################
CONFIG_FILE = "rtde-config.xml"
SAMPLING_FREQUENCY = 1000/TIME_STEP/10  # in Hz
HOST = "localhost"
PORT = 30004

conf = rtde_config.ConfigFile(CONFIG_FILE)
output_names, output_types = conf.get_recipe("out")
con = rtde.RTDE(HOST, PORT)
connected = False
while not connected:
    try:
        con.connect()
        connected = True
        print("[Robot]\tConnection established with URSIM.")
    except:
        print("[Robot]\tConnection failed, retrying...")
        pass
con.get_controller_version()
if not con.send_output_setup(output_names, output_types, frequency=SAMPLING_FREQUENCY):
    logging.error("Unable to configure output")
    sys.exit()
if not con.send_start():
    logging.error("Unable to start synchronization")
    sys.exit()


# Main loop:
# - perform simulation steps until Webots is stopping the controller
state = None
while robot.step(TIME_STEP) != -1:
    # RTDE Data Synchronization
    try:
        state = con.receive_buffered()
        if state is not None:
            set_joint_positions(state.target_q)
            set_gripper_position(state)
            # print("Robot pose: {}".format(state.actual_q))
            pass

    except rtde.RTDEException:
        con.disconnect()
        sys.exit()

    pass

# Enter here exit cleanup code.
con.disconnect()
