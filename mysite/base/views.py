from django.http import response
from django.shortcuts import redirect, render
from .models import GameInvite, Player,Team,Game,TeamInvite,PlayerGameStat,Organization
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def logout_user(request):
    if request.user.is_authenticated == True:
        logout(request)
        print("User has been logged out")
    return redirect("home")
def unauthorized(request):
    context = {}
    return render(request, "base/login_error_page.html", context)
def reset(request):
    for player in Player.objects.all():
        player.runs = 0
        player.wickets = 0
        player.catches = 0
        player.fours = 0
        player.sixes = 0
        player.games_played = 0
        player.games_won = 0
        player.win_percentage = 0
        player.fifties = 0
        player.runs_hs = 0
        player.wickets_hs = 0
        player.fours_hs = 0
        player.sixes_hs = 0
        player.runs_average = 0
        player.wickets_average = 0
        player.fours_average = 0
        player.sixes_average = 0
        player.catches_average = 0
        player.extras_average = 0
        player.balls_played = 0
        player.save()
    for game in Game.objects.all():
        game.delete()
    for stat in PlayerGameStat.objects.all():
        stat.delete()
    context = {}
    return render(request, "base/home.html", context)

def home(request):
    user = request.user
    if user.is_authenticated == False:
        context = {}
        return render(request, "base/home.html", context)
    
    print("user team: " + str(user.team))
    if user.team == None:
        team = Team.objects.create(name="filler", filler=True)  # creating filler-team-obj for new user with no tea
        user.team = team
        user.save()
        team.save()

    upcoming_games = []  # all games with completed=False
    for g in user.games.all():
        if g.entering_stats == False:
            upcoming_games.append(g)
    invites = user.team_invites.all()
    game_invites = user.game_invites.all()

    team_accept = request.POST.get("Accept")  # accept-val = "team-id#invite-id"
    team_decline = request.POST.get("Decline")
    game_accept = request.POST.get("Accept Game")
    game_decline = request.POST.get("Decline Game")
    if request.method == "POST":
        # IF PLAYER ACCEPTS TEAM INVITE ADD PLAYER TO THE TEAM
        if team_accept:
            arr = team_accept.split("#")
            try:
                prev_team = user.team
            except:
                prev_team = None
            prev_team.players.remove(user)
            t1 = Team.objects.get(id=int(arr[0]))
            t1.players.add(user)
            user.team = t1
            user.save()
            t1.save()
            prev_team.save()
            inv = TeamInvite.objects.get(id=int(arr[1]))
            inv.delete()
        # IF PLAYER DECLINES TEAM INVITE DELETE TEAM INVITE
        if team_decline:
            arr = team_decline.split("#")
            inv = TeamInvite.objects.get(id=int(arr[1]))
            inv.delete()
        # IF TEAM ACCEPTS GAME INVITE CREATE GAME OBJECT
        if game_accept:
            # get the game invite and create game-object
            inv = GameInvite.objects.get(id=game_accept)
            game = Game.objects.create(team1=inv.from_team, team2=inv.to_team, year=inv.year,month=inv.month,day=inv.day,time=inv.time,location=inv.location,overs=inv.overs)
            game.team1.games.add(game)
            game.team2.games.add(game)
            game.save()
            # create stat-objects for each player in game
            for player in game.team1.players.all():
                stat_line = PlayerGameStat.objects.create(game=game, player=player)
                game.players_stats.add(stat_line)
            for player in game.team2.players.all():
                stat_line = PlayerGameStat.objects.create(game=game, player=player)
                game.players_stats.add(stat_line)
            game.save()
            print("Num stats: "+str(len(game.players_stats.all())))
            # add the game to players.game attribute
            for player in game.team1.players.all():
                player.games.add(game)
            for player in game.team2.players.all():
                player.games.add(game)
            player.save() 
            inv.delete()
        # IF TEAM DECLINES GAME INVITE DELETE INVITE
        if game_decline:
            inv = GameInvite.objects.get(id=game_decline)
            inv.delete()

    context = {"games":upcoming_games, "invites":invites, "game_invites":game_invites}
    return render(request, "base/home.html", context)
 
def player_career(request, pk):
    player = Player.objects.get(id=pk)
    if player.games_won == 0 or player.games_played == 0:
        win_percentage = 0
    else:
        win_percentage = round(player.games_won/player.games_played *100)
    context = {"pk":pk, "user":player, "win_percentage":win_percentage}
    return render(request, "base/career.html", context)

def team(request, pk):   # check is player doesn't have a team
    user = request.user
    try:
        team = Team.objects.get(id=pk)
    except:
        team = Team.objects.create(name="filler", filler=True)  # creating filler-team-obj for new user with no team
        user.team = team
        user.save()
        team.save()
        context = {"players":None, "team":team}
        return render(request, "base/team.html", context)

    if request.method == "POST":
        username = request.POST.get("username")
        player = Player.objects.get(username=username)
        team_invite = TeamInvite.objects.create(to_team=request.user.team)
        player.team_invites.add(team_invite)
        team_invite.save()

    players = team.players
    if team.games_played != 0 or team.games_played != 0:
        win_percentage = round(team.games_won/team.games_played *100)
    else:
        win_percentage = 0
    context = {"players":players.all(), "team":team, "win_percentage":win_percentage}
    return render(request, "base/team.html", context)

def create_team(request):
    if request.method == "POST":
        name = request.POST.get("team_name")
        if name != None:
            user = request.user
            t1 = Team.objects.create(name=name, captain=request.user)
            t1.players.add(user)
            t1.captain = user
            t1.save()
            user.team = t1
            user.save()
            return redirect("team", t1.id)
    context = {}
    return render(request, "base/create_team.html", context)

def game_history(request):
    user = request.user
    games = []
    for g in user.games.all():
        if g.doneStats == True:  # a game-object is completed if 
            games.append(g)
    context = {"games":games}
    return render(request, "base/game_history.html", context)

def view_game(request, pk): # game.vids
    print(request.POST) # if box is not checked its key/val pair will not show up in request.POST, and tis value is None
    user = request.user
    game = Game.objects.get(id=int(pk))
    print(request.POST)
    # IF A FORM WAS SUBMITTED
    if request.method == "POST":
        if request.POST.get("batted-first-innings") != None:   # filling with empty stat-objs
            print("SETTING ORDER OF GAME: " + str(int(request.POST.get("batted-first-innings"))))
            batted_first_innings_id = int(request.POST.get("batted-first-innings"))
            if game.team1.id == batted_first_innings_id:
                game.entering_stats = True
                game.batting1_team = game.team1 
                game.bowling1_team = game.team2
                game.batting2_team = game.team2
                game.bowling2_team = game.team1
                game.save()
            if game.team2.id == batted_first_innings_id:   # filling with empty stat-objs
                game.entering_stats = True
                game.batting1_team = game.team2
                game.bowling1_team = game.team1
                game.batting2_team = game.team1
                game.bowling2_team = game.team2
                game.save()
        # THIS INFORMATION SHOULD BE EXTRACTED WHEN THE FIRST GAME INFO FORM IS SUBMITTED, AND WHEN EACH BALL IS SUBMITTED
        if request.POST.get("on-strike") != None:
            on_strike_batsman = Player.objects.get(id=int(request.POST.get("on-strike")))
            game.on_strike_batsman = on_strike_batsman
            onstrike_game_stat = on_strike_batsman.get_game_stat(game)
        if request.POST.get("off-strike") != None:
            off_strike_batsman = Player.objects.get(id=int(request.POST.get("off-strike")))
            game.off_strike_batsman = off_strike_batsman
            off_strike_batsman.get_game_stat(game)
        if request.POST.get("current-bowler") != None:
            current_bowler = Player.objects.get(id=int(request.POST.get("current-bowler")))
            game.current_bowler = current_bowler
            bowler_game_stat = current_bowler.get_game_stat(game)
        game.save()


        # BATSMAN SCORED RUNS BY HTTING
        if request.POST.get("runs_scored") != None:         # TODO: update game stats/attributes
            print("RUNS HITTED")
            runs_scored = int(request.POST.get("runs_scored"))
            # PLAYER STATS
            onstrike_game_stat.runs_scored += runs_scored
            onstrike_game_stat.balls_batted += 1
            if runs_scored == 4:
                onstrike_game_stat.fours += 1
            if runs_scored == 6:
                onstrike_game_stat.sixes += 1
            
            bowler_game_stat.balls_bowled += 1
            bowler_game_stat.runs_given_up += runs_scored
            onstrike_game_stat.save()
            bowler_game_stat.save()
            
            # GAME STATS
            if game.current_innings == 1:
                game.batting_score1 += runs_scored
            elif game.current_innings == 1:
                game.batting_score2 += runs_scored
            set_ball_icon(game, str(runs_scored))
            increment_game(game)
            game.save()
        # BATSMAN SCORED RUNS BY RUNNING: 
        if request.POST.get("runs_ran") != None:
            print("RUNS RAN")
            # PLAYER STATS
            runs_ran = int(request.POST.get("runs_ran"))
            onstrike_game_stat.runs_ran += runs_ran
            onstrike_game_stat.balls_batted += 1
            bowler_game_stat.runs_given_up += 1
            bowler_game_stat.balls_bowled += 1 
            onstrike_game_stat.save()
            bowler_game_stat.save()
            # GAME STATS
            set_ball_icon(game, str(runs_ran))
            increment_game(game)
            if game.current_innings == 1:
                game.batting_score1 += runs_ran
            elif game.current_innings == 1:
                game.batting_score2 += runs_ran
            game.save()
        # BOWLER GOT WICKET, WIDE, NO-BALL
        if request.POST.get("other") != None:
            outcome =  request.POST.get("other")
            # PLAYER STATS
            if "wicket" in outcome:
                if outcome == "wicket-bowled":
                    onstrike_game_stat.out_type = "bowled "+str(current_bowler.username)
                if outcome == "wicket-lbw":
                    onstrike_game_stat.out_type = "LBW "+str(current_bowler.username)
                if outcome == "wicket-catch":
                    fielder = Player.objects.get(id=int(request.POST.get("fielder")))  # TODO: select fielder who caught 
                    fielder.catches += 1
                    onstrike_game_stat.out_type = "bowled "+str(current_bowler.username)+", catch " +str(fielder.username)

                bowler_game_stat.wickets += 1   
                bowler_game_stat.balls_bowled += 1  
                onstrike_game_stat.balls_batted += 1
                onstrike_game_stat.out_ball = game.current_ball
                onstrike_game_stat.out_over = game.current_over
                bowler_game_stat.save()
                onstrike_game_stat.save()
                # GAME STATS
                set_ball_icon(game, "W")
                increment_game(game)
                if game.current_innings == 1:
                    game.bowling_score1 += 1
                elif game.current_innings == 1:
                    game.bowling_score2 += 1
                game.save()
            if outcome == "wide":       # do not update ball/over number
                # PLAYER STATS
                bowler_game_stat.extras += 1
                bowler_game_stat.save()
            if outcome == "no-ball":         # do not update ball/over number
                bowler_game_stat.extras += 1
                bowler_game_stat.save()

        if request.POST.get("finish_game") != None:
            print("Finish the game")
            game.archived = True  # moves game to game_history
            game.save()
            game.update_players_career_stats
            game.confirm_winner
            game.update_players_win_percentage
            game.save()
            return redirect("home")

         # IF GAME HAS BEEN STARTED
        if game.entering_stats == False:
            print("GAME COMPLETED IS FALSE")
            context = {"game":game}
            return render(request, "base/view_game.html", context)

        context = {"game":game}
        return render(request, "base/view_game.html", context)
    
    context = {"game":game}
    return render(request, "base/view_game.html", context)
    

def increment_game(game):
    if game.current_ball < 6:
        game.current_ball += 1
        game.save()
        return 
    if game.current_ball == 6:
        print("6TH BALL")
        if game.current_over < game.overs:
            game.current_ball = 1 
            print("INCREMENT OVER")
            game.current_over += 1
            reset_over_icons(game)
            game.save()
            return
        if game.current_over == game.overs and game.current_innings == 2:     # if its the last ball and over game is over
            print("GAME END")
            game.doneStats = True # concludes stat entering of game-object
            game.save()
            return
        if game.current_over == game.overs and game.current_innings == 1:     # if its the last ball and over game is over
            print("INNINGS 1 END")
            game.current_innings = 2
            game.current_ball = 1
            game.current_over = 1
            reset_over_icons(game)
            game.save()
            return
def set_ball_icon(game, outcome):
    print("SET BALL ICON")
    if game.current_ball == 1:
        game.ball1 = outcome
    if game.current_ball == 2:
        game.ball2 = outcome
    if game.current_ball == 3:
        game.ball3 = outcome
    if game.current_ball == 4:
        game.ball4 = outcome
    if game.current_ball == 5:
        game.ball5 = outcome
    if game.current_ball == 6:
        game.ball6 = outcome
    game.save()
def reset_over_icons(game):
    print("RESETTING OVER ICONS")
    game.ball1 = "None"
    game.ball2 = "None"
    game.ball3 = "None"
    game.ball4 = "None"
    game.ball5 = "None"
    game.ball6 = "None"
    game.save()

def create_organization(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        org = Organization.objects.create(name=name, description=description, location=location)
        org.members.add(user)
        user.organization = org
        user.save()
        org.save()
    context = {}
    return render(request, "base/create_organization.html", context) 
def view_organization(request, pk):
    org = Organization.objects.get(id=int(pk))
    query_players = []
    if request.method == "POST":
        query = request.POST.get("search-players")
        if query != None and query != "":
            for p in Player.objects.all():
                if query.lower() in p.username.lower() or query.lower() in p.first_name.lower() or query.lower() in p.last_name.lower():
                    query_players.append(p)
        add_player_id = request.POST.get("add-player-org")
        if add_player_id != None:
            pass
            """player_to_add = Player.objects.get(id=int(add_player_id))
            player_to_add.organization = org
            org.members.add(player_to_add)
            org.save()
            player_to_add.save()"""

                    
    context = {"org":org, "query_players":query_players}
    return render(request, "base/view_organization.html", context) 

def schedule_game(request):
    user = request.user
    if request.method == "POST":
        opp_team = request.POST.get("opp-team")
        location = request.POST.get("address")
        year = request.POST.get("year")
        month = request.POST.get("month")
        day = request.POST.get("day")
        time = request.POST.get("time")
        overs = request.POST.get("overs")
        if opp_team != None and location != None and year != None and month != None and day != None and time != None:
            team2 = Team.objects.get(name=opp_team)
            invite = GameInvite.objects.create(from_team=user.team, to_team=team2, year=year,month=month,day=day,time=time,location=location,overs=overs)
            invite.save()
            for player in team2.players.all():
                player.game_invites.add(invite)
                player.save()
        return redirect("home")
    context = {}
    return render(request, "base/schedule_game.html", context)

def login_page(request):
    page = "login"
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = Player.objects.get(email=email)
        except:
            messages.error(request, "User no exist")

        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            print(user)
            messages.error(request, "Wrong info")

    context = {"page":page}
    return render(request, "base/login_register.html", context)

def register_page(request):
    page = "register"
    if request.method == "POST":
        first = request.POST.get("first-name")
        last = request.POST.get("last-name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if first != None and last != None and username != None and email != None and password1 != None and password2 != None and password1==password2:
            user= Player.objects.create(first_name=first,last_name=last,username=username.lower(),email=email,password=password1)
            team = Team.objects.create(name="filler", filler=True)  # creating filler-team-obj for new user with no team
            team.filler = True
            user.team = team
            user.save()
            team.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error has occured during registration")
    context = {"page":page}
    return render(request, "base/login_register.html", context)