import json

class Database():
    def __init__(self):
        self.filename = 'database.json'
        self.data = {}
        self.loadData()

    def loadData(self):
        with open(self.filename, 'r') as file:
            self.data = json.load(file)

    def addUser(self, userId):
        # Delete any user with userID which already exists in database
        if userId in self.data:
            del self.data[userId]
        # Add user to database
        self.data[userId] = {}
        # print(self.data[userId])

    def addGesture(self, userId, gesture, points):
        # print(self.data)
        if gesture not in self.data[userId]:
            print("gesture not in database and user")
            self.data[userId][gesture] = []
        self.data[userId][gesture].append(points)
        self.dumpData()

    def getData(self):
        return self.data

    def clearData(self):
        with open(self.filename, 'w') as file:
            json.dump({}, file)

    def dumpData(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

# database = Database()
# database.loadData()
# database.addUser('user1')
# database.addUser('user2')
# database.addGesture('arrow',[[1,2],[2,3],[3,4],[5,6]], 'user1')
# database.addGesture('star',[[1,6],[2,9],[3,4],[5,6]], 'user1')
# database.addGesture('star',[[5,7],[10,4],[1,7],[2,2]], 'user1')
# database.addGesture('star',[[1,0],[4,4],[5,5],[6,6]], 'user2')
# print(database.getData())
# database.dumpData()
# database.clearData()