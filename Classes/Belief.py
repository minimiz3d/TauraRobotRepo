class Belief:
    """ This class maintains the taura robot's memory """
    def __init__(self, ball_doubt):
        # Ball memories
        self.ball_doubt = ball_doubt
        self.ball_look_cycle = ball_look_cycle
        self.ball_first_look = ball_first_look

        # Goal memories
        self.goal_doubt = goal_doubt
        self.goal_look_cycle = goal_look_cycle
        self.opposite_to_goal = opposite_to_goal
        self.right_goal = right_goal
