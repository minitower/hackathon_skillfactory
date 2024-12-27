# CODE FOR INITIALIZE ENVIROMENT
from src.parser.parse import Parser
from src.parser.download import Downloader
from src.autoencoder import Autoencoder


p = Parser()
p.parse()
d = Downloader()
d.download()
e = Autoencoder()
e.preprocess_image()
codes = e.fit_model()
print(codes)