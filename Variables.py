from Classes.Belief import *
from Constants import *

# Setting up variables
pan  = PAN_MIN
tilt = TILT_MIN

increasing_pan = 1
turn_to = 1
a_intercept = 0
direction = 0

tauraRobot = None
ball = None
otherRobot = None
pole1 = None
pole2 = None
belief = Belief(BALL_MEMORY_CYCLE, 0, 1,
GOAL_MEMORY_CYCLE, 0)
