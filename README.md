
## TODO / BUGS TO FIX / FEATURES TO ADD:
    - High Priority

        -Check stat calculation and setting in blank setting. Reset existing players stats.

        -Store the game score in integer variables instead 

        -Fix Unqiue constraint failed when submitted ball. UNIQUE constraint failed: base_game.on_strike_batsman_id. This happens when wrong batsmen are entered.

        -Refactor models for temporary & long term team creation and deletion. Create organization model where a community c an collectively create their own organization to run games with temporary & long term teams. 

        -When all wickets of a team fall end/increment innings.

    - Medium Priority
        - Configure media images for profile pictures.

        - Search functionality for playesr, teams, organizations.

        - Refactor so that no need to iterate to get batting score every time, store in variable.

        - Leader board rankings toggled based on various stats, shows current users rank.

        - To save databse only allow user to save 10 games, and discard other which deletes all related games?


    - Low Priority
        - Store data for where ball pitches and where ball is hit.
        - Social media posts.

        - Download score card of game as PDF.

        - Chat messaging between groups.

        - MVP scoring system for each game and storage of number of MVPs.

        - Machine leanring model to predict outcome of games.

        - Edit stats feature after iterating overs to alloq user to change mis-entered stats.

        - Implement a catch for incorrect authentication credentials

        - Privacy of viewing games
        
        - Find a better way to manage the state of the game without using multiple boolen variables.

        - Brainstorm features on how to make it more competitive for users.

## TESTS:
- Create 2 games. Record stats and entered and manually compute career stats
and make sure each game is working

## DONE:
- Implement Win condition for game. And win percentage for player in game.
- Update each player's career stats after game is over.
Iterate each game stat and update players career stat for that player. (TEST)
game.update_players_career_stats()
TypeError: 'NoneType' object is not callable 
- Move to next innings after 1st innings over is finished.
For last ball for 1st innings increment innings, this should be reflected in template. For the last ball of the second innings conclude the game. 
- AttributeError: 'NoneType' object has no attribute 'players', After clicking view details after accepting game.
- After game finished confirm its showing up in game history.
- Fixed unable to import django import bug error by deleting
existing virtual environment and restarting.
- Fixed early over increment bug.
- Make sure current score of entire game is showing.

