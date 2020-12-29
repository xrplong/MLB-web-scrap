from selenium import webdriver
import pandas as pd
import csv

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

year = 2006  # Choose year lower bound
while year <= 2020: # Choose year upper bound
    page = 1
    max_page = 9999
    rows_list = []
    while page <= max_page:
        driver.get('http://www.oddsportal.com/baseball/usa/mlb-' + str(year) + '/results/#/page/' + str(page))

        # Finding max page for current year
        if max_page == 9999:
            pagination = driver.find_element_by_xpath("//div[@id='pagination']")
            pagi_list = []
            for num in pagination.find_elements_by_xpath(".//a"):
                pagi_list.append((num.get_attribute('href'))[-3:-1])
            max_page = int(pagi_list[-1])

        table = driver.find_element_by_xpath("//table[@id='tournamentTable']")

        # Looping through each table row in tournament table for current page
        for row in table.find_elements_by_xpath(".//tr"):
            dict = {'date':'', 'team 1':'', 'team 2':'', 'team 1 score':'', 'team 2 score':'', 'team 1 win':'', 'team 2 win':''}

            # Finding date of current game
            if row.get_attribute('class') == 'center nob-border':
                date = row.text

            # Finding current game teams
            if row.get_attribute('class') in [' deactivate', 'odd deactivate']:
                teams = [td.text for td in row.find_elements_by_xpath(".//td[@class='name table-participant']")]
                if teams != []:
                    teams_ = (str(teams))[2:-2]

                dict['team 1'] = teams_.split(' - ')[0]
                if  teams_.split(' - ')[1][-2:] == 'n ':
                    dict['team 2'] = teams_.split(' - ')[1][:-3]
                else:
                    dict['team 2'] = teams_.split(' - ')[1]

                # Finding current game score
                score = [td.text for td in row.find_elements_by_xpath(".//td[@class='center bold table-odds table-score']")]
                if score != []:
                    if len(str(score)[2:-2].split(':')) != 2:
                         continue
                    dict['team 1 score'] = (str(score)[2:-2].split(':'))[0]
                    dict['team 2 score'] = (str(score)[2:-2].split(':'))[1]

                # Finding current game $odds
                payoff_loser = [td.text for td in row.find_elements_by_xpath(".//td[@class='odds-nowrp']")]
                payoff_winner = [td.text for td in row.find_elements_by_xpath(".//td[@class='result-ok odds-nowrp']")]
                if (payoff_loser != []) and (payoff_winner != []):
                    payoff_left = str(payoff_winner)[2:6]
                    payoff_right = str(payoff_loser)[2:6]
                    if int((str(score)[2:-2].split(':'))[0]) > int((str(score)[2:-2].split(':'))[-1]):
                        dict['team 1 win'] = payoff_left
                        dict['team 2 win'] = payoff_right
                    else:
                        dict['team 1 win'] = payoff_right
                        dict['team 2 win'] = payoff_left
                dict['date'] = (str(date))[0:11]

                # Skipping games not in regular season
                if len(str(date)) != 19:
                    continue

                # Appending current game stats to row_list
                rows_list.insert(0, dict)
        page += 1

    # Data into dataframe
    df = pd.DataFrame(rows_list)

    # Creating csv of data
    df.to_csv('MLB_' + str(year) + 'regularseason_results&odds.csv', index=False)
    year += 1
driver.quit()
