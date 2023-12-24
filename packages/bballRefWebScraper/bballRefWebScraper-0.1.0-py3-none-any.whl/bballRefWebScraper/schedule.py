"""
    Web scraping application for grabbing NBA team schedule data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def get_schedule(team: str, year: str) -> pd.DataFrame:
    """
    Args:
        team (str): team name to search for schedule
        year (str): schedule year to search for
    Returns:
        df (pd.DataFrame): schedule Dataframe
    """
    r = get(f'https://www.basketball-reference.com/teams/{team.upper()}/{year}_games.html')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        headers = []
        t_head = table.find('thead')
        header_row = t_head.find('tr')
        for th in header_row.find_all('th'):
            headers.append(th.get_text())
        data = []
        body = table.find('tbody')
        for row in body.find_all('tr', class_=lambda x: x != 'thead'):
            row_data = []
            row_data.append(row.find('th').get_text())
            for item in row.find_all('td'):
                row_data.append(item.get_text())
            data.append(row_data)
        df = pd.DataFrame(data, columns=headers)
        df.columns.values[4] = "Box Score"
        df.columns.values[5] = "@"
        df.columns.values[7] = "W/L"
        df.columns.values[8] = "OT?"
        print(df.columns.values)
        return df
