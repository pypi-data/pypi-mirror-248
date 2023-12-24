"""
    Collection of functions used to scrape mvp tracker data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from unidecode import unidecode

try:
    from utils import get_table_headers
except:
    from bballRefWebScraper.utils import get_table_headers

def get_mvp_tracker():
    """
    Returns a df of the bb-ref nba MVP tracker
    """
    r = get('https://www.basketball-reference.com/friv/mvp.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')

        headers = get_table_headers(table)

        data = []
        table_body = table.find('tbody')
        for row in table_body.find_all('tr'):
            row_data = []
            # get team name out of link from first col
            row_data.append(row.find('th').get_text())
            for td in row.find_all('td'):
                row_data.append(td.get_text())
            data.append(row_data)
        mvp_df = pd.DataFrame(data, columns=headers)
        return mvp_df

def get_mvp_percent(player_name: str) -> str:
    """
    Args:
        player_name (str): name of the player whos odds of winning mvp you want to see
    Returns:
        probability (str): current probability of player winning mvp according to bball ref
    """
    mvp_df = get_mvp_tracker()
    # remove accents from player name to allow filtering
    mvp_df['Player'] = mvp_df['Player'].apply(unidecode)
    filtered_df = mvp_df[mvp_df['Player'] == player_name]
    # check if player is in top 10 table
    if len(filtered_df) < 1:
        raise RuntimeError('Player not currently in top 10 of NBA MVP race')
    player_prob = filtered_df.at[filtered_df.index[0], 'Prob%']
    return f'{player_name} has a {player_prob} chance of winning mvp!'
