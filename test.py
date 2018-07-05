# -*- coding: utf-8 -*-
from pymongo import MongoClient

client=MongoClient("mongodb://127.0.0.1:27017,127.0.0.1:27021,127.0.0.1:27022",replicaset='rs0')
print(client.python.python.find_one())