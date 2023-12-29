from copy import deepcopy

from pettingzoo import AECEnv
from pettingzoo.classic.connect_four_v3 import raw_env as connect_four_raw
from pettingzoo.utils import BaseWrapper
from pettingzoo.utils.env import AgentID


class CopyWrapper(BaseWrapper):
    """
    Deepcopy has a very weird behaviour with wrapped pettinzoo environments.
    This wrapper serves as an alternative
    """

    def __init__(self, env: AECEnv):
        if not type(env.unwrapped) == connect_four_raw:
            raise ValueError(env.unwrapped)
        self.env = connect_four_raw()
        self.env.agent_selection = deepcopy(env.agent_selection)
        self.env.board = deepcopy(env.unwrapped.board)
        self.env.truncations = deepcopy(env.unwrapped.truncations)
        self.env.terminations = deepcopy(env.unwrapped.terminations)
        self.env._agent_selector = deepcopy(env.unwrapped._agent_selector)
        self.env.rewards = deepcopy(env.rewards)
        self.env._cumulative_rewards = deepcopy(env.unwrapped._cumulative_rewards)
        self.env.infos = deepcopy(env.unwrapped.infos)

    def step(self, action: int) -> None:
        return self.env.step(action)

    def last(self):
        return self.env.last()

    @property
    def agent_selection(self) -> AgentID:
        return self.env.agent_selection
