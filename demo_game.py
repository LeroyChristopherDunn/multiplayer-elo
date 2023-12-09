from abc import ABC, abstractmethod
from typing import List, NamedTuple, Optional

import numpy as np

PlayerKey = str | int


class Player(ABC):

    def __init__(self, key: PlayerKey):
        self.key = key

    @abstractmethod
    def play(self) -> float:
        pass


class PlayerGameResult(NamedTuple):
    player_key: PlayerKey
    position: int  # 0 is best. increasing
    player_action: float


GameResult = List[PlayerGameResult]


# player who guesses lower number wins
def run_demo_game(players: List[Player]) -> GameResult:
    results: List[PlayerGameResult] = []
    for i in range(len(players)):
        results.append(PlayerGameResult(
            player_key=players[i].key,
            player_action=players[i].play(),
            position=0,  # adjusted later
        ))

    sorted_results = sorted(results, key=lambda result: result.player_action)

    results_with_position = []
    for i in range(len(sorted_results)):
        results_with_position.append(PlayerGameResult(
            player_key=sorted_results[i].player_key,
            player_action=sorted_results[i].player_action,
            position=i,
        ))

    return results_with_position


class NormalDistributionPlayer(Player):

    def __init__(self, key: PlayerKey, mean: float, std_dev: float, seed=None):
        super().__init__(key)
        self._mean = mean
        self._std_dev = std_dev
        self._rng = np.random.default_rng(seed)

    def play(self) -> float:
        return self._rng.normal(self._mean, self._std_dev)


def find_player_result(player_key: PlayerKey, game_result: GameResult) -> Optional[PlayerGameResult]:
    for player_result in game_result:
        if player_result.player_key == player_key:
            return player_result
    return None
