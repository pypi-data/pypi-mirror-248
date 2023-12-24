"""
    Web scraping application for grabbing NBA player data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from utils import get_table_headers
except:
    from bballRefWebScraper.utils import get_table_headers

def get_player_stats(player: str) -> pd.DataFrame:
    """
    Args:
        player (str): player whos stats are returned
    Returns:
        player_stats_df (pd.DataFrame): player career stats as a DataFrame
    """
    names = player.split()
    first_name = names[0].lower() if names else ""
    last_name = " ".join(names[1:]) if len(names) > 1 else ""
    if len(last_name) <= 5:
        last_name = last_name[:].lower()
    else:
        last_name = last_name[:5].lower()
    last_name_first_initial = last_name[0]
    first_name_first_two_letters = first_name[:2]
    r = get(f'https://www.basketball-reference.com/players/{last_name_first_initial}/{last_name}{first_name_first_two_letters}01.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', id='per_game')
        headers = get_table_headers(table)
        body = table.find('tbody')
        data = []
        for row in body.find_all('tr'):
            row_data = []
            row_data.append(row.find('th').find('a').get_text())
            for td in row.find_all('td'):
                row_data.append(td.get_text())
            data.append(row_data)
        player_stats_df = pd.DataFrame(data, columns=headers)
        return player_stats_df
