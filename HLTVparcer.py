from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import itertools
import numpy as np
from collections import Counter
class Team:
    def __init__(self,href):
        self.href = href
        self.id = self.get_team_id()
        self.html_code = parsing_html_code(self.href)
        self.team_name = self.get_team_name()
        # self.world_rank = self.get_world_rank()
        # self.winrate = self.get_winrate()
        # self.current_streak = self.get_current_streak()
        # self.maps_stat = self.get_stats_maps()
    
    def get_team_id(self):
        #https://www.hltv.org/team/9565/vitality
        id = self.href.split('/')[4]
        return id
 
 
    def get_team_name(self):
        try:
            team_name = str(self.html_code.find('h1', {'class':'profile-team-name'})).split('>')[1].split('<')[0]
            return team_name
        except:
            print('Cant get team name')
            return None
 
    def get_world_rank(self):
        try:
            rank = int(str(self.html_code.find_all('div', {'class':'profile-team-stat'})).split('#')[1].split('<')[0])
            return rank
        except:
            print('Cant get world rank')
            return None
    def get_winrate(self):
        try:
            winrate = float(str(self.html_code.find_all('div', {'class':'stat'})[1]).split('>')[1].split('%')[0])
            return winrate
        except:
            print('Cant get winrate')
            return None
    def get_current_streak(self):
        try:
            streak = int(str(self.html_code.find_all('div', {'class':'stat'})[0]).split('>')[1].split('<')[0])
            return streak
        except:
            print('Cant get current streak')
            return None
    def get_stats_maps(self):
        try:
            maps = self.html_code.find_all('div', {'class':'map-statistics-row'})
            maps_dict = dict()
            for item in maps:
                map_name = str(item.find('div', {'class':'map-statistics-row-map-mapname'})).split('>')[1].split('<')[0]
                map_wr = float(str(item.find('div', {'class':'map-statistics-row-win-percentage'})).split('>')[1].split('%')[0])
                maps_dict[map_name] = map_wr
            return maps_dict
        except:
            print('Cant get maps statistic')
            return None
def filter_non_unique(lst):
    return [item for item, count in Counter(lst).items() if count ==1]
 
def parsing_html_code(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        r = requests.get(url, headers=headers)
        requiredHtml = r.text
        soup = BeautifulSoup(requiredHtml, 'html5lib')
        return soup
    except:
        print('Cant get html code')
def convert_date(date):
    #list_dates = ['january','february','march','april','may','june','july','august','september','october','november','december']
    date = date.split('/')
    # if date[1] !=10:
    #     date[1] = int(date[1].replace('0',''))-1
    
    date_int = [int(date[0])-1, int(date[1]),int(date[2])]
    new_date = chek_date(date_int,0)
    past_date = new_date
    past_date = past_date.split('-')
    past_date[1] = int(date_int[1])-3
    past_date = chek_date(past_date,1)
    
    return [past_date, new_date]
 
def chek_date(date,flag):
    if flag == 0:
 
        if int(date[0]) <= 0:
            date[0] = 28
            date[1] = int(date[1])-1
            if date[1] == 0:
                date[1] = 12
                date[2] = int(date[2])-1
 
        if int(date[1]) <= 0:
                date[1] = 12
                date[2] = int(date[2])-1
        
        if int(date[0]) < 10:
            date[0] = '0'+str(date[0])
        if int(date[1]) < 10:
            date[1] = '0'+str(date[1])
        if int(date[2]) < 10:
            date[2] = '0'+str(date[2])    
        date[0] = str(date[0])
        date[1] = str(date[1])
        if len(str(date[2]))==2:
            date[2] = '20'+str(date[2])
 
        new_date = [date[2],date[1],date[0]]
        new_date = '-'.join(new_date)
 
        return new_date
 
    if flag == 1:
                
        if int(date[1]) <= 0:
                date[1] = 12
                date[0] = int(date[0])-1
 
        if int(date[1]) < 10:
            date[1] = '0'+str(date[1])
    
        date[0] = str(date[0])
        date[1] = str(date[1])
 
        new_date = [date[0],date[1],date[2]]
        new_date = '-'.join(new_date)
 
        return new_date
 
def parse_head_to_head_stat(team1,team2):
    try:
        href = 'https://www.hltv.org/results?team={}&team={}&requireAllTeams='.format(team1.id,team2.id)
        html_code = parsing_html_code(href)
        result = html_code.findAll('div', {'class':'result'})
        winner = str()
        result_dict = {team1.team_name:0,team2.team_name:0}
 
        for item in result:
            teams = item.findAll('div', {'class':'team'})
            scores = item.find('td', {'class':'result-score'})
 
            team1 = str(teams[0]).split('>')[1].split('<')[0]
            team2 = str(teams[1]).split('>')[1].split('<')[0]
 
            score1 = str(scores).split('</span>')[0].split('>')[-1]
            score2 = str(scores).split('</span>')[1].split('>')[-1]
            if score1>score2:
                winner = team1
            else:
                winner = team2
            result_dict[winner] += 1
        return result_dict
    except:
        print('cant parse head to head')
        return None
def get_team_map_stat(Team, Map):
    try:
        href = 'https://www.hltv.org/stats/teams/map/{}/{}/{}?startDate=2019-10-28&endDate=2020-10-28'.format(Map[1],Team.id, Team.team_name)
        html_code = parsing_html_code(href)
        result = html_code.find('table', {'class':'stats-table'}).find('tbody').findAll('tr')
        winner = int()
        final_list =[]
        try:
            for item in result:
                try:
                    full_row = item.findAll('td')
                    date = convert_date(str(full_row[0]).split('>')[2].split('<')[0])
                    opponent = str(full_row[1].find('span')).split('>')[1].split('<')[0]
                    score = str(full_row[3]).split('>')[1].split('<')[0].replace(' ', '').split('-')
                    if int(score[0])>int(score[1]):
                        winner = 1
                    else:
                        winner = 0
                    
                    match_code = parsing_html_code('https://www.hltv.org'+str(full_row[0].find('a').get('href')))
                    team1_name = str(match_code.find('div', {'class':'team-left'}).find('a')).split('>')[1].split('<')[0]
                    team2_name = str(match_code.find('div', {'class':'team-right'}).find('a')).split('>')[1].split('<')[0]
                    team1_ref_h = str(match_code.find('div', {'class':'team-left'}).find('a').get('href')).split('?')[0]+'?startDate={}&endDate={}'.format(date[0],date[1])
                    team2_ref_h = str(match_code.find('div', {'class':'team-right'}).find('a').get('href')).split('?')[0]+'?startDate={}&endDate={}'.format(date[0],date[1])
                    print('new_match')
                    print(team1_name,team2_name,Map[0])
                    #https://www.hltv.org/stats/teams/matches/9565/Vitality?startDate=2020-06-11&endDate=2020-09-11
    
                    ref_h_team1 = team1_ref_h.split('/')
                    ref_h_team1[2] = ref_h_team1[2]+'/matches'
                    ref_h_team1 = '/'.join(ref_h_team1)
    
                    ref_h_team2 = team2_ref_h.split('/')
                    ref_h_team2[2] = ref_h_team2[2]+'/matches'
                    ref_h_team2 = '/'.join(ref_h_team2)
                    # try:
                    #     TPI1_code = parsing_html_code('https://www.hltv.org'+ref_h_team1).find('table',{'class':'stats-table no-sort'}).findAll('td',{'class':'text-center'})
                    #     TPI1_code = [TPI1_code[1],TPI1_code[3],TPI1_code[5],TPI1_code[7],TPI1_code[9]]
                    #     TPI1 = []
                    #     for item in TPI1_code:
                    #         item = str(item).split('>')[1].split('<')[0]
                    #         if item == 'L':
                    #             item = 0
                    #         else:
                    #             item = 1
                    #         TPI1.append(item)
                    #     TPI1 = 5*int(TPI1[0])+4*int(TPI1[1])+3*int(TPI1[2])+2*int(TPI1[3])+1*int(TPI1[4])
                    #     #print(TPI1)
                    # except:
                    #     TPI1 = None
                    # try:
                    #     TPI2_code = parsing_html_code('https://www.hltv.org'+ref_h_team2).find('table',{'class':'stats-table no-sort'}).findAll('td',{'class':'text-center'})
                    #     TPI2_code = [TPI2_code[1],TPI2_code[3],TPI2_code[5],TPI2_code[7],TPI2_code[9]]
                    #     TPI2 = []
                    #     for item in TPI2_code:
                    #         item = str(item).split('>')[1].split('<')[0]
                    #         if item == 'L':
                    #             item = 0
                    #         else:
                    #             item = 1
                    #         TPI2.append(item)
                    #     TPI2 = 5*int(TPI2[0])+4*int(TPI2[1])+3*int(TPI2[2])+2*int(TPI2[3])+1*int(TPI2[4])
                    # #print(TPI2)
                    # except:
                    #     TPI2 = None
    
                    ref_h_team1 = ref_h_team1.split('/')
                    ref_h_team1[-1] = ref_h_team1[-1]+'&maps={}'.format(Map[0])
                    ref_h_team1 = '/'.join(ref_h_team1)
    
                    ref_h_team2 = ref_h_team2.split('/')
                    ref_h_team2[-1] = ref_h_team2[-1]+'&maps={}'.format(Map[0])
                    ref_h_team2 = '/'.join(ref_h_team2)
                    #tpi map
                    try:
                        TPI1_code = parsing_html_code('https://www.hltv.org'+ref_h_team1).find('table',{'class':'stats-table no-sort'}).findAll('td',{'class':'text-center'})
                        TPI1_code = [TPI1_code[1],TPI1_code[3],TPI1_code[5],TPI1_code[7],TPI1_code[9]]
                        TPI1_map = []
                        for item in TPI1_code:
                            item = str(item).split('>')[1].split('<')[0]
                            if item == 'L':
                                item = 0
                            else:
                                item = 1
                            TPI1_map.append(item)
                        TPI1_map = 2*int(TPI1_map[0])+int(TPI1_map[1])+int(TPI1_map[2])
                    except:
                        TPI1_map = None
                    try:
                        TPI2_code = parsing_html_code('https://www.hltv.org'+ref_h_team2).find('table',{'class':'stats-table no-sort'}).findAll('td',{'class':'text-center'})
                        TPI2_code = [TPI2_code[1],TPI2_code[3],TPI2_code[5],TPI2_code[7],TPI2_code[9]]
                        TPI2_map = []
                        for item in TPI2_code:
                            item = str(item).split('>')[1].split('<')[0]
                            if item == 'L':
                                item = 0
                            else:
                                item = 1
                            TPI2_map.append(item)
                        TPI2_map = 2*int(TPI2_map[0])+int(TPI2_map[1])+int(TPI2_map[2])
                    except:
                        TPI2_map = None
    
                    ref = str(match_code.find('a',{'class':'match-page-link button'}).get('href'))
                    print(ref)
                    match_code = parsing_html_code('https://www.hltv.org'+ref)
                    head_to_head = match_code.find('div',{'class':'head-to-head'}).findAll('div', {'class':'bold'})
                    wins_hh_team1 = int(str(head_to_head[0]).split('>')[1].split('<')[0])
                    wins_hh_team2 = int(str(head_to_head[2]).split('>')[1].split('<')[0])
                    if int(wins_hh_team1) <=0:
                        (wins_hh_team1) = 1
                    if int(wins_hh_team2) <=0:
                        (wins_hh_team2) = 1
                    world_ranks = match_code.findAll('div',{'class':'teamRanking'})
                    world_rank_team1_h = int(str(world_ranks[0].find('a')).split('#')[1].split('<')[0])
                    world_rank_team2_h = int(str(world_ranks[1].find('a')).split('#')[1].split('<')[0])
                    
                    players_rating = match_code.findAll('td',{'class':'player'})
                    players = []
                    for player in players_rating:
                        player = player.find('a').get('href')
                        players.append(player)
                    team1 = []
                    team2 = []
                    for item in players[0:5]:
                        team1.append(item)
                    for item in players[10:15]:
                        team2.append(item)
                    team1_full = []
                    team2_full = []
                    for player in team1:
                        player = str(player).split('/')
                        player[0] = '/stats'
                        player[1] = player[1]+'s'
                        player = '/'.join(player)+'?startDate={}&endDate={}'.format(date[0],date[1])
                        team1_full.append(player)
                    
                    
                    for player in team2:
                        player = str(player).split('/')
                        player[0] = '/stats'
                        player[1] = player[1]+'s'
                        player = '/'.join(player)+'?startDate={}&endDate={}'.format(date[0],date[1])
                        team2_full.append(player)
                    
    
                    team1_rating20 = 0
                    team2_rating20 = 0    
                    for player in team1_full:
                        code = parsing_html_code('https://www.hltv.org'+player)
                        rating = str(code.findAll('div', {'class':'stats-row'})[-1]).split('</span>')[1].split('>')[1]
                        team1_rating20 +=round(float(rating),3)
    
                    for player in team2_full:
                        code = parsing_html_code('https://www.hltv.org'+player)
                        rating = str(code.findAll('div', {'class':'stats-row'})[-1]).split('</span>')[1].split('>')[1]
                        team2_rating20 +=round(float(rating),3)
    
                    if Team.team_name == team1_name:
                        team1_players_rating = team1_rating20
                        team2_players_rating = team2_rating20
                        team1_ref = team1_ref_h
                        team2_ref = team2_ref_h
                        wins_map_team1 = wins_hh_team1
                        wins_map_team2 = wins_hh_team2
                        world_rank_team1 = world_rank_team1_h
                        world_rank_team2 = world_rank_team2_h
                        # TPI_team1 = TPI1
                        # TPI_team2 = TPI2
                        TPI_team1_map = TPI1_map
                        TPI_team2_map = TPI2_map
    
                    else:
                        team1_players_rating = team2_rating20
                        team2_players_rating = team1_rating20
                        team1_ref = team2_ref_h
                        team2_ref = team1_ref_h
                        wins_map_team1 = wins_hh_team2
                        wins_map_team2 = wins_hh_team1
                        world_rank_team1 = world_rank_team2_h
                        world_rank_team2 = world_rank_team1_h
                        # TPI_team1 = TPI2
                        # TPI_team2 = TPI1
                        TPI_team1_map = TPI2_map
                        TPI_team2_map = TPI1_map
    
                    head_to_head_team1 = wins_map_team1/wins_map_team2
                    head_to_head_team2 = wins_map_team2/wins_map_team1
                    
                    #print(TPI1,TPI2)
                    #print(TPI1_map,TPI2_map)
                    
                    
                
                    team1_map_ref = team1_ref.split('/')
                    team1_map_ref[2] = team1_map_ref[2]+'/map/{}'.format(Map[1])
                    team1_map_ref = '/'.join(team1_map_ref)
    
                    team2_map_ref = team2_ref.split('/')
                    team2_map_ref[2] = team2_map_ref[2]+'/map/{}'.format(Map[1])
                    team2_map_ref = '/'.join(team2_map_ref)
                    #print(team1_map_ref,team2_map_ref)
    
                    #team1 stat
                    team1_map_code = parsing_html_code('https://www.hltv.org'+team1_map_ref)
                    team1_stat_map = team1_map_code.findAll('div', {'class':'stats-row'})
                    team1_results = str(team1_stat_map[1]).split('</span>')[1].split('<span>')[1].replace(' ','').split('/')
                    #first_kill_death = team1_map_code.findAll('div',{'class':'large-strong'})
    
                    team1_code = parsing_html_code('https://www.hltv.org'+team1_ref)
                    team1_stat = team1_code.findAll('div', {'class':'large-strong'})
                    team1_full_results = str(team1_stat[1]).split('>')[1].split('<')[0].replace(' ','').split('/')
    
    
                    team1_map_wins =int(team1_results[0])
                    team1_map_draws =int(team1_results[1])
                    team1_map_losses =int(team1_results[2])
                    team1_wr_map = round(float(str(team1_stat_map[4]).split('</span>')[1].split('>')[1].replace('%','')),3)
                    #print(team1_map_wins,team1_map_draws,team1_map_losses,team1_wr_map)
                    Map_success_index_team1 =(team1_map_wins+team1_map_draws+team1_map_losses)*team1_wr_map/100
                    #print(Map_success_index_team1)
                    team1_map_total_rounds = str(team1_stat_map[2]).split('</span>')[1].split('<span>')[1]
                    team1_map_total_rounds_won = str(team1_stat_map[3]).split('</span>')[1].split('<span>')[1]
                    if int(team1_map_total_rounds) <=0:
                        team1_map_total_rounds = 1
                    Map_success_index_round_team1 =int(team1_map_total_rounds_won)/int(team1_map_total_rounds)*team1_wr_map/100
                    #print(Map_success_index_round_team1)
                    
                    # team1_a_win_after_getting_first_kill = str(first_kill_death[0]).split('>')[1].split('%')[0]
                    # team1_a_round_win_after_receiving_first_kill = str(first_kill_death[1]).split('>')[1].split('%')[0]
                    # team1_total_maps_played = str(team1_stat[0]).split('>')[1].split('<')[0]
                    # team1_wins =team1_full_results[0]
                    # team1_draws =team1_full_results[1]
                    # team1_losses =team1_full_results[2]
                    # team1_total_kills = str(team1_stat[2]).split('>')[1].split('<')[0]
                    # team1_total_deaths = str(team1_stat[3]).split('>')[1].split('<')[0]
                    # team1_total_rounds_played = str(team1_stat[4]).split('>')[1].split('<')[0]
                    # team1_total_kda = str(team1_stat[5]).split('>')[1].split('<')[0]
    
                    #team2 stat
                    team2_map_code = parsing_html_code('https://www.hltv.org'+team2_map_ref)
                    team2_stat_map = team2_map_code.findAll('div', {'class':'stats-row'})
                    team2_results = str(team2_stat_map[1]).split('</span>')[1].split('<span>')[1].replace(' ','').split('/')
                    #first_kill_death = team2_map_code.findAll('div',{'class':'large-strong'})
    
                    team2_code = parsing_html_code('https://www.hltv.org'+team2_ref)
                    team2_stat = team2_code.findAll('div', {'class':'large-strong'})
                    team2_full_results = str(team2_stat[1]).split('>')[1].split('<')[0].replace(' ','').split('/')
    
    
                    team2_map_wins =int(team2_results[0])
                    team2_map_draws =int(team2_results[1])
                    team2_map_losses =int(team2_results[2])
                    team2_wr_map = round(float(str(team2_stat_map[4]).split('</span>')[1].split('>')[1].replace('%','')),3)
                    #print(team2_map_wins,team2_map_draws,team2_map_losses,team2_wr_map)
                    Map_success_index_team2 =(team2_map_wins+team2_map_draws+team2_map_losses)*team2_wr_map/100
                    #print(Map_success_index_team2)
                    team2_map_total_rounds = str(team2_stat_map[2]).split('</span>')[1].split('<span>')[1]
                    team2_map_total_rounds_won = str(team2_stat_map[3]).split('</span>')[1].split('<span>')[1]
                    if int(team2_map_total_rounds) <=0:
                        team2_map_total_rounds = 1
                    Map_success_index_round_team2 =int(team2_map_total_rounds_won)/int(team2_map_total_rounds)*team2_wr_map/100
                    #print(Map_success_index_round_team2)
    
                    final_list.append([
                                    Map[0],
                                    Team.team_name,world_rank_team1, team1_wr_map, TPI_team1_map, head_to_head_team1,
                                    opponent,world_rank_team2, team2_wr_map, TPI_team1_map,head_to_head_team1,
                                    winner])
                    help_list = [str(Map[0]),
                                    str(Team.team_name),str(world_rank_team1),str(round(team1_wr_map,3)), str(round(TPI_team1_map,3)), str(round(head_to_head_team1,3)),
                                    str(opponent),str(world_rank_team2),str(round(team2_wr_map,3)), str(round(TPI_team2_map,3)), str(round(head_to_head_team2,3)),
                                    str(winner),
                                    ]
                                    #map, team, world_rank, wr_map, tpi_map, head_to_head
                    help_list = ','.join(help_list)
                    print(help_list)
                    try:
                        with open('Spirit.csv','a') as fd:
                            fd.write('\n'+help_list)
                    except:
                        print('cant write to csv')
                except:
                    final_list.append([])
        except:
            final_list = []
 
        return final_list
 
            # team2_map_total_rounds = str(team2_stat_map[2]).split('</span>')[1].split('<span>')[1]
            # team2_map_total_rounds_won = str(team2_stat_map[3]).split('</span>')[1].split('<span>')[1]
            # team2_wr_map = str(team2_stat_map[4]).split('</span>')[1].split('>')[1].replace('%','')
            # team2_a_win_after_getting_first_kill = str(first_kill_death[0]).split('>')[1].split('%')[0]
            # team2_a_round_win_after_receiving_first_kill = str(first_kill_death[1]).split('>')[1].split('%')[0]
            # team2_total_maps_played = str(team2_stat[0]).split('>')[1].split('<')[0]
            # team2_wins =team2_full_results[0]
            # team2_draws =team2_full_results[1]
            # team2_losses =team2_full_results[2]
            # team2_total_kills = str(team2_stat[2]).split('>')[1].split('<')[0]
            # team2_total_deaths = str(team2_stat[3]).split('>')[1].split('<')[0]
            # team2_total_rounds_played = str(team2_stat[4]).split('>')[1].split('<')[0]
            # team2_total_kda = str(team2_stat[5]).split('>')[1].split('<')[0]
 
            
    except:
        print('error')
        final_list=[]
        return final_list
        # match_code = parsing_html_code('https://www.hltv.org'+str(full_row[0].find('a').get('href')))
        # ref = str(match_code.find('a',{'class':'match-page-link button'}).get('href'))
        # team_rating = str(match_code.findAll('div',{'class':'match-info-row'})[1].find('div',{'class':'right'})).split('>')[1].split('<')[0].replace(' ', '').split(':')
        # name1 = match_code.find('div', {'class':'team-left'}).find('a')
        # name2 = match_code.find('div', {'class':'team-right'}).find('a')
        # print(ref)
        # print(team_rating)
        # print(name1,name2)
        #help_date = date.split('/')
        # for item in hltv_raiting:
        #     item = item[0].split('/')
        #     if item[0]==help_date[0] and item[1]==help_date[1]:
        #         html_code = item[1]
        #     else:
        #         html_code = hltv_raiting[0][0]
        # dict_team_rating = dict()
        # for item in html_code:
        #     name = str(item.find('span',{'class':'name'})).split('>')[1].split('<')[0]
        #     rating = str(item.find('span',{'class':'position'})).split('#')[1].split('<')[0]
        #     dict_team_rating[name] = rating
        # try:
        #     rank_team1 = dict_team_rating[Team.team_name]
        # except:
        #     rank_team1 = None
        # try:
        #     rank_team2 = dict_team_rating[opponent]
        # except:
        #     rank_team2 = None
        
        #final_list.append([Team.team_name,opponent,rank_team1,rank_team2,Map[0],score[0], score[1],winner])
        #final_list.append([Team.team_name,opponent,Map[0],score[0], score[1],winner])
        
    
 
def create_DataFrame_teams():
    try:
        main_data = pd.DataFrame(index = ['World rank', 'Winrate', 'Streak', 'Maps'])
        for item in teams:
            #data = {'World_rank': item.world_rank, 'Winrate': item.winrate, 'Streak': item.current_streak, 'Maps_stat':item.maps_stat}
            data = {item.team_name :{'World rank': item.world_rank, 'Winrate': item.winrate, 'Streak': item.current_streak, 'Maps':item.maps_stat}}
            data = pd.DataFrame(data)
            data = data.reindex(['World rank', 'Winrate', 'Streak','Maps'])
            main_data = main_data.join(data)
            #fromat table
            ##              team1   team2
            ## World rank   1       5
            ## Winrate      50      70
            ## Streak       2       0
            ## Maps         {}      {}
        return main_data
    except:
        print('Cant create Dataframe teams')
 
def create_DataFrame_results():
    try:
        list_teams = []
        for item in teams:
            list_teams.append(item.team_name)
        main_data = pd.DataFrame(index = list_teams, columns= list_teams)
 
        for team1, team2 in itertools.combinations(teams, 2):
            data = parse_head_to_head_stat(team1,team2)
            values = [data[team1.team_name],data[team2.team_name]]
            main_data[team2.team_name][team1.team_name] = [values[0],values[1]]
            main_data[team1.team_name][team2.team_name] = [values[1],values[0]]
        #fromat table
            ##              team1               team 2
            ## team1         NaN                [wins team1, wins team2]
            ## team2        [wins team2, 
            #               wins team1]                  NaN
        return main_data
    except:
        print('Cant create DataFrame results')
 
 
def create_DataFrame_map():
    test_list = []
    for team in teams:
        for csmap in maps:
            try:
                data = get_team_map_stat(team,csmap)
            except:
                print('error cant map+team item')
            try:
                for item in data:
                    try:
                        test_list.append(item)
                    except:
                        print('cant add item to csv')
            except:
                print('cant iter item')
    #main_data = pd.DataFrame(test_list, columns=['Team A','Team B','Rank A','Rank B', 'Map', 'Score A', 'Score B', 'Result'])
    main_data = pd.DataFrame(test_list, columns=[
 
                    # final_list.append([
                    #         Map[0],
                    #         Team.team_name,world_rank_team1,team1_players_rating,Map_success_index_team1,Map_success_index_round_team1,head_to_head_team1,TPI1,TPI1_map,
                    #         opponent,world_rank_team2,team2_players_rating,Map_success_index_team2,Map_success_index_round_team2,head_to_head_team2,TPI2,TPI2_map,
                    #         winner])
        'map',
        'team1','world_rank_team1','team1_players_rating','Map_success_index_team1','Map_success_index_round_team1','head_to_head_team1','TPI1','TPI1_map',
        'team2', 'world_rank_team2','team2_players_rating','Map_success_index_team2','Map_success_index_round_team2','head_to_head_team2','TPI2','TPI2_map',
        'winner',
        ])
    
    return main_data
 
 
    
def export_to_csv(dataframe, typeframe):
    #typeframe is any string
    try:
        dataframe.to_csv('dataframe_{}_{}.csv'.format(typeframe,str(time.time())[10:]), index = False, header=True)
        print('Complite')
    except:
        print('Cant export to csv {}'.format(typeframe))
def add_to_csv():
    for team in teams:
        for csmap in maps:
            get_team_map_stat(team,csmap)
                
 
#main
 
#initialization teams
Spirit = Team('https://www.hltv.org/team/7020/spirit')
 
#list teams
#, Sprout, Spirit, Ence, thieves,Mousesports,
#GenG,Chaos,C9,MadLions,Forze,North,Gambit,VP,Espada
teams=[Spirit]
#hltv raiting
 
# hltv_raiting_href = [
#     '2020/january/27',
#     '2020/february/24',
#     '2020/march/30',
#     '2020/april/27',
#     '2020/may/25',
#     '2020/june/29',
#     '2020/july/27',
#     '2020/august/31',
#     '2020/september/21',
#     '2019/december/30',
#     '2019/november/25',
#     '2019/october/28',
#     '2019/september/30',
#     '2019/august/26',
#     '2019/july/29',
#     '2019/june/24',
#     '2019/may/27',
#     '2019/april/29',
# ]    
# hltv_raiting = [
#     ['2020/january/27', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[0])).findAll('div', {'class':'ranking-header'})],
#     ['2020/february/24', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[1])).findAll('div', {'class':'ranking-header'})],
#     ['2020/march/30', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[2])).findAll('div', {'class':'ranking-header'})],
#     ['2020/april/27', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[3])).findAll('div', {'class':'ranking-header'})],
#     ['2020/may/25', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[4])).findAll('div', {'class':'ranking-header'})],
#     ['2020/june/29', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[5])).findAll('div', {'class':'ranking-header'})],
#     ['2020/july/27', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[6])).findAll('div', {'class':'ranking-header'})],
#     ['2020/august/31', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[7])).findAll('div', {'class':'ranking-header'})],
#     ['2020/september/21', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[8])).findAll('div', {'class':'ranking-header'})],
#     ['2019/december/30', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[9])).findAll('div', {'class':'ranking-header'})],
#     ['2019/november/25', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[10])).findAll('div', {'class':'ranking-header'})],
#     ['2019/october/28', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[11])).findAll('div', {'class':'ranking-header'})],
#     ['2019/september/30', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[12])).findAll('div', {'class':'ranking-header'})],
#     ['2019/august/26', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[13])).findAll('div', {'class':'ranking-header'})],
#     ['2019/july/29', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[14])).findAll('div', {'class':'ranking-header'})],
#     ['2019/june/24', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[15])).findAll('div', {'class':'ranking-header'})],
#     ['2019/may/27', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[16])).findAll('div', {'class':'ranking-header'})],
#     ['2019/april/29', parsing_html_code('https://www.hltv.org/ranking/teams/{}'.format(hltv_raiting_href[17])).findAll('div', {'class':'ranking-header'})],
# ]            
 
 
#initialization maps
Dust2 = ['de_dust2', 31]
Inferno = ['de_inferno',33]
Mirage = ['de_mirage',32]
Nuke = ['de_nuke',34]
Overpass = ['de_overpass', 40]
Train = ['de_train', 35]
Vertigo = ['de_vertigo',46]
 
#list maps
 
#maps = [Dust2,Inferno,Mirage,Nuke,Overpass,Train,Vertigo]
 
maps = [Dust2, Inferno,Mirage, Nuke, Overpass, Train, Vertigo]
#print(get_team_map_stat(Vitality,Dust2))
#print(create_DataFrame_map())
 
#export_to_csv(create_DataFrame_map(), 'maps')
add_to_csv()
