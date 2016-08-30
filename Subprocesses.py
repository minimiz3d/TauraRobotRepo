# IN PROGRESS...
from setup import *
import Variables as v

""" SUBPROCESSES """
# Subprocess 0
def object_search():
    pole_found  = 0
    robot_found = 0

    v.belief.goal_doubt += GOAL_INCREASES_GOALDOUBT
    v.belief.ball_doubt += BALL_INCREASES_BALLDOUBT

    if v.belief.goal_doubt > GOAL_MEMORY_CYCLE:
        goal_free()

    if v.belief.ball_doubt > BALL_MEMORY_CYCLE:
        ball_free()

    # Look for some object in the field (world)
    for obj in world.objects_list:
        if obj.kind == "ball":
            if currentState == 0 or currentState == 1:
                v.ball = Ball(obj.position.r, obj.position.a)
                # return ball

        if obj.kind == "pole":
            pole_found +=1
            if pole_found == 1:
                v.pole1 = Pole(obj.position.r, obj.position.a)
                # return pole1

            if pole_found == 2:
                v.pole2 = Pole(obj.position.r, obj.position.a)
                goal_memorize()
                # return pole2


        if obj.kind == "robot":
            robot_found+=1
            if robot_found == 1:
                v.oppositeRobot = OppositeRobot(obj.position.r, obj.position.a, "black")
                # return oppositeRobot

# Subprocess 1
def ball_look_around():
    v.tauraRobot.setNeck((v.pan,v.tilt))

    if v.belief.ball_first_look == 1:
        v.belief.ball_first_look = 0
        v.pan = PAN_MIN
        v.tilt = TILT_MIN
        v.increasing_pan = 1
        v.belief.ball_look_cycle = 0
    if(v.tilt <= TILT_MAX):
        v.belief.ball_look_cycle +=1
        if v.pan < PAN_MAX and v.increasing_pan == 1:
            v.pan += PAN_STEP
        elif v.pan > PAN_MIN and v.increasing_pan == 0:
            v.pan -= PAN_STEP
        else:
            v.tilt += TILT_STEP
            v.increasing_pan = not v.increasing_pan
    else:
        v.tauraRobot.setNeck((0,0))
        turn_around()

# Subprocess 2
def turn_around():
    v.tauraRobot.setMovementVector(Point2(r=0, a=v.turn_to,phi=v.turn_to))

    if  v.belief.ball_look_cycle == 0:
        v.belief.ball_first_look = 1
        stop_to_walk()
    else:
        v.belief.ball_look_cycle -=1

# Subprocess 3
def walk_to():
    v.tauraRobot.setMovementVector(Point2(r=1,a=v.direction,phi=v.direction))

# Subprocess 4
def stop_to_walk():
    v.tauraRobot.setMovementVector(Point2())

# Subprocess 5
def opposite_goal_look_around():
    if v.belief.goal_look_cycle <= GOAL_LOOKING_CYCLE_MAX :
        if v.pan < PAN_MAX and v.increasing_pan == 1:
            v.pan += PAN_STEP
        elif v.pan > PAN_MIN and v.increasing_pan == 0:
            v.pan -= PAN_STEP
        else:
            v.increasing_pan = not v.increasing_pan
        v.tauraRobot.setNeck((v.pan,TILT_TO_LOOKING_GOAL))
        v.belief.goal_look_cycle+=1
    else:
        ball_turn_around()

# Subprocess 6
def ball_turn_around():
    v.tauraRobot.setMovementVector(Point2(r=1, a=pi/2*v.turn_to,phi=-pi/2*v.turn_to))

# Subprocess 7
def left_kick():
    v.tauraRobot.setKick( 1)

# Subprocess 8
def right_kick():
    v.tauraRobot.setKick(-1)

# Subprocess 9
def ball_memorize():
    v.belief.ball_doubt = 0
    v.belief.ball_look_cycle = 0
    v.belief.ball_first_look = 1

# Subprocess 10
def ball_free():
    v.belief.ball_doubt = BALL_MEMORY_CYCLE
    v.ball = None

# Subprocess 11
def goal_memorize():
    v.belief.goal_look_cycle = 0
    v.belief.goal_doubt = 0

    if v.pole2:
        if v.belief.ball_doubt < BALL_MEMORY_CYCLE:
            if(v.pole1.alpha + v.pole2.alpha)/2 < 0:
                v.turn_to =  1
            else:
                v.turn_to = -1
    elif v.belief.ball_doubt < BALL_MEMORY_CYCLE:
        if v.pole1.alpha < 0:
            v.turn_to =  1
        else:
            v.turn_to = -1

# Subprocess 12
def goal_free():
    v.belief.goal_doubt = GOAL_MEMORY_CYCLE
    v.pole1 = None
    v.pole2 = None

# Subprocess 12
def do_measure():
    if oppositeRobot:
        a = v.oppositeRobot.alpha
        b = v.oppositeRobot.distance
        c = v.ball.distance
        v.oppositeRobot.distance = sqrt(b*b+c*c-2*b*c*cos(a))
    else:
        v.oppositeRobot.distance = None

# Subprocess 13
def do_direction():
    # Need to determine the right distance using geometry

    if v.oppositeRobot.alpha > v.ball.distance:
        v.a_intercept = -1.5*abs(v.oppositeRobot.position.a)
    else:
        v.a_intercept =  1.5*abs(v.oppositeRobot.position.a)
