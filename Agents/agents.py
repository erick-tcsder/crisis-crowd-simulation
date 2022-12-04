from utils.position import Position
from actions import Actions


class Personality:
    def __init__(self, courage: int, kindness: int, ):
        self.courage = courage
        self.kindness = kindness

class Agent:
    def __init__(self, name, position : Position, velocity: float, actions: list(Actions),
                 state: int, personality: Personality, behavior: BehaviorFunctions):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.actions = actions
        self.state = state
        self.personality = personality
        self.behavior = behavior