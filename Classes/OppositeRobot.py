from Classes.WorldObject import *

class OppositeRobot(World_Object):
    def __init__(self, alpha, distance, tshirt_color, dist_to_ball = 0):
        super(OppositeRobot, self).__init__(alpha, distance)
        self.tshirt_color = tshirt_color
        self.dist_to_ball = dist_to_ball
