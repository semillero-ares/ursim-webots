"""pickAndPlace controller."""

import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
import logging
import sys
import socket

from controller import Supervisor

print("[Factory]\tInitiating the controller...")

# Webots Simulator Configuration ##############################################
simulator = Supervisor()

TIME_STEP = int(simulator.getBasicTimeStep())

rootNode = simulator.getRoot()  # get root of the scene tree
rootChildrenField = rootNode.getField('children')

pieceCounter = 0
pieceList = []
boxCounter = 0
boxList = []


def createWorkpiece(id):
    rootChildrenField.importMFNodeFromString(-1, f'''
DEF PIECE_{id} Solid {{
    children [ USE PIECE ]
    boundingObject USE PIECE
    name "piece-{id}"
    physics Physics {{
        density -1
        mass 1
    }}
}}
''')
    pieceNode = simulator.getFromDef(f'PIECE_{id}')
    pieceNode.getField('translation').setSFVec3f([2.2, 0, 0.8])
    pieceList.append(pieceNode)


def createBox(id):
    rootChildrenField.importMFNodeFromString(-1, f'''
DEF BOX_{id} Solid {{
    children [ USE BOX ]
    boundingObject USE BOX
    name "box-{id}"
    physics Physics {{
        density -1
        mass 1
    }}
}}
''')
    boxNode = simulator.getFromDef(f'BOX_{id}')
    boxNode.getField('translation').setSFVec3f([-0.6, -1.0, 0.71])
    boxList.append(boxNode)


def updateWorkpiece():
    global pieceCounter, pieceList
    if pieceList == []:
        pieceCounter += 1
        createWorkpiece(pieceCounter)
    lastPiece = pieceList[-1]
    x, _, _ = lastPiece.getField('translation').getSFVec3f()
    name = lastPiece.getField('name').getSFString()
    piece_id = name.split('-')[-1]
    # Spawn a new piece if the last one has moved enough
    if x < 1.5 and piece_id == str(pieceCounter):
        pieceCounter += 1
        createWorkpiece(pieceCounter)
    # Remove pieces that are out of bounds
    for piece in pieceList:
        x, y, z = piece.getField('translation').getSFVec3f()
        if z < 0.5 or (x < 0.0 and y > 2.0):
            piece.remove()
            pieceList.remove(piece)
    pass


def updateBox():
    global boxCounter, boxList
    if boxList == []:
        boxCounter += 1
        createBox(boxCounter)
    lastBox = boxList[-1]
    _, y, _ = lastBox.getField('translation').getSFVec3f()
    name = lastBox.getField('name').getSFString()
    box_id = name.split('-')[-1]
    if y > -0.1 and box_id == str(boxCounter):
        boxCounter += 1
        createBox(boxCounter)
    # print(f"[Factory]\tLast box: {box_id} at y={y:.2f}")
    for box in boxList:
        _, y, _ = box.getField('translation').getSFVec3f()
        if y > 2:
            box.remove()
            boxList.remove(box)
            # print(f"[Factory]\tRemoved box: {name} at y={y:.2f}")
    pass


laser_infeed = simulator.getDevice('laser_infeed')
laser_infeed.enable(TIME_STEP)

laser_outfeed = simulator.getDevice('laser_outfeed')
laser_outfeed.enable(TIME_STEP)

motor_infeed = simulator.getDevice('motor_infeed')
motor_infeed.setPosition(float('inf'))  # Set to infinite position control
motor_infeed.setVelocity(0.0)
motor_outfeed = simulator.getDevice('motor_outfeed')
motor_outfeed.setPosition(float('inf'))  # Set to infinite position control
motor_outfeed.setVelocity(0.0)


def set_conveyors_speed(state):
    """Set the speed of the conveyors."""
    global motor_infeed, motor_outfeed
    types = format(state.analog_io_types, "#04b")
    scalar_infeed = 10.0 if types[-3] == '1' else 4.0
    scalar_outfeed = 10.0 if types[-4] == '1' else 4.0
    speed_infeed = state.standard_analog_output0 / scalar_infeed
    speed_outfeed = state.standard_analog_output1 / scalar_outfeed
    activate_infeed = int(
        format(state.actual_digital_output_bits, '#020b')[-1])
    activate_outfeed = int(
        format(state.actual_digital_output_bits, '#020b')[-2])
    motor_infeed.setVelocity(0.5 * speed_infeed * activate_infeed)
    motor_outfeed.setVelocity(0.5 * speed_outfeed * activate_outfeed)


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
    """
    Initialize and start an RTDE session with a Universal Robots controller.
    This function:
    - Loads the RTDE configuration from CONFIG_FILE and extracts the "in" and "out"
        recipes (names and types).
    - Creates an RTDE client targeting HOST:PORT and retries connection until it
        succeeds (blocking loop).
    - Queries the controller version to complete the handshake.
    - Configures the input package used to send data to the robot and resets
        input_bit_register_64 and input_bit_register_65 to 0.
    - Configures the output recipe at the specified SAMPLING_FREQUENCY and starts
        RTDE synchronization.
    Side effects:
    - Establishes a TCP connection to the robot controller.
    - Initializes and assigns the global variables `con` (RTDE client) and `inputs`
        (input package).
    - Writes to the controller’s input bit registers 64 and 65.
    - Emits log/print messages.
    Uses:
    - Module-level constants: CONFIG_FILE, HOST, PORT, SAMPLING_FREQUENCY.
    - External libraries: `rtde`, `rtde_config`, `logging`, `sys`.
    Returns:
    - None
    Raises:
    - SystemExit: If input/output configuration or RTDE synchronization cannot be started.
    Notes:
    - The connection phase retries indefinitely; if the controller is unreachable,
        this function will block until a connection is established.
    """

    global con, inputs
    conf = rtde_config.ConfigFile(CONFIG_FILE)
    output_names, output_types = conf.get_recipe("out")
    input_names, input_types = conf.get_recipe("in")
    con = rtde.RTDE(HOST, PORT)
    # Trying to connect to UR5e robot controller
    connected = False
    while not connected:
        try:
            con.connect()
            connected = True
            print("[Factory]\tConnection established with URSIM.")
            simulator.setLabel(1, "pickAndPlace.wbt", 0.0,
                               0.0, 0.12, 0xffffff, 0, 'Arial')
        except:
            print("[Factory]\tConnection failed, retrying...")
            simulator.setLabel(1, "Error: Fallo la conexión\nReintentando...", 0.0,
                               0.0, 0.12, 0xff0000, 0, 'Arial')
            pass
    con.get_controller_version()
    inputs = con.send_input_setup(input_names, input_types)
    if not inputs:
        logging.error("Unable to configure input")
        sys.exit()

    inputs.input_bit_register_64 = 0  # Reset input bit register 64
    inputs.input_bit_register_65 = 0  # Reset input bit register 65

    if not con.send_output_setup(output_names, output_types, frequency=SAMPLING_FREQUENCY):
        logging.error("Unable to configure output")
        sys.exit()
    if not con.send_start():
        logging.error("Unable to start synchronization")
        sys.exit()


# simulator.setLabel(0, "pickAndPlace.wbt", 0.0,
#                    0.95, 0.10, 0xffffff, 0, 'Arial')

while simulator.step(TIME_STEP) != -1:

    updateWorkpiece()
    updateBox()

    laser_infeed_value = laser_infeed.getValue()
    laser_outfeed_value = laser_outfeed.getValue()

    if 'con' not in globals():
        if check_port(HOST, PORT):
            print("[Factory]\tAttempting to connect to URSIM...")
            setup_rtde_connection()
            continue
        else:
            simulator.setLabel(1, "Error: Sin conexion\nActivar contenedor URSIM", 0.0,
                               0.0, 0.12, 0xff0000, 0, 'Arial')
            continue
    else:
        try:

            inputs.input_bit_register_64 = int(laser_infeed_value < 100.0)
            inputs.input_bit_register_65 = int(laser_outfeed_value < 100.0)
            con.send(inputs)

            state = con.receive_buffered()
            if state is not None:
                set_conveyors_speed(state)
                pass

        except rtde.RTDEException:
            con.disconnect()
            sys.exit()

    pass

# Graceful disconnection
con.disconnect()
