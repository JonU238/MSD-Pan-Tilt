import board
import busio
import time
from adafruit_seesaw import digitalio, rotaryio, seesaw
i2c = busio.I2C(board.SCL0, board.SDA0)
seesaw = seesaw.Seesaw(i2c, addr=0x36)
encoder = rotaryio.IncrementalEncoder(seesaw)

while 1:
    try:
        print(encoder.position)
    except Exception as e:
        print(e)
    time.sleep(0.01)


