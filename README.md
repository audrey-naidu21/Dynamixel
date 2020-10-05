# Dynamixel-AX-12A

Requires an install of the [Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK) -- thank you Leon!!! I am using the Python libraries, downloaded June 19, 2020 (So, version 3.7.21), and Python 3.6.9 on Ubuntu 18.04.

I haven't tested it on anything else, but it should be pretty broadly compatible with Python 3 on any platform.

This provides complete, high-level controls in a python environment for the Dynamixel AX-12A.

I set up methods for every memory address, read any of them, write any of the writeable ones, all by name.

Notice that I have attached two AX-12A eManuals, both provided by Robotis.  The one labeled AX-12 Bioloid is obsolete -- it is actually for a different motor which predates the AX-12A, but I found it to be easier to use since it is better formatted, and not significantly different from the AX-12A.  If you are looking at the eManuals, the idea of the Dynamixel SDK and this module is to provide an interface where you don't have to understand how to assemble the packets, or know what the specific memory addresses are, or any of that.  Together, these provide a high-level object-oriented interface that allows you to not worry about all of those details.

# Documentation

I strongly recommend that you have the [Dynamixel Wizard](http://www.robotis.us/dynamixel-management/) set up on some device, and you have a physical setup with power and data hookups for one or more Dynamixels so that you can use it. For example, if you have a Dynamixel where you don't know both the ID and baud rate, you can use the Dynamixel Wizard to reset the Dynamixel firmware, and these will be reset to default values. If you are resetting the firmware, ID and/or baud rate, you should have only one Dynamixel hooked up.

This library contains one class: `AX_12A()`, and no functions.

## Class `AX_12A()`

  * [Declaring New Instances](#declaring-new-instances)
  * [Attributes](#attributes)
  * [Methods](#methods)
    * [Class Methods](#class-methods)
    * [Most Common Instance Methods](#most-common-instance-methods)
    * [All Other Instance Methods](#all-other-instance-methods)

### Declaring New Instances

Setting up a new instance of the class takes zero to four keyword arguments:
* `id`: default = `1` (matches factory default). The ID number of your smart servo. This can be set using the [Dynamixel Wizard](http://www.robotis.us/dynamixel-management/) or this library.  **If you are changing the ID of a Dynamixel, make sure you have only that one Dynamixel hooked up.**
* `baudRate`: default = `1000000` (matches factory default). This is equivalent to setting the value in the smart servo memory to 1.
* `devicePort`: default = '`/dev/ttyUSB0`'. This is the value if you are on a Linux system, and the USB-to-Serial device that you are using to connect to the Dynamixel is the first detected USB device. The last digit will change if it is not the first detected USB device; if you have multiple USB devices attached at bootup, the sequence may change unpredictably from one bootup to the next. If you are on a Windows system, this should take the form '`COM*`' and on a Mac, it will take the form '`/dev/tty.usbserial-*`'.
* `printInfo`: default = `True`. This flag determines if this library will output messages to console or not as it runs.  Note that any methods will return the appropriate value even if this is set to `False`, this only controls console output.

### Attributes

Each of the keyword arguments, above, is also an attribute for each instance.  In addition:
* `connected`: default = `False`. Set to `True` after the Dynamixel is connected (see `connect()` method below).
* Each memory address is also a constant attribute in the form `ADDR_XXX` (e.g. `ADDR_ID` or `ADDR_GOAL_POSITION)`.  I followed Leon's names as he set them up in the Dynamixel SDK, which occasionally differ slightly from the eManuals.  The complete list can be seen in the source code.

The class itself has one attribute:
* `AX_12A.instances`: default = `[]`. This is a list of all instances of the class, automatically added by the `init()` method. Notice that this means that instances could be in this list even though the associated motors have not been connected. This is intended for internal use, the method `AX_12A.listInstances()` will return this list.

## Methods

Notice that there are both instance methods and class methods. An instance method applies to a single instance of the `AX_12A` class; a class method applies to the entire class (and uses the `instances` attribute to apply to each instance).  For example:

```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
AX_12A.connectAll()
motor1.setGoalPosition(512)
motor2.setGoalPosition(512)
```

Here, `connectAll()` is a class method and `setGoalPosition()` is an instance method.

### Class Methods

  * [`listInstances()`](#listinstances)
  * [`connectAll()`](#connectall)
  * [`getAll()`](#getall)
  * [`setAll()`](#setall)
  * [`setPose()`](#setpose)
  * [`readPose()`](#readpose)
  * [`waitForMotors()`](#waitformotors)
  

#### `listInstances()`
  * Inputs: None
  * Returns: A list of AX_12A() objects.
  * Description: To get a list of all currently assigned instances of the class. Notice that each instance is added as part of the standard `init()` method, and therefore may include motors that are not yet connected.
  
Sample code:

```python
motor1 = AX_12A(id = 1)
motor1.connect()
motor2 = AX_12A(id = 2)
l = AX_12A.listInstances()
print(l)
# output should be something like: [<>,<>]
# Notice that motor1 is connected and motor2 is not, but both appear in the list, 
# with no indication of which is connected and which is not.
```

#### `connectAll()`
  * Inputs: None
  * Returns: None
  * Description: This will run the instance method [`connect()`](#connect) on each instance.
  
Sample code:

```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
AX_12A.connectAll()
# Now both motor1 and motor2 should be ready for read/write commands.
```

#### `getAll()`
  * Inputs: `method`: A string, the name of an instance method that reads from the servo memory.
  * Returns: A list, containing the values read from each servo.
  * Description: This will run the same `getXXX()` method on all instances and assemble the values in a single list.

Sample Code:

```python
motor1.AX_12A(id = 1)
motor2.AX_12A(id = 2)
AX_12A.connectAll()
positions = AX_12A.getAll('getPresentPosition')
print(positions)
# output should be something like: [ 511, 510 ]
# This output assumes both motors are very close to centered.
```

#### `setAll()`
  * Inputs:
    * `method`: A string, the name of an instance method that writes to the servo memory.
    * `value`: The value to be written to all servos
  * Return: A list, containing the value captured by each `setXXX()` method.  These should be `None` for each motor that successfully set the value as intended.
  * Description: This will run the same `{setmethod}(value)` method on each servo.
  
Sample Code:
```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
AX_12A.connectAll()
errs = AX_12A.setAll('setGoalPosition', 512)
AX_12A.waitForMotors()
print(errs)
# This should center both motors and then output: [ None, None ].
```

This is a shortcut for:
```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
motor1.connect()
motor2.connect()
errs = []
errs.append(motor1.setGoalPosition(512))
errs.append(motor2.setGoalPosition(512))
AX_12A.waitForMotors()
print(errs)
# This should center both motors and then output: [ None, None ].
```


#### `setPose()`
  * Input: List of integers, each a Goal Position for an AX-12A.  You can substitute `None` for any servo you wish to have hold its position.
  * Returns: None
  * Description: This is designed for use with a sequence of servos assembled together into a single body; this sets the body to a new 'pose' by setting the servos to new positions.  The length of the list does *not* have to be as long as the list of all servos, it will set the positions of the first *n* servos if given a list of length *n*, and leave all servos after the first *n* in their current position.  Notice that the ordering of the list depends on the order they are declared, so I strongly recommend declaring them in some order that makes sense with your construction.

Sample Code (I used this with the [PhantomX Pincher Robot Arm](https://www.trossenrobotics.com/p/PhantomX-Pincher-Robot-Arm.aspx), replacing the Arbotix controller with a linux-based microcontroller attached using a [Robotis U2D2](http://www.robotis.us/u2d2/)):

```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
motor3 = AX_12A(id = 3)
motor4 = AX_12A(id = 4)
motor5 = AX_12A(id = 5)
AX_12A.connectAll()
# Set arm to a stable rest position, with pincher open
AX_12A.setPose((512, 200, 1000, 650, 200)) # Notice double parentheses because the only argument is a list.
AX_12A.waitForMotors()
# Reach out with arm, leaving pincher open
AX_12A.setPose((None, 525, 710, 625)) # Leaves motor1 at 512 and motor5 at 200
AX_12A.waitForMotors()
# Close pincher
motor5.setGoalPosition(745)
AX_12A.waitForMotors()
# Retract arm, keeping pincher closed
AX_12A.setPose((None, 200, 1000, 650)) # Leaves motor1 at 512, and motor5 at 745
```

#### `readPose()`
  * Inputs: None
  * Returns: A list of integers, the positions of all of the declared motors.
  * Description: This is intended to simplify figuring out what the positions of the servos need to be to attain a certain position. The idea (see sample code below) would be to turn torque off on all the motors, then manually move the assembly to the desired position, and read the servo positions so that this position can be duplicated without excessive trial-and-error.

Sample Code (I used this with the [PhantomX Pincher Robot Arm](https://www.trossenrobotics.com/p/PhantomX-Pincher-Robot-Arm.aspx), replacing the Arbotix controller with a linux-based microcontroller attached using a [Robotis U2D2](http://www.robotis.us/u2d2/)):
```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
motor3 = AX_12A(id = 3)
motor4 = AX_12A(id = 4)
motor5 = AX_12A(id = 5)
AX_12A.connectAll()
# Sleep so that you have time to move your hands from the keyboard to the robotic arm
sleep(5) # imported from time in ax12a.py
# Release all the motors so you can move them manually
AX_12A.setAll('setTorqueEnable', 0) 
# Wait until the motors stop moving to read the pose
AX_12A.waitForMotors()
pose = AX_12A.readPose()
print(pose)
# If I were figuring out where the rest position was with pincher open, 
# I would get output something like: [ 510, 206, 993, 642, 211 ]
# and then round off to get values in setPose() above.
```

#### `waitForMotors()`
 * Inputs: None
 * Returns: None
 * Description: Pauses execution of the script until all of the servos stop moving. This method does not determine *why* the motors are moving, it just pauses the program until they stop moving. It will remain paused even if only one of several motors is still moving. This is important to use with any [`setGoalPosition()`](#setgoalposition) (including [`setPose()`](#setpose)). If you use two successive [`setGoalPosition()`](#segoalposition) commands with the same motor without waiting in between, the first will be wiped out by the second (see sample codes below). 

Sample Codes:
  * See [`setAll()`](#setall) above. In this script, if you had only this sample code, you wouldn't be able to see the difference whether or not you use [`waitForMotors()`](#waitformotors), except that, if you leave it out, the output would appear in the console and the script would end before the motors finished moving (assuming they had some distance to go to get to center).  This is because, once you send the command to set the new goal position, the motor will continue to move even after the script has ended as long as the motors have power.  However, if you had some other command involving these motors after the end of the sample lines, this command would overwrite the goal position before the motor completed its movement.
  * See [`setPose()`](#setpose) above. In this script, if you leave out all of the [`waitForMotors()`](#waitformotors) commands, the arm wouldn't reach at all and `motor5` would move from 200 to 745 (opening the pincher).  This is because the starting and ending positions are the same for the other four motors, and the new positions would overwrite so fast that the other four motors wouldn't get to execute the reach movement before being asked to go back to rest position.  Putting the [`waitForMotors()`](#waitformotors) in means that the motors would first complete the movement to the new pose before moving on to the next pose.
  * See [`readPose()`](#readpose) above. In this script, the [`waitForMotors()`](#waitformotors) causes the script to wait until you stop manipulating the arm before it reads the new pose.  In practice, I found, at times, that I stopped moving the arm before I intended -- the [`waitForMotors()`](#waitformotors) doesn't have any delay built in, so any pause at all in the movement will cause it to end, but then I just had to re-run the script.  
  
### Most Common Instance Methods

  * [`connect()`](#connect)
  * [`disableTorque()`](#disabletorque)
  * [`enableTorque()`](#enableTorque)
  * [`getCWAngleLimit()`](#getcwanglelimit)
  * [`getCCWAngleLimit()`](#getccwanglelimit)
  * [`getMovingSpeed()`](#getmovingspeed)
  * [`getPresentPosition()`](#getpresentposition)
  * [`getPresentSpeed()`](#getpresentspeed)
  * [`getPresentLoad()`](#getpresentload)
  * [`getPresentVoltage()`](#getpresentvoltage)
  * [`getPresentTemperature()`](#getpresenttemperature)
  * [`getMoving()`](#getmoving)
  * [`setCWAngleLimit()`](#setcwanglelimit)
  * [`setCCWAngleLimit()`](#setccwanglelimit)
  * [`setGoalPosition()`](#setgoalposition)
  * [`setID()`](#setid)
  * [`setLED()`](#setled)
  * [`setMovingSpeed()`](#setmovingspeed)

#### `connect()`
 * Inputs: None
 * Outputs: None
 * Description: Checks the connection to the motor and turns torque on; if `connect()` runs without error, then you know the motor is ready to use.  `connect()` does all of the following:
   * Checks if the motor has already been connected, using the `.connected` attribute.
   * Initializes the port and packet handlers set up by the Dynamixel SDK.
   * Sets the baud rate for communication to the motor.
   * Attempts a sample write, which enables Torque
   * Attempts a sample read
   * Checks if in Wheel Mode or Joint Mode
   * If in Joint Mode, checks if the current position is out of the designated range from CW Limit to CCW Limit; if so, moves it to the closest end of the range.
   * Set the `.connected` attribute to `True`.
   
See also the class method `connectAll()`.
   
Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
```

#### `disableTorque()`
 * Inputs: None
 * Outputs: None
 * Description: Turns torque off. This means that the servo will stop holding its position; if an external force is applied, the motor will turn, slowed only by inertia and friction. On an AX-12A, the gear inertia is quite significant if you have no leverage.  `motor.disableTorque()` is a shortcut for `motor.setTorqueEnable(0)`, mostly for readability.
 
Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
motor1.disableTorque()
```

See readPose() in Class Methods, above for why you might want to do this.

Sample Hack:

In the `readPose()` script, you could re-write the line `AX_12A.setAll('setTorqueEnable', 0)` as `AX_12A.getAll('disableTorque')` because the `getAll()` method will run any instance method that does not have an input value.  It doesn't read well, though, so I wouldn't do it.

#### `enableTorque()`
 * Inputs: None
 * Outputs: None
 * Description: Re-enables torque in a motor where it was disabled temporarily.  All motors have torque enabled as part of their `connect()` sequence, so you should only need this if you manually disabled torque.  `motor.enableTorque()` is a shortcut for `motor.setTorqueEnable(1)` mostly for readability.
 
Sample code (see readPose() above for why you might want to do this):
```python
motor1 = AX_12A(id = 1)
motor1.connect()
sleep(3) # imported from time in module
# Relax motor so it can be moved by hand
motor1.disableTorque()
# Wait until you are done moving it
AX_12A.waitForMotors()
# Hold the new position
motor1.enableTorque()
```

#### `getCWAngleLimit()`
  * Inputs: None
  * Returns: The CW Angle Limit (see Description below for what this means).
  * Description: In Joint Mode, the Dynamixel AX-12A can move within a 300 degree arc.  This arc is divided up into sections of about 0.3°, numbered 0-1023.  If you want to block your Dynamixel from being commanded to move below a certain value above 0 (for example, to avoid a collision between two body parts, or to avoid pinching a wire), then you can set a CW Angle Limit above 0.  In this case, any [`setGoalPosition()`](#setgoalposition) or [`setPose()`][#setpose) command that sends a value below that CW Angle Limit will stop at the CW Angle Limit.  Also, the [`connect()`](#connect) method will check if, on power up, if the current position is below the CW Angle Limit, and, if so, will move the Dynamixel up to the CW Angle Limit.

For example, in the [PhantomX Pincher Arm](https://www.trossenrobotics.com/p/PhantomX-Pincher-Robot-Arm.aspx), the gripper motor hits fully open at 200, and then starts to close again if it goes below that.  So, we set the CW Angle Limit for motor5 on that arm to 200.

Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
cwLimit = motor1.getCWAngleLimit()
print(cwLimit)
# By default, the output would be 0.  For motor5 in the PhantomX Pincher arm, it would be 200.
```

#### `getCCWAngleLimit()`
  * Inputs: None
  * Returns: The CCW Angle Limit
  * Description: For more information, see [`getCWAngleLimit()`](#getcwanglelimit) above.  This returns the maximum value in the 0-1023 range that the Dynamixel is allowed to move within.
  
In the [PhantomX Pincher Arm](https://www.trossenrobotics.com/p/PhantomX-Pincher-Robot-Arm.aspx), we found that the gripper was closed at 745, and that, beyond that, the connectors between the motor and the 'fingers' would start to overlap, so we set the CCW Angle Limit to 745.

Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
ccwLimit = motor1.getCCWAngleLimit()
print(ccwLimit)
# Default output would be 1023.  For motor5 in the PhantomX Pincher Arm, it would be 745.
```

#### `getMovingSpeed()`
  * Inputs: None
  * Returns: An integer, 0 - 1023, representing the *goal* moving speed of the Dynamixel.
  * Description: In Wheel Mode, this represents the speed the motor is attempting to move at right now.  In Joint Mode, this represents the speed the motor would attempt to move at if it receives a [`setGoalPosition()`](#setgoalposition) that is different from its current position.  To get the *actual* moving speed, use [`getPresentSpeed()`](#getpresentspeed).

Sample Code 1:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
# Set motor to 50% power
motor1.setMovingSpeed(512)
print(motor1.getMovingSpeed()) 
# Will output 512 even if actual speed is more/less than that.
while True:
  print(motor1.getPresentSpeed())
# Will output values very close to 512 as long as Dynamixel can spin freely.
```
  
Sample Code 2 (assuming a robot with two powered wheels):
```python
def goForward(speed):
  # Input speed as a percentage, convert to 0 - 1023
  speed = int(speed * 1023 / 100) 
  motor1.setMovingSpeed(speed)
  motor2.setMovingSpeed(speed)

def stop():
  motor1.setMovingSpeed(0)
  motor2.setMovingSpeed(0)
  
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
AX_12A.connectAll()
motor1.wheelMode()
motor2.wheelMode()
# Set motors to 50% speed
goForward(50)
sleep(1) # imported in ax12a.py
while True:
  if motor1.getMovingSpeed() - 50 > motor1.getPresentSpeed(): # If wheel on motor1 is stuck
    stop()
  if motor2.getMovingSpeed() - 50 > motor2.getPresentSpeed(): # If wheel on motor2 is stuck
    stop()
```    

#### `getPresentPosition()`
  * Inputs: None
  * Returns: An integer 0 - 1023, showing the *actual* position of the Dynamixel.
  * Description: This function will return the actual present position of the Dynamixel, assuming it is in the 300 degree range where Joint Mode is active.  I forget what happens if the Dynamixel is in Wheel Mode and is outside of that 300 degree range; I will test and update soon.
  
Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
pos = getPresentPosition()
print(pos)
# Should output something like 511 if the motor is centered.
```

#### `getPresentSpeed()`
  * Inputs: None
  * Returns: 
  * Description:
  
Sample Code:
```python
```

#### `getPresentLoad()`
  * Inputs: None
  * Returns: 
  * Description:
  
Sample Code:
```python
```

#### `getPresentVoltage()`
  * Inputs: None
  * Returns: 
  * Description:
  
Sample Code:
```python
```

#### `getPresentTemperature()`
  * Inputs: None
  * Returns: 
  * Description:
  
Sample Code:
```python
```

#### `getMoving()`
  * Inputs: None
  * Returns: 
  * Description:
  
Sample Code:
```python
```

#### `setCWAngleLimit()`
  * Inputs: One integer, the new CW Angle Limit.
  * Returns: 'None', or an error message if command fails.
  * Description: See [`getCWAngleLimit()`](#getcwanglelimit) for more information on what the CW Angle Limit is used for.  This command changes the CW Angle Limit to the new provided value.  This command modifies the EEPROM, so it includes a 0.25 second sleep to avoid corrupting the firmware.

Sample Code:
```python
motor5 = AX_12A(id = 5)
motor5.connect()
motor5.setCWAngleLimit(200)
# This sets the new CW Angle Limit to 200, as we did using the PhantomX Pincher Arm.
```

#### `setCCWAngleLimit()`
  * Inputs: One integer, the new CCW Angle Limit.
  * Returns: 'None', or an error message if command fails.
  * Description: See [`getCWAngleLimit()`](#getcwanglelimit) for more information on what the CCW Angle Limit is used for.  This command changes the CCW Angle Limit to the new provided value.  This command modifies the EEPROM, so it includes a 0.25 second sleep to avoid corrupting the firmware.


Sample Code:
```python
motor5 = AX_12A(id = 5)
motor5.connect()
motor5.setCCWAngleLimit(745)
# This sets the new CCW Angle Limit to 745, as we did using the PhantomX Pincher Arm.
```

#### `setGoalPosition()`
  * Inputs: One integer, the position that you want the servo to move to, between 0 and 1023.
  * Returns: `None`, or an error message if command fails.
  * Description: This (or its shortcut [`setPose()`](#setpose)) is the most important command when using a Dynamixel in Joint Mode.  In Joint Mode, the Dynamixel AX-12A can move within a 300 degree arc.  This arc is divided up into sections of about 0.3°, numbered 0-1023.  This command tells the Dynamixel to move to a new position in that arc.  Make sure you look at [`waitForMotors()`](#waitformotors) to see about waiting for the motor to get to its new position.
  
Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
# Rotate back and forth indefinitely
while True:
  # Move as far as possible in CW direction
  motor1.setGoalPosition(0)
  AX_12A.waitForMotors()
  # Move as far as possible in CCW direction
  motor1.setGoalPosition(1023)
  AX_12A.waitForMotors()
```

#### `setID()`
  * Inputs: One integer, the new ID value for the Dynamixel.  This must be between 0 and 253.
  * Returns: `None`, or an error message if command fails.
  * Description: Changes the ID in the EEPROM of the Dynamixel. It is strongly recommended that you have only one Dynamixel attached if you are changing its ID. This command modifies the EEPROM, so it includes a 0.25 second sleep to avoid corrupting the firmware.

Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
motor1.setID(37)
```
This would change the ID in the internal memory from 1 to 37.

#### `setLED()`
  * Inputs: 0 or 1, to turn LED off or on.
  * Returns: `None`, or an error message if command fails.
  * Description: Turns the red LED off or on.
  
Sample Code:
```python
# The Dynamixel equivalent of the Arduino sample code 'Blink'
motor1 = AX_12A(id = 1)
motor1.connect()
while True:
  motor1.setLED(1)
  sleep(1) # imported from time in module
  motor1.setLED(0)
  sleep(1)
```

#### `setMovingSpeed()`
  * Inputs: An integer, 0 - 1023.
  * Returns: `None`, or an error message if command fails.
  * Description: This is the most important command when using a Dynamixel in Wheel Mode.  Sets the Dynamixel to move at the speed set by the input value.  Also useful in Joint Mode, where it sets the speed that the motor moves when it changes to its new Goal Position.  Note that, in general, if you run the Dynamixel at lower speed, the torque should increase, so if your robot is having a hard time reaching a certain position because the load is too high, set the moving speed lower and try again.
  
**This needs to be updated for CW vs CCW motion.  The function itself may need work.

Sample Code 1 (basic goForward with two motors):
```python
motor1 = AX_12A(id = 1)
motor2 = AX_12A(id = 2)
AX_12A.connectAll()
motor1.wheelMode()
motor2.wheelMode()
motor1.setMovingSpeed(512) # 50% power
motor2.setMovingSpeed(512) # 50% power
```

Sample Code 2:
See Sample Code 2 in [`getMovingSpeed()`](#getmovingspeed), above.

#### `wheelMode()`
  * Inputs: None
  * Returns: None
  * Description: Sets the Dynamixel to Wheel Mode, where it can't accept a Goal Position, but it can spin freely, using [`setMovingSpeed`](#setmovingspeed). The Dynamixel enters Wheel Mode when both the CW and CCW Angle Limits are set to 0, so this is a shortcut that sets both of those values to 0. This command modifies the EEPROM twice, so it includes two 0.25 second sleeps to avoid corrupting the firmware.

Sample Code:
```python
motor1 = AX_12A(id = 1)
motor1.connect()
motor1.wheelMode()
motor1.setMovingSpeed(512)
# motor1 should now be spinning at 50% power.
```
