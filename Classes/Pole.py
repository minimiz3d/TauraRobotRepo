from MindInterface.Model import BaseObject

class Pole(BaseObject):
    def __init__(self, alpha, distance, opposite_to_goal, right_goal, seen):
        super(pos = Point2(0,0), "pole").__init__()

        self.alpha = alpha
        self.distance = distance
        self.opposite_to_goal = opposite_to_goal
        self.right_goal = right_goal
        self.seen = seen
