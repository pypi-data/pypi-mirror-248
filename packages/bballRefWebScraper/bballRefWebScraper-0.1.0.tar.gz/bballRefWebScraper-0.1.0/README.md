# Basketball-Reference Web Scraping Application

## Overview

* Grabs basketball data from [Basketball-Reference](https://www.basketball-reference.com/).
* Extracts player stats, game scores, team information, and more via BeautifulSoup.
* Ideal for basketball analytics, data science, and machine learning.

## Usage

### Installation

* Clone down the repository to your local machine using git clone
* Cd into the cloned repository
* Install the requirements with pip install -r requirements.txt

```bash
git clone https://github.com/michaelc143/BballRefWebScraper.git
cd BballRefWebScraper/
pip install -r requirements.txt
```

* There is also a Dockerfile built into this repository that can be used via:

```bash
docker build . -t BballRefScraper
docker run BballRefScraper
```

### Running the Application

* Example functionality can be found in the examples.py file

```bash
cd BballRefWebScraper/
python3 bball_ref_web_scraper/examples.py
```

### Packages Required

* Pandas
* BeautifulSoup
* Unidecode
* Requests
* Pytest
* Pylint
* Coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
