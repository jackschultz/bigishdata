import requests
from bs4 import BeautifulSoup
import csv
import urllib
import json

'''
base_url = "http://www.pgatour.com/data/r/"

def links_that_are_numbers(base_url):
    links = []
    page = requests.get(base_url)
    html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
    for link in html.find_all("a"):
        try:
            link_num_str = link["href"][0:-1]
            link_number = int(link_num_str)
            link_url = base_url + link_num_str #want the string since it has leading 0s
            links.append(link_url)
        except ValueError:
            pass
    return links

def has_teetimes_and_scores(year_url):
    teetimes = "teetimes.json"
    leaderboard = "leaderboard.json"
    page = requests.get(year_url)
    html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
    teetime_page = html.find("a", href=teetimes)
    leaderboard_page = html.find("a", href=leaderboard)
    return True if teetime_page and leaderboard_page else False

#Grab the tournament urls
tournament_urls = links_that_are_numbers(base_url)

valid_tournaments = []
#grab pages for each year that the tournament existed
for tournament_url in tournament_urls:
    year_urls = links_that_are_numbers(tournament_url + '/')
    for year_url in year_urls:
        if has_teetimes_and_scores(year_url):
            #now we can analyze
            print year_url
            valid_tournaments.append(year_url)
'''
#don't want to use a db here, so gonna pickle the correct years
asdf = [
'http://www.pgatour.com/data/r/002/2',
'http://www.pgatour.com/data/r/002/3',
'http://www.pgatour.com/data/r/002/2014',
'http://www.pgatour.com/data/r/002/2015',
'http://www.pgatour.com/data/r/002/2016',
'http://www.pgatour.com/data/r/003/2014',
'http://www.pgatour.com/data/r/003/2015',
'http://www.pgatour.com/data/r/003/2016',
'http://www.pgatour.com/data/r/004/2014',
'http://www.pgatour.com/data/r/004/2015',
'http://www.pgatour.com/data/r/004/2016',
'http://www.pgatour.com/data/r/005/2',
'http://www.pgatour.com/data/r/005/2014',
'http://www.pgatour.com/data/r/005/2015',
'http://www.pgatour.com/data/r/005/2016',
'http://www.pgatour.com/data/r/006/2015',
'http://www.pgatour.com/data/r/006/2016',
'http://www.pgatour.com/data/r/007/2014',
'http://www.pgatour.com/data/r/007/2015',
'http://www.pgatour.com/data/r/007/2016',
'http://www.pgatour.com/data/r/009/2014',
'http://www.pgatour.com/data/r/009/2015',
'http://www.pgatour.com/data/r/009/2016',
'http://www.pgatour.com/data/r/010/2014',
'http://www.pgatour.com/data/r/010/2015',
'http://www.pgatour.com/data/r/010/2016',
'http://www.pgatour.com/data/r/011/2014',
'http://www.pgatour.com/data/r/011/2015',
'http://www.pgatour.com/data/r/011/2016',
'http://www.pgatour.com/data/r/012/2014',
'http://www.pgatour.com/data/r/012/2015',
'http://www.pgatour.com/data/r/012/2016',
'http://www.pgatour.com/data/r/013/2014',
'http://www.pgatour.com/data/r/013/2015',
'http://www.pgatour.com/data/r/014/2014',
'http://www.pgatour.com/data/r/014/2015',
'http://www.pgatour.com/data/r/014/2016',
'http://www.pgatour.com/data/r/016/2015',
'http://www.pgatour.com/data/r/016/2016',
'http://www.pgatour.com/data/r/018/2014',
'http://www.pgatour.com/data/r/018/2015',
'http://www.pgatour.com/data/r/018/2016',
'http://www.pgatour.com/data/r/019/2014',
'http://www.pgatour.com/data/r/019/2015',
'http://www.pgatour.com/data/r/019/2016',
'http://www.pgatour.com/data/r/020/2014',
'http://www.pgatour.com/data/r/020/2015',
'http://www.pgatour.com/data/r/020/2016',
'http://www.pgatour.com/data/r/021/2014',
'http://www.pgatour.com/data/r/021/2015',
'http://www.pgatour.com/data/r/021/2016',
'http://www.pgatour.com/data/r/023/2014',
'http://www.pgatour.com/data/r/023/2015',
'http://www.pgatour.com/data/r/023/2016',
'http://www.pgatour.com/data/r/025/2014',
'http://www.pgatour.com/data/r/025/2015',
'http://www.pgatour.com/data/r/025/2016',
'http://www.pgatour.com/data/r/026/2014',
'http://www.pgatour.com/data/r/026/2015',
'http://www.pgatour.com/data/r/026/2016',
'http://www.pgatour.com/data/r/027/2014',
'http://www.pgatour.com/data/r/027/2015',
'http://www.pgatour.com/data/r/028/2014',
'http://www.pgatour.com/data/r/028/2015',
'http://www.pgatour.com/data/r/030/2014',
'http://www.pgatour.com/data/r/030/2015',
'http://www.pgatour.com/data/r/030/2016',
'http://www.pgatour.com/data/r/032/2014',
'http://www.pgatour.com/data/r/032/2015',
'http://www.pgatour.com/data/r/032/2016',
'http://www.pgatour.com/data/r/033/2014',
'http://www.pgatour.com/data/r/033/2015',
'http://www.pgatour.com/data/r/033/2016',
'http://www.pgatour.com/data/r/034/2014',
'http://www.pgatour.com/data/r/034/2015',
'http://www.pgatour.com/data/r/034/2016',
'http://www.pgatour.com/data/r/041/2014',
'http://www.pgatour.com/data/r/041/2015',
'http://www.pgatour.com/data/r/041/2016',
'http://www.pgatour.com/data/r/047/2015',
'http://www.pgatour.com/data/r/047/2016',
'http://www.pgatour.com/data/r/054/2015',
'http://www.pgatour.com/data/r/054/2016',
'http://www.pgatour.com/data/r/060/2014',
'http://www.pgatour.com/data/r/060/2015',
'http://www.pgatour.com/data/r/100/2014',
'http://www.pgatour.com/data/r/100/2015',
'http://www.pgatour.com/data/r/100/2016',
'http://www.pgatour.com/data/r/457/2015',
'http://www.pgatour.com/data/r/457/2016',
'http://www.pgatour.com/data/r/464/2015',
'http://www.pgatour.com/data/r/464/2016',
'http://www.pgatour.com/data/r/471/2014',
'http://www.pgatour.com/data/r/471/2015',
'http://www.pgatour.com/data/r/471/2016',
'http://www.pgatour.com/data/r/472/2014',
'http://www.pgatour.com/data/r/472/2015',
'http://www.pgatour.com/data/r/472/2016',
'http://www.pgatour.com/data/r/473/2014',
'http://www.pgatour.com/data/r/473/2015',
'http://www.pgatour.com/data/r/473/2016',
'http://www.pgatour.com/data/r/475/2014',
'http://www.pgatour.com/data/r/475/2015',
'http://www.pgatour.com/data/r/475/2016',
'http://www.pgatour.com/data/r/476/2014',
'http://www.pgatour.com/data/r/476/2015',
'http://www.pgatour.com/data/r/476/2016',
'http://www.pgatour.com/data/r/478/2015',
'http://www.pgatour.com/data/r/478/2016',
'http://www.pgatour.com/data/r/480/2014',
'http://www.pgatour.com/data/r/480/2015',
'http://www.pgatour.com/data/r/480/2016',
'http://www.pgatour.com/data/r/483/2014',
'http://www.pgatour.com/data/r/483/2015',
'http://www.pgatour.com/data/r/483/2016',
'http://www.pgatour.com/data/r/489/2015',
'http://www.pgatour.com/data/r/489/2016',
'http://www.pgatour.com/data/r/490/2014',
'http://www.pgatour.com/data/r/490/2015',
'http://www.pgatour.com/data/r/493/2015',
'http://www.pgatour.com/data/r/493/2016',
'http://www.pgatour.com/data/r/494/2015',
'http://www.pgatour.com/data/r/494/2016',
'http://www.pgatour.com/data/r/500/2015',
'http://www.pgatour.com/data/r/505/2014',
'http://www.pgatour.com/data/r/505/2015',
'http://www.pgatour.com/data/r/518/2015',
'http://www.pgatour.com/data/r/518/2016',
'http://www.pgatour.com/data/r/519/2016'
]

averages = []
for url in asdf:
    print url
    teetimes_url = url + "/teetimes.json"
    leaderboard_url = url + "/leaderboard.json"
    teetimes_page = requests.get(teetimes_url)
    teetime_json = json.loads(teetimes_page.text)
    leaderboard_page = requests.get(leaderboard_url)
    leaderboard_json = json.loads(leaderboard_page.text)

    players = {}
    #get dict of player id and whether or not they played in the morning
    for course in teetime_json['tournament']['rounds'][0]['courses']:
        for segment in course['segments']:
            for group in segment['groups']:
                for player in group['players']:
                    player_id = player['TournamentPlayerID']
                    wave = 0 if group['MorningStart'] == "Yes" else 1
                    players[player_id] = {'wave': wave}
    for player in leaderboard_json['lb']['pds']['p']:
        pid = player['id']
        scores = []
        for r in player['rs']['r']:
            round_number = r['rn']
            if round_number == '1' or round_number == '2':
                try:
                    scores.append(float((r['sc'])))
                except ValueError:
                    pass
        if len(scores) != 0:
            avg_score = sum(scores) / len(scores)
        if pid in players:
            players[pid]['avg'] = avg_score

    #wave average time
    wave_0 = []
    wave_1 = []
    for pid in players:
        player = players[pid]
        if 'avg' not in player:
            continue
        if player['wave'] == 0:
            wave_0.append(player['avg'])
        else:
            wave_1.append(player['avg'])
    if len(wave_0) != 0 and len(wave_1) != 0:
        wave_0_avg = sum(wave_0) / len(wave_0)
        wave_1_avg = sum(wave_1) / len(wave_1)
        diff = abs(wave_0_avg - wave_1_avg)
        data = (url, diff)
        averages.append(data)

averages.sort(key=lambda tup: tup[1]) #sort by biggest diff
for average in averages:
    print average
