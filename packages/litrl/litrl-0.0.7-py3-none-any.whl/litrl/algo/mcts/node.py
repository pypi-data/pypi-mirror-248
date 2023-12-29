from math import log, sqrt
from typing import Self

from loguru import logger

from litrl.algo.mcts.typing import ActType

MIN_REWARD = -1


class Node:
    def __init__(self, parent: Self):
        self.parent = parent
        self.children: dict[ActType, Self] = {}
        self.visits = 0
        self.reward_sum = 0
        self.depth = parent.depth + 1 if parent else 0  # for debugging/plotting
        # root's children encode agent's actions
        self.agent_turn = not parent.agent_turn if parent is not None else False

    def add_child(self, action: ActType):
        self.children[action] = Node(parent=self)

    @property
    def uncertainty(self) -> float:
        if self.visits == 0:
            return float("inf")
        return sqrt(log(self.parent.visits) / self.visits)

    @property
    def value(self) -> float:
        if self.visits == 0:
            return MIN_REWARD
        win_rate = self.reward_sum / self.visits
        return win_rate if self.agent_turn else 1 - win_rate


class Root(Node):
    def __init__(self):
        super().__init__(parent=None)

    def recommend(self) -> ActType:
        logger.debug(f"Visits: {[child.visits for child in self.children.values()]}")
        logger.debug(f"Values: {[child.value for child in self.children.values()]}")
        action = max(self.children, key=lambda action: self.children[action].visits)
        logger.debug(f"Recommending action {action} for player {self.agent_turn}")
        return action
