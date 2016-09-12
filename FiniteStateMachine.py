# IN PROGRESS...
from Subprocesses import *
from setup import *
import time
import Variables as v

# States dictionary
states = {'ball_search':0, 'ball_go_after':1, 'opposite_goal_search':2, 'opposite_to_goal':3, 'kick':4, \
               'ball_intercept':5, 'drive_ball':6, 'ball_kickout':7}

currentState = v.currentState

# FSM itself
def switch(state):
    if   state == 0: currentState = ball_search()
    elif state == 1: currentState = ball_go_after()
    elif state == 2: currentState = opposite_goal_search()
    elif state == 3: currentState = opposite_to_goal()
    elif state == 4: currentState = kick()
    elif state == 5: currentState = ball_intercept()
    else:
        print("ERROR!")
    return currentState

""" STATES """
# State 0
def ball_search():
    object_search()

    if v.ball:
        do_measure()

        if v.oppositeRobot:
            if v.ball.distance > v.oppositeRobot.distance + THRESHOLD_TO_INTERCEPT:
                return states['ball_intercept']

        return states['ball_go_after']

    else:
        ball_look_around()
        return states['ball_search']

# State 1
def ball_go_after():
    object_search()

    if v.ball.distance > BALL_RADIUS:
        walk_to(v.ball.alpha)
        return states['ball_go_after']

    if v.ball.distance > 5:
        return states['opposite_goal_search']

    else:
        return states['ball_search']

# State 2
def opposite_goal_search():
    object_search()

    if v.belief.ball_doubt < BALL_MEMORY_CYCLE:
        if v.pole1 or v.pole2:
            return states['opposite_to_goal']
        else:
            opposite_goal_look_around()
            return states['opposite_goal_search']
    else:
        v.belief.goal_look_cycle = 0
        return states['ball_search']

# State 3
def opposite_to_goal():
    object_search()

    if v.belief.ball_doubt < BALL_MEMORY_CYCLE:
        if v.pole1 and v.pole2:
            if(v.pole1.alpha+v.pole2.alpha)/2>0-THRESHOLD/3 and (v.pole1.alpha+v.pole2.alpha)/2<0+THRESHOLD/3:
                return states['kick']
            ball_turn_around()

        elif v.pole1:
            if v.pole1.alpha>0-THRESHOLD/3 and v.pole1.alpha<0+THRESHOLD/3:
                return states['kick']

            ball_turn_around()

        else:
            return states['opposite_goal_search']

        return states['opposite_to_goal']

    else:
        return states['ball_search']

# State 4
def kick():
    stop_to_walk()
    v.tauraRobot.updateSimulation()
    time.sleep(0.1)

    if v.ball.alpha > 0:
        left_kick()

    else:
        right_kick()

    ball_free()
    v.tauraRobot.updateSimulation()
    time.sleep(0.1)
    return states['ball_search']

# State 5
def ball_intercept():
    object_search()

    if v.oppositeRobot.alpha > v.ball.alpha-THRESHOLD_ALIGN_BALL_TO_ROBOT and v.oppositeRobot.alpha < v.ball.alpha+THRESHOLD_ALIGN_BALL_TO_ROBOT:
        v.direction = 0
        return states['ball_go_after']
    if v.direction:
        walk_to(v.a_intercept)
        if v.direction > 4:
            v.a_intercept = 0
        v.direction+=1
    else:
        do_direction()
        v.direction = 1

    if v.belief.ball_doubt < BALL_MEMORY_CYCLE:
        return states['ball_intercept']
    else:
        v.direction = 0
        return states['ball_search']

# State 6 - IN PROGRESS.
def drive_ball():
    print ("in PROGRESS")
    # if ((v.pole1.r + v.pole2.r)/2 > v.belief.SHOT_POWER_DISTANCE)
    #
    #     # setMovementVector
    #     return 6
    #
    # if ()
    #     return 2
    # if ()
    #     return 3

# State 7 - IN PROGRESS.
def ball_kickout():
    print("IN PROGRESS")
    # (...)
