import board
import time
import digitalio
import pwmio




def play(note,pull):
    ena.value = True
    pull.frequency = note
    time.sleep(0.5)
    ena.value = False
    time.sleep(0.1)


#The pull pin is connected to PUL- on the stepper controller
pull = pwmio.PWMOut(board.D2, frequency=440, duty_cycle=65535 // 2,variable_frequency=True)


direction = digitalio.DigitalInOut(board.D3)
direction.direction = digitalio.Direction.OUTPUT
direction.value = True

ena = digitalio.DigitalInOut(board.D4)
ena.direction = digitalio.Direction.OUTPUT
ena.value = True

notes = [294,329,349,392,440,493,523]
sequince = [3,2,1,2,3,3,3,2,2,2,3,3,3,3,2,1,2,3,3,3,3,2,2,3,2,1]
sequince = [4,3,2,3,4,4,4,3,3,3,4,4,4,4,3,2,3,4,4,4,4,3,3,4,3,2]

for i in sequince:
    play(notes[i],pull)



