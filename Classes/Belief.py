class Belief:
    """ This class maintains the taura robot's memory """
    def __init__(self, ball_doubt):
        # Ball memories
        self.ball_doubt = ball_doubt
        self.ball_look_cycle = ball_look_cycle
        self.ball_first_look = ball_first_look
        self.ball_a_last_seen = ball_a_last_seen
        self.ball_r_last_seen = ball_r_last_seen

        # Goal memories
        self.pole1_a_last_seen = pole1_a_last_seen
        self.pole1_r_last_seen = pole1_r_last_seen
        self.pole2_a_last_seen = pole2_a_last_seen
        self.pole2_r_last_seen = pole2_r_last_seen
        self.goal_doubt = goal_doubt
        self.goal_look_cycle = goal_look_cycle
