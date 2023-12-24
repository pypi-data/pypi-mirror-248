"""
    Web scraping application for grabbing NBA data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from utils import get_game_suffix, get_table_headers
except:
    from bballRefWebScraper.utils import get_game_suffix, get_table_headers

def get_standings(year: int) -> pd.DataFrame:
    """
    Get the standings for a conference in a given year
    Args:
        year (int): the year you want data from
    """

    def get_data_from_table(table):
        data = []
        table_body = table.find('tbody')
        for row in table_body.find_all('tr'):
            row_data = []
            # get team name out of link from first col
            row_data.append(row.find('th').find('a').get_text())
            for td in row.find_all('td'):
                row_data.append(td.get_text())
            data.append(row_data)
        return data

    r = get(f'https://www.basketball-reference.com/leagues/NBA_{year}_standings.html')

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        # if conference.lower() == 'eastern':
        e_table = soup.find(id='confs_standings_E')
        e_headers = get_table_headers(e_table)
        e_data = get_data_from_table(e_table)
        e_df = pd.DataFrame(e_data, columns=e_headers)

        # elif conference.lower() == 'western':
        w_table = soup.find(id='confs_standings_W')
        w_headers = get_table_headers(w_table)
        w_data = get_data_from_table(w_table)
        w_df = pd.DataFrame(w_data, columns=w_headers)

        ret_df = pd.concat([e_df, w_df], axis=1)
        return ret_df
    else:
        raise ValueError("Invalid year")

def get_box_scores(date, team1, team2, period='GAME', stat_type='BASIC') -> dict:
    """
    Get the box scores for a given game between two teams on a given date.

    Args:
        date (str): The date of the game in 'YYYY-MM-DD' format.
        team1 (str): 3-letter abbreviation of the first team.
        team2 (str): 3-letter abbreviation of the second team.
        period (str, optional): The period of the game to retrieve stats for. Defaults to 'GAME'.
        stat_type (str, optional): The type of stats to retrieve. Must be 'BASIC' or 'ADVANCED'. Defaults to 'BASIC'.

    Returns:
        dict: A dictionary containing the box scores for both teams.
    """
    if stat_type not in ['BASIC', 'ADVANCED']:
        raise ValueError('stat_type must be "BASIC" or "ADVANCED"')
    date = pd.to_datetime(date)
    # get game data from games table for provided date
    suffix = get_game_suffix(date, team1, team2)
    box_score_url="https://www.basketball-reference.com"+suffix
    print(box_score_url)
    response = get(box_score_url)
    dfs = []
    if stat_type == 'BASIC':
        table_selector_ids={
            team1:f"box-{team1}-game-basic",
            team2:f"box-{team2}-game-basic",
        }
    elif stat_type == 'ADVANCED':
        table_selector_ids={
            team1:f"box-{team1}-game-advanced",
            team2:f"box-{team2}-game-advanced"
        }

    if response.status_code==200:
        for team,selector_id in table_selector_ids.items():
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table',id=selector_id)
            headers = []
            table_head = table.find('thead')
            headers_row = table_head.find('tr', class_=None)
            for row in headers_row:
                headers.append(row.get_text())
            while 1:
                if '\n' in headers:
                    headers.remove('\n')
                else:
                    break
            print(headers)
            body = table.find('tbody')
            data = []
            for row in body.find_all('tr', class_=lambda x: x != 'thead'):
                row_data = []
                row_data.append(row.find('th').find('a').get_text()) # player name
                for td in row.find_all('td'):
                    row_data.append(td.get_text())
                data.append(row_data)
            df = pd.DataFrame(data, columns=headers)
            dfs.append(df)
        return {team1: dfs[0], team2: dfs[1]}
    else:
        raise Exception(f"Response status code: {response.status_code}")
