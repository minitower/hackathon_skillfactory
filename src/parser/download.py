import csv
import pathlib
import urllib.request

class Downloader:
    def __init__(self):
        '''
        Class for download images from parsed data
        '''
        self.idx = 0
        self.path = pathlib.Path(__file__).parent/'..'/'..'
        self.path = self.path.resolve()
        self.image_path = self.path/'data'/'images'

    def download(self):
        '''
        Function for 
        '''
        out = open(self.path/'data'/'parsed'/'final.tsv', 'w', encoding='utf8')

        with open(self.path/'data'/'parsed'/'parsed.tsv', newline='') as csvfile:
            rdr = csv.reader(csvfile, delimiter='\t')
            for row in rdr:
                remote = row[0].replace('/thumb', '')
                remote = '/'.join(remote.split('/')[:-1])
                url = "https:" + remote
                filename = self.image_path / (str(self.idx) + "." + row[0].split('.')[-1])
                print ("downloading image #" + str(self.idx) + "...")
                
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Smikler/89.0'), ('Api-User-Agent', 'Smikler/89.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, filename)
                
                self.idx += 1
                out.write(str(filename) + "\t" + row[1] + "\t" + row[2] + "\n")
                
        out.flush()
        out.close()
#idx = 0
#path = pathlib.Path(__file__).parent.resolve()


