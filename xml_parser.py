import os
import xml.etree.ElementTree as ET

class Parser():
    def __init__(self):
        self.offline_data = {}
        rootdir = os.getcwd() + "/xml_logs/"
        for directory in os.listdir(rootdir):
            user = os.path.join(rootdir, directory)
            userName = user.split("/")[-1]
            if os.path.isdir(user):
                self.offline_data[userName] = {}
                for speed in os.listdir(user):
                    self.offline_data[userName][speed] = {}
                    for fileName in os.listdir(user + "/" + speed):
                        gestureName = self.getCleanedFileName(fileName)
                        if gestureName in self.offline_data[userName][speed]:
                            self.offline_data[userName][speed][gestureName].append(self.getCoordinatesFromXML(user + "/" + speed + "/" + fileName))
                        else:
                            self.offline_data[userName][speed][gestureName] = []
                            self.offline_data[userName][speed][gestureName].append(self.getCoordinatesFromXML(user + "/" + speed + "/" + fileName))
    
    def getCoordinatesFromXML(self, fileLocation):
        points = []
        root = ET.parse(fileLocation).getroot()
        for child in root:
            points.append([int(child.attrib['X']), int(child.attrib['Y'])])
        return points
    
    def getCleanedFileName(self, fileName):
        fileName = fileName.replace(".xml", "")
        res = "".join(filter(lambda x: not x.isdigit(), fileName))
        return res

    def getOfflineData(self):
        return self.offline_data