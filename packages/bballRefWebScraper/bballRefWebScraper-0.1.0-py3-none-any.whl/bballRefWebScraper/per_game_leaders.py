"""
    Web scraping application for grabbing NBA per game leader data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def get_per_game_leaders_szn(stat: str) -> pd.DataFrame:
    """
    Args:
        stat (str): Ex) Pts, Ast, Trb, Stl, Blk
    Returns:
        df (pd.DataFrame): df containing top per game szns of NBA players for given stat
    """
    r = get(f'https://www.basketball-reference.com/leaders/{stat.lower()}_per_g_season.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='stats_table')
        headers = []
        t_head = table.find('thead')
        header_row = t_head.find('tr')
        for th in header_row.find_all('th'):
            headers.append(th.get_text())
        body = table.find('tbody')
        data = []
        for row in body.find_all('tr', class_=lambda x: x != 'thead'):
            row_data = []
            for td in row.find_all('td'):
                try:
                    row_data.append(td.find('a').get_text())
                except:
                    row_data.append(td.get_text())
            data.append(row_data)
        df = pd.DataFrame(data, columns=headers)
        return df
    else:
        raise ValueError("Invalid stat type")
