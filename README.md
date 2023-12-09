# Multiplayer Elo calculator

- Calculate Elo for multiplayer games (also works for 2 player games)
- Runs pairwise Elo updates from game results [(inspiration)](https://gamedev.stackexchange.com/questions/55441/player-ranking-using-elo-with-more-than-two-players)
- All players don't have to play in every game
- Proof of concept stabilizes after about 1000 games
- Can control population mean using `initial_mean` and variance using `k`
- Recommend running games and calculating Elo from results separately

