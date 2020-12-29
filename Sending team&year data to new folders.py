teams = ['Baltimore Orioles', 'Boston Red Sox', 'New York Yankees', 'Tampa Bay Rays', 'Toronto Blue Jays',
         'Chicago White Sox', 'Cleveland Indians', 'Detroit Tigers', 'Kansas City Royals', 'Minnesota Twins',
         'Houston Astros', 'Los Angeles Angles', 'Oakland Athletics', 'Seattle Mariners', 'Texas Rangers',
         'Atlanta Braves', 'Miami Marlins', 'New York Mets', 'Philadelphia Phillies', 'Washington Nationals',
         'Chicago Cubs', 'Cincinnati Reds', 'Milwaukee Brewers', 'Pittsburgh Pirates', 'St.Louis Cardinals',
         'Arizona Diamondbacks', 'Colorado Rockies', 'Los Angeles Dodgers', 'San Diego Padres', 'San Francisco Giants']

import os
import csv
import pandas as pd

year = 2006
while year <= 2020:

    df = pd.read_csv('C:\\Users\\61437\\Documents\\PythonProgramming\\MLB-Analysis\\MLB Season results&odds\\MLB_2006-2020 regular season results\\MLB_' + str(year) + 'regularseason_results&odds.csv')

    path = 'C:\\Users\\61437\\Documents\\PythonProgramming\\MLB-Analysis\\MLB Season results&odds\\' + str(year) + ' MLB regular season'
    os.chdir(path) # changes current directory (folder) to new path/directory

    for team in teams:

        with open('MLB_' + str(year) +' regular season - ' + team + '.csv', 'w') as new_file:

            csv_writer = csv.writer(new_file, delimiter = ',')
            csv_writer.writerow(['date', 'team 1', 'team 2', 'team 1 score', 'team 2 score', 'team 1 win', 'team 2 win'])
            # Note: row[1] = date, row[2] = team 1, row[3] = team 2, row[4] = team 1 score, row[5] = team 2 score,
            #       row[6] = team 1 win, row[7] = team 2 win
            for row in df.itertuples():
                if row[2] == team:
                    csv_writer.writerow(row[1:])
                if row[3] == team:
                    # Adjusting row to ensure file team game data always on LHS
                    date = row[1]
                    team1 = row[3]
                    team2 = row[2]
                    team1score = row[5]
                    team2score = row[4]
                    team1win = row[7]
                    team2win = row[6]
                    csv_writer.writerow([date, team1, team2, team1score, team2score, team1win, team2win])
    year += 1
