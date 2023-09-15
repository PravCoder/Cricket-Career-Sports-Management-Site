from django.db import models
from django.contrib.auth.models import AbstractUser

class Team(models.Model):
    name = models.CharField(max_length=200,null=True)
    captain = models.OneToOneField("Player", related_name="captain",on_delete=models.SET_NULL,null=True,blank=True,unique=False)
    players = models.ManyToManyField("Player", related_name="players", blank=True)
    games_played = models.IntegerField(default=0,null=True,blank=True)
    games_won = models.IntegerField(default=0,null=True,blank=True)
    runs_average = models.FloatField(default=0,null=True,blank=True)
    wickets_average = models.FloatField(default=0,null=True,blank=True)

    filler = models.BooleanField(default=False,null=True,blank=False)
    games = models.ManyToManyField("Game", related_name="gammes", blank=True)

class Game(models.Model):
    # we only care if these variables are True
    entering_stats = models.BooleanField(default=False,null=True,blank=False) # true if stat entering has began, this is set to true when the inilize game info is submitted
    doneStats = models.BooleanField(default=False,null=True,blank=False) # true is stat entering has concluded, this is set to true when the last over of the last innings is iterated through
    archived = models.BooleanField(default=False,null=True,blank=False) # this is set to true when the user confirms that there is no edits to make to the stats entered.
    winner = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="winner",blank=True)
    team1 = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="team1")  # team that sent invite
    team2 = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="team2")

    batting1_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="batting1")
    bowling1_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="bowling1")

    batting2_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="batting2")
    bowling2_team  = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="bowling2")



    year = models.CharField(max_length=200,null=True)
    month = models.CharField(max_length=200,null=True)
    day = models.CharField(max_length=200,null=True)
    time = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200,null=True)
    overs = models.IntegerField(default=0,null=True,blank=True)

    batting_score1 = models.IntegerField(default=0,null=True,blank=True) # number of runs for the first batting team
    batting_score2 = models.IntegerField(default=0,null=True,blank=True) # number of runs for second batting team

    bowling_score1 = models.IntegerField(default=0,null=True,blank=True) # number of wickets for the frist bowling team
    bowling_score2 = models.IntegerField(default=0,null=True,blank=True) # number of wickets for the second bowling team

    # Relative to the live current game
    current_innings =  models.IntegerField(default=1,  null=True,blank=True)
    current_over = models.IntegerField(default=1,  null=True,blank=True)
    current_ball = models.IntegerField(default=1,  null=True,blank=True)
    ball1 = models.CharField(max_length=200,null=True) # icon of first ball in current over
    ball2 = models.CharField(max_length=200,null=True)
    ball3 = models.CharField(max_length=200,null=True)
    ball4 = models.CharField(max_length=200,null=True)
    ball5 = models.CharField(max_length=200,null=True)
    ball6 = models.CharField(max_length=200,null=True)


    on_strike_batsman = models.OneToOneField("Player", related_name="on_strike_batsman",on_delete=models.SET_NULL,null=True,blank=True,unique=False)
    off_strike_batsman = models.OneToOneField("Player", related_name="off_strike_batsman",on_delete=models.SET_NULL,null=True,blank=True,unique=False)
    current_bowler = models.OneToOneField("Player", related_name="current_bowler",on_delete=models.SET_NULL,null=True,blank=True,unique=False)
    # Statistics
    players_stats = models.ManyToManyField("PlayerGameStat", related_name="players_stats", blank=True)

    @property
    def get_batting1_score(self):
        runs = 0
        for stat in self.players_stats.all():
            if stat.player in list(self.batting1_team.players.all()):
                runs += stat.total_runs
        return runs

    @property
    def get_batting2_score(self):
        runs = 0
        for stat in self.players_stats.all():
            if stat.player in list(self.batting2_team.players.all()):
                runs += stat.total_runs
        return runs

    @ property
    def get_bowling1_score(self):
        wickets = 0
        for stat in self.players_stats.all():
            if stat.player in list(self.bowling1_team.players.all()):
                wickets += stat.wickets
        return wickets

    @property
    def get_bowling2_score(self):
        wickets = 0
        for stat in self.players_stats.all():
            if stat.player in list(self.bowling2_team.players.all()):
                wickets += stat.wickets
        return wickets
    
class GameInvite(models.Model):
    from_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="from_team")
    to_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="to_team")

    year = models.CharField(max_length=200,null=True)
    month = models.CharField(max_length=200,null=True)
    day = models.CharField(max_length=200,null=True)
    time = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200,null=True)
    overs = models.IntegerField(default=0,null=True,blank=True)

class TeamInvite(models.Model):
    to_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True)  # the team you got invited to

class Player(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True)
    runs = models.IntegerField(default=0,null=True,blank=True)
    wickets = models.IntegerField(default=0,null=True,blank=True)  
    catches = models.IntegerField(default=0,null=True,blank=True)  
    sixes = models.IntegerField(default=0,null=True,blank=True)  
    fours = models.IntegerField(default=0,null=True,blank=True)  
    games_played = models.IntegerField(default=0,null=True,blank=True)
    games_won = models.IntegerField(default=0,null=True,blank=True)

    fifties = models.IntegerField(default=0,null=True,blank=True)  
    runs_hs = models.IntegerField(default=0,null=True,blank=True) 
    runs_average = models.FloatField(default=0,null=True,blank=True) 
    sr = models.FloatField(default=0,null=True,blank=True) 

    balls_bowled = models.IntegerField(default=0,null=True,blank=True)
    balls_played = models.IntegerField(default=0,null=True,blank=True)
    wickets_average = models.FloatField(default=0,null=True,blank=True)
    wickets_hs = models.IntegerField(default=0,null=True,blank=True)

    game_invites = models.ManyToManyField("GameInvite", related_name="game_invites", blank=True)
    team_invites = models.ManyToManyField("TeamInvite", related_name="team_invites", blank=True)

    games = models.ManyToManyField("Game", related_name="games", blank=True)

    fours_hs = models.IntegerField(default=0,null=True,blank=True)
    sixes_hs = models.IntegerField(default=0,null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_game_stat(self, game):
        for stat in game.players_stats.all():
            if stat.player == self:
                return stat


class PlayerGameStat(models.Model):
    game = models.ForeignKey(Game,on_delete=models.SET_NULL,null=True, related_name="player_game")
    player = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True, related_name="player_player")

    runs_scored = models.IntegerField(default=0,null=True,blank=True)
    runs_ran = models.IntegerField(default=0,null=True,blank=True)

    wickets = models.IntegerField(default=0,null=True,blank=True)

    extras = models.IntegerField(default=0,null=True,blank=True)

    balls_batted = models.IntegerField(default=0,null=True,blank=True)
    balls_bowled = models.IntegerField(default=0,null=True,blank=True)

    fours = models.IntegerField(default=0,null=True,blank=True)
    sixes = models.IntegerField(default=0,null=True,blank=True)

    catches = models.IntegerField(default=0,null=True,blank=True)
    runs_given_up = models.IntegerField(default=0,null=True,blank=True)

    out_type = models.CharField(max_length=200,null=True, default="not out")
    out_ball = models.IntegerField(default=-1,null=True,blank=True) # -1 means they havent been out
    out_over =  models.IntegerField(default=-1,null=True,blank=True) #-1 means they gavent been out

    @property
    def total_runs(self):
        return self.runs_scored + self.runs_ran



class Play(models.Model):
    batsman = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True, related_name="play_batsman")
    bowler = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True, related_name="play_bowler")
    outcome = models.CharField(max_length=200,null=True)
    highlight = models.BooleanField(default=False,null=True,blank=False) 
    extra = models.BooleanField(default=False,null=True,blank=False) 
    extra_type = models.CharField(max_length=200,null=True)

