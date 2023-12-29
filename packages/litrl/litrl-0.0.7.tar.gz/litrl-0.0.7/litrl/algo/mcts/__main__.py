from loguru import logger

from .agent import MCTSAgent
from .mcts import MCTSConfig

if __name__ == "__main__":
    import argparse
    from time import sleep

    from litrl import make

    parser = argparse.ArgumentParser()
    parser.add_argument("--n-simulations", default=500, type=int)
    parser.add_argument("--wait-time", default=1, type=int)
    parser.add_argument(
        "--prompt-action",
        default=True,
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()

    cfg = MCTSConfig(simulations=args.n_simulations)
    agent = MCTSAgent(cfg, prompt_action=args.prompt_action)
    opponent = MCTSAgent(cfg, prompt_action=args.prompt_action)
    env = make("ConnectFour-v3", render_mode="human", opponent=opponent)
    _, info = env.reset(seed=123)
    terminated, truncated = False, False
    while not (terminated or truncated):
        sleep(args.wait_time)
        action = agent.get_action(env)
        obs, reward, terminated, truncated, info = env.step(action)
    logger.info(f"Game over, final reward is {reward}")
