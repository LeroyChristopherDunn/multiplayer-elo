from typing import List

import matplotlib.pyplot as plt
import numpy as np

from demo_game import NormalDistributionPlayer, run_demo_game, find_player_result, GameResult
from multiplayer_elo_calculator import MultiplayerEloCalculator


def tournament1():
    seed = 0
    rng = np.random.default_rng(seed)
    num_rounds = 1000

    player1 = NormalDistributionPlayer(key=0, mean=0.25, std_dev=0.05, seed=seed + 1)
    player2 = NormalDistributionPlayer(key=1, mean=0.75, std_dev=0.05, seed=seed + 2)
    players = [player1, player2]
    player_keys = list(map(lambda p: p.key, players))

    tournament_results: List[GameResult] = []
    for i in range(num_rounds):
        rng.shuffle(players)
        game_result = run_demo_game(players)
        tournament_results.append(game_result)

    # temp to debug player behaviour
    player_1_actions = []
    for game_result in tournament_results:
        player1_result = find_player_result(player_keys[0], game_result)
        if player1_result is not None:
            player_1_actions.append(player1_result.player_action)

    player_elos = MultiplayerEloCalculator(player_keys=player_keys, initial_elo=1000).calculate(tournament_results)

    # plt.hist(player_1_actions, bins=50)

    plt.plot(player_elos[player_keys[0]], label=f"player{player_keys[0]}")
    plt.plot(player_elos[player_keys[1]], label=f"player{player_keys[1]}")
    plt.xlabel("Game")
    plt.ylabel("Elo")
    plt.legend(loc="best")
    plt.show()


if __name__ == '__main__':
    tournament1()
