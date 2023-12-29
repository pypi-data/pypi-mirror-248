from dataclasses import dataclass
from litrl.common.agent import Agent, RandomAgent
import numpy as np
from loguru import logger

from litrl.algo.mcts.node import Node, Root
from litrl.wrappers import StaticOpponentWrapper
from litrl.wrappers.copy_wrapper import CopyWrapper

@dataclass
class MCTSConfig:
    simulations: int = 50
    seed: int = 123
    rollout_agent: Agent = RandomAgent()
    
    def __str__(self) -> str:
        return f"simulations={self.simulations}, rollout_agent={str(self.rollout_agent)}"


class MCTS:
    def __init__(self, env: StaticOpponentWrapper, cfg: MCTSConfig = MCTSConfig()):
        self._root = Root()
        self._root_env = env
        self._cfg = cfg
        self._np_random = np.random.default_rng(seed=cfg.seed)
        self._simulation_env = CopyWrapper(self._root_env)
        self._expand(self._root)

    def get_action(self) -> int:
        for _ in range(self._cfg.simulations):
            self._simulation_env = CopyWrapper(self._root_env)
            node = self._select(self._root)
            self._expand(node)
            reward = self._rollout()
            self._backpropagate(node, reward)
        return self._root.recommend()

    def _select(self, node: Node) -> Node:
        uncertainties = []
        values = []
        for child in node.children.values():
            uncertainties.append(child.uncertainty)
            values.append(child.value)
            
        score = np.array(values) + np.array(uncertainties)
        action_index = np.argmax(score)
        action, child = list(node.children.items())[action_index]
        self._simulation_env.step(action)
        _, _, terminated, truncated, _ = self._simulation_env.last()
        if terminated or truncated or child.visits == 0:
            return child
        else:
            return self._select(child)

    def _expand(self, node: Node):
        legal_actions = self._simulation_env.observe(
            self._simulation_env.agent_selection,
        )["action_mask"]
        actions = np.nonzero(legal_actions)[0]
        for action in actions:
            node.add_child(action)

    def _rollout(self):
        _, reward, terminated, truncated, _ = self._simulation_env.last()
        while not (terminated or truncated):
            action = self._cfg.rollout_agent.get_action(self._simulation_env)
            self._simulation_env.step(action)
            _, reward, terminated, truncated, _ = self._simulation_env.last()

        if self._simulation_env.agent_selection != self._root_env.agent_selection:
            reward *= (
                -1
            )  # flip the sign. Reward observed from the opponent's perspective
        # use scale from 0 to 1:
        return max(reward, 0)

    def _backpropagate(self, node: Node, reward: float):
        node.visits += 1
        node.reward_sum += reward
        if node.parent:
            self._backpropagate(node.parent, reward)
