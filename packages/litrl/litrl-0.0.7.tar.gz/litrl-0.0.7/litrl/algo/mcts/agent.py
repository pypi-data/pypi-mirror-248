from pettingzoo.utils.env import AECEnv

from litrl.algo.mcts.mcts import MCTS, MCTSConfig
from litrl.common.agent import Agent

class MCTSAgent(Agent):
    def __init__(self, cfg: MCTSConfig = MCTSConfig(), *, prompt_action: bool = False):
        super().__init__()
        self._cfg = cfg
        self._prompt_action = prompt_action

    def get_action(self, env: AECEnv) -> int:
        mcts = MCTS(env, self._cfg)
        action = mcts.get_action()
        if self._prompt_action:
            input("Opponent's turn, press enter to continue")
        return action

    def __str__(self) -> str:
        return self.__class__.__name__ + "|" + str(self._cfg)