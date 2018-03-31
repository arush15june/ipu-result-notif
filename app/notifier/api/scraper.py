from notifier.settings import RESULTS_URI, ROOT_RESULTS_URL

import requests
from bs4 import BeautifulSoup

class ResultScraper():
    def __init__(self, scrape_url):
        self.soup = None
        self.results = []
        self.url = scrape_url

    def __repr__(self):
        return "<ResultScraper URL: {}".format(self.url)
        
    def _fetch(self):
        req = requests.get(self.url)
        assert req.status_code == 200, "Results Is Not Up, Code:{}".format(req.status_code)
        try:
            self.soup = BeautifulSoup(req.text, 'html.parser')
        except:
            print("Soup couldn't be prepared")

    def _fill_results(self):
        assert self.soup is not None, "Soup isn't prepared"
        
        self.results = []
        
        table = self.soup.table
        rows = table.find_all('tr')
        
        for result in rows:
            """ first <td> contains title of row, second <td> contains date """
            result_raw_data = result.find_all('td')

            if len(result_raw_data) == 0:
                continue

            """ If title is not present """
            if result_raw_data[0] is None:
                continue

            result_data = {
                'text': result_raw_data[0].a.string.strip().replace('\n', '').replace('\r','').replace('\t',''), 
                'href': ROOT_RESULTS_URL+result_raw_data[0].a['href'] if result_raw_data[0].a['href'] else None, 
                'date': result_raw_data[1].string if result_raw_data[1].string else None
            }
            
            self.results.append(result_data)
                    
    def scrape(self):
        self._fetch()
        self._fill_results()
    
