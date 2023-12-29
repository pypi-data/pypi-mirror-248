from datetime import datetime

import gymnasium as gym
from dateutil import tz
from gymnasium.core import Wrapper
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo

from litrl.wrappers.static_opponent_wrapper import StaticOpponentWrapper


class ValidationWrapper(Wrapper):
    def __init__(
        self,
        env: gym.Env | StaticOpponentWrapper,
        render_each_n_episodes: int,
    ):
        self.render_each_n_episodes = render_each_n_episodes

        def episode_trigger(episode: int) -> bool:
            return episode % self.render_each_n_episodes == 0

        super().__init__(
            RecordVideo(
                env=RecordEpisodeStatistics(env),
                video_folder=f"temp/{env}/{datetime.now(tz.UTC)}",
                episode_trigger=episode_trigger,
                disable_logger=True,
            ),
        )
