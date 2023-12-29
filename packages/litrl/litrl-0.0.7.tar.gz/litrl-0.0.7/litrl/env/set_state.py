from pettingzoo.utils.env import AECEnv
from pettingzoo.utils.wrappers import BaseWrapper
from collections import Counter

def set_state(env: AECEnv, board: list[list[int]])->None:
    flat_board = [item for row in board for item in row]
    counter = Counter(flat_board)
    
    env.unwrapped.board = flat_board
    obs, _, _, _, info = env.last()
    
    # TerminateIllegalWrapper needs these to be set
    env._prev_obs = obs
    env._prev_info = info
    
    # set the correct player turn
    if counter[1] > counter[2]:
        if env.unwrapped.agent_selection == "player_0":
            env.unwrapped.agent_selection = env.unwrapped._agent_selector.next()

if __name__ == "__main__":
    from pettingzoo.classic.connect_four_v3 import env as connect_four
    env = connect_four(render_mode="human")
    env.reset(seed=123)
    board = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [1,0,0,1,2,0,0],
    ]
    set_state(env, board)
    terminated, truncated = False, False
    while not (terminated or truncated):
        env.render()
        action = int(input("Enter action: "))
        env.step(action)
        _, reward, terminated, truncated, _ = env.last()
    print(f"Game over, final reward is {reward}")