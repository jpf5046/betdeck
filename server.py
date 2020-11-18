from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
app = Flask(__name__)

df = pd.read_csv('current_week_games.csv')
results = pd.read_csv('nfl_2020.csv')
odds = pd.read_csv('week_11_bovada_odds.csv')

@app.route('/teams')
def teams_page():
    temp_df = results.copy()
    list_of_teams = temp_df['team'].unique()
    return render_template('teams.html', list_of_teams=list_of_teams)

@app.route('/teams/<team>')
def team_page(team):
    team_page_df = results.copy()
    team_page_df = team_page_df[team_page_df['team'] == team]

    # o_u_roi
    o_u_roi = team_page_df.sum()['over_payout']
    # spread_roi
    spread_roi = team_page_df.sum()['spread_payout']
    # ml_roi
    ml_roi = team_page_df.sum()['moneyline_payout']
    return render_template('team.html', team=team, 
                            o_u_roi=o_u_roi, spread_roi=spread_roi, 
                            ml_roi=ml_roi)

@app.route('/')
def home_page():
    temp_df = odds.copy()
    list_discriptions = temp_df['game_description'].unique()
    return render_template('index.html', list_discriptions = list_discriptions)


@app.route('/<matchup>')
def matchup_view(matchup):

    
    
    temp_df = odds.copy()
    
    temp_df = temp_df[temp_df['game_description'] == matchup]
    print(temp_df.head())
    temp_df = temp_df.reset_index()
    # team names
    team_1 = temp_df['team'][0]
    team_2 = temp_df['team'][1]
    o_u = temp_df['over_under'][0]

    # vegas implied score
    team_1_vi = temp_df['vegas_implied_score'][0]
    team_2_vi = temp_df['vegas_implied_score'][1]

    # spread
    team_1_sp = temp_df['spread'][0]
    team_2_sp = temp_df['spread'][1]
    # spread price
    team_1_sp_p = temp_df['spread_price'][0]
    team_2_sp_p = temp_df['spread_price'][1]
    # moneyline 
    team_1_ml = temp_df['moneyline'][0]
    team_2_ml = temp_df['moneyline'][1]


    # use team_1/team_2 as fitlers 

    results_df = results.copy()

    results_df_1 = results_df[results_df['team'] == team_1]
    overs_hit_1 = results_df_1.sum()['over_hit']
    beat_spread_1 = results_df_1.sum()['beat_spread']
    beat_ml_1 = results_df_1.sum()['beat_ml']
    vegas_acc_1 = results_df_1.mean()['vegas_accuracy']
    team_1_opp_acc = results_df_1.mean()['opp_vegas_accuracy']
    len_team_1 = len(results_df_1)

    results_df_2 = results_df[results_df['team'] == team_2]
    overs_hit_2 = results_df_2.sum()['over_hit']
    beat_spread_2 = results_df_2.sum()['beat_spread']
    beat_ml_2 = results_df_2.sum()['beat_ml']
    vegas_acc_2 = results_df_2.mean()['vegas_accuracy']
    team_2_opp_acc = results_df_2.mean()['opp_vegas_accuracy']
    len_team_2 = len(results_df_2)

    return render_template('matchup.html', team_1=team_1, team_2=team_2, o_u=o_u,
                             team_1_vi=team_1_vi, team_2_vi=team_2_vi,
                             team_1_sp=team_1_sp, team_2_sp=team_2_sp, 
                             team_1_sp_p=team_1_sp_p, team_2_sp_p=team_2_sp_p, 
                             team_1_ml= team_1_ml, team_2_ml=team_2_ml,
                             len_team_1=len_team_1, len_team_2=len_team_2,
                             overs_hit_1=overs_hit_1, overs_hit_2=overs_hit_2, 
                             beat_spread_1=beat_spread_1, beat_spread_2=beat_spread_2, 
                             beat_ml_1=beat_ml_1, beat_ml_2=beat_ml_2, 
                             vegas_acc_1=vegas_acc_1, vegas_acc_2=vegas_acc_2, 
                             team_1_opp_acc=team_1_opp_acc, team_2_opp_acc=team_2_opp_acc)

def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.divide(val, total)

@app.route('/overs_json')
def overs_json():
    overs = results.copy()

    overs = overs[['over_hit', 'team']]
    overs['over'] = np.where(overs['over_hit'] == 1, 'over', 'under')
    overs = overs[['team', 'over']]
    overs = overs.to_json()
    return jsonify(overs)

