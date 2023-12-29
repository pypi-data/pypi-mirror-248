import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics
from loguru import logger
from pettingzoo.classic.connect_four_v3 import env as connect_four

from litrl.wrappers import (
    ClipRewardWrapper,
    StaticOpponentWrapper,
    ValidationWrapper,
)


def make(id: str, *, val: bool = False, **kwargs) -> gym.Env:
    logger.debug(f"Creating environment: {id}")
    render_mode = "rgb_array" if val else kwargs.pop("render_mode", None)
    render_each_n_episodes = kwargs.pop("render_each_n_episodes", 1)
    match id:
        case "CartPole-v1":
            env = gym.make("CartPole-v1", render_mode=render_mode, **kwargs)
        case "ConnectFour-v3":
            opponent = kwargs.pop("opponent", None)
            env = StaticOpponentWrapper(
                connect_four(render_mode=render_mode, **kwargs),
                opponent=opponent,
            )
        case "LunarLander-v2":
            env = ClipRewardWrapper(
                gym.make("LunarLander-v2", render_mode=render_mode, **kwargs),
                min_reward=-1,
            )
        case _:
            raise ValueError(f"Unsupported environment: {id}")
    if val:
        env = ValidationWrapper(env, render_each_n_episodes=render_each_n_episodes)
    else:
        env = RecordEpisodeStatistics(env)
    return env
