# Robot overall configuration parameters
# Hans Verdolaga
# MSc Mechatronics 2023
# MC-F23 Thesis

# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
import time
import os
import numpy as np
from scipy import signal

# -----------------------------------------------------------------------------
# Configuration functions
# -----------------------------------------------------------------------------
# Function to calculate the coefficients of the low-pass filter
def dcFilterCoefficients(cutoffFreq: float, samplingFreq: float):
    # Continuous transfer function
    w0 = 2*np.pi*cutoffFreq
    num = w0 # Numerator
    den = [1, w0] # Denominator
    lowPass = signal.TransferFunction(num, den)

    # Discrete transfer function
    dt = 1/samplingFreq
    lowPassDiscrete = lowPass.to_discrete(dt,method='gbt',alpha=0.5)

    # Difference equations coefficients
    b = lowPassDiscrete.num
    a = -lowPassDiscrete.den
    
    return b, a[1:]

# -----------------------------------------------------------------------------
# High-level experiment parameters
# -----------------------------------------------------------------------------
# Timing
runTimeStart = 5 # Start time of the robot run in seconds
runTimeout = 300 # Timeout of the robot run in seconds
reconfigDelay = 0.1 # Delay between reconfiguration commands in seconds
serialTime = 0.175 # Time between serial writing in seconds
snsPrepTime = 2.5 # Time to prepare sensors and read from serial output before writing

warmupTime = 15 # Sensor warmup time in seconds
calibrateTime = 5 # Sensor nominal measurement in seconds
transferTime = 0.5 # Transfer to surge time in seconds
bufferTime = 2.5 # State buffer time in seconds

servoHopfUpdateTime = 2.0 # Time between servo hopf updates in seconds

# Sensors
sensorLeftID = 0 # ID of the left sensor for baseline setting
sensorRightID = 1 # ID of the right sensor for baseline setting
sensorMiddleID = 2 # ID of the middle sensor for baseline setting
sensorLoops = 1 # Number of samples per serial read
sensorStorageSize = 50*sensorLoops # Number of samples to store per sensor object
sensorSigMax = 2000 # Maximum signal value of the sensors in PPM
sensorThresholdValue = 200 # Ethanol detection threshold in PPM
sensorAbsenceLimit = 10 # Number of consecutive absence readings to trigger state change
sensorThresholdRange = np.min([5,sensorStorageSize]) # Horizon of samples for threshold calculation
sensorInstantRange = np.min([5,sensorStorageSize]) # Horizon of instantaneous samples
sensorDynamicRange = np.min([10,sensorStorageSize]) # Horizon of increment and decrement samples
sensorFiltering = 2 # Filtering mode for the sensors
    # 0: No filtering
    # 1: Moving average
    # 2: Butterworth filter
sensorFilterCutOff = 0.1 # Cutoff frequency for the Butterworth filter in Hz

# DC motors 
staticBraitenbergTest = False # Experiment flag for testing surge without DC motor movement
    # True: Lock in surge state
    # False: Normal operation
braitenbergBehaviour = 1 # Braitenberg behaviour mode
    # 0: Fear
    # 1: Aggression
    # 2: Love
    # 3: Exploration
braitenbergDynamic = False # Braitenberg dynamic switch
    # True: Dynamic
    # False: Simple
braitenbergTransferWeight = 0.5 # Factor to multiply to Braitenberg speed when transferring

dcRpmInit = 30 # Constant speed of the DC motor in RPM if not surging
dcRpmMax = 50 # Maximum allowable speed of the DC motor in RPM
#dcAlpha = 1 # Motor multiplier, to be scaled appropriately
dcAlpha = 1 # Scaling for tVOC
# dcAlpha = dcMaxVelocity/sensorSigMax # Motor multiplier, to be scaled appropriately
dcK = 1 # Simple Braitenberg instantaneous signal multiplier
dcKN = 0.2 # Dynamic Braitenberg instanteous signal multiplier
dcKI= 1000 # Dynamic Braitenberg increment signal multiplier
dcKD = 330 # Dynamic Braitenberg decrement signal multiplier

# Servo motors
servoAntennaeType = 1 # Antennae type
    # 0: Fixed position
    # 1: Fixed speed
    # 2: Sinusoidal speed
    # 3: Hopf oscillation
servoInitSpeed = 27.5 # Initial speed of the servo in RPM

# -----------------------------------------------------------------------------
# Calibration parameters
# -----------------------------------------------------------------------------
# Curve fitting functions
def func0(x, a, b): # Straight line
    return a*x + b

# Offset correction parameters
offsetCorrection = True # Offset correction flag in operation
sensorNominalRange = np.min([20,sensorStorageSize]) # Horizon of samples for nominal value averaging

# Symmetry measurement parameters
symTime = 120 # Time to measure sensor data for symmetry calibration in seconds
symOffsetStart = 15 # Start time to measure sensor data for offset correction in seconds
symOffsetEnd = 25 # End time to measure sensor data for offset correction in seconds
symRef = 2 # Reference sensor for symmetry calibration
symMinu = 0 # Minuend of the symmetry correction 
symSubt = 1 # Subtrahend of the symmetry correction

# Symmetry correction in state machine parameters
symCorrection = True # Symmetry correction flag in operation
symPower = 0.4 # User-defined strength of correction, scale down for extreme ref sensor values
# Usage of above: df['sensorDiff'] = df["sensor"+str(symMinu)] - df["sensor"+str(symSubt)]

# Coefficients for symmetry correction (automatically updated by running hvCalibrateSymmetry.py)
symCoeffs = [0.10623806772137356, 14.785488678025214]

# -----------------------------------------------------------------------------
# DC motor Arduino configuration parameters
# -----------------------------------------------------------------------------
# Communication parameters
#mtrSerialPort = "/dev/ttyACM0" # Serial port of the DC motor Arduino connected to the Pi
#mtrSerialPort = 'COM5' # Serial port of the DC motor Arduino connected to the Windows PC
mtrSerialNumber = '242353133363519061C0' # Serial number of the DC motor Arduino
mtrBaudRate = 38400 # Baud rate of the serial connection, must match Arduino's
mtrVerbose = 0 # Verbose mode of the Arduino
    # 0: No verbose
    # 1: Verbose

# Precision parameters
mtrSpeedPrecision = 3 # Number of digits to add to the serial velocity write
mtrConfigPrecision = 4 # Number of digits to add to serial reconfiguration

# DC motor misc parameters
ppr = 960.0 # Pulses per motor shaft revolution of the DC motor encoder
pidKP = 7.0 # PID proportional gain
pidKI = 5.0 # PID integral gain
pidKD = 0.1 # PID derivative gain

# -----------------------------------------------------------------------------
# Servo and sensor Arduino configuration parameters
# -----------------------------------------------------------------------------
# Communication parameters
#snsSerialPort = "/dev/ttyACM0" # Serial port of the servo and sensor Arduino connected to the Pi
#snsSerialPort = 'COM5' # Serial port of the servo and sensor Arduino connected to the Windows PC
snsSerialNumber = '8513831303435110C171' # Serial number of the servo and sensor Arduino
snsBaudRate = 38400 # Baud rate of the serial connection, must match Arduino's
snsVerbose = 0 # Verbose mode of the Arduino
    # 0: No verbose
    # 1: Verbose

# -----------------------------------------------------------------------------
# Pi reconfiguration parameters
# -----------------------------------------------------------------------------
# MQTT configuration
enableMQTT = True # Enable MQTT-based robot control
mqttBroker = '192.168.149.40' # IP address of the PC-side MQTT broker
mqttPort = 1883 # Port of the MQTT broker
mqttConnectTimeout = 30 # Timeout of the MQTT connection in seconds
mqttMsgTimeout = 300 # Timeout of receiving a new MQTT message in seconds
commandTopic = 'commandTopic' # Topic for the robot commands
stateTopic = 'stateTopic' # Topic for the robot state

# Directory parameters
parentFolder = os.path.dirname(__file__) + "/" + time.strftime("%Y%m%d") + "_data/" # Parent folder to organise subfolder data
expSumFileName = parentFolder + "run_summary" # Prefix of the summary file
expLogFolder = parentFolder + "experiment_logs/" # Folder for the log files
expLogFileNamePrefix = time.strftime("%Y%m%d_log_") # Prefix of the log file
cfgLogFolder = parentFolder + "config_logs/" # Folder for the experiment configuration files
cfgLogFileNamePrefix = time.strftime("%Y%m%d_cfg_") # Prefix of the log file
sensorSymmetryFolder = parentFolder + "symmetry_sensor_data/" # Folder for the symmetry sensor data
sensorBaselineFolder = parentFolder + "baseline_sensor_data/" # Folder for the baseline sensor data
sensorRawFolder = parentFolder + "raw_sensor_data/" # Folder for the sensor data
sensorRawFileNamePrefix = time.strftime("%Y%m%d_raw_") # Prefix of the signal CSV file per sensor
sensorFilteredFolder = parentFolder + "filtered_sensor_data/" # Folder for the filtered sensor data
sensorFilteredFileNamePrefix = time.strftime("%Y%m%d_filtered_") # Prefix of the filtered signal CSV file per sensor

# Communication parameters
defaultBaudRate = 38400 # Default baud rate of the serial connection

# Sensor default parameters
sensorBaselineReset = 0 # Flag to reset the sensor baseline before every run
    # 0: No baseline setting 
    # 1: Reset baseline at start of run
sensorBaselineTime = warmupTime-2 # Time to reset the sensor baseline in seconds
sensorSamplingFrequency = 6.4102564103 # Sampling frequency of coupled sensors in Hz
# sensorBaselineArray = [2533004109,2468975339,2474088992,2452592194,2572589579,2437583554,2493881124,2529269421] # Default baseline array for logging

# Baseline array for the 3 sensors (to be updated by hvCalibrate3Baseline.py)
# 2502463364,2440924975,2428409083
# 2488372928,2433584766,2433520368
# 2410121872,2349632061,2350157189
sensorBaseline3Arr = [2488372928,2433584766,2433520368]
sensorBaselineLeft = sensorBaseline3Arr[sensorLeftID] # Default left baseline
sensorBaselineRight = sensorBaseline3Arr[sensorRightID] # Default right baseline
sensorBaselineMiddle = sensorBaseline3Arr[sensorMiddleID] # Default middle baseline

# dcRightCorrection = 1.0 # Correction factor for the right DC motor
dcFilterCutoff = 15 # Cutoff frequency for the encoder filter in Hz
dcSamplingFrequency = 1000 # Sampling frequency of the DC motor encoder in Hz

# Servo default parameters
servoDefaultLeft = 2000 # Default left servo position in microseconds
servoDefaultRight = 1000 # Default right servo position in microseconds
servoMaxSpeed = 40. # Maximum loaded speed of the servo in RPM
servoFrontLeft = 1000 # Front left servo position in microseconds
servoFrontRight = 2000 # Front right servo position in microseconds
servoBackLeft = 2500 # Back left servo position in microseconds
servoBackRight = 500 # Back right servo position in microseconds
servoMidPointLeft = ((servoBackLeft + servoFrontLeft)//2) # Mid point left servo position in microseconds
servoMidPointRight = ((servoBackRight + servoFrontRight)//2) # Mid point right servo position in microseconds
servoInitAmpLeft = (abs(servoFrontLeft - servoBackLeft)//2) # Initial amplitude of the left servo in microseconds
servoInitAmpRight = (abs(servoFrontRight - servoBackRight)//2) # Initial amplitude of the right servo in microseconds