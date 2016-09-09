# IN PROGRESS...
from FiniteStateMachine import *
from setup import *
import Variables as v
import time

""" SIMULATION PARAMETERS """
INITIAL_STATE = 0
v.currentState = INITIAL_STATE
v.tauraRobot = Simulation.start()

# Simulation itself
while v.tauraRobot.updateSimulation():
    v.world = v.tauraRobot.perceiveWorld()
    v.tauraRobot.setKick(0)

    if not v.world:
        sys.exit("No world received")
        # teste(state)
    v.currentState = switch(v.currentState)

    # DEB
    #print("ball_look_cycle = ", ball_look_cycle)
    #print("goal_look_cycle = ", goal_look_cycle)
    print("state = ", v.currentState)
    # print("BALL:\n")
    print("ball_doubt = ", v.belief.ball_doubt)
    # print("ball_distance = ", v.ball.distance)
    #print("pan = ", pan)
    #print("tilt = ", tilt)
    #print("ball_doubt = ", ball_doubt)
    #print("goal_doubt = ", goal_doubt)
    #print("turn_to = ", turn_to)
    # print("robot1_dist_ball = ",robot1_dist_ball)
    # print("ball_r_last_seen = ",ball_r_last_seen)
    #print("ball_a_last_seen = ",ball_a_last_seen)
    #if robot1:
    #    print("robot1.a = ", robot1.position.a)
    #print("a_intercept = ", a_intercept)
    print("===================")
    time.sleep(0.1)
