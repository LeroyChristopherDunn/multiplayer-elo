from typing import List

import numpy as np
import matplotlib.pyplot as plt

from demo_game import NormalDistributionPlayer, run_demo_game, find_player_result, GameResult


def calculate_elo(prev_elo_a: int, prev_elo_b: int, score: float, k=32):
    Qa = 10.0 ** (prev_elo_a / 400)
    Qb = 10.0 ** (prev_elo_b / 400)
    Ea = 1.0 * Qa / (Qa + Qb)
    new_elo = prev_elo_a + k * (score - Ea)
    return round(new_elo)


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

    player_elos = {}
    for player_key in player_keys:
        player_elos[player_key] = [1000]

    # temp to debug player behaviour
    player_1_actions = []

    for game_result in tournament_results:

        # copy elos before new updates
        for player_key in player_keys:
            prev_player_elo = player_elos[player_key][-1]
            player_elos[player_key].append(prev_player_elo)

        # temp to debug player behaviour
        player1_result = find_player_result(player_keys[0], game_result)
        if player1_result is not None:
            player_1_actions.append(player1_result.player_action)

        # every player vs every other player
        game_player_keys = list(map(lambda r: r.player_key, game_result))
        for player_index in range(len(game_player_keys)):
            for opponent_index in range(len(game_player_keys)):

                # need to consider pairs so elo allocation is zero-sum
                # only consider pairs once. A vs B = B vs A. A vs A invalid
                if player_index >= opponent_index:
                    continue

                player_key = game_player_keys[player_index]
                opponent_key = game_player_keys[opponent_index]

                player_position = find_player_result(player_key, game_result).position
                opponent_position = find_player_result(opponent_key, game_result).position

                player_elo_score = 1 if player_position < opponent_position else 0 if opponent_position < player_position else 0.5
                opponent_elo_score = 1 - player_elo_score

                player_elo = player_elos[player_key][-1]
                opponent_elo = player_elos[opponent_key][-1]

                new_player_elo = calculate_elo(player_elo, opponent_elo, player_elo_score)
                new_opponent_elo = calculate_elo(opponent_elo, player_elo, opponent_elo_score)

                player_elos[player_key][-1] = new_player_elo
                player_elos[opponent_key][-1] = new_opponent_elo

                # print(game_result_per_player)
                # print(f"player {player} opponent {opponent} player_elo {player_elo} opponent_elo {opponent_elo} new_player_elo {new_player_elo} new_opponent_elo {new_opponent_elo}")

    # plt.hist(player_1_actions, bins=50)

    plt.plot(player_elos[player_keys[0]], label=f"player{player_keys[0]}")
    plt.plot(player_elos[player_keys[1]], label=f"player{player_keys[1]}")
    plt.xlabel("Game")
    plt.ylabel("Elo")
    plt.legend(loc="best")
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    tournament1()

