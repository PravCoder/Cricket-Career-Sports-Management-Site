
## TODO / BUGS TO FIX / FEATURES TO ADD:
    - High Priority
        - Move to next innings after 1st innings over is finished.
        For last ball for 1st innings increment innings, this should be relfected in template.
        For last ball for 2nd innings conclude the game.
        - Unit tests for correct stat storage and incrementation.
        - Update each player's career stats after game is over.
        - Refactor models for temporary & long term team creation and deletion. Create organization model where a community can collectively create their own organization to run games with temporary & long term teams. 
    - Medium Priority
        - Configure media images for profile pictures.
        - Search functionality for playesr, teams, organizations.
        - Refactor so that no need to iterate to get batting score every time, store in variable.
    - Low Priority
        - Social media posts.
        - Download score card of game as PDF.
        - Chat messaging between groups.
        - MVP scoring system for each game and storage of number of MVPs.
        - Machine leanring model to predict outcome of games.
        - Edit stats feature after iterating overs to alloq user to change mis-entered stats.
        - Implement a catch for incorrect authentication credentials
        - Privacy of viewing games
        - Find a better way to manage the state of the game without using multiple boolen variables.


## DONE:
- AttributeError: 'NoneType' object has no attribute 'players', After clicking view details after accepting game.
- After game finished confirm its showing up in game history.
- Fixed unable to import django import bug error by deleting
existing virtual environment and restarting.
- Fixed early over increment bug.
- Make sure current score of entire game is showing.

