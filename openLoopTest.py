import time
import math
inittime = time.monotonic()
msteps = 2
degperstep = 1.8
thetaddm = 10 #rad/s/s

theta0 = 0
thetaf = 10
thetaf = thetaf-thetaf%(degperstep/msteps)

print(thetaf)

numStep = ((thetaf-theta0)/degperstep)*msteps
print(numStep)

thetadd = thetaddm
thetad = 0
theta = 0
tn = time.monotonic()

period = (degperstep/msteps)

for i in range(numStep):

    print("step")

    