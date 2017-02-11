#install needed libraries
#pip install html5lib
#pip install lxml
#pip install cssselect
#pip install requests

#import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib as url
import lxml.html
from lxml.cssselect import CSSSelector
import requests

#function to pull fantasy football data from ESPN site
def pull_weeks(week):

    #define url to grab game scores
    ff_url="http://games.espn.com/ffl/scoreboard?leagueId=493801&matchupPeriodId="
    ff_url = ff_url+str(week)

    #pull html and build tree
    r = requests.get(ff_url)
    tree = lxml.html.fromstring(r.text)

    #grab full team names
    team_selector = CSSSelector('td.team')
    all_teams = team_selector(tree)
    all_teams[3].text_content()
    teams = [teams.text_content() for teams in all_teams]

    #grab scores
    score_selector = CSSSelector('td.score')
    all_scores = score_selector(tree)
    all_scores[0].text_content()
    scores = [scores.text_content() for scores in all_scores]

    #grab team abbreviations
    abbrev_selector = CSSSelector('td.abbrev')
    all_abbrevs = abbrev_selector(tree)
    all_abbrevs[2].text_content()
    abbrevs = [abbrevs.text_content() for abbrevs in all_abbrevs]

    #create week and game data sets and merge with teams and scores
    pd_week = pd.DataFrame(np.repeat(week,10))
    pd_game = pd.Series([1,1,2,2,3,3,4,4,5,5])
    pd_abbrev = pd.DataFrame(abbrevs)
    pd_score = pd.DataFrame(scores)
    abbrev_score = pd.concat([pd_week,pd_game,pd_abbrev,pd_score],axis=1)
    abbrev_score.columns = ['week','game','team','score']
    abbrev_score["score"] = abbrev_score["score"].astype(int)
    return abbrev_score

#ENTER WEEK NUMBER
weeknum = 8
week_list = list(range(1,weeknum + 1))

for w in week_list:
    if w == 1:
        all_weeks = pull_weeks(w)
    else:
        all_weeks2 = pull_weeks(w)
        all_weeks = pd.concat([all_weeks,all_weeks2])

#Calc average and max by game and append to score data
week_game_group = all_weeks.groupby(['week','game']).agg({'score' : {'max_score':np.max, 'mean_score':np.mean }})
week_game_group.reset_index(inplace=True)
week_game_group.columns = ['week','game','avg_score','max_score']
all_weeks_week_game_group = pd.merge(all_weeks,week_game_group,how='inner',on=['week','game'])

#Calc win/loss/tie
a=all_weeks_week_game_group
a['win']=0
a['loss']=0
a['tie']=0
a.ix[a.avg_score==a.max_score,'tie'] = 1
a.ix[a.score < a.max_score,'loss'] = 1
a.ix[a.loss+a.tie == 0, 'win'] = 1