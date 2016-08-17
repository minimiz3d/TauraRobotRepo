from Ball import *
from OtherRobot import *
from Pole import *

from Constants import *

from MindInterface import Simulation
from MindInterface.config import *

class TauraFSM():
    """ """

    def __init__(self, currentState, ball, otherRobot, pole1, pole2, tauraRobot):
        self.currentState = currentState
        self.ball = ball
        self.otherRobot = otherRobot
        self.pole1 = pole1
        self.pole2 = pole2
        self.tauraRobot = tauraRobot

    # FSM itself
    def switch(self, state):
        if   state == 0: self.currentState = self.ball_search()
        elif state == 1: self.currentState = ball_go_after()
        elif state == 2: self.currentState = opposite_goal_search()
        elif state == 3: self.currentState = opposite_to_goal()
        elif state == 4: self.currentState = kick()
        elif state == 5: self.currentState = ball_intercept()
        else:
            print("ERROR!")
        return self.currentState

    """ STATES """
    # State 0
    def ball_search(self):
        self.object_search()

        if self.ball:
            do_measure()
            if otherRobot.dist_ball:
                if self.ball.position.r > self.otherRobot.dist_ball + THRESHOLD_TO_INTERCEPT:
                    return 5
            return 1
        else:
            self.ball.look_around()
            return 0

    # State 1
    def ball_go_after():
        object_search()
        if self.ball.r_last_seen > BALL_RADIUS:
            walk_to(self.ball.a_last_seen)
            return 1
        if self.ball.r_last_seen > 5:
            return 2
        else:
            return 0

    # State 2
    def opposite_goal_search():
        # global pole1
        # global pole2
        # global balldoubt

        # global goal_look_cycle

        object_search()
        if self.ball.doubt < BALL_MEMORY_CYCLE:
            if self.pole1 or self.pole2:
                return 3
            else:
                opposite_goal_look_around()
                return 2
        else:
            goal_look_cycle = 0
            return 0

    # State 3
    def opposite_to_goal():
        object_search()

        if self.ball.doubt < BALL_MEMORY_CYCLE:
            if self.pole1 and self.pole2:
                if(self.pole1.position.a+self.pole2.position.a)/2>0-THRESHOLD/3 and (self.pole1.position.a+self.pole2.position.a)/2<0+THRESHOLD/3:
                    return 4
                ball_turn_around()
            elif self.pole1:
                if self.pole1.position.a>0-THRESHOLD/3 and self.pole1.position.a<0+THRESHOLD/3:
                    return 4
                ball_turn_around()
            else:
                return 2
            return 3
        else:
            return 0

    # State 4
    def kick():
        stop_to_walk()
        self.tauraRobot.updateSimulation()
        time.sleep(0.1)
        if self.ball.a_last_seen > 0:
            left_kick()
        else:
            right_kick()
        ball_free()
        self.tauraRobot.updateSimulation()
        time.sleep(0.1)
        return 0

    # State 5
    def ball_intercept():
        # global ball_doubt
        # global ball_a_last_seen
        # global robot1

        # global a_intercept
        # global direction

        # from TauraPlayerAI_sim import direction, a_intercept ???

        object_search()
        if self.otherRobot.position.a > self.ball.a_last_seen-THRESHOLD_ALIGN_BALL_TO_ROBOT and otherRobot.position.a < self.ball.a_last_seen+THRESHOLD_ALIGN_BALL_TO_ROBOT:
            direction = 0
            return 1
        if direction:
            walk_to(a_intercept)
            if direction > 4:
                a_intercept = 0
            direction+=1
        else:
            do_direction()
            direction = 1
        if self.ball.doubt < BALL_MEMORY_CYCLE:
            return 5
        else:
            direction = 0
            return 0

    """ SUBPROCESSES """
    # Subprocess 0
    def object_search(self):
        # global state

        # global ball_doubt
        # global goal_doubt
        # global ball

        # global pole1
        # global pole2

        # global robot1

        pole_found  = 0
        robot_found = 0

        goal_doubt += GOAL_INCREASES_GOALDOUBT
        self.ball.doubt += BALL_INCREASES_BALLDOUBT
        for obj in world.objects_list:
            if obj.kind == "ball":
                if self.currentState == 0 or self.currentState == 1:
                    self.ball = obj
                    self.ball.memorize(self.ball)
            if obj.kind == "pole":
                pole_found +=1
                if pole_found == 1:
                    pole1 = obj
                if pole_found == 2:
                    pole2 = obj
                goal_memorize()
            if obj.kind == "robot":
                robot_found+=1
                if robot_found == 1:
                    robot1 = obj

        if goal_doubt > GOAL_MEMORY_CYCLE:
            goal_free()
        if self.ball.doubt > BALL_MEMORY_CYCLE:
            ball_free()

    # Subprocess 1
    def ball_look_around():
        # global ball_first_look
        # global TILT_MIN
        # global TILT_MAX
        # global PAN_MIN
        # global PAN_MAX
        # global TILT_STEP
        # global PAN_STEP
        # global ball_look_cycle
        global increasing_pan
        global pan
        global tilt

        self.tauraRobot.setNeck((pan,tilt))
        if self.ball.first_look == 1:
            self.ball.first_look = 0
            pan = PAN_MIN
            tilt = TILT_MIN
            increasing_pan = 1
            self.ball.look_cycle = 0
        if(tilt <= TILT_MAX):
            self.ball.look_cycle +=1
            if pan < PAN_MAX and increasing_pan == 1:
                pan += PAN_STEP
            elif pan > PAN_MIN and increasing_pan == 0:
                pan -= PAN_STEP
            else:
                tilt += TILT_STEP
                increasing_pan = not increasing_pan
        else:
            self.tauraRobot.setNeck((0,0))
            turn_around()

    # Subprocess 2
    def turn_around():
        # global ball_look_cycle
        # global ball_first_look
        global turn_to

        self.tauraRobot.setMovementVector(Point2(r=0, a=turn_to,phi=turn_to))
        if  self.ball.look_cycle == 0:
            self.ball.first_look = 1
            stop_to_walk()
        else:
            self.ball.look_cycle -=1

    # Subprocess 3
    def walk_to(direction):
        self.tauraRobot.setMovementVector(Point2(r=1,a=direction,phi=direction))

    # Subprocess 4
    def stop_to_walk():
        self.tauraRobot.setMovementVector(Point2())

    # Subprocess 5
    def opposite_goal_look_around():
        global increasing_pan
        global pan
        global goal_look_cycle
        # global PAN_MIN
        # global PAN_MAX
        # global PAN_STEP

        if goal_look_cycle <= GOAL_LOOKING_CYCLE_MAX :
            if pan < PAN_MAX and increasing_pan == 1:
                pan += PAN_STEP
            elif pan > PAN_MIN and increasing_pan == 0:
                pan -= PAN_STEP
            else:
                increasing_pan = not increasing_pan
            self.tauraRobot.setNeck((pan,TILT_TO_LOOKING_GOAL))
            goal_look_cycle+=1
        else:
            self.ball.turn_around()

    # Subprocess 6
    def ball_turn_around():
        global turnto
        self.tauraRobot.setMovementVector(Point2(r=1, a=pi/2*turn_to,phi=-pi/2*turn_to))

    # Subprocess 7
    def left_kick():
        self.tauraRobot.setKick( 1)

    # Subprocess 8
    def right_kick():
        self.tauraRobot.setKick(-1)

    # Subprocess 9 - VERIFICAR AQUI.
    def ball_memorize(ball):
        global ball_a_last_seen
        global ball_r_last_seen
        global ball_doubt
        global ball_first_look
        global ball_look_cycle

        self.ball.a_last_seen = ball.position.a
        self.ball.r_last_seen = ball.position.r
        self.ball.doubt = 0
        self.ball.first_look = 1
        self.ball.look_cycle = 0

    # Subprocess 10
    def ball_free():
        global ball
        global ball_a_last_seen
        global ball_r_last_seen
        global ball_doubt

        self.ball.a_last_seen = 0
        self.ball.r_last_seen = 0
        self.ball.doubt = BALL_MEMORY_CYCLE

        self.ball.ball = None
        # Dúvida aqui. O objeto bola deve desaparecer?

    # Subprocess 11
    def goal_memorize():
        global pole1_a_last_seen
        global pole1_r_last_seen
        global pole2_a_last_seen
        global pole2_r_last_seen
        global goal_doubt
        global goal_look_cycle
        global turn_to
        global pole1
        global pole2

        goal_look_cycle = 0
        self.pole1.a_last_seen = pole1.position.a
        self.pole1.r_last_seen = pole1.position.r
        goal_doubt = 0

        if self.pole2:
            self.pole2a_last_seen = pole2.position.a
            self.pole2r_last_seen = pole2.position.r

            if self.ball.doubt < BALL_MEMORY_CYCLE:
                if(self.pole1.a_last_seen + self.pole2.a_last_seen)/2 < 0:
                    turn_to =  1
                else:
                    turn_to = -1
        elif self.ball.doubt < BALL_MEMORY_CYCLE:
            if self.pole1.a_last_seen < 0:
                turn_to =  1
            else:
                turn_to = -1

    # Subprocess 12
    def goal_free():
        global pole1
        global pole2
        global pole1_a_last_seen
        global pole1_r_last_seen
        global pole2_a_last_seen
        global pole2_r_last_seen
        global goal_doubt

        self.pole1.a_last_seen = 0
        self.pole1.r_last_seen = 0
        self.pole2.a_last_seen = 0
        self.pole2.r_last_seen = 0
        goal_doubt = GOAL_MEMORY_CYCLE
        self.pole1 = None   # DÚVIDA AQUI TB.
        self.pole2 = None   # DÚVIDA AQUI TB.

    # Subprocess 12
    def do_measure(otherRobot, ball):
        # global robot1
        # global robot1_dist_ball

        if otherRobot:
            a = otherRobot.position.a
            b = otherRobot.position.r
            c = ball.r_last_seen
            otherRobot.dist_ball = sqrt(b*b+c*c-2*b*c*cos(a))
        else:
            otherRobot.dist_ball = None

    # Subprocess 13
    def do_direction():
        global a_intercept
        global robot1
        global robot1_dist_ball

        if robot1.position.a > ball_r_last_seen:
            a_intercept = -1.5*abs(robot1.position.a)
        else:
            a_intercept =  1.5*abs(robot1.position.a)
