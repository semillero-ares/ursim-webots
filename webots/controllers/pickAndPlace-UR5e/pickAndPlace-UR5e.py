"""UR5e controller."""

import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
import logging
import sys
import socket

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
CONFIG_FILE = "rtde.config.xml"
SAMPLING_FREQUENCY = 1000/TIME_STEP/10  # in Hz
HOST = "localhost"
PORT = 30004


def check_port(host, port, timeout=2):
    """
    Checks if a specific port on a host is open by attempting a TCP connection.

    Args:
        host (str): The hostname or IP address of the target.
        port (int): The port number to check.
        timeout (int): The timeout in seconds for the connection attempt.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def setup_rtde_connection():
    """Setup the RTDE connection."""
    global con, inputs
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
set_joint_positions([0, -pi/2, -pi/2, -pi/2, 0, 0])
state = None
while robot.step(TIME_STEP) != -1:
    # RTDE Data Synchronization
    if 'con' not in globals():
        if check_port(HOST, PORT):
            print("[Robot]\tAttempting to connect to URSIM...")
            setup_rtde_connection()
    else:
        try:
            state = con.receive_buffered()
            if state is not None:
                set_joint_positions(state.target_q)
                set_gripper_position(state)

        except rtde.RTDEException:
            con.disconnect()
            sys.exit()

    pass

# Enter here exit cleanup code.
con.disconnect()
