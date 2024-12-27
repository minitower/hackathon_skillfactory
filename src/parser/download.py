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
        Function for download image from parsed file of WikiData
        '''
        out = open(self.path/'data'/'parsed'/'final.csv', 'w', encoding='utf8') # open file to final result

        with open(self.path/'data'/'parsed'/'parsed.tsv', newline='') as csvfile: # open parsed data
            rdr = csv.reader(csvfile, delimiter='\t') # read data
            for row in rdr:
                remote = row[0].replace('/thumb', '') # replace thumb files to sourse
                remote = '/'.join(remote.split('/')[:-1])
                url = "https:" + remote
                filename = self.image_path / (str(self.idx) + "." + row[0].split('.')[-1]) # init unique path
                print ("downloading image #" + str(self.idx) + "...")
                
                opener = urllib.request.build_opener() # build server for requests
                opener.addheaders = [('User-agent', 'Smikler/89.0'), ('Api-User-Agent', 'Smikler/89.0')] # add User-Agent
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, filename) # save file
                
                self.idx += 1
                out.write(str(self.idx) + "," + row[1].replace(',', ';') + "," + row[2].replace(',', ';') + "\n") # save ID of image and description
                
        out.flush()
        out.close() # close file


