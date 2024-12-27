try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import requests
import pathlib
import os

class Parser():
    def __init__(self):
        '''
        Class for resolve parser of Hermitage museum painting
        '''
        # Init pathes for parser
        self.raw_path = pathlib.Path(__file__).parent.resolve()/'..'/'..'/'data'/'raw'
        self.wiki_page = 'https://www.wikidata.org/wiki/Wikidata:WikiProject_sum_of_all_paintings/Collection/Hermitage_Museum'
        self.parsed_path = pathlib.Path(__file__).parent.resolve()/'../../data'/'parsed'
        
    def get_wiki_page(self):
        '''
        Function for get last wiki page version
        '''
        res = requests.get(self.wiki_page) # get page
        if os.path.exists(self.raw_path/'wikidata.html'):
            print('Wikidata file already exists! Delete them and continue') # if data exist - remove them with new data
            os.remove(self.raw_path/'wikidata.html')
        if res.ok:
            print('GET request successful! Write in file')
            with open(self.raw_path/'wikidata.html', 'w+', encoding='utf8') as f:
                f.write(res.text) # write content of page
        else:
            raise Exception('GET request failed! Request result: '+res.content)

    def parse(self):
        '''
        Main function of the class. Resolve parse of wikidata
        '''
        self.get_wiki_page() # get HTML file
        print("reading file...")
        with open(self.raw_path/'wikidata.html', 'r', encoding='utf8') as file:
            html = file.read()
        if os.path.exists(self.parsed_path/'parsed.tsv'):
            print('Find old parsed data. Delete them!')
            os.remove(self.parsed_path/'parsed.tsv')
        out = open(self.parsed_path/'parsed.tsv', 'w', encoding='utf8') # init file to write results
        print("parsing html...")
        parsed_html = BeautifulSoup(html, 'html.parser') # init parser library
        print("parsing data...")
        for tr in parsed_html.body.find_all('tr'):
            td_idx = -1
            image = None
            label = None
            creator = None
            for td in tr.find_all('td'):
                td_idx += 1
                
                if td_idx == 0: #image
                    for img in td.find_all("img"):
                        image = img['src']
                if td_idx == 1: #label
                    label = td.get_text().strip()
                if td_idx == 3: #creator
                    creator = td.get_text().strip()
            
            if image != None and label != None and creator != None:
                out.write(image + "\t" + label + "\t" + creator + "\n")

            # <figure class="mw-halign-center"

        out.flush()
        out.close()







