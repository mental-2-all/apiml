from flask import Flask, request, jsonify
from utils import *
from transformers import AutoModelForSequenceClassification, pipeline


app = Flask(__name__)


@app.route("/tests", methods=["POST"])
async def test():
    key = request.json.get("id")
    # insertMsg(
    #     key,
    #     {
    #         "content": "Annie is already a captain",
    #         "emotion": [{"label": "joy", "score": 0.7924253940582275}],
    #         "sentiment": [{"label": "NEU", "score": 0.9031711220741272}],
    #     },
    # )
    # doc = getMeAUsersMsgList(key)
    # print(doc)

    d = readData()

    for key in d.keys():
        # msgs = d[key]
        # setMsgs(key, msgs)
        print(key)

    # pred = readPred(key)
    # print(pred)
    # doc = getMeAUsersMsgList(key)

    # for ls in lst:
    #     print(ls)
    # j = readData()
    # writeAllUsers(j)
    # users = readAllUsers()
    # print(users)

    return jsonify({"code": 200})


@app.route("/chonky_pred", methods=["POST"])
async def chonkpred():
    data = request.json

    key = data.get("id")
    msgs = getMeAUsersMsgList(key)
    if len(msgs) == 0:
        return jsonify({"status": 400, "msg": "msgs len is 0", "code": 169})

    count = len(msgs)
    index = 0
    for msg in msgs:
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

    predd = index / count
    setPred(key, predd)
    # print(f"pred: {predd}")

    return jsonify({"status": 200, "msg": "success", "pred": predd})


@app.route("/pred", methods=["POST"])
async def pred():
    data = request.json
    key = data.get("id")
    pred = readPred(key)
    return jsonify({"status": 200, "msg": "success", "pred": pred})


@app.route("/data_and_pred", methods=["POST"])
async def data():
    user_data = request.json

    key = user_data["id"]
    user_data.pop("user")
    user_data.pop("id")
    content = user_data.get("content")

    copy_dict = dict(user_data)

    model_name = "jitesh/emotion-english"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline("text-classification", model=model, tokenizer=model_name)
    prediction = classifier(content)
    copy_dict["emotion"] = prediction

    model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=model_name)
    prediction = classifier(content)

    copy_dict["sentiment"] = prediction

    msgs = getMeAUsersMsgList(key)

    count = len(msgs) + 1
    index = readPred(key)
    idx = getPred(copy_dict, index)

    insertMsg(key, copy_dict)
    setPred(key, str(idx / count))

    return jsonify({"code": 200})


@app.route("/")
def main():
    return "hihihihihi"


# Running the app
if __name__ == "__main__":
    app.run(debug=True, port="6969")
