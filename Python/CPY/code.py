import board
import time
import digitalio
import pwmio
import busio
import math

#Encoder code
from adafruit_seesaw import rotaryio, seesaw
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
kp = 0.07
ki = 0.07
kd = 0.02

CI = 0.0
CD = [0,0,0] #CD is a list of the last X# of values for derivitive filtering
oldTime = time.monotonic()
Feedback = 0

#Stepper info
microsteps = 400
maxSpeed = 1 #rev/s
maxFreq = microsteps*maxSpeed

def PID(R,Feedback, CI, CD,oldTime):
    Error = R-Feedback
    dt = time.monotonic()-oldTime
    CI = CI+Error*dt
    try:
        D = sum(CD)/len(CD)/dt
    except:
        D = 0
    out = kp*Error+ki*CI+kd*D
    return out


a = 0.8782
b = 2.6051
c = 0.4273
d = 89.5457
ti = time.monotonic()


while time.monotonic()-ti<10:
    #R =  d+(a-d)/(1+((time.monotonic()-ti)/c)**b)  
    #R = 100
    R = 90*math.sin(2*(time.monotonic()-ti))

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
        direction.value = True

    ena.value = enaFlag #Tell the motor to turn on, IDK rn why its not just done in the if statment but perhaps past me is smart or somthing idk
    if enaFlag:
        pull.frequency = int(PIDout)

    oldTime = time.monotonic()


    try:
        feedbackRead = encoder.position/1.23
    except:
        pass
    Feedback = feedbackRead
    print("TFOR\t",time.monotonic()-ti ,"\t",Feedback,"\t",int(PIDout),"\t",R)

ena.value = False
