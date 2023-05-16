# from flask import Flask, request, jsonify
# import json
# from utils import *

# # import pandas as pd
# # import joblib
# import openai
# from transformers import AutoModelForSequenceClassification, pipeline
# from connect import giveAClient, sendemail
# import os
# from dotenv import load_dotenv
# import re

# load_dotenv()


# api_key = os.getenv("OPENAI")
# openai.my_api_key = api_key


# # Declare a Flask app
# app = Flask(__name__)


# # @app.route("/flag", methods=["POST"])
# # def flag():
# #     data = request.json
# #     print("flagged call")
# #     key = data["user"]
# #     booll = data["bool"]
# #     rating = data["score"]
# #     red = giveAClient()
# #     red.set(key, json.dumps({"ill": booll, "rate": rating}))
# #     print("flagged")
# #     print({"ill": booll, "rate": rating})

# #     # {
# #     #     key:
# #     #         ill
# #     #         rate

# #     # }

# #     # key + "health"

# #     # {
# #     #     "user":"username",
# #     #     "HEART_RATE":"",
# #     #     "STEPS":"",
# #     #     "SLEEP_IN_BED":"",
# #     #     "SLEEP_AWAKE":"",
# #     #     "RESTING_HEART_RATE":"",

# #     # }

# #     # key + "msgs"
# #     # [{},{},{}]

# #     return jsonify({"status": 200, "msg": "success"})


# @app.route("/pred", methods=["POST"])
# def pred():
#     emotions = {
#         "anger": -0.7,
#         "cheeky": 0.2,
#         "confuse": 0.2,
#         "curious": 0.5,
#         "disgust": -0.6,
#         "empathetic": 0.8,
#         "energetic": 0.9,
#         "fear": -0.9,
#         "grumpy": -1,
#         "guilty": -0.7,
#         "impatient": -0.6,
#         "joy": 1,
#         "love": 1,
#         "neutral": 0,
#         "sadness": -1,
#         "serious": 0.2,
#         "surprise": 0.2,
#         "suspicious": 0.2,
#         "think": 0.2,
#         "whiny": 0.2,
#     }

#     index = 0

#     data = request.json

#     key = data.get("user")
#     red = giveAClient()
#     msgs = red.lrange(key + "msgs", 0, -1)
#     if len(msgs) == 0:
#         return jsonify({"status": 400, "msg": "msgs len is 0"})

#     cleanedString = ""
#     count = 0
#     regex_string = r"\b(kill|harm|suicide|bomb|fuck|dead|sad|hate)\b"
#     for msg in msgs:
#         txt = msg.decode("utf-8")
#         txt_dict = json.loads(txt.replace("'", '"'))

#         sent = txt_dict["sentiment"][0]["label"]
#         if sent == "POS":
#             index += 1 * float(txt_dict["sentiment"][0]["score"])
#         elif sent == "NEG":
#             match = re.search(regex_string, txt_dict["content"])
#             if match:
#                 index += -3 * float(txt_dict["sentiment"][0]["score"])
#             else:
#                 index += -1 * float(txt_dict["sentiment"][0]["score"])

#         else:
#             index += 0

#         em_modify = emotions[txt_dict["emotion"][0]["label"]]
#         score_em = float(txt_dict["emotion"][0]["score"])
#         index += score_em * em_modify

#         cleanedString += txt + "\n"
#         count += 1

#     health = red.get(key + "healthkit")
#     if health is None:
#         return jsonify({"status": 400, "msg": "health is none"})

#     # print(health)
#     health = health.decode("utf-8")

#     avgHRidx = health.find(": ")
#     avgHRidxEnd = health.find(",")
#     avgHr = int(health[avgHRidx + 2 : avgHRidxEnd].split(".")[0])
#     # print(avgHr)
#     health = health[avgHRidxEnd + 2 : len(health)]

#     restHRidx = health.find(": ")
#     restHRidxEnd = health.find(",")
#     restHr = float(health[restHRidx + 2 : restHRidxEnd])
#     # print(restHr)
#     health = health[restHRidxEnd + 2 : len(health)]

#     sleepidx = health.find(": ")
#     sleepEnd = health.find(",")
#     sleep = float(health[sleepidx + 2 : sleepEnd])
#     # print(sleep)
#     health = health[sleepEnd + 2 : len(health)]

#     idx = health.find(": ")
#     end = health.find("}")
#     exercise = float(health[idx + 2 : end])
#     # print(ex)

#     if avgHr > restHr:
#         index += ((avgHr - restHr) / 2) * 0.01 * -1
#     else:
#         index += 1

#     if sleep // 60 > 8:
#         index += 1 * 0.7
#     else:
#         index += -1 * 0.7

#     if exercise >= 2:
#         index += 1 * 0.69
#     else:
#         index += -1 * 0.69

#     count += 3

#     return jsonify({"status": 200, "msg": "success", "pred": index / count})


# @app.route("/data", methods=["POST"])
# def data():
#     user_data = request.json

#     key = user_data["user"]
#     user_data.pop("user")
#     content = user_data.get("content")

#     copy_dict = dict(user_data)

#     model_name = "jitesh/emotion-english"
#     model = AutoModelForSequenceClassification.from_pretrained(model_name)
#     classifier = pipeline("text-classification", model=model, tokenizer=model_name)
#     prediction = classifier(content)
#     copy_dict["emotion"] = prediction

#     model_name = "finiteautomata/bertweet-base-sentiment-analysis"
#     model = AutoModelForSequenceClassification.from_pretrained(model_name)
#     classifier = pipeline("sentiment-analysis", model=model, tokenizer=model_name)
#     prediction = classifier(content)

#     copy_dict["sentiment"] = prediction

#     # print(copy_dict)

#     data = readData()
#     if key not in data:
#         data[key] = {"msgs": []}
#     data[key]["msgs"].append(copy_dict)
#     writeData(data)

#     # red = giveAClient()
#     # red.rpush(key + "msgs", json.dumps(copy_dict))
#     # print(red.lrange(key+"msgs", 0, -1))
#     # print(red.ping())

#     # nvm ig just storing the discord ata

#     # process the data do some sentiment analysis.

#     # after sentiment analysis, get emtions

#     # after that, we update teh data dict and send it to redis

#     # call redis function to append data to the user name key from the thing

#     # then read the entire user messages

#     # maybe read the health data from flutter api

#     # then shove everything into a neural network, or like something that will identify trends (maybe a for loop)

#     # then after that, we output the percentage chance that you are mentally ill

#     return jsonify({"code": 200})


# # @app.route("/summarize", methods=["POST"])
# # def summarizeWithGPT():
# #     # given this data in json... please summarize and HIGHLIGHT some texts that are concerning for a mentally ill patient, then, construct a description of the user from this data
# #     # the data is all the redis stuff and the health stuff

# #     # this summary is like a profilio for like the patient, so that the patient can just hand this directly to the therapist.

# #     return jsonify({"result":""})


# @app.route("/")
# def main():
#     return "hihihihihi"


# @app.route("/getData", methods=["POST"])
# def getData():
#     key = request.json["user"]
#     red = giveAClient()
#     msgs = red.lrange(key + "msgs", 0, -1)
#     table = {}
#     emos = []
#     for msg in msgs:
#         txt = msg.decode("utf-8")
#         txt_dict = json.loads(txt.replace("'", '"'))
#         emos.append(txt_dict)

#     print(emos)

#     for emo in emos:
#         emooo = emo["emotion"][0]["label"]
#         if emooo not in table:
#             table[emooo] = 0
#         table[emooo] += 1

#     red.set(key + "emotion", json.dumps(table))
#     return jsonify(table)


# # @app.route("/inform", methods=["POST"])
# # def informTheTherapist():
# #     therapist_data = [
# #         {"email": "eddietang2314@gmail.com", "name": "Eddie Tang"},
# #         {"name": "Ekam :)", "email": "ekamghai74@gmail.com"},
# #     ]
# #     key = request.json["user"]

# #     header = "Ok heres some data, the first line is the index showing how close a user is to being mentally ill, it is between -1 and 1, the closer to -1, the more mentally ill, create a diagnoses in your mind for this data below, which highlights some rather concerning texts in the description of the patient. After you formula a diagnosis, please generate a body for an email that will be sent to a local therapist.\n\n"

# #     red = giveAClient()
# #     msgs = red.lrange(key + "msgs", 0, -1)
# #     if len(msgs) == 0:
# #         return jsonify({"status": 400, "msg": "msgs len is 0"})

# #     cleanedString = ""
# #     for msg in msgs[30 : len(msgs)]:
# #         txt = msg.decode("utf-8")
# #         cleanedString += txt + "\n"

# #     # print(key)
# #     txt = red.get(key).decode("utf-8")
# #     data = json.loads(txt.replace("'", '"'))

# #     rating = data["rate"]

# #     body = str(rating) + "\n" + cleanedString

# #     chat = openai.ChatCompletion.create(
# #         model="gpt-3.5-turbo",
# #         messages=[
# #             {"role": "system", "content": "You are a intelligent docotor/therapist."},
# #             {"role": "user", "content": header + body},
# #         ],
# #     )
# #     reply = str(chat.choices[0].message.content)
# #     idx = reply.find("],")
# #     idxEnd = reply[idx + 1 : len(reply)].lower().find("thank")
# #     print(reply[idx + 2 : idxEnd])

# #     body = reply[idx + 2 : idxEnd]

# #     for doc in therapist_data:
# #         sendemail(doc["email"], body, doc["name"])

# #     # summarize with chatgpt

# #     # therapist data should be a hard coded list from the frontend that has all the therapist locations near by
# #     # [{"email":"asdfdasf", "name": "eddie"}, {},{}]

# #     # please download the app, then like contact them through the virtual chat (it will be in the message sent to the therapists, maybe via emial....)

# #     # idea that just poped up - we need a therapist account, and a user account, cuz like these two will have different permissions, cuz the therapists will need to see which user they have
# #     # (maybe in a lsit builder view), then like click on one and start a messaging conversion.

# #     # maybe include a page/tab in the frontend whihc like has all the converstations a normal user has, and have hte first option be  like with AI
# #     # and then once

# #     # maybe like the chats are stored in db

# #     return jsonify({"code": 200})


# # Running the app
# if __name__ == "__main__":
#     app.run(debug=True, port="6969")
