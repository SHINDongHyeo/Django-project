from django.shortcuts import render
import json
from datetime import datetime, timedelta
import requests

# Create your views here.
def api_league(request, league_name):
    ###################################### api 호출로 변형되야 하는 부분
    # with open(f"C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/{league_name}.json", 'r', encoding='UTF8') as file:
    #     json_data = json.load(file)
    # with open(f"C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/{league_name}_standings.json", 'r', encoding='UTF8') as file:
    #     standings_data = json.load(file)
    # with open(f"C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/{league_name}_scorers.json", 'r', encoding='UTF8') as file:
    #     scorers_data = json.load(file)
    json_data = requests.get(f"http://api.football-data.org/v4/competitions/{league_name}/matches",
                             headers={
                                 'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                             }).json()

    
    standings_data = requests.get(f"http://api.football-data.org/v4/competitions/{league_name}/standings",
                             headers={
                                 'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                             }).json()

    
    scorers_data = requests.get(f"http://api.football-data.org/v4/competitions/{league_name}/scorers",
                             headers={
                                 'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                             }).json()

    #################################################################################################

    season = json_data["filters"]["season"] + " - " + str(int(json_data["filters"]["season"])+1)
    total_matches = json_data["resultSet"]["count"]
    total_matchday = json_data["resultSet"]["count"]//10
    current_matchday = ((json_data["resultSet"]["played"]-1)//10)+1
    played_match = json_data["resultSet"]["played"]
    bar_matchday = str(current_matchday/total_matchday*100)+"%"
    emblem = json_data["competition"]["emblem"]

    all_matches = json_data["matches"]
    for match in all_matches:
        utc_time = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
        kst_time = utc_time + timedelta(hours=8.5)
        kst_time_str = kst_time.strftime("%Y-%m-%d %H:%M:%S")
        split_time = kst_time_str.split(" ")
        match["kstDate"] = split_time[0]
        match["kstTime"] = split_time[1][:5]
    if league_name=="premier_league":
        league_name = "프리미어리그"
    elif league_name=="primera_league":
        league_name = "라리가"
    elif league_name=="bundesliga_league":
        league_name = "분데스리가"
    elif league_name=="ligue1_league":
        league_name = "리그앙"
    
    context = {
        'league_name':league_name,
        'season': season,
        'total_matches': total_matches,
        'total_matchday': total_matchday,
        'current_matchday': current_matchday,
        'played_match': played_match,
        'bar_matchday': bar_matchday,
        'all_matches': all_matches,
        'standings_data': standings_data,
        'scorers_data': scorers_data,
        'emblem':emblem,
    }
    return render(request, 'football/api_league.html', context=context)

def championship_league(request):
    ###################################### api 호출로 변형되야 하는 부분
    # with open("C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/championship_league.json", 'r', encoding='UTF8') as file:
    #     json_data = json.load(file)
    # with open("C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/championship_league_standings.json", 'r', encoding='UTF8') as file:
    #     standings_data = json.load(file)
    # with open("C:/Users/smdh1/OneDrive/바탕 화면/test/myproject/static/football/championship_league_scorers.json", 'r', encoding='UTF8') as file:
    #     scorers_data = json.load(file)
    json_data = requests.get("http://api.football-data.org/v4/competitions/CL/matches",
                            headers={
                                'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                            }).json()

    
    standings_data = requests.get("http://api.football-data.org/v4/competitions/CL/standings",
                             headers={
                                 'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                             }).json()

    
    scorers_data = requests.get("http://api.football-data.org/v4/competitions/CL/scorers",
                             headers={
                                 'X-Auth-Token': '73ebf45340e849478620192724b14f49',
                             }).json()
    #################################################################################################

    season = json_data["filters"]["season"] + " - " + str(int(json_data["filters"]["season"])+1)
    total_matches = json_data["resultSet"]["count"]
    total_matchday = json_data["resultSet"]["count"]//10
    current_matchday = ((json_data["resultSet"]["played"]-1)//10)+1
    played_match = json_data["resultSet"]["played"]
    bar_matchday = str(current_matchday/total_matchday*100)+"%"
    emblem = json_data["competition"]["emblem"]

    all_matches = json_data["matches"]
    for match in all_matches:
        utc_time = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
        kst_time = utc_time + timedelta(hours=8.5)
        kst_time_str = kst_time.strftime("%Y-%m-%d %H:%M:%S")
        split_time = kst_time_str.split(" ")
        match["kstDate"] = split_time[0]
        match["kstTime"] = split_time[1][:5]

    context = {
        'season': season,
        'total_matches': total_matches,
        'total_matchday': total_matchday,
        'current_matchday': current_matchday,
        'played_match': played_match,
        'bar_matchday': bar_matchday,
        'all_matches': all_matches,
        'standings_data': standings_data,
        'scorers_data': scorers_data,
        'emblem':emblem,
    }
    return render(request, 'football/championship_league.html', context=context)


def k1_league(request):

    context = {

    }
    return render(request, 'football/k1_league.html', context=context)

def k2_league(request):
    
    context = {
        
    }
    return render(request, 'football/k2_league.html', context=context)