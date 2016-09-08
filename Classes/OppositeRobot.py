from Classes.WorldObject import *

class OppositeRobot(World_Object):
    def __init__(self, alpha, distance, tshirt_color):
        super(OppositeRobot, self).__init__(alpha, distance)
        self.tshirt_color = tshirt_color
