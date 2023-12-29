from abc import ABC, abstractmethod

from pettingzoo.utils.env import AECEnv


class Agent(ABC):
    @abstractmethod
    def get_action(self, env: AECEnv) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

class RandomAgent(Agent):
    def get_action(self, env: AECEnv):
        obs = env.observe(env.agent_selection)
        return env.action_space(env.agent_selection).sample(obs["action_mask"])
