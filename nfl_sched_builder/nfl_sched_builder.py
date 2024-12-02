import random
import sys

# NFL divisions and teams
NFL_TEAMS = {
    "AFC East": ["Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets"],
    "AFC North": ["Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers"],
    "AFC South": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
    "AFC West": ["Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers"],
    "NFC East": ["Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders"],
    "NFC North": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
    "NFC South": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
    "NFC West": ["Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"],
}

def get_team_division(team_name):
    """
    Return the division of the given team.
    
    Args:
        team_name: the name of the NFL team.
    """
    for division, teams in NFL_TEAMS.items():
        if team_name in teams:
            return division, teams
    raise ValueError(f"Team '{team_name}' not found in NFL team list.")

def assign_home_away(games, home_count):
    """
    Assign a "home" or "away" designation to a list of games, ensuring that the specified
    number of home games (home_count) and away games are properly distributed.

    Args:
        games: A list of opponents or games for which "home" or "away" assignments need
            to be made.
        home_count: The number of games that should be designated as home games.
    """
    home_games = random.sample(games, home_count)
    away_games = [game for game in games if game not in home_games]
    return [(game, "home") for game in home_games] + [(game, "away") for game in away_games]

def generate_schedule(team_name):
    """
    Generate an NFL schedule for the given team.
    
    Args:
        team_name: The name of the NFL team to build a schedule for.
    """
    # retrieve the team's division
    division, division_teams = get_team_division(team_name)
    
    # generate intra-division games (6 games, home and away)
    division_opponents = [team for team in division_teams if team != team_name]
    intra_division_games = [(team, "home") for team in division_opponents] + \
                           [(team, "away") for team in division_opponents]
    
    # randomly select one divisional opponent for Week 18
    week_18_opponent = random.choice(division_opponents)
    week_18_game = (week_18_opponent, random.choice(["home", "away"]))
    intra_division_games.remove((week_18_opponent, "home"))
    intra_division_games.remove((week_18_opponent, "away"))
    
    # generate intra-conference and inter-conference games
    conference = division.split()[0]
    other_conference = "NFC" if conference == "AFC" else "AFC"
    conference_divisions = [div for div in NFL_TEAMS if div.startswith(conference) and div != division]
    inter_conference_divisions = [div for div in NFL_TEAMS if div.startswith(other_conference)]
    
    intra_conference_division = random.choice(conference_divisions)
    inter_conference_division = random.choice(inter_conference_divisions)
    
    intra_conference_games = [team for team in NFL_TEAMS[intra_conference_division]]
    inter_conference_games = [team for team in NFL_TEAMS[inter_conference_division]]
    
    # generate 3 remaining games
    remaining_opponents = [
        team for div in conference_divisions if div != intra_conference_division
        for team in NFL_TEAMS[div]
    ]
    random.shuffle(remaining_opponents)
    other_games = remaining_opponents[:3]
    
    # combine all games excluding divisional games
    all_non_divisional_games = intra_conference_games + inter_conference_games + other_games
    
    # assign home/away for non-divisional games
    total_home_games = random.choice([8, 9])
    
    non_divisional_home_count = total_home_games - 3  # 3 divisional home games
    
    non_divisional_assignments = assign_home_away(
        all_non_divisional_games, non_divisional_home_count
    )
    
    # combine all games
    all_games = intra_division_games + non_divisional_assignments
    random.shuffle(all_games)
    
    # assign a bye week
    bye_week = random.randint(5, 14)
    
    # enforce bye week and Week 18
    full_schedule = []
    for week in range(1, 19):  # 18 weeks
        if week == bye_week:
            full_schedule.append(("Bye Week", "none"))
        elif week == 18:
            full_schedule.append(week_18_game)
        elif all_games:
            full_schedule.append(all_games.pop(0))
    
    schedule = {"schedule": full_schedule, "bye_week": bye_week}
    return schedule

def main():
    """
    Generate an 18-week schedule for an NFL team. Include divisional, intra-conference,
    and inter-conference games.
    """
    if len(sys.argv) != 2:
        print("Usage: python nfl_schedule_builder.py \"Team Name\"")
        sys.exit(1)
    
    team_name = sys.argv[1]
    try:
        schedule = generate_schedule(team_name)
        print(f"Schedule for {team_name}:")
        for week, (opponent, location) in enumerate(schedule["schedule"], 1):
            if opponent == "Bye Week":
                print(f"Week {week}: Bye Week")
            else:
                print(f"Week {week}: {opponent} ({location})")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
