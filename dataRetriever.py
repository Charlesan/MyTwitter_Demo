#coding=utf-8
import pymongo

class DataRetriever(object):
	def __init__(self):
		conn = pymongo.Connection("localhost", 27017)
		self.db = conn["twitterDB"]

	def getUser(self, username):
		userColct = self.db.userSets
		return userColct.find_one({"name" : username})

	def updateTwitter(self, username, newTwitter):
		userColct = self.db.userSets
		userColct.update({"name": username}, {"$set": {"twitters": newTwitter}})