from Classes.Ball import *
from Classes.OtherRobot import *
from Classes.Pole import *
from Classes.Belief import *

from Constants import *

from MindInterface import Simulation
from MindInterface.config import *

class TauraFSM:
    """ """

    # Default arguments
    def __init__(self, belief, currentState, tauraRobot):
        self.belief = belief
        self.currentState = currentState
        self.tauraRobot = tauraRobot
        self.ball = None
        self.otherRobot = None
        self.pole1 = None
        self.pole2 = None

    # FSM itself
    def switch(self, state):
        if   state == 0: self.currentState = self.ball_search()
        elif state == 1: self.currentState = self.ball_go_after()
        elif state == 2: self.currentState = self.opposite_goal_search()
        elif state == 3: self.currentState = self.opposite_to_goal()
        elif state == 4: self.currentState = self.kick()
        elif state == 5: self.currentState = self.ball_intercept()
        else:
            print("ERROR!")
        return self.currentState

    """ STATES """
    # State 0
    def ball_search(self):
        self.object_search()

        if self.ball:
            self.do_measure()

            if self.otherRobot.distance:
                if self.ball.distance > self.otherRobot.distance + THRESHOLD_TO_INTERCEPT:
                    return 5

            return 1

        else:
            self.ball_look_around()
            return 0

    # State 1
    def ball_go_after(self):
        self.object_search()

        if self.ball.distance > BALL_RADIUS:
            walk_to(self.ball.distance)
            return 1

        if self.ball.distance > 5:
            return 2

        else:
            return 0

    # State 2
    def opposite_goal_search(self):
        self.object_search()

        if self.belief.ball_doubt < BALL_MEMORY_CYCLE:
            if self.pole1 or self.pole2:
                return 3
            else:
                self.opposite_goal_look_around()
                return 2
        else:
            self.belief.goal_look_cycle = 0
            return 0

    # State 3
    def opposite_to_goal(self):
        self.object_search()

        if self.belief.ball_doubt < BALL_MEMORY_CYCLE:
            if self.pole1 and self.pole2:
                if(self.pole1.alpha+self.pole2.alpha)/2>0-THRESHOLD/3 and (self.pole1.alpha+self.pole2.alpha)/2<0+THRESHOLD/3:
                    return 4
                self.ball_turn_around()

            elif self.pole1:
                if self.pole1.alpha>0-THRESHOLD/3 and self.pole1.alpha<0+THRESHOLD/3:
                    return 4

                self.ball_turn_around()

            else:
                return 2

            return 3

        else:
            return 0

    # State 4
    def kick(self):
        self.stop_to_walk()
        self.tauraRobot.updateSimulation()
        time.sleep(0.1)

        if self.belief.ball_a_last_seen > 0:
            self.left_kick()

        else:
            self.right_kick()

        self.ball_free()
        self.tauraRobot.updateSimulation()
        time.sleep(0.1)
        return 0

    # State 5
    def ball_intercept(self):
        # from TauraPlayerAI_sim import direction, a_intercept ???
        self.object_search()

        if self.otherRobot.alpha > self.ball.alpha-THRESHOLD_ALIGN_BALL_TO_ROBOT and otherRobot.alpha < self.ball.alpha+THRESHOLD_ALIGN_BALL_TO_ROBOT:
            self.direction = 0
            return 1
        if direction:
            self.walk_to(self.a_intercept)
            if direction > 4:
                self.a_intercept = 0
            self.direction+=1
        else:
            self.do_direction()
            direction = 1

        if self.belief.ball_doubt < BALL_MEMORY_CYCLE:
            return 5
        else:
            direction = 0
            return 0

    # State 6 - IN PROGRESS.
    def drive_ball(self):
        if ((self.pole1.r + self.pole2.r)/2 > self.belief.SHOT_POWER_DISTANCE)

            setMovementVector
            return 6

        if ()
            return 2
        if ()
            return 3



    """ SUBPROCESSES """
    # Subprocess 0
    def object_search(self):
        pole_found  = 0
        robot_found = 0

        self.belief.goal_doubt += GOAL_INCREASES_GOALDOUBT
        self.belief.ball_doubt += BALL_INCREASES_BALLDOUBT

        # Look for some object in the field (world)
        for obj in world.objects_list:
            if obj.kind == "ball":
                if self.currentState == 0 or self.currentState == 1:
                    self.ball = Ball(obj.position.r, obj.position.a)

            if obj.kind == "pole":
                pole_found +=1
                if pole_found == 1:
                    self.pole1 = Pole(obj.position.r, obj.position.a)
                if pole_found == 2:
                    self.pole2 = Pole(obj.position.r, obj.position.a)
                self.goal_memorize()

            if obj.kind == "robot":
                robot_found+=1
                if robot_found == 1:
                    self.otherRobot = OtherRobot(obj.position.r, obj.position.a, "black")

        if self.belief.goal_doubt > GOAL_MEMORY_CYCLE:
            self.goal_free()
        if self.belief.ball_doubt > BALL_MEMORY_CYCLE:
            self.ball_free()

    # Subprocess 1
    def ball_look_around(self):
        # global ball_first_look
        # global TILT_MIN
        # global TILT_MAX
        # global PAN_MIN
        # global PAN_MAX
        # global TILT_STEP
        # global PAN_STEP
        # global ball_look_cycle
        # global increasing_pan
        # global pan
        # global tilt

        self.tauraRobot.setNeck((pan,tilt))
        if self.belief.ball_first_look == 1:
            self.belief.ball_first_look = 0
            pan = PAN_MIN
            tilt = TILT_MIN
            increasing_pan = 1
            self.belief.ball_look_cycle = 0
        if(tilt <= TILT_MAX):
            self.belief.ball_look_cycle +=1
            if pan < PAN_MAX and increasing_pan == 1:
                pan += PAN_STEP
            elif pan > PAN_MIN and increasing_pan == 0:
                pan -= PAN_STEP
            else:
                tilt += TILT_STEP
                increasing_pan = not increasing_pan
        else:
            self.tauraRobot.setNeck((0,0))
            self.turn_around()

    # Subprocess 2
    def turn_around(self):
        self.tauraRobot.setMovementVector(Point2(r=0, a=turn_to,phi=turn_to))

        if  self.belief.ball_look_cycle == 0:
            self.belief.ball_first_look = 1
            self.stop_to_walk()
        else:
            self.belief.ball_look_cycle -=1

    # Subprocess 3
    def walk_to(direction):
        self.tauraRobot.setMovementVector(Point2(r=1,a=direction,phi=direction))

    # Subprocess 4
    def stop_to_walk(self):
        self.tauraRobot.setMovementVector(Point2())

    # Subprocess 5
    def opposite_goal_look_around(self):
        if self.belief.goal_look_cycle <= GOAL_LOOKING_CYCLE_MAX :
            if pan < PAN_MAX and increasing_pan == 1:
                pan += PAN_STEP
            elif pan > PAN_MIN and increasing_pan == 0:
                pan -= PAN_STEP
            else:
                increasing_pan = not increasing_pan
            self.tauraRobot.setNeck((pan,TILT_TO_LOOKING_GOAL))
            self.belief.goal_look_cycle+=1
        else:
            self.ball_turn_around()

    # Subprocess 6
    def ball_turn_around(self):
        self.tauraRobot.setMovementVector(Point2(r=1, a=pi/2*turn_to,phi=-pi/2*turn_to))

    # Subprocess 7
    def left_kick(self):
        self.tauraRobot.setKick( 1)

    # Subprocess 8
    def right_kick(self):
        self.tauraRobot.setKick(-1)

    # Subprocess 9
    def ball_memorize(self):
        self.belief.ball_doubt = 0
        self.belief.ball_look_cycle = 0
        self.belief.ball_first_look = 1

    # Subprocess 10
    def ball_free(self):
        self.belief.ball_doubt = BALL_MEMORY_CYCLE
        self.ball = None

    # Subprocess 11
    def goal_memorize(self):
        self.belief.goal_look_cycle = 0
        self.belief.goal_doubt = 0

        if self.pole2:
            if self.belief.ball_doubt < BALL_MEMORY_CYCLE:
                if(self.pole1.alpha + self.pole2.alpha)/2 < 0:
                    turn_to =  1
                else:
                    turn_to = -1
        elif self.belief.ball_doubt < BALL_MEMORY_CYCLE:
            if self.pole1.alpha < 0:
                turn_to =  1
            else:
                turn_to = -1

    # Subprocess 12
    def goal_free(self):
        self.belief.goal_doubt = GOAL_MEMORY_CYCLE
        self.pole1 = None
        self.pole2 = None

    # Subprocess 12
    def do_measure(self):
        if otherRobot:
            a = self.otherRobot.alpha
            b = self.otherRobot.distance
            c = self.ball.distance
            self.otherRobot.distance = sqrt(b*b+c*c-2*b*c*cos(a))
        else:
            self.otherRobot.distance = None

    # Subprocess 13
    def do_direction(self):
        global a_intercept

        # Need to determine the right distance using geometry

        if self.otherRobot.alpha > self.ball.distance:
            a_intercept = -1.5*abs(self.otherRobot.position.a)
        else:
            a_intercept =  1.5*abs(self.otherRobot.position.a)
