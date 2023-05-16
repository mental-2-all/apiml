import json
import pymongo
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import re

load_dotenv()


def giveClient() -> pymongo.MongoClient:
    key = os.getenv("mongo")
    uri = f"mongodb+srv://eddietang2314:{key}@cluster0.tv3utvy.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    # try:
    #     client.admin.command("ping")
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)
    return client


"""
def uploadStudentFormData(data):
   
    db = CLIENT.Students
    collection = db.get_collection(DB_FORM_CLUSTER_NAME)
    col = collection
    x = col.insert_one(data)"""


def insertMsg(idd, msg_dict):
    c = giveClient()
    db = c.V1
    collection = db.get_collection("msgs")
    collection.update_one(
        {"_id": str(idd) + "123456"},
        {"$push": {"msgs": msg_dict}},
        upsert=True,
    )


def setMsgs(idd, msgs_dict):
    c = giveClient()
    db = c.V1
    collection = db.get_collection("msgs")
    collection.update_one(
        {"_id": str(idd) + "123456"},
        {"$push": msgs_dict},
        upsert=True,
    )


def getMeAUsersMsgList(idd):
    c = giveClient()
    db = c.V1
    collection = db.get_collection("msgs")
    document = collection.find_one({"_id": str(idd) + "123456"})
    if document is None:
        return []
    else:
        return document["msgs"][0]


def setPred(idd, pred):
    c = giveClient()
    db = c.V1
    collection = db.get_collection("users")
    doc = collection.find_one({"_id": str(idd) + "123456"})
    if doc is None:
        doc = {}
    doc["pred"] = pred
    collection.update_one(
        {"_id": str(idd) + "123456"},
        {"$set": doc},
        upsert=True,
    )


def readPred(idd) -> float:
    c = giveClient()
    db = c.V1
    collection = db.get_collection("users")
    doc = collection.find_one({"_id": str(idd) + "123456"})
    if doc is not None:
        return float(doc["pred"])
    else:
        return 0.0


def getPred(msg, idx):
    index = idx
    emotions = {
        "anger": -0.7,
        "cheeky": 0.2,
        "confuse": 0.2,
        "curious": 0.5,
        "disgust": -0.6,
        "empathetic": 0.8,
        "energetic": 0.9,
        "fear": -0.9,
        "grumpy": -1,
        "guilty": -0.7,
        "impatient": -0.6,
        "joy": 1,
        "love": 1,
        "neutral": 0,
        "sadness": -1,
        "serious": 0.2,
        "surprise": 0.2,
        "suspicious": 0.2,
        "think": 0.2,
        "whiny": 0.2,
    }

    regex_string = r"\b(kill|harm|suicide|bomb|fuck|dead|sad|hate)\b"
    sent = msg["sentiment"][0]["label"]
    if sent == "POS":
        index += 1 * float(msg["sentiment"][0]["score"])
    elif sent == "NEG":
        match = re.search(regex_string, msg["content"])
        if match:
            index += -3 * float(msg["sentiment"][0]["score"])
        else:
            index += -1 * float(msg["sentiment"][0]["score"])

    else:
        index += 0

    em_modify = emotions[msg["emotion"][0]["label"]]
    score_em = float(msg["emotion"][0]["score"])

    index += score_em * em_modify
    return index


def readData():
    with open("data.json", "r") as openfile:
        json_object = json.load(openfile)
        return json_object
