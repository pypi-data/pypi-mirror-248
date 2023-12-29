import gymnasium as gym
from gymnasium.wrappers.transform_reward import TransformReward


class ClipRewardWrapper(TransformReward):
    def __init__(
        self,
        env: gym.Env,
        min_reward: float = -float("inf"),
        max_reward: float = float("inf"),
    ):
        def f(x):
            return max(min(x, max_reward), min_reward)

        super().__init__(env, f)
