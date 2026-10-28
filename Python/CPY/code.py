import board
import time
import digitalio
import pwmio



#The pull pin is connected to PUL- on the stepper controller
pull = pwmio.PWMOut(board.D2, frequency=440, duty_cycle=65535 // 2,variable_frequency=True)


direction = digitalio.DigitalInOut(board.D3)
direction.direction = digitalio.Direction.OUTPUT
direction.value = True

ena = digitalio.DigitalInOut(board.D4)
ena.direction = digitalio.Direction.OUTPUT
ena.value = False

#PID STUFF
kp = 1
ki = 1
kd = 1

CI = 0
CD = [0,0,0]#CD is a list of the last X# of values for derivitive filtering
oldTime = 0
Feedback = 0

#Stepper info
microsteps = 400

def PID(R,Feedback, CI, CD,oldTime):
    Error = R-Feedback
    dt = time.monotonic()-oldTime
    CI = CI+Error*dt
    D = sum(CD)/len(CD)/dt
    return kp*Error+ki*CI+kd*D




while 1:

    if time.monotonic%5>2.5:
        R=0
    else:
        R=90
    
    PIDout = PID(R,Feedback,DI,DC,oldTime)

    if abs(Freq)<20:
        Freq = 20
        ena.value = False
    elif Freq<0:
        Freq = abs(Freq)
        direction.value = False
        

    pull.frequency = PIDout*microstep
    
    Feedback = Feedback+((freq/microstep)*time.monotonic-oldtime)*(Freq/abs(Freq))
    oldTime = time.monotonic
    
    





