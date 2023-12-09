from typing import List, NamedTuple, Optional

PlayerKey = str | int


class PlayerGameResult(NamedTuple):
    player_key: PlayerKey
    position: int  # 0 is best. increasing


GameResult = List[PlayerGameResult]


def calculate_elo(prev_elo_a: int, prev_elo_b: int, score: float, k=32):
    Qa = 10.0 ** (prev_elo_a / 400)
    Qb = 10.0 ** (prev_elo_b / 400)
    Ea = 1.0 * Qa / (Qa + Qb)
    new_elo = prev_elo_a + k * (score - Ea)
    return round(new_elo)


class MultiplayerEloCalculator:
    def __init__(self, player_keys: List[str | int], initial_elo=1000):
        self.player_keys = player_keys
        self.initial_elo = initial_elo

    def calculate(self, tournament_results: List[GameResult]):

        player_elos = {}
        for player_key in self.player_keys:
            player_elos[player_key] = [self.initial_elo]

        for game_result in tournament_results:

            # copy elos before new updates
            for player_key in self.player_keys:
                prev_player_elo = player_elos[player_key][-1]
                player_elos[player_key].append(prev_player_elo)

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

        return player_elos


def find_player_result(player_key: PlayerKey, game_result: GameResult) -> Optional[PlayerGameResult]:
    for player_result in game_result:
        if player_result.player_key == player_key:
            return player_result
    return None
