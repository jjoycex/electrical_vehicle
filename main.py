from pololu_3pi_2040_robot import robot
from gyro import Gyro
from timer import Timer
from displayer import Displayer

#initalizing variables
button_a = robot.ButtonA()
button_b = robot.ButtonB()
button_c = robot.ButtonC()
displayer: Displayer = Displayer() #display pannel 
gyro: Gyro = Gyro(displayer) 
timer: Timer = Timer(gyro) #keep checking gyro 
MOTOR_SPEED_LEFT=2000
MOTOR_SPEED_RIGHT=2026
encoders = robot.Encoders() # 0.0287cm/count 
motors = robot.Motors()
distance_to_gate = 313.21  #cm CHANGE
angle_to_gate = 16.7 # degree CHANGE

def left(target_angle)
  current_angle = gyro.degree()
  motors.set_speeds(0, MOTOR_SPEED_RIGHT)
  while current_angle < target_angle
    current_angle = gyro.degree()

  motors.off()
  timer.sleep_ms(500)

def right(target_angle)
  current_angle = gyro.degree()
  motors.set_speeds(MOTOR_SPEED_LEFT, 0)
  while current_angle > target_angle
    current_angle = gyro.degree()

  motors.off()
  timer.sleep_ms(500)
  
def drive(distance, target_angle): #move certain distance at certain angle 
  target_count = distance / 0.0287 
  right_adjusted = 0
  encoders.get_counts(reset = True)
  count = 0
  while count < target_count:
    motors.set_speeds(MOTOR_SPEED_LEFT, MOTOR_SPEED_RIGHT + right_adjusted) # if the gyro sensor is not right , correct it.
    angle = gyro.degree()
    if angle < target_angle - 0.25:
      right_adjusted = 50
    elif angle > target_angle + 0.25:
      right_adjusted = -50
    else:
      right_adjusted = 0

    counts = encoders.get_counts()
    count = (counts[0] + counts[1]) / 2

  motors.off()
  timer.sleep_ms(500)

displayer.show("Press A to start...")

while True:
    if button_a.check() == True:
      timer.sleep_ms(500)
      displayer.show("start driving ...")
      ############
      left(angle_to_gate)
      drive(distance_to_gate, angle_to_gate)
      right(0)
      drive(100, 0)
      right(-angle_to_gate)
      drive(distance_to_gate, -angle_to_gate)

    gyro.degree()

# This for 7m distance with 20cm wide gate.
# 1. travel at 16.7 degree for 313.21 cm. 
# 2. turn degree -16.7, so that we are at degree 0.
# 3. travel at 0 degree for 100cm.
# 4. turn degree -16.7, so that we aim to the target.
# 5. travel at -16.7 degreee for 313.21cm
#
#        0
#        |
# (+)    |    (-)
#        |
# turning of gyro system, don't forget sweetie!!!! :DD
