"""Contains functions for getting and storing data MongoDB"""

import pymongo
from bson.objectid import ObjectId
from datetime import datetime

def create_trainer(code, name="", when=datetime.now(), location=""):
	"""creates document with trainer info"""
	db = pymongo.MongoClient().pokeflask
	db.trainers.insert_one({"name": name, "code": code, "when": when, "location": location})

def get_trainers(limit=50):
	"""returns list of dicts"""
	db = pymongo.MongoClient().pokeflask
	trainers = list(db.trainers.find({}).sort("_id", pymongo.DESCENDING).limit(limit))
	return trainers

def get_trainers_belowid(id=None, limit=50):
	"""returns list of dicts with records with lower id the id passed as argument"""
	db = pymongo.MongoClient().pokeflask
	if not id:
		return get_trainers(limit=limit)

	return list(db.trainers.find({"_id": {"$lt": ObjectId(id)}}).sort("_id", pymongo.DESCENDING).limit(limit))

def get_trainer(code):
	"""returns record by code"""
	db = pymongo.MongoClient().pokeflask
	return db.trainers.find({"code": code})

def exists_trainer(code):
	"""Check if record with this code already exits"""
	if get_trainer(code):
		return True
	return False