from pymongo import MongoClient

MC = MongoClient(host='127.0.0.1', port=27017)

mongo = MC['test2']

users = mongo.users.find({'name': 'henry'})
print(users)
for user in users:
    print(user)
