import os

class Parser():
    def __init__(self):
        offline_data = {}
        rootdir = os.getcwd() + "/xml_logs/"
        for directory in os.listdir(rootdir):
            user = os.path.join(rootdir, directory)
            if os.path.isdir(user):
                for 

parser = Parser()