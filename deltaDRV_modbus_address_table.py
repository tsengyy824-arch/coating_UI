#!/usr/bin/env python3
"""
deltaDRV_modbus_address_table.py
Delta DRV Modbus Address Table
Structured definitions of all Modbus registers for Delta DRV robot controller
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Dict

__version__ = "1.0.0"
__author__ = "RICHIE.TSAI"


"""Servo ON/OFF Control Registers"""
class ServoControl(IntEnum):
    J5_J6_SERVO = 0x0000          # J5, J6 Servo ON/OFF
    EXTERNAL_AXIS_1_2 = 0x0001    # External AXIS 1, 2 Servo ON/OFF
    EXTERNAL_AXIS_3_4 = 0x0002    # External AXIS 3, 4 Servo ON/OFF
    J1_J2_SERVO = 0x0006          # J1, J2 Servo ON/OFF
    J3_J4_SERVO = 0x0007          # J3, J4 Servo ON/OFF
    J1_J6_SERVO = 0x0010          # J1~J6 Servo ON/OFF (0x0001=ON, 0x0002=OFF)


"""Servo Alarm Reset Registers"""
class ServoAlarmReset(IntEnum):
    J5_J6_RESET = 0x0020          # J5, J6 alarm reset
    EXTERNAL_AXIS_1_2_RESET = 0x0021  # External AXIS 1, 2 alarm reset
    EXTERNAL_AXIS_3_4_RESET = 0x0022  # External AXIS 3, 4 alarm reset
    J1_J2_RESET = 0x0026          # J1, J2 alarm reset
    J3_J4_RESET = 0x0027          # J3, J4 alarm reset
    ROBOT_GROUP_RESET = 0x0180    # Robot Group error Reset


"""Joint Position Registers (Unit: PUU - 2 registers per joint)"""
class JointPosition(IntEnum):
    J5_POSITION = 0x0080          # Robot J5 position
    J6_POSITION = 0x0082          # Robot J6 position
    EXTERNAL_AXIS_1 = 0x0084      # External AXIS 1 position
    EXTERNAL_AXIS_2 = 0x0086      # External AXIS 2 position
    EXTERNAL_AXIS_3 = 0x0088      # External AXIS 3 position
    EXTERNAL_AXIS_4 = 0x008A      # External AXIS 4 position
    J1_POSITION = 0x0098          # Robot J1 position
    J2_POSITION = 0x009A          # Robot J2 position
    J3_POSITION = 0x009C          # Robot J3 position
    J4_POSITION = 0x009E          # Robot J4 position


"""Joint Degree Position Registers (Unit: 0.001 degree - 2 registers per joint)"""
class JointDegreePosition(IntEnum):
    J1_DEGREE = 0x0168            # J1 Degree Position
    J2_DEGREE = 0x016A            # J2 Degree Position
    J3_DEGREE = 0x016C            # J3 Degree Position
    J4_DEGREE = 0x016E            # J4 Degree Position
    J5_DEGREE = 0x0150            # J5 Degree Position
    J6_DEGREE = 0x0152            # J6 Degree Position


"""Joint Velocity Registers (Unit: 0.1 rpm - 2 registers per joint)"""
class JointVelocity(IntEnum):
    J5_VELOCITY = 0x00A0          # Robot J5 velocity
    J6_VELOCITY = 0x00A2          # Robot J6 velocity
    EXTERNAL_AXIS_1_VEL = 0x00A4  # External AXIS 1 velocity
    EXTERNAL_AXIS_2_VEL = 0x00A6  # External AXIS 2 velocity
    EXTERNAL_AXIS_3_VEL = 0x00A8  # External AXIS 3 velocity
    EXTERNAL_AXIS_4_VEL = 0x00AA  # External AXIS 4 velocity
    J1_VELOCITY = 0x00B8          # Robot J1 velocity
    J2_VELOCITY = 0x00BA          # Robot J2 velocity
    J3_VELOCITY = 0x00BC          # Robot J3 velocity
    J4_VELOCITY = 0x00BE          # Robot J4 velocity


"""Joint Current Registers (Unit: 0.01% - 2 registers per joint)"""
class JointCurrent(IntEnum):
    J5_CURRENT = 0x00C0           # Robot J5 current
    J6_CURRENT = 0x00C2           # Robot J6 current
    EXTERNAL_AXIS_1_CURR = 0x00C4 # External AXIS 1 current
    EXTERNAL_AXIS_2_CURR = 0x00C6 # External AXIS 2 current
    EXTERNAL_AXIS_3_CURR = 0x00C8 # External AXIS 3 current
    EXTERNAL_AXIS_4_CURR = 0x00CA # External AXIS 4 current
    J1_CURRENT = 0x00D8           # Robot J1 current
    J2_CURRENT = 0x00DA           # Robot J2 current
    J3_CURRENT = 0x00DC           # Robot J3 current
    J4_CURRENT = 0x00DE           # Robot J4 current


"""Cartesian Position Registers (X,Y,Z in mm, RX,RY,RZ in 0.001 degree - 2 registers each)"""
class CartesianPosition(IntEnum):
    X_POSITION = 0x00F0           # Cartesian X position
    Y_POSITION = 0x00F2           # Cartesian Y position
    Z_POSITION = 0x00F4           # Cartesian Z position
    RX_POSITION = 0x00F6          # Cartesian RX rotation
    RY_POSITION = 0x00F8          # Cartesian RY rotation
    RZ_POSITION = 0x00FA          # Cartesian RZ rotation
    CARTESIAN_SPEED = 0x00FE      # Cartesian speed (mm/sec)


"""Robot Frame Information Registers"""
class RobotFrame(IntEnum):
    USER_FRAME_INDEX = 0x00E2     # Robot User Frame index (0~9)
    TOOL_FRAME_INDEX = 0x00E3     # Robot Tool Frame index (0~9)
    CARTESIAN_POSTURE = 0x00E4    # Cartesian coordinate Posture

"""Robot System Status Registers"""
class RobotStatus(IntEnum):
    MOTION_STATUS = 0x00E0        # Robot motion status (0=stopped, 1=running)
    SYSTEM_STATUS = 0x0138        # Robot System Status (0=Normal, 2=Pause, 3=Running+Pause)
    OPERATION_MODE = 0x0139       # Operation Mode (0=Not Wired, 1=T1, 2=T2, 3=Auto)
    TP_ENABLE = 0x013B            # TP Operation Enable (0=Disable, 1=Enable)
    CONTROLLER_READY = 0x0202     # Controller Ready Status

"""Joint Temperature Registers"""
class Temperature(IntEnum):
    J1_TEMP = 0x0110              # J1 Temperature
    J2_TEMP = 0x0111              # J2 Temperature
    J3_TEMP = 0x0112              # J3 Temperature
    J4_TEMP = 0x0113              # J4 Temperature
    J5_TEMP = 0x0114              # J5 Temperature
    J6_TEMP = 0x0115              # J6 Temperature

"""Error Code Registers"""
class ErrorCode(IntEnum):
    J5_ERROR = 0x0140             # Robot J5 error code
    J6_ERROR = 0x0141             # Robot J6 error code
    EXTERNAL_AXIS_1_ERROR = 0x0142 # External Axis 1 error code
    EXTERNAL_AXIS_2_ERROR = 0x0143 # External Axis 2 error code
    EXTERNAL_AXIS_3_ERROR = 0x0144 # External Axis 3 error code
    EXTERNAL_AXIS_4_ERROR = 0x0145 # External Axis 4 error code
    J1_ERROR = 0x014C             # Robot J1 error code
    J2_ERROR = 0x014D             # Robot J2 error code
    J3_ERROR = 0x014E             # Robot J3 error code
    J4_ERROR = 0x014F             # Robot J4 error code
    ROBOT_GROUP_ERROR = 0x01E0    # Robot Group error code
    CONTROLLER_ERROR = 0x01FF     # Controller error code
    ROBOT_WARNING = 0x020E        # Robot warning code

"""Robot Language Control Registers"""
class RobotLanguage(IntEnum):
    RL_STATUS = 0x0213            # RL executive status (0=Close, 1=Running, 2=Break, 3=Pause, 4=Pre-run)
    RL_EXEC_LINE = 0x0214         # RL executive line
    DYNAMIC_BREAK = 0x021E        # Dynamic break (1=OFF, 2=ON)
    RL_ID_SETTING = 0x0220        # RL ID setting (0-999)
    RL_LAST_LINE = 0x0227         # RL project last execution line
    RL_EXEC_MODE = 0x0228         # RL executive mode

"""Modbus Connection Registers"""
class ModbusConnection(IntEnum):
    CONNECTION_COUNT = 0x0232     # Modbus connection count

"""Speed Control Registers"""
class SpeedControl(IntEnum):
    SPEED_OVERRIDE = 0x0246       # Robot running speed (Unit: 0.1%)

"""Digital Input/Output Registers"""
class DigitalIO(IntEnum):
    USER_DI_MONITOR = 0x02FA      # User DI Monitor (2 registers)
    USER_DO_MONITOR = 0x02FC      # User DO Monitor (2 registers)
    USER_DO_CONTROL = 0x02FE      # User DO control On/Off (16 bit)

"""JOG Function Registers"""
class JogFunction(IntEnum):
    JOG_COMMAND = 0x0300          # JOG function command / GO command
    JOG_ACCELERATION = 0x030A     # ACC (0.01 PUU/msec2, 0.01 um/msec2)
    JOG_DECELERATION = 0x030C     # DEC (0.01 PUU/msec2, 0.01 um/msec2)
    JOG_INCH_CARTESIAN = 0x0320   # Inch JOG Cartesian displacement (um)
    JOG_INCH_JOINT = 0x0322       # Inch JOG Joint angle (PUU)
    JOG_SPEED = 0x0324            # JOG speed and GO function speed (Unit: %)

"""GO Function Registers"""
class GoFunction(IntEnum):
    IN_POSITION_FLAG = 0x031F     # GO in position flag (1=in position, 2=not reached)
    EXTERNAL_AXIS_POS = 0x032A    # GO target absolute axis position - External Axis
    JOINT_INDEX_J1_J4 = 0x032E    # GO target J1~J4 Joint index
    JOINT_INDEX_J5_J6 = 0x032F    # GO target J5~J6 Joint index
    TARGET_X = 0x0330             # GO target X / Joint J1 (Unit: um / 0.001 degree)
    TARGET_Y = 0x0332             # GO target Y / Joint J2 (Unit: um / 0.001 degree)
    TARGET_Z = 0x0334             # GO target Z / Joint J3 (Unit: um / 0.001 degree)
    TARGET_RX = 0x0336            # GO target RX / Joint J4 (Unit: 0.001 degree)
    TARGET_RY = 0x0338            # GO target RY / Joint J5 (Unit: 0.001 degree)
    TARGET_RZ = 0x033A            # GO target RZ / Joint J6 (Unit: 0.001 degree)
    TARGET_USER_FRAME = 0x033C    # GO target UserFrame
    TARGET_POSTURE = 0x033D       # GO target Posture (0-7)
    TARGET_COORD_SYSTEM = 0x033E  # GO target Coordinate system (0=MCS, 1=PCS, 2=TCS, 3=ACS)
    TARGET_TOOL_FRAME = 0x033F    # GO target ToolFrame

"""Device Buffer and Latch Data Registers"""
class DeviceBuffer(IntEnum):
    BUFFER_START = 0x1000         # Device Buffer Data start
    BUFFER_END = 0x1FFF           # Device Buffer Data end
    LATCH_START = 0x3000          # Device Latch Data start
    LATCH_END = 0x3FFF            # Device Latch Data end

"""System I/O Registers"""
class SystemIO(IntEnum):
    SYS_DI_START = 0x9800         # System DI start (8 In)
    SYS_DI_END = 0x9807           # System DI end
    SYS_DO_START = 0x9C00         # System DO start (8 Out)
    SYS_DO_END = 0x9C07           # System DO end

"""DMCNET I/O Registers"""
class DMCNetIO(IntEnum):
    DI3_START = 0x9820            # DMCNET Equipment DI3 start
    DI3_END = 0x9827              # DMCNET Equipment DI3 end
    DO3_START = 0x9C20            # DMCNET Equipment DO3 start
    DO3_END = 0x9C27              # DMCNET Equipment DO3 end


"""Servo Control Command Values"""
@dataclass
class ServoControlValues:
    J1_J6_ON: int = 0x0001        # Turn on J1~J6 servos
    J1_J6_OFF: int = 0x0002       # Turn off J1~J6 servos
    J5_J6_ON: int = 0x0101        # J5 and J6 ON
    J5_ON: int = 0x0001           # J5 ON only
    J6_ON: int = 0x0100           # J6 ON only
    ALL_OFF: int = 0x0000         # All servos OFF


"""Motion Command Values for JOG_COMMAND register"""
@dataclass
class MotionCommandValues:
    STOP: int = 1000              # Motion Stop
    MOVP: int = 301               # GO MovP (Point to Point)
    MOVL: int = 302               # GO MovL (Linear)
    MULTI_MOVEJ: int = 305        # GO MultiMoveJ
    MARCH_P: int = 306            # GO MArchP
    MARCH_L: int = 307            # GO MArchL
    # Homing commands
    HOME_XYZRZ: int = 1400        # Robot homing to mechanical origin in Z->RZ->Y->X sequence
    HOME_J1: int = 1401           # Robot J1 homing to mechanical origin
    HOME_J2: int = 1402           # Robot J2 homing to mechanical origin
    HOME_J3: int = 1403           # Robot J3 homing to mechanical origin
    HOME_J4: int = 1404           # Robot J4 homing to mechanical origin
    HOME_J1_J4: int = 1405        # Robot J1~J4 homing together


"""Robot Posture Configuration Values"""
@dataclass
class PostureValues:
    RNU: int = 0                  # Right, Non-flip, Up (bit0=0, bit1=0, bit2=0)
    LNU: int = 1                  # Left, Non-flip, Up (bit0=1, bit1=0, bit2=0)
    RND: int = 2                  # Right, Non-flip, Down (bit0=0, bit1=1, bit2=0)
    LND: int = 3                  # Left, Non-flip, Down (bit0=1, bit1=1, bit2=0)
    RHU: int = 4                  # Right, Flip, Up (bit0=0, bit1=0, bit2=1)
    LHU: int = 5                  # Left, Flip, Up (bit0=1, bit1=0, bit2=1)
    RHD: int = 6                  # Right, Flip, Down (bit0=0, bit1=1, bit2=1)
    LHD: int = 7                  # Left, Flip, Down (bit0=1, bit1=1, bit2=1)


"""Coordinate System Values"""
@dataclass
class CoordinateSystemValues:
    MCS: int = 0                  # World coordinate system (Machine Coordinate System)
    PCS: int = 1                  # User coordinate system (Part Coordinate System)
    TCS: int = 2                  # Tool coordinate system
    ACS: int = 3                  # Joint coordinate system (Axis Coordinate System)


# Instantiate value constants
SERVO_VALUES = ServoControlValues()
MOTION_COMMANDS = MotionCommandValues()
POSTURE = PostureValues()
COORD_SYSTEM = CoordinateSystemValues()


# Helper dictionaries for lookups
JOINT_DEGREE_ADDRESSES: Dict[str, int] = {
    'J1': JointDegreePosition.J1_DEGREE,
    'J2': JointDegreePosition.J2_DEGREE,
    'J3': JointDegreePosition.J3_DEGREE,
    'J4': JointDegreePosition.J4_DEGREE,
    'J5': JointDegreePosition.J5_DEGREE,
    'J6': JointDegreePosition.J6_DEGREE,
}

JOINT_VELOCITY_ADDRESSES: Dict[str, int] = {
    'J1': JointVelocity.J1_VELOCITY,
    'J2': JointVelocity.J2_VELOCITY,
    'J3': JointVelocity.J3_VELOCITY,
    'J4': JointVelocity.J4_VELOCITY,
    'J5': JointVelocity.J5_VELOCITY,
    'J6': JointVelocity.J6_VELOCITY,
}

CARTESIAN_ADDRESSES: Dict[str, int] = {
    'X': CartesianPosition.X_POSITION,
    'Y': CartesianPosition.Y_POSITION,
    'Z': CartesianPosition.Z_POSITION,
    'RX': CartesianPosition.RX_POSITION,
    'RY': CartesianPosition.RY_POSITION,
    'RZ': CartesianPosition.RZ_POSITION,
}


if __name__ == "__main__":
    # Test and display address table
    print("Delta DRV Modbus Address Table")
    print("=" * 60)

    print("\n=== Servo Control ===")
    print(f"J1~J6 Servo: {hex(ServoControl.J1_J6_SERVO)} (ON={hex(SERVO_VALUES.J1_J6_ON)}, OFF={hex(SERVO_VALUES.J1_J6_OFF)})")

    print("\n=== Motion Commands ===")
    print(f"MOVP (P2P): {MOTION_COMMANDS.MOVP}")
    print(f"MOVL (Linear): {MOTION_COMMANDS.MOVL}")
    print(f"STOP: {MOTION_COMMANDS.STOP}")

    print("\n=== Joint Degree Positions ===")
    for joint, addr in JOINT_DEGREE_ADDRESSES.items():
        print(f"{joint}: {hex(addr)}")

    print("\n=== Cartesian Positions ===")
    for axis, addr in CARTESIAN_ADDRESSES.items():
        print(f"{axis}: {hex(addr)}")

    print("\n=== Robot Status ===")
    print(f"Motion Status: {hex(RobotStatus.MOTION_STATUS)}")
    print(f"System Status: {hex(RobotStatus.SYSTEM_STATUS)}")
    print(f"Controller Ready: {hex(RobotStatus.CONTROLLER_READY)}")

    print("\n=== Error Codes ===")
    print(f"Robot Group Error: {hex(ErrorCode.ROBOT_GROUP_ERROR)}")
    print(f"Controller Error: {hex(ErrorCode.CONTROLLER_ERROR)}")
    print(f"Robot Warning: {hex(ErrorCode.ROBOT_WARNING)}")
