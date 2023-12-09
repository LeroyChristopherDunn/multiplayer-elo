from typing import List

import matplotlib.pyplot as plt
import numpy as np

from demo_game import NormalDistributionPlayer, run_demo_game, find_player_result, GameResult
from multiplayer_elo_calculator import MultiplayerEloCalculator


def tournament1():
    seed = 0
    rng = np.random.default_rng(seed)
    num_rounds = 1000
    initial_elo = 1500
    k = 32

    player1 = NormalDistributionPlayer(key=0, mean=0.25, std_dev=0.25, seed=seed + 1)
    player2 = NormalDistributionPlayer(key=1, mean=0.50, std_dev=0.25, seed=seed + 2)
    player3 = NormalDistributionPlayer(key=2, mean=0.75, std_dev=0.25, seed=seed + 3)
    player4 = NormalDistributionPlayer(key=3, mean=1.00, std_dev=0.25, seed=seed + 4)

    players = [player1, player2, player3, player4]
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

    elo_calculator = MultiplayerEloCalculator(player_keys=player_keys, initial_elo=initial_elo, k=k)
    player_elos = elo_calculator.calculate(tournament_results)

    # plt.hist(player_1_actions, bins=50)

    for player_key in player_keys:
        plt.plot(player_elos[player_key], label=f"player{player_key}")
    plt.xlabel("Game")
    plt.ylabel("Elo")
    plt.legend(loc="best")
    plt.show()


if __name__ == '__main__':
    tournament1()
