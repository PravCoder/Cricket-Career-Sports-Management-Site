from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class Organization(models.Model): # Club
    name = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=200,null=True)
    members = models.ManyToManyField("Player", related_name="members", blank=True)
    date_established = models.DateTimeField(default=datetime.now, blank=True)
    location = models.CharField(max_length=200,null=True)
    games = models.ManyToManyField("Game", related_name="org_games", blank=True)

    teams = models.ManyToManyField("Team", related_name="org_teams", blank=True)

class Team(models.Model):
    name = models.CharField(max_length=200,null=True)
    captain = models.OneToOneField("Player", related_name="captain",on_delete=models.SET_NULL,null=True,blank=True,unique=False)
    players = models.ManyToManyField("Player", related_name="players", blank=True)
    games_played = models.IntegerField(default=0,null=True,blank=True)
    games_won = models.IntegerField(default=0,null=True,blank=True)
    runs_average = models.FloatField(default=0,null=True,blank=True)
    wickets_average = models.FloatField(default=0,null=True,blank=True)
    # organ
    games = models.ManyToManyField("Game", related_name="gammes", blank=True)
    temporary = models.BooleanField(default=False,null=True,blank=False)
    organization = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True, related_name="winner",blank=True)


class Game(models.Model):
    # we only care if these variables are True
    entering_stats = models.BooleanField(default=False,null=True,blank=False) # true if stat entering has began, this is set to true when the inilize game info is submitted
    doneStats = models.BooleanField(default=False,null=True,blank=False) # true is stat entering has concluded, this is set to true when the last over of the last innings is iterated through
    archived = models.BooleanField(default=False,null=True,blank=False) # this is set to true when the user confirms that there is no edits to make to the stats entered.
    winner = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="winner",blank=True)
    team1 = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="team1")  # team that sent invite
    team2 = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="team2")
    # Short-term team within organization
    temporary = models.BooleanField(default=False,null=True,blank=False)

    batting1_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="batting1")
    bowling1_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="bowling1")

    batting2_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="batting2")
    bowling2_team  = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="bowling2")

    date = models.CharField(max_length=200,null=True)
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
    def update_players_career_stats(self):
        for stat in self.players_stats.all():
            player = stat.player
            player.runs += stat.total_runs
            player.wickets += stat.wickets
            player.catches += stat.catches
            player.fours += stat.fours
            player.sixes += stat.sixes
            player.catches += stat.catches
            player.balls_bowled = stat.balls_bowled
            player.balls_played = stat.balls_batted
            player.games_played += 1  # increment each players games-played
            if stat.is_fiftey == True:
                player.fifties += 1
            if stat.is_century == True:
                player.centuries += 1
            player.save()
            player.update_career_highscores(stat)
            player.update_career_averages()
            player.save()

    @property
    def confirm_winner(self):
        if self.get_batting1_score > self.get_batting2_score:
            self.winner = self.team1
        if self.get_batting2_score > self.get_batting1_score:
            self.winner = self.team2
        self.save()
    @property
    def update_players_win_percentage(self):
            if self.winner == self.team1:
                for player in self.team1.players.all():
                    player.games_won += 1
                    player.save()
                    player.set_win_percentage
                for player in self.team2.players.all():
                    player.save()
                    player.set_win_percentage
            if self.winner == self.team2:
                for player in self.team1.players.all():
                    player.save()
                    player.set_win_percentage
                for player in self.team2.players.all():
                    player.games_won += 1
                    player.save()
                    player.set_win_percentage
                    

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
    
class GameInvite(models.Model): # for games outside of organization
    from_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="from_team")
    to_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True, related_name="to_team")

    date = models.CharField(max_length=200,null=True)
    time = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200,null=True)
    overs = models.IntegerField(default=0,null=True,blank=True)

class TeamInvite(models.Model):  # for long term team?
    to_team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True)  # the team you got invited to

class OrganizationInvite(models.Model):
    organization = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True, blank=True)

class Player(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    teams = models.ManyToManyField("Team", related_name="teams", blank=True) # long-term-team outside of organization

    organization = models.ForeignKey(Organization,on_delete=models.SET_NULL,null=True, blank=True)
    runs = models.IntegerField(default=0,null=True,blank=True)
    wickets = models.IntegerField(default=0,null=True,blank=True)  
    catches = models.IntegerField(default=0,null=True,blank=True)  
    sixes = models.IntegerField(default=0,null=True,blank=True)  
    fours = models.IntegerField(default=0,null=True,blank=True)  
    extras = models.IntegerField(default=0,null=True,blank=True)  
    games_played = models.IntegerField(default=0,null=True,blank=True)
    games_won = models.IntegerField(default=0,null=True,blank=True)
    win_percentage = models.FloatField(default=0,null=True,blank=True) 

    fifties = models.IntegerField(default=0,null=True,blank=True)  
    centuries = models.IntegerField(default=0,null=True,blank=True)  
    sr = models.FloatField(default=0,null=True,blank=True) 

    runs_hs = models.IntegerField(default=0,null=True,blank=True) 
    wickets_hs = models.IntegerField(default=0,null=True,blank=True)
    fours_hs = models.IntegerField(default=0,null=True,blank=True)
    sixes_hs = models.IntegerField(default=0,null=True,blank=True)

    runs_average = models.FloatField(default=0,null=True,blank=True) 
    wickets_average = models.FloatField(default=0,null=True,blank=True)
    fours_average = models.FloatField(default=0,null=True,blank=True)
    sixes_average = models.FloatField(default=0,null=True,blank=True)
    catches_average = models.FloatField(default=0,null=True,blank=True)
    extras_average = models.FloatField(default=0,null=True,blank=True)


    balls_bowled = models.IntegerField(default=0,null=True,blank=True)
    balls_played = models.IntegerField(default=0,null=True,blank=True)

    game_invites = models.ManyToManyField("GameInvite", related_name="game_invites", blank=True)
    team_invites = models.ManyToManyField("TeamInvite", related_name="team_invites", blank=True)
    org_invites = models.ManyToManyField("OrganizationInvite", related_name="org_invites", blank=True)
    games = models.ManyToManyField("Game", related_name="games", blank=True)



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def set_win_percentage(self):
        self.win_percentage = self.games_won/self.games_played
        self.save()

    def get_game_stat(self, game):
        for stat in game.players_stats.all():
            if stat.player == self:
                return stat
    def update_career_highscores(self, stat):
        if stat.total_runs > self.runs_hs:
            self.runs_hs = stat.total_runs
        if stat.fours > self.fours_hs:
            self.fours_hs = stat.fours
        if stat.sixes > self.sixes_hs:
            self.sixes_hs = stat.sixes
        if stat.wickets > self.wickets_hs:
            self.wickets_hs = stat.wickets
        self.save()
    def update_career_averages(self):
        self.runs_average = self.runs /self.games_played
        self.wickets_average = self.wickets /self.games_played
        self.fours_average = self.fours /self.games_played
        self.sixes_average = self.sixes /self.games_played
        self.catches_average = self.catches /self.games_played
        self.extras_average = self.extras /self.games_played
        self.save()



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
    @property
    def is_fiftey(self):
        if self.total_runs >= 50 and self.total_runs < 100:
            return True
        else:
            return False
    @property
    def is_century(self):
        if self.total_runs >= 100:
            return True
        else:
            return False



class Play(models.Model):
    batsman = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True, related_name="play_batsman")
    bowler = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True, related_name="play_bowler")
    outcome = models.CharField(max_length=200,null=True)
    highlight = models.BooleanField(default=False,null=True,blank=False) 
    extra = models.BooleanField(default=False,null=True,blank=False) 
    extra_type = models.CharField(max_length=200,null=True)

