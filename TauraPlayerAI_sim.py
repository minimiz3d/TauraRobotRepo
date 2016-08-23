from TauraFSM import *

from MindInterface import Simulation
from MindInterface.config import *

from Classes.Ball import *
from Classes.OtherRobot import *
from Classes.Pole import *

from Constants import *

""" VARIABLES """
pan  = PAN_MIN
tilt = TILT_MIN
increasing_pan = 1

turn_to = 1
a_intercept = 0
direction = 0

""" SIMULATION PARAMETERS """
INITIAL_STATE = 0
state = INITIAL_STATE

# Initialize the TauraRobot and other objects in the simulation
ball = Ball(20, 1, 1, 1)
otherRobot = OtherRobot(1, 25, "blue")
pole1 = Pole(1, 30, True, True, True)
pole2 = Pole(1, 33, True, True, True)

robot = Simulation.start()
tauraPlayerFSM = TauraFSM(state, ball, otherRobot, pole1, pole2, robot)

# Simulation itself
while robot.updateSimulation():
    world = robot.perceiveWorld()
    robot.setKick(0)

    if not world:
        sys.exit("No world received")
        state = tauraPlayerFSM.switch(state)

        # DEBUGG
        #print("ball_look_cycle = ", ball_look_cycle)
        #print("goal_look_cycle = ", goal_look_cycle)
        print("state = ", state)
        #print("pan = ", pan)
        #print("tilt = ", tilt)
        #print("ball_doubt = ", ball_doubt)
        #print("goal_doubt = ", goal_doubt)
        #print("turn_to = ", turn_to)
        print("robot1_dist_ball = ",robot1_dist_ball)
        print("ball_r_last_seen = ",ball_r_last_seen)
        #print("ball_a_last_seen = ",ball_a_last_seen)
        #if robot1:
        #    print("robot1.a = ", robot1.position.a)
        #print("a_intercept = ", a_intercept)
        print("===================")
        time.sleep(0.1)






# # Ball Memories
# ball_a_last_seen = 0
# ball_r_last_seen = 0
# ball_doubt = BALL_MEMORY_CYCLE
# ball_look_cycle = 0
# ball_first_look = 1
#
# # Goal Memories
# pole1_a_last_seen = 0
# pole1_r_last_seen = 0
# pole2_a_last_seen = 0
# pole2_r_last_seen = 0
# goal_doubt = GOAL_MEMORY_CYCLE
# goal_look_cycle = 0
#
#
# ball  = None
# pole1 = None
# pole2 = None
# robot1 = None
# robot1_dist_ball = None
