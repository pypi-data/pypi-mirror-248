"""
    Web scraping application for grabbing NBA draft class data
    from https://www.basketball-reference.com/
"""
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def get_draft_class(year):
    """
    Args:
        year (int): year of the draft class to retrieve
    Returns:
        df (DataFrame): DataFrame containing draft class information for a given year
    """
    r = get(f'https://www.basketball-reference.com/draft/NBA_{year}.html')
    df = None

    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')

        headers = []
        t_head = table.find('thead')
        table_headers = t_head.find('tr', class_=False)
        for header in table_headers.find_all('th'):
            headers.append(header.get_text())
        headers.remove(headers[0])
        # ['Pk', 'Tm', 'Player', 'College', 'Yrs', 'G', 'MP', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%', 'MP', 'PTS', 'TRB', 'AST', 'WS', 'WS/48', 'BPM', 'VORP']

        data = []
        table_body = table.find('tbody')
        for row in table_body.find_all('tr'):
            row_data = []
            for td in row.find_all('td'):
                row_data.append(td.get_text())
            data.append(row_data)
        df = pd.DataFrame(data, columns=headers)
        return df
    else:
        raise RuntimeError("Draft year not found")
