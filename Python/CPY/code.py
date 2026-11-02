import board
import time
import digitalio
import pwmio


#Encoder code
from adafruit_seesaw import digitalio, rotaryio, seesaw
i2c = busio.I2C(board.SCL0, board.SDA0)
seesaw = seesaw.Seesaw(i2c, addr=0x36)
encoder = rotaryio.IncrementalEncoder(seesaw)


#The pull pin is connected to PUL- on the stepper controller
pull = pwmio.PWMOut(board.D2, frequency=440, duty_cycle=65535 // 2,variable_frequency=True)


direction = digitalio.DigitalInOut(board.D3)
direction.direction = digitalio.Direction.OUTPUT
direction.value = True


ena = digitalio.DigitalInOut(board.D4)
ena.direction = digitalio.Direction.OUTPUT
ena.value = False #motor default state is off


#PID Config 
kp = 1
ki = 1
kd = 1

CI = 0.0
CD = [0,0,0] #CD is a list of the last X# of values for derivitive filtering
oldTime = time.monotonic()
Feedback = 0

#Stepper info
microsteps = 400
maxSpeed = 2 #rev/s
maxFreq = microsteps*maxSpeed

def PID(R,Feedback, CI, CD,oldTime):
    Error = R-Feedback
    print("PID Error: ",Error)
    dt = time.monotonic()-oldTime
    print("PID dt: ",dt)
    CI = CI+Error*dt
    try:
        D = sum(CD)/len(CD)/dt
    except:
        D = 0
    out = kp*Error+ki*CI+kd*D
    print("PID out:",out)
    return out


a = 1.1755
b = 2.6051
c = 0.4273
d = 89.5457

while 1:
    
    R = d+(a-b)/(1+(time.monotonic()/c)^b) 
    
    PIDout = PID(R,Feedback,CI,CD,oldTime)*microsteps


    #VV Capping the max speed of the motor
    if abs(PIDout)>maxFreq:
            PIDout = maxFreq*(PIDout/abs(PIDout))

    
    if abs(PIDout)<20: #Minimum frequency setting, microsteps should be set in a way where the min frequency of like 20 hz is very slow
        enaFlag = False
    elif PIDout<0:#IF trying to tell the motor to go in reverse actually do that
        enaFlag = True
        PIDout = abs(PIDout)
        direction.value = False
    else:#else go forwards
        enaFlag = True
        direction.value = False
    
    ena.value = enaFlag #Tell the motor to turn on, IDK rn why its not just done in the if statment but perhaps past me is smart or somthing idk

    print("Feedback",Feedback,"PIDout",PIDout)

    pull.frequency = int(PIDout)

    try:
        feedbackRead = encoder.position/50
    except Exception as e:
        print(e)

    oldTime = time.monotonic()



