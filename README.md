2016 NBA Finals Simulator

This project simulates **Game 7 of the 2016 NBA Finals** between the Cleveland Cavaliers and Golden State Warriors.  
It models a basketball game possession by possession, with logic for steals, shot selection, assists, fouls, blocks, rebounds, and free throws.  



Features:
- Play-by-play mode: A list of plays is given so the logic can be understood. 
- Auto-sim mode: Quickly simulate an entire quarter and view updated scores.  
- Player stats lookup: Enter a player’s full name mid-game to view their current box score.  
- Realistic stats tracking: Points, rebounds, assists, steals, blocks, turnovers, FG%, 3P%, and FT%.  
- Object-oriented design: Player and Team classes handle data and logic cleanly.  



Functionality:
- Each possession begins with a chance of a steal.
- A shooter is selected based on team shot distribution rates.  
- Shots are evaluated using each player’s 2P% and 3P% skill values.  
- Misses can result in fouls, rebounds, or out-of-bounds turnovers.  
- Stats are updated live throughout the game.  



Running the Simulator
Clone the repo and run the script with Python 3:

```bash
git clone https://github.com/whitepaulv/2016_finals_simulator_v2.git
cd 2016_finals_simulator_v2
python3 nba_sim.py
