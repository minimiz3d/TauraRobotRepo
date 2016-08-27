from setup import *
import Variables as v

""" SIMULATION PARAMETERS """
INITIAL_STATE = 0
state = INITIAL_STATE
v.tauraRobot = Simulation.start()

# Simulation itself
while v.tauraRobot.updateSimulation():
    world = v.tauraRobot.perceiveWorld()
    v.tauraRobot.setKick(0)

    if not world:
        sys.exit("No world received")
        state = switch(state)

        # DEB
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
